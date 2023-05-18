from flask_migrate import Migrate
from api import create_app
from api.utils.configurations.extensions import db

app = create_app()

migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run()
