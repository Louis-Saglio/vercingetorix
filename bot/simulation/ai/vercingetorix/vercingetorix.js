// Vercingetorix — skeleton baseline.
//
// One scripted plan, no adaptation: grow to a fixed number of citizen
// soldiers (which both gather and fight in 0.28 — there are no dedicated
// workers), then attack the nearest enemy entity and keep sweeping until
// every enemy unit and structure is gone (Conquest requires all of them).
// Everything here is meant to be replaced by evidence-driven changes in
// later turns.

import { BaseAI } from "simulation/ai/common-api/baseAI.js";
import * as filters from "simulation/ai/common-api/filters.js";
import { SquareVectorDistance } from "simulation/ai/common-api/utils.js";

const SOLDIER_TARGET = 50;
const ATTACK_THRESHOLD = SOLDIER_TARGET;
// Army scaling (G4a): 50 citizen soldiers; pop support: 8 houses.
const HOUSE_TARGET = 8;
// City Phase requires 3 Town-class structures; forges carry the Town class
// (VisibleClasses "Town Forge"), cost 200 wood, and have no entity limits.
const FORGE_TARGET = 3;
// Forge placement rings: 16 candidates at 72 m plus 16 at 88 m around the
// CC. The single 72 m ring exhausted itself on terrain on half the seeds
// (turn 022); forges require clearance from existing structures (22x22
// footprint), which the structureClear walk applies.
const FORGE_OFFSETS = [];
for (let i = 0; i < 16; ++i)
{
	const angle = i * Math.PI / 8;
	FORGE_OFFSETS.push([
		Math.round(72 * Math.cos(angle)),
		Math.round(72 * Math.sin(angle))
	]);
}
for (let i = 0; i < 16; ++i)
{
	const angle = i * Math.PI / 8 + Math.PI / 16;
	FORGE_OFFSETS.push([
		Math.round(88 * Math.cos(angle)),
		Math.round(88 * Math.sin(angle))
	]);
}
const FORGE_CLEARANCE_SQ = 28 * 28;
// Siege endgame: one arsenal (300 wood, needs City) trains the rams. Three
// rams total; the attack starts when two exist.
const ARSENAL_TARGET = 1;
const RAM_TARGET = 3;
// House placement: houses 1-5 use the proven fixed offsets (fast pre-town);
// houses 6-8 and the fallback use the clearance ring.
const FIXED_HOUSE_OFFSETS = [[64, 0], [-64, 0], [0, 64], [0, -64], [45, 45], [-45, 45], [45, -45], [-45, -45]];
const HOUSE_OFFSETS = [];
for (let i = 0; i < 16; ++i)
{
	const angle = i * Math.PI / 8;
	HOUSE_OFFSETS.push([
		Math.round(56 * Math.cos(angle)),
		Math.round(56 * Math.sin(angle))
	]);
}
for (let i = 0; i < 16; ++i)
{
	const angle = i * Math.PI / 8 + Math.PI / 16;
	HOUSE_OFFSETS.push([
		Math.round(64 * Math.cos(angle)),
		Math.round(64 * Math.sin(angle))
	]);
}
const HOUSE_CLEARANCE_SQ = 26 * 26;
// Post-town, a fixed share of the army gathers the City Phase resources:
// id % 16 < 3 → stone, < 5 → metal (≈ 6 + 4 of the 32-soldier army). Stone
// mines sit farther out, so stone gets more hands. The rest keep the 2:1
// wood:food split. (Turn 016 evidence: this carve-out is economy-safe but
// starts too late; the starting workers close the gap — see manageWorkers.)
const SHARE_MOD = 16;
const STONE_SHARE = 3;
const METAL_SHARE = 2;
// print() in the AI realm does not append newlines.
const hlog = msg => print("[HARNESS] " + msg + "\n");

