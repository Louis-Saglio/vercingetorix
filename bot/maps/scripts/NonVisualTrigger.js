// Vercingetorix override of the engine's non-visual trigger script.
// (The autostart loads "maps/scripts/NonVisualTrigger.js"; because the
// bot mod is mounted after the public mod, this file replaces it.)
//
// Adds one behavior to the upstream script: a time limit that ends
// time-limited experiments cleanly with full statistics.

// End the experiment after this much game time (20 minutes by default).
const TIME_LIMIT_MS = 30 * 60 * 1000;

/**
 * This will print the statistics at the end of a game.
 * In order for this to work, the player's state has to be changed before the event.
 */
Trigger.prototype.EndGameAction = function()
{
	if (!this.once || Engine.QueryInterface(SYSTEM_ENTITY, IID_PlayerManager).GetActivePlayers().length)
		return;

	this.once = false;

	for (const player of Engine.GetEntitiesWithInterface(IID_StatisticsTracker))
	{
		const cmpStatisticsTracker = Engine.QueryInterface(player, IID_StatisticsTracker);
		if (cmpStatisticsTracker)
			print(cmpStatisticsTracker.GetStatisticsJSON() + "\n");
	}
};

/**
 * Time-limit end: mark every active player as won so the engine quits
 * (IsGameFinished checks for a won state) and EndGameAction prints the
 * statistics. Both players are marked won; the report tool reads that
 * combination as a time-limit draw.
 */
Trigger.prototype.TimeLimitAction = function()
{
	if (Engine.QueryInterface(SYSTEM_ENTITY, IID_Timer).GetTime() < TIME_LIMIT_MS)
		return;

	const cmpPlayerManager = Engine.QueryInterface(SYSTEM_ENTITY, IID_PlayerManager);
	const activePlayers = cmpPlayerManager.GetActivePlayers();
	if (!activePlayers.length)
		return;

	for (const playerID of activePlayers)
		QueryPlayerIDInterface(playerID).Win(undefined);
};

{
	const cmpTrigger = Engine.QueryInterface(SYSTEM_ENTITY, IID_Trigger);
	cmpTrigger.RegisterTrigger("OnPlayerWon", "EndGameAction", { "enabled": true });
	cmpTrigger.RegisterTrigger("OnPlayerDefeated", "EndGameAction", { "enabled": true });
	cmpTrigger.RegisterTrigger("OnInterval", "TimeLimitAction", { "enabled": true, "interval": 1000 });
	cmpTrigger.once = true;
}
