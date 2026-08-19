//! `harness report`: the protocol's verdict machinery over two batch JSONs.
//!
//! Everything here is pure scoring over the batch data; the filesystem
//! touchpoints (loading batches, writing `report.md`, printing the summary)
//! live in `run` at the bottom.

use std::fs;
use std::io;
use std::path::PathBuf;

use serde::Deserialize;

const GOOD_THRESHOLD: f64 = 4.0;
const METRIC_WEIGHT: f64 = 0.4;
/// resource keys summed for the gathered/used metrics; `vegetarianFood` is a
/// subset of `food` (the engine's GUI counters skip it to avoid double
/// counting), so it is deliberately excluded.
const RESOURCE_KEYS: [&str; 4] = ["food", "wood", "metal", "stone"];

#[derive(Debug, PartialEq, Eq, Clone, Copy)]
enum Outcome {
    Win,
    Draw,
    Loss,
}

impl Outcome {
    #[must_use]
    fn score(self) -> f64 {
        match self {
            Self::Win => 3.0,
            Self::Draw => 1.0,
            Self::Loss => 0.0,
        }
    }

    #[must_use]
    fn label(self) -> &'static str {
        match self {
            Self::Win => "win",
            Self::Draw => "draw",
            Self::Loss => "loss",
        }
    }
}

#[derive(Debug, PartialEq)]
enum Verdict {
    Good,
    Bad,
    Neutral,
    Invalid(String),
}

impl Verdict {
    #[must_use]
    fn label(&self) -> String {
        match self {
            Self::Good => String::from("good"),
            Self::Bad => String::from("bad"),
            Self::Neutral => String::from("neutral"),
            Self::Invalid(reason) => format!("invalid: {reason}"),
        }
    }
}

/// The batch JSON the runner writes, with only the fields the report needs.
/// Unknown extra fields are ignored (the runner is the only producer).
#[derive(Deserialize)]
struct Batch {
    tag: String,
    command: String,
    matches: Vec<MatchRecord>,
}

#[derive(Deserialize)]
#[allow(dead_code)] // wall_seconds/stderr are read by nobody on purpose:
                    // they are exactly the fields the canary check excludes.
struct MatchRecord {
    seed: u32,
    exit: String,
    wall_seconds: u64,
    turns: u64,
    players: Vec<serde_json::Value>,
    harness_lines: Vec<String>,
    js_errors: usize,
    stderr: String,
}

#[derive(Debug)]
enum ReportArgsError {
    UnknownFlag(String),
    MissingValue(String),
    MissingFlag(String),
}

impl std::fmt::Display for ReportArgsError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::UnknownFlag(flag) => write!(f, "unknown flag: {flag}"),
            Self::MissingValue(flag) => write!(f, "missing value for {flag}"),
            Self::MissingFlag(flag) => write!(f, "missing required flag {flag}"),
        }
    }
}

struct ReportArgs {
    baseline: PathBuf,
    treatment: Option<PathBuf>,
    canary: Option<PathBuf>,
    out_dir: PathBuf,
}

/// The 40-line clippy cap is waived: one cohesive parser of the report
/// subcommand's fixed flag set, mirroring the runner's parser.
#[allow(clippy::too_many_lines)]
fn parse_args(args: &[String]) -> Result<ReportArgs, ReportArgsError> {
    let mut baseline = None;
    let mut treatment = None;
    let mut canary = None;
    let mut out_dir = PathBuf::from(".");

    let mut i = 0;
    while i < args.len() {
        let arg = &args[i];
        let value = |flag: &str| {
            args.get(i + 1)
                .cloned()
                .ok_or_else(|| ReportArgsError::MissingValue(flag.to_string()))
        };
        match arg.as_str() {
            "--baseline" => {
                baseline = Some(PathBuf::from(value("--baseline")?));
                i += 2;
            }
            "--treatment" => {
                treatment = Some(PathBuf::from(value("--treatment")?));
                i += 2;
            }
            "--canary" => {
                canary = Some(PathBuf::from(value("--canary")?));
                i += 2;
            }
            "--out" => {
                out_dir = PathBuf::from(value("--out")?);
                i += 2;
            }
            other => return Err(ReportArgsError::UnknownFlag(other.to_string())),
        }
    }

    let baseline = baseline.ok_or(ReportArgsError::MissingFlag(String::from("--baseline")))?;
    Ok(ReportArgs {
        baseline,
        treatment,
        canary,
        out_dir,
    })
}

