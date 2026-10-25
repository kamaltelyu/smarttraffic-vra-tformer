# SmartTraffic IJIES — FINAL Resume Result Digest

## Reproducibility / cache audit
| Asset                   |   Count | Path                                                                        |
|:------------------------|--------:|:----------------------------------------------------------------------------|
| Clean sequence parquet  |      32 | /content/drive/MyDrive/SmartTraffic_VRA_TFormer_IJIES/cache/aicity_clean    |
| Degraded parquet        |      31 | /content/drive/MyDrive/SmartTraffic_VRA_TFormer_IJIES/cache/aicity_degraded |
| Model checkpoints (.pt) |       8 | /content/drive/MyDrive/SmartTraffic_VRA_TFormer_IJIES/models                |
| Existing tables/files   |       9 | /content/drive/MyDrive/SmartTraffic_VRA_TFormer_IJIES/tables                |
| Existing figures        |      12 | /content/drive/MyDrive/SmartTraffic_VRA_TFormer_IJIES/figures               |
| Existing logs           |       9 | /content/drive/MyDrive/SmartTraffic_VRA_TFormer_IJIES/logs                  |

## Forecast split
| split   |   windows |
|:--------|----------:|
| train   |       798 |
| val     |       294 |
| test    |       294 |

## Mean clean forecasting results
| Model                         |     MAE |    RMSE |   WAPE_pct |       R2 |
|:------------------------------|--------:|--------:|-----------:|---------:|
| Transformer+ReliabilityConcat | 11.0902 | 14.6127 |    22.095  | 0.813123 |
| Transformer                   | 11.1905 | 14.665  |    22.2963 | 0.813235 |
| VRA-TFormer                   | 11.2283 | 14.8414 |    22.3728 | 0.808851 |
| PatchTST                      | 11.8849 | 15.6854 |    23.6798 | 0.786665 |
| LSTM                          | 13.1008 | 19.2018 |    26.1031 | 0.680584 |
| GRU                           | 13.6429 | 18.0155 |    27.1856 | 0.717408 |
| iTransformer                  | 14.2562 | 18.8955 |    28.4037 | 0.691112 |
| Persistence                   | 15.324  | 20.3989 |    30.5325 | 0.637271 |

## Clean statistical comparison
| Horizon   | Baseline                      |   Baseline_MAE |   VRA_MAE |   Improvement_% |   VRA_win_rate_% |   Wilcoxon_stat |     p_raw |   p_holm | significant_0.05   |
|:----------|:------------------------------|---------------:|----------:|----------------:|-----------------:|----------------:|----------:|---------:|:-------------------|
| 30s       | Transformer+ReliabilityConcat |        11.9038 |   11.5176 |         3.24433 |          53.7415 |           19388 | 0.0578919 | 0.231567 | False              |
| 60s       | Transformer+ReliabilityConcat |        10.935  |   10.4534 |         4.40437 |          55.4422 |           19723 | 0.0896197 | 0.268859 | False              |
| 90s       | Transformer+ReliabilityConcat |        11.2967 |   10.9623 |         2.95994 |          52.0408 |           20116 | 0.141473  | 0.282945 | False              |
| 120s      | Transformer+ReliabilityConcat |        10.2252 |   11.9798 |       -17.1597  |          42.8571 |           28373 | 0.999998  | 0.999998 | False              |

## Ablation
| Model                |     MAE |    RMSE |   WAPE_% |       R2 |
|:---------------------|--------:|--------:|---------:|---------:|
| A0_Transformer       | 11.1905 | 14.665  |  22.2963 | 0.813235 |
| A1_ReliabilityConcat | 11.0902 | 14.6127 |  22.095  | 0.813123 |
| A2_ReliabilityGate   | 12.4577 | 16.2173 |  24.8172 | 0.772258 |
| A3_VRA-TFormer       | 11.2283 | 14.8414 |  22.3728 | 0.808851 |

## Robustness configuration
- Robustness history: **24 steps (120 s)**
- Robustness sequences: **cam_1, cam_2_rain**
- Number of degradation scenarios: **8**

