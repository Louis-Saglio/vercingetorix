# Report — baseline vs treatment

Settings: `-autostart=random/mainland -autostart-seed=<seed> -autostart-biome=generic/temperate -autostart-placement=circle -autostart-nonvisual -autostart-players=2 -autostart-size=128 -autostart-victory=conquest_civic_centers -autostart-ai=1:vercingetorix -autostart-ai=2:petra -autostart-aidiff=2:0 -autostart-civ=1:gaul -autostart-civ=2:rome -autostart-player=-1 -unique-logs -nosound -mod=public -mod=vercingetorix`

## Canary

PASS

## Pairs

| seed | base | treatment | outcome | survival | total | JS errors (base→treat) |
|---|---|---|---|---|---|---|
| 201 | draw | draw | +0.00 | +0.00 | -1.01 | 0→0 |
| 202 | draw | draw | +0.00 | +0.00 | -0.85 | 0→0 |
| 203 | draw | draw | +0.00 | +0.00 | -0.55 | 0→0 |
| 204 | draw | draw | +0.00 | +0.00 | -1.08 | 0→0 |
| 205 | draw | draw | +0.00 | +0.00 | -0.22 | 0→0 |
| 206 | draw | draw | +0.00 | +0.00 | -0.99 | 0→0 |
| 207 | draw | draw | +0.00 | +0.00 | -1.02 | 0→0 |
| 208 | draw | draw | +0.00 | +0.00 | -1.04 | 0→0 |
| 209 | draw | draw | +0.00 | +0.00 | +0.00 | 0→0 |
| 210 | draw | draw | +0.00 | +0.00 | -0.93 | 0→0 |

## Metric deltas

| seed | metric | base | treatment | weighted delta |
|---|---|---|---|---|
| 201 | resourcesGathered | 8239 | 4591 | -0.177 |
| 201 | resourcesUsed | 4875 | 4775 | -0.008 |
| 201 | enemyUnitsKilled | 250 | 0 | -0.400 |
| 201 | unitsTrained | 33 | 13 | -0.242 |
| 201 | populationPeak | 39 | 21 | -0.185 |
| 202 | resourcesGathered | 5164 | 3728 | -0.111 |
| 202 | resourcesUsed | 2375 | 1575 | -0.135 |
| 202 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 202 | unitsTrained | 9 | 0 | -0.400 |
| 202 | populationPeak | 18 | 9 | -0.200 |
| 203 | resourcesGathered | 7604 | 4675 | -0.154 |
| 203 | resourcesUsed | 4475 | 4775 | +0.027 |
| 203 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 203 | unitsTrained | 31 | 12 | -0.245 |
| 203 | populationPeak | 38 | 21 | -0.179 |
| 204 | resourcesGathered | 7148 | 3868 | -0.184 |
| 204 | resourcesUsed | 3875 | 1775 | -0.217 |
| 204 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 204 | unitsTrained | 24 | 0 | -0.400 |
| 204 | populationPeak | 31 | 9 | -0.284 |
| 205 | resourcesGathered | 6097 | 4357 | -0.114 |
| 205 | resourcesUsed | 3375 | 4675 | +0.154 |
| 205 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 205 | unitsTrained | 20 | 12 | -0.160 |
| 205 | populationPeak | 27 | 20 | -0.104 |
| 206 | resourcesGathered | 6210 | 3804 | -0.155 |
| 206 | resourcesUsed | 2975 | 1575 | -0.188 |
| 206 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 206 | unitsTrained | 15 | 0 | -0.400 |
| 206 | populationPeak | 23 | 9 | -0.243 |
| 207 | resourcesGathered | 7975 | 4637 | -0.167 |
| 207 | resourcesUsed | 5075 | 4875 | -0.016 |
| 207 | enemyUnitsKilled | 850 | 0 | -0.400 |
| 207 | unitsTrained | 37 | 14 | -0.249 |
| 207 | populationPeak | 40 | 21 | -0.190 |
| 208 | resourcesGathered | 6845 | 3891 | -0.173 |
| 208 | resourcesUsed | 3475 | 1775 | -0.196 |
| 208 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 208 | unitsTrained | 21 | 0 | -0.400 |
| 208 | populationPeak | 28 | 9 | -0.271 |
| 209 | resourcesGathered | 3919 | 3919 | +0.000 |
| 209 | resourcesUsed | 300 | 300 | +0.000 |
| 209 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 209 | unitsTrained | 0 | 0 | +0.000 |
| 209 | populationPeak | 9 | 9 | +0.000 |
| 210 | resourcesGathered | 7533 | 4789 | -0.146 |
| 210 | resourcesUsed | 4675 | 4875 | +0.017 |
| 210 | enemyUnitsKilled | 650 | 0 | -0.400 |
| 210 | unitsTrained | 33 | 14 | -0.230 |
| 210 | populationPeak | 39 | 22 | -0.174 |

## Totals

-7.70 total = 0.00 outcome + -7.70 quality + 0.00 survival

## Verdict

bad
