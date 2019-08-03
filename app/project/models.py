from app import db, db_redis

class Imports(db.Model):
    __tablename__ = 'imports'
    import_id = db.Column(db.Integer, autoincrement=True, primary_key=True, index=True)

    @classmethod
    def add_import(cls) -> int:
        """
        Adds a new import

        :return: import_id
        """

        new_import = Imports()
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
    def db_commit(cls) -> None:
        """
        Database commit

        :return: True
        """

        db.session.commit()

    @classmethod
    def save_list_citizens(cls, data) -> None:
        """
        Keeps people in the database

        :param data: List of data
        :return: True
        """

        db.session.bulk_save_objects(data)
        db.session.commit()


    @classmethod
    def get_citizens(cls, import_id) -> object or None:
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
    def find_citizen(cls, import_id, citizen_id) -> object:
        """
        Looking for a man

        :param import_id: in which the person is located
        :param citizen_id: man's
        :return:
        """

        return cls.query.filter_by(import_id=import_id, citizen_id=citizen_id).first()

    @classmethod
    def append_relatives_citizens(cls, import_id, citizen_id, updated_id) -> None:
        """
        Adds a person to relatives

        :param import_id: in which the person is located
        :param citizen_id: man's
        :param updated_id: id of the user you want to add
        :return:
        """

        people = cls.find_citizen(import_id, citizen_id)
        people_relatives = [i for i in people.relatives]
        if updated_id not in people_relatives:
            people_relatives.append(updated_id)
            people.relatives = people_relatives
        db.session.commit()

    @classmethod
    def remove_relatives_citizens(cls, import_id, citizen_id, remove_id) -> None:
        """
        Remove a person to relatives

        :param import_id: in which the person is located
        :param citizen_id: man's
        :param remove_id: id of the person you want to delete
        :return:
        """

        people = cls.find_citizen(import_id, citizen_id)
        people_relatives = [i for i in people.relatives]
        if remove_id in people_relatives:
            people_relatives.remove(remove_id)
            people.relatives = people_relatives
        db.session.commit()

    @classmethod
    def set_birth_month(cls, key, value) -> None:
        """
        Sets the value for the key in Redis

        :param key:
        :param value:
        :return:
        """

        db_redis.set(key, value)

    @classmethod
    def get_birth_month(cls, key, request_type=None) -> int or str:
        """
        Gets the key value from Redis

        :param key:
        :param request_type: optional field, type of request
        :return: the value of the Redis key
        """

        data = db_redis.get(key)
        if request_type == "int":
            return int(data)
        return data
