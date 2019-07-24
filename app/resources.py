from flask import Flask, jsonify, abort, request
from flask_restful import Api, Resource, reqparse, abort
from app import app, db
from app.models import Imports, Citizen
from datetime import datetime, date
from math import ceil, floor
from functools import partial
from threading import Thread


class API_Add_Import(Resource):
    def post(self):

        new_import = Imports()
        data, relatives = {}, {}

        for citizen in request.get_json()["citizens"]:
            print(citizen["citizen_id"])
            new_import.citizens.append(Citizen(citizen_id=citizen["citizen_id"],
                                               town=citizen["town"],
                                               street=citizen["street"],
                                               building=citizen["building"],
                                               appartement=citizen["appartement"],
                                               name=citizen["name"],
                                               birth_date=datetime.strptime(citizen["birth_date"], '%d.%m.%Y').date(),
                                               gender=citizen["gender"],
                                               relatives_ids=citizen["relatives"]))

        new_import = Imports.add_import(new_import)
        if new_import:
            flow = Thread(target=Citizen.connect_citizens, args=(new_import,))
            print(flow.name)
            flow.start()
            return jsonify({"data": {"import_id": new_import}})
        abort(400)


class API_Get_Citizens(Resource):
    def get(self, import_id):
        all_citizens = Citizen.get_citizens(import_id)
        if all_citizens:
            all_citizens = [{"citizen_id": citizen.citizen_id,
                             "town": citizen.town,
                             "street": citizen.street,
                             "building": citizen.building,
                             "appartement": citizen.appartement,
                             "name": citizen.name,
                             "birth_date": citizen.birth_date.strftime('%d.%m.%Y'),
                             "gender": citizen.gender,
                             "relatives_ids": citizen.relatives_ids} for citizen in all_citizens]
            return jsonify({"data": all_citizens})
        abort(400)


class API_Update_Citizen(Resource):
    def patch(self, import_id, citizen_id):
        update = Citizen.update_citizens(import_id, citizen_id, request.get_json())
        if update:
            return jsonify({"data": update})
        abort(400)


class API_Get_Gifts(Resource):
    def get(self, import_id):
        birthday = {1: dict(), 2: dict(), 3: dict(), 4: dict(), 5: dict(), 6: dict(), 7: dict(), 8: dict(), 9: dict(),
                    10: dict(), 11: dict(), 12: dict()}
        citizens = Citizen.get_citizens(import_id)

        if citizens:
            for citizen in citizens:
                for kindred in citizen.relatives_ids:
                    month = Citizen.find_citizen(import_id, kindred).birth_date.month
                    if citizen.citizen_id in birthday[month]:
                        birthday[month][citizen.citizen_id] = birthday[month][citizen.citizen_id] + 1
                    else:
                        birthday[month].update({citizen.citizen_id: 1})
            return jsonify({"data": {str(month): [{"citizen_id": citizen_id,
                                                   "presents": presents} for citizen_id, presents in data.items()] for
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
