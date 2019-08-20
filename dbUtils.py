import mysql.connector


class ConnectionController(object):
	
	def __init__(self,f):
		self.f = f
		#with open("conexion.json") as f:
			#self.cadConexion = json.load(f)

	def start_connection(self):
		try:
			self.conexion = mysql.connector.connect( user='root', password='mitz43', database='centraldb')
			self.cursor = self.conexion.cursor()
	
		except Exception as e:
			#print("excepcion: {0}".format(e))
			pass

	def close_connection(self):
		self.cursor.close()
		self.conexion.close()

	def __call__(self, *args):
		self.start_connection()
		regreso = self.f(*args, cursor=self.cursor)

		if regreso == None:
			#print('Lo llamo un insert')
			self.conexion.commit()

		self.close_connection()
		return regreso


@ConnectionController
def execute_query(query, cursor=None):
	'''
	Realiza la ejecucion de un query pasandole el query a ejecutar
	'''
	#print('Entra a execute_query')
	try:
		#print('------------------------------')
		#print('{0}'.format(query))
		#print('------------------------------')
	
		cursor.execute(query)
		lista = cursor.fetchall()
	except Exception as e:
		#print("excepcion: {0}".format(e))
		lista = None

	#print('++++++++++++++++++++++++++++++')
	#print(lista)
	#print('++++++++++++++++++++++++++++++')

	return lista
	
	
