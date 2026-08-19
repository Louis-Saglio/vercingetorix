# Report — baseline vs treatment

Settings: `-autostart=random/mainland -autostart-seed=<seed> -autostart-biome=generic/temperate -autostart-placement=circle -autostart-nonvisual -autostart-players=2 -autostart-size=128 -autostart-victory=conquest_civic_centers -autostart-ai=1:vercingetorix -autostart-ai=2:petra -autostart-aidiff=2:0 -autostart-civ=1:gaul -autostart-civ=2:rome -autostart-player=-1 -unique-logs -nosound -mod=public -mod=vercingetorix`

## Canary

PASS

## Pairs

| seed | base | treatment | outcome | survival | total | JS errors (base→treat) |
|---|---|---|---|---|---|---|
| 151 | draw | draw | +0.00 | +0.00 | -0.67 | 0→0 |
| 152 | draw | draw | +0.00 | +0.00 | -0.07 | 0→0 |
| 153 | draw | draw | +0.00 | +0.00 | -0.49 | 0→0 |
| 154 | draw | draw | +0.00 | +0.00 | -0.60 | 0→0 |
| 155 | draw | draw | +0.00 | +0.00 | +0.14 | 0→0 |
| 156 | draw | draw | +0.00 | +0.00 | -0.66 | 0→0 |
| 157 | draw | draw | +0.00 | +0.00 | -0.15 | 0→0 |
| 158 | draw | draw | +0.00 | +0.00 | -0.07 | 0→0 |
| 159 | draw | draw | +0.00 | +0.00 | +0.35 | 0→0 |
| 160 | draw | draw | +0.00 | +0.00 | -0.12 | 0→0 |

## Metric deltas

| seed | metric | base | treatment | weighted delta |
|---|---|---|---|---|
| 151 | resourcesGathered | 5650 | 6179 | +0.037 |
| 151 | resourcesUsed | 4000 | 3850 | -0.015 |
| 151 | enemyUnitsKilled | 1200 | 0 | -0.400 |
| 151 | unitsTrained | 37 | 21 | -0.173 |
| 151 | populationPeak | 39 | 27 | -0.123 |
| 152 | resourcesGathered | 6397 | 8193 | +0.112 |
| 152 | resourcesUsed | 4000 | 3900 | -0.010 |
| 152 | enemyUnitsKilled | 750 | 450 | -0.160 |
| 152 | unitsTrained | 37 | 36 | -0.011 |
| 152 | populationPeak | 40 | 40 | +0.000 |
| 153 | resourcesGathered | 6021 | 7473 | +0.096 |
| 153 | resourcesUsed | 4900 | 3700 | -0.098 |
| 153 | enemyUnitsKilled | 1100 | 100 | -0.364 |
| 153 | unitsTrained | 46 | 33 | -0.113 |
| 153 | populationPeak | 40 | 39 | -0.010 |
| 154 | resourcesGathered | 5608 | 6683 | +0.077 |
| 154 | resourcesUsed | 4000 | 3925 | -0.007 |
| 154 | enemyUnitsKilled | 1050 | 0 | -0.400 |
| 154 | unitsTrained | 37 | 21 | -0.173 |
| 154 | populationPeak | 39 | 30 | -0.092 |
| 155 | resourcesGathered | 5887 | 7693 | +0.123 |
| 155 | resourcesUsed | 4300 | 4400 | +0.009 |
| 155 | enemyUnitsKilled | 850 | 850 | +0.000 |
| 155 | unitsTrained | 40 | 41 | +0.010 |
| 155 | populationPeak | 40 | 40 | +0.000 |
| 156 | resourcesGathered | 5261 | 6813 | +0.118 |
| 156 | resourcesUsed | 5600 | 3300 | -0.164 |
| 156 | enemyUnitsKilled | 1350 | 0 | -0.400 |
| 156 | unitsTrained | 51 | 29 | -0.173 |
| 156 | populationPeak | 40 | 36 | -0.040 |
| 157 | resourcesGathered | 5693 | 8897 | +0.225 |
| 157 | resourcesUsed | 3900 | 3800 | -0.010 |
| 157 | enemyUnitsKilled | 750 | 150 | -0.320 |
| 157 | unitsTrained | 36 | 33 | -0.033 |
| 157 | populationPeak | 40 | 39 | -0.010 |
| 158 | resourcesGathered | 5102 | 7454 | +0.184 |
| 158 | resourcesUsed | 4000 | 3900 | -0.010 |
| 158 | enemyUnitsKilled | 1350 | 550 | -0.237 |
| 158 | unitsTrained | 37 | 36 | -0.011 |
| 158 | populationPeak | 39 | 39 | +0.000 |
| 159 | resourcesGathered | 5989 | 8220 | +0.149 |
| 159 | resourcesUsed | 4000 | 4900 | +0.090 |
| 159 | enemyUnitsKilled | 1100 | 1100 | +0.000 |
| 159 | unitsTrained | 37 | 46 | +0.097 |
| 159 | populationPeak | 39 | 40 | +0.010 |
| 160 | resourcesGathered | 5527 | 8756 | +0.234 |
| 160 | resourcesUsed | 5600 | 4600 | -0.071 |
| 160 | enemyUnitsKilled | 1600 | 600 | -0.250 |
| 160 | unitsTrained | 44 | 39 | -0.045 |
| 160 | populationPeak | 39 | 40 | +0.010 |

## Totals

-2.34 total = 0.00 outcome + -2.34 quality + 0.00 survival

## Verdict

neutral
