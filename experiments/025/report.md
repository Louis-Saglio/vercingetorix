# Report — baseline vs treatment

Settings: `-autostart=random/mainland -autostart-seed=<seed> -autostart-biome=generic/temperate -autostart-placement=circle -autostart-nonvisual -autostart-players=2 -autostart-size=128 -autostart-victory=conquest_civic_centers -autostart-ai=1:vercingetorix -autostart-ai=2:petra -autostart-aidiff=2:0 -autostart-civ=1:gaul -autostart-civ=2:rome -autostart-player=-1 -unique-logs -nosound -mod=public -mod=vercingetorix`

## Canary

PASS

## Pairs

| seed | base | treatment | outcome | survival | total | JS errors (base→treat) |
|---|---|---|---|---|---|---|
| 231 | draw | draw | +0.00 | +0.10 | -0.58 | 0→0 |
| 232 | draw | draw | +0.00 | +0.10 | -0.80 | 0→0 |
| 233 | draw | draw | +0.00 | +0.10 | -0.57 | 0→0 |
| 234 | draw | draw | +0.00 | +0.10 | -0.70 | 0→0 |
| 235 | draw | draw | +0.00 | +0.10 | -0.49 | 0→0 |
| 236 | draw | draw | +0.00 | +0.10 | -0.64 | 0→0 |
| 237 | draw | draw | +0.00 | +0.10 | -0.64 | 0→0 |
| 238 | draw | draw | +0.00 | +0.10 | -0.65 | 0→0 |
| 239 | draw | draw | +0.00 | +0.10 | -0.69 | 0→0 |
| 240 | draw | draw | +0.00 | +0.10 | -0.72 | 0→0 |

## Metric deltas

| seed | metric | base | treatment | weighted delta |
|---|---|---|---|---|
| 231 | resourcesGathered | 4188 | 4313 | +0.012 |
| 231 | resourcesUsed | 4475 | 3475 | -0.089 |
| 231 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 231 | unitsTrained | 9 | 0 | -0.400 |
| 231 | populationPeak | 18 | 9 | -0.200 |
| 232 | resourcesGathered | 4754 | 4501 | -0.021 |
| 232 | resourcesUsed | 4975 | 1975 | -0.241 |
| 232 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 232 | unitsTrained | 15 | 0 | -0.400 |
| 232 | populationPeak | 22 | 9 | -0.236 |
| 233 | resourcesGathered | 4367 | 4469 | +0.009 |
| 233 | resourcesUsed | 4675 | 3775 | -0.077 |
| 233 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 233 | unitsTrained | 12 | 0 | -0.400 |
| 233 | populationPeak | 18 | 9 | -0.200 |
| 234 | resourcesGathered | 4223 | 4425 | +0.019 |
| 234 | resourcesUsed | 4675 | 1975 | -0.231 |
| 234 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 234 | unitsTrained | 12 | 0 | -0.400 |
| 234 | populationPeak | 17 | 9 | -0.188 |
| 235 | resourcesGathered | 3994 | 4558 | +0.056 |
| 235 | resourcesUsed | 4375 | 3475 | -0.082 |
| 235 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 235 | unitsTrained | 9 | 0 | -0.400 |
| 235 | populationPeak | 15 | 9 | -0.160 |
| 236 | resourcesGathered | 4577 | 4439 | -0.012 |
| 236 | resourcesUsed | 4975 | 3475 | -0.121 |
| 236 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 236 | unitsTrained | 15 | 0 | -0.400 |
| 236 | populationPeak | 19 | 9 | -0.211 |
| 237 | resourcesGathered | 4759 | 4657 | -0.009 |
| 237 | resourcesUsed | 4875 | 3475 | -0.115 |
| 237 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 237 | unitsTrained | 13 | 0 | -0.400 |
| 237 | populationPeak | 20 | 9 | -0.220 |
| 238 | resourcesGathered | 4749 | 4642 | -0.009 |
| 238 | resourcesUsed | 4775 | 3475 | -0.109 |
| 238 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 238 | unitsTrained | 13 | 0 | -0.400 |
| 238 | populationPeak | 21 | 9 | -0.229 |
| 239 | resourcesGathered | 4155 | 4415 | +0.025 |
| 239 | resourcesUsed | 4675 | 1975 | -0.231 |
| 239 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 239 | unitsTrained | 11 | 0 | -0.400 |
| 239 | populationPeak | 17 | 9 | -0.188 |
| 240 | resourcesGathered | 4962 | 4542 | -0.034 |
| 240 | resourcesUsed | 5175 | 3475 | -0.131 |
| 240 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 240 | unitsTrained | 17 | 0 | -0.400 |
| 240 | populationPeak | 24 | 9 | -0.250 |

## Totals

-6.47 total = 0.00 outcome + -7.47 quality + 1.00 survival

## Verdict

bad
