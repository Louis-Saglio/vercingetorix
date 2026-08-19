# Report — baseline vs treatment

Settings: `-autostart=random/mainland -autostart-seed=<seed> -autostart-biome=generic/temperate -autostart-placement=circle -autostart-nonvisual -autostart-players=2 -autostart-size=128 -autostart-victory=conquest_civic_centers -autostart-ai=1:vercingetorix -autostart-ai=2:petra -autostart-aidiff=2:0 -autostart-civ=1:gaul -autostart-civ=2:rome -autostart-player=-1 -unique-logs -nosound -mod=public -mod=vercingetorix`

## Canary

PASS

## Pairs

| seed | base | treatment | outcome | survival | total | JS errors (base→treat) |
|---|---|---|---|---|---|---|
| 221 | draw | draw | +0.00 | +0.10 | +0.18 | 0→0 |
| 222 | draw | draw | +0.00 | +0.10 | +1.07 | 0→0 |
| 223 | draw | draw | +0.00 | +0.10 | +0.58 | 0→0 |
| 224 | draw | draw | +0.00 | +0.10 | +1.06 | 0→0 |
| 225 | draw | draw | +0.00 | +0.10 | +1.06 | 0→19 |
| 226 | draw | draw | +0.00 | +0.10 | +1.00 | 0→0 |
| 227 | draw | draw | +0.00 | +0.10 | +1.65 | 0→0 |
| 228 | draw | draw | +0.00 | +0.10 | +1.07 | 0→41 |
| 229 | draw | draw | +0.00 | +0.10 | +1.08 | 0→0 |
| 230 | draw | draw | +0.00 | +0.10 | +0.95 | 0→37 |

## Metric deltas

| seed | metric | base | treatment | weighted delta |
|---|---|---|---|---|
| 221 | resourcesGathered | 3821 | 4568 | +0.078 |
| 221 | resourcesUsed | 300 | 300 | +0.000 |
| 221 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 221 | unitsTrained | 0 | 0 | +0.000 |
| 221 | populationPeak | 9 | 9 | +0.000 |
| 222 | resourcesGathered | 4694 | 7602 | +0.248 |
| 222 | resourcesUsed | 5075 | 6675 | +0.126 |
| 222 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 222 | unitsTrained | 16 | 29 | +0.325 |
| 222 | populationPeak | 22 | 37 | +0.273 |
| 223 | resourcesGathered | 3674 | 4370 | +0.076 |
| 223 | resourcesUsed | 300 | 1775 | +0.400 |
| 223 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 223 | unitsTrained | 0 | 0 | +0.000 |
| 223 | populationPeak | 9 | 9 | +0.000 |
| 224 | resourcesGathered | 4351 | 7064 | +0.249 |
| 224 | resourcesUsed | 4775 | 6175 | +0.117 |
| 224 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 224 | unitsTrained | 12 | 23 | +0.367 |
| 224 | populationPeak | 19 | 30 | +0.232 |
| 225 | resourcesGathered | 4403 | 7022 | +0.238 |
| 225 | resourcesUsed | 4775 | 6725 | +0.163 |
| 225 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 225 | unitsTrained | 13 | 24 | +0.338 |
| 225 | populationPeak | 20 | 31 | +0.220 |
| 226 | resourcesGathered | 4052 | 6203 | +0.212 |
| 226 | resourcesUsed | 4475 | 5575 | +0.098 |
| 226 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 226 | unitsTrained | 9 | 18 | +0.400 |
| 226 | populationPeak | 17 | 25 | +0.188 |
| 227 | resourcesGathered | 4878 | 8099 | +0.264 |
| 227 | resourcesUsed | 5275 | 6875 | +0.121 |
| 227 | enemyUnitsKilled | 0 | 50 | +0.400 |
| 227 | unitsTrained | 17 | 34 | +0.400 |
| 227 | populationPeak | 21 | 40 | +0.362 |
| 228 | resourcesGathered | 4764 | 7796 | +0.255 |
| 228 | resourcesUsed | 5175 | 7475 | +0.178 |
| 228 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 228 | unitsTrained | 17 | 29 | +0.282 |
| 228 | populationPeak | 22 | 36 | +0.255 |
| 229 | resourcesGathered | 4032 | 6483 | +0.243 |
| 229 | resourcesUsed | 4575 | 5875 | +0.114 |
| 229 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 229 | unitsTrained | 11 | 21 | +0.364 |
| 229 | populationPeak | 17 | 28 | +0.259 |
| 230 | resourcesGathered | 4201 | 6369 | +0.206 |
| 230 | resourcesUsed | 4575 | 6125 | +0.136 |
| 230 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 230 | unitsTrained | 11 | 20 | +0.327 |
| 230 | populationPeak | 18 | 26 | +0.178 |

## Totals

9.69 total = 0.00 outcome + 8.69 quality + 1.00 survival

**Error veto**: a pair increased the bot's JS error count.

## Verdict

bad
