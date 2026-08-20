# Report — baseline vs treatment

Settings: `-autostart=random/mainland -autostart-seed=<seed> -autostart-biome=generic/temperate -autostart-placement=circle -autostart-nonvisual -autostart-players=2 -autostart-size=192 -autostart-victory=conquest_civic_centers -autostart-ai=1:vercingetorix -autostart-ai=2:petra -autostart-aidiff=2:0 -autostart-civ=1:gaul -autostart-civ=2:rome -autostart-player=-1 -unique-logs -nosound -mod=public -mod=vercingetorix`

## Canary

PASS

## Pairs

| seed | base | treatment | outcome | survival | total | JS errors (base→treat) |
|---|---|---|---|---|---|---|
| 61 | draw | draw | +0.00 | +0.00 | +0.11 | 0→0 |
| 62 | draw | draw | +0.00 | +0.00 | +0.06 | 0→0 |
| 63 | draw | draw | +0.00 | +0.00 | -0.04 | 0→0 |
| 64 | draw | draw | +0.00 | +0.00 | +0.10 | 0→0 |
| 65 | draw | draw | +0.00 | +0.00 | +0.02 | 0→0 |
| 66 | draw | draw | +0.00 | +0.00 | +0.37 | 0→0 |
| 67 | draw | draw | +0.00 | +0.00 | -0.01 | 0→0 |
| 68 | draw | draw | +0.00 | +0.00 | -0.45 | 0→0 |
| 69 | draw | draw | +0.00 | +0.00 | +0.08 | 0→0 |
| 70 | draw | draw | +0.00 | +0.00 | +0.00 | 0→0 |

## Metric deltas

| seed | metric | base | treatment | weighted delta |
|---|---|---|---|---|
| 61 | resourcesGathered | 9689 | 10791 | +0.045 |
| 61 | resourcesUsed | 6525 | 6850 | +0.020 |
| 61 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 61 | unitsTrained | 96 | 101 | +0.021 |
| 61 | populationPeak | 105 | 110 | +0.019 |
| 62 | resourcesGathered | 12993 | 12871 | -0.004 |
| 62 | resourcesUsed | 6525 | 6850 | +0.020 |
| 62 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 62 | unitsTrained | 96 | 101 | +0.021 |
| 62 | populationPeak | 105 | 110 | +0.019 |
| 63 | resourcesGathered | 8473 | 7797 | -0.032 |
| 63 | resourcesUsed | 6575 | 6675 | +0.006 |
| 63 | enemyUnitsKilled | 150 | 150 | +0.000 |
| 63 | unitsTrained | 97 | 99 | +0.008 |
| 63 | populationPeak | 105 | 100 | -0.019 |
| 64 | resourcesGathered | 9874 | 10832 | +0.039 |
| 64 | resourcesUsed | 6525 | 6850 | +0.020 |
| 64 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 64 | unitsTrained | 96 | 101 | +0.021 |
| 64 | populationPeak | 105 | 110 | +0.019 |
| 65 | resourcesGathered | 12528 | 13049 | +0.017 |
| 65 | resourcesUsed | 6525 | 6525 | +0.000 |
| 65 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 65 | unitsTrained | 96 | 96 | +0.000 |
| 65 | populationPeak | 105 | 105 | +0.000 |
| 66 | resourcesGathered | 10675 | 9341 | -0.050 |
| 66 | resourcesUsed | 7575 | 7725 | +0.008 |
| 66 | enemyUnitsKilled | 0 | 100 | +0.400 |
| 66 | unitsTrained | 107 | 111 | +0.015 |
| 66 | populationPeak | 105 | 105 | +0.000 |
| 67 | resourcesGathered | 13135 | 12870 | -0.008 |
| 67 | resourcesUsed | 6525 | 6525 | +0.000 |
| 67 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 67 | unitsTrained | 96 | 96 | +0.000 |
| 67 | populationPeak | 105 | 105 | +0.000 |
| 68 | resourcesGathered | 12511 | 13101 | +0.019 |
| 68 | resourcesUsed | 7425 | 6925 | -0.027 |
| 68 | enemyUnitsKilled | 100 | 0 | -0.400 |
| 68 | unitsTrained | 106 | 96 | -0.038 |
| 68 | populationPeak | 105 | 105 | +0.000 |
| 69 | resourcesGathered | 9262 | 9646 | +0.017 |
| 69 | resourcesUsed | 6525 | 6850 | +0.020 |
| 69 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 69 | unitsTrained | 96 | 101 | +0.021 |
| 69 | populationPeak | 105 | 110 | +0.019 |
| 70 | resourcesGathered | 8959 | 9008 | +0.002 |
| 70 | resourcesUsed | 6525 | 6525 | +0.000 |
| 70 | enemyUnitsKilled | 0 | 0 | +0.000 |
| 70 | unitsTrained | 96 | 96 | +0.000 |
| 70 | populationPeak | 105 | 105 | +0.000 |

## Totals

0.24 total = 0.00 outcome + 0.24 quality + 0.00 survival

## Verdict

neutral
