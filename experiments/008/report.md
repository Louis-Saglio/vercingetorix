# Report — baseline vs treatment

Settings: `-autostart=random/mainland -autostart-seed=<seed> -autostart-biome=generic/temperate -autostart-placement=circle -autostart-nonvisual -autostart-players=2 -autostart-size=128 -autostart-victory=conquest_civic_centers -autostart-ai=1:vercingetorix -autostart-ai=2:petra -autostart-aidiff=2:0 -autostart-civ=1:gaul -autostart-civ=2:rome -autostart-player=-1 -unique-logs -nosound -mod=public -mod=vercingetorix`

## Canary

PASS

## Pairs

| seed | base | treatment | outcome | survival | total | JS errors (base→treat) |
|---|---|---|---|---|---|---|
| 71 | draw | draw | +0.00 | +0.00 | +0.50 | 0→0 |
| 72 | draw | draw | +0.00 | +0.00 | +0.11 | 0→0 |
| 73 | draw | draw | +0.00 | +0.00 | +0.09 | 0→0 |
| 74 | draw | draw | +0.00 | +0.00 | +0.23 | 0→0 |
| 75 | draw | draw | +0.00 | +0.00 | +0.53 | 0→0 |
| 76 | draw | draw | +0.00 | +0.00 | +0.04 | 0→0 |
| 77 | draw | draw | +0.00 | +0.00 | +0.39 | 0→0 |
| 78 | draw | draw | +0.00 | +0.00 | +0.37 | 0→0 |
| 79 | draw | draw | +0.00 | +0.00 | -0.12 | 0→0 |
| 80 | draw | draw | +0.00 | +0.00 | +0.09 | 0→0 |

## Metric deltas

| seed | metric | base | treatment | weighted delta |
|---|---|---|---|---|
| 71 | resourcesGathered | 5914 | 7259 | +0.091 |
| 71 | resourcesUsed | 4925 | 4900 | -0.002 |
| 71 | enemyUnitsKilled | 950 | 1550 | +0.253 |
| 71 | unitsTrained | 47 | 46 | -0.009 |
| 71 | populationPeak | 28 | 40 | +0.171 |
| 72 | resourcesGathered | 5779 | 7252 | +0.102 |
| 72 | resourcesUsed | 3925 | 3900 | -0.003 |
| 72 | enemyUnitsKilled | 1250 | 950 | -0.096 |
| 72 | unitsTrained | 37 | 36 | -0.011 |
| 72 | populationPeak | 30 | 39 | +0.120 |
| 73 | resourcesGathered | 5865 | 8065 | +0.150 |
| 73 | resourcesUsed | 4125 | 4100 | -0.002 |
| 73 | enemyUnitsKilled | 1650 | 900 | -0.182 |
| 73 | unitsTrained | 39 | 38 | -0.010 |
| 73 | populationPeak | 30 | 40 | +0.133 |
| 74 | resourcesGathered | 5820 | 6506 | +0.047 |
| 74 | resourcesUsed | 4725 | 4500 | -0.019 |
| 74 | enemyUnitsKilled | 2650 | 3400 | +0.113 |
| 74 | unitsTrained | 45 | 42 | -0.027 |
| 74 | populationPeak | 31 | 40 | +0.116 |
| 75 | resourcesGathered | 4003 | 7213 | +0.321 |
| 75 | resourcesUsed | 4425 | 6700 | +0.206 |
| 75 | enemyUnitsKilled | 2050 | 1100 | -0.185 |
| 75 | unitsTrained | 42 | 51 | +0.086 |
| 75 | populationPeak | 32 | 40 | +0.100 |
| 76 | resourcesGathered | 6234 | 7962 | +0.111 |
| 76 | resourcesUsed | 4025 | 3900 | -0.012 |
| 76 | enemyUnitsKilled | 1450 | 750 | -0.193 |
| 76 | unitsTrained | 38 | 36 | -0.021 |
| 76 | populationPeak | 29 | 40 | +0.152 |
| 77 | resourcesGathered | 6795 | 9296 | +0.147 |
| 77 | resourcesUsed | 5625 | 6800 | +0.084 |
| 77 | enemyUnitsKilled | 1050 | 1050 | +0.000 |
| 77 | unitsTrained | 54 | 57 | +0.022 |
| 77 | populationPeak | 30 | 40 | +0.133 |
| 78 | resourcesGathered | 6183 | 8133 | +0.126 |
| 78 | resourcesUsed | 4025 | 4100 | +0.007 |
| 78 | enemyUnitsKilled | 950 | 1150 | +0.084 |
| 78 | unitsTrained | 38 | 38 | +0.000 |
| 78 | populationPeak | 28 | 39 | +0.157 |
| 79 | resourcesGathered | 5293 | 6237 | +0.071 |
| 79 | resourcesUsed | 4425 | 4000 | -0.038 |
| 79 | enemyUnitsKilled | 3700 | 1250 | -0.265 |
| 79 | unitsTrained | 42 | 37 | -0.048 |
| 79 | populationPeak | 28 | 39 | +0.157 |
| 80 | resourcesGathered | 6528 | 8717 | +0.134 |
| 80 | resourcesUsed | 5050 | 4900 | -0.012 |
| 80 | enemyUnitsKilled | 2050 | 1000 | -0.205 |
| 80 | unitsTrained | 48 | 46 | -0.017 |
| 80 | populationPeak | 27 | 40 | +0.193 |

## Totals

2.23 total = 0.00 outcome + 2.23 quality + 0.00 survival

## Verdict

neutral
