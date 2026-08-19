# Report — baseline vs treatment

Settings: `-autostart=random/mainland -autostart-seed=<seed> -autostart-biome=generic/temperate -autostart-placement=circle -autostart-nonvisual -autostart-players=2 -autostart-size=128 -autostart-victory=conquest_civic_centers -autostart-ai=1:vercingetorix -autostart-ai=2:petra -autostart-aidiff=2:0 -autostart-civ=1:gaul -autostart-civ=2:rome -autostart-player=-1 -unique-logs -nosound -mod=public -mod=vercingetorix`

## Canary

PASS

## Pairs

| seed | base | treatment | outcome | survival | total | JS errors (base→treat) |
|---|---|---|---|---|---|---|
| 41 | draw | draw | +0.00 | +0.00 | -0.29 | 0→0 |
| 42 | draw | draw | +0.00 | +0.00 | -0.77 | 0→0 |
| 43 | draw | draw | +0.00 | +0.00 | -0.58 | 0→0 |
| 44 | draw | draw | +0.00 | +0.00 | -0.25 | 0→0 |
| 45 | draw | draw | +0.00 | +0.00 | -0.24 | 0→0 |
| 46 | draw | draw | +0.00 | +0.00 | -0.27 | 0→0 |
| 47 | draw | draw | +0.00 | +0.00 | -0.16 | 0→0 |
| 48 | draw | draw | +0.00 | +0.00 | -0.20 | 0→0 |
| 49 | draw | draw | +0.00 | +0.00 | -0.34 | 0→0 |
| 50 | draw | draw | +0.00 | +0.00 | -0.22 | 0→0 |

## Metric deltas

| seed | metric | base | treatment | weighted delta |
|---|---|---|---|---|
| 41 | resourcesGathered | 6719 | 8654 | +0.115 |
| 41 | resourcesUsed | 4125 | 4425 | +0.029 |
| 41 | enemyUnitsKilled | 950 | 0 | -0.400 |
| 41 | unitsTrained | 39 | 26 | -0.133 |
| 41 | populationPeak | 28 | 35 | +0.100 |
| 42 | resourcesGathered | 6674 | 7524 | +0.051 |
| 42 | resourcesUsed | 6450 | 3850 | -0.161 |
| 42 | enemyUnitsKilled | 800 | 0 | -0.400 |
| 42 | unitsTrained | 61 | 21 | -0.262 |
| 42 | populationPeak | 30 | 30 | +0.000 |
| 43 | resourcesGathered | 5987 | 6882 | +0.060 |
| 43 | resourcesUsed | 5625 | 4425 | -0.085 |
| 43 | enemyUnitsKilled | 3150 | 0 | -0.400 |
| 43 | unitsTrained | 49 | 26 | -0.188 |
| 43 | populationPeak | 32 | 35 | +0.038 |
| 44 | resourcesGathered | 6129 | 8479 | +0.153 |
| 44 | resourcesUsed | 3925 | 4425 | +0.051 |
| 44 | enemyUnitsKilled | 750 | 0 | -0.400 |
| 44 | unitsTrained | 37 | 26 | -0.119 |
| 44 | populationPeak | 30 | 35 | +0.067 |
| 45 | resourcesGathered | 5161 | 7678 | +0.195 |
| 45 | resourcesUsed | 3925 | 4425 | +0.051 |
| 45 | enemyUnitsKilled | 900 | 0 | -0.400 |
| 45 | unitsTrained | 37 | 26 | -0.119 |
| 45 | populationPeak | 32 | 35 | +0.038 |
| 46 | resourcesGathered | 5347 | 8692 | +0.250 |
| 46 | resourcesUsed | 5225 | 4425 | -0.061 |
| 46 | enemyUnitsKilled | 2350 | 200 | -0.366 |
| 46 | unitsTrained | 50 | 26 | -0.192 |
| 46 | populationPeak | 28 | 35 | +0.100 |
| 47 | resourcesGathered | 4846 | 8626 | +0.312 |
| 47 | resourcesUsed | 4425 | 4425 | +0.000 |
| 47 | enemyUnitsKilled | 1700 | 0 | -0.400 |
| 47 | unitsTrained | 42 | 26 | -0.152 |
| 47 | populationPeak | 29 | 35 | +0.083 |
| 48 | resourcesGathered | 4579 | 8363 | +0.331 |
| 48 | resourcesUsed | 5025 | 4425 | -0.048 |
| 48 | enemyUnitsKilled | 1800 | 0 | -0.400 |
| 48 | unitsTrained | 48 | 26 | -0.183 |
| 48 | populationPeak | 28 | 35 | +0.100 |
| 49 | resourcesGathered | 4863 | 6939 | +0.171 |
| 49 | resourcesUsed | 4625 | 4425 | -0.017 |
| 49 | enemyUnitsKilled | 1700 | 0 | -0.400 |
| 49 | unitsTrained | 44 | 26 | -0.164 |
| 49 | populationPeak | 30 | 35 | +0.067 |
| 50 | resourcesGathered | 5214 | 7859 | +0.203 |
| 50 | resourcesUsed | 4125 | 4425 | +0.029 |
| 50 | enemyUnitsKilled | 2200 | 0 | -0.400 |
| 50 | unitsTrained | 39 | 26 | -0.133 |
| 50 | populationPeak | 29 | 35 | +0.083 |

## Totals

-3.31 total = 0.00 outcome + -3.31 quality + 0.00 survival

## Verdict

neutral
