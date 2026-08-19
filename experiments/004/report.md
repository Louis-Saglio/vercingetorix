# Report — baseline vs treatment

Settings: `-autostart=random/mainland -autostart-seed=<seed> -autostart-biome=generic/temperate -autostart-placement=circle -autostart-nonvisual -autostart-players=2 -autostart-size=128 -autostart-victory=conquest_civic_centers -autostart-ai=1:vercingetorix -autostart-ai=2:petra -autostart-aidiff=2:0 -autostart-civ=1:gaul -autostart-civ=2:rome -autostart-player=-1 -unique-logs -nosound -mod=public -mod=vercingetorix`

## Canary

PASS

## Pairs

| seed | base | treatment | outcome | survival | total | JS errors (base→treat) |
|---|---|---|---|---|---|---|
| 21 | draw | draw | +0.00 | +0.00 | +1.21 | 0→0 |
| 22 | draw | draw | +0.00 | +0.00 | +0.68 | 0→0 |
| 23 | draw | draw | +0.00 | +0.00 | +0.65 | 0→0 |
| 24 | draw | draw | +0.00 | +0.00 | +1.43 | 0→0 |
| 25 | draw | draw | +0.00 | +0.00 | +1.54 | 0→0 |
| 26 | draw | draw | +0.00 | +0.00 | +0.28 | 0→0 |
| 27 | draw | draw | +0.00 | +0.00 | +1.51 | 0→0 |
| 28 | draw | draw | +0.00 | +0.00 | +0.29 | 0→0 |
| 29 | draw | draw | +0.00 | +0.00 | +0.08 | 0→0 |
| 30 | draw | draw | +0.00 | +0.00 | +1.34 | 0→0 |

## Metric deltas

| seed | metric | base | treatment | weighted delta |
|---|---|---|---|---|
| 21 | resourcesGathered | 3684 | 5475 | +0.194 |
| 21 | resourcesUsed | 1750 | 4950 | +0.400 |
| 21 | enemyUnitsKilled | 1800 | 2450 | +0.144 |
| 21 | unitsTrained | 16 | 48 | +0.400 |
| 21 | populationPeak | 23 | 27 | +0.070 |
| 22 | resourcesGathered | 5129 | 5376 | +0.019 |
| 22 | resourcesUsed | 3850 | 4325 | +0.049 |
| 22 | enemyUnitsKilled | 1200 | 2700 | +0.400 |
| 22 | unitsTrained | 37 | 41 | +0.043 |
| 22 | populationPeak | 22 | 31 | +0.164 |
| 23 | resourcesGathered | 4663 | 5745 | +0.093 |
| 23 | resourcesUsed | 3350 | 4025 | +0.081 |
| 23 | enemyUnitsKilled | 850 | 1450 | +0.282 |
| 23 | unitsTrained | 31 | 38 | +0.090 |
| 23 | populationPeak | 23 | 29 | +0.104 |
| 24 | resourcesGathered | 4522 | 5787 | +0.112 |
| 24 | resourcesUsed | 1550 | 4025 | +0.400 |
| 24 | enemyUnitsKilled | 150 | 1750 | +0.400 |
| 24 | unitsTrained | 14 | 38 | +0.400 |
| 24 | populationPeak | 23 | 30 | +0.122 |
| 25 | resourcesGathered | 4460 | 6900 | +0.219 |
| 25 | resourcesUsed | 2275 | 5525 | +0.400 |
| 25 | enemyUnitsKilled | 600 | 2600 | +0.400 |
| 25 | unitsTrained | 22 | 53 | +0.400 |
| 25 | populationPeak | 23 | 30 | +0.122 |
| 26 | resourcesGathered | 4445 | 5588 | +0.103 |
| 26 | resourcesUsed | 3550 | 4025 | +0.054 |
| 26 | enemyUnitsKilled | 1550 | 1450 | -0.026 |
| 26 | unitsTrained | 34 | 38 | +0.047 |
| 26 | populationPeak | 24 | 30 | +0.100 |
| 27 | resourcesGathered | 4478 | 6990 | +0.224 |
| 27 | resourcesUsed | 1550 | 4225 | +0.400 |
| 27 | enemyUnitsKilled | 450 | 1900 | +0.400 |
| 27 | unitsTrained | 14 | 40 | +0.400 |
| 27 | populationPeak | 23 | 28 | +0.087 |
| 28 | resourcesGathered | 5497 | 6332 | +0.061 |
| 28 | resourcesUsed | 3750 | 4225 | +0.051 |
| 28 | enemyUnitsKilled | 1450 | 1550 | +0.028 |
| 28 | unitsTrained | 36 | 40 | +0.044 |
| 28 | populationPeak | 23 | 29 | +0.104 |
| 29 | resourcesGathered | 5218 | 6280 | +0.081 |
| 29 | resourcesUsed | 4150 | 4025 | -0.012 |
| 29 | enemyUnitsKilled | 1550 | 1350 | -0.052 |
| 29 | unitsTrained | 40 | 38 | -0.020 |
| 29 | populationPeak | 24 | 29 | +0.083 |
| 30 | resourcesGathered | 4571 | 6285 | +0.150 |
| 30 | resourcesUsed | 2350 | 4325 | +0.336 |
| 30 | enemyUnitsKilled | 500 | 1250 | +0.400 |
| 30 | unitsTrained | 22 | 41 | +0.345 |
| 30 | populationPeak | 23 | 29 | +0.104 |

## Totals

9.00 total = 0.00 outcome + 9.00 quality + 0.00 survival

## Verdict

good
