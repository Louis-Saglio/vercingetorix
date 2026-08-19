# Report — baseline vs treatment

Settings: `-autostart=random/mainland -autostart-seed=<seed> -autostart-biome=generic/temperate -autostart-placement=circle -autostart-nonvisual -autostart-players=2 -autostart-size=128 -autostart-victory=conquest_civic_centers -autostart-ai=1:vercingetorix -autostart-ai=2:petra -autostart-aidiff=2:0 -autostart-civ=1:gaul -autostart-civ=2:rome -autostart-player=-1 -unique-logs -nosound -mod=public -mod=vercingetorix`

## Canary

PASS

## Pairs

| seed | base | treatment | outcome | survival | total | JS errors (base→treat) |
|---|---|---|---|---|---|---|
| 101 | draw | draw | +0.00 | +0.00 | -0.24 | 0→0 |
| 102 | draw | draw | +0.00 | +0.00 | -0.00 | 0→0 |
| 103 | draw | draw | +0.00 | +0.00 | -0.67 | 0→0 |
| 104 | draw | draw | +0.00 | +0.00 | -0.55 | 0→0 |
| 105 | draw | draw | +0.00 | +0.00 | +0.02 | 0→0 |
| 106 | draw | draw | +0.00 | +0.00 | -0.11 | 0→0 |
| 107 | draw | draw | +0.00 | +0.00 | +0.08 | 0→0 |
| 108 | draw | draw | +0.00 | +0.00 | -0.36 | 0→0 |
| 109 | draw | draw | +0.00 | +0.00 | -0.14 | 0→0 |
| 110 | draw | draw | +0.00 | +0.00 | -0.17 | 0→0 |

## Metric deltas

| seed | metric | base | treatment | weighted delta |
|---|---|---|---|---|
| 101 | resourcesGathered | 5733 | 4689 | -0.073 |
| 101 | resourcesUsed | 4000 | 4100 | +0.010 |
| 101 | enemyUnitsKilled | 950 | 500 | -0.189 |
| 101 | unitsTrained | 37 | 38 | +0.011 |
| 101 | populationPeak | 40 | 40 | +0.000 |
| 102 | resourcesGathered | 6502 | 5988 | -0.032 |
| 102 | resourcesUsed | 4000 | 4000 | +0.000 |
| 102 | enemyUnitsKilled | 1100 | 1150 | +0.018 |
| 102 | unitsTrained | 37 | 37 | +0.000 |
| 102 | populationPeak | 39 | 40 | +0.010 |
| 103 | resourcesGathered | 6203 | 4803 | -0.090 |
| 103 | resourcesUsed | 5600 | 4600 | -0.071 |
| 103 | enemyUnitsKilled | 2700 | 100 | -0.385 |
| 103 | unitsTrained | 53 | 38 | -0.113 |
| 103 | populationPeak | 39 | 38 | -0.010 |
| 104 | resourcesGathered | 7337 | 5509 | -0.100 |
| 104 | resourcesUsed | 5900 | 5400 | -0.034 |
| 104 | enemyUnitsKilled | 1400 | 350 | -0.300 |
| 104 | unitsTrained | 56 | 35 | -0.150 |
| 104 | populationPeak | 37 | 40 | +0.032 |
| 105 | resourcesGathered | 7048 | 5918 | -0.064 |
| 105 | resourcesUsed | 5200 | 5200 | +0.000 |
| 105 | enemyUnitsKilled | 2650 | 3250 | +0.091 |
| 105 | unitsTrained | 49 | 48 | -0.008 |
| 105 | populationPeak | 40 | 40 | +0.000 |
| 106 | resourcesGathered | 7383 | 5647 | -0.094 |
| 106 | resourcesUsed | 3900 | 4000 | +0.010 |
| 106 | enemyUnitsKilled | 1250 | 1100 | -0.048 |
| 106 | unitsTrained | 36 | 37 | +0.011 |
| 106 | populationPeak | 39 | 40 | +0.010 |
| 107 | resourcesGathered | 7855 | 6238 | -0.082 |
| 107 | resourcesUsed | 6000 | 4000 | -0.133 |
| 107 | enemyUnitsKilled | 200 | 950 | +0.400 |
| 107 | unitsTrained | 49 | 37 | -0.098 |
| 107 | populationPeak | 40 | 39 | -0.010 |
| 108 | resourcesGathered | 8193 | 5355 | -0.139 |
| 108 | resourcesUsed | 4800 | 4000 | -0.067 |
| 108 | enemyUnitsKilled | 1150 | 950 | -0.070 |
| 108 | unitsTrained | 45 | 37 | -0.071 |
| 108 | populationPeak | 40 | 39 | -0.010 |
| 109 | resourcesGathered | 8230 | 6523 | -0.083 |
| 109 | resourcesUsed | 4100 | 4100 | +0.000 |
| 109 | enemyUnitsKilled | 900 | 750 | -0.067 |
| 109 | unitsTrained | 38 | 38 | +0.000 |
| 109 | populationPeak | 39 | 40 | +0.010 |
| 110 | resourcesGathered | 7437 | 5579 | -0.100 |
| 110 | resourcesUsed | 4200 | 4300 | +0.010 |
| 110 | enemyUnitsKilled | 1850 | 1400 | -0.097 |
| 110 | unitsTrained | 39 | 40 | +0.010 |
| 110 | populationPeak | 39 | 40 | +0.010 |

## Totals

-2.14 total = 0.00 outcome + -2.14 quality + 0.00 survival

## Verdict

neutral
