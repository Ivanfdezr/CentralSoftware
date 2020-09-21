import numpy as np
#from numpy import array
import re
import copy
import dbUtils
import matplotlib.tri as mpltri
import sys, inspect


gravitationalAcceleration = 32.17405*12 #in/s²
configurations = {	('b', None,None): {'nest':[['A']],'label':'=\n|\nA\n|\n=','PLfactor':0.05},
					('r', None,None): {'nest':[['A']],'label':'=\n/\nA\n/\n=','PLfactor':1},
					('b', 'b', None): {'nest':[['A','B']],'label':'=\nA\n|\nB\n=','PLfactor':1},
					('b', 'r', None): {'nest':[['A'],['B']],'label':'=\n|\nA\n|\n=\n/\nB\n/\n=','PLfactor':1.5},
					('r', 'b', None): {'nest':[['A'],['B']],'label':'=\n/\nA\n/\n=\n|\nB\n|\n=','PLfactor':1.5},
					('r', 'r', None): {'nest':[['A'],['B']],'label':'=\n/\nA\n/\n=\n/\nB\n/\n=','PLfactor':2},
					('b', None,'b' ): {'nest':[['A'],[],['C']],'label':'=\n|\nA\n|\n=\n|\n|\n|\n=\n|\nC\n|\n=','PLfactor':2},
					('b', None,'r' ): {'nest':[['A'],[],['C']],'label':'=\n|\nA\n|\n=\n|\n|\n|\n=\n/\nC\n/\n=','PLfactor':2.5},
					('r', None,'b' ): {'nest':[['A'],[],['C']],'label':'=\n/\nA\n/\n=\n|\n|\n|\n=\n|\nC\n|\n=','PLfactor':2.5},
					('r', None,'r' ): {'nest':[['A'],[],['C']],'label':'=\n/\nA\n/\n=\n|\n|\n|\n=\n/\nC\n/\n=','PLfactor':3},
					('b', 'b', 'b' ): {'nest':[['A','B','C']],'label':'=\nA\nB\nC\n=','PLfactor':1},
					('b', 'b', 'r' ): {'nest':[['A','B'],['C']],'label':'=\nA\n|\nB\n=\n/\nC\n/\n=','PLfactor':2},
					('r', 'b', 'b' ): {'nest':[['A'],['B','C']],'label':'=\n/\nA\n/\n=\nB\n|\nC\n=','PLfactor':2},	
					('b', 'r', 'b' ): {'nest':[['A'],['B'],['C']],'label':'=\n|\nA\n|\n=\n/\nB\n/\n=\n|\nC\n|\n=','PLfactor':2},
					('b', 'r', 'r' ): {'nest':[['A'],['B'],['C']],'label':'=\n|\nA\n|\n=\n/\nB\n/\n=\n/\nC\n/\n=','PLfactor':2.5},
					('r', 'r', 'b' ): {'nest':[['A'],['B'],['C']],'label':'=\n/\nA\n/\n=\n/\nB\n/\n=\n|\nC\n|\n=','PLfactor':2.5},
					('r', 'b', 'r' ): {'nest':[['A'],['B'],['C']],'label':'=\n/\nA\n/\n=\n|\nB\n|\n=\n/\nC\n/\n=','PLfactor':3},
					('r', 'r', 'r' ): {'nest':[['A'],['B'],['C']],'label':'=\n/\nA\n/\n=\n/\nB\n/\n=\n/\nC\n/\n=','PLfactor':3}	}


def __repr__(self):
	if len(self)==0:
		return '[]'
	elif len(self)==1:
		return '[' + str(self[0]) +']'
	else:
		return '[' + str(self[0]) +', ... '+ str(self[-1]) + ']'

np.set_string_function(__repr__)
array = lambda L: np.array(L)


def get_decimalPointPattern():
	
	return '(([\-\+]?\d*\.?\d+)|([\-\+]?\d+\.?\d*))'


def get_decimalPointWithThousandsCommaPattern():
	
	return '(([\-\+]?\d{1,3}(\,\d{3})*\.\d*)|([\-\+]?\d*\.?\d+)|([\-\+]?\d+\.?\d*))'


def get_decimalCommaPattern():
	
	return '(([\-\+]?\d{1,3}(\.\d{3})*\,\d*)|([\-\+]?\d*\,?\d+)|([\-\+]?\d+\,?\d*))'


def get_decimalFloatPointFunction():
	def text2float(text):
		items = re.split(',',text)
		text = ''.join(items)
		return float(text)
	return text2float


def get_decimalFloatCommaFunction():
	def text2float(text):
		items = re.split(',',text)
		assert(len(items)==2)
		tridigs = re.split('\.',items[0])
		items[0] = ''.join(tridigs)
		text = '.'.join(items)
		return float(text)
	return text2float


