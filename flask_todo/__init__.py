from flask import Flask, session
import os
import secrets


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')

    def generate_csrf_token():
        token = session.get('_csrf_token')
        if not token:
            token = secrets.token_hex(16)
            session['_csrf_token'] = token
        return token

    app.jinja_env.globals['csrf_token'] = generate_csrf_token

    from .routes import bp

    app.register_blueprint(bp)

    return app
