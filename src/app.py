from flask import Flask
from pymongo import MongoClient

def create_app():
	# INIT Flask App
	app = Flask(__name__)

	# INIT Configs
	app.config.from_pyfile('settings.py')
	DB_CONNECTION_STRING = app.config.get('DB_CONNECTION_STRING')
	DB_NAME = app.config.get('DB_NAME')
	FLASK_RUN_PORT = app.config.get('FLASK_RUN_PORT')
	print(f'FLASK_RUN_PORT: {FLASK_RUN_PORT}')

	# INIT Cors
	from flask_cors import CORS
	cors = CORS(app, resources={r"/*": {"origins": "*"}})

	# INIT RESTFul API 
	from flask_restful import Api
	api = Api(app, catch_all_404s=True)

	# INIT DB Object
	from src.database import Database
	db = Database(connection_string = DB_CONNECTION_STRING, database = DB_NAME)

	db_client = MongoClient(DB_CONNECTION_STRING)
	main_db = db_client[DB_NAME]

	# Add UserModel Controller
	from src.controllers.UserModel import UserModelBlueprint
	app.register_blueprint(UserModelBlueprint(main_db))

	return app