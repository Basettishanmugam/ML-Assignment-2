# Publishing the project to GitHub (manual steps)

> Nothing has been uploaded for you. Follow these steps with your own account. Never commit `kaggle.json`, tokens or `.env` files (already in `.gitignore`).
> The whole project is ~20 MB; the largest file is the 3 MB Excel dataset, far below GitHub's 100 MB limit.

## 1. Create a GitHub account (skip if you have one)
1. Go to https://github.com/signup, enter email, password, username; verify the email.
2. (Recommended) enable two-factor authentication under *Settings → Password and authentication*.

## 2. Create an empty repository
1. Click **+ → New repository**.
2. Repository name: `ML_Assignment_2` (or similar). Visibility: **Public** (Streamlit Community Cloud's free tier needs access to the repo; public is simplest, and your evaluator can open it).
3. **Do NOT** tick "Add a README", ".gitignore" or "license" (the project already has them - this avoids merge conflicts).
4. Click **Create repository** and copy the HTTPS URL, e.g. `https://github.com/Basetti-Shanmugam/ML-Assignment-2-AIML.git`.

## 3. Install and configure Git (once)
```bash
git --version                                   # if missing: https://git-scm.com/downloads
git config --global user.name  "Your Name"
git config --global user.email "your-github-email@example.com"
```

## 4. Initialise, commit and push

**About commit history.** Your faculty guide asks for a *genuine* sequence of commits and says not to manufacture history after finishing a project.
Splitting finished work into fake "milestones", back-dating commits or reusing generic messages would misrepresent how you worked, so this guide does not do that.
Commit when you *really* complete a step, with a message describing that step.

**Your repository already exists and is not empty** (`https://github.com/Basetti-Shanmugam/ML-Assignment-2-AIML` has one commit with a `README.md` and `.gitignore`), so do **not** run `git init`;
clone it, copy the project in, and work from the clone:
```bash
git clone https://github.com/Basetti-Shanmugam/ML-Assignment-2-AIML.git
cd ML-Assignment-2-AIML
```
Now copy the **contents** of the unzipped `ML_Assignment_2` folder into this `ML-Assignment-2-AIML` folder, overwriting the existing `README.md` and `.gitignore`.
Include hidden items (`.gitignore`, `.streamlit/`, `.gitattributes`). Pick your shell (replace the paths):

| Shell | Command |
|---|---|
| Windows PowerShell / cmd | `robocopy "<unzipped-folder>\ML_Assignment_2" "<your-repo-folder>" /E` (exit codes 0-7 mean success) |
| Windows PowerShell (alternative) | `Copy-Item "<unzipped-folder>\ML_Assignment_2\*" "<your-repo-folder>" -Recurse -Force` |
| macOS / Linux | `cp -a /path/to/unzipped/ML_Assignment_2/. /path/to/ML-Assignment-2-AIML/` |
| Any OS, no terminal | File Explorer / Finder drag-and-drop with "Show hidden items" turned on |

All other git commands in this guide are identical on every OS, and GitHub Desktop has Commit/Push buttons for the same steps. The Windows warning *"LF will be replaced by CRLF"* is harmless.
```bash
git status                                      # check: files listed, no kaggle.json / secrets
```

**If you are still working through the project (recommended):** run, read and adapt each part yourself, and commit after each real step, e.g.
```bash
git add README.md requirements.txt .gitignore config.py data
git commit -m "Initial project setup and dataset selection"           # when you have chosen/checked the dataset
git add src/data_loader.py src/preprocessing.py notebooks
git commit -m "Add dataset exploration and preprocessing"             # after you ran and understood the EDA
git add src/train_models.py
git commit -m "Implement the five classifiers as scikit-learn pipelines"
git add src/evaluate_models.py src/visualization.py reports
git commit -m "Add evaluation metrics, comparison table and observations"
git add models data/test_data.csv
git commit -m "Save trained pipelines and held-out test data"
git add app.py .streamlit
git commit -m "Add Streamlit evaluation application"
git add deployment tests tools PROJECT_OVERVIEW.md SUBMISSION_CHECKLIST.md screenshots submission
git commit -m "Add deployment documentation and tests"
git push -u origin main
```
Only commit a step after you have really done it; edit the messages so they describe what *you* changed.

**If you are submitting the finished project as it is:** use one honest commit and then record the genuine later changes as separate commits.
```bash
git add .
git commit -m "Add complete Dry Bean classification project (notebook, models, Streamlit app)"
git push -u origin main
# ...later, each genuinely separate change:
git add README.md && git commit -m "Add GitHub and Streamlit links to README" && git push
```
**Authentication:** GitHub no longer accepts account passwords for `git push`. When prompted, use your username and a **Personal Access Token** as the password
(*Settings → Developer settings → Personal access tokens → Fine-grained → repository access to this repo, permission "Contents: Read and write"*), or install the GitHub CLI and run `gh auth login`, or use Git Credential Manager (bundled with Git for Windows).

## 5. Verify
1. Refresh the repository page: you should see `app.py`, `requirements.txt`, `models/`, `src/`, `data/`, `notebooks/` etc. and the README rendered with tables and the comparison image.
2. Open `models/` - the five `.joblib` files must be listed (if they are missing, check they are not excluded by `.gitignore`).
3. Open the notebook on GitHub - outputs should render.
4. Optional full test: clone into a new folder and run it
```bash
git clone https://github.com/Basetti-Shanmugam/ML-Assignment-2-AIML.git test_clone && cd test_clone
python -m venv .venv
# activate: Windows PowerShell  .venv\Scripts\Activate.ps1  |  cmd  .venv\Scripts\activate.bat  |  macOS/Linux  source .venv/bin/activate
pip install -r requirements.txt
python tests/run_checks.py
```
5. Paste the repository URL into README section **d** and commit it as its own change:
```bash
git add README.md && git commit -m "Add GitHub repository link to README" && git push
```

## Troubleshooting
| Problem | Fix |
|---|---|
| `fatal: not a git repository` | Run `git init -b main` inside the project folder |
| `remote origin already exists` | `git remote set-url origin <URL>` |
| `Authentication failed` | Use a Personal Access Token (not your password) or `gh auth login` |
| `rejected ... fetch first` | You created the repo with a README: `git pull origin main --rebase` then push |
| Large-file warning | Not expected here; never commit raw Kaggle zips >50 MB |
