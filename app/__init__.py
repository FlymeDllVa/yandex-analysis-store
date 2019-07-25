from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from redis import Redis
from config import Flask_Config

app = Flask(__name__)
app.config.from_object(Flask_Config)

db = SQLAlchemy(app)
db_redis = Redis(host='localhost', port=6379, db=0)

from app import models, resources
from app.models import Imports, Citizen

# db.drop_all()
db.create_all()
db_redis.flushall()
"""
API
"""
api = Api(app)

api.add_resource(resources.API_Add_Import, '/imports')
api.add_resource(resources.API_Update_Citizen, '/imports/<int:import_id>/citizens/<int:citizen_id>')
api.add_resource(resources.API_Get_Citizens, '/imports/<int:import_id>/citizens')
api.add_resource(resources.API_Get_Gifts, '/imports/<int:import_id>/citizens/birthdays')
api.add_resource(resources.API_Get_Citizen_Percentile, '/imports/<int:import_id>/towns/stat/percentile/age')
