from flask import Blueprint, render_template, request, redirect, url_for, abort, session
from tinydb import TinyDB, Query
import random

bp = Blueprint('todo', __name__)

db = TinyDB('db.json')


def _validate_csrf():
    session_token = session.get('_csrf_token')
    request_token = request.form.get('csrf_token')
    if not session_token or not request_token or session_token != request_token:
        return abort(400)

@bp.route('/')
def index():
    todo_list = db.all()
    return render_template('index.html', todo_list=todo_list)

@bp.route('/add', methods=['POST'])
def add():
    csrf_response = _validate_csrf()
    if csrf_response:
        return csrf_response
    title = request.form.get('title')
    db.insert({'id': random.randint(0, 1000), 'title': title, 'complete': False})
    return redirect(url_for('todo.index'))

@bp.route('/update', methods=['POST'])
def update():
    csrf_response = _validate_csrf()
    if csrf_response:
        return csrf_response
    todo_db = Query()
    new_text = request.form.get('inputField')
    todo_id = request.form.get('hiddenField')
    db.update({'title': new_text}, todo_db.id == int(todo_id))
    return redirect(url_for('todo.index'))

@bp.route('/delete/<int:todo_id>', methods=['POST'])
def delete(todo_id):
    csrf_response = _validate_csrf()
    if csrf_response:
        return csrf_response
    todo_db = Query()
    db.remove(todo_db.id == todo_id)
    return redirect(url_for('todo.index'))

@bp.route('/complete/<int:todo_id>', methods=['POST'])
def complete(todo_id):
    csrf_response = _validate_csrf()
    if csrf_response:
        return csrf_response
    todo_db = Query()
    db.update({'complete': True}, todo_db.id == todo_id)
    return redirect(url_for('todo.index'))
