from app import db, connects_residents
from datetime import datetime
from time import sleep

class Imports(db.Model):
    __tablename__ = 'imports'
    import_id = db.Column(db.Integer, autoincrement=True, primary_key=True, index=True)

    def add_import(new_import):
        db.session.add(new_import)
        db.session.commit()
        return new_import.import_id

    def find_import(import_id):
        current_import = Imports.query.filter_by(import_id=import_id).first()
        if current_import:
            return current_import
        return None


class Citizen(db.Model):
    __tablename__ = 'citizens'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, index=True)

    imports = db.relationship("Imports", backref="citizens")
    import_id = db.Column(db.Integer, db.ForeignKey(
        'imports.import_id', ondelete='CASCADE'), index=True)

    citizen_id = db.Column(db.Integer, index=True)
    town = db.Column(db.String(256))
    street = db.Column(db.String(256))
    building = db.Column(db.String(256))
    appartement = db.Column(db.Integer)
    name = db.Column(db.String(256))
    birth_date = db.Column(db.DateTime, index=True)
    gender = db.Column(db.String(256))
    relatives_ids = db.Column(db.ARRAY(db.Integer))

    kindred = db.Table('relatives',
                       db.Column('id', db.Integer, autoincrement=True, primary_key=True, index=True),
                       db.Column('citizen_id', db.Integer, db.ForeignKey('citizens.id'), index=True),
                       db.Column('relatives_id', db.Integer, db.ForeignKey('citizens.id'), index=True)
                       )

    relatives = db.relationship('Citizen',
                                secondary=kindred,
                                primaryjoin=(kindred.c.citizen_id == id),
                                secondaryjoin=(kindred.c.relatives_id == id),
                                backref=db.backref('kindred', lazy='dynamic'),
                                lazy='dynamic'
                                )

    def get_citizens(import_id):
        current_import = Imports.find_import(import_id)
        if current_import:
            return current_import.citizens
        return None

    def update_citizens(import_id, citizen_id, args):
        global connects_residents
        connects_residents = False

        citizen = Citizen.query.filter_by(import_id=import_id, citizen_id=citizen_id).first()

        try:
            if "name" in args:citizen.name = args["name"]
            if "gender" in args: citizen.gender = args["gender"]
            if "birth_date" in args: citizen.birth_date = datetime.strptime(args["birth_date"], '%d.%m.%Y').date()
            if "relatives" in args:
                citizen.relatives_ids = args["relatives"]
                for item in citizen.relatives_ids:
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
                    "relatives": citizen.relatives_ids}

        connects_residents = True
        return response

    def connect_citizens(import_id):
        global connects_residents
        def check_connects_residents():
            global connects_residents
            if connects_residents is False:
                print("connects_residents is FALSE")
                sleep(0.1)
                check_connects_residents()
            else:
                print("connects_residents is TRUE")
        connects_residents = True
        current_import = Citizen.get_citizens(import_id)
        if current_import:
            for citizen_id, relatives in {citizen.citizen_id: citizen.relatives_ids for citizen in current_import if citizen.relatives_ids}.items():
                citizen = Citizen.query.filter_by(import_id=import_id, citizen_id=citizen_id).first().relatives
                for item in relatives:
                    citizen.append(Citizen.query.filter_by(import_id=import_id, citizen_id=item).first())
                check_connects_residents()
                print(citizen_id)
            db.session.commit()
        connects_residents = False
