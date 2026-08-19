# Report — baseline vs treatment

Settings: `-autostart=random/mainland -autostart-seed=<seed> -autostart-biome=generic/temperate -autostart-placement=circle -autostart-nonvisual -autostart-players=2 -autostart-size=128 -autostart-victory=conquest_civic_centers -autostart-ai=1:vercingetorix -autostart-ai=2:petra -autostart-aidiff=2:0 -autostart-civ=1:gaul -autostart-civ=2:rome -autostart-player=-1 -unique-logs -nosound -mod=public -mod=vercingetorix`

## Canary

PASS

## Pairs

| seed | base | treatment | outcome | survival | total | JS errors (base→treat) |
|---|---|---|---|---|---|---|
| 31 | draw | draw | +0.00 | +0.00 | -0.47 | 0→0 |
| 32 | draw | draw | +0.00 | +0.00 | -0.41 | 0→0 |
| 33 | draw | draw | +0.00 | +0.00 | -0.42 | 0→0 |
| 34 | draw | draw | +0.00 | +0.00 | -0.27 | 0→0 |
| 35 | draw | draw | +0.00 | +0.00 | -0.44 | 0→0 |
| 36 | draw | draw | +0.00 | +0.00 | -0.41 | 0→0 |
| 37 | draw | draw | +0.00 | +0.00 | -0.43 | 0→0 |
| 38 | draw | draw | +0.00 | +0.00 | -0.44 | 0→0 |
| 39 | draw | draw | +0.00 | +0.00 | -0.46 | 0→0 |
| 40 | draw | draw | +0.00 | +0.00 | -0.44 | 0→0 |

## Metric deltas

| seed | metric | base | treatment | weighted delta |
|---|---|---|---|---|
| 31 | resourcesGathered | 5892 | 5890 | -0.000 |
| 31 | resourcesUsed | 5150 | 4650 | -0.039 |
| 31 | enemyUnitsKilled | 2500 | 0 | -0.400 |
| 31 | unitsTrained | 49 | 45 | -0.033 |
| 31 | populationPeak | 30 | 30 | +0.000 |
| 32 | resourcesGathered | 5495 | 5493 | -0.000 |
| 32 | resourcesUsed | 3950 | 3850 | -0.010 |
| 32 | enemyUnitsKilled | 1050 | 0 | -0.400 |
| 32 | unitsTrained | 38 | 37 | -0.011 |
| 32 | populationPeak | 29 | 30 | +0.014 |
| 33 | resourcesGathered | 5854 | 5852 | -0.000 |
| 33 | resourcesUsed | 3925 | 3825 | -0.010 |
| 33 | enemyUnitsKilled | 1350 | 0 | -0.400 |
| 33 | unitsTrained | 37 | 36 | -0.011 |
| 33 | populationPeak | 29 | 29 | +0.000 |
| 34 | resourcesGathered | 5328 | 5520 | +0.014 |
| 34 | resourcesUsed | 5425 | 5625 | +0.015 |
| 34 | enemyUnitsKilled | 1400 | 300 | -0.314 |
| 34 | unitsTrained | 51 | 54 | +0.024 |
| 34 | populationPeak | 32 | 31 | -0.013 |
| 35 | resourcesGathered | 5387 | 5365 | -0.002 |
| 35 | resourcesUsed | 3950 | 3750 | -0.020 |
| 35 | enemyUnitsKilled | 1450 | 0 | -0.400 |
| 35 | unitsTrained | 38 | 36 | -0.021 |
| 35 | populationPeak | 29 | 29 | +0.000 |
| 36 | resourcesGathered | 4820 | 4859 | +0.003 |
| 36 | resourcesUsed | 4025 | 3825 | -0.020 |
| 36 | enemyUnitsKilled | 1700 | 100 | -0.376 |
| 36 | unitsTrained | 38 | 36 | -0.021 |
| 36 | populationPeak | 30 | 30 | +0.000 |
| 37 | resourcesGathered | 6151 | 6150 | -0.000 |
| 37 | resourcesUsed | 4750 | 4550 | -0.017 |
| 37 | enemyUnitsKilled | 1000 | 0 | -0.400 |
| 37 | unitsTrained | 46 | 44 | -0.017 |
| 37 | populationPeak | 30 | 30 | +0.000 |
| 38 | resourcesGathered | 5826 | 5849 | +0.002 |
| 38 | resourcesUsed | 4025 | 3825 | -0.020 |
| 38 | enemyUnitsKilled | 950 | 0 | -0.400 |
| 38 | unitsTrained | 38 | 36 | -0.021 |
| 38 | populationPeak | 30 | 30 | +0.000 |
| 39 | resourcesGathered | 2893 | 2893 | +0.000 |
| 39 | resourcesUsed | 3325 | 3125 | -0.024 |
| 39 | enemyUnitsKilled | 2400 | 0 | -0.400 |
| 39 | unitsTrained | 31 | 28 | -0.039 |
| 39 | populationPeak | 28 | 28 | +0.000 |
| 40 | resourcesGathered | 3205 | 3205 | +0.000 |
| 40 | resourcesUsed | 3925 | 3725 | -0.020 |
| 40 | enemyUnitsKilled | 1950 | 0 | -0.400 |
| 40 | unitsTrained | 37 | 35 | -0.022 |
| 40 | populationPeak | 30 | 30 | +0.000 |

## Totals

-4.21 total = 0.00 outcome + -4.21 quality + 0.00 survival

## Verdict

bad
