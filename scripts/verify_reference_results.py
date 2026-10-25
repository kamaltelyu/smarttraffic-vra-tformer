from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "results" / "reference" / "main"
RR = ROOT / "results" / "reference" / "rr"
RB = ROOT / "results" / "reference" / "rb"


def close(name, got, expected, tol=5e-3):
    ok = abs(float(got) - expected) <= tol
    print(
        f"{'PASS' if ok else 'FAIL'}  {name:42s} "
        f"got={float(got):.4f} expected≈{expected:.4f}"
    )
    if not ok:
        raise AssertionError(name)


main = pd.read_csv(MAIN / "table_main_forecasting_results_FINAL.csv")
means = main.groupby("Model")["MAE"].mean()
close("ReliabilityConcat clean mean MAE", means["Transformer+ReliabilityConcat"], 11.0902)
close("Transformer clean mean MAE", means["Transformer"], 11.1905)
close("VRA-TFormer clean mean MAE", means["VRA-TFormer"], 11.2283)

rob = (
    pd.read_csv(MAIN / "table_robustness_summary_FINAL.csv")
    .groupby("Model", as_index=True)["Relative_Degradation_%"]
    .mean()
)
close("Transformer average RD (%)", rob["Transformer"], 8.5420)
close("ReliabilityConcat average RD (%)", rob["Transformer+ReliabilityConcat"], 63.2007)
close("VRA-TFormer average RD (%)", rob["VRA-TFormer"], 23.9365)

rr_clean = pd.read_csv(RR / "RR_clean_mean.csv").set_index("Model")
rr_rob = pd.read_csv(RR / "RR_robustness_average.csv").set_index("Model")
close("RR-TFormer clean mean MAE", rr_clean.loc["RR-TFormer", "MAE"], 12.9558)
close("RR-TFormer degraded absolute MAE", rr_rob.loc["RR-TFormer", "Degraded_MAE"], 17.7079)
close("RR-TFormer average RD (%)", rr_rob.loc["RR-TFormer", "Relative_Degradation_pct"], 3.9412)

rb_clean = pd.read_csv(RB / "RB_clean_mean.csv").set_index("Model")
rb_rob = pd.read_csv(RB / "RB_robustness_average.csv").set_index("Model")
alpha = (
    pd.read_csv(RB / "RB_alpha_validation_selection.csv")
    .sort_values("Selection_Score")
    .iloc[0]["alpha"]
)
close("RB-TFormer selected alpha", alpha, 0.3, tol=1e-9)
close("RB-TFormer clean mean MAE", rb_clean.loc["RB-TFormer", "MAE"], 11.4381)
close("RB-TFormer degraded absolute MAE", rb_rob.loc["RB-TFormer", "Degraded_MAE"], 16.9763)
close("RB-TFormer average RD (%)", rb_rob.loc["RB-TFormer", "Relative_Degradation_pct"], 7.4075)

print("\nAll reference-result checks passed.")
