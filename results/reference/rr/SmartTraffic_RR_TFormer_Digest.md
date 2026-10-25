# SmartTraffic RR-TFormer — One-Shot Digest

## Architecture
- Inference input: traffic history only.
- Visual reliability is privileged training supervision only.
- Auxiliary denoising reconstruction head.
- Auxiliary reliability prediction head.
- Auxiliary heads are not needed for forecasting inference.
- No video or detector reprocessing.

## Clean mean results
| Model                         |     MAE |    RMSE |   WAPE_pct |       R2 |
|:------------------------------|--------:|--------:|-----------:|---------:|
| Transformer+ReliabilityConcat | 11.0902 | 14.6127 |    22.095  | 0.813123 |
| Transformer                   | 11.1905 | 14.665  |    22.2963 | 0.813235 |
| VRA-TFormer-old               | 11.2283 | 14.8414 |    22.3728 | 0.808851 |
| RR-TFormer                    | 12.9558 | 16.992  |    25.8169 | 0.748622 |

## Clean horizon results
| Model                         | Horizon   |     MAE |    RMSE |   WAPE_% |       R2 |
|:------------------------------|:----------|--------:|--------:|---------:|---------:|
| Transformer                   | 30s       | 11.4877 | 14.765  |  22.8666 | 0.789619 |
| Transformer                   | 60s       | 10.6191 | 13.6545 |  21.2584 | 0.830156 |
| Transformer                   | 90s       | 11.2201 | 15.0881 |  22.2106 | 0.814913 |
| Transformer                   | 120s      | 11.4349 | 15.1524 |  22.8496 | 0.818251 |
| Transformer+ReliabilityConcat | 30s       | 11.9038 | 15.4338 |  23.6947 | 0.770128 |
| Transformer+ReliabilityConcat | 60s       | 10.935  | 14.1509 |  21.8909 | 0.817585 |
| Transformer+ReliabilityConcat | 90s       | 11.2967 | 15.0342 |  22.3622 | 0.816232 |
| Transformer+ReliabilityConcat | 120s      | 10.2252 | 13.8319 |  20.4322 | 0.848548 |
| VRA-TFormer-old               | 30s       | 11.5176 | 14.8339 |  22.926  | 0.787653 |
| VRA-TFormer-old               | 60s       | 10.4534 | 13.5767 |  20.9267 | 0.832086 |
| VRA-TFormer-old               | 90s       | 10.9623 | 15.1827 |  21.7003 | 0.812584 |
| VRA-TFormer-old               | 120s      | 11.9798 | 15.7721 |  23.9383 | 0.803081 |
| RR-TFormer                    | 30s       | 13.5207 | 17.4407 |  26.9132 | 0.706462 |
| RR-TFormer                    | 60s       | 12.3691 | 16.0962 |  24.7618 | 0.763982 |
| RR-TFormer                    | 90s       | 12.2312 | 16.4487 |  24.212  | 0.780028 |
| RR-TFormer                    | 120s      | 13.7024 | 17.9825 |  27.3806 | 0.744017 |

## Average paired robustness
| Model                         |   Clean_MAE |   Degraded_MAE |   Relative_Degradation_pct |
|:------------------------------|------------:|---------------:|---------------------------:|
| RR-TFormer                    |     17.0364 |        17.7079 |                     3.9412 |
| Transformer                   |     15.4764 |        16.7984 |                     8.542  |
| VRA-TFormer-old               |     15.6581 |        19.4061 |                    23.9365 |
| Transformer+ReliabilityConcat |     16.7561 |        27.3461 |                    63.2007 |

## RR robustness details
| Model      | Condition   |   Severity |   Clean_MAE |   Degraded_MAE |   Relative_Degradation_% |   N_windows |   N_sequences |   Aux_Reliability_Clean |   Aux_Reliability_Degraded | Scenario      |
|:-----------|:------------|-----------:|------------:|---------------:|-------------------------:|------------:|--------------:|------------------------:|---------------------------:|:--------------|
| RR-TFormer | blur        |          1 |     17.0364 |        15.5771 |                 -8.56609 |          26 |             2 |                 0.83208 |                   0.828959 | blur-S1       |
| RR-TFormer | blur        |          3 |     17.0364 |        20.6248 |                 21.0628  |          26 |             2 |                 0.83208 |                   0.818446 | blur-S3       |
| RR-TFormer | frame_drop  |          1 |     17.0364 |        18.8125 |                 10.4253  |          26 |             2 |                 0.83208 |                   0.83303  | frame_drop-S1 |
| RR-TFormer | frame_drop  |          3 |     17.0364 |        16.3229 |                 -4.18803 |          26 |             2 |                 0.83208 |                   0.825927 | frame_drop-S3 |
| RR-TFormer | lowlight    |          1 |     17.0364 |        16.0164 |                 -5.98742 |          26 |             2 |                 0.83208 |                   0.836148 | lowlight-S1   |
| RR-TFormer | lowlight    |          3 |     17.0364 |        15.8909 |                 -6.72424 |          26 |             2 |                 0.83208 |                   0.834405 | lowlight-S3   |
| RR-TFormer | occlusion   |          1 |     17.0364 |        17.7766 |                  4.34446 |          26 |             2 |                 0.83208 |                   0.831764 | occlusion-S1  |
| RR-TFormer | occlusion   |          3 |     17.0364 |        20.6418 |                 21.1628  |          26 |             2 |                 0.83208 |                   0.827261 | occlusion-S3  |

## Decision criteria
| Criterion                            | Pass   |   RR_value |   Threshold_reference |
|:-------------------------------------|:-------|-----------:|----------------------:|
| Strict clean best                    | False  |    12.9558 |               11.0902 |
| Strict robustness best               | True   |     3.9412 |                8.542  |
| Clean MAE <=11.20                    | False  |    12.9558 |               11.2    |
| Average robustness degradation <=10% | True   |     3.9412 |               10      |
| 120-s MAE <= vanilla reference       | False  |    13.7024 |               11.4349 |
| Worst scenario degradation <=40%     | True   |    21.1628 |               40      |

## Final decision
STOP ARCHITECTURE OPTIMIZATION: RR-TFormer did not satisfy the pre-registered success criteria. Retain the existing accuracy-robustness manuscript.