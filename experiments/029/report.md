# Report — baseline vs treatment

Settings: `-autostart=random/mainland -autostart-seed=<seed> -autostart-biome=generic/temperate -autostart-placement=circle -autostart-nonvisual -autostart-players=2 -autostart-size=128 -autostart-victory=conquest_civic_centers -autostart-ai=1:vercingetorix -autostart-ai=2:petra -autostart-aidiff=2:0 -autostart-civ=1:gaul -autostart-civ=2:rome -autostart-player=-1 -unique-logs -nosound -mod=public -mod=vercingetorix`

## Canary

PASS

## Pairs

| seed | base | treatment | outcome | survival | total | JS errors (base→treat) |
|---|---|---|---|---|---|---|
| 261 | draw | draw | +0.00 | +0.20 | +1.78 | 0→0 |
| 262 | draw | draw | +0.00 | +0.20 | +1.61 | 0→0 |
| 263 | draw | draw | +0.00 | +0.20 | +2.14 | 0→0 |
| 264 | draw | draw | +0.00 | +0.20 | +1.80 | 0→0 |
| 265 | draw | draw | +0.00 | +0.20 | +1.80 | 0→0 |
| 266 | draw | draw | +0.00 | +0.20 | +1.78 | 0→0 |
| 267 | draw | draw | +0.00 | +0.20 | +1.68 | 0→0 |
| 268 | draw | draw | +0.00 | +0.20 | +1.40 | 0→0 |
| 269 | draw | draw | +0.00 | +0.20 | +1.40 | 0→0 |
| 270 | draw | draw | +0.00 | +0.20 | +1.80 | 0→0 |

## Metric deltas

| seed | metric | base | treatment | weighted delta |
|---|---|---|---|---|
| 261 | resourcesGathered | 4238 | 16431 | +0.400 |
| 261 | resourcesUsed | 4375 | 8500 | +0.377 |
| 261 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 261 | unitsTrained | 9 | 48 | +0.400 |
| 261 | populationPeak | 17 | 57 | +0.400 |
| 262 | resourcesGathered | 5019 | 15545 | +0.400 |
| 262 | resourcesUsed | 5275 | 8100 | +0.214 |
| 262 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 262 | unitsTrained | 17 | 44 | +0.400 |
| 262 | populationPeak | 24 | 53 | +0.400 |
| 263 | resourcesGathered | 4798 | 15417 | +0.400 |
| 263 | resourcesUsed | 5275 | 9725 | +0.337 |
| 263 | enemyUnitsKilled | 0 | 100 | +0.400 |
| 263 | unitsTrained | 17 | 47 | +0.400 |
| 263 | populationPeak | 22 | 55 | +0.400 |
| 264 | resourcesGathered | 4897 | 16946 | +0.400 |
| 264 | resourcesUsed | 5175 | 12250 | +0.400 |
| 264 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 264 | unitsTrained | 17 | 51 | +0.400 |
| 264 | populationPeak | 24 | 60 | +0.400 |
| 265 | resourcesGathered | 4264 | 16219 | +0.400 |
| 265 | resourcesUsed | 4375 | 11150 | +0.400 |
| 265 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 265 | unitsTrained | 9 | 49 | +0.400 |
| 265 | populationPeak | 17 | 58 | +0.400 |
| 266 | resourcesGathered | 4138 | 16946 | +0.400 |
| 266 | resourcesUsed | 4575 | 8900 | +0.378 |
| 266 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 266 | unitsTrained | 10 | 49 | +0.400 |
| 266 | populationPeak | 17 | 58 | +0.400 |
| 267 | resourcesGathered | 4887 | 14490 | +0.400 |
| 267 | resourcesUsed | 4975 | 8500 | +0.283 |
| 267 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 267 | unitsTrained | 15 | 44 | +0.400 |
| 267 | populationPeak | 23 | 50 | +0.400 |
| 268 | resourcesGathered | 3704 | 16399 | +0.400 |
| 268 | resourcesUsed | 300 | 11250 | +0.400 |
| 268 | enemyUnitsKilled | 100 | 0 | -0.400 |
| 268 | unitsTrained | 0 | 50 | +0.400 |
| 268 | populationPeak | 9 | 59 | +0.400 |
| 269 | resourcesGathered | 3790 | 17035 | +0.400 |
| 269 | resourcesUsed | 300 | 8600 | +0.400 |
| 269 | enemyUnitsKilled | 200 | 0 | -0.400 |
| 269 | unitsTrained | 0 | 49 | +0.400 |
| 269 | populationPeak | 9 | 58 | +0.400 |
| 270 | resourcesGathered | 3880 | 13453 | +0.400 |
| 270 | resourcesUsed | 4475 | 10600 | +0.400 |
| 270 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 270 | unitsTrained | 10 | 49 | +0.400 |
| 270 | populationPeak | 16 | 60 | +0.400 |

## Totals

17.19 total = 0.00 outcome + 15.19 quality + 2.00 survival

## Verdict

good
