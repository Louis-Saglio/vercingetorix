# Report — baseline vs treatment

Settings: `-autostart=random/mainland -autostart-seed=<seed> -autostart-biome=generic/temperate -autostart-placement=circle -autostart-nonvisual -autostart-players=2 -autostart-size=192 -autostart-victory=conquest_civic_centers -autostart-ai=1:vercingetorix -autostart-ai=2:petra -autostart-aidiff=2:0 -autostart-civ=1:gaul -autostart-civ=2:rome -autostart-player=-1 -unique-logs -nosound -mod=public -mod=vercingetorix`

## Canary

PASS

## Pairs

| seed | base | treatment | outcome | survival | total | JS errors (base→treat) |
|---|---|---|---|---|---|---|
| 51 | draw | draw | +0.00 | +0.00 | +0.46 | 0→0 |
| 52 | draw | draw | +0.00 | +0.00 | +0.04 | 0→0 |
| 53 | draw | draw | +0.00 | +0.00 | +0.05 | 0→0 |
| 54 | draw | draw | +0.00 | +0.00 | +0.02 | 0→0 |
| 55 | draw | draw | +0.00 | +0.00 | -0.00 | 0→0 |
| 56 | draw | draw | +0.00 | +0.00 | +0.04 | 0→0 |
| 57 | draw | draw | +0.00 | +0.00 | -0.35 | 0→0 |
| 58 | draw | draw | +0.00 | +0.00 | +0.02 | 0→0 |
| 59 | draw | draw | +0.00 | +0.00 | -0.41 | 0→0 |
| 60 | draw | draw | +0.00 | +0.00 | +0.08 | 0→0 |

## Metric deltas

| seed | metric | base | treatment | weighted delta |
|---|---|---|---|---|
| 51 | resourcesGathered | 13387 | 12221 | -0.035 |
| 51 | resourcesUsed | 6625 | 7875 | +0.075 |
| 51 | enemyUnitsKilled | 0 | 200 | +0.400 |
| 51 | unitsTrained | 106 | 112 | +0.023 |
| 51 | populationPeak | 105 | 105 | +0.000 |
| 52 | resourcesGathered | 12275 | 12550 | +0.009 |
| 52 | resourcesUsed | 6075 | 6525 | +0.030 |
| 52 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 52 | unitsTrained | 96 | 96 | +0.000 |
| 52 | populationPeak | 105 | 105 | +0.000 |
| 53 | resourcesGathered | 9225 | 9677 | +0.020 |
| 53 | resourcesUsed | 6075 | 6525 | +0.030 |
| 53 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 53 | unitsTrained | 96 | 96 | +0.000 |
| 53 | populationPeak | 105 | 105 | +0.000 |
| 54 | resourcesGathered | 10030 | 9712 | -0.013 |
| 54 | resourcesUsed | 6075 | 6525 | +0.030 |
| 54 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 54 | unitsTrained | 96 | 96 | +0.000 |
| 54 | populationPeak | 105 | 105 | +0.000 |
| 55 | resourcesGathered | 11124 | 10167 | -0.034 |
| 55 | resourcesUsed | 6075 | 6525 | +0.030 |
| 55 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 55 | unitsTrained | 96 | 96 | +0.000 |
| 55 | populationPeak | 105 | 105 | +0.000 |
| 56 | resourcesGathered | 13040 | 13451 | +0.013 |
| 56 | resourcesUsed | 6075 | 6525 | +0.030 |
| 56 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 56 | unitsTrained | 96 | 96 | +0.000 |
| 56 | populationPeak | 105 | 105 | +0.000 |
| 57 | resourcesGathered | 12622 | 13542 | +0.029 |
| 57 | resourcesUsed | 6125 | 6525 | +0.026 |
| 57 | enemyUnitsKilled | 100 | 0 | -0.400 |
| 57 | unitsTrained | 97 | 96 | -0.004 |
| 57 | populationPeak | 105 | 105 | +0.000 |
| 58 | resourcesGathered | 11611 | 11348 | -0.009 |
| 58 | resourcesUsed | 6075 | 6525 | +0.030 |
| 58 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 58 | unitsTrained | 96 | 96 | +0.000 |
| 58 | populationPeak | 105 | 105 | +0.000 |
| 59 | resourcesGathered | 9558 | 9447 | -0.005 |
| 59 | resourcesUsed | 6325 | 6525 | +0.013 |
| 59 | enemyUnitsKilled | 100 | 0 | -0.400 |
| 59 | unitsTrained | 101 | 96 | -0.020 |
| 59 | populationPeak | 105 | 105 | +0.000 |
| 60 | resourcesGathered | 13276 | 15081 | +0.054 |
| 60 | resourcesUsed | 6075 | 6525 | +0.030 |
| 60 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 60 | unitsTrained | 96 | 96 | +0.000 |
| 60 | populationPeak | 105 | 105 | +0.000 |

## Totals

-0.05 total = 0.00 outcome + -0.05 quality + 0.00 survival

## Verdict

neutral
