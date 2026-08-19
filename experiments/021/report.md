# Report — baseline vs treatment

Settings: `-autostart=random/mainland -autostart-seed=<seed> -autostart-biome=generic/temperate -autostart-placement=circle -autostart-nonvisual -autostart-players=2 -autostart-size=128 -autostart-victory=conquest_civic_centers -autostart-ai=1:vercingetorix -autostart-ai=2:petra -autostart-aidiff=2:0 -autostart-civ=1:gaul -autostart-civ=2:rome -autostart-player=-1 -unique-logs -nosound -mod=public -mod=vercingetorix`

## Canary

PASS

## Pairs

| seed | base | treatment | outcome | survival | total | JS errors (base→treat) |
|---|---|---|---|---|---|---|
| 191 | draw | draw | +0.00 | +0.00 | -1.58 | 0→0 |
| 192 | draw | draw | +0.00 | +0.00 | -0.97 | 0→0 |
| 193 | draw | draw | +0.00 | +0.00 | +0.00 | 0→0 |
| 194 | draw | draw | +0.00 | +0.00 | -1.11 | 0→0 |
| 195 | draw | draw | +0.00 | +0.00 | -1.17 | 0→0 |
| 196 | draw | draw | +0.00 | +0.00 | -1.16 | 0→0 |
| 197 | draw | draw | +0.00 | +0.00 | -1.59 | 0→0 |
| 198 | draw | draw | +0.00 | +0.00 | -0.93 | 0→0 |
| 199 | draw | draw | +0.00 | +0.00 | +0.00 | 0→0 |
| 200 | draw | draw | +0.00 | +0.00 | -1.09 | 0→0 |

## Metric deltas

| seed | metric | base | treatment | weighted delta |
|---|---|---|---|---|
| 191 | resourcesGathered | 7387 | 3709 | -0.199 |
| 191 | resourcesUsed | 4375 | 1375 | -0.274 |
| 191 | enemyUnitsKilled | 150 | 0 | -0.400 |
| 191 | unitsTrained | 30 | 0 | -0.400 |
| 191 | populationPeak | 38 | 9 | -0.305 |
| 192 | resourcesGathered | 4837 | 3880 | -0.079 |
| 192 | resourcesUsed | 3275 | 1375 | -0.232 |
| 192 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 192 | unitsTrained | 19 | 0 | -0.400 |
| 192 | populationPeak | 26 | 9 | -0.262 |
| 193 | resourcesGathered | 3835 | 3835 | +0.000 |
| 193 | resourcesUsed | 300 | 300 | +0.000 |
| 193 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 193 | unitsTrained | 0 | 0 | +0.000 |
| 193 | populationPeak | 9 | 9 | +0.000 |
| 194 | resourcesGathered | 7223 | 3792 | -0.190 |
| 194 | resourcesUsed | 3875 | 1575 | -0.237 |
| 194 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 194 | unitsTrained | 25 | 0 | -0.400 |
| 194 | populationPeak | 32 | 9 | -0.288 |
| 195 | resourcesGathered | 7853 | 3876 | -0.203 |
| 195 | resourcesUsed | 4675 | 1575 | -0.265 |
| 195 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 195 | unitsTrained | 31 | 0 | -0.400 |
| 195 | populationPeak | 38 | 9 | -0.305 |
| 196 | resourcesGathered | 7325 | 3659 | -0.200 |
| 196 | resourcesUsed | 4375 | 1575 | -0.256 |
| 196 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 196 | unitsTrained | 30 | 0 | -0.400 |
| 196 | populationPeak | 36 | 9 | -0.300 |
| 197 | resourcesGathered | 7893 | 3989 | -0.198 |
| 197 | resourcesUsed | 5075 | 1375 | -0.292 |
| 197 | enemyUnitsKilled | 850 | 0 | -0.400 |
| 197 | unitsTrained | 37 | 0 | -0.400 |
| 197 | populationPeak | 38 | 9 | -0.305 |
| 198 | resourcesGathered | 5860 | 3714 | -0.146 |
| 198 | resourcesUsed | 2575 | 1575 | -0.155 |
| 198 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 198 | unitsTrained | 12 | 0 | -0.400 |
| 198 | populationPeak | 21 | 9 | -0.229 |
| 199 | resourcesGathered | 3783 | 3783 | +0.000 |
| 199 | resourcesUsed | 300 | 300 | +0.000 |
| 199 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 199 | unitsTrained | 0 | 0 | +0.000 |
| 199 | populationPeak | 9 | 9 | +0.000 |
| 200 | resourcesGathered | 7316 | 3914 | -0.186 |
| 200 | resourcesUsed | 3875 | 1775 | -0.217 |
| 200 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 200 | unitsTrained | 24 | 0 | -0.400 |
| 200 | populationPeak | 31 | 9 | -0.284 |

## Totals

-9.61 total = 0.00 outcome + -9.61 quality + 0.00 survival

## Verdict

bad
