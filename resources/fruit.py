from flask import jsonify
from flask import make_response
from flask import request
from flask_restful import Resource
from sqlalchemy import exc as sql_exc

from common.utils import NotJsonFileError
from common.utils import RecordNotFound
from common.utils import ValidationError
from models.fruit_model import FruitModel


class Fruit(Resource):
    def get(self, _id):
        """
        Get a record from the database based on provided ID
        :return: response of the request
        :rtype: Response
        """
        try:
            record = FruitModel.find_by_id(_id)
            if record:
                response = make_response(jsonify(record.json()))
            else:
                response = make_response(
                    jsonify({"message": f"Provided record with id: {_id} does not exists"}), 404)
        except Exception as exc:
            response = make_response(
                jsonify({"message": f"Server error occurred: {exc}"}), 500)

        return response

    def put(self, _id):
        """
        Update a record in the database based on provided ID
        :return: response of the request
        :rtype: Response
        :raises: NotJsonFileError if data is not a json format
        """
        try:
            if not request.is_json:
                raise NotJsonFileError()

            data = request.get_json()
            record = FruitModel.find_by_id(_id)

            FruitModel.data_validation(data)
            if record:
                record.update(data)
            else:
                record = FruitModel(**data)
            record.save_to_db()
            response = make_response(jsonify(record.json()))
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

    def delete(self, _id):
        """
        Delete a record from the database based on provided ID
        :return: response of the request
        :rtype: Response
        :raises: RecordNotFound if record has not been found
        """
        try:
            record = FruitModel.find_by_id(_id)
            if not record:
                raise RecordNotFound()

            record.delete_from_db()
            response = make_response(jsonify({"message": f"Record with id: {_id} has been deleted"}))
        except RecordNotFound:
            response = make_response(
                jsonify({"message": f"Provided record with id: {_id} does not exists"}), 404)
        except Exception as exc:
            response = make_response(
                jsonify({"message": f"Server error occurred: {exc}"}), 500)

        return response

