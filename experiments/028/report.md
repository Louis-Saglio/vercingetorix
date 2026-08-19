# Report — baseline vs treatment

Settings: `-autostart=random/mainland -autostart-seed=<seed> -autostart-biome=generic/temperate -autostart-placement=circle -autostart-nonvisual -autostart-players=2 -autostart-size=128 -autostart-victory=conquest_civic_centers -autostart-ai=1:vercingetorix -autostart-ai=2:petra -autostart-aidiff=2:0 -autostart-civ=1:gaul -autostart-civ=2:rome -autostart-player=-1 -unique-logs -nosound -mod=public -mod=vercingetorix`

## Canary

PASS

## Pairs

| seed | base | treatment | outcome | survival | total | JS errors (base→treat) |
|---|---|---|---|---|---|---|
| 261 | draw | draw | +0.00 | +0.20 | +1.31 | 0→0 |
| 262 | draw | draw | +0.00 | +0.20 | +0.65 | 0→0 |
| 263 | draw | draw | +0.00 | +0.20 | +0.70 | 0→0 |
| 264 | draw | draw | +0.00 | +0.20 | +0.73 | 0→0 |
| 265 | draw | draw | +0.00 | +0.20 | +1.03 | 0→0 |
| 266 | draw | draw | +0.00 | +0.20 | +0.97 | 0→0 |
| 267 | draw | draw | +0.00 | +0.20 | +0.79 | 0→0 |
| 268 | draw | draw | +0.00 | +0.20 | +1.10 | 0→0 |
| 269 | draw | draw | +0.00 | +0.20 | +1.08 | 0→0 |
| 270 | draw | draw | +0.00 | +0.20 | +0.94 | 0→0 |

## Metric deltas

| seed | metric | base | treatment | weighted delta |
|---|---|---|---|---|
| 261 | resourcesGathered | 4238 | 10293 | +0.400 |
| 261 | resourcesUsed | 4375 | 5500 | +0.103 |
| 261 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 261 | unitsTrained | 9 | 18 | +0.400 |
| 261 | populationPeak | 17 | 26 | +0.212 |
| 262 | resourcesGathered | 5019 | 10030 | +0.399 |
| 262 | resourcesUsed | 5275 | 5700 | +0.032 |
| 262 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 262 | unitsTrained | 17 | 17 | +0.000 |
| 262 | populationPeak | 24 | 25 | +0.017 |
| 263 | resourcesGathered | 4798 | 9597 | +0.400 |
| 263 | resourcesUsed | 5275 | 5625 | +0.027 |
| 263 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 263 | unitsTrained | 17 | 17 | +0.000 |
| 263 | populationPeak | 22 | 26 | +0.073 |
| 264 | resourcesGathered | 4897 | 10551 | +0.400 |
| 264 | resourcesUsed | 5175 | 5900 | +0.056 |
| 264 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 264 | unitsTrained | 17 | 18 | +0.024 |
| 264 | populationPeak | 24 | 27 | +0.050 |
| 265 | resourcesGathered | 4264 | 8523 | +0.400 |
| 265 | resourcesUsed | 4375 | 5400 | +0.094 |
| 265 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 265 | unitsTrained | 9 | 14 | +0.222 |
| 265 | populationPeak | 17 | 22 | +0.118 |
| 266 | resourcesGathered | 4138 | 9062 | +0.400 |
| 266 | resourcesUsed | 4575 | 5400 | +0.072 |
| 266 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 266 | unitsTrained | 10 | 14 | +0.160 |
| 266 | populationPeak | 17 | 23 | +0.141 |
| 267 | resourcesGathered | 4887 | 10723 | +0.400 |
| 267 | resourcesUsed | 4975 | 5725 | +0.060 |
| 267 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 267 | unitsTrained | 15 | 18 | +0.080 |
| 267 | populationPeak | 23 | 26 | +0.052 |
| 268 | resourcesGathered | 3704 | 6694 | +0.323 |
| 268 | resourcesUsed | 300 | 4400 | +0.400 |
| 268 | enemyUnitsKilled | 100 | 0 | -0.400 |
| 268 | unitsTrained | 0 | 4 | +0.400 |
| 268 | populationPeak | 9 | 13 | +0.178 |
| 269 | resourcesGathered | 3790 | 6653 | +0.302 |
| 269 | resourcesUsed | 300 | 4400 | +0.400 |
| 269 | enemyUnitsKilled | 200 | 0 | -0.400 |
| 269 | unitsTrained | 0 | 4 | +0.400 |
| 269 | populationPeak | 9 | 13 | +0.178 |
| 270 | resourcesGathered | 3880 | 7722 | +0.396 |
| 270 | resourcesUsed | 4475 | 5300 | +0.074 |
| 270 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 270 | unitsTrained | 10 | 13 | +0.120 |
| 270 | populationPeak | 16 | 22 | +0.150 |

## Totals

9.31 total = 0.00 outcome + 7.31 quality + 2.00 survival

## Verdict

good