export function VercingetorixBot(settings)
{
	BaseAI.call(this, settings);
	this.playedTurn = 0;
	this.attackStarted = false;
	this.reportMinute = 0;
	this.finalReported = false;
	this.houseAttempts = 0;
	this.townResearched = false;
	this.forgeAttempts = 0;
	this.cityAttempted = false;
	this.arsenalAttempts = 0;
}

VercingetorixBot.prototype = Object.create(BaseAI.prototype);

VercingetorixBot.prototype.Serialize = function()
{
	return {
		"playedTurn": this.playedTurn,
		"attackStarted": this.attackStarted,
		"reportMinute": this.reportMinute,
		"finalReported": this.finalReported,
		"houseAttempts": this.houseAttempts,
		"townResearched": this.townResearched,
		"forgeAttempts": this.forgeAttempts,
		"cityAttempted": this.cityAttempted,
		"arsenalAttempts": this.arsenalAttempts
	};
};

VercingetorixBot.prototype.Deserialize = function(data)
{
	this.playedTurn = data.playedTurn;
	this.attackStarted = data.attackStarted;
	this.reportMinute = data.reportMinute;
	this.finalReported = data.finalReported;
	this.houseAttempts = data.houseAttempts;
	this.townResearched = data.townResearched;
	this.forgeAttempts = data.forgeAttempts || 0;
	this.cityAttempted = data.cityAttempted || false;
	this.arsenalAttempts = data.arsenalAttempts || 0;
	this.isDeserialized = true;
};

// Research Town Phase once the 500 food / 500 wood are available AND the
// sim says the requirements are met; then City once 750/750 are banked and
// the sim's requirements (3 Town structures) pass. canResearch is the sim's
// own gate — it was false for every Town post since turn 011 (turn 018).
VercingetorixBot.prototype.manageResearch = function(gameState, cc)
{
	const techs = cc.researchableTechs(gameState, gameState.getPlayerCiv());
	if (!techs)
		return;
	if (!this.townResearched)
	{
		const townTech = techs.find(t => t.startsWith("phase_town"));
		if (!townTech)
			return;
		const res = gameState.getResources();
		if (res.food >= 500 && res.wood >= 500 && gameState.canResearch(townTech))
		{
			cc.research(townTech);
			this.townResearched = true;
			return;
		}
	}
	if (this.cityAttempted || gameState.currentPhase() < 2)
		return;
	const cityTech = techs.find(t => t.startsWith("phase_city"));
	if (!cityTech)
		return;
	// City needs 3 Town-class structures (the forges) — canResearch is the
	// sim's gate for that, the resources are the bot's.
	const res = gameState.getResources();
	if (res.stone >= 750 && res.metal >= 750 && gameState.canResearch(cityTech))
	{
		cc.research(cityTech);
		this.cityAttempted = true;
	}
};

VercingetorixBot.prototype.CustomInit = function(gameState)
{
	this.chat("Vercingetorix skeleton online.");
};

VercingetorixBot.prototype.OnUpdate = function(sharedAI)
{
	if (this.gameFinished || this.gameState.playerData.state == "defeated")
		return;

	// Think every 8 turns, offset per player like Petra, to spread load.
	if (!this.playedTurn || (this.turn + this.player) % 8 == 5)
	{
		this.playedTurn++;
		this.play(this.gameState);
	}

	this.report(this.gameState);
	this.turn++;
};

