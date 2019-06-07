from flask import jsonify
from flask import make_response
from flask import request
from flask_restful import Resource
from sqlalchemy import exc as sql_exc

from common.utils import NotJsonFileError
from common.utils import ValidationError
from models.fruit_model import FruitModel


class Fruits(Resource):
    def get(self):
        """
        Get all records from the database
        :return: response of the request
        :rtype: Response
        """
        try:
            records = FruitModel.get_all_records()
            if not records:
                response = make_response(jsonify({"message": "No records found"}), 404)
            else:
                response = make_response(jsonify([record.json() for record in records]))
        except Exception as exc:
            response = make_response(
                jsonify({"message": f"Server error occurred: {exc}"}), 500)

        return response

    def post(self):
        """
        Add records to the database
        :return: response of the request
        :rtype: Response
        :raises: NotJsonFileError if data is not a json format
        """
        try:
            if not request.is_json:
                raise NotJsonFileError()

            data = request.get_json()
            fruits_models = []
            for record in data:
                FruitModel.data_validation(record)
                fruit_model = FruitModel(**record)
                fruit_model.save_to_db()
                fruits_models.append(fruit_model.json())
            response = make_response(jsonify([record for record in fruits_models]), 201)
        except NotJsonFileError:
            response = make_response(jsonify({"message": "No JSON received"}), 400)
        except ValidationError as exc:
            response = make_response(
                jsonify({"message": f"An error occurred: {exc}"}), 400)
        except sql_exc.StatementError:
            response = make_response(
                jsonify({"message": "Wrong value type for provided key/keys"}), 400)
        except Exception as exc:
            response = make_response(
                jsonify({"message": f"Server error occurred: {exc}"}), 500)

        return response
