//! Vercingetorix experiment harness: spawns headless 0 A.D. matches and
//! extracts their results into per-match JSON files plus a batch aggregate.
//!
//! One match = one isolated HOME, one `pyrogenesis` process under a `timeout`
//! wrapper, one parsed result. The engine prints one JSON block per player at
//! game end (see `NonVisualTrigger.js`), which is the primary data channel.

#![deny(clippy::all, clippy::pedantic)]

use serde::Serialize;
use std::env;
use std::fs;
use std::io;
use std::path::{Path, PathBuf};
use std::process::{Command, Output};
use std::time::Instant;

const PYROGENESIS: &str = "/usr/games/pyrogenesis";

#[derive(Clone, Copy, PartialEq, Eq)]
struct Seed(u32);

#[derive(Clone, Copy)]
struct Difficulty(u8);

#[derive(Clone, Copy)]
struct TurnCount(u64);

#[derive(Clone, Copy)]
struct WallSeconds(u64);

enum MatchExit {
    Finished,
    TimedOut,
    Failed(i32),
}

impl MatchExit {
    fn as_str(&self) -> String {
        match self {
            Self::Finished => String::from("finished"),
            Self::TimedOut => String::from("timed_out"),
            Self::Failed(code) => format!("failed:{code}"),
        }
    }
}

struct Config {
    tag: String,
    seeds: Vec<Seed>,
    out_dir: PathBuf,
    ai1: String,
    ai2: String,
    difficulty2: Difficulty,
    civ1: String,
    civ2: String,
    bot_mod: Option<String>,
    mod_dir: Option<PathBuf>,
    map: String,
    map_size: u32,
    timeout_secs: u64,
}

#[derive(Debug)]
enum CliError {
    UnknownFlag(String),
    MissingValue(String),
    MissingFlag(String),
    InvalidValue(String),
}

impl std::fmt::Display for CliError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::UnknownFlag(flag) => write!(f, "unknown flag: {flag}"),
            Self::MissingValue(flag) => write!(f, "missing value for {flag}"),
            Self::MissingFlag(flag) => write!(f, "missing required flag {flag}"),
            Self::InvalidValue(detail) => write!(f, "invalid value: {detail}"),
        }
    }
}