## Robustness summary
| Model                         | Condition   |   Severity |   Clean_MAE |   Degraded_MAE |   Relative_Degradation_% |   N_windows |   N_sequences |   Robust_Lookback_steps |   Robust_Lookback_sec |
|:------------------------------|:------------|-----------:|------------:|---------------:|-------------------------:|------------:|--------------:|------------------------:|----------------------:|
| Transformer                   | blur        |          1 |     15.4764 |        14.8636 |                -3.95974  |          26 |             2 |                      24 |                   120 |
| Transformer+ReliabilityConcat | blur        |          1 |     16.7561 |        27.6592 |                65.0692   |          26 |             2 |                      24 |                   120 |
| VRA-TFormer                   | blur        |          1 |     15.6581 |        15.6894 |                 0.199985 |          26 |             2 |                      24 |                   120 |
| Transformer                   | blur        |          3 |     15.4764 |        23.7397 |                53.3928   |          26 |             2 |                      24 |                   120 |
| Transformer+ReliabilityConcat | blur        |          3 |     16.7561 |        34.1495 |               103.803    |          26 |             2 |                      24 |                   120 |
| VRA-TFormer                   | blur        |          3 |     15.6581 |        28.93   |                84.7606   |          26 |             2 |                      24 |                   120 |
| Transformer                   | frame_drop  |          1 |     15.4764 |        16.6853 |                 7.81092  |          26 |             2 |                      24 |                   120 |
| Transformer+ReliabilityConcat | frame_drop  |          1 |     16.7561 |        43.7568 |               161.139    |          26 |             2 |                      24 |                   120 |
| VRA-TFormer                   | frame_drop  |          1 |     15.6581 |        25.6579 |                63.8636   |          26 |             2 |                      24 |                   120 |
| Transformer                   | frame_drop  |          3 |     15.4764 |        15.3181 |                -1.02298  |          26 |             2 |                      24 |                   120 |
| Transformer+ReliabilityConcat | frame_drop  |          3 |     16.7561 |        44.6252 |               166.322    |          26 |             2 |                      24 |                   120 |
| VRA-TFormer                   | frame_drop  |          3 |     15.6581 |        18.6831 |                19.3188   |          26 |             2 |                      24 |                   120 |
| Transformer                   | lowlight    |          1 |     15.4764 |        14.948  |                -3.41419  |          26 |             2 |                      24 |                   120 |
| Transformer+ReliabilityConcat | lowlight    |          1 |     16.7561 |        14.152  |               -15.5417   |          26 |             2 |                      24 |                   120 |
| VRA-TFormer                   | lowlight    |          1 |     15.6581 |        15.3605 |                -1.90063  |          26 |             2 |                      24 |                   120 |
| Transformer                   | lowlight    |          3 |     15.4764 |        15.1029 |                -2.41372  |          26 |             2 |                      24 |                   120 |
| Transformer+ReliabilityConcat | lowlight    |          3 |     16.7561 |        23.0324 |                37.4565   |          26 |             2 |                      24 |                   120 |
| VRA-TFormer                   | lowlight    |          3 |     15.6581 |        16.882  |                 7.81668  |          26 |             2 |                      24 |                   120 |
| Transformer                   | occlusion   |          1 |     15.4764 |        15.8795 |                 2.60444  |          26 |             2 |                      24 |                   120 |
| Transformer+ReliabilityConcat | occlusion   |          1 |     16.7561 |        16.2265 |                -3.16076  |          26 |             2 |                      24 |                   120 |
| VRA-TFormer                   | occlusion   |          1 |     15.6581 |        15.7877 |                 0.82766  |          26 |             2 |                      24 |                   120 |
| Transformer                   | occlusion   |          3 |     15.4764 |        17.8503 |                15.3385   |          26 |             2 |                      24 |                   120 |
| Transformer+ReliabilityConcat | occlusion   |          3 |     16.7561 |        15.1674 |                -9.48148  |          26 |             2 |                      24 |                   120 |
| VRA-TFormer                   | occlusion   |          3 |     15.6581 |        18.2581 |                16.6051   |          26 |             2 |                      24 |                   120 |

## Average relative degradation
| Model                         |   Relative_Degradation_% |
|:------------------------------|-------------------------:|
| Transformer                   |                   8.542  |
| VRA-TFormer                   |                  23.9365 |
| Transformer+ReliabilityConcat |                  63.2007 |

