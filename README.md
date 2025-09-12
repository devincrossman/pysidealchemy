# PySide Alchemy

PySide Alchemy is an experimental desktop application built with **Python 3.13**, **PySide6** (Qt for Python), and **SQLAlchemy**.  
It provides a simple GUI for managing **Products**, **Orders**, and **Users**, with login and role-based access control. It was developed while
learning PySide and SQLAlchemy

---

## 🚀 Features
- GUI built with **PySide6** (Qt widgets).
- Database via **SQLAlchemy**:
  - Default: **SQLite** (local file `database.db`).
  - Optional: **MS SQL Server** (switch by editing `db/base.py`).
- **Products, Orders, and Users** management tabs.
- **Authentication system** with login/logout.
- Role-based access:
  - Any logged-in user can view **Orders**.
  - Only **admins** can view **Users**.
- Menu bar with *About*, *Logout*, and *Quit*.
- **Export Data**: Export the current view to CSV or Excel (.xlsx) format from the "Export" menu.
- Secure tab switching (restricted tabs only open after successful login).

---

## 📦 Requirements
- Python **3.13** (older versions may work, but this is the tested version).
- [uv](https://github.com/astral-sh/uv) (modern Python package/dependency manager).
- A supported database engine:
  - SQLite (default, works out of the box).
  - Microsoft SQL Server (requires drivers, see below).

Install `uv` if you don’t have it yet:

```
pip install uv
```

## 🔧 Setup
Clone this repo and install dependencies:

```
git clone https://github.com/devincrossman/pysidealchemy.git
cd pysidealchemy
uv sync
```

This will:

- Create a virtual environment.
- Install dependencies from `pyproject.toml`.
- Pin exact versions from `uv.lock` for reproducibility.

## ▶️ Running the app
```
uv run python main.py
```

The main window will open with tabs for **Products**, **Orders**, and **Users**.

- Products tab: always accessible.
- Orders tab: requires login.
- Users tab: requires admin login.

## 🔑 Authentication
- A login dialog pops up when you try to access restricted tabs.
- If you log out, access to Orders/Users is disabled until you log in again.
- User roles are stored in the `users` table in the database.

## 🗄️ Database Backends
PySide Alchemy supports both SQLite and MS SQL Server.

- SQLite (default)
    - Stores data locally in `database.db`.
    - Easiest to use, no setup required.
- MS SQL Server
    - Open `db/base.py`.
    - Comment out the SQLite connection line.
    - Uncomment the MSSQL connection line and update the connection string.

## 📂 Project Structure
```
pysidealchemy/
├── main.py              # Entry point for the app
├── database.db          # SQLite database file (auto-created if missing)
├── db/                  # Database setup and models
│   ├── base.py          # Database engine setup (SQLite or MSSQL)
│   ├── create_db.py     # Creates tables on startup
│   └── models/          # Table definitions
│       ├── products.py
│       ├── orders.py
│       └── users.py
├── models_qt/           # Qt table models (bridge between DB and UI)
│   ├── products_model.py
│   ├── orders_model.py
│   └── users_model.py
├── services/            # Business logic / services
│   └── auth_service.py  # Authentication & authorization logic
├── ui/                  # GUI components
│   ├── main_window.py   # Main application window
│   ├── secure_tab_bar.py# Custom tab bar to enforce auth before switching
│   ├── login_dialog.py  # Login popup
│   ├── products_view.py # Products tab
│   ├── orders_view.py   # Orders tab
│   └── users_view.py    # Users tab
├── utils/               # Helpers/config
│   └── config.py
├── pyproject.toml       # Project metadata & dependencies
├── PySideAlchemy.spec   # PyInstaller spec file
├── uv.lock              # Locked dependencies for reproducible installs
├── .env                 # Local environment variables (ignored by git)
└── .env.example         # Example env file for sharing
```
## ⚙️ Tools
### uv
PySideAlchemy uses [uv](https://github.com/astral-sh/uv) instead of pip/venv/poetry.
`uv` is a fast, modern tool for Python dependency management.

Common commands:

- `uv sync` → install dependencies into a virtual environment.
- `uv run python main.py` → run the app inside that environment.
- `uv add package` → add a new dependency.
- `uv pip list` → list installed packages.

### Ruff
Code style and linting are enforced with [ruff](https://docs.astral.sh/ruff/).

Run lint checks:

```
uv run ruff check .
```
Auto-fix simple issues:

```
uv run ruff check . --fix
```

### PyInstaller
The application can be built into an exe using PyInstaller.

Run `pyinstaller pysidealchemy.spec` to generate the exe in the dist folder

### Testing
This project uses `pytest` for testing. To run the test suite:

```
uv run pytest
```

This command will automatically discover and run all tests in the `tests/` directory.

## 🌱 Development Notes
- To reset the app, delete database.db and rerun — it will recreate tables.
- Environment variables go in .env. Use .env.example as a template.
- For MSSQL, ensure you install the correct ODBC driver.
- Code style: follow ruff recommendations.