#[derive(Debug)]
enum LoadBatchError {
    Read {
        path: PathBuf,
        source: io::Error,
    },
    Parse {
        path: PathBuf,
        source: serde_json::Error,
    },
}

impl std::fmt::Display for LoadBatchError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::Read { path, source } => write!(f, "cannot read {}: {source}", path.display()),
            Self::Parse { path, source } => {
                write!(f, "cannot parse {}: {source}", path.display())
            }
        }
    }
}

fn load_batch(path: &PathBuf) -> Result<Batch, LoadBatchError> {
    let text = fs::read_to_string(path).map_err(|source| LoadBatchError::Read {
        path: path.clone(),
        source,
    })?;
    serde_json::from_str(&text).map_err(|source| LoadBatchError::Parse {
        path: path.clone(),
        source,
    })
}

#[derive(Debug)]
enum ClassifyOutcomeError {
    MissingPlayer(u32),
    UnknownState { player: u32, state: String },
}

impl std::fmt::Display for ClassifyOutcomeError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::MissingPlayer(id) => write!(f, "no player {id} block in match statistics"),
            Self::UnknownState { player, state } => {
                write!(f, "player {player} has unknown playerState {state:?}")
            }
        }
    }
}

fn player_state(players: &[serde_json::Value], id: u32) -> Result<String, ClassifyOutcomeError> {
    players
        .iter()
        .find(|p| p.get("playerID").and_then(serde_json::Value::as_u64) == Some(u64::from(id)))
        .and_then(|p| p.get("playerState"))
        .and_then(serde_json::Value::as_str)
        .map(str::to_string)
        .ok_or(ClassifyOutcomeError::MissingPlayer(id))
}

/// Outcome from player 1's (the bot's) perspective. The time-limit trigger
/// marks every still-active player "won", so all-won is a draw, as is the
/// mutual-destruction all-defeated case.
fn classify_outcome(players: &[serde_json::Value]) -> Result<Outcome, ClassifyOutcomeError> {
    let ours = player_state(players, 1)?;
    let theirs = player_state(players, 2)?;
    let (ours_won, theirs_won) = match (ours.as_str(), theirs.as_str()) {
        ("won", "won") | ("defeated", "defeated") => return Ok(Outcome::Draw),
        ("won", "defeated") => (true, false),
        ("defeated", "won") => (false, true),
        _ => {
            let (player, state) = if ours != "won" && ours != "defeated" {
                (1, ours.clone())
            } else {
                (2, theirs.clone())
            };
            return Err(ClassifyOutcomeError::UnknownState { player, state });
        }
    };
    Ok(if ours_won && !theirs_won {
        Outcome::Win
    } else {
        Outcome::Loss
    })
}

#[derive(Clone, Copy)]
struct MatchMetrics {
    resources_gathered: Option<f64>,
    resources_used: Option<f64>,
    enemy_units_killed: Option<f64>,
    units_trained: Option<f64>,
    population_peak: Option<f64>,
}

impl MatchMetrics {
    #[must_use]
    fn empty() -> Self {
        Self {
            resources_gathered: None,
            resources_used: None,
            enemy_units_killed: None,
            units_trained: None,
            population_peak: None,
        }
    }
}

fn sum_stat_keys(stats: &serde_json::Value, counter: &str, keys: &[&str]) -> Option<f64> {
    let obj = stats.get(counter)?;
    keys.iter()
        .map(|key| obj.get(key).and_then(serde_json::Value::as_f64))
        .sum()
}

/// Population peak from the bot's per-minute `[HARNESS]` samples
/// (`"pop":"18/30"` → numerator). Lines that do not carry a sample are
/// skipped; no samples at all means the metric is absent.
fn population_peak(harness_lines: &[String]) -> Option<f64> {
    let mut peak: u32 = 0;
    let mut found = false;
    for line in harness_lines {
        let Some(json) = line.strip_prefix("[HARNESS] ") else {
            continue;
        };
        let Ok(value) = serde_json::from_str::<serde_json::Value>(json) else {
            continue;
        };
        let Some(pop) = value.get("pop").and_then(serde_json::Value::as_str) else {
            continue;
        };
        let Some((numerator, _)) = pop.split_once('/') else {
            continue;
        };
        let Ok(count) = numerator.parse::<u32>() else {
            continue;
        };
        found = true;
        peak = peak.max(count);
    }
    found.then_some(f64::from(peak))
}

