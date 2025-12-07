# Flask TODO Application

## Introduction
This repository contains a lightweight to-do list web application built with [Flask](https://flask.palletsprojects.com/) and [TinyDB](https://tinydb.readthedocs.io/). The app lets you add tasks, edit their titles, mark them complete, and delete them—all stored in a simple JSON file for easy local development or demos.

## Project Structure
```
Flask-TODO-APP/
├── app.py             # Application factory and entry point
├── routes.py          # Blueprint with all task routes
├── templates/
│   └── index.html     # Single-page UI for the to-do list
├── db.json            # TinyDB data store (created automatically)
├── screenshot/        # Example screenshots of the UI
└── tests/             # Pytest-based smoke tests
```

## Components
- **`app.py`** – Defines `create_app()` to initialize the Flask instance and register the routes blueprint; running the file directly starts the development server with reloading enabled. 【F:app.py†L1-L10】
- **`routes.py`** – Declares the `todo` blueprint and all task-related endpoints: render the list, add new tasks, update titles, delete items, and mark tasks complete. TinyDB persists each task with an `id`, `title`, and `complete` flag. 【F:routes.py†L1-L34】
- **`templates/index.html`** – Renders the UI using W3.CSS styling. It lists current tasks, shows completion state, and includes forms/buttons for add, edit (popup), complete, and delete actions. A small script handles the live clock and pre-fills the edit popup. 【F:templates/index.html†L15-L107】
- **`db.json`** – JSON file created by TinyDB to store tasks. Deleting it resets the app’s data.
- **`tests/`** – Placeholder for automated tests (none required to run the app).

## Prerequisites
- Python 3.8 or newer
- `pip` for installing dependencies

## Setup Instructions
1. **Clone the repository**
   ```bash
   git clone https://github.com/your-user/Flask-TODO-APP.git
   cd Flask-TODO-APP
   ```
2. **(Optional) Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
3. **Install dependencies**
   ```bash
   pip install flask tinydb
   ```

## Running the Application
Start the Flask development server:
```bash
python app.py
```
Then open `http://127.0.0.1:5000/` in your browser to access the to-do list.

## How the App Works
1. **Render the list (`GET /`)** – Fetches all tasks from TinyDB and renders `index.html` with the list. 【F:routes.py†L9-L13】
2. **Add a task (`POST /add`)** – Submits a title from the form; assigns a random integer `id`, sets `complete=False`, stores in TinyDB, and redirects back to the list. 【F:routes.py†L15-L18】
3. **Mark complete (`POST /complete/<id>`)** – Updates the `complete` flag to `True` for the given task. 【F:routes.py†L30-L33】
4. **Edit a task (`POST /update`)** – The popup fills current text and task ID into hidden/input fields; the route updates the title in TinyDB. 【F:routes.py†L20-L25】【F:templates/index.html†L70-L105】
5. **Delete a task (`POST /delete/<id>`)** – Removes the matching record from TinyDB. 【F:routes.py†L26-L29】
6. **Front-end behavior** – Tasks are styled differently when complete, and the page shows a live datetime stamp. Buttons trigger form submissions or open the edit popup. 【F:templates/index.html†L37-L107】

## Development Notes
- The server runs with `debug=True` for automatic reloads during development. 【F:app.py†L7-L10】
- All data lives in `db.json`; you can clear this file to reset the task list.
- The app uses plain Flask and TinyDB with no additional build steps, so it is easy to experiment with.

## Screenshots
See the `screenshot/` directory for example images of the UI.
