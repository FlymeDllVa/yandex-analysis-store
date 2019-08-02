import re
from app.project.models import Imports, Citizen
from flask import request
from flask_restful import Resource, abort
from datetime import date, datetime
from math import ceil, floor


class API_Add_Import(Resource):
    def post(self):
        """
        API method that adds import

        :return: import_id
        """

        def check_args(args):
            """
            Checks the arguments for validity

            :param args: import arguments
            :return: validated data or None
            """
            if "citizens" in args:
                data = dict()
                for citizen in args["citizens"]:
                    if all(item in {'citizen_id', "town", "street", "building", "apartment", "name", "birth_date",
                                    "gender", "relatives"} for item in citizen.keys()):
                        if all(isinstance(item, int) for item in [citizen["citizen_id"], citizen["apartment"]]) and \
                                all(isinstance(item, str) for item in
                                    {citizen["town"], citizen["street"], citizen["building"], citizen["name"],
                                     citizen["birth_date"], citizen["gender"]}) and \
                                isinstance(citizen["relatives"], list):
                            try:
                                citizen["birth_date"] = datetime.strptime(citizen["birth_date"], '%d.%m.%Y').date()
                            except Exception:
                                return None
                            if re.fullmatch(r'^[\D]+', citizen["name"]) and \
                                    re.fullmatch(r'^female|male', citizen["gender"]) and \
                                    re.search(r'^[\w\d]+', citizen["building"]) and \
                                    re.search(r'^[\w\d]+', citizen["street"]) and \
                                    re.search(r'^[\D]+', citizen["town"]):
                                data.update({citizen["citizen_id"]: dict(town=citizen["town"], street=citizen["street"],
                                                                         building=citizen["building"],
                                                                         name=citizen["name"],
                                                                         apartment=citizen["apartment"],
                                                                         birth_date=citizen["birth_date"],
                                                                         gender=citizen["gender"],
                                                                         relatives=citizen["relatives"])})
                            else:
                                return None
                        else:
                            return None
                    else:
                        return None
                for citizen_id, citizen in data.items():
                    for relatives_id in citizen["relatives"]:
                        if relatives_id in data:
                            if not citizen_id in data[relatives_id]["relatives"]:
                                return None
                        else:
                            return None
                return data
            return None

        data = check_args(request.get_json())
        if data:
            import_id = Imports.add_import(Imports())
            request_data = list()
            for citizen_id, citizen in data.items():
                Citizen.set_birth_month(f"{import_id}_{citizen_id}_birth_date", citizen["birth_date"].month)
                request_data.append(
                    Citizen(import_id=import_id, citizen_id=citizen_id, town=citizen["town"], street=citizen["street"],
                            building=citizen["building"], apartment=int(citizen["apartment"]), name=citizen["name"],
                            birth_date=citizen["birth_date"], gender=citizen["gender"],
                            relatives=citizen["relatives"])
                )
            Citizen.save_list_citizens(request_data)
            return {"data": {"import_id": import_id}}, 201
        abort(400)


class API_Update_Citizen(Resource):
    def patch(self, import_id, citizen_id):
        """
        An API method that updates the import resident information

        :param import_id: indexer import
        :param citizen_id: current import person identifier
        :return: the answer
        """

        def check_args(args):
            """
            Checks the arguments for validity

            :param args: import arguments
            :return: validated data or None
            """
            if any(item in args for item in
                   ["town", "street", "building", "apartment", "name", "birth_date", "gender", "relatives"]):
                if "name" in args:
                    if not re.fullmatch(r'^\w+(\s\w+|(\s\w+){2})', args["name"]):
                        return None
                if "gender" in args:
                    if not re.fullmatch(r'^female|male', args["gender"]):
                        return None
                if "birth_date" in args:
                    try:
                        args["birth_date"] = datetime.strptime(args["birth_date"], '%d.%m.%Y').date()
                    except Exception:
                        return None
                if "town" in args:
                    if not re.search(r'^[\w]+', args["town"]):
                        return None
                if "street" in args:
                    if not re.search(r'^[\w\d]+', args["street"]):
                        return None
                if "building" in args:
                    if not re.search(r'^[\w\d]+', args["building"]):
                        return None
                if "apartment" in args:
                    if not isinstance(args["apartment"], int):
                        return None
                if "relatives" in args:
                    for relative in args["relatives"]:
                        if not Citizen.find_citizen(import_id, relative):
                            return None
                return args
            return None

        citizen = Citizen.find_citizen(import_id, citizen_id)
        args = check_args(request.get_json())
        if citizen and args:
            if "name" in args:
                citizen.name = args["name"]
            if "gender" in args:
                citizen.gender = args["gender"]
            if "birth_date" in args:
                citizen.birth_date = args["birth_date"]
            if "town" in args:
                citizen.town = args["town"]
            if "street" in args:
                citizen.street = args["street"]
            if "building" in args:
                citizen.building = args["building"]
            if "apartment" in args:
                citizen.apartment = args["apartment"]
            if "relatives" in args:
                for people in set(citizen.relatives) - set(args["relatives"]):
                    Citizen.remove_relatives_citizens(import_id, people, citizen_id)
                for people in args["relatives"]:
                    Citizen.append_relatives_citizens(import_id, people, citizen_id)
                citizen.relatives = args["relatives"]
            Citizen.db_commit()
            return {"data": dict(citizen_id=citizen.citizen_id, town=citizen.town, street=citizen.street,
                                 building=citizen.building, apartment=citizen.apartment, name=citizen.name,
                                 birth_date=citizen.birth_date.strftime('%d.%m.%Y'), gender=citizen.gender,
                                 relatives=citizen.relatives)}
        abort(400)