fn extract_metrics(record: &MatchRecord) -> MatchMetrics {
    let stats = record
        .players
        .iter()
        .find(|p| p.get("playerID").and_then(serde_json::Value::as_u64) == Some(1))
        .and_then(|p| p.get("statistics"));
    let Some(stats) = stats else {
        return MatchMetrics::empty();
    };
    MatchMetrics {
        resources_gathered: sum_stat_keys(stats, "resourcesGathered", &RESOURCE_KEYS),
        resources_used: sum_stat_keys(stats, "resourcesUsed", &RESOURCE_KEYS),
        enemy_units_killed: stats
            .get("enemyUnitsKilledValue")
            .and_then(serde_json::Value::as_f64),
        units_trained: stats
            .get("unitsTrained")
            .and_then(|trained| trained.get("total"))
            .and_then(serde_json::Value::as_f64),
        population_peak: population_peak(&record.harness_lines),
    }
}

#[must_use]
fn relative_delta(base: f64, treatment: f64) -> f64 {
    ((treatment - base) / base.max(1.0)).clamp(-1.0, 1.0)
}

struct MetricDelta {
    name: &'static str,
    base: f64,
    treatment: f64,
    weighted_delta: f64,
}

fn metric_delta(
    name: &'static str,
    base: Option<f64>,
    treatment: Option<f64>,
) -> Option<MetricDelta> {
    let (base, treatment) = (base?, treatment?);
    Some(MetricDelta {
        name,
        base,
        treatment,
        weighted_delta: relative_delta(base, treatment) * METRIC_WEIGHT,
    })
}

struct PairDiff {
    seed: u32,
    base_outcome: Outcome,
    treatment_outcome: Outcome,
    outcome_delta: f64,
    survival_delta: f64,
    metric_deltas: Vec<MetricDelta>,
    js_errors: (usize, usize),
    total: f64,
}

#[derive(Debug)]
enum ScorePairError {
    Base(ClassifyOutcomeError),
    Treatment(ClassifyOutcomeError),
}

impl std::fmt::Display for ScorePairError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::Base(source) => write!(f, "baseline match: {source}"),
            Self::Treatment(source) => write!(f, "treatment match: {source}"),
        }
    }
}

#[allow(clippy::cast_precision_loss)] // turn counts are ≪ 2^53: exact in f64
fn score_pair(base: &MatchRecord, treatment: &MatchRecord) -> Result<PairDiff, ScorePairError> {
    let base_outcome = classify_outcome(&base.players).map_err(ScorePairError::Base)?;
    let treatment_outcome =
        classify_outcome(&treatment.players).map_err(ScorePairError::Treatment)?;
    let base_metrics = extract_metrics(base);
    let treatment_metrics = extract_metrics(treatment);

    let outcome_delta = treatment_outcome.score() - base_outcome.score();
    let survival_delta = match (base_outcome, treatment_outcome) {
        (Outcome::Loss, Outcome::Loss) | (Outcome::Draw, Outcome::Draw) => {
            relative_delta(base.turns as f64, treatment.turns as f64) * METRIC_WEIGHT
        }
        _ => 0.0,
    };
    let metric_deltas = [
        metric_delta(
            "resourcesGathered",
            base_metrics.resources_gathered,
            treatment_metrics.resources_gathered,
        ),
        metric_delta(
            "resourcesUsed",
            base_metrics.resources_used,
            treatment_metrics.resources_used,
        ),
        metric_delta(
            "enemyUnitsKilled",
            base_metrics.enemy_units_killed,
            treatment_metrics.enemy_units_killed,
        ),
        metric_delta(
            "unitsTrained",
            base_metrics.units_trained,
            treatment_metrics.units_trained,
        ),
        metric_delta(
            "populationPeak",
            base_metrics.population_peak,
            treatment_metrics.population_peak,
        ),
    ]
    .into_iter()
    .flatten()
    .collect::<Vec<_>>();
    let total = outcome_delta
        + survival_delta
        + metric_deltas
            .iter()
            .map(|delta| delta.weighted_delta)
            .sum::<f64>();

    Ok(PairDiff {
        seed: base.seed,
        base_outcome,
        treatment_outcome,
        outcome_delta,
        survival_delta,
        metric_deltas,
        js_errors: (base.js_errors, treatment.js_errors),
        total,
    })
}

struct BatchScore {
    pairs: Vec<PairDiff>,
    total: f64,
    error_veto: bool,
}

