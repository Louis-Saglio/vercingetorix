# Report — baseline vs treatment

Settings: `-autostart=random/mainland -autostart-seed=<seed> -autostart-biome=generic/temperate -autostart-placement=circle -autostart-nonvisual -autostart-players=2 -autostart-size=128 -autostart-victory=conquest_civic_centers -autostart-ai=1:vercingetorix -autostart-ai=2:petra -autostart-aidiff=2:0 -autostart-civ=1:gaul -autostart-civ=2:rome -autostart-player=-1 -unique-logs -nosound -mod=public -mod=vercingetorix`

## Canary

PASS

## Pairs

| seed | base | treatment | outcome | survival | total | JS errors (base→treat) |
|---|---|---|---|---|---|---|
| 181 | draw | draw | +0.00 | +0.00 | -0.44 | 0→0 |
| 182 | draw | draw | +0.00 | +0.00 | -0.16 | 0→0 |
| 183 | draw | draw | +0.00 | +0.00 | +0.04 | 0→0 |
| 184 | draw | draw | +0.00 | +0.00 | -0.11 | 0→0 |
| 185 | draw | draw | +0.00 | +0.00 | -0.09 | 0→0 |
| 186 | draw | draw | +0.00 | +0.00 | +0.03 | 0→0 |
| 187 | draw | draw | +0.00 | +0.00 | +0.00 | 0→0 |
| 188 | draw | draw | +0.00 | +0.00 | -0.00 | 0→0 |
| 189 | draw | draw | +0.00 | +0.00 | +0.27 | 0→0 |
| 190 | draw | draw | +0.00 | +0.00 | +0.68 | 0→0 |

## Metric deltas

| seed | metric | base | treatment | weighted delta |
|---|---|---|---|---|
| 181 | resourcesGathered | 7748 | 7722 | -0.001 |
| 181 | resourcesUsed | 4675 | 4775 | +0.009 |
| 181 | enemyUnitsKilled | 100 | 0 | -0.400 |
| 181 | unitsTrained | 32 | 30 | -0.025 |
| 181 | populationPeak | 39 | 37 | -0.021 |
| 182 | resourcesGathered | 6484 | 6242 | -0.015 |
| 182 | resourcesUsed | 3075 | 2875 | -0.026 |
| 182 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 182 | unitsTrained | 16 | 13 | -0.075 |
| 182 | populationPeak | 25 | 22 | -0.048 |
| 183 | resourcesGathered | 5927 | 5995 | +0.005 |
| 183 | resourcesUsed | 2575 | 2775 | +0.031 |
| 183 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 183 | unitsTrained | 12 | 12 | +0.000 |
| 183 | populationPeak | 21 | 21 | +0.000 |
| 184 | resourcesGathered | 6789 | 6547 | -0.014 |
| 184 | resourcesUsed | 4275 | 4275 | +0.000 |
| 184 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 184 | unitsTrained | 28 | 24 | -0.057 |
| 184 | populationPeak | 34 | 31 | -0.035 |
| 185 | resourcesGathered | 7794 | 7516 | -0.014 |
| 185 | resourcesUsed | 4375 | 4375 | +0.000 |
| 185 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 185 | unitsTrained | 30 | 27 | -0.040 |
| 185 | populationPeak | 37 | 34 | -0.032 |
| 186 | resourcesGathered | 7947 | 7936 | -0.001 |
| 186 | resourcesUsed | 4375 | 4575 | +0.018 |
| 186 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 186 | unitsTrained | 30 | 30 | +0.000 |
| 186 | populationPeak | 37 | 38 | +0.011 |
| 187 | resourcesGathered | 3875 | 3875 | +0.000 |
| 187 | resourcesUsed | 300 | 300 | +0.000 |
| 187 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 187 | unitsTrained | 0 | 0 | +0.000 |
| 187 | populationPeak | 9 | 9 | +0.000 |
| 188 | resourcesGathered | 8522 | 8462 | -0.003 |
| 188 | resourcesUsed | 4975 | 5275 | +0.024 |
| 188 | enemyUnitsKilled | 250 | 250 | +0.000 |
| 188 | unitsTrained | 34 | 33 | -0.012 |
| 188 | populationPeak | 38 | 37 | -0.011 |
| 189 | resourcesGathered | 5019 | 5243 | +0.018 |
| 189 | resourcesUsed | 2275 | 2575 | +0.053 |
| 189 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 189 | unitsTrained | 9 | 12 | +0.133 |
| 189 | populationPeak | 17 | 20 | +0.071 |
| 190 | resourcesGathered | 6082 | 6861 | +0.051 |
| 190 | resourcesUsed | 2775 | 3875 | +0.159 |
| 190 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 190 | unitsTrained | 14 | 25 | +0.314 |
| 190 | populationPeak | 23 | 32 | +0.157 |

## Totals

0.22 total = 0.00 outcome + 0.22 quality + 0.00 survival

## Verdict

neutral