class API_Get_Citizens(Resource):
    def get(self, import_id):
        """
        An API method that returns all residents of a single import

        :param import_id: indexer import
        :return: the answer
        """
        citizens = Citizen.get_citizens(import_id)
        if citizens:
            return {"data": [
                dict(citizen_id=citizen.citizen_id, town=citizen.town, street=citizen.street, building=citizen.building,
                     apartment=citizen.apartment, name=citizen.name,
                     birth_date=citizen.birth_date.strftime('%d.%m.%Y'), gender=citizen.gender,
                     relatives=citizen.relatives) for citizen in citizens]}
        abort(400)


class API_Get_Gifts(Resource):
    def get(self, import_id):
        """
        An API method that calculates the required number of gifts for each month of a single import

        :param import_id: indexer import
        :return: the answer
        """

        birthday = {1: dict(), 2: dict(), 3: dict(), 4: dict(), 5: dict(), 6: dict(), 7: dict(),
                    8: dict(), 9: dict(), 10: dict(), 11: dict(), 12: dict()}
        citizens = Citizen.get_citizens(import_id)
        if citizens:
            for citizen in citizens:
                for citizen_id in citizen.relatives:
                    month = Citizen.get_birth_month(f"{import_id}_{citizen_id}_birth_date", 'int')
                    birthday[month].update({citizen.citizen_id: birthday[month].get(citizen.citizen_id, 0) + 1})
            return {"data": {str(month): [{"citizen_id": citizen_id,
                                           "presents": presents} for citizen_id,
                                                                     presents in data.items()] for
                             month, data in birthday.items()}}
        abort(400)


class API_Get_Citizen_Percentile(Resource):
    def get(self, import_id):
        """
        An API method that counts the percentile of one import for each city

        :param import_id: indexer import
        :return: the answer
        """

        def percentile(N, percent, key=lambda x: x):
            """
            Find the percentile of a list of values.

            :param N: is a list of values. Note N MUST BE already sorted.
            :param percent: a float value from 0.0 to 1.0.
            :param key: optional key function to compute value from each element of N.
            :return: the percentile of the values
            """
            if not N:
                return None
            k = (len(N) - 1) * percent
            f = floor(k)
            c = ceil(k)
            if f == c:
                return key(N[int(k)])
            d0 = key(N[int(f)]) * (c - k)
            d1 = key(N[int(c)]) * (k - f)
            return d0 + d1

        def calculate_age(citizen_date):
            """
            Calculates a person's age by date of birth

            :param citizen_date: date of birth
            :return: age
            """
            today = date.today()
            return today.year - citizen_date.year - ((today.month, today.day) < (citizen_date.month, citizen_date.day))

        cities = dict()
        citizens = Citizen.get_citizens(import_id)
        if citizens:
            for citizen in citizens:
                if citizen.town in cities:
                    cities[citizen.town].append(calculate_age(citizen.birth_date))
                else:
                    cities[citizen.town] = [calculate_age(citizen.birth_date)]
            return {"data": [{"town": city,
                              "p50": percentile(sorted(ages), 0.5),
                              "p75": percentile(sorted(ages), 0.75),
                              "p99": percentile(sorted(ages), 0.99)} for city, ages in cities.items()]}
        abort(400)
