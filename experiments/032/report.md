# Report — baseline vs treatment

Settings: `-autostart=random/mainland -autostart-seed=<seed> -autostart-biome=generic/temperate -autostart-placement=circle -autostart-nonvisual -autostart-players=2 -autostart-size=128 -autostart-victory=conquest_civic_centers -autostart-ai=1:vercingetorix -autostart-ai=2:petra -autostart-aidiff=2:0 -autostart-civ=1:gaul -autostart-civ=2:rome -autostart-player=-1 -unique-logs -nosound -mod=public -mod=vercingetorix`

## Canary

PASS

## Pairs

| seed | base | treatment | outcome | survival | total | JS errors (base→treat) |
|---|---|---|---|---|---|---|
| 291 | draw | draw | +0.00 | +0.00 | -0.12 | 0→0 |
| 292 | draw | draw | +0.00 | +0.00 | +0.16 | 0→0 |
| 293 | draw | draw | +0.00 | +0.00 | -0.01 | 0→0 |
| 294 | draw | draw | +0.00 | +0.00 | -0.05 | 0→0 |
| 295 | draw | draw | +0.00 | +0.00 | -0.93 | 0→0 |
| 296 | draw | draw | +0.00 | +0.00 | -0.11 | 0→0 |
| 297 | draw | draw | +0.00 | +0.00 | +0.23 | 0→0 |
| 298 | draw | draw | +0.00 | +0.00 | +0.02 | 0→0 |
| 299 | draw | draw | +0.00 | +0.00 | +0.29 | 0→0 |
| 300 | draw | draw | +0.00 | +0.00 | -0.19 | 0→0 |

## Metric deltas

| seed | metric | base | treatment | weighted delta |
|---|---|---|---|---|
| 291 | resourcesGathered | 17671 | 10720 | -0.157 |
| 291 | resourcesUsed | 9100 | 7200 | -0.084 |
| 291 | enemyUnitsKilled | 250 | 1550 | +0.400 |
| 291 | unitsTrained | 51 | 32 | -0.149 |
| 291 | populationPeak | 58 | 39 | -0.131 |
| 292 | resourcesGathered | 13659 | 10334 | -0.097 |
| 292 | resourcesUsed | 8825 | 8875 | +0.002 |
| 292 | enemyUnitsKilled | 0 | 2100 | +0.400 |
| 292 | unitsTrained | 46 | 39 | -0.061 |
| 292 | populationPeak | 53 | 42 | -0.083 |
| 293 | resourcesGathered | 15415 | 7678 | -0.201 |
| 293 | resourcesUsed | 8100 | 7300 | -0.040 |
| 293 | enemyUnitsKilled | 100 | 2250 | +0.400 |
| 293 | unitsTrained | 41 | 33 | -0.078 |
| 293 | populationPeak | 50 | 39 | -0.088 |
| 294 | resourcesGathered | 16299 | 10863 | -0.133 |
| 294 | resourcesUsed | 9725 | 7125 | -0.107 |
| 294 | enemyUnitsKilled | 0 | 1750 | +0.400 |
| 294 | unitsTrained | 46 | 35 | -0.096 |
| 294 | populationPeak | 55 | 40 | -0.109 |
| 295 | resourcesGathered | 17956 | 9452 | -0.189 |
| 295 | resourcesUsed | 12950 | 5500 | -0.230 |
| 295 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 295 | unitsTrained | 49 | 15 | -0.278 |
| 295 | populationPeak | 58 | 24 | -0.234 |
| 296 | resourcesGathered | 16856 | 8839 | -0.190 |
| 296 | resourcesUsed | 8800 | 7400 | -0.064 |
| 296 | enemyUnitsKilled | 0 | 1550 | +0.400 |
| 296 | unitsTrained | 48 | 34 | -0.117 |
| 296 | populationPeak | 57 | 37 | -0.140 |
| 297 | resourcesGathered | 14163 | 10206 | -0.112 |
| 297 | resourcesUsed | 8200 | 9400 | +0.059 |
| 297 | enemyUnitsKilled | 0 | 2350 | +0.400 |
| 297 | unitsTrained | 42 | 40 | -0.019 |
| 297 | populationPeak | 51 | 39 | -0.094 |
| 298 | resourcesGathered | 15450 | 8698 | -0.175 |
| 298 | resourcesUsed | 9650 | 8150 | -0.062 |
| 298 | enemyUnitsKilled | 250 | 3000 | +0.400 |
| 298 | unitsTrained | 42 | 36 | -0.057 |
| 298 | populationPeak | 50 | 39 | -0.088 |
| 299 | resourcesGathered | 12244 | 8012 | -0.138 |
| 299 | resourcesUsed | 6900 | 5300 | -0.093 |
| 299 | enemyUnitsKilled | 0 | 2000 | +0.400 |
| 299 | unitsTrained | 28 | 33 | +0.071 |
| 299 | populationPeak | 35 | 39 | +0.046 |
| 300 | resourcesGathered | 17045 | 9523 | -0.177 |
| 300 | resourcesUsed | 12700 | 7900 | -0.151 |
| 300 | enemyUnitsKilled | 550 | 3250 | +0.400 |
| 300 | unitsTrained | 52 | 39 | -0.100 |
| 300 | populationPeak | 60 | 36 | -0.160 |

## Totals

-0.70 total = 0.00 outcome + -0.70 quality + 0.00 survival

## Verdict

neutral
