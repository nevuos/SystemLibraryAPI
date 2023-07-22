from flask import Flask
from api.auth.routes.auth_routes import auth_bp

app = Flask(__name__)
app.register_blueprint(auth_bp)
