# Report — baseline vs treatment

Settings: `-autostart=random/mainland -autostart-seed=<seed> -autostart-biome=generic/temperate -autostart-placement=circle -autostart-nonvisual -autostart-players=2 -autostart-size=128 -autostart-victory=conquest_civic_centers -autostart-ai=1:vercingetorix -autostart-ai=2:petra -autostart-aidiff=2:0 -autostart-civ=1:gaul -autostart-civ=2:rome -autostart-player=-1 -unique-logs -nosound -mod=public -mod=vercingetorix`

## Canary

PASS

## Pairs

| seed | base | treatment | outcome | survival | total | JS errors (base→treat) |
|---|---|---|---|---|---|---|
| 311 | draw | draw | +0.00 | +0.00 | -1.26 | 0→0 |
| 312 | draw | draw | +0.00 | +0.00 | -1.28 | 0→0 |
| 313 | draw | draw | +0.00 | +0.00 | -1.27 | 0→0 |
| 314 | draw | draw | +0.00 | +0.00 | -1.21 | 0→0 |
| 315 | draw | draw | +0.00 | +0.00 | -1.08 | 0→0 |
| 316 | draw | draw | +0.00 | +0.00 | -1.24 | 0→0 |
| 317 | draw | draw | +0.00 | +0.00 | -1.62 | 0→0 |
| 318 | draw | draw | +0.00 | +0.00 | -1.69 | 0→0 |
| 319 | draw | draw | +0.00 | +0.00 | -1.18 | 0→0 |
| 320 | draw | draw | +0.00 | +0.00 | -1.20 | 0→0 |

## Metric deltas

| seed | metric | base | treatment | weighted delta |
|---|---|---|---|---|
| 311 | resourcesGathered | 16264 | 5144 | -0.273 |
| 311 | resourcesUsed | 10125 | 3625 | -0.257 |
| 311 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 311 | unitsTrained | 46 | 0 | -0.400 |
| 311 | populationPeak | 55 | 9 | -0.335 |
| 312 | resourcesGathered | 15971 | 5338 | -0.266 |
| 312 | resourcesUsed | 12950 | 4000 | -0.276 |
| 312 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 312 | unitsTrained | 49 | 0 | -0.400 |
| 312 | populationPeak | 58 | 9 | -0.338 |
| 313 | resourcesGathered | 15606 | 5481 | -0.260 |
| 313 | resourcesUsed | 12400 | 4000 | -0.271 |
| 313 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 313 | unitsTrained | 49 | 0 | -0.400 |
| 313 | populationPeak | 60 | 9 | -0.340 |
| 314 | resourcesGathered | 16102 | 5548 | -0.262 |
| 314 | resourcesUsed | 8400 | 3925 | -0.213 |
| 314 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 314 | unitsTrained | 44 | 0 | -0.400 |
| 314 | populationPeak | 53 | 9 | -0.332 |
| 315 | resourcesGathered | 11415 | 5413 | -0.210 |
| 315 | resourcesUsed | 6900 | 4000 | -0.168 |
| 315 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 315 | unitsTrained | 29 | 0 | -0.400 |
| 315 | populationPeak | 38 | 9 | -0.305 |
| 316 | resourcesGathered | 16504 | 5405 | -0.269 |
| 316 | resourcesUsed | 8800 | 3625 | -0.235 |
| 316 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 316 | unitsTrained | 48 | 0 | -0.400 |
| 316 | populationPeak | 57 | 9 | -0.337 |
| 317 | resourcesGathered | 15954 | 5510 | -0.262 |
| 317 | resourcesUsed | 8800 | 4000 | -0.218 |
| 317 | enemyUnitsKilled | 100 | 0 | -0.400 |
| 317 | unitsTrained | 48 | 0 | -0.400 |
| 317 | populationPeak | 56 | 9 | -0.336 |
| 318 | resourcesGathered | 17511 | 5373 | -0.277 |
| 318 | resourcesUsed | 12950 | 4000 | -0.276 |
| 318 | enemyUnitsKilled | 150 | 0 | -0.400 |
| 318 | unitsTrained | 50 | 0 | -0.400 |
| 318 | populationPeak | 60 | 9 | -0.340 |
| 319 | resourcesGathered | 14763 | 5304 | -0.256 |
| 319 | resourcesUsed | 8000 | 4000 | -0.200 |
| 319 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 319 | unitsTrained | 43 | 0 | -0.400 |
| 319 | populationPeak | 50 | 9 | -0.328 |
| 320 | resourcesGathered | 14591 | 5511 | -0.249 |
| 320 | resourcesUsed | 8725 | 3925 | -0.220 |
| 320 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 320 | unitsTrained | 46 | 0 | -0.400 |
| 320 | populationPeak | 55 | 9 | -0.335 |

## Totals

-13.05 total = 0.00 outcome + -13.05 quality + 0.00 survival

## Verdict

bad
