# Report — baseline vs treatment2

Settings: `-autostart=random/mainland -autostart-seed=<seed> -autostart-biome=generic/temperate -autostart-placement=circle -autostart-nonvisual -autostart-players=2 -autostart-size=192 -autostart-victory=conquest_civic_centers -autostart-ai=1:vercingetorix -autostart-ai=2:petra -autostart-aidiff=2:0 -autostart-civ=1:gaul -autostart-civ=2:rome -autostart-player=-1 -unique-logs -nosound -mod=public -mod=vercingetorix`

## Canary

PASS

## Pairs

| seed | base | treatment | outcome | survival | total | JS errors (base→treat) |
|---|---|---|---|---|---|---|
| 21 | draw | draw | +0.00 | +0.00 | +1.53 | 0→0 |
| 22 | draw | draw | +0.00 | +0.00 | +1.55 | 0→0 |
| 23 | draw | draw | +0.00 | +0.00 | +1.45 | 0→0 |
| 24 | draw | draw | +0.00 | +0.00 | +1.58 | 0→0 |
| 25 | draw | draw | +0.00 | +0.00 | +1.40 | 0→0 |
| 26 | draw | draw | +0.00 | +0.00 | +1.45 | 0→0 |
| 27 | draw | draw | +0.00 | +0.00 | +1.45 | 0→0 |
| 28 | draw | draw | +0.00 | +0.00 | +1.41 | 0→0 |
| 29 | draw | draw | +0.00 | +0.00 | +1.60 | 0→0 |
| 30 | draw | draw | +0.00 | +0.00 | +1.49 | 0→0 |

## Metric deltas

| seed | metric | base | treatment | weighted delta |
|---|---|---|---|---|
| 21 | resourcesGathered | 8813 | 16192 | +0.335 |
| 21 | resourcesUsed | 550 | 3450 | +0.400 |
| 21 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 21 | unitsTrained | 11 | 54 | +0.400 |
| 21 | populationPeak | 20 | 62 | +0.400 |
| 22 | resourcesGathered | 8712 | 16231 | +0.345 |
| 22 | resourcesUsed | 550 | 3175 | +0.400 |
| 22 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 22 | unitsTrained | 11 | 50 | +0.400 |
| 22 | populationPeak | 20 | 58 | +0.400 |
| 23 | resourcesGathered | 8189 | 13257 | +0.248 |
| 23 | resourcesUsed | 550 | 3650 | +0.400 |
| 23 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 23 | unitsTrained | 11 | 57 | +0.400 |
| 23 | populationPeak | 20 | 65 | +0.400 |
| 24 | resourcesGathered | 7666 | 14870 | +0.376 |
| 24 | resourcesUsed | 550 | 2850 | +0.400 |
| 24 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 24 | unitsTrained | 11 | 45 | +0.400 |
| 24 | populationPeak | 20 | 53 | +0.400 |
| 25 | resourcesGathered | 8337 | 12568 | +0.203 |
| 25 | resourcesUsed | 550 | 2800 | +0.400 |
| 25 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 25 | unitsTrained | 11 | 43 | +0.400 |
| 25 | populationPeak | 20 | 51 | +0.400 |
| 26 | resourcesGathered | 8773 | 14172 | +0.246 |
| 26 | resourcesUsed | 550 | 3825 | +0.400 |
| 26 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 26 | unitsTrained | 11 | 60 | +0.400 |
| 26 | populationPeak | 20 | 68 | +0.400 |
| 27 | resourcesGathered | 8754 | 14263 | +0.252 |
| 27 | resourcesUsed | 550 | 3325 | +0.400 |
| 27 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 27 | unitsTrained | 11 | 53 | +0.400 |
| 27 | populationPeak | 20 | 61 | +0.400 |
| 28 | resourcesGathered | 9026 | 13828 | +0.213 |
| 28 | resourcesUsed | 550 | 4425 | +0.400 |
| 28 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 28 | unitsTrained | 11 | 69 | +0.400 |
| 28 | populationPeak | 20 | 75 | +0.400 |
| 29 | resourcesGathered | 8037 | 16624 | +0.400 |
| 29 | resourcesUsed | 550 | 4300 | +0.400 |
| 29 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 29 | unitsTrained | 11 | 68 | +0.400 |
| 29 | populationPeak | 20 | 76 | +0.400 |
| 30 | resourcesGathered | 8648 | 14844 | +0.287 |
| 30 | resourcesUsed | 550 | 3500 | +0.400 |
| 30 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 30 | unitsTrained | 11 | 55 | +0.400 |
| 30 | populationPeak | 20 | 63 | +0.400 |

## Totals

14.90 total = 0.00 outcome + 14.90 quality + 0.00 survival

## Verdict

good
