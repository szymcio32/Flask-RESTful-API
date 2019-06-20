import json
import os
import unittest

from unittest.mock import MagicMock

from common.json_parser import JsonParser


class TestJsonParser(unittest.TestCase):
    """Class responsible for testing JsonParser class"""
    DATA_PATH = "resources/data.json"
    JSON_KEYS = ['currency', 'country', 'city', 'fruit']

    # expected output files
    CURRENCY_COUNTRY_CITY_FRUIT_FILE_1 = "resources/currency_country_city_fruit_output_1.json"
    CURRENCY_COUNTRY_CITY_FRUIT_FILE_2 = "resources/currency_country_city_fruit_output_2.json"
    CURRENCY_COUNTRY_CITY_FRUIT_FILE_3 = "resources/currency_country_city_fruit_output_3.json"
    COUNTRY_CURRENCY_FILE = "resources/country_currency_output.json"
    COUNTRY_FILE = "resources/country_output.json"

    @classmethod
    def setUpClass(cls):
        """Load json data to be tested"""
        file_full_path = cls.get_full_path(cls.DATA_PATH)
        cls.DATA = cls.load_json_file(file_full_path)

    def setUp(self):
        """Setup method for all test methods"""
        self.json_parser = JsonParser(self.JSON_KEYS, self.DATA)

    def test_init(self):
        """Test init method"""
        self.assertEqual(self.JSON_KEYS, self.json_parser.json_keys)
        self.assertEqual(len(self.JSON_KEYS), self.json_parser.keys_length)
        self.assertEqual(self.DATA, self.json_parser.input_data)
        self.assertIsInstance(self.json_parser.input_data, list)
        self.assertEqual({}, self.json_parser._output_data)

    def test_output_data(self):
        """Test if output_data method returns correct data"""
        return_value = self.json_parser.output_data

        self.assertEqual(self.json_parser._output_data, return_value)

    def test_get_json_input(self):
        """Test if get_json_input method returns correct data"""
        expected = ['USD', 'US', 'Boston', 'apple']

        return_value = self.json_parser._get_json_input(self.DATA[0])
        self.assertEqual(expected, return_value)

    def test_create_output(self):
        """Test if create_output method invokes correct methods"""
        self.json_parser._get_json_input = MagicMock()
        self.json_parser._get_leaf_dictionaries = MagicMock()
        self.json_parser._update_data_with_single_row = MagicMock()

        self.json_parser.create_output()

        input_data_length = len(self.json_parser.input_data)
        self.assertEqual(input_data_length, self.json_parser._get_json_input.call_count)
        self.assertEqual(input_data_length, self.json_parser._get_leaf_dictionaries.call_count)
        self.assertEqual(input_data_length, self.json_parser._update_data_with_single_row.call_count)

    def test_get_leaf_dictionaries(self):
        """Test if get_leaf_dictionaries method returns correct data"""
        expected = {"price": self.DATA[0]['price']}

        return_value = self.json_parser._get_leaf_dictionaries(self.DATA[0])

        self.assertEqual(expected, return_value)

        # different input
        self.json_parser.json_keys = ['country', 'city', 'id']
        self.json_parser.keys_length = len(self.json_parser.json_keys)
        expected = {
            "currency": self.DATA[0]['currency'],
            "fruit": self.DATA[0]['fruit'],
            "price": self.DATA[0]['price']
        }

        return_value = self.json_parser._get_leaf_dictionaries(self.DATA[0])

        self.assertEqual(expected, return_value)

    def test_update_data_with_single_row_returns_correct_output_1(self):
        """Test if update_data_with_single_row method returns correct data"""
        file = self.get_full_path(self.CURRENCY_COUNTRY_CITY_FRUIT_FILE_1)
        first_dict = self.load_json_file(file)
        file = self.get_full_path(self.CURRENCY_COUNTRY_CITY_FRUIT_FILE_2)
        second_dict = self.load_json_file(file)
        file = self.get_full_path(self.CURRENCY_COUNTRY_CITY_FRUIT_FILE_3)
        third_dict = self.load_json_file(file)
        expected = [first_dict, second_dict, third_dict]

        data = {}
        for index, row in enumerate(self.DATA):
            json_keys_data = self.json_parser._get_json_input(row)
            leaf_dictionaries = self.json_parser._get_leaf_dictionaries(row)
            self.json_parser._update_data_with_single_row(json_keys_data, data, leaf_dictionaries)
            self.assertEqual(expected[index], data)

    def test_update_data_with_single_row_returns_correct_output_2(self):
        """Test if update_data_with_single_row method returns correct data with only 2 provided keys"""
        self.json_parser.json_keys = ['country', 'currency']
        self.json_parser.keys_length = len(self.json_parser.json_keys)
        file = self.get_full_path(self.COUNTRY_CURRENCY_FILE)
        expected = self.load_json_file(file)

        data = {}
        for row in self.DATA:
            json_keys_data = self.json_parser._get_json_input(row)
            leaf_dictionaries = self.json_parser._get_leaf_dictionaries(row)
            self.json_parser._update_data_with_single_row(json_keys_data, data, leaf_dictionaries)

        self.assertEqual(expected, data)

    def test_update_data_with_single_row_returns_correct_output_3(self):
        """Test if update_data_with_single_row method returns correct data with only 1 provided key"""
        self.json_parser.json_keys = ['country']
        self.json_parser.keys_length = len(self.json_parser.json_keys)
        file = self.get_full_path(self.COUNTRY_FILE)
        expected = self.load_json_file(file)

        data = {}
        for row in self.DATA:
            json_keys_data = self.json_parser._get_json_input(row)
            leaf_dictionaries = self.json_parser._get_leaf_dictionaries(row)
            self.json_parser._update_data_with_single_row(json_keys_data, data, leaf_dictionaries)

        self.assertEqual(expected, data)

    def test_remove_duplicate_keys_returns_correct_value(self):
        """Test if remove_duplicate_keys returns correct value"""
        expected = ['country', 'city']

        return_value = self.json_parser.remove_duplicate_keys(expected)

        self.assertEqual(expected, return_value)

    def test_remove_duplicate_keys_returns_correct_value_when_duplicated_keys_provided(self):
        """Test if remove_duplicate_keys returns correct value when duplicated keys provided"""
        keys = ['country', 'city', 'city', 'currency', 'country']
        expected = ['country', 'city', 'currency']

        return_value = self.json_parser.remove_duplicate_keys(keys)

        self.assertEqual(expected, return_value)

    @staticmethod
    def load_json_file(json_file):
        """Helper method responsible for loading json file"""
        with open(json_file) as file:
            data = json.load(file)
        return data

    @staticmethod
    def get_full_path(file):
        """Helper method responsible for getting a full path to file"""
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_full_path = os.path.join(dir_path, file)
        return file_full_path

