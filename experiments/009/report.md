# Report — baseline vs treatment

Settings: `-autostart=random/mainland -autostart-seed=<seed> -autostart-biome=generic/temperate -autostart-placement=circle -autostart-nonvisual -autostart-players=2 -autostart-size=128 -autostart-victory=conquest_civic_centers -autostart-ai=1:vercingetorix -autostart-ai=2:petra -autostart-aidiff=2:0 -autostart-civ=1:gaul -autostart-civ=2:rome -autostart-player=-1 -unique-logs -nosound -mod=public -mod=vercingetorix`

## Canary

PASS

## Pairs

| seed | base | treatment | outcome | survival | total | JS errors (base→treat) |
|---|---|---|---|---|---|---|
| 81 | draw | draw | +0.00 | +0.00 | -0.40 | 0→0 |
| 82 | draw | draw | +0.00 | +0.00 | -0.46 | 0→0 |
| 83 | draw | draw | +0.00 | +0.00 | -0.42 | 0→0 |
| 84 | draw | draw | +0.00 | +0.00 | -0.40 | 0→0 |
| 85 | draw | draw | +0.00 | +0.00 | -0.41 | 0→0 |
| 86 | draw | draw | +0.00 | +0.00 | -0.44 | 0→0 |
| 87 | draw | draw | +0.00 | +0.00 | -0.42 | 0→0 |
| 88 | draw | draw | +0.00 | +0.00 | -0.42 | 0→0 |
| 89 | draw | draw | +0.00 | +0.00 | -0.46 | 0→0 |
| 90 | draw | draw | +0.00 | +0.00 | -0.42 | 0→0 |

## Metric deltas

| seed | metric | base | treatment | weighted delta |
|---|---|---|---|---|
| 81 | resourcesGathered | 7927 | 7935 | +0.000 |
| 81 | resourcesUsed | 3900 | 3900 | +0.000 |
| 81 | enemyUnitsKilled | 700 | 0 | -0.400 |
| 81 | unitsTrained | 36 | 36 | +0.000 |
| 81 | populationPeak | 39 | 39 | +0.000 |
| 82 | resourcesGathered | 6775 | 6779 | +0.000 |
| 82 | resourcesUsed | 4000 | 3800 | -0.020 |
| 82 | enemyUnitsKilled | 1350 | 0 | -0.400 |
| 82 | unitsTrained | 37 | 35 | -0.022 |
| 82 | populationPeak | 40 | 38 | -0.020 |
| 83 | resourcesGathered | 7492 | 7515 | +0.001 |
| 83 | resourcesUsed | 4000 | 3900 | -0.010 |
| 83 | enemyUnitsKilled | 850 | 0 | -0.400 |
| 83 | unitsTrained | 37 | 36 | -0.011 |
| 83 | populationPeak | 40 | 40 | +0.000 |
| 84 | resourcesGathered | 8629 | 8683 | +0.003 |
| 84 | resourcesUsed | 5000 | 4800 | -0.016 |
| 84 | enemyUnitsKilled | 1700 | 150 | -0.365 |
| 84 | unitsTrained | 47 | 45 | -0.017 |
| 84 | populationPeak | 40 | 40 | +0.000 |
| 85 | resourcesGathered | 7722 | 7721 | -0.000 |
| 85 | resourcesUsed | 4800 | 4700 | -0.008 |
| 85 | enemyUnitsKilled | 1100 | 0 | -0.400 |
| 85 | unitsTrained | 45 | 44 | -0.009 |
| 85 | populationPeak | 39 | 40 | +0.010 |
| 86 | resourcesGathered | 8623 | 8618 | -0.000 |
| 86 | resourcesUsed | 4200 | 4000 | -0.019 |
| 86 | enemyUnitsKilled | 1400 | 0 | -0.400 |
| 86 | unitsTrained | 39 | 37 | -0.021 |
| 86 | populationPeak | 40 | 40 | +0.000 |
| 87 | resourcesGathered | 6737 | 6739 | +0.000 |
| 87 | resourcesUsed | 4000 | 3900 | -0.010 |
| 87 | enemyUnitsKilled | 1550 | 0 | -0.400 |
| 87 | unitsTrained | 37 | 36 | -0.011 |
| 87 | populationPeak | 40 | 40 | +0.000 |
| 88 | resourcesGathered | 6257 | 6705 | +0.029 |
| 88 | resourcesUsed | 5000 | 4700 | -0.024 |
| 88 | enemyUnitsKilled | 1850 | 0 | -0.400 |
| 88 | unitsTrained | 47 | 44 | -0.026 |
| 88 | populationPeak | 40 | 40 | +0.000 |
| 89 | resourcesGathered | 9043 | 9045 | +0.000 |
| 89 | resourcesUsed | 4300 | 4000 | -0.028 |
| 89 | enemyUnitsKilled | 1100 | 0 | -0.400 |
| 89 | unitsTrained | 40 | 37 | -0.030 |
| 89 | populationPeak | 40 | 40 | +0.000 |
| 90 | resourcesGathered | 7606 | 7597 | -0.000 |
| 90 | resourcesUsed | 4000 | 3900 | -0.010 |
| 90 | enemyUnitsKilled | 700 | 0 | -0.400 |
| 90 | unitsTrained | 37 | 36 | -0.011 |
| 90 | populationPeak | 40 | 40 | +0.000 |

## Totals

-4.24 total = 0.00 outcome + -4.24 quality + 0.00 survival

## Verdict

bad
