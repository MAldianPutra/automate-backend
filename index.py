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