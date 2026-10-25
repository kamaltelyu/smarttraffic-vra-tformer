# SmartTraffic: Visual Reliability in Camera-Derived Multi-Horizon Traffic Flow Forecasting

Reproducibility repository for the manuscript:

> **Visual Reliability in Camera-Derived Multi-Horizon Traffic Flow Forecasting: An Accuracy-Robustness Study**

This repository reproduces the camera-to-forecast pipeline, model comparisons, controlled degradation study, statistical tests, and paper figures for SmartTraffic.

## What is reproduced

- fixed-CCTV video processing with **YOLO11s + ByteTrack**;
- 5-s camera-derived traffic observations: `car`, `motorcycle`, `bus`, `truck`, `total`;
- six lightweight visual-reliability descriptors: detection confidence, track continuity, blur, illumination quality, occlusion quality, and frame availability;
- direct multi-horizon forecasting at **30 / 60 / 90 / 120 s** from a **300-s** historical window;
- Persistence, LSTM, GRU, Transformer, PatchTST, iTransformer, ReliabilityConcat, and VRA-TFormer comparisons;
- VRA-TFormer ablations and Wilcoxon-Holm tests;
- paired controlled degradation with **clean future targets**;
- RR-TFormer robustness-regularized training;
- RB-TFormer validation-selected checkpoint interpolation.

The paper is an **accuracy-robustness study**, not a universal-superiority claim. Under the stored reference run, ReliabilityConcat gives the lowest clean mean MAE, while the plain Transformer gives the lowest absolute degraded forecasting error.

## Repository structure

```text
.
├── configs/
│   └── paper_config.yaml
├── data/
│   └── README.md
├── notebooks/
│   ├── 01_prepare_data_and_train_models.ipynb
│   ├── 02_reproduce_main_paper_results.ipynb
│   ├── 03_train_rr_tformer.ipynb
│   └── 04_select_rb_tformer.ipynb
├── src/smarttraffic/
│   ├── config.py
│   ├── models.py
│   ├── vision.py
│   └── evaluation.py
├── scripts/
│   ├── check_notebooks.py
│   └── verify_reference_results.py
├── results/
│   ├── reference/
│   └── figures/
├── paper/
│   └── VRA_TFormer_architecture.png
├── requirements.txt
├── CITATION.cff
└── README.md
```

## Reproducibility levels

### A. Fast result verification

No raw video is needed. The repository includes the final CSV artifacts used to check the headline manuscript values.

```bash
pip install -r requirements.txt
python scripts/verify_reference_results.py
```

### B. Reproduce final paper tables from existing caches/checkpoints

Run:

`notebooks/02_reproduce_main_paper_results.ipynb`

This notebook intentionally **does not download or reprocess video**. It expects the clean/degraded parquet caches and forecasting checkpoints produced by Notebook 01.

### C. Full camera-to-forecast reproduction

Run the notebooks in order:

1. `01_prepare_data_and_train_models.ipynb`  
   Generates YOLO11s/ByteTrack-derived clean and degraded caches and trains the main models.
2. `02_reproduce_main_paper_results.ipynb`  
   Reconstructs the exact chronological split and final paired robustness evaluation with **degraded history → clean future target**.
3. `03_train_rr_tformer.ipynb`  
   Trains the traffic-only RR-TFormer using reliability as privileged training supervision.
4. `04_select_rb_tformer.ipynb`  
   Selects checkpoint-interpolation weight `alpha` using validation data only and evaluates the locked RB-TFormer.

Notebook 01 is the **data-preparation/training notebook**. For manuscript robustness numbers and final figures, Notebook 02 is authoritative because it applies the corrected paired clean-target protocol.

## Data placement

The main raw dataset is the **AI City Challenge 2021 Track 1 multi-class vehicle-counting video collection**. Raw data are not redistributed in this repository.

The Colab notebooks use the following Google Drive project root by default:

```text
MyDrive/SmartTraffic_VRA_TFormer_IJIES/
```

Expected generated layout:

```text
SmartTraffic_VRA_TFormer_IJIES/
├── data/aicity21/
├── cache/
│   ├── aicity_clean/
│   └── aicity_degraded/
├── models/
├── tables/
├── figures/
├── logs/
├── rr/
└── rb/
```

If the raw archive cannot be downloaded automatically, place it in the path requested by Notebook 01 and rerun the extraction cell. Do **not** commit the raw videos to GitHub.

## Final paper configuration

See `configs/paper_config.yaml`. Key settings are:

| Setting | Value |
|---|---:|
| Random seed | 42 |
| Base aggregation | 5 s |
| Main lookback | 60 steps = 300 s |
| Forecast horizons | 30, 60, 90, 120 s |
| Split | 60% / 20% / 20% chronological |
| YOLO model | YOLO11s |
| Detector confidence | 0.25 |
| Detector IoU | 0.50 |
| Image size | 960 |
| Vehicle classes | car, motorcycle, bus, truck |
| Transformer width | 64 |
| Attention heads | 4 |
| Encoder layers | 2 |
| Stress-test history | 24 steps = 120 s |
| Stress conditions | blur, low light, occlusion, frame drop |
| Stress severities | 1 and 3 |
| RB-TFormer selected α | 0.3 |

## Important target definition

The forecast target is **camera-derived traffic intensity from the clean vision pipeline**, not an official movement-of-interest ground-truth count. ByteTrack first-seen track IDs are accumulated as traffic events within each 5-s bin. This distinction is important when interpreting fragmentation and counting error.

## Robustness protocol

The final robustness test is paired in time:

```text
degraded historical camera-derived observation
        ↓
forecasting model
        ↓
CLEAN future traffic target at the same timestamps
```

Relative degradation is reported together with **absolute degraded MAE**. A small relative degradation alone is not interpreted as superior robustness when the matched clean error is already high.

## Reference results

Reference CSVs and paper figures are stored under `results/`. Run:

```bash
python scripts/verify_reference_results.py
```

Representative stored results include:

- ReliabilityConcat clean mean MAE ≈ **11.0902**;
- Transformer clean mean MAE ≈ **11.1905**;
- VRA-TFormer clean mean MAE ≈ **11.2283**;
- Transformer average relative degradation ≈ **8.542%**;
- VRA-TFormer average relative degradation ≈ **23.9365%**;
- RR-TFormer relative degradation ≈ **3.9412%**, but with higher absolute degraded MAE;
- RB-TFormer selected `α = 0.3`, clean mean MAE ≈ **11.4381**, degraded MAE ≈ **16.9763**.

## Reference environment

The stored final-run environment was:

```text
Python 3.13.16
PyTorch 2.11.0+cu130
NumPy 2.1.3
pandas 2.2.3
scikit-learn 1.6.1
SciPy 1.16.3
CUDA 13.0
```

Exact GPU/Colab package builds can evolve. `requirements.txt` therefore specifies the main Python dependencies, while `results/reference/main/environment.json` records the reference environment used for the final run.

## Code / data release notes

- Raw AI City videos are intentionally excluded.
- Generated parquet caches and most checkpoints are excluded from Git because they are reproducible from Notebook 01 and can become large.
- Do not commit personal Google Drive paths, access tokens, or credentials.
- Add your preferred open-source `LICENSE` before public release; this package does not assume a license on your behalf.

## Authors

Mustafa Kamal; Michael Angello Qadosy Riyadi; Farah Zakiyah Rahmanti; Alqis Rausanfita; Sulthonika Mahfudz Al Mujahidin.

## Citation

Use `CITATION.cff` or cite the associated IJIES manuscript when publication metadata become available.
