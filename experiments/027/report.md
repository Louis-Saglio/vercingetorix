# Report — baseline vs treatment

Settings: `-autostart=random/mainland -autostart-seed=<seed> -autostart-biome=generic/temperate -autostart-placement=circle -autostart-nonvisual -autostart-players=2 -autostart-size=128 -autostart-victory=conquest_civic_centers -autostart-ai=1:vercingetorix -autostart-ai=2:petra -autostart-aidiff=2:0 -autostart-civ=1:gaul -autostart-civ=2:rome -autostart-player=-1 -unique-logs -nosound -mod=public -mod=vercingetorix`

## Canary

PASS

## Pairs

| seed | base | treatment | outcome | survival | total | JS errors (base→treat) |
|---|---|---|---|---|---|---|
| 251 | draw | draw | +0.00 | +0.20 | +1.44 | 0→0 |
| 252 | draw | draw | +0.00 | +0.20 | +1.69 | 0→0 |
| 253 | draw | draw | +0.00 | +0.20 | +0.48 | 0→0 |
| 254 | draw | draw | +0.00 | +0.20 | +0.00 | 0→0 |
| 255 | draw | draw | +0.00 | +0.20 | +0.96 | 0→0 |
| 256 | draw | draw | +0.00 | +0.20 | +1.26 | 0→0 |
| 257 | draw | draw | +0.00 | +0.20 | +1.13 | 0→0 |
| 258 | draw | draw | +0.00 | +0.20 | +1.05 | 0→0 |
| 259 | draw | draw | +0.00 | +0.20 | +0.61 | 0→0 |
| 260 | draw | draw | +0.00 | +0.20 | +1.05 | 0→0 |

## Metric deltas

| seed | metric | base | treatment | weighted delta |
|---|---|---|---|---|
| 251 | resourcesGathered | 4223 | 6757 | +0.240 |
| 251 | resourcesUsed | 4775 | 6625 | +0.155 |
| 251 | enemyUnitsKilled | 0 | 1450 | +0.400 |
| 251 | unitsTrained | 12 | 18 | +0.200 |
| 251 | populationPeak | 18 | 29 | +0.244 |
| 252 | resourcesGathered | 3949 | 6765 | +0.285 |
| 252 | resourcesUsed | 300 | 5475 | +0.400 |
| 252 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 252 | unitsTrained | 0 | 17 | +0.400 |
| 252 | populationPeak | 9 | 26 | +0.400 |
| 253 | resourcesGathered | 4496 | 5985 | +0.132 |
| 253 | resourcesUsed | 4875 | 5075 | +0.016 |
| 253 | enemyUnitsKilled | 0 | 250 | +0.400 |
| 253 | unitsTrained | 13 | 6 | -0.215 |
| 253 | populationPeak | 21 | 18 | -0.057 |
| 254 | resourcesGathered | 4226 | 6438 | +0.209 |
| 254 | resourcesUsed | 4475 | 3875 | -0.054 |
| 254 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 254 | unitsTrained | 10 | 4 | -0.240 |
| 254 | populationPeak | 18 | 13 | -0.111 |
| 255 | resourcesGathered | 4971 | 6947 | +0.159 |
| 255 | resourcesUsed | 5175 | 6625 | +0.112 |
| 255 | enemyUnitsKilled | 0 | 500 | +0.400 |
| 255 | unitsTrained | 17 | 18 | +0.024 |
| 255 | populationPeak | 24 | 28 | +0.067 |
| 256 | resourcesGathered | 4408 | 6775 | +0.215 |
| 256 | resourcesUsed | 4975 | 7075 | +0.169 |
| 256 | enemyUnitsKilled | 0 | 600 | +0.400 |
| 256 | unitsTrained | 14 | 18 | +0.114 |
| 256 | populationPeak | 20 | 28 | +0.160 |
| 257 | resourcesGathered | 4641 | 6826 | +0.188 |
| 257 | resourcesUsed | 4975 | 6625 | +0.133 |
| 257 | enemyUnitsKilled | 0 | 1100 | +0.400 |
| 257 | unitsTrained | 15 | 18 | +0.080 |
| 257 | populationPeak | 21 | 28 | +0.133 |
| 258 | resourcesGathered | 4929 | 6974 | +0.166 |
| 258 | resourcesUsed | 5075 | 6725 | +0.130 |
| 258 | enemyUnitsKilled | 0 | 1400 | +0.400 |
| 258 | unitsTrained | 16 | 19 | +0.075 |
| 258 | populationPeak | 24 | 29 | +0.083 |
| 259 | resourcesGathered | 4254 | 5861 | +0.151 |
| 259 | resourcesUsed | 4575 | 5075 | +0.044 |
| 259 | enemyUnitsKilled | 0 | 350 | +0.400 |
| 259 | unitsTrained | 11 | 6 | -0.182 |
| 259 | populationPeak | 19 | 19 | +0.000 |
| 260 | resourcesGathered | 4880 | 7737 | +0.234 |
| 260 | resourcesUsed | 5375 | 6575 | +0.089 |
| 260 | enemyUnitsKilled | 0 | 1900 | +0.400 |
| 260 | unitsTrained | 19 | 21 | +0.042 |
| 260 | populationPeak | 25 | 30 | +0.080 |

## Totals

9.67 total = 0.00 outcome + 7.67 quality + 2.00 survival

## Verdict

good
