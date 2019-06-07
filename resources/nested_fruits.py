from flask import jsonify
from flask import make_response
from flask_restful import Resource
from flask_restful import reqparse

from common.json_parser import JsonParser
from common.utils import ValidationError
from models.fruit_model import FruitModel


class NestedFruits(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('key', action='append', location='args')

    def get(self):
        """
        Get a parsed json data based on provided keys in parameters
        :return: response of the request
        :rtype: Response
        :raises: ValidationError if no keys have been provided
        :raises: KeyError if provided key does not exist in the data
        """
        try:
            args = NestedFruits.parser.parse_args()
            keys = args['key']
            if keys is None:
                raise ValidationError()
            unique_keys = JsonParser.remove_duplicate_keys(keys)

            data = FruitModel.get_all_records()
            data_json = [record.json() for record in data]

            json_parser = JsonParser(unique_keys, data_json)
            json_parser.create_output()
            response = make_response(jsonify(json_parser.output_data))
        except ValidationError:
            response = make_response(
                jsonify({"message": f"Missing keys in request params"}), 400)
        except KeyError as exc:
            response = make_response(
                jsonify({"message": f"Provided key {exc} does not exists in database"}), 400)
        except Exception as exc:
            response = make_response(
                jsonify({"message": f"Server error occurred: {exc}"}), 500)

        return response