/// The 100-line clippy cap is waived here: this is one cohesive parser of a
/// fixed flag set; splitting it into helpers would fragment trivial assignments.
#[allow(clippy::too_many_lines)]
fn parse_args(args: &[String]) -> Result<Config, CliError> {
    let mut tag = None;
    let mut seeds = None;
    let mut out_dir = None;
    let mut ai1 = String::from("vercingetorix");
    let mut ai2 = String::from("petra");
    let mut difficulty2 = Difficulty(3);
    let mut civ1 = String::from("gaul");
    let mut civ2 = String::from("rome");
    let mut bot_mod = None;
    let mut mod_dir = None;
    let mut map = String::from("random/mainland");
    let mut map_size = 128;
    let mut timeout_secs = 1200;

    let mut i = 0;
    while i < args.len() {
        let arg = &args[i];
        let value = |flag: &str| {
            args.get(i + 1)
                .cloned()
                .ok_or_else(|| CliError::MissingValue(flag.to_string()))
        };
        match arg.as_str() {
            "--tag" => {
                tag = Some(value("--tag")?);
                i += 2;
            }
            "--seeds" => {
                seeds = Some(value("--seeds")?);
                i += 2;
            }
            "--out" => {
                out_dir = Some(PathBuf::from(value("--out")?));
                i += 2;
            }
            "--ai1" => {
                ai1 = value("--ai1")?;
                i += 2;
            }
            "--ai2" => {
                ai2 = value("--ai2")?;
                i += 2;
            }
            "--difficulty2" => {
                let raw = value("--difficulty2")?;
                let parsed = raw.parse::<u8>().ok().filter(|d| *d <= 5);
                difficulty2 = parsed
                    .map(Difficulty)
                    .ok_or_else(|| CliError::InvalidValue(format!("--difficulty2={raw}")))?;
                i += 2;
            }
            "--civ1" => {
                civ1 = value("--civ1")?;
                i += 2;
            }
            "--civ2" => {
                civ2 = value("--civ2")?;
                i += 2;
            }
            "--mod" => {
                bot_mod = Some(value("--mod")?);
                i += 2;
            }
            "--mod-dir" => {
                mod_dir = Some(PathBuf::from(value("--mod-dir")?));
                i += 2;
            }
            "--map" => {
                map = value("--map")?;
                i += 2;
            }
            "--size" => {
                let raw = value("--size")?;
                map_size = raw
                    .parse::<u32>()
                    .map_err(|_| CliError::InvalidValue(format!("--size={raw}")))?;
                i += 2;
            }
            "--timeout" => {
                let raw = value("--timeout")?;
                timeout_secs = raw
                    .parse::<u64>()
                    .map_err(|_| CliError::InvalidValue(format!("--timeout={raw}")))?;
                i += 2;
            }
            other => return Err(CliError::UnknownFlag(other.to_string())),
        }
    }

    let tag = tag.ok_or(CliError::MissingFlag("--tag".to_string()))?;
    let seeds_raw = seeds.ok_or(CliError::MissingFlag("--seeds".to_string()))?;
    let out_dir = out_dir.ok_or(CliError::MissingFlag("--out".to_string()))?;

    let seeds = seeds_raw
        .split(',')
        .map(|s| {
            s.trim()
                .parse::<u32>()
                .map(Seed)
                .map_err(|_| CliError::InvalidValue(format!("--seeds={s}")))
        })
        .collect::<Result<Vec<Seed>, CliError>>()?;

    Ok(Config {
        tag,
        seeds,
        out_dir,
        ai1,
        ai2,
        difficulty2,
        civ1,
        civ2,
        bot_mod,
        mod_dir,
        map,
        map_size,
        timeout_secs,
    })
}

/// The command line shared by `run_match` and the batch provenance string.
/// `seed == None` yields the template form used in the provenance string.
fn match_arguments(cfg: &Config, seed: Option<Seed>) -> Vec<String> {
    let seed_text = seed.map_or(String::from("<seed>"), |s| s.0.to_string());
    let mut args = vec![
        format!("-autostart={}", cfg.map),
        format!("-autostart-seed={seed_text}"),
        String::from("-autostart-nonvisual"),
        String::from("-autostart-players=2"),
        format!("-autostart-size={}", cfg.map_size),
        format!("-autostart-ai=1:{}", cfg.ai1),
        format!("-autostart-ai=2:{}", cfg.ai2),
        format!("-autostart-aidiff=2:{}", cfg.difficulty2.0),
        format!("-autostart-civ=1:{}", cfg.civ1),
        format!("-autostart-civ=2:{}", cfg.civ2),
        String::from("-autostart-player=-1"),
        String::from("-unique-logs"),
        String::from("-nosound"),
    ];
    if let Some(mod_name) = &cfg.bot_mod {
        // The engine only auto-enables the public mod when no -mod flag is
        // given at all; without public there are no autostart scripts, so a
        // user mod on its own can never start. public first, mod over it.
        args.push(String::from("-mod=public"));
        args.push(format!("-mod={mod_name}"));
    }
    args
}

fn build_match_command(seed: Seed, cfg: &Config, home: &Path) -> Command {
    let mut cmd = Command::new("timeout");
    cmd.arg(cfg.timeout_secs.to_string())
        .arg(PYROGENESIS)
        .args(match_arguments(cfg, Some(seed)))
        .env("HOME", home);
    cmd
}

/// Counts the engine's per-turn progress lines printed on stdout.
fn count_turns(stdout: &str) -> TurnCount {
    TurnCount(
        stdout
            .lines()
            .filter(|line| line.starts_with("Turn "))
            .count() as u64,
    )
}

#[derive(Debug)]
enum ParseStatsError {
    Unbalanced(String),
    InvalidJson(serde_json::Error),
}

