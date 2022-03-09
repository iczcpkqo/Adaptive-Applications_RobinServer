from flask_restful import Resource
from src.response import Response

class HelloWorld(Resource):
	def __init__(self, **kwargs):
		self.db = kwargs['db']
	
	def get(self):
		print(f"Hello World")
		return Response.send_json_200("Hello World!")