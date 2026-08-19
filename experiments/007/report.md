# Report — baseline vs treatment

Settings: `-autostart=random/mainland -autostart-seed=<seed> -autostart-biome=generic/temperate -autostart-placement=circle -autostart-nonvisual -autostart-players=2 -autostart-size=128 -autostart-victory=conquest_civic_centers -autostart-ai=1:vercingetorix -autostart-ai=2:petra -autostart-aidiff=2:0 -autostart-civ=1:gaul -autostart-civ=2:rome -autostart-player=-1 -unique-logs -nosound -mod=public -mod=vercingetorix`

## Canary

PASS

## Pairs

| seed | base | treatment | outcome | survival | total | JS errors (base→treat) |
|---|---|---|---|---|---|---|
| 51 | draw | draw | +0.00 | +0.00 | +0.80 | 0→0 |
| 52 | draw | draw | +0.00 | +0.00 | +0.22 | 0→0 |
| 53 | draw | draw | +0.00 | +0.00 | -0.38 | 0→0 |
| 54 | draw | draw | +0.00 | +0.00 | +0.07 | 0→0 |
| 55 | draw | draw | +0.00 | +0.00 | -0.00 | 0→0 |
| 56 | draw | draw | +0.00 | +0.00 | -0.03 | 0→0 |
| 57 | draw | draw | +0.00 | +0.00 | +0.18 | 0→0 |
| 58 | draw | draw | +0.00 | +0.00 | +0.04 | 0→0 |
| 59 | draw | draw | +0.00 | +0.00 | -0.04 | 0→0 |
| 60 | draw | draw | +0.00 | +0.00 | +0.65 | 0→0 |
| 61 | draw | draw | +0.00 | +0.00 | +0.18 | 0→0 |
| 62 | draw | draw | +0.00 | +0.00 | +0.17 | 0→0 |
| 63 | draw | draw | +0.00 | +0.00 | +0.07 | 0→0 |
| 64 | draw | draw | +0.00 | +0.00 | +0.22 | 0→0 |
| 65 | draw | draw | +0.00 | +0.00 | +0.06 | 0→0 |
| 66 | draw | draw | +0.00 | +0.00 | +0.05 | 0→0 |
| 67 | draw | draw | +0.00 | +0.00 | +0.23 | 0→0 |
| 68 | draw | draw | +0.00 | +0.00 | +0.13 | 0→0 |
| 69 | draw | draw | +0.00 | +0.00 | +0.48 | 0→0 |
| 70 | draw | draw | +0.00 | +0.00 | +0.70 | 0→0 |

## Metric deltas

