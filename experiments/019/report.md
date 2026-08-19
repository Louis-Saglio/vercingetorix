# Report — baseline vs treatment

Settings: `-autostart=random/mainland -autostart-seed=<seed> -autostart-biome=generic/temperate -autostart-placement=circle -autostart-nonvisual -autostart-players=2 -autostart-size=128 -autostart-victory=conquest_civic_centers -autostart-ai=1:vercingetorix -autostart-ai=2:petra -autostart-aidiff=2:0 -autostart-civ=1:gaul -autostart-civ=2:rome -autostart-player=-1 -unique-logs -nosound -mod=public -mod=vercingetorix`

## Canary

PASS

## Pairs

| seed | base | treatment | outcome | survival | total | JS errors (base→treat) |
|---|---|---|---|---|---|---|
| 171 | draw | draw | +0.00 | +0.00 | -0.54 | 0→0 |
| 172 | draw | draw | +0.00 | +0.00 | -0.67 | 0→0 |
| 173 | draw | draw | +0.00 | +0.00 | -1.63 | 0→0 |
| 174 | draw | draw | +0.00 | +0.00 | +0.67 | 0→0 |
| 175 | draw | draw | +0.00 | +0.00 | -0.74 | 0→0 |
| 176 | draw | draw | +0.00 | +0.00 | -0.60 | 0→0 |
| 177 | draw | draw | +0.00 | +0.00 | -0.39 | 0→0 |
| 178 | draw | draw | +0.00 | +0.00 | -0.51 | 0→0 |
| 179 | draw | draw | +0.00 | +0.00 | -0.19 | 0→0 |
| 180 | draw | draw | +0.00 | +0.00 | -0.59 | 0→0 |

## Metric deltas

| seed | metric | base | treatment | weighted delta |
|---|---|---|---|---|
| 171 | resourcesGathered | 7555 | 7782 | +0.012 |
| 171 | resourcesUsed | 4600 | 4475 | -0.011 |
| 171 | enemyUnitsKilled | 1400 | 0 | -0.400 |
| 171 | unitsTrained | 43 | 30 | -0.121 |
| 171 | populationPeak | 39 | 37 | -0.021 |
| 172 | resourcesGathered | 8938 | 6637 | -0.103 |
| 172 | resourcesUsed | 3900 | 3975 | +0.008 |
| 172 | enemyUnitsKilled | 400 | 0 | -0.400 |
| 172 | unitsTrained | 36 | 26 | -0.111 |
| 172 | populationPeak | 40 | 34 | -0.060 |
| 173 | resourcesGathered | 7631 | 4061 | -0.187 |
| 173 | resourcesUsed | 4600 | 375 | -0.367 |
| 173 | enemyUnitsKilled | 2150 | 200 | -0.363 |
| 173 | unitsTrained | 40 | 0 | -0.400 |
| 173 | populationPeak | 40 | 9 | -0.310 |
| 174 | resourcesGathered | 6148 | 7043 | +0.058 |
| 174 | resourcesUsed | 3275 | 3475 | +0.024 |
| 174 | enemyUnitsKilled | 0 | 150 | +0.400 |
| 174 | unitsTrained | 16 | 21 | +0.125 |
| 174 | populationPeak | 25 | 29 | +0.064 |
| 175 | resourcesGathered | 7545 | 5094 | -0.130 |
| 175 | resourcesUsed | 3800 | 2475 | -0.139 |
| 175 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 175 | unitsTrained | 33 | 11 | -0.267 |
| 175 | populationPeak | 39 | 19 | -0.205 |
| 176 | resourcesGathered | 8166 | 7463 | -0.034 |
| 176 | resourcesUsed | 4200 | 4175 | -0.002 |
| 176 | enemyUnitsKilled | 1500 | 0 | -0.400 |
| 176 | unitsTrained | 39 | 28 | -0.113 |
| 176 | populationPeak | 40 | 35 | -0.050 |
| 177 | resourcesGathered | 7586 | 8047 | +0.024 |
| 177 | resourcesUsed | 3600 | 4275 | +0.075 |
| 177 | enemyUnitsKilled | 50 | 0 | -0.400 |
| 177 | unitsTrained | 32 | 28 | -0.050 |
| 177 | populationPeak | 39 | 35 | -0.041 |
| 178 | resourcesGathered | 7119 | 7925 | +0.045 |
| 178 | resourcesUsed | 4100 | 4175 | +0.007 |
| 178 | enemyUnitsKilled | 900 | 0 | -0.400 |
| 178 | unitsTrained | 38 | 27 | -0.116 |
| 178 | populationPeak | 40 | 35 | -0.050 |
| 179 | resourcesGathered | 7713 | 8418 | +0.037 |
| 179 | resourcesUsed | 4400 | 5275 | +0.080 |
| 179 | enemyUnitsKilled | 1650 | 600 | -0.255 |
| 179 | unitsTrained | 41 | 37 | -0.039 |
| 179 | populationPeak | 40 | 39 | -0.010 |
| 180 | resourcesGathered | 7187 | 7327 | +0.008 |
| 180 | resourcesUsed | 3900 | 3875 | -0.003 |
| 180 | enemyUnitsKilled | 1200 | 0 | -0.400 |
| 180 | unitsTrained | 36 | 25 | -0.122 |
| 180 | populationPeak | 39 | 32 | -0.072 |

## Totals

-5.18 total = 0.00 outcome + -5.18 quality + 0.00 survival

## Verdict

bad
