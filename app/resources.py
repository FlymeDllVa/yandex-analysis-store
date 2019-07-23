from flask import Flask, jsonify, abort, request
from flask_restful import Api, Resource, reqparse, abort
from app import app, db
from app.models import Imports, Citizen
from datetime import datetime
from threading import Thread

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


class API_Import(Resource):
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


class API_Update_Citizen(Resource):
    def patch(self, import_id, citizen_id):
        update = Citizen.update_citizens(import_id, citizen_id, request.get_json())
        if update:
            return jsonify({"data": update})
        abort(400)
