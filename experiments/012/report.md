# Report — baseline vs treatment

Settings: `-autostart=random/mainland -autostart-seed=<seed> -autostart-biome=generic/temperate -autostart-placement=circle -autostart-nonvisual -autostart-players=2 -autostart-size=128 -autostart-victory=conquest_civic_centers -autostart-ai=1:vercingetorix -autostart-ai=2:petra -autostart-aidiff=2:0 -autostart-civ=1:gaul -autostart-civ=2:rome -autostart-player=-1 -unique-logs -nosound -mod=public -mod=vercingetorix`

## Canary

PASS

## Pairs

| seed | base | treatment | outcome | survival | total | JS errors (base→treat) |
|---|---|---|---|---|---|---|
| 111 | draw | draw | +0.00 | +0.00 | -1.83 | 0→0 |
| 112 | draw | draw | +0.00 | +0.00 | -1.83 | 0→0 |
| 113 | draw | draw | +0.00 | +0.00 | -1.83 | 0→0 |
| 114 | draw | draw | +0.00 | +0.00 | -1.83 | 0→0 |
| 115 | draw | draw | +0.00 | +0.00 | -1.83 | 0→0 |
| 116 | draw | draw | +0.00 | +0.00 | -1.83 | 0→0 |
| 117 | draw | draw | +0.00 | +0.00 | -1.84 | 0→0 |
| 118 | draw | draw | +0.00 | +0.00 | -1.83 | 0→0 |
| 119 | draw | draw | +0.00 | +0.00 | -1.84 | 0→0 |
| 120 | draw | draw | +0.00 | +0.00 | -1.85 | 0→0 |

## Metric deltas

| seed | metric | base | treatment | weighted delta |
|---|---|---|---|---|
| 111 | resourcesGathered | 6558 | 1139 | -0.331 |
| 111 | resourcesUsed | 3800 | 0 | -0.400 |
| 111 | enemyUnitsKilled | 900 | 0 | -0.400 |
| 111 | unitsTrained | 35 | 0 | -0.400 |
| 111 | populationPeak | 37 | 9 | -0.303 |
| 112 | resourcesGathered | 5571 | 1152 | -0.317 |
| 112 | resourcesUsed | 3900 | 0 | -0.400 |
| 112 | enemyUnitsKilled | 750 | 0 | -0.400 |
| 112 | unitsTrained | 36 | 0 | -0.400 |
| 112 | populationPeak | 40 | 9 | -0.310 |
| 113 | resourcesGathered | 5027 | 1002 | -0.320 |
| 113 | resourcesUsed | 4100 | 0 | -0.400 |
| 113 | enemyUnitsKilled | 750 | 0 | -0.400 |
| 113 | unitsTrained | 38 | 0 | -0.400 |
| 113 | populationPeak | 40 | 9 | -0.310 |
| 114 | resourcesGathered | 5115 | 990 | -0.323 |
| 114 | resourcesUsed | 5200 | 0 | -0.400 |
| 114 | enemyUnitsKilled | 1700 | 0 | -0.400 |
| 114 | unitsTrained | 49 | 0 | -0.400 |
| 114 | populationPeak | 40 | 9 | -0.310 |
| 115 | resourcesGathered | 5842 | 1174 | -0.320 |
| 115 | resourcesUsed | 4600 | 0 | -0.400 |
| 115 | enemyUnitsKilled | 600 | 0 | -0.400 |
| 115 | unitsTrained | 38 | 0 | -0.400 |
| 115 | populationPeak | 40 | 9 | -0.310 |
| 116 | resourcesGathered | 5639 | 1182 | -0.316 |
| 116 | resourcesUsed | 5100 | 0 | -0.400 |
| 116 | enemyUnitsKilled | 1800 | 0 | -0.400 |
| 116 | unitsTrained | 48 | 0 | -0.400 |
| 116 | populationPeak | 40 | 9 | -0.310 |
| 117 | resourcesGathered | 6293 | 1153 | -0.327 |
| 117 | resourcesUsed | 3900 | 0 | -0.400 |
| 117 | enemyUnitsKilled | 900 | 0 | -0.400 |
| 117 | unitsTrained | 36 | 0 | -0.400 |
| 117 | populationPeak | 40 | 9 | -0.310 |
| 118 | resourcesGathered | 5319 | 1111 | -0.316 |
| 118 | resourcesUsed | 6000 | 0 | -0.400 |
| 118 | enemyUnitsKilled | 3300 | 0 | -0.400 |
| 118 | unitsTrained | 56 | 0 | -0.400 |
| 118 | populationPeak | 40 | 9 | -0.310 |
| 119 | resourcesGathered | 6229 | 1133 | -0.327 |
| 119 | resourcesUsed | 4900 | 0 | -0.400 |
| 119 | enemyUnitsKilled | 1150 | 0 | -0.400 |
| 119 | unitsTrained | 46 | 0 | -0.400 |
| 119 | populationPeak | 40 | 9 | -0.310 |
| 120 | resourcesGathered | 6147 | 967 | -0.337 |
| 120 | resourcesUsed | 4700 | 0 | -0.400 |
| 120 | enemyUnitsKilled | 900 | 0 | -0.400 |
| 120 | unitsTrained | 40 | 0 | -0.400 |
| 120 | populationPeak | 40 | 9 | -0.310 |

## Totals

-18.33 total = 0.00 outcome + -18.33 quality + 0.00 survival

## Verdict

bad
