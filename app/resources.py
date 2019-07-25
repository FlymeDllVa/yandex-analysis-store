from app import db_redis
from app.models import Imports, Citizen
from flask import jsonify, abort, request
from flask_restful import Resource, abort
from datetime import date, datetime
from math import ceil, floor

class API_Add_Import(Resource):
    def post(self):
        def check_args(args, import_id):
            if "citizens" in args:
                data, citizens = dict(), list()
                if "citizens" not in args: return None
                for citizen in args["citizens"]:
                    if "citizen_id" not in citizen: return None
                    data.update({citizen["citizen_id"]: citizen})


                for citizen_id, citizen in data.items():
                    citizen["birth_date"] = datetime.strptime(citizen["birth_date"], '%d.%m.%Y').date()
                    try:
                        citizens.append(Citizen(import_id=import_id,
                                                citizen_id=citizen["citizen_id"],
                                                town=citizen["town"],
                                                street=citizen["street"],
                                                building=citizen["building"],
                                                appartement=int(citizen["appartement"]),
                                                name=citizen["name"],
                                                birth_date=citizen["birth_date"],
                                                gender=citizen["gender"],
                                                relatives=citizen["relatives"]))
                    except Exception:
                        return None
                    db_redis.set(f"{import_id}_{citizen_id}_birth_date", str(citizen["birth_date"].month))
                db_redis.bgsave()
                return citizens
            return None
        import_id = Imports.add_import(Imports())
        print(import_id)
        data = check_args(request.get_json(), import_id)
        if data:
            Citizen.save_list_citizens(data)
            return jsonify({"data": {"import_id": import_id}})
        Imports.delete_import(import_id)
        abort(400)


class API_Update_Citizen(Resource):
    def patch(self, import_id, citizen_id):
        update = Citizen.update_citizens(import_id, citizen_id, request.get_json())
        if update:
            return jsonify({"data": update})
        abort(400)


class API_Get_Citizens(Resource):
    def get(self, import_id):
        citizens = Citizen.get_citizens(import_id)
        if citizens:
            data = list()
            for citizen in citizens:
                data.append({"citizen_id": citizen.citizen_id,
                         "town": citizen.town,
                         "street": citizen.street,
                         "building": citizen.building,
                         "appartement": citizen.appartement,
                         "name": citizen.name,
                         "birth_date": citizen.birth_date.strftime('%d.%m.%Y'),
                         "gender": citizen.gender,
                         "relatives": citizen.relatives})
            return jsonify({"data": data})
        abort(400)


class API_Get_Gifts(Resource):
    def get(self, import_id):
        birthday = {1: dict(), 2: dict(), 3: dict(), 4: dict(), 5: dict(), 6: dict(), 7: dict(),
                    8: dict(), 9: dict(), 10: dict(), 11: dict(), 12: dict()}
        citizens = Citizen.get_citizens(import_id)

        if citizens:
            for citizen in citizens:
                for citizen_id in citizen.relatives:
                    month = int(db_redis.get(f"{import_id}_{citizen_id}_birth_date"))
                    birthday[month].update({citizen.citizen_id: birthday[month].get(citizen.citizen_id, 0) + 1})
            return jsonify({"data":{str(month): [{"citizen_id": citizen_id,
                                                   "presents": presents} for citizen_id,
                                                                             presents in data.items()] for
                                     month, data in birthday.items()}})
        abort(400)


class API_Get_Citizen_Percentile(Resource):
    def get(self, import_id):

        def percentile(N, percent, key=lambda x: x):
            """
            Find the percentile of a list of values.

            @parameter N - is a list of values. Note N MUST BE already sorted.
            @parameter percent - a float value from 0.0 to 1.0.
            @parameter key - optional key function to compute value from each element of N.

            @return - the percentile of the values
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

        def calculate_age(born):
            today = date.today()
            return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

        cities = dict()
        citizens = Citizen.get_citizens(import_id)
        if citizens:
            for citizen in citizens:
                if citizen.town in cities:
                    cities[citizen.town].append(calculate_age(citizen.birth_date))
                else:
                    cities[citizen.town] = [calculate_age(citizen.birth_date)]
            return jsonify({"data": [{"town": city,
                                      "p50": percentile(sorted(ages), 0.5),
                                      "p75": percentile(sorted(ages), 0.75),
                                      "p99": percentile(sorted(ages), 0.99)} for city, ages in cities.items()]})
        abort(400)
