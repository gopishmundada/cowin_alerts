from os import environ
from cowin_alerts import create_app

app = create_app(environ.get('FLASK_ENV'))


if __name__ == "__main__":
    app.run(port=8000)