VercingetorixBot.prototype.play = function(gameState)
{
	const cc = this.ownCivCentre(gameState);
	if (!cc)
		return;

	// Gather candidates once per tick: gaia resources (trees have no
	// Identity classes — identify by ResourceSupply), restricted to a safe
	// radius around the CC (venturing further got gatherers killed).
	// Positions are in meters, 4 m per tile: 40 tiles = 160 m.
	const woodResources = [];
	const foodResources = [];
	const maxDistSq = 160 * 160;
	// Auto-maintained caches replace the full-map getEntities() scan. The
	// filters only select resource supplies; ownership, position and distance
	// are still applied here so behavior is unchanged.
	const woodCache = gameState.updatingGlobalCollection("resource-wood",
		{ "func": ent => ent.getResourceType() == "wood", "dynamicProperties": [] },
		gameState.getEntities());
	const foodCache = gameState.updatingGlobalCollection("resource-food",
		{ "func": ent => ent.getResourceType() == "food", "dynamicProperties": [] },
		gameState.getEntities());
	for (const ent of woodCache.values())
	{
		if (ent.owner() !== 0 || !ent.position())
			continue;
		if (SquareVectorDistance(cc.position(), ent.position()) > maxDistSq)
			continue;
		woodResources.push(ent);
	}
	for (const ent of foodCache.values())
	{
		if (ent.owner() !== 0 || !ent.position())
			continue;
		if (SquareVectorDistance(cc.position(), ent.position()) > maxDistSq)
			continue;
		foodResources.push(ent);
	}
	// Stone/metal mines are placed ≥ 20 tiles from player territory (mainland
	// map script), so the 160 m wood/food cap hides them. Scan the whole map:
	// mines are a few dozen entities, cheap to filter. Gatherers walk to the
	// nearest one, whatever the distance.
	const stoneCache = gameState.updatingGlobalCollection("resource-stone",
		{ "func": ent => ent.getResourceType() == "stone", "dynamicProperties": [] },
		gameState.getEntities());
	const metalCache = gameState.updatingGlobalCollection("resource-metal",
		{ "func": ent => ent.getResourceType() == "metal", "dynamicProperties": [] },
		gameState.getEntities());
	const stoneResources = [];
	const metalResources = [];
	for (const ent of stoneCache.values())
		if (ent.owner() === 0 && ent.position())
			stoneResources.push(ent);
	for (const ent of metalCache.values())
		if (ent.owner() === 0 && ent.position())
			metalResources.push(ent);

	this.manageResearch(gameState, cc);
	this.manageWorkers(gameState, stoneResources, metalResources, foodResources);
	this.manageHouses(gameState, cc);
	this.manageForges(gameState, cc);
	this.manageArsenal(gameState, cc);
	this.manageRams(gameState);
	this.manageSoldiers(gameState, cc, woodResources, foodResources, stoneResources, metalResources);
};

VercingetorixBot.prototype.ownCivCentre = function(gameState)
{
	const ccs = gameState.getOwnEntities().filter(filters.byClass("CivCentre"));
	return ccs.length ? ccs.values().next().value : undefined;
};

// Nearest enemy entity (unit or structure). Gaia (owner 0) is excluded:
// attacking trees would waste the army.
VercingetorixBot.prototype.nearestEnemyEntity = function(gameState, reference)
{
	let best;
	let bestDist = Infinity;
	for (const ent of gameState.getEntities().values())
	{
		const owner = ent.owner();
		if (owner === this.player || owner === 0)
			continue;
		// Entities mid-destruction may have no position.
		if (!ent.position())
			continue;
		const dist = SquareVectorDistance(reference.position(), ent.position());
		if (dist < bestDist)
		{
			bestDist = dist;
			best = ent;
		}
	}
	return best;
};

VercingetorixBot.prototype.nearestResource = function(worker, resources)
{
	let best;
	let bestDist = Infinity;
	for (const res of resources)
	{
		const dist = SquareVectorDistance(worker.position(), res.position());
		if (dist < bestDist)
		{
			bestDist = dist;
			best = res;
		}
	}
	return best;
};

