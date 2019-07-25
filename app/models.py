from app import db
from datetime import datetime

class Imports(db.Model):
    __tablename__ = 'imports'
    import_id = db.Column(db.Integer, autoincrement=True, primary_key=True, index=True)

    @classmethod
    def add_import(cls, new_import):
        db.session.add(new_import)
        db.session.commit()
        return new_import.import_id

    @classmethod
    def delete_import(cls, import_id):
        Imports.query.filter_by(import_id=import_id).delete()
        db.session.commit()
        return True



class Citizen(db.Model):
    __tablename__ = 'citizens'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, index=True)

    import_id = db.Column(db.Integer, index=True)
    citizen_id = db.Column(db.Integer, index=True)
    town = db.Column(db.String(256))
    street = db.Column(db.String(256))
    building = db.Column(db.String(256))
    appartement = db.Column(db.Integer)
    name = db.Column(db.String(256))
    birth_date = db.Column(db.DateTime)
    gender = db.Column(db.String(256))
    relatives = db.Column(db.ARRAY(db.Integer))

    @classmethod
    def save_list_citizens(cls, data):
        db.session.bulk_save_objects(data)
        db.session.commit()

    @classmethod
    def get_citizens(cls, import_id):
        current_import = Citizen.query.filter_by(import_id=import_id).all()
        if current_import:
            return current_import
        return None

    @classmethod
    def find_citizen(cls, import_id, citizen_id):
        return Citizen.query.filter_by(import_id=import_id, citizen_id=citizen_id).first()

    @classmethod
    def update_citizens(cls, import_id, citizen_id, args):

        citizen = Citizen.find_citizen(import_id, citizen_id)

        try:
            if "name" in args:citizen.name = args["name"]
            if "gender" in args: citizen.gender = args["gender"]
            if "birth_date" in args: citizen.birth_date = datetime.strptime(args["birth_date"], '%d.%m.%Y').date()
            if "relatives" in args:
                citizen.relatives_ids = args["relatives"]
                for item in citizen.relatives_ids:
                    citizen.relatives = list()
                    found_citizen = Citizen.query.filter_by(import_id=import_id, citizen_id=item).first()
                    if found_citizen:
                        citizen.relatives.append(found_citizen)
            if "town" in args: citizen.town = args["town"]
            if "street" in args: citizen.street = args["street"]
            if "building" in args: citizen.building = args["building"]
            if "appartement" in args: citizen.appartement = args["appartement"]
        except AttributeError:
            return None

        db.session.commit()

        response = {"citizen_id": citizen.citizen_id,
                    "town": citizen.town,
                    "street": citizen.street,
                    "building": citizen.building,
                    "appartement": citizen.appartement,
                    "name": citizen.name,
                    "birth_date": citizen.birth_date.strftime('%d.%m.%Y'),
                    "gender": citizen.gender,
                    "relatives": citizen.relatives}

        return response
