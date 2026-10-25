# SmartTraffic RB-TFormer — Final Validation-Selected Interpolation Digest

## Model naming
- Transformer
- ReliabilityConcat
- VRA-TFormer
- RR-TFormer
- RB-TFormer

## Selection protocol
- RB-TFormer alpha is selected only from validation data.
- Selection combines clean validation MAE and synthetic-corruption validation MAE.
- Clean test and real degraded cache are untouched until alpha is locked.

## Selected alpha
- **α = 0.3**

## Validation selection
|   alpha |   Validation_Clean_MAE |   Validation_Corrupt_MAE |   Clean_Ratio_to_Transformer |   Corrupt_Ratio_to_Transformer |   Selection_Score |
|--------:|-----------------------:|-------------------------:|-----------------------------:|-------------------------------:|------------------:|
|     0   |                10.6002 |                  12.3363 |                      1       |                       1        |          1        |
|     0.1 |                10.6875 |                  12.1096 |                      1.00823 |                       0.981622 |          0.994927 |
|     0.2 |                10.7977 |                  11.9112 |                      1.01862 |                       0.965537 |          0.99208  |
|     0.3 |                10.944  |                  11.7346 |                      1.03243 |                       0.951222 |          0.991827 |
|     0.4 |                11.1177 |                  11.5862 |                      1.04882 |                       0.939192 |          0.994005 |
|     0.5 |                11.3121 |                  11.4684 |                      1.06715 |                       0.929643 |          0.998398 |
|     0.6 |                11.5329 |                  11.3757 |                      1.08798 |                       0.922131 |          1.00506  |
|     0.7 |                11.7814 |                  11.314  |                      1.11143 |                       0.917128 |          1.01428  |
|     0.8 |                12.0581 |                  11.2861 |                      1.13753 |                       0.914868 |          1.0262   |
|     0.9 |                12.3578 |                  11.2913 |                      1.1658  |                       0.915285 |          1.04054  |
|     1   |                12.6848 |                  11.3223 |                      1.19665 |                       0.917803 |          1.05723  |

## Clean mean results
| Model             |     MAE |    RMSE |   WAPE_pct |       R2 |
|:------------------|--------:|--------:|-----------:|---------:|
| ReliabilityConcat | 11.0902 | 14.6127 |    22.095  | 0.813123 |
| Transformer       | 11.1905 | 14.665  |    22.2963 | 0.813235 |
| VRA-TFormer       | 11.2283 | 14.8414 |    22.3728 | 0.808851 |
| RB-TFormer        | 11.4381 | 15.0294 |    22.7902 | 0.803835 |
| RR-TFormer        | 12.9558 | 16.992  |    25.8169 | 0.748622 |

## Average robustness
| Model             |   Clean_MAE |   Degraded_MAE |   Relative_Degradation_pct |   Worst_Scenario_RD |
|:------------------|------------:|---------------:|---------------------------:|--------------------:|
| Transformer       |     15.4764 |        16.7984 |                    8.542   |             53.3928 |
| RB-TFormer        |     15.8055 |        16.9763 |                    7.40749 |             45.0261 |
| RR-TFormer        |     17.0364 |        17.7079 |                    3.9412  |             21.1628 |
| VRA-TFormer       |     15.6581 |        19.4061 |                   23.9365  |             84.7606 |
| ReliabilityConcat |     16.7561 |        27.3461 |                   63.2007  |            166.322  |

## Decision criteria
| Criterion                                     | Pass   |   RB_value |   Threshold_reference |
|:----------------------------------------------|:-------|-----------:|----------------------:|
| Clean within 1% of best clean model           | False  |    11.4381 |               11.2011 |
| Absolute degraded MAE better than Transformer | False  |    16.9763 |               16.7984 |
| Clean MAE better than Transformer             | False  |    11.4381 |               11.1905 |
| 120-s MAE <=11.50                             | False  |    11.8779 |               11.5    |

## Final decision
RB-TFormer does not improve the clean-robustness Pareto frontier enough to justify replacing the existing accuracy-robustness study framing.