def np_dot( u,v ):
	
	return np.sum(u*v,axis=1,keepdims=True)

def np_cross( u,v ):
	
	return np.cross(u,v,axis=1)

def np_norm( v ):
	norm = np.linalg.norm(v,axis=1)
	norm = norm.reshape(-1,1)
	return v/norm


def calculate_buoyancyFactor( OD, ID, ρs, ρe, ρi ):

	doverDsq = (ID/OD)**2
	return ( (1-ρe/ρs)-doverDsq*(1-ρi/ρs) )/( 1-doverDsq )


def render_circle( center, radius, n=120, mode='all', xscale=1, yscale=1 ):

	if mode=='all':
		θ = np.linspace(0,np.pi*2,n)
		θ += np.pi/2 #- np.pi/20
	elif mode=='top':
		θ = np.linspace(0,np.pi,n)
	elif mode=='bottom':
		θ = np.linspace(np.pi,np.pi*2,n)
	elif mode=='right':
		θ = np.linspace(-np.pi/2,np.pi*2,n)
	elif mode=='left':
		θ = np.linspace(np.pi/2,np.pi*3/2,n)

	x = radius*np.cos(θ)*xscale
	y = radius*np.sin(θ)*yscale
	x += center[0]
	y += center[1]

	return np.array([x,y])


def RodriguesRotationFormula( v, u, θ ): 

	# Equation Reference:
	#		https://en.wikipedia.org/wiki/Rodrigues%27_rotation_formula
	return v*np.cos(θ) + np_cross( u,v )*np.sin(θ) + u*np_dot( u,v )*(1-np.cos(θ))


def render_wellbore( fields, radius, n=12 ):

	x = np.array( fields.EW )
	y = np.array( fields.NS )
	z = np.array( fields.TVD )
	c = 1.0#np.array( fields.MD )
	
	"""
	max_EW = max( fields.EW )
	min_EW = min( fields.EW )

	max_NS = max( fields.NS )
	min_NS = min( fields.NS )

	max_TVD = max( fields.TVD )
	min_TVD = min( fields.TVD )

	ΔEW  = max_EW  - min_EW
	ΔNS  = max_NS  - min_NS
	ΔTVD = max_TVD - min_TVD

	if ΔEW>ΔNS:
		zfactor = ΔEW/ΔTVD
	else:
		zfactor = ΔNS/ΔTVD
	zfactor=1
	z *= zfactor
	"""

	S = np.array([x,y,z])
	S = S.T

	U = S[2:] - S[:-2]
	U = np.append([U[0]],  U, axis=0)
	U = np.append(U, [U[-1]], axis=0)
	U = np_norm(U)

	P = np.array([[1,0,0]])
	
	V = np_cross(U,P)
	V = radius*np_norm(V)
	l = len(V)

	R = [ V+S ]
	φ = 2*np.pi/n

	for i in range(n):
		V = RodriguesRotationFormula( V, U, φ )
		R.append( V+S )

	R = np.array(R)
	R = R.reshape(-1,3)
	
	n+=1
	#nl = n*l
	#triangles = []
	
	X,Y,Z = R.T

	X = X.reshape(n,l)
	Y = Y.reshape(n,l)
	Z = Z.reshape(n,l)
	C = c*np.ones((n,l))

	return X,Y,Z,C#triangles #,Z/zfactor


def make_cleanAverage( X ):

	if len(X)>0:
		a = np.average(X)
		for i in range(10):
			W = np.exp(-np.abs(X-a))
			a = np.average(X, weights=W)
		return a
	else:
		return None


def isNoneEntry( entry ):
	
	return entry=='' and hasattr(entry,'unit')


def isSomething( value ):
	
	return value!='' and value!=None and value!=False


def unitConvert_value( value, originUnit, targetUnit ):

	query = """select u.factorToReferenceUnit, u.offsetToReferenceUnit from units u
			where u.representation = '{origin}' """.format(origin=originUnit)
	items_origin = dbUtils.execute_query(query)

	query = """select u.factorToReferenceUnit, u.offsetToReferenceUnit from units u 
			where u.representation = '{target}' """.format(target=targetUnit)
	items_target = dbUtils.execute_query(query)

	factor_origin = float(items_origin[0][0])
	factor_target = float(items_target[0][0])
	
	offset_origin = float(items_origin[0][1])
	offset_target = float(items_target[0][1])

	value = physicalValue( factor_origin/factor_target * value + (offset_origin - offset_target)/factor_target, targetUnit )

	return value


