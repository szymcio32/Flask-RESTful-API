import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from flask import Flask
from flask_restful import Api

from common.utils import setup_logging
from resources.fruit import Fruit
from resources.fruits import Fruits
from resources.nested_fruits import NestedFruits


app = Flask(__name__)
app.secret_key = "dev"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)

api.add_resource(Fruits, "/api/v1/fruits")
api.add_resource(Fruit, "/api/v1/fruit/<int:_id>")
api.add_resource(NestedFruits, "/api/v1/fruit/nest")


if __name__ == "__main__":
    @app.before_first_request
    def create_tables():
        db.create_all()

    from db import db
    setup_logging()
    db.init_app(app)
    app.run(port=5000, host="0.0.0.0")
