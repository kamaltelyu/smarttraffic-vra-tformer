from dataclasses import dataclass, field
from typing import Tuple

TRAFFIC_COLS = ("car", "motorcycle", "bus", "truck", "total")
REL_COLS = (
    "mean_conf", "track_continuity", "blur_log",
    "illumination_quality", "occlusion_quality", "frame_availability",
)

@dataclass(frozen=True)
class PaperConfig:
    seed: int = 42
    bin_sec: int = 5
    lookback_steps: int = 60
    forecast_block_steps: int = 6
    n_horizons: int = 4
    train_frac: float = 0.60
    val_frac: float = 0.20
    yolo_weights: str = "yolo11s.pt"
    yolo_conf: float = 0.25
    yolo_iou: float = 0.50
    vehicle_class_ids: Tuple[int, ...] = (2, 3, 5, 7)
    video_frame_stride: int = 2
    image_size: int = 960
    d_model: int = 64
    n_head: int = 4
    n_layers: int = 2
    dropout: float = 0.10
    batch_size: int = 64
    epochs: int = 80
    patience: int = 12
    lr: float = 1e-3
    weight_decay: float = 1e-4
    robust_lookback_steps: int = 24
    degradations: Tuple[str, ...] = ("blur", "lowlight", "occlusion", "frame_drop")
    degradation_severities: Tuple[int, ...] = (1, 3)
    rb_alphas: Tuple[float, ...] = tuple(i / 10 for i in range(11))
    selected_rb_alpha: float = 0.3