#[derive(Debug)]
enum ScoreBatchError {
    SeedMismatch {
        baseline: Vec<u32>,
        treatment: Vec<u32>,
    },
    Pair(ScorePairError),
}

impl std::fmt::Display for ScoreBatchError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::SeedMismatch {
                baseline,
                treatment,
            } => write!(
                f,
                "seed sets differ: baseline {baseline:?} vs treatment {treatment:?}"
            ),
            Self::Pair(source) => write!(f, "{source}"),
        }
    }
}

fn sorted_seeds(batch: &Batch) -> Vec<u32> {
    let mut seeds = batch.matches.iter().map(|m| m.seed).collect::<Vec<_>>();
    seeds.sort_unstable();
    seeds
}

fn score_batch(base: &Batch, treatment: &Batch) -> Result<BatchScore, ScoreBatchError> {
    let base_seeds = sorted_seeds(base);
    let treatment_seeds = sorted_seeds(treatment);
    if base_seeds != treatment_seeds {
        return Err(ScoreBatchError::SeedMismatch {
            baseline: base_seeds,
            treatment: treatment_seeds,
        });
    }

    let mut pairs = Vec::new();
    let mut error_veto = false;
    for seed in &base_seeds {
        let base_match = base.matches.iter().find(|m| m.seed == *seed);
        let treatment_match = treatment.matches.iter().find(|m| m.seed == *seed);
        let (Some(base_match), Some(treatment_match)) = (base_match, treatment_match) else {
            // Unreachable: the seed sets were just checked equal, so both
            // lookups succeed for every seed.
            return Err(ScoreBatchError::SeedMismatch {
                baseline: base_seeds,
                treatment: treatment_seeds,
            });
        };
        let pair = score_pair(base_match, treatment_match).map_err(ScoreBatchError::Pair)?;
        if treatment_match.js_errors > base_match.js_errors {
            error_veto = true;
        }
        pairs.push(pair);
    }
    let total = pairs.iter().map(|pair| pair.total).sum();
    Ok(BatchScore {
        pairs,
        total,
        error_veto,
    })
}

/// A canary match is identical to the baseline match with the same seed on
/// every deterministic field; `wall_seconds` (wall-clock noise) and `stderr`
/// (pid/timestamp-specific paths) are excluded by construction.
struct CanaryReport {
    pass: bool,
    details: Vec<String>,
}

#[derive(Debug)]
enum CheckCanaryError {
    SeedNotFound { seed: u32 },
}

impl std::fmt::Display for CheckCanaryError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::SeedNotFound { seed } => {
                write!(
                    f,
                    "canary seed {seed} has no baseline match to compare against"
                )
            }
        }
    }
}

fn check_canary(base: &Batch, canary: &Batch) -> Result<CanaryReport, CheckCanaryError> {
    let mut details = Vec::new();
    if canary.command != base.command {
        details.push(format!(
            "settings differ: baseline `{}` vs canary `{}`",
            base.command, canary.command
        ));
    }
    for canary_match in &canary.matches {
        let Some(base_match) = base.matches.iter().find(|m| m.seed == canary_match.seed) else {
            return Err(CheckCanaryError::SeedNotFound {
                seed: canary_match.seed,
            });
        };
        if canary_match.exit != base_match.exit {
            details.push(format!(
                "seed {}: exit {} vs {}",
                canary_match.seed, canary_match.exit, base_match.exit
            ));
        }
        if canary_match.turns != base_match.turns {
            details.push(format!(
                "seed {}: turns {} vs {}",
                canary_match.seed, canary_match.turns, base_match.turns
            ));
        }
        if canary_match.players != base_match.players {
            details.push(format!(
                "seed {}: player statistics differ",
                canary_match.seed
            ));
        }
        if canary_match.harness_lines != base_match.harness_lines {
            details.push(format!("seed {}: harness lines differ", canary_match.seed));
        }
        if canary_match.js_errors != base_match.js_errors {
            details.push(format!(
                "seed {}: JS errors {} vs {}",
                canary_match.seed, canary_match.js_errors, base_match.js_errors
            ));
        }
    }
    Ok(CanaryReport {
        pass: details.is_empty(),
        details,
    })
}

fn decide_verdict(score: Option<&BatchScore>, canary: Option<&CanaryReport>) -> Option<Verdict> {
    if let Some(canary) = canary {
        if !canary.pass {
            return Some(Verdict::Invalid(canary.details.join("; ")));
        }
    }
    let score = score?;
    Some(if score.error_veto {
        Verdict::Bad
    } else if score.total >= GOOD_THRESHOLD {
        Verdict::Good
    } else if score.total <= -GOOD_THRESHOLD {
        Verdict::Bad
    } else {
        Verdict::Neutral
    })
}