def referenceUnitConvert_value( value, unit ):

	query = """select u.factorToReferenceUnit, u.offsetToReferenceUnit, u.referenceUnit from units u
			where u.representation = '{unit}' """.format(unit=unit)
	items = dbUtils.execute_query(query)

	factor = float(items[0][0])
	offset = float(items[0][1])
	referenceUnit = items[0][2]

	value = physicalValue( factor*value+offset, referenceUnit )

	return value


def inverseReferenceUnitConvert_value( value, unit ):

	query = """select u.factorToReferenceUnit, u.offsetToReferenceUnit from units u
			where u.representation = '{unit}' """.format(unit=unit)
	items = dbUtils.execute_query(query)

	factor = float(items[0][0])
	offset = float(items[0][1])

	value = physicalValue( (value-offset)/factor, unit )

	return value


def create_physicalValue_and_appendTo_field(value, field, unit=None ):

	if unit=='referenceUnit':
		value = physicalValue( value, field.referenceUnit )
	elif unit==None:
		value = physicalValue( value, field.unit )
	else:
		value = physicalValue( value, unit )
	field.append( value )



def xfloat( expression ):
	if isinstance(expression, float) or isinstance(expression, np.float32) or isinstance(expression, np.float64):
		value = __float__( expression )
		return value
	else:
		if expression=='' or expression==None:
			raise ValueError
		items = re.split('[ ]+',str(expression))
		value = __float__( eval( '+'.join(items) ) )
		value.fraction = expression
		return value


def physicalValue(value, unit):
	
	if isinstance(value, int) or isinstance(value, np.int32) or isinstance(value, np.int64):
		entry = __int__(value)
	elif isinstance(value, float) or isinstance(value, np.float32) or isinstance(value, np.float64):
		entry = __float__(value)
	elif isinstance(value, str):
		entry = __str__(value)
	elif isinstance(value, type(None)):
		entry = __str__('')
	entry.unit = unit
	#entry.repr = lambda: str(entry._repr_)+' '+entry._repr_.unit
	
	return entry


class LogicalError( Exception ): pass


class __int__(int): pass                                                   


class __float__(float): pass                                               


class __str__(str): pass


class FieldList( list ):
	
	def __init__(self):
		super().__init__()
		

	def append(self, field):
		field.pos = len(self)
		setattr(self, str(field.abbreviation), field)
		super().append(field)


	def insert_data(self, data):
		for field in self:
			try:
				try:
					field.append(data[field.abbreviation])
				except AttributeError:
					value = physicalValue(data[field.abbreviation],field.unit)
					field.append(value)
			except KeyError:
				value = physicalValue(None,field.unit)
				field.append(value)


	def extract_data_from_row(self, row, representation=False):
		data = {}
		for field in self:
			if representation:
				data[field.abbreviation] = field[row]._repr_
			else:
				data[field.abbreviation] = field[row]
		return data


	def extract_fields_from_row(self, row):
		
		fields = FieldList()

		"""
		for field in self:
			newfield = Field(field.id)
			newfield.append(field[row])
			fields.append(newfield)
		"""

		for field in self:
			newfield = copy.deepcopy( field )
			newfield.clear()
			newfield.append(field[row])
			fields.append(newfield)

		return fields


	def clear_content(self):
		for field in self:
			field.clear()


	def referenceUnitConvert_fields(self):
		for field in self:
			#print(field.abbreviation,' ...')
			field.referenceUnitConvert()
			#print(field.abbreviation,' !')


	def inverseReferenceUnitConvert_fields(self):
		for field in self:
			field.inverseReferenceUnitConvert()


