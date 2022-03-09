
class Database:
	def __init__(self, connection_string, database):
		self._connection_string = connection_string
		self._db = database