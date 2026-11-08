# Project overview

## What each file does
| File | Purpose |
|---|---|
| `config.py` | Single source of paths (relative, no hard-coded folders), seeds, class/feature names, dataset links and citation |
| `src/data_loader.py` | **Option A** `load_from_uci()` (ucimlrepo) and **Option B** `load_from_file()` (Excel/CSV); `standardize_columns()` makes both sources identical; `validate_dataset()`; `validate_uploaded_df()` used by the app |
| `src/preprocessing.py` | `clean_dataset()` (missing/duplicates), `encode_target()`, `split_data()` (stratified 80:20, seed 42), `save_splits()` |
| `src/train_models.py` | Builds the five `Pipeline(StandardScaler → classifier)` objects, trains on the training split only, saves `.joblib` + metadata |
| `src/evaluate_models.py` | `compute_metrics()` (Accuracy, AUC, Precision, Recall, F1, MCC), `safe_macro_auc()`, writes comparison CSVs, classification reports, figures |
| `src/visualization.py` | EDA plots, confusion matrix, comparison chart, macro ROC curves |
| `app.py` | Streamlit UI: upload → validate → choose model → metrics, confusion matrix, report, comparison, predictions |
| `notebooks/ML_Assignment_2.ipynb` | Teaching notebook: both data loaders, EDA, preprocessing, models, metrics, observations (already executed) |
| `tests/run_checks.py` | Automated checks; writes `reports/TESTING_REPORT.md` |
| `tools/*.py` | Regenerate the notebook and the documents/PDF from the results (not needed to run the app) |
| `models/` | Trained pipelines (`logistic_regression`, `decision_tree`, `knn`, `naive_bayes`, `svm`), `label_encoder.joblib`, `metadata.json` |
| `reports/` | `model_comparison.csv`, details, classification reports, figures, testing report |
| `data/` | Raw + processed data and `test_data.csv` (held-out 20 % split) |
| `deployment/` | Step-by-step GitHub and Streamlit Cloud guides |
| `submission/ML_Assignment_2_Submission.pdf` | Submission template + full README content |

## Install dependencies (all operating systems)
Python 3.11+ is required. Commands for **Windows PowerShell / cmd / Git Bash, macOS and Linux** are in [`SETUP_BY_OS.md`](SETUP_BY_OS.md); the short version:

| OS / shell | Environment | Install |
|---|---|---|
| Windows PowerShell | `py -3.12 -m venv .venv` → `.venv\Scripts\Activate.ps1` | `pip install -r requirements.txt` |
| Windows cmd | `py -3.12 -m venv .venv` → `.venv\Scripts\activate.bat` | `pip install -r requirements.txt` |
| macOS / Linux | `python3 -m venv .venv` → `source .venv/bin/activate` | `pip install -r requirements.txt` |

Add `pip install -r requirements-dev.txt` for Jupyter and the PDF builder.

## Run the notebook
`jupyter notebook notebooks/ML_Assignment_2.ipynb` (any OS) → *Kernel → Restart & Run All*; or in VS Code open the notebook, **Select Kernel → `.venv`**, **Run All**.
Switch data source in the Phase 1 cell by commenting Option B and un-commenting Option A (needs internet).

## Train the models (command line, any OS)
`python -m src.train_models` then `python -m src.evaluate_models` (about 17 seconds in our test run).

## Launch Streamlit (any OS)
`streamlit run app.py` (or `python -m streamlit run app.py`) → open http://localhost:8501 → click **Use bundled sample test set** or upload `data/test_data.csv`.

## Upload to GitHub / deploy
Follow `deployment/GITHUB_DEPLOYMENT.md` then `deployment/STREAMLIT_DEPLOYMENT.md`. Then paste the two links into `README.md` (sections d and l) and regenerate the PDF with your details (needs `requirements-dev.txt`). This single line works in **every** shell (PowerShell, cmd, bash, zsh):
```
python tools/build_submission_pdf.py --name "Your Name" --student-id "2026AJxxxxx" --email "you@example.com" --github "https://github.com/Basetti-Shanmugam/ML-Assignment-2-AIML" --app "https://YOUR-APP.streamlit.app" --screenshot screenshots/bits_virtual_lab.png
```
Any option you omit stays as a visible placeholder.

## Viva cheat-sheet (what to be able to explain)
1. Why duplicates are removed *before* the split and why scaling sits *inside* the pipeline (leakage).
2. Why macro-averaged metrics + MCC (class imbalance 6.8:1) and how multiclass AUC is computed (OvR, macro, from `predict_proba`).
3. Why SVM wins on 5 of 6 metrics, yet Logistic Regression has a slightly higher AUC and the gap is within noise.
4. Why KNN's training accuracy is 1.0 (distance weighting) and why Naive Bayes is weakest (correlated features).
5. That the app only loads saved pipelines and evaluates uploaded data - it never retrains.
