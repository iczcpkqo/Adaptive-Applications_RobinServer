from flask_restful import Resource
from src.response import Response
from pymongo import MongoClient

class HelloWorld(Resource):
	def __init__(self, **kwargs):
		self.db = kwargs['db']

		# Connect to your MongoDB cluster
		client = MongoClient(self.db._connection_string)
		self.curr_db = client['sample_analytics']
	
	def get(self):
		cust = self.curr_db.customers.find_one({'email': "arroyocolton@gmail.com"})
		return Response.send_json_200({"Customer": cust["name"]})