// The civic centre only provides 20 population; houses give 5 each. When
// the cap is near and wood allows, send a builder to raise a house next to
// the CC. Retries are driven by the actual house count (built or
// foundation), never by a burnt counter — a failed placement just retries.
VercingetorixBot.prototype.manageHouses = function(gameState, cc)
{
	const houseTemplate = gameState.applyCiv("structures/{civ}/house");

	// A foundation is placed but not built by the construct command (the
	// API helper posts autorepair:false); the actual construction is a
	// separate repair order. Send a unit that *can build houses* to do it:
	// the old "any idle unit" pick could grab the cavalry javelineer, which
	// has no Builder mixin — the order silently does nothing and the
	// foundation stalls forever (turn 019 invalid run).
	const foundations = gameState.getOwnEntities().filter(filters.byClass("Foundation"));
	if (foundations.length)
	{
		const foundation = foundations.values().next().value;
		for (const ent of gameState.getOwnEntities().values())
		{
			const buildable = ent.buildableEntities(gameState.getPlayerCiv());
			if (buildable && buildable.indexOf(houseTemplate) !== -1)
			{
				ent.repair(foundation);
				break;
			}
		}
		return;
	}

	const houses = gameState.getOwnEntities().filter(filters.byClass("House"));
	if (houses.length >= HOUSE_TARGET)
		return;
	// Only the 5 Village-requirement houses pre-town — the extra pop houses
	// come after Town (the pre-town budget is 1100 wood + 500 food with 5
	// gatherer hands, and 8 houses delayed Town by 1-2 minutes on the
	// marginal seeds, turn 029 iteration 3).
	if (!this.townResearched && houses.length >= 5)
		return;

	const template = gameState.getTemplate(houseTemplate);
	const woodRaw = template ? template.get("Cost/Resources/wood") : undefined;
	if (woodRaw === undefined)
		return;
	const woodCost = +woodRaw;
	if (gameState.getResources().wood < woodCost)
		return;

	let builder;
	for (const ent of gameState.getOwnEntities().values())
	{
		const buildable = ent.buildableEntities(gameState.getPlayerCiv());
		if (buildable && buildable.indexOf(houseTemplate) !== -1)
		{
			builder = ent;
			break;
		}
	}
	if (!builder)
		return;

	const pos = cc.position();
	const candidates =
		houses.length < 5 && this.houseAttempts < FIXED_HOUSE_OFFSETS.length ?
			FIXED_HOUSE_OFFSETS : HOUSE_OFFSETS;
	for (let i = 0; i < candidates.length; ++i)
	{
		const candidate = candidates[(this.houseAttempts + i) % candidates.length];
		const x = pos[0] + candidate[0];
		const z = pos[1] + candidate[1];
		if (candidates === FIXED_HOUSE_OFFSETS ||
		    this.structureClear(gameState, x, z, HOUSE_CLEARANCE_SQ))
		{
			builder.construct(houseTemplate, x, z, 0, undefined);
			break;
		}
	}
	this.houseAttempts++;
};

// True when (x, z) is at least the clearance distance from every own
// structure (the sim silently rejects placements that overlap anything).
VercingetorixBot.prototype.structureClear = function(gameState, x, z, minDistSq)
{
	for (const ent of gameState.getOwnEntities().values())
	{
		if (!ent.hasClass("Structure") || !ent.position())
			continue;
		if (SquareVectorDistance([x, z], ent.position()) < minDistSq)
			return false;
	}
	return true;
};

// Three forges for the City Phase requirement (each carries the sim's Town
// class). Same foundation/repair pattern as houses, after real Town only.
// Placement walks the dedicated double ring with structure clearance — the
// house offsets are exhausted by the 5 houses (turn 021), and the single
// 72 m ring lost to terrain on half the seeds (turn 022).
VercingetorixBot.prototype.manageForges = function(gameState, cc)
{
	if (gameState.currentPhase() < 2)
		return;

	const forgeTemplate = gameState.applyCiv("structures/{civ}/forge");

	const foundations = gameState.getOwnEntities().filter(filters.byClass("Foundation"));
	if (foundations.length)
	{
		const foundation = foundations.values().next().value;
		for (const ent of gameState.getOwnEntities().values())
		{
			const buildable = ent.buildableEntities(gameState.getPlayerCiv());
			if (buildable && buildable.indexOf(forgeTemplate) !== -1)
			{
				ent.repair(foundation);
				break;
			}
		}
		return;
	}

	const forges = gameState.getOwnEntities().filter(filters.byClass("Forge"));
	if (forges.length >= FORGE_TARGET)
		return;

	const template = gameState.getTemplate(forgeTemplate);
	const woodRaw = template ? template.get("Cost/Resources/wood") : undefined;
	if (woodRaw === undefined)
		return;
	if (gameState.getResources().wood < +woodRaw)
		return;

	let builder;
	for (const ent of gameState.getOwnEntities().values())
	{
		const buildable = ent.buildableEntities(gameState.getPlayerCiv());
		if (buildable && buildable.indexOf(forgeTemplate) !== -1)
		{
			builder = ent;
			break;
		}
	}
	if (!builder)
		return;

	const pos = cc.position();
	for (let i = 0; i < FORGE_OFFSETS.length; ++i)
	{
		const candidate = FORGE_OFFSETS[(this.forgeAttempts + i) % FORGE_OFFSETS.length];
		const x = pos[0] + candidate[0];
		const z = pos[1] + candidate[1];
		if (this.structureClear(gameState, x, z, FORGE_CLEARANCE_SQ))
		{
			builder.construct(forgeTemplate, x, z, 0, undefined);
			break;
		}
	}
	this.forgeAttempts++;
};

