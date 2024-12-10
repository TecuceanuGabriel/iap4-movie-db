from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

from app.config import Config
from app.extensions import mongo
from app.extensions import scheduler

from app.routes.auth import auth
from app.routes.protected import protected
from app.routes.tmdb import tmdb
from app.routes.friends import friends

from app.tasks import clear_friend_reqeuests_task


def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

    mongo.init_app(app)
    scheduler.init_app(app)
    scheduler.start()

    app.register_blueprint(auth)
    app.register_blueprint(protected)
    app.register_blueprint(tmdb)
    app.register_blueprint(friends)

    @app.teardown_appcontext
    def cleanup(exception):
        mongo.cx.close()
        scheduler.shutdown(wait=True)

    return app