fn render_markdown(
    base: &Batch,
    treatment_tag: Option<&str>,
    score: Option<&BatchScore>,
    canary: Option<&CanaryReport>,
    verdict: Option<&Verdict>,
) -> String {
    use std::fmt::Write as _;

    let mut md = String::new();
    let _ = writeln!(
        md,
        "# Report — {} vs {}",
        base.tag,
        treatment_tag.unwrap_or("(no treatment)")
    );
    let _ = writeln!(md, "\nSettings: `{}`", base.command);

    if let Some(canary) = canary {
        let _ = writeln!(
            md,
            "\n## Canary\n\n{}",
            if canary.pass {
                String::from("PASS")
            } else {
                format!("FAIL — {}", canary.details.join("; "))
            }
        );
    }

    if let Some(score) = score {
        let _ = writeln!(md, "\n## Pairs\n");
        let _ = writeln!(
            md,
            "| seed | base | treatment | outcome | survival | total | JS errors (base→treat) |"
        );
        let _ = writeln!(md, "|---|---|---|---|---|---|---|");
        for pair in &score.pairs {
            let js = format!("{}→{}", pair.js_errors.0, pair.js_errors.1);
            let _ = writeln!(
                md,
                "| {} | {} | {} | {:+.2} | {:+.2} | {:+.2} | {} |",
                pair.seed,
                pair.base_outcome.label(),
                pair.treatment_outcome.label(),
                pair.outcome_delta,
                pair.survival_delta,
                pair.total,
                js
            );
        }
        let _ = writeln!(md, "\n## Metric deltas\n");
        let _ = writeln!(md, "| seed | metric | base | treatment | weighted delta |");
        let _ = writeln!(md, "|---|---|---|---|---|");
        for pair in &score.pairs {
            for delta in &pair.metric_deltas {
                let _ = writeln!(
                    md,
                    "| {} | {} | {:.0} | {:.0} | {:+.3} |",
                    pair.seed, delta.name, delta.base, delta.treatment, delta.weighted_delta
                );
            }
        }
        let outcome_sum = score
            .pairs
            .iter()
            .map(|pair| pair.outcome_delta)
            .sum::<f64>();
        let quality_sum = score
            .pairs
            .iter()
            .flat_map(|pair| &pair.metric_deltas)
            .map(|delta| delta.weighted_delta)
            .sum::<f64>();
        let survival_sum = score
            .pairs
            .iter()
            .map(|pair| pair.survival_delta)
            .sum::<f64>();
        let _ = writeln!(
            md,
            "\n## Totals\n\n{:.2} total = {:.2} outcome + {:.2} quality + {:.2} survival",
            score.total, outcome_sum, quality_sum, survival_sum
        );
        if score.error_veto {
            let _ = writeln!(
                md,
                "\n**Error veto**: a pair increased the bot's JS error count."
            );
        }
    }

    let _ = writeln!(
        md,
        "\n## Verdict\n\n{}",
        verdict.map_or(
            String::from("not scored (no treatment batch)"),
            Verdict::label
        )
    );
    md
}

fn print_summary(
    base: &Batch,
    treatment: Option<&Batch>,
    score: Option<&BatchScore>,
    canary: Option<&CanaryReport>,
    verdict: Option<&Verdict>,
) {
    println!("report: baseline={}", base.tag);
    match treatment {
        Some(batch) => println!(
            "        treatment={} ({} pairs)",
            batch.tag,
            score.map_or(0, |s| s.pairs.len())
        ),
        None => println!("        treatment=- (no treatment batch)"),
    }
    match canary {
        Some(canary) if canary.pass => println!("        canary=PASS"),
        Some(canary) => println!("        canary=FAIL — {}", canary.details.join("; ")),
        None => println!("        canary=-"),
    }
    if let Some(score) = score {
        println!(
            "        total={:+.2}, error_veto={}",
            score.total, score.error_veto
        );
    }
    println!(
        "        verdict={}",
        verdict.map_or(String::from("not scored"), Verdict::label)
    );
}

#[derive(Debug)]
enum WriteReportError {
    CreateDir { path: PathBuf, source: io::Error },
    Write { path: PathBuf, source: io::Error },
}

