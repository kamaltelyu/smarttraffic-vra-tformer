import numpy as np

try:
    import cv2
except ImportError:  # allows importing non-vision utilities without OpenCV
    cv2 = None


def iou_matrix(boxes):
    b = np.asarray(boxes, float)
    n = len(b)
    if n < 2:
        return np.zeros((n, n))
    x1 = np.maximum(b[:, None, 0], b[None, :, 0])
    y1 = np.maximum(b[:, None, 1], b[None, :, 1])
    x2 = np.minimum(b[:, None, 2], b[None, :, 2])
    y2 = np.minimum(b[:, None, 3], b[None, :, 3])
    inter = np.clip(x2-x1, 0, None) * np.clip(y2-y1, 0, None)
    area = np.clip(b[:, 2]-b[:, 0], 0, None) * np.clip(b[:, 3]-b[:, 1], 0, None)
    union = area[:, None] + area[None, :] - inter + 1e-9
    m = inter / union
    np.fill_diagonal(m, 0)
    return m


def frame_quality(frame, boxes, confs, ids, prev_ids):
    if cv2 is None:
        raise ImportError("opencv-python is required for frame_quality")
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    bright = float(gray.mean() / 255)
    illum = float(np.clip(1 - abs(bright - .5) / .5, 0, 1))
    blur_log = float(np.log1p(cv2.Laplacian(gray, cv2.CV_64F).var()))
    mean_conf = float(np.mean(confs)) if len(confs) else np.nan
    ids = {int(i) for i in ids if i is not None and int(i) >= 0}
    prev = {int(i) for i in prev_ids if i is not None and int(i) >= 0}
    continuity = (len(ids & prev) / len(ids)) if ids else np.nan
    if len(boxes) >= 2:
        overlap = iou_matrix(boxes).max(axis=1)
        occ_risk = float(np.mean(overlap > .10))
    else:
        occ_risk = 0.0
    return {
        "mean_conf": mean_conf,
        "track_continuity": continuity,
        "blur_log": blur_log,
        "brightness": bright,
        "illumination_quality": illum,
        "occlusion_quality": 1 - occ_risk,
    }


def degrade(frame, condition="clean", severity=0, seed=42):
    """Controlled visual degradation used to create the stress-test cache."""
    if cv2 is None:
        raise ImportError("opencv-python is required for degrade")
    if condition == "clean" or severity == 0:
        return frame
    if severity not in (1, 2, 3):
        raise ValueError("severity must be 1, 2, or 3")
    out = frame.copy()
    h, w = out.shape[:2]
    rng = np.random.default_rng(seed)
    if condition == "blur":
        k = {1:5, 2:11, 3:21}[severity]
        out = cv2.GaussianBlur(out, (k, k), 0)
    elif condition == "lowlight":
        f = {1:.70, 2:.45, 3:.25}[severity]
        out = np.clip(out.astype(np.float32) * f, 0, 255).astype(np.uint8)
    elif condition == "occlusion":
        n = {1:1, 2:2, 3:3}[severity]
        frac = {1:.10, 2:.16, 3:.22}[severity]
        for _ in range(n):
            rw, rh = max(8, int(w*frac)), max(8, int(h*frac))
            x = int(rng.integers(0, max(1, w-rw)))
            y = int(rng.integers(int(h*.25), max(int(h*.25)+1, h-rh)))
            cv2.rectangle(out, (x,y), (x+rw,y+rh), (0,0,0), -1)
    elif condition == "frame_drop":
        # Frame dropping is implemented in the video loop; no pixel transform here.
        pass
    else:
        raise ValueError(f"Unknown condition: {condition}")
    return out
