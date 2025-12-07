import pytest
from tinydb import TinyDB, Query
from tinydb.storages import MemoryStorage

from flask import session
from flask_todo import create_app, routes


@pytest.fixture()
def client(monkeypatch):
    # Use in-memory TinyDB to keep tests isolated
    test_db = TinyDB(storage=MemoryStorage)
    monkeypatch.setattr(routes, "db", test_db)

    app = create_app()
    app.config["TESTING"] = True

    test_client = app.test_client()
    session.clear()
    yield test_client

    session.clear()
    test_db.close()


def _set_csrf_token(client, token="test-token"):
    session["_csrf_token"] = token
    return token


def test_main_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200


def test_add_task(client):
    csrf_token = _set_csrf_token(client)

    response = client.post(
        "/add",
        data={"title": "New Task", "csrf_token": csrf_token},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert any(task["title"] == "New Task" for task in routes.db.all())


def test_delete_task(client):
    task_id = 123
    routes.db.insert({"id": task_id, "title": "Delete Me", "complete": False})
    csrf_token = _set_csrf_token(client)

    response = client.post(
        f"/delete/{task_id}", data={"csrf_token": csrf_token}, follow_redirects=True
    )

    assert response.status_code == 200
    assert routes.db.search(Query().id == task_id) == []
