# Setup and run commands for every operating system

Pick **your** operating system / shell below and copy the commands in order. All commands are run **from the project root**
(the folder that contains `app.py` and `requirements.txt`). In VS Code open it with **File → Open Folder**, then **Terminal → New Terminal**.

**Requirements:** Python **3.11 or newer** (3.12 recommended and used for testing). scikit-learn 1.8 and the pinned numpy/pandas versions do not install on Python 3.10 or older.

> Tested environment: Linux, Python 3.12. The Windows and macOS commands below use standard tooling and the project uses `pathlib` and explicit UTF-8 file handling,
> but they were **not executed on Windows or macOS** by the author of this package - if one fails, see the troubleshooting table at the end.

## Which command starts Python?

| OS | Check the version | Command to create the environment |
|---|---|---|
| Windows | `py --version` (or `python --version`) | `py -3.12 -m venv .venv` (or `python -m venv .venv`) |
| macOS | `python3 --version` | `python3 -m venv .venv` |
| Linux (Ubuntu/Debian) | `python3 --version` | `python3 -m venv .venv` (if it fails: `sudo apt install python3-venv`) |

Install Python from https://www.python.org/downloads/ if needed. On Windows tick **"Add python.exe to PATH"** in the installer.
`py -0` lists the Python versions installed on Windows.

---

## Windows - PowerShell (default VS Code terminal)

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```
If activation says *"running scripts is disabled on this system"*, run this once and retry:
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```
Leave the environment with `deactivate`.

## Windows - Command Prompt (cmd)

```bat
py -3.12 -m venv .venv
.venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

## Windows - Git Bash

```bash
py -3.12 -m venv .venv
source .venv/Scripts/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

## macOS (Terminal / zsh)

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

## Linux (Ubuntu / Debian / Fedora ...)

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

You know the environment is active when the prompt starts with `(.venv)`.
The app opens at **http://localhost:8501** - click **Use bundled sample test set** or upload `data/test_data.csv`. Stop it with **Ctrl + C**.

---

## Commands that are identical on every OS (after activating `.venv`)

| What | Command |
|---|---|
| Train and save the five models | `python -m src.train_models` |
| Metrics, reports, confusion matrices, figures | `python -m src.evaluate_models` |
| EDA figures only | `python -m src.visualization` |
| Run all automated checks (writes `reports/TESTING_REPORT.md`) | `python tests/run_checks.py` |
| Start the Streamlit app | `streamlit run app.py` |
| Start the app if `streamlit` is "not recognized" | `python -m streamlit run app.py` |
| Start the app on another port | `streamlit run app.py --server.port 8502` |
| Install notebook extras (Jupyter etc.) | `pip install -r requirements-dev.txt` |
| Open the notebook in a browser | `jupyter notebook notebooks/ML_Assignment_2.ipynb` |
| Rebuild README / guides from the results | `python tools/build_docs.py` |
| Rebuild the notebook (then re-execute it) | `python tools/build_notebook.py` |

**Notebook in VS Code instead:** open `notebooks/ML_Assignment_2.ipynb`, click **Select Kernel** (top right) → **Python Environments** → choose `.venv`, then **Run All**.

---

## Regenerate the submission PDF with your details

Needs `pip install -r requirements-dev.txt`. The one-line form works in **every** shell:

```
python tools/build_submission_pdf.py --name "Basetti Shanmugam" --student-id "2026AJ05044" --email "you@example.com" --github "https://github.com/Basetti-Shanmugam/ML-Assignment-2-AIML" --app "https://YOUR-APP.streamlit.app" --screenshot screenshots/bits_virtual_lab.png
```
Output: `submission/ML_Assignment_2_Submission.pdf` (add `--out some\path.pdf` to choose another location). To split the command over several lines, use the line-continuation character of your shell:
**PowerShell** `` ` `` (backtick) · **cmd** `^` · **bash / zsh** `\`.

---

## Copy the project into your cloned GitHub repository

From the folder where you unzipped `ML_Assignment_2_Complete.zip`; replace the two paths. These commands include hidden files (`.gitignore`, `.streamlit/`, `.gitattributes`).

| Shell | Command |
|---|---|
| Windows PowerShell or cmd | `robocopy "<unzipped-folder>\ML_Assignment_2" "<your-repo-folder>" /E` |
| Windows PowerShell (alternative) | `Copy-Item "<unzipped-folder>\ML_Assignment_2\*" "<your-repo-folder>" -Recurse -Force` |
| macOS / Linux | `cp -a /path/to/unzipped/ML_Assignment_2/. /path/to/ML-Assignment-2-AIML/` |

`robocopy` prints a summary and returns exit codes 0-7 for success (that is normal). Or simply drag everything (with "Show hidden items" on) in File Explorer / Finder.

## Git commands (same on every OS)
```
git status
git add .
git commit -m "Add complete Dry Bean classification project (notebook, models, Streamlit app)"
git push origin <your-branch-name>
```
In **GitHub Desktop** you do the same with the Commit and Push buttons. Warnings such as *"LF will be replaced by CRLF"* on Windows are harmless (`.gitattributes` keeps binary files such as `.joblib` untouched).

---

## Troubleshooting by symptom

| Symptom | OS | Fix |
|---|---|---|
| `python` is not recognized / opens the Microsoft Store | Windows | Use `py` instead, or install Python from python.org with "Add to PATH"; or turn off the *App execution aliases* for python.exe in Windows Settings |
| `running scripts is disabled on this system` | Windows PowerShell | `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`, or use cmd / Git Bash |
| `'streamlit' is not recognized` / `command not found` | all | The environment is not active, or use `python -m streamlit run app.py` |
| `No matching distribution found for scikit-learn==1.8.0` or numpy/pandas | all | Python is older than 3.11: install 3.12 and recreate `.venv` (delete the folder first) |
| `ModuleNotFoundError: No module named 'src'` / `config` | all | You are not in the project root - `cd` to the folder with `app.py` |
| `ModuleNotFoundError: seaborn` (etc.) | all | Activate `.venv`, then `pip install -r requirements.txt`; in VS Code select the `.venv` interpreter (Ctrl+Shift+P → *Python: Select Interpreter*) |
| `Port 8501 is already in use` | all | Close the other Streamlit window or run with `--server.port 8502` |
| `InconsistentVersionWarning` when loading models | all | Install the pinned versions (`pip install -r requirements.txt`) or retrain: `python -m src.train_models` |
| Path too long / odd errors when the project is inside OneDrive | Windows | Move the project to a short local path such as `C:\ML\ML-Assignment-2-AIML` |
| `python3: command not found` | Linux/macOS | Install Python 3 (`sudo apt install python3 python3-venv` or `brew install python@3.12`) |
| Kernel not found / wrong packages in the notebook | all | Select the `.venv` kernel (VS Code) or run `python -m ipykernel install --user --name ml-assignment` |