// One arsenal in City Phase: it trains the siege rams. Same
// foundation/repair pattern, placed on the forge double ring with clearance.
VercingetorixBot.prototype.manageArsenal = function(gameState, cc)
{
	if (gameState.currentPhase() < 3)
		return;

	const arsenalTemplate = gameState.applyCiv("structures/{civ}/arsenal");

	const foundations = gameState.getOwnEntities().filter(filters.byClass("Foundation"));
	if (foundations.length)
	{
		const foundation = foundations.values().next().value;
		for (const ent of gameState.getOwnEntities().values())
		{
			const buildable = ent.buildableEntities(gameState.getPlayerCiv());
			if (buildable && buildable.indexOf(arsenalTemplate) !== -1)
			{
				ent.repair(foundation);
				break;
			}
		}
		return;
	}

	let arsenalCount = 0;
	for (const ent of gameState.getOwnEntities().filter(filters.byClass("Arsenal")).values())
		if (!ent.hasClass("Foundation"))
			arsenalCount++;
	if (arsenalCount >= ARSENAL_TARGET)
		return;

	const template = gameState.getTemplate(arsenalTemplate);
	const woodRaw = template ? template.get("Cost/Resources/wood") : undefined;
	if (woodRaw === undefined)
		return;
	if (gameState.getResources().wood < +woodRaw)
		return;

	let builder;
	for (const ent of gameState.getOwnEntities().values())
	{
		const buildable = ent.buildableEntities(gameState.getPlayerCiv());
		if (buildable && buildable.indexOf(arsenalTemplate) !== -1)
		{
			builder = ent;
			break;
		}
	}
	if (!builder)
		return;

	const pos = cc.position();
	for (let i = 0; i < FORGE_OFFSETS.length; ++i)
	{
		const candidate = FORGE_OFFSETS[(this.arsenalAttempts + i) % FORGE_OFFSETS.length];
		const x = pos[0] + candidate[0];
		const z = pos[1] + candidate[1];
		if (this.structureClear(gameState, x, z, FORGE_CLEARANCE_SQ))
		{
			builder.construct(arsenalTemplate, x, z, 0, undefined);
			break;
		}
	}
	this.arsenalAttempts++;
};

// Train siege rams at the arsenal once City is up and the army is complete
// (G4a: the rams steal the soldiers' wood otherwise — turn 028 iteration 4).
VercingetorixBot.prototype.manageRams = function(gameState)
{
	if (gameState.currentPhase() < 3)
		return;
	if (gameState.getOwnEntities().filter(filters.byClass("Melee")).length < SOLDIER_TARGET)
		return;
	let arsenal;
	for (const ent of gameState.getOwnEntities().filter(filters.byClass("Arsenal")).values())
		if (!ent.hasClass("Foundation"))
		{
			arsenal = ent;
			break;
		}
	if (!arsenal)
		return;

	const rams = gameState.getOwnEntities().filter(filters.byClass("Siege"));
	if (rams.length >= RAM_TARGET)
		return;

	const res = gameState.getResources();
	if (res.wood < 300 || res.metal < 150)
		return;

	arsenal.train(gameState.getPlayerCiv(), gameState.applyCiv("units/{civ}/siege_ram"), 1);
};