| seed | metric | base | treatment | weighted delta |
|---|---|---|---|---|
| 51 | resourcesGathered | 6582 | 7662 | +0.066 |
| 51 | resourcesUsed | 3950 | 5225 | +0.129 |
| 51 | enemyUnitsKilled | 900 | 2600 | +0.400 |
| 51 | unitsTrained | 38 | 50 | +0.126 |
| 51 | populationPeak | 29 | 35 | +0.083 |
| 52 | resourcesGathered | 5084 | 6023 | +0.074 |
| 52 | resourcesUsed | 4825 | 5625 | +0.066 |
| 52 | enemyUnitsKilled | 1750 | 1550 | -0.046 |
| 52 | unitsTrained | 46 | 54 | +0.070 |
| 52 | populationPeak | 31 | 35 | +0.052 |
| 53 | resourcesGathered | 6429 | 7643 | +0.076 |
| 53 | resourcesUsed | 4650 | 4325 | -0.028 |
| 53 | enemyUnitsKilled | 2150 | 600 | -0.288 |
| 53 | unitsTrained | 45 | 28 | -0.151 |
| 53 | populationPeak | 30 | 31 | +0.013 |
| 54 | resourcesGathered | 5785 | 7314 | +0.106 |
| 54 | resourcesUsed | 3925 | 3825 | -0.010 |
| 54 | enemyUnitsKilled | 850 | 650 | -0.094 |
| 54 | unitsTrained | 37 | 36 | -0.011 |
| 54 | populationPeak | 29 | 35 | +0.083 |
| 55 | resourcesGathered | 6619 | 7379 | +0.046 |
| 55 | resourcesUsed | 4025 | 3925 | -0.010 |
| 55 | enemyUnitsKilled | 1450 | 1100 | -0.097 |
| 55 | unitsTrained | 38 | 37 | -0.011 |
| 55 | populationPeak | 30 | 35 | +0.067 |
| 56 | resourcesGathered | 5466 | 5410 | -0.004 |
| 56 | resourcesUsed | 5025 | 4925 | -0.008 |
| 56 | enemyUnitsKilled | 2150 | 1800 | -0.065 |
| 56 | unitsTrained | 48 | 47 | -0.008 |
| 56 | populationPeak | 31 | 35 | +0.052 |
| 57 | resourcesGathered | 6749 | 8002 | +0.074 |
| 57 | resourcesUsed | 4025 | 3925 | -0.010 |
| 57 | enemyUnitsKilled | 700 | 750 | +0.029 |
| 57 | unitsTrained | 38 | 37 | -0.011 |
| 57 | populationPeak | 28 | 35 | +0.100 |
| 58 | resourcesGathered | 4975 | 6784 | +0.145 |
| 58 | resourcesUsed | 4125 | 3925 | -0.019 |
| 58 | enemyUnitsKilled | 1500 | 950 | -0.147 |
| 58 | unitsTrained | 39 | 37 | -0.021 |
| 58 | populationPeak | 29 | 35 | +0.083 |
| 59 | resourcesGathered | 5826 | 5950 | +0.009 |
| 59 | resourcesUsed | 4125 | 4000 | -0.012 |
| 59 | enemyUnitsKilled | 1400 | 1100 | -0.086 |
| 59 | unitsTrained | 39 | 37 | -0.021 |
| 59 | populationPeak | 29 | 34 | +0.069 |
| 60 | resourcesGathered | 5272 | 6321 | +0.080 |
| 60 | resourcesUsed | 3925 | 5025 | +0.112 |
| 60 | enemyUnitsKilled | 1250 | 2100 | +0.272 |
| 60 | unitsTrained | 37 | 48 | +0.119 |
| 60 | populationPeak | 30 | 35 | +0.067 |
| 61 | resourcesGathered | 5002 | 6371 | +0.109 |
| 61 | resourcesUsed | 3925 | 4000 | +0.008 |
| 61 | enemyUnitsKilled | 1100 | 1050 | -0.018 |
| 61 | unitsTrained | 37 | 37 | +0.000 |
| 61 | populationPeak | 29 | 35 | +0.083 |
| 62 | resourcesGathered | 5704 | 6520 | +0.057 |
| 62 | resourcesUsed | 6125 | 6125 | +0.000 |
| 62 | enemyUnitsKilled | 2700 | 3100 | +0.059 |
| 62 | unitsTrained | 59 | 59 | +0.000 |
| 62 | populationPeak | 31 | 35 | +0.052 |
| 63 | resourcesGathered | 6915 | 8159 | +0.072 |
| 63 | resourcesUsed | 5125 | 5000 | -0.010 |
| 63 | enemyUnitsKilled | 1550 | 1350 | -0.052 |
| 63 | unitsTrained | 49 | 47 | -0.016 |
| 63 | populationPeak | 30 | 36 | +0.080 |
| 64 | resourcesGathered | 5841 | 6208 | +0.025 |
| 64 | resourcesUsed | 5925 | 6600 | +0.046 |
| 64 | enemyUnitsKilled | 1100 | 1200 | +0.036 |
| 64 | unitsTrained | 54 | 60 | +0.044 |
| 64 | populationPeak | 31 | 36 | +0.065 |
| 65 | resourcesGathered | 6311 | 7700 | +0.088 |
| 65 | resourcesUsed | 4825 | 4900 | +0.006 |
| 65 | enemyUnitsKilled | 1200 | 800 | -0.133 |
| 65 | unitsTrained | 46 | 46 | +0.000 |
| 65 | populationPeak | 29 | 36 | +0.097 |
| 66 | resourcesGathered | 5984 | 6048 | +0.004 |
| 66 | resourcesUsed | 4225 | 4025 | -0.019 |
| 66 | enemyUnitsKilled | 1250 | 1250 | +0.000 |
| 66 | unitsTrained | 40 | 38 | -0.020 |
| 66 | populationPeak | 29 | 35 | +0.083 |
| 67 | resourcesGathered | 5005 | 6203 | +0.096 |
| 67 | resourcesUsed | 4825 | 5700 | +0.073 |
| 67 | enemyUnitsKilled | 1750 | 1300 | -0.103 |
| 67 | unitsTrained | 46 | 54 | +0.070 |
| 67 | populationPeak | 31 | 38 | +0.090 |
| 68 | resourcesGathered | 6211 | 7455 | +0.080 |
| 68 | resourcesUsed | 5225 | 5300 | +0.006 |
| 68 | enemyUnitsKilled | 2550 | 2200 | -0.055 |
| 68 | unitsTrained | 50 | 50 | +0.000 |
| 68 | populationPeak | 29 | 36 | +0.097 |
| 69 | resourcesGathered | 6086 | 6483 | +0.026 |
| 69 | resourcesUsed | 4125 | 4500 | +0.036 |
| 69 | enemyUnitsKilled | 1250 | 2200 | +0.304 |
| 69 | unitsTrained | 39 | 42 | +0.031 |
| 69 | populationPeak | 30 | 36 | +0.080 |
| 70 | resourcesGathered | 5016 | 6239 | +0.098 |
| 70 | resourcesUsed | 3925 | 4400 | +0.048 |
| 70 | enemyUnitsKilled | 1100 | 3750 | +0.400 |
| 70 | unitsTrained | 37 | 41 | +0.043 |
| 70 | populationPeak | 28 | 36 | +0.114 |

## Totals

3.79 total = 0.00 outcome + 3.79 quality + 0.00 survival

## Verdict

neutral