impl std::fmt::Display for ParseStatsError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::Unbalanced(detail) => write!(f, "unbalanced statistics block: {detail}"),
            Self::InvalidJson(source) => write!(f, "invalid statistics JSON: {source}"),
        }
    }
}

/// Extracts the per-player statistics blocks the engine prints at game end.
/// Each block is a pretty-printed JSON object whose root braces sit at column 0.
fn extract_player_blocks(stdout: &str) -> Result<Vec<serde_json::Value>, ParseStatsError> {
    let mut blocks: Vec<serde_json::Value> = Vec::new();
    let mut current: Option<String> = None;
    for line in stdout.lines() {
        if line == "{" {
            if current.is_some() {
                return Err(ParseStatsError::Unbalanced(String::from(
                    "block start '{' while already inside a block",
                )));
            }
            current = Some(String::from("{\n"));
            continue;
        }
        if line == "}" {
            let Some(mut buf) = current.take() else {
                return Err(ParseStatsError::Unbalanced(String::from(
                    "block end '}' outside any block",
                )));
            };
            buf.push_str("}\n");
            let value = serde_json::from_str(&buf).map_err(ParseStatsError::InvalidJson)?;
            blocks.push(value);
            continue;
        }
        if let Some(buf) = &mut current {
            buf.push_str(line);
            buf.push('\n');
        }
    }
    if current.is_some() {
        return Err(ParseStatsError::Unbalanced(String::from(
            "unterminated block at end of stdout",
        )));
    }
    Ok(blocks)
}

/// Lines the bot prints to stdout for the harness (`print("[HARNESS] ...")`).
fn extract_harness_lines(stdout: &str) -> Vec<String> {
    stdout
        .lines()
        .filter(|line| line.contains("[HARNESS]"))
        .map(str::trim)
        .map(str::to_string)
        .collect()
}

fn read_interesting_log(home: &Path) -> Result<String, io::Error> {
    let log_dir = home.join(".local/state/0ad/log");
    let mut found: Option<PathBuf> = None;
    for entry in fs::read_dir(&log_dir)? {
        let entry = entry?;
        let name = entry.file_name().to_string_lossy().into_owned();
        if name.starts_with("interestinglog") {
            found = Some(entry.path());
            break;
        }
    }
    match found {
        Some(path) => fs::read_to_string(path),
        None => Err(io::Error::new(
            io::ErrorKind::NotFound,
            format!("no interestinglog in {}", log_dir.display()),
        )),
    }
}

/// Bot script errors land in the interesting log as `ERROR:` lines.
fn count_js_errors(log_content: &str) -> usize {
    log_content
        .lines()
        .filter(|line| line.contains("ERROR:"))
        .count()
}

#[derive(Debug)]
enum ReadModNameError {
    Read {
        path: PathBuf,
        source: io::Error,
    },
    Parse {
        path: PathBuf,
        source: serde_json::Error,
    },
    MissingName,
}

impl std::fmt::Display for ReadModNameError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::Read { path, source } => {
                write!(f, "cannot read {}: {source}", path.display())
            }
            Self::Parse { path, source } => {
                write!(f, "cannot parse {}: {source}", path.display())
            }
            Self::MissingName => write!(f, "mod.json has no \"name\" field"),
        }
    }
}

fn read_mod_name(mod_dir: &Path) -> Result<String, ReadModNameError> {
    let manifest_path = mod_dir.join("mod.json");
    let text = fs::read_to_string(&manifest_path).map_err(|source| ReadModNameError::Read {
        path: manifest_path.clone(),
        source,
    })?;
    let value: serde_json::Value =
        serde_json::from_str(&text).map_err(|source| ReadModNameError::Parse {
            path: manifest_path,
            source,
        })?;
    value
        .get("name")
        .and_then(serde_json::Value::as_str)
        .map(str::to_string)
        .ok_or(ReadModNameError::MissingName)
}

#[derive(Debug)]
enum CopyTreeError {
    ReadDir {
        path: PathBuf,
        source: io::Error,
    },
    CreateDir {
        path: PathBuf,
        source: io::Error,
    },
    Copy {
        from: PathBuf,
        to: PathBuf,
        source: io::Error,
    },
}