class Field( list ):
	
	def __init__(self, fieldID, altBg=False, altTx=False, altFg=False, mandatory=False, substitutefieldID=None):
		super().__init__()
		self.pos = None
		self.id = fieldID
		self.mandatory = mandatory
		self._altFg_ = altFg

		if substitutefieldID:
			query = """ select f.abbreviation from fields f where f.fieldID = '{fieldID}' """.format(fieldID=substitutefieldID)			
			self.substitute = dbUtils.execute_query(query)[0][0]
		else:
			self.substitute = None
		
		query = """ select f.description, f.representation, f.dataType, f.precision, 
					f.backgroundColor, f.altBackgroundColor, f.textColor, f.altTextColor, f.flag, f.altFlag, f.abbreviation
					from fields f where f.fieldID = '{fieldID}' """.format(fieldID=fieldID)			
		items = dbUtils.execute_query(query)[0]
		
		nom_i,alt_i = (5,4) if altBg else (4,5)
		nom_j,alt_j = (7,6) if altTx else (6,7)
		nom_k,alt_k = (9,8) if altFg else (8,9)
		
		self.description        = items[0]
		self.representation     = items[1]
		self.dataType           = eval(items[2])
		self.backgroundColor    = np.array([ int(items[nom_i][:2],16), int(items[nom_i][2:4],16), int(items[nom_i][4:],16) ])
		self.altBackgroundColor = np.array([ int(items[alt_i][:2],16), int(items[alt_i][2:4],16), int(items[alt_i][4:],16) ])
		self.textColor          = np.array([ int(items[nom_j][:2],16), int(items[nom_j][2:4],16), int(items[nom_j][4:],16) ])
		self.altTextColor       = np.array([ int(items[alt_j][:2],16), int(items[alt_j][2:4],16), int(items[alt_j][4:],16) ])
		self.flag               = int(items[nom_k])
		self.altFlag            = int(items[alt_k])
		self.abbreviation       = items[10]
		
		try:
			self.precision = int(items[3])
		except TypeError:
			self.precision = None
		
		try:
			query = """ select u.representation from units u, work_units qu, fields f
						where u.unitID=qu.unitID and qu.parameterID=f.parameterID and f.fieldID='{fieldID}' """.format(fieldID=fieldID)
			self.unit = dbUtils.execute_query(query)[0][0]
			self.set_unit(self.unit) 

		except IndexError:
			self.headerName = self.representation
			self.unit = None
			self.factorToReferenceUnit = None
			self.offsetToReferenceUnit = None
			self.referenceUnit = None

	def __repr__(self):
		"""
		if len(self)==0:
			return '[]'
		elif len(self)==1:
			return '[' + str(self[0]) +']'
		else:
			return '[' + str(self[0]) +', ... '+ str(self[-1]) + ']'
		"""
		return __repr__(self)

	
	def set_abbreviation(self, newAbbreviation):

		self.abbreviation = newAbbreviation
	

	def set_representation(self, newRepresentation):

		self.representation = newRepresentation
		if self.unit:
			self.headerName = newRepresentation + ' ['+self.unit+']'
		else:
			self.headerName = newRepresentation


	def set_unit(self, newUnit):

		self.headerName = self.representation + ' ['+newUnit+']'

		query = """select u.factorToReferenceUnit, u.offsetToReferenceUnit, u.referenceUnit from units u
				where u.representation = '{unit}' """.format(unit=newUnit)
		items = dbUtils.execute_query(query)

		self.unit = newUnit
		self.factorToReferenceUnit = float(items[0][0])
		self.offsetToReferenceUnit = float(items[0][1])
		self.referenceUnit = items[0][2]


	def append(self, newValue):
		if isNoneEntry(newValue) or newValue==None:
			value = physicalValue(None, self.unit)
			value._repr_ = physicalValue(None, self.unit)
		else:
			unit = newValue.unit
			value = self.dataType(newValue)
			value = physicalValue(value, unit)
			value._repr_ = newValue
		super().append(value)


	def put(self, pos, newValue):
		if isNoneEntry(newValue) or newValue==None:
			value = physicalValue(None, self.unit)
			value._repr_ = physicalValue(None, self.unit)
		else:
			unit = newValue.unit
			value = self.dataType(newValue)
			value = physicalValue(value, unit)
			value._repr_ = newValue
		try:
			self[pos] = value
		except IndexError:
			super().append(value)


	def insert(self, pos, newValue):
		if isNoneEntry(newValue) or newValue==None:
			value = physicalValue(None, self.unit)
			value._repr_ = physicalValue(None, self.unit)
		else:
			unit = newValue.unit
			value = self.dataType(newValue)
			value = physicalValue(value, unit)
			value._repr_ = newValue
		super().insert(pos, value)


	def referenceUnitConvert(self):

		for i,value in enumerate(self):
			if isNoneEntry(value):
				newValue = physicalValue( None, self.referenceUnit )
				self[i] = newValue
			else:
				if value.unit==self.referenceUnit:
					newValue = value
				elif value.unit==self.unit:
					newValue = physicalValue( self.factorToReferenceUnit*value + self.offsetToReferenceUnit, self.referenceUnit )
				else:	
					raise(ValueError)
				self[i] = newValue
		return self
	

	def inverseReferenceUnitConvert(self):

		for i,value in enumerate(self):
			if isNoneEntry(value):
				newValue = physicalValue( None, self.unit )
				self[i] = newValue
			else:
				if value.unit==self.unit:
					newValue = value
				elif value.unit==self.referenceUnit:
					newValue = physicalValue( (value-self.offsetToReferenceUnit)/self.factorToReferenceUnit, self.unit )
				else:
					raise(ValueError)
				self[i] = newValue
		return self