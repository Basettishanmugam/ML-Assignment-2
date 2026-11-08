"""Streamlit app - Dry Bean classification (ML Assignment 2).

The app LOADS the five saved pipelines from models/ and never retrains.
An uploaded CSV is only used for prediction + evaluation.

Run:  streamlit run app.py
"""
from __future__ import annotations

import io

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from sklearn.metrics import classification_report, confusion_matrix

import config
from src import data_loader
from src import evaluate_models as ev
from src import visualization as viz

st.set_page_config(page_title="Dry Bean Classifier | ML Assignment 2", page_icon="🫘", layout="wide")

st.markdown("""
<style>
/* Visual polish + keyboard focus visibility. Keep Streamlit's native controls/DOM order. */
:root {
  --bean-green: #175C35;
  --bean-green-dark: #104528;
  --bean-ink: #17251D;
  --bean-muted: #42534A;
  --bean-border: #A9B9AE;
  --bean-surface: #F5F8F5;
}
.block-container {padding-top: 1.25rem; padding-bottom: 2.5rem; max-width: 1440px;}
[data-testid="stAppViewContainer"] {color: var(--bean-ink);}
[data-testid="stSidebar"] {border-right: 1px solid var(--bean-border);}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {line-height: 1.55;}
div[data-testid="stMetric"] {
  background: var(--bean-surface); border: 1px solid var(--bean-border);
  border-radius: 12px; padding: 12px 14px; min-height: 104px;
}
div[data-testid="stMetric"] label {color: var(--bean-muted) !important; font-weight: 650;}
div[data-testid="stMetric"] [data-testid="stMetricValue"] {color: var(--bean-green-dark); font-weight: 750;}
.hero {
  background: linear-gradient(110deg, #104528 0%, #1B6840 70%, #287B4E 100%);
  color: #FFFFFF; padding: 22px 26px; border-radius: 14px; margin-bottom: 18px;
  box-shadow: 0 3px 12px rgba(16,69,40,.14);
}
.hero h1 {margin:0; font-size: clamp(1.55rem, 2.4vw, 2.1rem); line-height:1.2; color:#FFFFFF;}
.hero p {margin:8px 0 0 0; color:#FFFFFF; opacity:1; line-height:1.5;}
h1, h2, h3 {letter-spacing: -.015em;}
[data-testid="stTabs"] button[role="tab"] {font-weight:650; min-height:46px;}
[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
  color: var(--bean-green-dark); border-bottom-color: var(--bean-green);
}
.stButton button, .stDownloadButton button {
  border-radius: 9px; font-weight:650; min-height:44px;
}
.stButton button[kind="primary"], .stDownloadButton button[kind="primary"] {
  background:#175C35; border-color:#175C35; color:#FFFFFF;
}
.stButton button:focus-visible, .stDownloadButton button:focus-visible,
input:focus-visible, textarea:focus-visible, select:focus-visible,
[role="tab"]:focus-visible, [role="radio"]:focus-visible,
[role="checkbox"]:focus-visible, [role="button"]:focus-visible {
  outline: 3px solid #E09B24 !important; outline-offset: 3px !important;
  box-shadow: 0 0 0 2px #FFFFFF !important;
}
[data-testid="stCaptionContainer"] {color: var(--bean-muted);}
[data-testid="stAlert"] {border-radius: 10px;}
@media (max-width: 700px) {
  .block-container {padding-left: 1rem; padding-right: 1rem;}
  .hero {padding: 18px;}
  div[data-testid="stMetric"] {min-height: 88px;}
}
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {scroll-behavior:auto !important; animation:none !important; transition:none !important;}
}
</style>
""", unsafe_allow_html=True)


MODEL_INFO = {
    "Logistic Regression": "**Logistic Regression** - linear model; learns one weighted sum of the scaled features per class and converts the scores to probabilities (softmax). Fast, stable, hard to over-fit.",
    "Decision Tree": "**Decision Tree** - learns a hierarchy of if/else splits (max depth 10). Easy to interpret, but can over-fit and gives coarse probabilities.",
    "KNN": "**K-Nearest Neighbors** - classifies a bean by a distance-weighted vote of its 7 closest training beans in scaled feature space. No training step, slower predictions.",
    "Naive Bayes": "**Gaussian Naive Bayes** - applies Bayes' rule assuming features are independent and normally distributed within each class. Very fast; weakened here by strongly correlated features.",
    "SVM": "**Support Vector Machine (RBF)** - finds a maximum-margin, non-linear boundary using the RBF kernel; probabilities via Platt scaling.",
}


# ------------------------------------------------------------------ loading
@st.cache_resource(show_spinner="Loading the five saved models ...")
def get_models():
    return ev.load_models()


