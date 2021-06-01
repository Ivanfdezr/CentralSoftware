import sqlite3


class ConnectionController(object):
	
	def __init__(self,f):
		self.f = f

	def start_connection(self):
		try:
			#self.conexion = mysql.connector.connect( user='admin', password='password', database='centraldb')
			self.conexion = sqlite3.connect('CentralDB.sqlite')
			self.cursor = self.conexion.cursor()
	
		except Exception as e:
			pass

	def close_connection(self):
		#self.cursor.close()
		self.conexion.close()

	def __call__(self, *args):
		self.start_connection()
		records = self.f(*args, cursor=self.cursor)

		if records == None:
			self.conexion.commit()

		self.close_connection()
		return records


@ConnectionController
def execute_query(query, cursor=None):
	'''
	Realiza la ejecucion de un query pasandole el query a ejecutar
	'''
	try:
		cursor.execute(query)
		records = cursor.fetchall()
	except Exception as e:
		records = None

	return records
	
	
