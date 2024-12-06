from app import create_app
import logging

app = create_app()

if __name__ == '__main__':
    logging.basicConfig(filename='error.log', level=logging.DEBUG)
    app.run()