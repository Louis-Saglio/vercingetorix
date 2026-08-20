// Vercingetorix — turn 001: idle starting units gather the nearest suitable
// resource supply around the civil centre (see turns/001-gather-starting-workers.md).
//
// Observability harness consumers rely on:
//  - a per-minute [HARNESS] {"event":"sample",...} JSON line with neutral
//    state (time, resources, population, unit-state histogram) — the
//    harness report tool reads "pop" from these samples;
//  - a final [HARNESS] {"event":"end","state":...} line when the player
//    leaves the active state.

import { BaseAI } from "simulation/ai/common-api/baseAI.js";

// print() in the AI realm does not append newlines.
const hlog = msg => print("[HARNESS] " + msg + "\n");

export function VercingetorixBot(settings)
{
	BaseAI.call(this, settings);
	this.reportMinute = 0;
	this.finalReported = false;

	// Gathering (turn 001): cached resource-supply ids around the civil
	// centre; refreshed with a larger radius when exhausted.
	this.turn = 0;
	this.supplyIds = null;
	this.supplyRadius = 140;
}

VercingetorixBot.prototype = Object.create(BaseAI.prototype);

VercingetorixBot.prototype.Serialize = function()
{
	return {
		"reportMinute": this.reportMinute,
		"finalReported": this.finalReported,
		"turn": this.turn,
		"supplyIds": this.supplyIds,
		"supplyRadius": this.supplyRadius
	};
};

VercingetorixBot.prototype.Deserialize = function(data)
{
	this.reportMinute = data.reportMinute;
	this.finalReported = data.finalReported;
	this.turn = data.turn;
	this.supplyIds = data.supplyIds;
	this.supplyRadius = data.supplyRadius;
	this.isDeserialized = true;
};

VercingetorixBot.prototype.CustomInit = function(gameState)
{
	this.chat("Vercingetorix do-nothing baseline online.");
};

VercingetorixBot.prototype.OnUpdate = function(sharedAI)
{
	if (this.gameState.playerData.state == "active")
	{
		// Play decisions run every 8th sim turn (throttle).
		if (++this.turn % 8 === 0)
			this.play(this.gameState);
	}
	this.report(this.gameState);
};

VercingetorixBot.prototype.play = function(gameState)
{
	if (!this.supplyIds)
		this.cacheSupplies(gameState);
	if (!this.supplyIds)
		return; // no civil centre yet — retry next play tick

	// Turn 004: steer idle gatherers by need — food while food gatherers are
	// below 75 % of all gatherers, wood otherwise (G1 needs ~4:1 food:wood).
	let foodWorkers = 0;
	let gatherers = 0;
	for (const ent of gameState.getOwnEntities().values())
	{
		if (!ent.isGatherer())
			continue;
		++gatherers;
		const orders = ent.unitAIOrderData();
		if (orders && orders.length && orders[0].target !== undefined)
		{
			const target = gameState.getEntityById(orders[0].target);
			if (target && target.getResourceType() == "food")
				++foodWorkers;
		}
	}

	for (const ent of gameState.getOwnEntities().values())
	{
		if (ent.hasClass("CivCentre"))
			this.trainWorker(gameState, ent);
		if (!ent.isGatherer() || !ent.isIdle() || !ent.position())
			continue;
		const rates = ent.resourceGatherRates();
		if (!rates)
			continue;
		let wanted;
		if (this.canGather(rates, "food") && foodWorkers * 4 < gatherers * 3)
			wanted = "food";
		else if (this.canGather(rates, "wood"))
			wanted = "wood";
		let target = this.nearestSupply(gameState, ent, wanted);
		if (!target && wanted)
			target = this.nearestSupply(gameState, ent, undefined);
		if (target)
		{
			ent.gather(target);
			if (target.getResourceType() == "food")
				++foodWorkers;
		}
	}
};

VercingetorixBot.prototype.canGather = function(rates, generic)
{
	for (const type in rates)
		if (type.split(".")[0] == generic && rates[type] > 0)
			return true;
	return false;
};

// Turn 002: keep the civil centre training workers while food and
// population room allow; at most one item queued (reservations lock
// population and food, and training blocked at the cap fails silently).
VercingetorixBot.prototype.trainWorker = function(gameState, cc)
{
	if (gameState.getResources().food < 50 ||
		gameState.getPopulation() >= gameState.getPopulationLimit())
		return;
	const queue = cc.trainingQueue();
	if (queue && queue.length)
		return;
	cc.train(gameState.playerData.civ,
		gameState.applyCiv("units/{civ}/support_civilian"), 1);
};

// One scan for resource supplies around the civil centre; rerun with a
// grown radius when everything cached is exhausted.
VercingetorixBot.prototype.cacheSupplies = function(gameState)
{
	let cc;
	for (const ent of gameState.getOwnEntities().values())
		if (ent.hasClass("CivCentre") && ent.position())
		{
			cc = ent;
			break;
		}
	if (!cc)
		return;

	const ccPos = cc.position();
	const maxDistSq = this.supplyRadius * this.supplyRadius;
	const ids = [];
	for (const ent of gameState.getEntities().values())
	{
		const pos = ent.position();
		if (!pos || !ent.get("ResourceSupply"))
			continue;
		const dx = pos[0] - ccPos[0];
		const dz = pos[1] - ccPos[1];
		if (dx * dx + dz * dz <= maxDistSq)
			ids.push(ent.id());
	}
	this.supplyIds = ids;
};

VercingetorixBot.prototype.nearestSupply = function(gameState, ent, wanted)
{
	if (!this.supplyIds)
		return undefined; // widened this play tick — rescan happens next tick
	const rates = ent.resourceGatherRates();
	if (!rates)
		return undefined;
	const pos = ent.position();
	let best;
	let bestDistSq = Infinity;
	for (const id of this.supplyIds)
	{
		const supply = gameState.getEntityById(id);
		if (!supply || !supply.position() || supply.resourceSupplyAmount() <= 0)
			continue;
		const type = supply.resourceSupplyType();
		if (!type || !(rates[type.generic + "." + type.specific] || rates[type.generic]))
			continue;
		if (wanted && type.generic != wanted)
			continue;
		const sPos = supply.position();
		const dx = sPos[0] - pos[0];
		const dz = sPos[1] - pos[1];
		const distSq = dx * dx + dz * dz;
		if (distSq < bestDistSq)
		{
			bestDistSq = distSq;
			best = supply;
		}
	}
	if (!best && this.supplyRadius < 500)
	{
		// Everything cached is exhausted or unsuitable — widen the search.
		this.supplyRadius += 80;
		this.supplyIds = null;
	}
	return best;
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

	const states = {};
	for (const ent of gameState.getOwnEntities().values())
	{
		const st = ent.unitAIState();
		states[st] = (states[st] || 0) + 1;
	}
	const res = gameState.getResources();
	hlog('{"event":"sample","t":' + minute +
		',"food":' + res.food + ',"wood":' + res.wood +
		',"stone":' + res.stone + ',"metal":' + res.metal +
		',"pop":"' + gameState.getPopulation() + '/' + gameState.getPopulationLimit() + '"' +
		',"states":' + JSON.stringify(states) + '}');
};
