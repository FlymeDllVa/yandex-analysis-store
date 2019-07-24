from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from config import Flask_Config

app = Flask(__name__)
app.config.from_object(Flask_Config)

db = SQLAlchemy(app)

connects_residents = False

from app import models, resources
from app.models import Citizen, Imports

# db.drop_all()
db.create_all()
"""
API
"""
api = Api(app)

api.add_resource(resources.API_Add_Import, '/imports')
api.add_resource(resources.API_Update_Citizen, '/imports/<int:import_id>/citizens/<int:citizen_id>')
api.add_resource(resources.API_Get_Citizens, '/imports/<int:import_id>/citizens')
api.add_resource(resources.API_Get_Gifts, '/imports/<int:import_id>/citizens/birthdays')
api.add_resource(resources.API_Get_Citizen_Percentile, '/imports/<int:import_id>/towns/stat/percentile/age')