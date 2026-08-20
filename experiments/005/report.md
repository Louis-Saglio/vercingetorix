# Report — baseline vs treatment

Settings: `-autostart=random/mainland -autostart-seed=<seed> -autostart-biome=generic/temperate -autostart-placement=circle -autostart-nonvisual -autostart-players=2 -autostart-size=192 -autostart-victory=conquest_civic_centers -autostart-ai=1:vercingetorix -autostart-ai=2:petra -autostart-aidiff=2:0 -autostart-civ=1:gaul -autostart-civ=2:rome -autostart-player=-1 -unique-logs -nosound -mod=public -mod=vercingetorix`

## Canary

PASS

## Pairs

| seed | base | treatment | outcome | survival | total | JS errors (base→treat) |
|---|---|---|---|---|---|---|
| 41 | draw | draw | +0.00 | +0.00 | +1.42 | 0→0 |
| 42 | draw | draw | +0.00 | +0.00 | +1.38 | 0→0 |
| 43 | draw | draw | +0.00 | +0.00 | +1.52 | 0→0 |
| 44 | draw | draw | +0.00 | +0.00 | +1.45 | 0→0 |
| 45 | draw | draw | +0.00 | +0.00 | +1.53 | 0→0 |
| 46 | draw | draw | +0.00 | +0.00 | +1.49 | 0→0 |
| 47 | draw | draw | +0.00 | +0.00 | +1.40 | 0→0 |
| 48 | draw | draw | +0.00 | +0.00 | +1.60 | 0→0 |
| 49 | draw | draw | +0.00 | +0.00 | +1.45 | 0→0 |
| 50 | draw | draw | +0.00 | +0.00 | +1.54 | 0→0 |

## Metric deltas

| seed | metric | base | treatment | weighted delta |
|---|---|---|---|---|
| 41 | resourcesGathered | 6614 | 10325 | +0.224 |
| 41 | resourcesUsed | 550 | 6075 | +0.400 |
| 41 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 41 | unitsTrained | 11 | 96 | +0.400 |
| 41 | populationPeak | 20 | 105 | +0.400 |
| 42 | resourcesGathered | 7158 | 10348 | +0.178 |
| 42 | resourcesUsed | 550 | 6075 | +0.400 |
| 42 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 42 | unitsTrained | 11 | 96 | +0.400 |
| 42 | populationPeak | 20 | 102 | +0.400 |
| 43 | resourcesGathered | 7419 | 13379 | +0.321 |
| 43 | resourcesUsed | 550 | 6075 | +0.400 |
| 43 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 43 | unitsTrained | 11 | 96 | +0.400 |
| 43 | populationPeak | 20 | 105 | +0.400 |
| 44 | resourcesGathered | 6721 | 10972 | +0.253 |
| 44 | resourcesUsed | 550 | 6075 | +0.400 |
| 44 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 44 | unitsTrained | 11 | 96 | +0.400 |
| 44 | populationPeak | 20 | 105 | +0.400 |
| 45 | resourcesGathered | 6186 | 11283 | +0.330 |
| 45 | resourcesUsed | 550 | 6075 | +0.400 |
| 45 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 45 | unitsTrained | 11 | 96 | +0.400 |
| 45 | populationPeak | 20 | 105 | +0.400 |
| 46 | resourcesGathered | 7550 | 13045 | +0.291 |
| 46 | resourcesUsed | 550 | 6075 | +0.400 |
| 46 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 46 | unitsTrained | 11 | 96 | +0.400 |
| 46 | populationPeak | 20 | 105 | +0.400 |
| 47 | resourcesGathered | 7233 | 10813 | +0.198 |
| 47 | resourcesUsed | 550 | 6075 | +0.400 |
| 47 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 47 | unitsTrained | 11 | 96 | +0.400 |
| 47 | populationPeak | 20 | 105 | +0.400 |
| 48 | resourcesGathered | 7182 | 14374 | +0.400 |
| 48 | resourcesUsed | 550 | 6075 | +0.400 |
| 48 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 48 | unitsTrained | 11 | 96 | +0.400 |
| 48 | populationPeak | 20 | 105 | +0.400 |
| 49 | resourcesGathered | 6839 | 11194 | +0.255 |
| 49 | resourcesUsed | 600 | 6125 | +0.400 |
| 49 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 49 | unitsTrained | 12 | 97 | +0.400 |
| 49 | populationPeak | 20 | 105 | +0.400 |
| 50 | resourcesGathered | 6900 | 12804 | +0.342 |
| 50 | resourcesUsed | 550 | 6075 | +0.400 |
| 50 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 50 | unitsTrained | 11 | 96 | +0.400 |
| 50 | populationPeak | 20 | 105 | +0.400 |

## Totals

14.79 total = 0.00 outcome + 14.79 quality + 0.00 survival

## Verdict

good