// The nearest enemy civic centre — the assault's target.
VercingetorixBot.prototype.nearestEnemyCivCentre = function(gameState, reference)
{
	let best;
	let bestDist = Infinity;
	for (const ent of gameState.getEntities().values())
	{
		const owner = ent.owner();
		if (owner === this.player || owner === 0 || !ent.hasClass("CivCentre"))
			continue;
		if (!ent.position())
			continue;
		const dist = SquareVectorDistance(reference.position(), ent.position());
		if (dist < bestDist)
		{
			bestDist = dist;
			best = ent;
		}
	}
	return best;
};

// The four starting support workers (Support class, not Melee — the soldier
// loop never commands them) sit idle all game. Put them on the City Phase
// resources from minute 0: two on stone, two on metal, stable by entity id.
// They gather at 0.35/s and never fight, so they are pure economy all match.
// The four starting support workers (Support class, not Melee) never fight.
// Pre-town: two on stone, two on metal (the City Phase resources). Post-town:
// two switch to food — every soldier costs 50 food, and the early food
// sources deplete on some seeds (turn 029 iteration 4); workers gather food
// at 1.0/s, twice the soldier rate.
VercingetorixBot.prototype.manageWorkers = function(gameState, stoneResources, metalResources, foodResources)
{
	for (const worker of gameState.getOwnEntities().filter(filters.byClass("Support")).values())
		if (worker.unitAIState() == "INDIVIDUAL.IDLE")
		{
			let resources;
			if (this.townResearched && worker.id() % 4 >= 2)
				resources = foodResources;
			else
				resources = worker.id() % 4 == 0 ? stoneResources : metalResources;
			const target = this.nearestResource(worker, resources);
			if (target)
				worker.gather(target);
		}
};

VercingetorixBot.prototype.manageSoldiers = function(gameState, cc, woodResources, foodResources, stoneResources, metalResources)
{
	// The Trainer list uses "units/{civ}/..." (slash), unlike older versions.
	const spearTemplate = gameState.applyCiv("units/{civ}/infantry_spearman_b");
	const soldiers = gameState.getOwnEntities().filter(filters.byClass("Melee"));
	// All citizen soldiers gather — including the two starting javelineers
	// and the cavalry javelineer, which the old Melee-only filter left idle
	// all game (turn 019: the pre-town economy needs their hands to afford
	// the 5 Village houses + the Town research).
	const gatherers = gameState.getOwnEntities().filter(filters.byClass("CitizenSoldier"));

	// Grow to the target, then keep replenishing losses up to it. Hold
	// training until Town Phase is researched so the 500 food/wood for the
	// research can accumulate instead of being spent on soldiers. After
	// Town, train freely — every soldier is a gatherer, so the army
	// compounds (G4a).
	if (this.townResearched && soldiers.length < SOLDIER_TARGET)
		cc.train(gameState.getPlayerCiv(), spearTemplate, 1);

	// Pre-town: two thirds wood, one third food — the Village phase needs
	// 1100 wood (8 houses + the Town research) but only 500 food. Post-town:
	// half wood, half food — every soldier costs 50 food AND 50 wood (the
	// base infantry template's 50 food is inherited by the spearman, turn
	// 029 diagnosis), so 1:1 balances the two 50-costs.
	for (const gatherer of gatherers.values())
		if (!this.attackStarted && gatherer.unitAIState() == "INDIVIDUAL.IDLE")
		{
			const share = gatherer.id() % SHARE_MOD;
			let resources;
			if (this.townResearched && share < STONE_SHARE)
				resources = stoneResources;
			else if (this.townResearched && share < STONE_SHARE + METAL_SHARE)
				resources = metalResources;
			else if (this.townResearched)
				resources = gatherer.id() % 2 == 0 ? foodResources : woodResources;
			else
				resources = gatherer.id() % 3 == 0 ? foodResources : woodResources;
			const target = this.nearestResource(gatherer, resources);
			if (target)
				gatherer.gather(target);
		}
	// Attack when two rams exist — one ram alone dies to the garrison
	// arrows; two split them. The army escorts from here.
	const rams = gameState.getOwnEntities().filter(filters.byClass("Siege"));
	if (!this.attackStarted && rams.length >= 2)
	{
		this.attackStarted = true;
		this.chat("Vercingetorix attacks!");
	}

	// Sweep: after the attack starts, every soldier not already fighting
	// attack-moves at the enemy civic centre — the objective. Gathering
	// soldiers are interrupted too (turn 026 iteration 5).
	if (this.attackStarted)
		for (const soldier of soldiers.values())
		{
			const state = soldier.unitAIState();
			if (state && state.startsWith("INDIVIDUAL.COMBAT"))
				continue;
			const target = this.nearestEnemyCivCentre(gameState, soldier);
			if (target)
				soldier.attackMove(target.position()[0], target.position()[1], ["Unit", "Structure"]);
		}
	// Rams go straight for the civic centre — that is the victory condition.
	if (this.attackStarted)
		for (const ram of gameState.getOwnEntities().filter(filters.byClass("Siege")).values())
			if (ram.unitAIState() == "INDIVIDUAL.IDLE")
			{
				const target = this.nearestEnemyCivCentre(gameState, ram);
				if (target)
					ram.attack(target.id());
			}
};