@st.cache_data(show_spinner=False)
def evaluate_everything(df: pd.DataFrame):
    """Predict + score all five models on the uploaded data (no training)."""
    pipes, le, _ = get_models()
    k = len(le.classes_)
    X = df[config.FEATURE_COLS]
    y = le.transform(df[config.TARGET_COL])
    table, store = ev.evaluate_all(pipes, X, y, k)
    return table, store, y


try:
    pipes, le, meta = get_models()
except Exception as exc:  # missing / incompatible model files
    st.error(f"Could not load the saved models from `{config.MODELS_DIR.name}/`: {exc}\n\n"
             "Run `python -m src.train_models` to regenerate them (see README).")
    st.stop()
classes = list(le.classes_)

# ------------------------------------------------------------------ header
st.markdown(f"""<div class="hero">
<h1>Dry Bean Variety Classifier</h1>
<p>M.Tech (AIML) · Machine Learning · Assignment 2 · Five classifiers on the UCI Dry Bean dataset</p>
</div>""", unsafe_allow_html=True)

# ------------------------------------------------------------------ sidebar
with st.sidebar:
    st.header("Test data")
    st.caption("Step 1 of 2 · Provide labelled CSV data for evaluation.")
    uploaded = st.file_uploader("Upload a test CSV", type=["csv"],
                                help="Must contain the 16 feature columns and the 'Class' column.")
    if st.button("Use bundled sample test set", key="use_sample", width="stretch",
                 help="The held-out 20 % split that none of the models saw during training."):
        st.session_state["source"] = "sample"
    if uploaded is not None:
        st.session_state["source"] = "upload"
    if config.SAMPLE_TEST_CSV.exists():
        st.download_button("Download sample test CSV", config.SAMPLE_TEST_CSV.read_bytes(),
                           "test_data.csv", "text/csv", width="stretch")
    st.header("Model")
    st.caption("Step 2 of 2 · Choose one of the five saved classifiers.")
    model_name = st.selectbox("Choose a model", list(pipes.keys()), key="model_select")
    st.caption("Models are loaded from `models/*.joblib`; nothing is retrained.")
    st.info(MODEL_INFO[model_name])

# ------------------------------------------------------------------ data intake
df, errors, source_label = None, [], None
if st.session_state.get("source") == "upload" and uploaded is not None:
    try:
        raw = pd.read_csv(uploaded)
        df, errors = data_loader.validate_uploaded_df(raw)
        source_label = f"uploaded file `{uploaded.name}`"
    except pd.errors.EmptyDataError:
        errors = ["The uploaded file is empty."]
    except Exception as exc:
        errors = [f"Could not read the file as CSV: {exc}"]
elif st.session_state.get("source") == "sample":
    df, errors = data_loader.validate_uploaded_df(pd.read_csv(config.SAMPLE_TEST_CSV))
    source_label = "bundled sample test set (`data/test_data.csv`)"

if not errors and df is not None:
    unknown = sorted(set(df[config.TARGET_COL].astype(str)) - set(classes))
    if unknown:
        errors.append(f"Unknown label(s) in '{config.TARGET_COL}': {unknown}. Allowed: {classes}")

ready = df is not None and not errors

# ------------------------------------------------------------------ tabs
tab_dash, tab_eval, tab_cmp, tab_pred = st.tabs(
    ["📋 Dashboard", "📊 Evaluation", "⚖️ Model comparison", "🔮 Predictions"])

with tab_dash:
    st.subheader("About this application")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Instances (raw)", f"{meta['n_instances_raw']:,}")
    c2.metric("After duplicate removal", f"{meta['n_instances_after_cleaning']:,}")
    c3.metric("Input features", meta["n_features"])
    c4.metric("Target classes", meta["n_classes"])
    st.markdown(f"""
**Dataset.** UCI *Dry Bean* (Koklu & Ozkan, 2020): morphological measurements extracted from images of
13,611 grains of seven registered dry-bean varieties — **{', '.join(classes)}**. The target column is `Class`.
Source: [{config.UCI_URL}]({config.UCI_URL}) · Also on [Kaggle]({config.KAGGLE_URL}).

**Training protocol.** {meta['n_train']:,} training / {meta['n_test']:,} test rows (80:20, stratified, `random_state={meta['random_state']}`).
Each model is a scikit-learn `Pipeline` (StandardScaler → classifier) fitted on the training split only.
**Uploaded files are never used for training** - the app only loads the saved pipelines, predicts and evaluates.

**How to use.** ① Upload a CSV (or use the bundled sample) → ② pick a model → ③ explore the tabs.
""")
    with st.expander("Required CSV format"):
        st.write("Columns (exact names; `AspectRation`/`roundness` spellings are also accepted):")
        st.code(", ".join(config.FEATURE_COLS + [config.TARGET_COL]))
    if ready:
        st.success(f"Loaded {source_label}: {len(df):,} rows.")

