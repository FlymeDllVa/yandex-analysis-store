from app import db
from datetime import datetime

class Imports(db.Model):
    __tablename__ = 'imports'
    import_id = db.Column(db.Integer, autoincrement=True, primary_key=True, index=True)

    @classmethod
    def add_import(cls, new_import):
        """
        Adds a new import

        :param new_import: Import()
        :return: import_id
        """
        db.session.add(new_import)
        db.session.commit()
        return new_import.import_id


class Citizen(db.Model):
    __tablename__ = 'citizens'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, index=True)

    import_id = db.Column(db.Integer, index=True)
    citizen_id = db.Column(db.Integer, index=True)
    town = db.Column(db.String(256))
    street = db.Column(db.String(256))
    building = db.Column(db.String(256))
    apartment = db.Column(db.Integer)
    name = db.Column(db.String(256))
    birth_date = db.Column(db.DateTime)
    gender = db.Column(db.String(256))
    relatives = db.Column(db.ARRAY(db.Integer))

    @classmethod
    def save_list_citizens(cls, data):
        """
        Keeps people in the database

        :param data: List of data
        :return: None
        """
        db.session.bulk_save_objects(data)
        db.session.commit()

    @classmethod
    def get_citizens(cls, import_id):
        """
        Returns a list of people for a single import

        :param import_id: import_id you want to find
        :return: the current import
        """
        current_import = cls.query.filter_by(import_id=import_id).all()
        if current_import:
            return current_import
        return None

    @classmethod
    def find_citizen(cls, import_id, citizen_id):
        """
        Looking for a man

        :param import_id: in which the person is located
        :param citizen_id: man's
        :return:
        """
        return cls.query.filter_by(import_id=import_id, citizen_id=citizen_id).first()

    @classmethod
    def update_citizens(cls, import_id, citizen_id, args):

        citizen = cls.find_citizen(import_id, citizen_id)

        try:
            if "name" in args:citizen.name = args["name"]
            if "gender" in args: citizen.gender = args["gender"]
            if "birth_date" in args: citizen.birth_date = datetime.strptime(args["birth_date"], '%d.%m.%Y').date()
            if "relatives" in args:
                citizen.relatives_ids = args["relatives"]
                for item in citizen.relatives_ids:
                    citizen.relatives = list()
                    found_citizen = cls.query.filter_by(import_id=import_id, citizen_id=item).first()
                    if found_citizen:
                        citizen.relatives.append(found_citizen)
            if "town" in args: citizen.town = args["town"]
            if "street" in args: citizen.street = args["street"]
            if "building" in args: citizen.building = args["building"]
            if "apartment" in args: citizen.apartment = args["apartment"]
        except AttributeError:
            return None

        db.session.commit()

        response = {"citizen_id": citizen.citizen_id,
                    "town": citizen.town,
                    "street": citizen.street,
                    "building": citizen.building,
                    "apartment": citizen.apartment,
                    "name": citizen.name,
                    "birth_date": citizen.birth_date.strftime('%d.%m.%Y'),
                    "gender": citizen.gender,
                    "relatives": citizen.relatives}

        return response
