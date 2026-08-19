# Report — baseline vs treatment

Settings: `-autostart=random/mainland -autostart-seed=<seed> -autostart-biome=generic/temperate -autostart-placement=circle -autostart-nonvisual -autostart-players=2 -autostart-size=128 -autostart-victory=conquest_civic_centers -autostart-ai=1:vercingetorix -autostart-ai=2:petra -autostart-aidiff=2:0 -autostart-civ=1:gaul -autostart-civ=2:rome -autostart-player=-1 -unique-logs -nosound -mod=public -mod=vercingetorix`

## Canary

PASS

## Pairs

| seed | base | treatment | outcome | survival | total | JS errors (base→treat) |
|---|---|---|---|---|---|---|
| 241 | draw | draw | +0.00 | +0.20 | +1.08 | 0→0 |
| 242 | draw | draw | +0.00 | +0.20 | +1.28 | 0→0 |
| 243 | draw | draw | +0.00 | +0.20 | +0.36 | 0→0 |
| 244 | draw | draw | +0.00 | +0.20 | +0.81 | 0→0 |
| 245 | draw | draw | +0.00 | +0.20 | +0.76 | 0→0 |
| 246 | draw | draw | +0.00 | +0.20 | +1.73 | 0→0 |
| 247 | draw | draw | +0.00 | +0.20 | +0.05 | 0→0 |
| 248 | draw | draw | +0.00 | +0.20 | +1.27 | 0→0 |
| 249 | draw | draw | +0.00 | +0.20 | +1.07 | 0→0 |
| 250 | draw | draw | +0.00 | +0.20 | +1.11 | 0→0 |

## Metric deltas

| seed | metric | base | treatment | weighted delta |
|---|---|---|---|---|
| 241 | resourcesGathered | 4503 | 6721 | +0.197 |
| 241 | resourcesUsed | 5075 | 6175 | +0.087 |
| 241 | enemyUnitsKilled | 0 | 1000 | +0.400 |
| 241 | unitsTrained | 15 | 17 | +0.053 |
| 241 | populationPeak | 19 | 26 | +0.147 |
| 242 | resourcesGathered | 4617 | 7196 | +0.223 |
| 242 | resourcesUsed | 4875 | 6475 | +0.131 |
| 242 | enemyUnitsKilled | 0 | 2050 | +0.400 |
| 242 | unitsTrained | 14 | 20 | +0.171 |
| 242 | populationPeak | 21 | 29 | +0.152 |
| 243 | resourcesGathered | 3857 | 5389 | +0.159 |
| 243 | resourcesUsed | 300 | 300 | +0.000 |
| 243 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 243 | unitsTrained | 0 | 0 | +0.000 |
| 243 | populationPeak | 9 | 9 | +0.000 |
| 244 | resourcesGathered | 4349 | 8652 | +0.396 |
| 244 | resourcesUsed | 4875 | 5175 | +0.025 |
| 244 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 244 | unitsTrained | 14 | 17 | +0.086 |
| 244 | populationPeak | 20 | 25 | +0.100 |
| 245 | resourcesGathered | 4976 | 6507 | +0.123 |
| 245 | resourcesUsed | 5375 | 6525 | +0.086 |
| 245 | enemyUnitsKilled | 0 | 850 | +0.400 |
| 245 | unitsTrained | 19 | 16 | -0.063 |
| 245 | populationPeak | 24 | 25 | +0.017 |
| 246 | resourcesGathered | 4183 | 6592 | +0.230 |
| 246 | resourcesUsed | 4275 | 6175 | +0.178 |
| 246 | enemyUnitsKilled | 0 | 1050 | +0.400 |
| 246 | unitsTrained | 8 | 17 | +0.400 |
| 246 | populationPeak | 15 | 27 | +0.320 |
| 247 | resourcesGathered | 3974 | 6059 | +0.210 |
| 247 | resourcesUsed | 4375 | 3875 | -0.046 |
| 247 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 247 | unitsTrained | 9 | 4 | -0.222 |
| 247 | populationPeak | 17 | 13 | -0.094 |
| 248 | resourcesGathered | 4508 | 6796 | +0.203 |
| 248 | resourcesUsed | 4975 | 6725 | +0.141 |
| 248 | enemyUnitsKilled | 0 | 1050 | +0.400 |
| 248 | unitsTrained | 14 | 19 | +0.143 |
| 248 | populationPeak | 20 | 29 | +0.180 |
| 249 | resourcesGathered | 4683 | 6831 | +0.183 |
| 249 | resourcesUsed | 4875 | 6175 | +0.107 |
| 249 | enemyUnitsKilled | 0 | 200 | +0.400 |
| 249 | unitsTrained | 14 | 17 | +0.086 |
| 249 | populationPeak | 21 | 26 | +0.095 |
| 250 | resourcesGathered | 5065 | 6977 | +0.151 |
| 250 | resourcesUsed | 4875 | 6625 | +0.144 |
| 250 | enemyUnitsKilled | 0 | 1050 | +0.400 |
| 250 | unitsTrained | 14 | 17 | +0.086 |
| 250 | populationPeak | 22 | 29 | +0.127 |

## Totals

9.51 total = 0.00 outcome + 7.51 quality + 2.00 survival

## Verdict

good
