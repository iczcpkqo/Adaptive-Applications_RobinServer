from flask import Flask

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

	# ADD Routes
	route_args = {'db': db}

	from src.resources import HelloWorld
	api.add_resource(HelloWorld, '/', resource_class_kwargs=route_args)

	return app