impl std::fmt::Display for CopyTreeError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::ReadDir { path, source } => {
                write!(f, "cannot read {}: {source}", path.display())
            }
            Self::CreateDir { path, source } => {
                write!(f, "cannot create {}: {source}", path.display())
            }
            Self::Copy { from, to, source } => write!(
                f,
                "cannot copy {} to {}: {source}",
                from.display(),
                to.display()
            ),
        }
    }
}

/// Recursive directory copy for installing the bot mod into a match home.
/// `std::fs` has no recursive copy, so this small walk is the whole of it.
fn copy_tree(from: &Path, to: &Path) -> Result<(), CopyTreeError> {
    fs::create_dir_all(to).map_err(|source| CopyTreeError::CreateDir {
        path: to.to_path_buf(),
        source,
    })?;
    for entry in fs::read_dir(from).map_err(|source| CopyTreeError::ReadDir {
        path: from.to_path_buf(),
        source,
    })? {
        let entry = entry.map_err(|source| CopyTreeError::ReadDir {
            path: from.to_path_buf(),
            source,
        })?;
        let from_path = entry.path();
        let to_path = to.join(entry.file_name());
        let file_type = entry.file_type().map_err(|source| CopyTreeError::ReadDir {
            path: from_path.clone(),
            source,
        })?;
        if file_type.is_dir() {
            copy_tree(&from_path, &to_path)?;
        } else {
            fs::copy(&from_path, &to_path).map_err(|source| CopyTreeError::Copy {
                from: from_path,
                to: to_path,
                source,
            })?;
        }
    }
    Ok(())
}

#[derive(Serialize)]
struct MatchResult {
    seed: u32,
    exit: String,
    wall_seconds: u64,
    turns: u64,
    // The engine's own per-player statistics objects, stored verbatim: the
    // runner's job is faithful extraction, not interpretation.
    players: Vec<serde_json::Value>,
    harness_lines: Vec<String>,
    js_errors: usize,
    // Kept for diagnosing failed matches; contains pid/timestamp-specific
    // paths, so it is excluded from determinism comparisons.
    stderr: String,
}

#[derive(Serialize)]
struct BatchResult {
    tag: String,
    command: String,
    matches: Vec<MatchResult>,
}

#[derive(Debug)]
enum RunMatchError {
    CreateHomeDir { path: PathBuf, source: io::Error },
    ModName(ReadModNameError),
    InstallMod(CopyTreeError),
    SpawnFailed { source: io::Error },
    NonUtf8Output,
    NoExitStatus { stderr: String },
    StatsParse(ParseStatsError),
    LogRead { source: io::Error },
}

impl std::fmt::Display for RunMatchError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::CreateHomeDir { path, source } => {
                write!(f, "cannot create match home {}: {source}", path.display())
            }
            Self::ModName(source) => write!(f, "cannot read mod name: {source}"),
            Self::InstallMod(source) => write!(f, "cannot install bot mod: {source}"),
            Self::SpawnFailed { source } => write!(f, "cannot spawn engine: {source}"),
            Self::NonUtf8Output => write!(f, "engine output is not valid UTF-8"),
            Self::NoExitStatus { stderr } => {
                write!(f, "engine killed without exit status: {stderr}")
            }
            Self::StatsParse(source) => write!(f, "cannot parse statistics: {source}"),
            Self::LogRead { source } => write!(f, "cannot read engine logs: {source}"),
        }
    }
}

