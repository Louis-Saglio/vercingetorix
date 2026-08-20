# Report — baseline vs treatment

Settings: `-autostart=random/mainland -autostart-seed=<seed> -autostart-biome=generic/temperate -autostart-placement=circle -autostart-nonvisual -autostart-players=2 -autostart-size=128 -autostart-victory=conquest_civic_centers -autostart-ai=1:vercingetorix -autostart-ai=2:petra -autostart-aidiff=2:0 -autostart-civ=1:gaul -autostart-civ=2:rome -autostart-player=-1 -unique-logs -nosound -mod=public -mod=vercingetorix`

## Canary

PASS

## Pairs

| seed | base | treatment | outcome | survival | total | JS errors (base→treat) |
|---|---|---|---|---|---|---|
| 281 | draw | draw | +0.00 | +0.00 | +0.05 | 0→0 |
| 282 | draw | win | +2.00 | +0.00 | +1.93 | 0→0 |
| 283 | draw | draw | +0.00 | +0.00 | -0.19 | 0→0 |
| 284 | draw | draw | +0.00 | +0.00 | +0.19 | 0→0 |
| 285 | draw | win | +2.00 | +0.00 | +2.65 | 0→0 |
| 286 | draw | draw | +0.00 | +0.00 | -0.06 | 0→0 |
| 287 | draw | draw | +0.00 | +0.00 | -0.73 | 0→0 |
| 288 | draw | draw | +0.00 | +0.00 | +0.19 | 0→0 |
| 289 | draw | draw | +0.00 | +0.00 | +0.86 | 0→0 |
| 290 | draw | draw | +0.00 | +0.00 | +0.08 | 0→0 |

## Metric deltas

| seed | metric | base | treatment | weighted delta |
|---|---|---|---|---|
| 281 | resourcesGathered | 14429 | 16278 | +0.051 |
| 281 | resourcesUsed | 8600 | 8600 | +0.000 |
| 281 | enemyUnitsKilled | 100 | 100 | +0.000 |
| 281 | unitsTrained | 49 | 49 | +0.000 |
| 281 | populationPeak | 57 | 57 | +0.000 |
| 282 | resourcesGathered | 14930 | 10663 | -0.114 |
| 282 | resourcesUsed | 9500 | 10050 | +0.023 |
| 282 | enemyUnitsKilled | 2650 | 3150 | +0.075 |
| 282 | unitsTrained | 55 | 49 | -0.044 |
| 282 | populationPeak | 58 | 57 | -0.007 |
| 283 | resourcesGathered | 15015 | 14551 | -0.012 |
| 283 | resourcesUsed | 9100 | 8600 | -0.022 |
| 283 | enemyUnitsKilled | 300 | 200 | -0.133 |
| 283 | unitsTrained | 51 | 49 | -0.016 |
| 283 | populationPeak | 56 | 55 | -0.007 |
| 284 | resourcesGathered | 16555 | 10485 | -0.147 |
| 284 | resourcesUsed | 10125 | 9925 | -0.008 |
| 284 | enemyUnitsKilled | 0 | 3050 | +0.400 |
| 284 | unitsTrained | 46 | 46 | +0.000 |
| 284 | populationPeak | 55 | 48 | -0.051 |
| 285 | resourcesGathered | 13352 | 11502 | -0.055 |
| 285 | resourcesUsed | 7700 | 10675 | +0.155 |
| 285 | enemyUnitsKilled | 0 | 4400 | +0.400 |
| 285 | unitsTrained | 37 | 46 | +0.097 |
| 285 | populationPeak | 46 | 52 | +0.052 |
| 286 | resourcesGathered | 11564 | 10809 | -0.026 |
| 286 | resourcesUsed | 6525 | 6425 | -0.006 |
| 286 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 286 | unitsTrained | 26 | 25 | -0.015 |
| 286 | populationPeak | 35 | 34 | -0.011 |
| 287 | resourcesGathered | 16540 | 10971 | -0.135 |
| 287 | resourcesUsed | 12850 | 6300 | -0.204 |
| 287 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 287 | unitsTrained | 49 | 23 | -0.212 |
| 287 | populationPeak | 57 | 31 | -0.182 |
| 288 | resourcesGathered | 16380 | 10925 | -0.133 |
| 288 | resourcesUsed | 8325 | 8725 | +0.019 |
| 288 | enemyUnitsKilled | 0 | 2500 | +0.400 |
| 288 | unitsTrained | 46 | 41 | -0.043 |
| 288 | populationPeak | 55 | 48 | -0.051 |
| 289 | resourcesGathered | 14417 | 17520 | +0.086 |
| 289 | resourcesUsed | 8100 | 15600 | +0.370 |
| 289 | enemyUnitsKilled | 0 | 100 | +0.400 |
| 289 | unitsTrained | 51 | 51 | +0.000 |
| 289 | populationPeak | 60 | 60 | +0.000 |
| 290 | resourcesGathered | 16593 | 16304 | -0.007 |
| 290 | resourcesUsed | 8000 | 10150 | +0.107 |
| 290 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 290 | unitsTrained | 51 | 49 | -0.016 |
| 290 | populationPeak | 60 | 60 | +0.000 |

## Totals

4.98 total = 4.00 outcome + 0.98 quality + 0.00 survival

## Verdict

good
