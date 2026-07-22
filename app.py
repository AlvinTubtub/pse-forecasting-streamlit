"""ForecastPH — Streamlit rebuild.

Keeps the original dashboard's exact HTML/CSS/JS (Tailwind + ApexCharts +
Phosphor Icons) via st.components.v1.html(), but replaces every
Math.random() mock value with real numbers: real historical OHLCV data,
real trained-model metrics, and real next-day predictions on uploaded CSVs.

No database — everything is CSV in, forecast out, per Streamlit run.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

from services.data_loader import load_companies
from services.data_validator import CSVValidationError, validate_ohlcv_csv
from services.forecasting import run_all_models

BASE_DIR = Path(__file__).resolve().parent
TEMPLATE_PATH = BASE_DIR / "assets" / "dashboard_template.html"
DATA_DIR = BASE_DIR / "data" / "raw"

st.set_page_config(
    page_title="ForecastPH | Educational Stock Forecasting",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------------------------
# Cached model training — keyed by symbol + file modified time, so a bundled
# CSV is only retrained when it actually changes, not on every rerun.
# ---------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def _train_symbol(symbol: str, _mtime: float) -> dict:
    df = validate_ohlcv_csv(DATA_DIR / f"{symbol}.csv")
    return run_all_models(df)


@st.cache_data(show_spinner=False)
def _run_live_prediction(file_bytes: bytes) -> dict:
    import io

    df = validate_ohlcv_csv(io.BytesIO(file_bytes))
    result = run_all_models(df)

    preview_rows = [
        {
            "date": r.Date.strftime("%Y-%m-%d"),
            "open": round(float(r.Open), 2),
            "high": round(float(r.High), 2),
            "low": round(float(r.Low), 2),
            "close": round(float(r.Close), 2),
            "volume": int(r.Volume),
        }
        for r in df.head(5).itertuples()
    ]

    recent = df.tail(21)
    historical = [
        {"x": int(pd.Timestamp(r.Date).timestamp() * 1000), "y": round(float(r.Close), 2)}
        for r in recent.itertuples()
    ]

    return {
        "ready": True,
        "previewRows": preview_rows,
        "historical": historical,
        "predictions": result["next_close"],  # {lag, arima, lstm}
    }


def build_app_data(active_page: str) -> dict:
    companies, dataframes, missing = load_companies()

    metrics_by_symbol = {}
    predictions_by_symbol = {}

    for symbol, df in dataframes.items():
        mtime = (DATA_DIR / f"{symbol}.csv").stat().st_mtime
        result = _train_symbol(symbol, mtime)
        metrics_by_symbol[symbol] = result["metrics"]
        predictions_by_symbol[symbol] = {
            "nextClose": result["next_close"]["lag"],
            "backtest30": result["backtest30"],
        }

    # Aggregate = mean of each numeric metric across companies that trained
    # successfully. Falls back to zeros if nothing trained yet.
    aggregate = {}
    for model_id in ["lag_reg", "arima", "lstm", "naive"]:
        rows = [metrics_by_symbol[s][model_id] for s in metrics_by_symbol]
        if rows:
            aggregate[model_id] = {
                k: f"{np.mean([float(r[k]) for r in rows]):.4f}" if k != "mape"
                else f"{np.mean([float(r[k]) for r in rows]):.2f}"
                for k in ["rmse", "mae", "mape", "r2"]
            }
        else:
            aggregate[model_id] = {"rmse": "0", "mae": "0", "mape": "0", "r2": "0"}

    live_prediction = st.session_state.get("live_prediction", {"ready": False})

    return {
        "companies": companies,
        "metrics": {"bySymbol": metrics_by_symbol, "aggregate": aggregate},
        "predictions": predictions_by_symbol,
        "livePrediction": live_prediction,
        "activePage": active_page,
    }, missing


def render_dashboard(app_data: dict):
    html_template = TEMPLATE_PATH.read_text(encoding="utf-8")
    html = html_template.replace("__APP_DATA_JSON__", json.dumps(app_data))
    # st.iframe (replaces the deprecated st.components.v1.html) embeds this
    # raw HTML string in a same-origin iframe that allows JS execution.
    st.iframe(html, height=2200, width="stretch")


def main():
    # Which tab the embedded dashboard is showing. Python has no visibility into
    # the iframe's internal JS-only tab state, so the dashboard's nav() function
    # syncs a ?page=live URL param on this top-level page whenever the user enters
    # or leaves the Live Prediction tab (see assets/dashboard_template.html).
    active_page = "home"

    st.sidebar.header("📤 Live Prediction")

    uploaded = st.sidebar.file_uploader(
        "Upload OHLCV CSV",
        type=["csv"]
    )

    if uploaded:
        try:
            st.session_state["live_prediction"] = _run_live_prediction(
                uploaded.getvalue()
            )
            st.sidebar.success("Prediction generated.")
        except CSVValidationError as exc:
            st.sidebar.error(str(exc))
            st.session_state["live_prediction"] = {"ready": False}

    if st.sidebar.button("Clear Prediction"):
        st.session_state["live_prediction"] = {"ready": False}

    app_data, missing = build_app_data(active_page)

    if missing:
        st.sidebar.warning(
            "Using placeholder data for: " + ", ".join(missing) + ". "
            "Add real CSVs to data/raw/<SYMBOL>.csv to replace these."
        )

    render_dashboard(app_data)

if __name__ == "__main__":
    main()