fn run_match(seed: Seed, cfg: &Config) -> Result<MatchResult, RunMatchError> {
    let home = cfg
        .out_dir
        .join("homes")
        .join(format!("{}-{}", cfg.tag, seed.0));
    fs::create_dir_all(&home).map_err(|source| RunMatchError::CreateHomeDir {
        path: home.clone(),
        source,
    })?;

    if let Some(mod_dir) = &cfg.mod_dir {
        let mod_name = read_mod_name(mod_dir).map_err(RunMatchError::ModName)?;
        let dest = home.join(".local/share/0ad/mods").join(mod_name);
        copy_tree(mod_dir, &dest).map_err(RunMatchError::InstallMod)?;
    }

    let start = Instant::now();
    let Output {
        status,
        stdout,
        stderr,
    } = build_match_command(seed, cfg, &home)
        .output()
        .map_err(|source| RunMatchError::SpawnFailed { source })?;
    let wall_seconds = WallSeconds(start.elapsed().as_secs());

    let stdout = String::from_utf8(stdout).map_err(|_| RunMatchError::NonUtf8Output)?;
    let stderr = String::from_utf8(stderr).map_err(|_| RunMatchError::NonUtf8Output)?;

    let exit = match status.code() {
        Some(0) => MatchExit::Finished,
        Some(124) => MatchExit::TimedOut,
        Some(code) => MatchExit::Failed(code),
        None => return Err(RunMatchError::NoExitStatus { stderr }),
    };

    let players = extract_player_blocks(&stdout).map_err(RunMatchError::StatsParse)?;
    let turns = count_turns(&stdout);
    let harness_lines = extract_harness_lines(&stdout);
    let log_content =
        read_interesting_log(&home).map_err(|source| RunMatchError::LogRead { source })?;
    let js_errors = count_js_errors(&log_content);

    Ok(MatchResult {
        seed: seed.0,
        exit: exit.as_str(),
        wall_seconds: wall_seconds.0,
        turns: turns.0,
        players,
        harness_lines,
        js_errors,
        stderr,
    })
}

#[derive(Debug)]
enum WriteJsonError {
    CreateDir { path: PathBuf, source: io::Error },
    Serialize(serde_json::Error),
    Write { path: PathBuf, source: io::Error },
}

impl std::fmt::Display for WriteJsonError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::CreateDir { path, source } => {
                write!(f, "cannot create directory {}: {source}", path.display())
            }
            Self::Serialize(source) => write!(f, "cannot serialize JSON: {source}"),
            Self::Write { path, source } => {
                write!(f, "cannot write {}: {source}", path.display())
            }
        }
    }
}

fn write_json(path: &Path, value: &impl Serialize) -> Result<(), WriteJsonError> {
    if let Some(parent) = path.parent() {
        fs::create_dir_all(parent).map_err(|source| WriteJsonError::CreateDir {
            path: parent.to_path_buf(),
            source,
        })?;
    }
    let mut text = serde_json::to_string_pretty(value).map_err(WriteJsonError::Serialize)?;
    text.push('\n');
    fs::write(path, text).map_err(|source| WriteJsonError::Write {
        path: path.to_path_buf(),
        source,
    })
}

#[derive(Debug)]
enum MainError {
    Cli(CliError),
    Match(RunMatchError),
    Write(WriteJsonError),
}

impl std::fmt::Display for MainError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::Cli(source) => write!(f, "{source}"),
            Self::Match(source) => write!(f, "{source}"),
            Self::Write(source) => write!(f, "{source}"),
        }
    }
}

fn main() -> Result<(), MainError> {
    let args: Vec<String> = env::args().skip(1).collect();
    let cfg = parse_args(&args).map_err(MainError::Cli)?;

    let mut matches = Vec::new();
    for seed in &cfg.seeds {
        matches.push(run_match(*seed, &cfg).map_err(MainError::Match)?);
    }

    let batch = BatchResult {
        tag: cfg.tag.clone(),
        command: match_arguments(&cfg, None).join(" "),
        matches,
    };
    let per_match_dir = cfg.out_dir.join(&cfg.tag);
    for result in &batch.matches {
        let path = per_match_dir.join(format!("{}.json", result.seed));
        write_json(&path, result).map_err(MainError::Write)?;
    }
    let batch_path = cfg.out_dir.join(format!("{}.json", cfg.tag));
    write_json(&batch_path, &batch).map_err(MainError::Write)?;
    println!(
        "batch {}: {} matches written to {}/",
        cfg.tag,
        batch.matches.len(),
        cfg.out_dir.display()
    );
    Ok(())
}
