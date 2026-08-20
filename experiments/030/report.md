# Report — baseline vs treatment

Settings: `-autostart=random/mainland -autostart-seed=<seed> -autostart-biome=generic/temperate -autostart-placement=circle -autostart-nonvisual -autostart-players=2 -autostart-size=128 -autostart-victory=conquest_civic_centers -autostart-ai=1:vercingetorix -autostart-ai=2:petra -autostart-aidiff=2:0 -autostart-civ=1:gaul -autostart-civ=2:rome -autostart-player=-1 -unique-logs -nosound -mod=public -mod=vercingetorix`

## Canary

PASS

## Pairs

| seed | base | treatment | outcome | survival | total | JS errors (base→treat) |
|---|---|---|---|---|---|---|
| 271 | draw | draw | +0.00 | +0.00 | +0.00 | 0→0 |
| 272 | draw | draw | +0.00 | +0.00 | +0.00 | 0→0 |
| 273 | draw | draw | +0.00 | +0.00 | +0.00 | 0→0 |
| 274 | draw | draw | +0.00 | +0.00 | +0.50 | 0→0 |
| 275 | draw | draw | +0.00 | +0.00 | +0.00 | 0→0 |
| 276 | draw | draw | +0.00 | +0.00 | +0.00 | 0→0 |
| 277 | draw | draw | +0.00 | +0.00 | +0.00 | 0→0 |
| 278 | draw | draw | +0.00 | +0.00 | +0.00 | 0→0 |
| 279 | draw | draw | +0.00 | +0.00 | +0.00 | 0→0 |
| 280 | draw | draw | +0.00 | +0.00 | +0.00 | 0→0 |

## Metric deltas

| seed | metric | base | treatment | weighted delta |
|---|---|---|---|---|
| 271 | resourcesGathered | 13582 | 13582 | +0.000 |
| 271 | resourcesUsed | 8200 | 8200 | +0.000 |
| 271 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 271 | unitsTrained | 42 | 42 | +0.000 |
| 271 | populationPeak | 51 | 51 | +0.000 |
| 272 | resourcesGathered | 16888 | 16888 | +0.000 |
| 272 | resourcesUsed | 11600 | 11600 | +0.000 |
| 272 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 272 | unitsTrained | 49 | 49 | +0.000 |
| 272 | populationPeak | 58 | 58 | +0.000 |
| 273 | resourcesGathered | 16727 | 16727 | +0.000 |
| 273 | resourcesUsed | 11150 | 11150 | +0.000 |
| 273 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 273 | unitsTrained | 49 | 49 | +0.000 |
| 273 | populationPeak | 58 | 58 | +0.000 |
| 274 | resourcesGathered | 13357 | 12622 | -0.022 |
| 274 | resourcesUsed | 8400 | 9500 | +0.052 |
| 274 | enemyUnitsKilled | 0 | 4050 | +0.400 |
| 274 | unitsTrained | 44 | 46 | +0.018 |
| 274 | populationPeak | 50 | 56 | +0.048 |
| 275 | resourcesGathered | 16220 | 16220 | +0.000 |
| 275 | resourcesUsed | 11650 | 11650 | +0.000 |
| 275 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 275 | unitsTrained | 51 | 51 | +0.000 |
| 275 | populationPeak | 60 | 60 | +0.000 |
| 276 | resourcesGathered | 14837 | 14837 | +0.000 |
| 276 | resourcesUsed | 8300 | 8300 | +0.000 |
| 276 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 276 | unitsTrained | 51 | 51 | +0.000 |
| 276 | populationPeak | 60 | 60 | +0.000 |
| 277 | resourcesGathered | 17386 | 17386 | +0.000 |
| 277 | resourcesUsed | 9825 | 9825 | +0.000 |
| 277 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 277 | unitsTrained | 47 | 47 | +0.000 |
| 277 | populationPeak | 55 | 55 | +0.000 |
| 278 | resourcesGathered | 14017 | 14017 | +0.000 |
| 278 | resourcesUsed | 8300 | 8300 | +0.000 |
| 278 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 278 | unitsTrained | 43 | 43 | +0.000 |
| 278 | populationPeak | 52 | 52 | +0.000 |
| 279 | resourcesGathered | 16342 | 16342 | +0.000 |
| 279 | resourcesUsed | 8300 | 8300 | +0.000 |
| 279 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 279 | unitsTrained | 51 | 51 | +0.000 |
| 279 | populationPeak | 60 | 60 | +0.000 |
| 280 | resourcesGathered | 13014 | 13014 | +0.000 |
| 280 | resourcesUsed | 8700 | 8700 | +0.000 |
| 280 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 280 | unitsTrained | 48 | 48 | +0.000 |
| 280 | populationPeak | 56 | 56 | +0.000 |

## Totals

0.50 total = 0.00 outcome + 0.50 quality + 0.00 survival

## Verdict

neutral