impl std::fmt::Display for WriteReportError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::CreateDir { path, source } => {
                write!(f, "cannot create directory {}: {source}", path.display())
            }
            Self::Write { path, source } => {
                write!(f, "cannot write {}: {source}", path.display())
            }
        }
    }
}

#[derive(Debug)]
#[allow(private_interfaces)] // this aggregate is the module's single error
                             // boundary; its payloads are module-local by design.
pub enum RunReportError {
    Args(ReportArgsError),
    LoadBaseline(LoadBatchError),
    LoadTreatment(LoadBatchError),
    LoadCanary(LoadBatchError),
    Score(ScoreBatchError),
    Canary(CheckCanaryError),
    Write(WriteReportError),
}

impl std::fmt::Display for RunReportError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::Args(source) => write!(f, "{source}"),
            Self::LoadBaseline(source) | Self::LoadTreatment(source) | Self::LoadCanary(source) => {
                write!(f, "{source}")
            }
            Self::Score(source) => write!(f, "{source}"),
            Self::Canary(source) => write!(f, "{source}"),
            Self::Write(source) => write!(f, "{source}"),
        }
    }
}

pub fn run(args: &[String]) -> Result<(), RunReportError> {
    let args = parse_args(args).map_err(RunReportError::Args)?;

    let baseline = load_batch(&args.baseline).map_err(RunReportError::LoadBaseline)?;
    let treatment = match &args.treatment {
        Some(path) => Some(load_batch(path).map_err(RunReportError::LoadTreatment)?),
        None => None,
    };
    let score = match &treatment {
        Some(batch) => Some(score_batch(&baseline, batch).map_err(RunReportError::Score)?),
        None => None,
    };
    let canary = match &args.canary {
        Some(path) => Some(load_batch(path).map_err(RunReportError::LoadCanary)?),
        None => None,
    };
    let canary_report = match &canary {
        Some(batch) => Some(check_canary(&baseline, batch).map_err(RunReportError::Canary)?),
        None => None,
    };
    let verdict = decide_verdict(score.as_ref(), canary_report.as_ref());

    let markdown = render_markdown(
        &baseline,
        treatment.as_ref().map(|batch| batch.tag.as_str()),
        score.as_ref(),
        canary_report.as_ref(),
        verdict.as_ref(),
    );

    fs::create_dir_all(&args.out_dir)
        .map_err(|source| WriteReportError::CreateDir {
            path: args.out_dir.clone(),
            source,
        })
        .map_err(RunReportError::Write)?;
    let out_path = args.out_dir.join("report.md");
    fs::write(&out_path, markdown)
        .map_err(|source| WriteReportError::Write {
            path: out_path,
            source,
        })
        .map_err(RunReportError::Write)?;

    print_summary(
        &baseline,
        treatment.as_ref(),
        score.as_ref(),
        canary_report.as_ref(),
        verdict.as_ref(),
    );
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    /// The fixture keeps wood at 0 so `resourcesGathered` equals the food
    /// value the tests set — the hand-computed deltas stay simple.
    fn players(p1: &str, p2: &str) -> Vec<serde_json::Value> {
        let player = |id: u64, state: &str| {
            serde_json::json!({
                "playerID": id,
                "playerState": state,
                "statistics": {
                    "resourcesGathered": {
                        "food": 100, "wood": 0, "metal": 0, "stone": 0, "vegetarianFood": 10
                    },
                    "resourcesUsed": {"food": 50, "wood": 0, "metal": 0, "stone": 0},
                    "enemyUnitsKilledValue": 500,
                    "unitsTrained": {"total": 10, "Unit": 10}
                }
            })
        };
        vec![player(1, p1), player(2, p2)]
    }

    fn assert_close(actual: f64, expected: f64) {
        assert!(
            (actual - expected).abs() < 1e-9,
            "expected {expected}, got {actual}"
        );
    }

    fn record(seed: u32, p1: &str, p2: &str, turns: u64, js_errors: usize) -> MatchRecord {
        MatchRecord {
            seed,
            exit: String::from("finished"),
            wall_seconds: 10,
            turns,
            players: players(p1, p2),
            harness_lines: vec![
                String::from("[HARNESS] {\"event\":\"sample\",\"pop\":\"12/20\"}"),
                String::from("[HARNESS] {\"event\":\"sample\",\"pop\":\"18/20\"}"),
            ],
            js_errors,
            stderr: String::new(),
        }
    }

    fn batch(records: Vec<MatchRecord>) -> Batch {
        Batch {
            tag: String::from("tag"),
            command: String::from("cmd"),
            matches: records,
        }
    }

    #[test]
    fn classifies_win_loss_and_draw() {
        assert_eq!(
            classify_outcome(&players("won", "won")).unwrap(),
            Outcome::Draw
        );
        assert_eq!(
            classify_outcome(&players("defeated", "defeated")).unwrap(),
            Outcome::Draw
        );
        assert_eq!(
            classify_outcome(&players("won", "defeated")).unwrap(),
            Outcome::Win
        );
        assert_eq!(
            classify_outcome(&players("defeated", "won")).unwrap(),
            Outcome::Loss
        );
    }

    #[test]
    fn rejects_unknown_player_state() {
        assert!(matches!(
            classify_outcome(&players("won", "active")),
            Err(ClassifyOutcomeError::UnknownState { .. })
        ));
        assert!(matches!(
            classify_outcome(
                players("defeated", "defeated")
                    .get(1..2)
                    .unwrap_or_default()
            ),
            Err(ClassifyOutcomeError::MissingPlayer(_))
        ));
    }

    #[test]
    fn outcome_delta_is_three_for_win_over_loss() {
        let pair = score_pair(
            &record(1, "defeated", "won", 100, 0),
            &record(1, "won", "defeated", 100, 0),
        )
        .unwrap();
        assert_close(pair.outcome_delta, 3.0);
        let pair = score_pair(
            &record(1, "won", "defeated", 100, 0),
            &record(1, "defeated", "won", 100, 0),
        )
        .unwrap();
        assert_close(pair.outcome_delta, -3.0);
    }

    #[test]
    fn quality_delta_clamps_at_one() {
        let mut treatment = record(1, "won", "won", 100, 0);
        treatment.players[0]["statistics"]["resourcesGathered"]["food"] =
            serde_json::json!(100_000.0);
        let pair = score_pair(&record(1, "won", "won", 100, 0), &treatment).unwrap();
        let gathered = pair
            .metric_deltas
            .iter()
            .find(|d| d.name == "resourcesGathered")
            .unwrap();
        assert_close(gathered.weighted_delta, METRIC_WEIGHT);
    }

    #[test]
    fn missing_metric_is_skipped() {
        let mut treatment = record(1, "won", "won", 100, 0);
        treatment.players[0]["statistics"]
            .as_object_mut()
            .unwrap()
            .remove("resourcesUsed");
        let pair = score_pair(&record(1, "won", "won", 100, 0), &treatment).unwrap();
        assert!(!pair.metric_deltas.iter().any(|d| d.name == "resourcesUsed"));
    }

    #[test]
    fn survival_applies_only_to_loss_loss_and_draw_draw() {
        let pair = score_pair(
            &record(1, "won", "defeated", 100, 0),
            &record(1, "won", "defeated", 200, 0),
        )
        .unwrap();
        assert_close(pair.survival_delta, 0.0);
        let pair = score_pair(
            &record(1, "won", "won", 100, 0),
            &record(1, "won", "won", 200, 0),
        )
        .unwrap();
        assert_close(pair.survival_delta, METRIC_WEIGHT);
    }

    #[test]
    fn population_peak_comes_from_samples() {
        let metrics = extract_metrics(&record(1, "won", "won", 100, 0));
        assert_close(metrics.population_peak.unwrap_or(f64::NAN), 18.0);
    }

    #[test]
    fn error_veto_forces_bad_verdict() {
        let base = batch(vec![record(1, "won", "defeated", 100, 0)]);
        let treatment = batch(vec![record(1, "won", "defeated", 100, 1)]);
        let score = score_batch(&base, &treatment).unwrap();
        assert!(score.error_veto);
        assert_eq!(decide_verdict(Some(&score), None), Some(Verdict::Bad));
    }

    #[test]
    fn verdict_thresholds_are_plus_minus_four() {
        let with_metrics = |seed: u32, p1: &str, p2: &str, turns: u64, food: f64, trained: f64| {
            let mut rec = record(seed, p1, p2, turns, 0);
            rec.players[0]["statistics"]["resourcesGathered"]["food"] = serde_json::json!(food);
            rec.players[0]["statistics"]["unitsTrained"]["total"] = serde_json::json!(trained);
            rec
        };

        // Good side: pair 1 loss → win (+3) with doubled gathering (+0.4);
        // pair 2 loss-loss with longer survival (100→200 turns, +0.4),
        // doubled gathering (+0.4) and doubled training (+0.4).
        // Total = 3.4 + 1.2 = 4.6 ≥ 4 → good.
        let base = batch(vec![
            with_metrics(1, "defeated", "won", 100, 100.0, 10.0),
            with_metrics(2, "defeated", "won", 100, 100.0, 10.0),
        ]);
        let treatment = batch(vec![
            with_metrics(1, "won", "defeated", 100, 200.0, 10.0),
            with_metrics(2, "defeated", "won", 200, 200.0, 20.0),
        ]);
        let score = score_batch(&base, &treatment).unwrap();
        assert_eq!(decide_verdict(Some(&score), None), Some(Verdict::Good));

        // Pair 1 alone (3.4) is neutral.
        let base = batch(vec![with_metrics(1, "defeated", "won", 100, 100.0, 10.0)]);
        let treatment = batch(vec![with_metrics(1, "won", "defeated", 100, 200.0, 10.0)]);
        let score = score_batch(&base, &treatment).unwrap();
        assert_eq!(decide_verdict(Some(&score), None), Some(Verdict::Neutral));

        // Bad side: pair 1 win → loss (−3) with halved gathering (−0.2) and
        // halved training (−0.2); pairs 2 and 3 loss-loss with halved
        // survival (200→100 turns, −0.2) and halved gathering (−0.2) each
        // = −0.4 each. Total = −3.4 − 0.8 = −4.2 ≤ −4 → bad.
        let base = batch(vec![
            with_metrics(1, "won", "defeated", 100, 200.0, 10.0),
            with_metrics(2, "defeated", "won", 200, 200.0, 10.0),
            with_metrics(3, "defeated", "won", 200, 200.0, 10.0),
        ]);
        let treatment = batch(vec![
            with_metrics(1, "defeated", "won", 100, 100.0, 5.0),
            with_metrics(2, "defeated", "won", 100, 100.0, 10.0),
            with_metrics(3, "defeated", "won", 100, 100.0, 10.0),
        ]);
        let score = score_batch(&base, &treatment).unwrap();
        assert_eq!(decide_verdict(Some(&score), None), Some(Verdict::Bad));
    }

    #[test]
    fn seed_set_mismatch_is_an_error() {
        let base = batch(vec![record(1, "won", "won", 100, 0)]);
        let treatment = batch(vec![record(2, "won", "won", 100, 0)]);
        assert!(matches!(
            score_batch(&base, &treatment),
            Err(ScoreBatchError::SeedMismatch { .. })
        ));
    }

    #[test]
    fn canary_passes_despite_wall_clock_noise() {
        let base = batch(vec![record(1, "won", "won", 100, 0)]);
        let mut canary = batch(vec![record(1, "won", "won", 100, 0)]);
        canary.matches[0].wall_seconds = 999;
        canary.matches[0].stderr = String::from("pid 1234 paths");
        assert!(check_canary(&base, &canary).unwrap().pass);
    }

    #[test]
    fn canary_fails_on_turns_difference() {
        let base = batch(vec![record(1, "won", "won", 100, 0)]);
        let canary = batch(vec![record(1, "won", "won", 101, 0)]);
        assert!(!check_canary(&base, &canary).unwrap().pass);
    }

    #[test]
    fn canary_fails_on_settings_drift() {
        let base = batch(vec![record(1, "won", "won", 100, 0)]);
        let mut canary = batch(vec![record(1, "won", "won", 100, 0)]);
        canary.command = String::from("different settings");
        assert!(!check_canary(&base, &canary).unwrap().pass);
    }

    #[test]
    fn canary_unknown_seed_is_an_error() {
        let base = batch(vec![record(1, "won", "won", 100, 0)]);
        let canary = batch(vec![record(2, "won", "won", 100, 0)]);
        assert!(matches!(
            check_canary(&base, &canary),
            Err(CheckCanaryError::SeedNotFound { .. })
        ));
    }

    #[test]
    fn canary_failure_makes_the_verdict_invalid() {
        let base = batch(vec![record(1, "won", "won", 100, 0)]);
        let canary = batch(vec![record(1, "won", "won", 101, 0)]);
        let report = check_canary(&base, &canary).unwrap();
        let score = score_batch(&base, &batch(vec![record(1, "won", "won", 100, 0)])).unwrap();
        assert!(matches!(
            decide_verdict(Some(&score), Some(&report)),
            Some(Verdict::Invalid(_))
        ));
    }
}
