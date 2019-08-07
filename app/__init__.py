from app.project.environment import *
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from redis import Redis
from celery import Celery

app = Flask(__name__)
app.config.update(
    SECRET_KEY=SECRET_KEY,
    SQLALCHEMY_DATABASE_URI=DATABASE_URI + POSTGRES_DB,
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    CELERY_BROKER_URL=f'redis://{REDIS_HOST}:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/2',
    CELERY_RESULT_BACKEND=f'redis://{REDIS_HOST}:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/2'
)

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

db = SQLAlchemy(app)
db_redis = Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    db=REDIS_DB
)

from app.project import models, resources
from app.project.models import Imports, Citizen

db.create_all()

api = Api(app)

api.add_resource(resources.API_Add_Import, '/imports')
api.add_resource(resources.API_Update_Citizen, '/imports/<int:import_id>/citizens/<int:citizen_id>')
api.add_resource(resources.API_Get_Citizens, '/imports/<int:import_id>/citizens')
api.add_resource(resources.API_Get_Gifts, '/imports/<int:import_id>/citizens/birthdays')
api.add_resource(resources.API_Get_Citizen_Percentile, '/imports/<int:import_id>/towns/stat/percentile/age')


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")
