# Report — baseline vs treatment

Settings: `-autostart=random/mainland -autostart-seed=<seed> -autostart-biome=generic/temperate -autostart-placement=circle -autostart-nonvisual -autostart-players=2 -autostart-size=192 -autostart-victory=conquest_civic_centers -autostart-ai=1:vercingetorix -autostart-ai=2:petra -autostart-aidiff=2:0 -autostart-civ=1:gaul -autostart-civ=2:rome -autostart-player=-1 -unique-logs -nosound -mod=public -mod=vercingetorix`

## Canary

PASS

## Pairs

| seed | base | treatment | outcome | survival | total | JS errors (base→treat) |
|---|---|---|---|---|---|---|
| 11 | draw | draw | +0.00 | +0.00 | +1.55 | 0→0 |
| 12 | draw | draw | +0.00 | +0.00 | +1.51 | 0→0 |
| 13 | draw | draw | +0.00 | +0.00 | +1.51 | 0→0 |
| 14 | draw | draw | +0.00 | +0.00 | +1.47 | 0→0 |
| 15 | draw | draw | +0.00 | +0.00 | +1.53 | 0→0 |
| 16 | draw | draw | +0.00 | +0.00 | +1.55 | 0→0 |
| 17 | draw | draw | +0.00 | +0.00 | +1.56 | 0→0 |
| 18 | draw | draw | +0.00 | +0.00 | +1.48 | 0→0 |
| 19 | draw | draw | +0.00 | +0.00 | +1.50 | 0→0 |
| 20 | draw | draw | +0.00 | +0.00 | +1.48 | 0→0 |

## Metric deltas

| seed | metric | base | treatment | weighted delta |
|---|---|---|---|---|
| 11 | resourcesGathered | 4640 | 8691 | +0.349 |
| 11 | resourcesUsed | 0 | 550 | +0.400 |
| 11 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 11 | unitsTrained | 0 | 11 | +0.400 |
| 11 | populationPeak | 9 | 20 | +0.400 |
| 12 | resourcesGathered | 4822 | 8530 | +0.308 |
| 12 | resourcesUsed | 0 | 550 | +0.400 |
| 12 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 12 | unitsTrained | 0 | 11 | +0.400 |
| 12 | populationPeak | 9 | 20 | +0.400 |
| 13 | resourcesGathered | 5035 | 8881 | +0.306 |
| 13 | resourcesUsed | 0 | 550 | +0.400 |
| 13 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 13 | unitsTrained | 0 | 11 | +0.400 |
| 13 | populationPeak | 9 | 20 | +0.400 |
| 14 | resourcesGathered | 4636 | 7730 | +0.267 |
| 14 | resourcesUsed | 0 | 550 | +0.400 |
| 14 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 14 | unitsTrained | 0 | 11 | +0.400 |
| 14 | populationPeak | 9 | 20 | +0.400 |
| 15 | resourcesGathered | 4534 | 8225 | +0.326 |
| 15 | resourcesUsed | 0 | 550 | +0.400 |
| 15 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 15 | unitsTrained | 0 | 11 | +0.400 |
| 15 | populationPeak | 9 | 20 | +0.400 |
| 16 | resourcesGathered | 4610 | 8605 | +0.347 |
| 16 | resourcesUsed | 0 | 550 | +0.400 |
| 16 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 16 | unitsTrained | 0 | 11 | +0.400 |
| 16 | populationPeak | 9 | 20 | +0.400 |
| 17 | resourcesGathered | 4535 | 8665 | +0.364 |
| 17 | resourcesUsed | 0 | 550 | +0.400 |
| 17 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 17 | unitsTrained | 0 | 11 | +0.400 |
| 17 | populationPeak | 9 | 20 | +0.400 |
| 18 | resourcesGathered | 5328 | 9009 | +0.276 |
| 18 | resourcesUsed | 0 | 550 | +0.400 |
| 18 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 18 | unitsTrained | 0 | 11 | +0.400 |
| 18 | populationPeak | 9 | 20 | +0.400 |
| 19 | resourcesGathered | 4830 | 8496 | +0.304 |
| 19 | resourcesUsed | 0 | 550 | +0.400 |
| 19 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 19 | unitsTrained | 0 | 11 | +0.400 |
| 19 | populationPeak | 9 | 20 | +0.400 |
| 20 | resourcesGathered | 4885 | 8264 | +0.277 |
| 20 | resourcesUsed | 0 | 550 | +0.400 |
| 20 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 20 | unitsTrained | 0 | 11 | +0.400 |
| 20 | populationPeak | 9 | 20 | +0.400 |

## Totals

15.12 total = 0.00 outcome + 15.12 quality + 0.00 survival

## Verdict

good
