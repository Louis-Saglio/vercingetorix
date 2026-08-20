# Report — baseline vs treatment

Settings: `-autostart=random/mainland -autostart-seed=<seed> -autostart-biome=generic/temperate -autostart-placement=circle -autostart-nonvisual -autostart-players=2 -autostart-size=192 -autostart-victory=conquest_civic_centers -autostart-ai=1:vercingetorix -autostart-ai=2:petra -autostart-aidiff=2:0 -autostart-civ=1:gaul -autostart-civ=2:rome -autostart-player=-1 -unique-logs -nosound -mod=public -mod=vercingetorix`

## Canary

PASS

## Pairs

| seed | base | treatment | outcome | survival | total | JS errors (base→treat) |
|---|---|---|---|---|---|---|
| 71 | draw | draw | +0.00 | +0.00 | +0.11 | 0→0 |
| 72 | draw | draw | +0.00 | +0.00 | -0.01 | 0→0 |
| 73 | draw | draw | +0.00 | +0.00 | +0.00 | 0→0 |
| 74 | draw | draw | +0.00 | +0.00 | -0.00 | 0→0 |
| 75 | draw | draw | +0.00 | +0.00 | -0.02 | 0→0 |
| 76 | draw | draw | +0.00 | +0.00 | +0.07 | 0→0 |
| 77 | draw | draw | +0.00 | +0.00 | -0.05 | 0→0 |
| 78 | draw | draw | +0.00 | +0.00 | +0.04 | 0→0 |
| 79 | draw | draw | +0.00 | +0.00 | -0.03 | 0→0 |
| 80 | draw | draw | +0.00 | +0.00 | +0.04 | 0→0 |

## Metric deltas

| seed | metric | base | treatment | weighted delta |
|---|---|---|---|---|
| 71 | resourcesGathered | 10570 | 13447 | +0.109 |
| 71 | resourcesUsed | 7425 | 7425 | +0.000 |
| 71 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 71 | unitsTrained | 97 | 97 | +0.000 |
| 71 | populationPeak | 105 | 105 | +0.000 |
| 72 | resourcesGathered | 10407 | 10248 | -0.006 |
| 72 | resourcesUsed | 6525 | 6525 | +0.000 |
| 72 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 72 | unitsTrained | 96 | 96 | +0.000 |
| 72 | populationPeak | 105 | 105 | +0.000 |
| 73 | resourcesGathered | 9478 | 9516 | +0.002 |
| 73 | resourcesUsed | 6575 | 6575 | +0.000 |
| 73 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 73 | unitsTrained | 96 | 96 | +0.000 |
| 73 | populationPeak | 105 | 105 | +0.000 |
| 74 | resourcesGathered | 11812 | 11759 | -0.002 |
| 74 | resourcesUsed | 6525 | 6525 | +0.000 |
| 74 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 74 | unitsTrained | 96 | 96 | +0.000 |
| 74 | populationPeak | 105 | 105 | +0.000 |
| 75 | resourcesGathered | 14852 | 14101 | -0.020 |
| 75 | resourcesUsed | 6575 | 6525 | -0.003 |
| 75 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 75 | unitsTrained | 96 | 96 | +0.000 |
| 75 | populationPeak | 105 | 105 | +0.000 |
| 76 | resourcesGathered | 10588 | 12495 | +0.072 |
| 76 | resourcesUsed | 6525 | 6525 | +0.000 |
| 76 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 76 | unitsTrained | 96 | 96 | +0.000 |
| 76 | populationPeak | 105 | 105 | +0.000 |
| 77 | resourcesGathered | 9404 | 8274 | -0.048 |
| 77 | resourcesUsed | 6525 | 6525 | +0.000 |
| 77 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 77 | unitsTrained | 96 | 96 | +0.000 |
| 77 | populationPeak | 105 | 105 | +0.000 |
| 78 | resourcesGathered | 9984 | 11073 | +0.044 |
| 78 | resourcesUsed | 7425 | 7425 | +0.000 |
| 78 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 78 | unitsTrained | 99 | 98 | -0.004 |
| 78 | populationPeak | 105 | 105 | +0.000 |
| 79 | resourcesGathered | 12114 | 11205 | -0.030 |
| 79 | resourcesUsed | 6525 | 6525 | +0.000 |
| 79 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 79 | unitsTrained | 96 | 96 | +0.000 |
| 79 | populationPeak | 105 | 105 | +0.000 |
| 80 | resourcesGathered | 12454 | 14074 | +0.052 |
| 80 | resourcesUsed | 6675 | 6525 | -0.009 |
| 80 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 80 | unitsTrained | 96 | 96 | +0.000 |
| 80 | populationPeak | 105 | 105 | +0.000 |

## Totals

0.16 total = 0.00 outcome + 0.16 quality + 0.00 survival

## Verdict

neutral