VercingetorixBot.prototype.report = function(gameState)
{
	const state = gameState.playerData.state;
	if (state != "active")
	{
		if (!this.finalReported)
		{
			this.finalReported = true;
			hlog('{"event":"end","state":"' + state + '","t":' +
				gameState.getTimeElapsed() + '}');
		}
		return;
	}

	const minute = Math.floor(gameState.getTimeElapsed() / 60000);
	if (minute <= this.reportMinute)
		return;
	this.reportMinute = minute;

	const melee = gameState.getOwnEntities().filter(filters.byClass("Melee"));
	const states = {};
	for (const s of gameState.getOwnEntities().values())
	{
		const st = s.unitAIState();
		states[st] = (states[st] || 0) + 1;
	}
	const res = gameState.getResources();
	hlog('{"event":"sample","t":' + minute + ',"melee":' + melee.length +
		',"attack":' + this.attackStarted +
		',"food":' + res.food + ',"wood":' + res.wood +
		',"stone":' + res.stone + ',"metal":' + res.metal +
		',"pop":"' + gameState.getPopulation() + '/' + gameState.getPopulationLimit() + '"' +
		',"houses":' + gameState.getOwnEntities().filter(filters.byClass("House")).length +
		',"foundations":' + gameState.getOwnEntities().filter(filters.byClass("Foundation")).length +
		',"town":' + (this.townResearched ? "true" : "false") +
		',"phase":' + gameState.currentPhase() +
		',"villageClass":' + (gameState.playerData.classCounts["Village"] || 0) +
		',"townClass":' + (gameState.playerData.classCounts["Town"] || 0) +
		',"forges":' + gameState.getOwnEntities().filter(filters.byClass("Forge")).length +
		',"arsenal":' + gameState.getOwnEntities().filter(filters.byClass("Arsenal")).length +
		',"rams":' + gameState.getOwnEntities().filter(filters.byClass("Siege")).length +

		',"townCan":' + (() => {
			const cc = this.ownCivCentre(gameState);
			const t = cc && cc.researchableTechs(gameState, gameState.getPlayerCiv());
			const townTech = t && t.find(x => x.startsWith("phase_town"));
			return townTech ? gameState.canResearch(townTech) : "noTech";
		})() +
		',"states":' + JSON.stringify(states) + '}');
};
