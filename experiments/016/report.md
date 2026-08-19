# Report — baseline vs treatment

Settings: `-autostart=random/mainland -autostart-seed=<seed> -autostart-biome=generic/temperate -autostart-placement=circle -autostart-nonvisual -autostart-players=2 -autostart-size=128 -autostart-victory=conquest_civic_centers -autostart-ai=1:vercingetorix -autostart-ai=2:petra -autostart-aidiff=2:0 -autostart-civ=1:gaul -autostart-civ=2:rome -autostart-player=-1 -unique-logs -nosound -mod=public -mod=vercingetorix`

## Canary

PASS

## Pairs

| seed | base | treatment | outcome | survival | total | JS errors (base→treat) |
|---|---|---|---|---|---|---|
| 141 | draw | draw | +0.00 | +0.00 | -0.36 | 0→0 |
| 142 | draw | draw | +0.00 | +0.00 | +0.09 | 0→0 |
| 143 | draw | draw | +0.00 | +0.00 | -0.58 | 0→0 |
| 144 | draw | draw | +0.00 | +0.00 | -0.06 | 0→0 |
| 145 | draw | draw | +0.00 | +0.00 | -0.61 | 0→0 |
| 146 | draw | draw | +0.00 | +0.00 | -0.02 | 0→0 |
| 147 | draw | draw | +0.00 | +0.00 | -0.17 | 0→0 |
| 148 | draw | draw | +0.00 | +0.00 | -0.50 | 0→0 |
| 149 | draw | draw | +0.00 | +0.00 | +0.39 | 0→0 |
| 150 | draw | draw | +0.00 | +0.00 | -0.73 | 0→0 |

## Metric deltas

| seed | metric | base | treatment | weighted delta |
|---|---|---|---|---|
| 141 | resourcesGathered | 4519 | 6034 | +0.134 |
| 141 | resourcesUsed | 4000 | 3500 | -0.050 |
| 141 | enemyUnitsKilled | 1450 | 0 | -0.400 |
| 141 | unitsTrained | 37 | 31 | -0.065 |
| 141 | populationPeak | 38 | 40 | +0.021 |
| 142 | resourcesGathered | 6768 | 7543 | +0.046 |
| 142 | resourcesUsed | 4100 | 4300 | +0.020 |
| 142 | enemyUnitsKilled | 1250 | 1300 | +0.016 |
| 142 | unitsTrained | 38 | 39 | +0.011 |
| 142 | populationPeak | 40 | 40 | +0.000 |
| 143 | resourcesGathered | 5585 | 5774 | +0.014 |
| 143 | resourcesUsed | 4000 | 3200 | -0.080 |
| 143 | enemyUnitsKilled | 850 | 0 | -0.400 |
| 143 | unitsTrained | 37 | 29 | -0.086 |
| 143 | populationPeak | 39 | 36 | -0.031 |
| 144 | resourcesGathered | 6828 | 7205 | +0.022 |
| 144 | resourcesUsed | 5000 | 5000 | +0.000 |
| 144 | enemyUnitsKilled | 1700 | 1350 | -0.082 |
| 144 | unitsTrained | 47 | 47 | +0.000 |
| 144 | populationPeak | 40 | 40 | +0.000 |
| 145 | resourcesGathered | 4773 | 4840 | +0.006 |
| 145 | resourcesUsed | 4100 | 4100 | +0.000 |
| 145 | enemyUnitsKilled | 1350 | 0 | -0.400 |
| 145 | unitsTrained | 38 | 26 | -0.126 |
| 145 | populationPeak | 39 | 30 | -0.092 |
| 146 | resourcesGathered | 7294 | 7086 | -0.011 |
| 146 | resourcesUsed | 4900 | 4700 | -0.016 |
| 146 | enemyUnitsKilled | 700 | 800 | +0.057 |
| 146 | unitsTrained | 45 | 39 | -0.053 |
| 146 | populationPeak | 40 | 40 | +0.000 |
| 147 | resourcesGathered | 5933 | 7717 | +0.120 |
| 147 | resourcesUsed | 5100 | 4600 | -0.039 |
| 147 | enemyUnitsKilled | 2250 | 1350 | -0.160 |
| 147 | unitsTrained | 48 | 37 | -0.092 |
| 147 | populationPeak | 40 | 40 | +0.000 |
| 148 | resourcesGathered | 6035 | 6842 | +0.053 |
| 148 | resourcesUsed | 5100 | 4400 | -0.055 |
| 148 | enemyUnitsKilled | 2050 | 0 | -0.400 |
| 148 | unitsTrained | 48 | 36 | -0.100 |
| 148 | populationPeak | 40 | 40 | +0.000 |
| 149 | resourcesGathered | 5802 | 6326 | +0.036 |
| 149 | resourcesUsed | 4300 | 4000 | -0.028 |
| 149 | enemyUnitsKilled | 0 | 100 | +0.400 |
| 149 | unitsTrained | 38 | 36 | -0.021 |
| 149 | populationPeak | 40 | 40 | +0.000 |
| 150 | resourcesGathered | 4993 | 4733 | -0.021 |
| 150 | resourcesUsed | 4900 | 4025 | -0.071 |
| 150 | enemyUnitsKilled | 50 | 0 | -0.400 |
| 150 | unitsTrained | 33 | 22 | -0.133 |
| 150 | populationPeak | 40 | 30 | -0.100 |

## Totals

-2.56 total = 0.00 outcome + -2.56 quality + 0.00 survival

## Verdict

neutral
