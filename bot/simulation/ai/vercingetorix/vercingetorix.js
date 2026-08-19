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

const SOLDIER_TARGET = 20;
const ATTACK_THRESHOLD = SOLDIER_TARGET;
const HOUSE_TARGET = 4;
// House placement offsets around the civic centre, in meters
// (4 m per tile, so these are 16 tiles out).
const HOUSE_OFFSETS = [[64, 0], [-64, 0], [0, 64], [0, -64]];

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
}

VercingetorixBot.prototype = Object.create(BaseAI.prototype);

VercingetorixBot.prototype.Serialize = function()
{
	return {
		"playedTurn": this.playedTurn,
		"attackStarted": this.attackStarted,
		"reportMinute": this.reportMinute,
		"finalReported": this.finalReported,
		"houseAttempts": this.houseAttempts
	};
};

VercingetorixBot.prototype.Deserialize = function(data)
{
	this.playedTurn = data.playedTurn;
	this.attackStarted = data.attackStarted;
	this.reportMinute = data.reportMinute;
	this.finalReported = data.finalReported;
	this.houseAttempts = data.houseAttempts;
	this.isDeserialized = true;
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
	for (const ent of gameState.getEntities().values())
	{
		const type = ent.getResourceType();
		if (ent.owner() !== 0 || (type != "wood" && type != "food"))
			continue;
		if (!ent.position())
			continue;
		if (SquareVectorDistance(cc.position(), ent.position()) > maxDistSq)
			continue;
		(type == "wood" ? woodResources : foodResources).push(ent);
	}

	this.manageHouses(gameState, cc);
	this.manageSoldiers(gameState, cc, woodResources, foodResources);
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
	// A foundation is placed but not built by the construct command (the
	// API helper posts autorepair:false); the actual construction is a
	// separate repair order. Send an idle unit to build the pending
	// foundation.
	const foundations = gameState.getOwnEntities().filter(filters.byClass("Foundation"));
	if (foundations.length)
	{
		const foundation = foundations.values().next().value;
		for (const ent of gameState.getOwnEntities().values())
			if (ent.unitAIState() == "INDIVIDUAL.IDLE")
			{
				ent.repair(foundation);
				break;
			}
		return;
	}

	const houses = gameState.getOwnEntities().filter(filters.byClass("House"));
	if (houses.length >= HOUSE_TARGET)
		return;
	if (gameState.getPopulation() + 2 < gameState.getPopulationLimit())
		return;

	const houseTemplate = gameState.applyCiv("structures/{civ}/house");
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

	const offset = HOUSE_OFFSETS[this.houseAttempts % HOUSE_OFFSETS.length];
	const pos = cc.position();
	builder.construct(houseTemplate, pos[0] + offset[0], pos[1] + offset[1], 0, undefined);
	this.houseAttempts++;
};

VercingetorixBot.prototype.manageSoldiers = function(gameState, cc, woodResources, foodResources)
{
	// The Trainer list uses "units/{civ}/..." (slash), unlike older versions.
	const spearTemplate = gameState.applyCiv("units/{civ}/infantry_spearman_b");
	const soldiers = gameState.getOwnEntities().filter(filters.byClass("Melee"));

	// Grow to the target, then keep replenishing losses up to it.
	if (soldiers.length < SOLDIER_TARGET)
		cc.train(gameState.getPlayerCiv(), spearTemplate, 1);

	// The same units gather while we are still growing. Wood is the
	// binding resource (spearmen and houses cost wood), so two thirds of
	// the gatherers take wood and one third food (stable split by entity id).
	for (const soldier of soldiers.values())
		if (!this.attackStarted && soldier.unitAIState() == "INDIVIDUAL.IDLE")
		{
			const resources = soldier.id() % 3 == 0 ? foodResources : woodResources;
			const target = this.nearestResource(soldier, resources);
			if (target)
				soldier.gather(target);
		}
	if (!this.attackStarted && soldiers.length >= ATTACK_THRESHOLD)
	{
		this.attackStarted = true;
		this.chat("Vercingetorix attacks!");
	}

	// Sweep: idle soldiers attack-move at the nearest enemy entity. The
	// target is recomputed every tick, so the army works through the whole
	// enemy base — Conquest needs every unit and structure destroyed.
	if (this.attackStarted)
		for (const soldier of soldiers.values())
			if (soldier.unitAIState() == "INDIVIDUAL.IDLE")
			{
				const target = this.nearestEnemyEntity(gameState, soldier);
				if (target)
					soldier.attackMove(target.position()[0], target.position()[1], ["Unit", "Structure"]);
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
		',"pop":"' + gameState.getPopulation() + '/' + gameState.getPopulationLimit() + '"' +
		',"houses":' + gameState.getOwnEntities().filter(filters.byClass("House")).length +
		',"foundations":' + gameState.getOwnEntities().filter(filters.byClass("Foundation")).length +
		',"states":' + JSON.stringify(states) + '}');
};
