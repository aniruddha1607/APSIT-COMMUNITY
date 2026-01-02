# Running APSIT-COMMUNITY locally

This document describes the exact steps to get the project running locally on macOS (zsh). It includes cloning the repo, creating a virtual environment, installing the minimal requirements we use for development, running the Flask app, and inspecting the SQLite database.

---

## Prerequisites
- Python 3.8+ installed. (If you need Python 3.11 for certain projects, see the `pyenv` note below.)
- Git
- Optional but helpful: VS Code with the "SQLite" extension by alexcvzz (for browsing `campus.db`).


## 1) Clone the repo
```bash
# pick a directory where you want the project
git clone https://github.com/aniruddha1607/APSIT-COMMUNITY.git
cd APSIT-COMMUNITY
```

## 2) Create & activate a Python virtual environment (recommended)
```bash
# create venv in project root
python3 -m venv venv
# activate (zsh)
source venv/bin/activate
```

If you prefer a different location for the venv, change the path accordingly.

## 3) Install the minimal dependencies
We created `requirements-minimal.txt` which contains only the runtime packages the app imports. Install them into the activated venv:

```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements-minimal.txt
```

If you want the original (larger) `requirements.txt`, you can install that instead — but we removed problematic/incorrect entries (like `turtle`) from the original to avoid pip errors.

If pip fails with a "Requires-Python >=3.11" message for a specific package, either install that package at a compatible version or use Python 3.11 (see the `pyenv` note below).

## 4) Set Flask environment variables and run
Option A — Flask CLI (recommended during development)
```bash
export FLASK_APP=app.py
export FLASK_ENV=development   # optional: enables debug & auto-reload
flask run --host=127.0.0.1 --port=5000
```

Option B — run the script directly (works because `app.py` has `app.run(debug=True)` at the bottom)
```bash
python3 app.py
```

Open in your browser: http://127.0.0.1:5000 or http://localhost:5000

<!-- Use the followin accounts to play around in the app -->
username - 20102145@apsit.edu.in
password - 1234

username - 20102002@apsit.edu.in
password - 1234

Notes:
- The root route currently redirects unauthenticated users to `/login`.
- Registration requires an email matching the pattern `\b[0-9]+@apsit.edu.in` (the code validates that). For local testing you can either register with such an email or temporarily relax that check in `app.py`.

## 5) Inspect the database (`campus.db`)
Stop the Flask server before making writes to the DB. Make a backup first:

```bash
cp campus.db campus.db.bak
```

### Using the command-line (sqlite3)
```bash
# open an interactive shell
sqlite3 campus.db
# inside sqlite3:
.tables
PRAGMA table_info('users');
SELECT * FROM users LIMIT 10;
.exit
```

### Using VS Code (SQLite extension by alexcvzz)
1. Install the extension.
2. In the SQLite panel click "Open Database" and choose `campus.db`.
3. Expand `Tables` → right‑click a table (e.g. `users`) → "Open Table" to see columns and rows.

### Quick script (already included)
We've added `scripts/db_inspect.py` which prints:
- list of tables
- schema for `users`
- row-count and first 20 rows

Run it:
```bash
python3 scripts/db_inspect.py
```

## 6) Common troubleshooting
- "ModuleNotFoundError": ensure the venv is activated and you installed the requirements file into that venv.
- "Could not find a version that satisfies the requirement turtle": `turtle` is part of the Python stdlib and should not be installed; we've removed it from `requirements.txt`.
- "Requires-Python >=3.11": install Python 3.11 (pyenv is recommended) or adjust the package versions.

## 7) Optional: Install Python 3.11 with pyenv (if needed)
If you see package wheel incompatibilities requiring Python 3.11, install `pyenv` and create a venv using Python 3.11:

```bash
# install pyenv via Homebrew
brew update
brew install pyenv
# install Python 3.11 (example version)
pyenv install 3.11.6
pyenv local 3.11.6   # sets the Python version for this folder
# recreate venv using pyenv's Python
python -m venv venv
source venv/bin/activate
pip install -r requirements-minimal.txt
```

## 8) Notes about credentials & mailing
`app.py` currently contains these values:
```python
my_email = "pythonisez@yahoo.com"
password = "jdqsxomgcvrttjvi"
```
These appear to be real credentials (or placeholders). For security:
- Replace them with your own sender email and app password OR
- Use environment variables and python-dotenv to load secrets (recommended). Example:

```bash
export MY_EMAIL="you@example.com"
export MY_EMAIL_PASSWORD="your_password"
```
Then modify `app.py` to read from `os.environ`.

## 9) Making the index publicly visible for local testing
If you want the root (`/`) to render the index page without login during local testing, find `get_all_posts()` in `app.py` and temporarily remove or comment out the `if current_user.is_authenticated` check. Don't keep this change in production.

## 10) Contact / Next steps
If you get errors while installing or running, copy the full terminal traceback and paste it. I can:
- help pin package versions for a different Python version,
- update `requirements-minimal.txt` further,
- add a `.env` example and update `app.py` to read secrets from environment variables.

---

Happy hacking — run the app and let me know any errors you hit and I will help fix them.
