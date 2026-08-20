# Report — baseline vs treatment

Settings: `-autostart=random/mainland -autostart-seed=<seed> -autostart-biome=generic/temperate -autostart-placement=circle -autostart-nonvisual -autostart-players=2 -autostart-size=128 -autostart-victory=conquest_civic_centers -autostart-ai=1:vercingetorix -autostart-ai=2:petra -autostart-aidiff=2:0 -autostart-civ=1:gaul -autostart-civ=2:rome -autostart-player=-1 -unique-logs -nosound -mod=public -mod=vercingetorix`

## Canary

PASS

## Pairs

| seed | base | treatment | outcome | survival | total | JS errors (base→treat) |
|---|---|---|---|---|---|---|
| 301 | draw | draw | +0.00 | +0.00 | -0.47 | 0→0 |
| 302 | draw | draw | +0.00 | +0.00 | -0.39 | 0→0 |
| 303 | draw | draw | +0.00 | +0.00 | -0.48 | 0→0 |
| 304 | draw | draw | +0.00 | +0.00 | -0.22 | 0→0 |
| 305 | draw | draw | +0.00 | +0.00 | -0.75 | 0→0 |
| 306 | draw | draw | +0.00 | +0.00 | -0.82 | 0→0 |
| 307 | draw | draw | +0.00 | +0.00 | -0.70 | 0→0 |
| 308 | draw | draw | +0.00 | +0.00 | -0.73 | 0→0 |
| 309 | draw | draw | +0.00 | +0.00 | -0.66 | 0→0 |
| 310 | draw | draw | +0.00 | +0.00 | -0.76 | 0→0 |

## Metric deltas

| seed | metric | base | treatment | weighted delta |
|---|---|---|---|---|
| 301 | resourcesGathered | 16489 | 8702 | -0.189 |
| 301 | resourcesUsed | 8500 | 7300 | -0.056 |
| 301 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 301 | unitsTrained | 48 | 35 | -0.108 |
| 301 | populationPeak | 57 | 41 | -0.112 |
| 302 | resourcesGathered | 14892 | 9846 | -0.136 |
| 302 | resourcesUsed | 10600 | 8000 | -0.098 |
| 302 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 302 | unitsTrained | 49 | 40 | -0.073 |
| 302 | populationPeak | 56 | 45 | -0.079 |
| 303 | resourcesGathered | 18066 | 9320 | -0.194 |
| 303 | resourcesUsed | 8800 | 7300 | -0.068 |
| 303 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 303 | unitsTrained | 48 | 35 | -0.108 |
| 303 | populationPeak | 57 | 41 | -0.112 |
| 304 | resourcesGathered | 14879 | 8326 | -0.176 |
| 304 | resourcesUsed | 10125 | 6725 | -0.134 |
| 304 | enemyUnitsKilled | 0 | 100 | +0.400 |
| 304 | unitsTrained | 46 | 27 | -0.165 |
| 304 | populationPeak | 55 | 35 | -0.145 |
| 305 | resourcesGathered | 15243 | 7903 | -0.193 |
| 305 | resourcesUsed | 11050 | 6500 | -0.165 |
| 305 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 305 | unitsTrained | 49 | 25 | -0.196 |
| 305 | populationPeak | 60 | 31 | -0.193 |
| 306 | resourcesGathered | 17560 | 7193 | -0.236 |
| 306 | resourcesUsed | 8900 | 5800 | -0.139 |
| 306 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 306 | unitsTrained | 49 | 21 | -0.229 |
| 306 | populationPeak | 58 | 27 | -0.214 |
| 307 | resourcesGathered | 15765 | 8679 | -0.180 |
| 307 | resourcesUsed | 12850 | 7000 | -0.182 |
| 307 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 307 | unitsTrained | 49 | 28 | -0.171 |
| 307 | populationPeak | 59 | 35 | -0.163 |
| 308 | resourcesGathered | 16682 | 7837 | -0.212 |
| 308 | resourcesUsed | 8500 | 6000 | -0.118 |
| 308 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 308 | unitsTrained | 48 | 23 | -0.208 |
| 308 | populationPeak | 57 | 30 | -0.189 |
| 309 | resourcesGathered | 17370 | 8643 | -0.201 |
| 309 | resourcesUsed | 8900 | 6800 | -0.094 |
| 309 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 309 | unitsTrained | 51 | 27 | -0.188 |
| 309 | populationPeak | 60 | 34 | -0.173 |
| 310 | resourcesGathered | 13860 | 7620 | -0.180 |
| 310 | resourcesUsed | 7600 | 5300 | -0.121 |
| 310 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 310 | unitsTrained | 36 | 13 | -0.256 |
| 310 | populationPeak | 45 | 22 | -0.204 |

## Totals

-5.96 total = 0.00 outcome + -5.96 quality + 0.00 survival

## Verdict

bad