if errors:
    for e in errors:
        st.error(e)
elif df is None:
    for t in (tab_eval, tab_cmp, tab_pred):
        with t:
            st.info("👈 Upload a test CSV or click **Use bundled sample test set** in the sidebar.")

if ready:
    table, store, y_true = evaluate_everything(df)
    n_classes_present = len(np.unique(y_true))
    if n_classes_present < len(classes):
        st.warning(f"The data contains only {n_classes_present} of {len(classes)} classes. "
                   "AUC is averaged over the classes that can be scored.")
    pred = store[model_name]["pred"]

    with tab_eval:
        st.subheader(f"{model_name} — evaluation on {source_label}")
        st.caption("ℹ️ The uploaded data is used only for prediction and evaluation. It is **not** used to retrain or modify any model.")
        row = table.set_index("ML Model Name").loc[model_name]
        cols = st.columns(6)
        for col, m in zip(cols, ev.METRIC_COLS):
            val = row[m]
            col.metric(m if m != "AUC" else "AUC (OvR macro)", "n/a" if pd.isna(val) else f"{val:.4f}")
        left, right = st.columns([1, 1])
        with left:
            st.markdown("**Confusion matrix**")
            st.caption("Rows are actual classes; columns are predicted classes. Each cell shows count and row percentage.")
            cm = confusion_matrix(y_true, pred, labels=list(range(len(classes))))
            fig = viz.plot_confusion_matrix(cm, classes, f"{model_name}")
            fig.set_dpi(160)
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
            # Text/table equivalent so the chart is not the only way to access the result.
            cm_table = pd.DataFrame(cm, index=classes, columns=classes)
            cm_table.index.name = "Actual \\ Predicted"
            with st.expander("View confusion matrix as a data table"):
                st.dataframe(cm_table, use_container_width=True)
        with right:
            st.markdown("**Classification report**")
            rep = classification_report(y_true, pred, labels=list(range(len(classes))),
                                        target_names=classes, output_dict=True, zero_division=0)
            rep_df = pd.DataFrame(rep).T.rename(columns={"f1-score": "f1"})
            rep_df["support"] = rep_df["support"].astype(int)
            st.dataframe(rep_df.style.format({"precision": "{:.4f}", "recall": "{:.4f}", "f1": "{:.4f}"}),
                         width="stretch", height=370)
            st.caption("Macro-averaged precision / recall / F1 are used for the multiclass summary metrics.")

    with tab_cmp:
        st.subheader("All five models on the same data")
        styled = table.style.format({m: "{:.4f}" for m in ev.METRIC_COLS}, na_rep="n/a") \
                            .highlight_max(subset=ev.METRIC_COLS, color="#C8E6C9")
        st.dataframe(styled, width="stretch", hide_index=True)
        st.caption("The table is the precise, screen-reader-friendly alternative to the chart. Green highlights the highest value in each metric column.")

        fig = viz.plot_model_comparison(table)
        fig.set_dpi(160)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
        best = table.set_index("ML Model Name")
        st.info("Best per metric: " + " · ".join(f"**{m}** → {best[m].idxmax()}" for m in ev.METRIC_COLS
                                                  if best[m].notna().any()))
        st.download_button("Download comparison table (CSV)", table.round(4).to_csv(index=False).encode(),
                           "model_comparison_uploaded.csv", "text/csv")

    with tab_pred:
        st.subheader(f"Predictions — {model_name}")
        proba = store[model_name]["proba"]
        out = df.copy()
        out = out.rename(columns={config.TARGET_COL: "Actual"})
        out["Predicted"] = le.inverse_transform(pred)
        out["Confidence"] = proba.max(axis=1).round(4)
        out["Correct"] = out["Actual"] == out["Predicted"]
        n_wrong = int((~out["Correct"]).sum())
        c1, c2 = st.columns(2)
        c1.metric("Correct", f"{len(out) - n_wrong:,}")
        c2.metric("Misclassified", f"{n_wrong:,}")
        only_wrong = st.checkbox("Show only misclassified rows", value=False)
        view = out[~out["Correct"]] if only_wrong else out
        front = ["Actual", "Predicted", "Correct", "Confidence"]
        st.dataframe(view[front + config.FEATURE_COLS], width="stretch", height=420)
        buf = io.StringIO(); out[front + config.FEATURE_COLS].to_csv(buf, index=False)
        st.download_button("⬇️ Download predictions (CSV)", buf.getvalue().encode(),
                           f"predictions_{config.MODEL_FILES[model_name].replace('.joblib', '')}.csv", "text/csv")

st.divider()
st.caption("ML Assignment 2 · Data: Koklu & Ozkan (2020), CC BY 4.0 · Models are trained offline; this app only predicts and evaluates. Keyboard users: use Tab / Shift+Tab to move through controls and the arrow keys within tab and radio groups.")
