# import sys
# from os.path import dirname, abspath

# # Add the parent directory to the system path
# sys.path.append(dirname(dirname(abspath(__file__))))

# from app import create_app

# app = create_app()

# # Vercel requires an 'app' callable
# handler = app

from flask import Flask

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def hello():
        return "Hello, World!"

    return app

app = create_app()

# Vercel requires an 'app' callable
handler = app
