# Report — baseline vs treatment

Settings: `-autostart=random/mainland -autostart-seed=<seed> -autostart-biome=generic/temperate -autostart-placement=circle -autostart-nonvisual -autostart-players=2 -autostart-size=128 -autostart-victory=conquest_civic_centers -autostart-ai=1:vercingetorix -autostart-ai=2:petra -autostart-aidiff=2:0 -autostart-civ=1:gaul -autostart-civ=2:rome -autostart-player=-1 -unique-logs -nosound -mod=public -mod=vercingetorix`

## Canary

PASS

## Pairs

| seed | base | treatment | outcome | survival | total | JS errors (base→treat) |
|---|---|---|---|---|---|---|
| 211 | draw | draw | +0.00 | +0.00 | -1.09 | 0→0 |
| 212 | draw | draw | +0.00 | +0.00 | -0.92 | 0→0 |
| 213 | draw | draw | +0.00 | +0.00 | -0.95 | 0→0 |
| 214 | draw | draw | +0.00 | +0.00 | -0.59 | 0→0 |
| 215 | draw | draw | +0.00 | +0.00 | +0.29 | 0→0 |
| 216 | draw | draw | +0.00 | +0.00 | -0.20 | 0→0 |
| 217 | draw | draw | +0.00 | +0.00 | -0.40 | 0→0 |
| 218 | draw | draw | +0.00 | +0.00 | +0.30 | 0→0 |
| 219 | draw | draw | +0.00 | +0.00 | -0.86 | 0→0 |
| 220 | draw | draw | +0.00 | +0.00 | -0.39 | 0→0 |

## Metric deltas

| seed | metric | base | treatment | weighted delta |
|---|---|---|---|---|
| 211 | resourcesGathered | 7777 | 4304 | -0.179 |
| 211 | resourcesUsed | 5075 | 4675 | -0.032 |
| 211 | enemyUnitsKilled | 850 | 0 | -0.400 |
| 211 | unitsTrained | 36 | 12 | -0.267 |
| 211 | populationPeak | 38 | 18 | -0.211 |
| 212 | resourcesGathered | 7869 | 4618 | -0.165 |
| 212 | resourcesUsed | 4775 | 5175 | +0.034 |
| 212 | enemyUnitsKilled | 350 | 0 | -0.400 |
| 212 | unitsTrained | 34 | 16 | -0.212 |
| 212 | populationPeak | 39 | 22 | -0.174 |
| 213 | resourcesGathered | 7825 | 4748 | -0.157 |
| 213 | resourcesUsed | 4875 | 5075 | +0.016 |
| 213 | enemyUnitsKilled | 350 | 0 | -0.400 |
| 213 | unitsTrained | 35 | 15 | -0.229 |
| 213 | populationPeak | 40 | 22 | -0.180 |
| 214 | resourcesGathered | 6321 | 4321 | -0.127 |
| 214 | resourcesUsed | 3375 | 4875 | +0.178 |
| 214 | enemyUnitsKilled | 100 | 0 | -0.400 |
| 214 | unitsTrained | 20 | 13 | -0.140 |
| 214 | populationPeak | 27 | 20 | -0.104 |
| 215 | resourcesGathered | 5441 | 4364 | -0.079 |
| 215 | resourcesUsed | 2575 | 4875 | +0.357 |
| 215 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 215 | unitsTrained | 12 | 13 | +0.033 |
| 215 | populationPeak | 20 | 19 | -0.020 |
| 216 | resourcesGathered | 5408 | 4034 | -0.102 |
| 216 | resourcesUsed | 2875 | 4475 | +0.223 |
| 216 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 216 | unitsTrained | 15 | 9 | -0.160 |
| 216 | populationPeak | 23 | 14 | -0.157 |
| 217 | resourcesGathered | 6939 | 4519 | -0.140 |
| 217 | resourcesUsed | 3975 | 4775 | +0.081 |
| 217 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 217 | unitsTrained | 25 | 13 | -0.192 |
| 217 | populationPeak | 33 | 21 | -0.145 |
| 218 | resourcesGathered | 5243 | 4330 | -0.070 |
| 218 | resourcesUsed | 2275 | 4375 | +0.369 |
| 218 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 218 | unitsTrained | 9 | 9 | +0.000 |
| 218 | populationPeak | 17 | 17 | +0.000 |
| 219 | resourcesGathered | 8230 | 4882 | -0.163 |
| 219 | resourcesUsed | 4675 | 5275 | +0.051 |
| 219 | enemyUnitsKilled | 100 | 0 | -0.400 |
| 219 | unitsTrained | 33 | 18 | -0.182 |
| 219 | populationPeak | 39 | 23 | -0.164 |
| 220 | resourcesGathered | 7314 | 4554 | -0.151 |
| 220 | resourcesUsed | 3875 | 4875 | +0.103 |
| 220 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 220 | unitsTrained | 25 | 13 | -0.192 |
| 220 | populationPeak | 32 | 20 | -0.150 |

## Totals

-4.80 total = 0.00 outcome + -4.80 quality + 0.00 survival

## Verdict

bad
