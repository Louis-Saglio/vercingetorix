// Vercingetorix — do-nothing baseline.
//
// The bot issues no orders: units keep their default UnitAI behavior
// (starting units stand idle, buildings do nothing). The strategy that
// used to live here was reset — future turns rebuild it from the game
// reference in docs/game_description/.
//
// What remains is the observability harness consumers rely on:
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
}

VercingetorixBot.prototype = Object.create(BaseAI.prototype);

VercingetorixBot.prototype.Serialize = function()
{
	return {
		"reportMinute": this.reportMinute,
		"finalReported": this.finalReported
	};
};

VercingetorixBot.prototype.Deserialize = function(data)
{
	this.reportMinute = data.reportMinute;
	this.finalReported = data.finalReported;
	this.isDeserialized = true;
};

VercingetorixBot.prototype.CustomInit = function(gameState)
{
	this.chat("Vercingetorix do-nothing baseline online.");
};

VercingetorixBot.prototype.OnUpdate = function(sharedAI)
{
	// The bot issues no orders, so there is nothing to guard against after
	// defeat — and report() must keep running to emit the end event.
	this.report(this.gameState);
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
