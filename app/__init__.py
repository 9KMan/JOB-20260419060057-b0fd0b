import os
from flask import Flask
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from app.models import Base

engine = create_engine(os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/carwash_crm"))
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

def create_app():
    app = Flask(__name__)
    CORS(app)

    from app.routes import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    @app.teardown_appcontext
    def cleanup(resp_or_exc):
        Session.remove()

    return app