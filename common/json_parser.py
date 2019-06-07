SUCCESS = 0
FAILURE = 1


class JsonParser:
    """
    Class responsible for parsing json input
    """
    def __init__(self, json_keys, input_data):
        """
        Method responsible for initializing the instance of JsonParser class
        :param json_keys: keys which will be used to get the data
        :type json_keys: list
        :param input_data: data to be parsed
        :type input_data: list
        """
        self.json_keys = json_keys
        self.keys_length = len(json_keys)

        self.input_data = input_data
        self._output_data = {}

    @property
    def output_data(self):
        """
        Method responsible for returning the parsed data
        :return: parsed json data
        :rtype: dict
        """
        return self._output_data

    def create_output(self):
        """
        Method responsible for creating a json data
        """
        for row in self.input_data:
            # linking output data to current dictionary
            current_data = self._output_data
            single_json_keys_data = self._get_json_input(row)
            leaf_dictionaries = self._get_leaf_dictionaries(row)
            self._update_data_with_single_row(single_json_keys_data, current_data, leaf_dictionaries)

    def _get_json_input(self, row):
        """
        Method responsible for filtering data using provided json keys
        :param row: row of json data
        :type row: dict
        :return: filtered data using provided keys
        :rtype: list
        """
        json_inputs = [row[key] for key in self.json_keys]

        return json_inputs

    def _get_leaf_dictionaries(self, row):
        """
        Method responsible for retrieving leaf_dictionaries from single data row
        :param row: row of json data
        :type row: dict
        :return: leaf_dictionaries for specific row
        :rtype: dict
        """
        leaf_dictionaries = {key: value for key, value in row.items()
                             if key not in self.json_keys}
        if "id" in leaf_dictionaries:
            del leaf_dictionaries["id"]

        return leaf_dictionaries

    def _update_data_with_single_row(self, single_json_keys_data, current_data, leaf_dictionaries):
        """
        Method responsible for updating base dictionary data
        :param single_json_keys_data: single json keys with data
        :type single_json_keys_data: list
        :param current_data: current dictionary data
        :type current_data: dict
        :param leaf_dictionaries: dictionary with leaf data
        :type leaf_dictionaries: dict
        """
        for index, key in enumerate(single_json_keys_data, start=1):
            if key not in current_data:
                current_data[key] = [leaf_dictionaries] if index == self.keys_length else {}
            elif isinstance(current_data[key], list):
                current_data[key].append(leaf_dictionaries)
            current_data = current_data[key]

    @staticmethod
    def remove_duplicate_keys(json_keys):
        """
        Method responsible for removing duplicated keys
        :param json_keys: provided json keys
        :type json_keys: list
        :return: unique list of keys
        :rtype: list
        """
        unique_ordered_keys = []
        for key in json_keys:
            if key not in unique_ordered_keys:
                unique_ordered_keys.append(key)

        return unique_ordered_keys
