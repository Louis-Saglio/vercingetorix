# Report — baseline vs treatment

Settings: `-autostart=random/mainland -autostart-seed=<seed> -autostart-biome=generic/temperate -autostart-placement=circle -autostart-nonvisual -autostart-players=2 -autostart-size=128 -autostart-victory=conquest_civic_centers -autostart-ai=1:vercingetorix -autostart-ai=2:petra -autostart-aidiff=2:0 -autostart-civ=1:gaul -autostart-civ=2:rome -autostart-player=-1 -unique-logs -nosound -mod=public -mod=vercingetorix`

## Canary

PASS

## Pairs

| seed | base | treatment | outcome | survival | total | JS errors (base→treat) |
|---|---|---|---|---|---|---|
| 121 | draw | draw | +0.00 | +0.00 | +0.00 | 0→0 |
| 122 | draw | draw | +0.00 | +0.00 | +0.33 | 0→0 |
| 123 | draw | draw | +0.00 | +0.00 | +0.10 | 0→0 |
| 124 | draw | draw | +0.00 | +0.00 | +0.28 | 0→0 |
| 125 | draw | draw | +0.00 | +0.00 | -0.07 | 0→0 |
| 126 | draw | draw | +0.00 | +0.00 | +0.03 | 0→0 |
| 127 | draw | draw | +0.00 | +0.00 | -0.09 | 0→0 |
| 128 | draw | draw | +0.00 | +0.00 | -0.30 | 0→0 |
| 129 | draw | draw | +0.00 | +0.00 | +0.40 | 0→0 |
| 130 | draw | draw | +0.00 | +0.00 | -0.11 | 0→0 |

## Metric deltas

| seed | metric | base | treatment | weighted delta |
|---|---|---|---|---|
| 121 | resourcesGathered | 3725 | 3725 | +0.000 |
| 121 | resourcesUsed | 4025 | 4025 | +0.000 |
| 121 | enemyUnitsKilled | 500 | 500 | +0.000 |
| 121 | unitsTrained | 24 | 24 | +0.000 |
| 121 | populationPeak | 25 | 25 | +0.000 |
| 122 | resourcesGathered | 5556 | 7518 | +0.141 |
| 122 | resourcesUsed | 5100 | 5350 | +0.020 |
| 122 | enemyUnitsKilled | 1750 | 2100 | +0.080 |
| 122 | unitsTrained | 48 | 49 | +0.008 |
| 122 | populationPeak | 40 | 48 | +0.080 |
| 123 | resourcesGathered | 5525 | 6588 | +0.077 |
| 123 | resourcesUsed | 4100 | 5350 | +0.122 |
| 123 | enemyUnitsKilled | 1150 | 350 | -0.278 |
| 123 | unitsTrained | 38 | 46 | +0.084 |
| 123 | populationPeak | 40 | 50 | +0.100 |
| 124 | resourcesGathered | 6734 | 7540 | +0.048 |
| 124 | resourcesUsed | 4000 | 5750 | +0.175 |
| 124 | enemyUnitsKilled | 950 | 550 | -0.168 |
| 124 | unitsTrained | 37 | 50 | +0.141 |
| 124 | populationPeak | 40 | 49 | +0.090 |
| 125 | resourcesGathered | 5144 | 6396 | +0.097 |
| 125 | resourcesUsed | 4400 | 5150 | +0.068 |
| 125 | enemyUnitsKilled | 2650 | 250 | -0.362 |
| 125 | unitsTrained | 40 | 44 | +0.040 |
| 125 | populationPeak | 40 | 49 | +0.090 |
| 126 | resourcesGathered | 5485 | 5964 | +0.035 |
| 126 | resourcesUsed | 4300 | 4450 | +0.014 |
| 126 | enemyUnitsKilled | 1200 | 900 | -0.100 |
| 126 | unitsTrained | 40 | 40 | +0.000 |
| 126 | populationPeak | 39 | 47 | +0.082 |
| 127 | resourcesGathered | 6690 | 7505 | +0.049 |
| 127 | resourcesUsed | 5000 | 5050 | +0.004 |
| 127 | enemyUnitsKilled | 1500 | 750 | -0.200 |
| 127 | unitsTrained | 47 | 46 | -0.009 |
| 127 | populationPeak | 40 | 47 | +0.070 |
| 128 | resourcesGathered | 4997 | 5092 | +0.008 |
| 128 | resourcesUsed | 5100 | 4950 | -0.012 |
| 128 | enemyUnitsKilled | 750 | 0 | -0.400 |
| 128 | unitsTrained | 38 | 41 | +0.032 |
| 128 | populationPeak | 39 | 46 | +0.072 |
| 129 | resourcesGathered | 5826 | 7153 | +0.091 |
| 129 | resourcesUsed | 5400 | 6550 | +0.085 |
| 129 | enemyUnitsKilled | 1750 | 2150 | +0.091 |
| 129 | unitsTrained | 50 | 54 | +0.032 |
| 129 | populationPeak | 40 | 50 | +0.100 |
| 130 | resourcesGathered | 5581 | 6539 | +0.069 |
| 130 | resourcesUsed | 4200 | 4650 | +0.043 |
| 130 | enemyUnitsKilled | 1400 | 250 | -0.329 |
| 130 | unitsTrained | 39 | 42 | +0.031 |
| 130 | populationPeak | 40 | 48 | +0.080 |

## Totals

0.59 total = 0.00 outcome + 0.59 quality + 0.00 survival

## Verdict

neutral
