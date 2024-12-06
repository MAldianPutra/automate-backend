from app import create_app

app = create_app()

# Vercel requires an 'app' callable
handler = app

if __name__ == '__main__':
    app.run(debug=True)