## Robustness significance
| Condition   |   Severity | Comparator                    |   N_windows |   Comparator_MAE |   VRA_MAE |   VRA_Improvement_% |   VRA_win_rate_% |   Wilcoxon_stat |       p_raw |      p_holm | significant_0.05   |
|:------------|-----------:|:------------------------------|------------:|-----------------:|----------:|--------------------:|-----------------:|----------------:|------------:|------------:|:-------------------|
| blur        |          1 | Transformer                   |          26 |          14.8636 |   15.6894 |           -5.55604  |          19.2308 |             277 | 0.996031    | 1           | False              |
| blur        |          1 | Transformer+ReliabilityConcat |          26 |          27.6592 |   15.6894 |           43.276    |         100      |               0 | 1.49012e-08 | 2.38419e-07 | True               |
| blur        |          3 | Transformer                   |          26 |          23.7397 |   28.93   |          -21.8633   |           0      |             351 | 1           | 1           | False              |
| blur        |          3 | Transformer+ReliabilityConcat |          26 |          34.1495 |   28.93   |           15.2844   |          65.3846 |              53 | 0.000582561 | 0.00757329  | True               |
| frame_drop  |          1 | Transformer                   |          26 |          16.6853 |   25.6579 |          -53.776    |           0      |             351 | 1           | 1           | False              |
| frame_drop  |          1 | Transformer+ReliabilityConcat |          26 |          43.7568 |   25.6579 |           41.3624   |          57.6923 |              88 | 0.0126754   | 0.152104    | False              |
| frame_drop  |          3 | Transformer                   |          26 |          15.3181 |   18.6831 |          -21.9673   |           0      |             351 | 1           | 1           | False              |
| frame_drop  |          3 | Transformer+ReliabilityConcat |          26 |          44.6252 |   18.6831 |           58.1334   |         100      |               0 | 1.49012e-08 | 2.38419e-07 | True               |
| lowlight    |          1 | Transformer                   |          26 |          14.948  |   15.3605 |           -2.75937  |          42.3077 |             233 | 0.928642    | 1           | False              |
| lowlight    |          1 | Transformer+ReliabilityConcat |          26 |          14.152  |   15.3605 |           -8.53974  |          34.6154 |             237 | 0.941759    | 1           | False              |
| lowlight    |          3 | Transformer                   |          26 |          15.1029 |   16.882  |          -11.7804   |          19.2308 |             293 | 0.99911     | 1           | False              |
| lowlight    |          3 | Transformer+ReliabilityConcat |          26 |          23.0324 |   16.882  |           26.7031   |          69.2308 |              40 | 0.000124007 | 0.0017361   | True               |
| occlusion   |          1 | Transformer                   |          26 |          15.8795 |   15.7877 |            0.578079 |          50      |             162 | 0.372696    | 1           | False              |
| occlusion   |          1 | Transformer+ReliabilityConcat |          26 |          16.2265 |   15.7877 |            2.70434  |          61.5385 |             164 | 0.391767    | 1           | False              |
| occlusion   |          3 | Transformer                   |          26 |          17.8503 |   18.2581 |           -2.28502  |          26.9231 |             261 | 0.986402    | 1           | False              |
| occlusion   |          3 | Transformer+ReliabilityConcat |          26 |          15.1674 |   18.2581 |          -20.3775   |          34.6154 |             271 | 0.993524    | 1           | False              |

## Efficiency
|   Params |   Latency_ms_per_batch |   Latency_ms_per_sample | Model                         |
|---------:|-----------------------:|------------------------:|:------------------------------|
|    51716 |               0.665447 |              0.0113171  | LSTM                          |
|    38852 |               0.586341 |              0.00997178 | GRU                           |
|   100740 |               1.53114  |              0.0260399  | Transformer                   |
|   102660 |               1.9897   |              0.0338385  | PatchTST                      |
|   105476 |               1.45328  |              0.0247157  | iTransformer                  |
|   101124 |               1.54934  |              0.0263492  | Transformer+ReliabilityConcat |
|   114630 |               4.00234  |              0.068067   | VRA-TFormer                   |

## Factual manuscript notes
- Best mean clean-MAE model: **Transformer+ReliabilityConcat** (MAE=11.0902).
- VRA-TFormer mean clean MAE: **11.2283**.
- VRA-TFormer mean clean WAPE: **22.37%**.
- Lowest mean relative degradation: **Transformer** (8.54%).
- Lowest average degraded-MAE model: **Transformer**.
- Learned attention reliability strength lambda: **0.6922**.

## Suggested empirical framing
Do not claim VRA-TFormer superiority. The safer manuscript framing is visual-reliability augmentation / controlled comparison, with the empirically best clean and robustness variants reported honestly.