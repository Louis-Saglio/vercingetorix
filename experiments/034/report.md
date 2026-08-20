# Report — baseline vs treatment

Settings: `-autostart=random/mainland -autostart-seed=<seed> -autostart-biome=generic/temperate -autostart-placement=circle -autostart-nonvisual -autostart-players=2 -autostart-size=128 -autostart-victory=conquest_civic_centers -autostart-ai=1:vercingetorix -autostart-ai=2:petra -autostart-aidiff=2:0 -autostart-civ=1:gaul -autostart-civ=2:rome -autostart-player=-1 -unique-logs -nosound -mod=public -mod=vercingetorix`

## Canary

PASS

## Pairs

| seed | base | treatment | outcome | survival | total | JS errors (base→treat) |
|---|---|---|---|---|---|---|
| 301 | draw | draw | +0.00 | +0.00 | -0.22 | 0→0 |
| 302 | draw | draw | +0.00 | +0.00 | +0.04 | 0→0 |
| 303 | draw | draw | +0.00 | +0.00 | -0.07 | 0→0 |
| 304 | draw | draw | +0.00 | +0.00 | -0.05 | 0→0 |
| 305 | draw | draw | +0.00 | +0.00 | +0.42 | 0→0 |
| 306 | draw | draw | +0.00 | +0.00 | +0.17 | 0→0 |
| 307 | draw | draw | +0.00 | +0.00 | -0.95 | 0→0 |
| 308 | draw | draw | +0.00 | +0.00 | -0.01 | 0→0 |
| 309 | draw | win | +2.00 | +0.00 | +2.09 | 0→0 |
| 310 | draw | draw | +0.00 | +0.00 | +0.53 | 0→0 |

## Metric deltas

| seed | metric | base | treatment | weighted delta |
|---|---|---|---|---|
| 301 | resourcesGathered | 16489 | 12589 | -0.095 |
| 301 | resourcesUsed | 8500 | 8000 | -0.024 |
| 301 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 301 | unitsTrained | 48 | 43 | -0.042 |
| 301 | populationPeak | 57 | 49 | -0.056 |
| 302 | resourcesGathered | 14892 | 17440 | +0.068 |
| 302 | resourcesUsed | 10600 | 10150 | -0.017 |
| 302 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 302 | unitsTrained | 49 | 48 | -0.008 |
| 302 | populationPeak | 56 | 56 | +0.000 |
| 303 | resourcesGathered | 18066 | 15729 | -0.052 |
| 303 | resourcesUsed | 8800 | 8500 | -0.014 |
| 303 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 303 | unitsTrained | 48 | 48 | +0.000 |
| 303 | populationPeak | 57 | 57 | +0.000 |
| 304 | resourcesGathered | 14879 | 15786 | +0.024 |
| 304 | resourcesUsed | 10125 | 8325 | -0.071 |
| 304 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 304 | unitsTrained | 46 | 46 | +0.000 |
| 304 | populationPeak | 55 | 55 | +0.000 |
| 305 | resourcesGathered | 15243 | 15353 | +0.003 |
| 305 | resourcesUsed | 11050 | 10900 | -0.005 |
| 305 | enemyUnitsKilled | 0 | 200 | +0.400 |
| 305 | unitsTrained | 49 | 52 | +0.024 |
| 305 | populationPeak | 60 | 60 | +0.000 |
| 306 | resourcesGathered | 17560 | 17249 | -0.007 |
| 306 | resourcesUsed | 8900 | 12950 | +0.182 |
| 306 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 306 | unitsTrained | 49 | 49 | +0.000 |
| 306 | populationPeak | 58 | 58 | +0.000 |
| 307 | resourcesGathered | 15765 | 8446 | -0.186 |
| 307 | resourcesUsed | 12850 | 5400 | -0.232 |
| 307 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 307 | unitsTrained | 49 | 14 | -0.286 |
| 307 | populationPeak | 59 | 22 | -0.251 |
| 308 | resourcesGathered | 16682 | 16406 | -0.007 |
| 308 | resourcesUsed | 8500 | 8500 | +0.000 |
| 308 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 308 | unitsTrained | 48 | 48 | +0.000 |
| 308 | populationPeak | 57 | 56 | -0.007 |
| 309 | resourcesGathered | 17370 | 9177 | -0.189 |
| 309 | resourcesUsed | 8900 | 9000 | +0.004 |
| 309 | enemyUnitsKilled | 0 | 3700 | +0.400 |
| 309 | unitsTrained | 51 | 43 | -0.063 |
| 309 | populationPeak | 60 | 51 | -0.060 |
| 310 | resourcesGathered | 13860 | 10237 | -0.105 |
| 310 | resourcesUsed | 7600 | 9100 | +0.079 |
| 310 | enemyUnitsKilled | 0 | 2450 | +0.400 |
| 310 | unitsTrained | 36 | 44 | +0.089 |
| 310 | populationPeak | 45 | 52 | +0.062 |

## Totals

1.96 total = 2.00 outcome + -0.04 quality + 0.00 survival

## Verdict

neutral
