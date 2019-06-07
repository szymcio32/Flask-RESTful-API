from db import db

from common.utils import ValidationError


class FruitModel(db.Model):
    """
    Class responsible for interaction with database.
    """
    __tablename__ = 'fruits'

    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(80), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    currency = db.Column(db.String(10), nullable=False)
    fruit = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Float(precision=1))

    @classmethod
    def data_validation(cls, data):
        """
        Method responsible for checking if the provided json keys exist in the database.
        :param data: json data
        :type data: dict
        :raises: ValidationError if key does not exist in the database
        """
        db_fields = {column.name for column in cls.__table__.columns if column.name != 'id'}
        for key in data.keys():
            if key not in db_fields:
                raise ValidationError(f"Provided key: '{key}' does not exists in the database")

    def update(self, data):
        """
        Method responsible for updating database fields.
        :param data: json data
        :type data: dict
        """
        for key, value in data.items():
            setattr(self, key, value)

    def json(self):
        """
        Method responsible for returning a dict containing the database fields.
        :return: dict with database fields and values
        :rtype: dict
        """
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    def save_to_db(self):
        """
        Method responsible for saving the data to the database.
        """
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """
        Method responsible for deleting the data from the database.
        """
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        """
        Method responsible for retrieving item from the database based on id.
        :param _id: id of a record
        :type _id: str
        :return: database item
        :rtype: database object
        """
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def get_all_records(cls):
        """
        Method responsible for retrieving all items from the database.
        :return: database items
        :rtype: database object
        """
        return cls.query.all()
