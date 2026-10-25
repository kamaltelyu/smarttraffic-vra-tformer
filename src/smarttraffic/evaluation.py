import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def forecast_metrics(y_true, y_pred):
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    return {
        "MAE": float(mean_absolute_error(y_true, y_pred)),
        "RMSE": float(mean_squared_error(y_true, y_pred) ** 0.5),
        "WAPE_pct": float(np.abs(y_true-y_pred).sum() / max(np.abs(y_true).sum(), 1e-9) * 100),
        "R2": float(r2_score(y_true, y_pred)),
    }


def relative_degradation(clean_error, degraded_error):
    return float((degraded_error-clean_error) / max(clean_error, 1e-9) * 100)
