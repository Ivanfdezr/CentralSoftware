import re
import numpy as np
import numpy.linalg as la
import codecs
from MdlUtilities import Field, FieldList
import MdlUtilities as mdl
import dbUtils

		 
def set_workUnits_as(unitSystem):

	defaultUnitTable = 'default_{system}_units'.format(system=unitSystem)

	query = """ update work_units,{defaultUnitTable} set work_units.unitID={defaultUnitTable}.unitID 
				where work_units.parameterID={defaultUnitTable}.parameterID """.format(defaultUnitTable=defaultUnitTable)
	dbUtils.execute_query(query)
	#


def get_s2DataSurvey_fields():

	MD   = Field(2001)
	Inc  = Field(2002)
	Azi  = Field(2003)
	TVD  = Field(2004, altBg=True, altFg=True)
	HD   = Field(2005, altBg=True, altFg=True)
	NS   = Field(2006, altBg=True, altFg=True)
	EW   = Field(2007, altBg=True, altFg=True)
	DL   = Field(2008, altBg=True, altFg=True)
	s2DataSurvey_fields = FieldList()
	s2DataSurvey_fields.append( MD  )
	s2DataSurvey_fields.append( Inc )
	s2DataSurvey_fields.append( Azi )
	s2DataSurvey_fields.append( TVD )
	s2DataSurvey_fields.append( HD  )
	s2DataSurvey_fields.append( NS  )
	s2DataSurvey_fields.append( EW  )
	s2DataSurvey_fields.append( DL  )
	
	return s2DataSurvey_fields


def get_s2SurveyTortuosity_fields():

	From       = Field(2056)
	To         = Field(2057)
	Amplitude  = Field(2058)
	Period     = Field(2059)
	Interval   = Field(2060)
	s2SurveyTortuosity_fields = FieldList()
	s2SurveyTortuosity_fields.append( From )
	s2SurveyTortuosity_fields.append( To )
	s2SurveyTortuosity_fields.append( Amplitude )
	s2SurveyTortuosity_fields.append( Period )
	s2SurveyTortuosity_fields.append( Interval )
	
	return s2SurveyTortuosity_fields


def get_s2TortuosityInterval_field():

	s2TortuosityInterval_field = Field(2060)
	return s2TortuosityInterval_field
	
	
def get_s3WellboreIntervals_fields():

	Desc  = Field(2055, altBg=True, altFg=True)
	ID    = Field(2031, altBg=True, altFg=True)
	Drift = Field(2046, altBg=True, altFg=True)
	MDbot = Field(2001, altBg=True, altFg=True)
	MDtop = Field(2001, altBg=True, altFg=True)
	FF    = Field(2027, altBg=True, altFg=True)
	MDbot.set_abbreviation('MDbot')
	MDtop.set_abbreviation('MDtop')
	ID.set_representation('ID / <HID>')
	Drift.set_representation('Drift / <BS>')
	MDbot.set_representation('bottom MD')
	MDtop.set_representation('top MD')
	s3WellboreIntervals_fields = FieldList()
	s3WellboreIntervals_fields.append( Desc  )
	s3WellboreIntervals_fields.append( ID    )
	s3WellboreIntervals_fields.append( Drift )
	s3WellboreIntervals_fields.append( MDtop )
	s3WellboreIntervals_fields.append( MDbot )
	s3WellboreIntervals_fields.append( FF    )
	
	return s3WellboreIntervals_fields


def get_s3PipeCentralizationStage_fields():

	Desc   = Field(2055, altBg=True, altFg=True)
	Length = Field(2080)
	MD     = Field(2001)
	s3PipeCentralizationStage_fields = FieldList()
	s3PipeCentralizationStage_fields.append( Desc   )
	s3PipeCentralizationStage_fields.append( Length )
	s3PipeCentralizationStage_fields.append( MD     )

	return s3PipeCentralizationStage_fields


def get_s3CentralizerSpacing_fields():

	MinSpacing = Field(2071)
	MaxSpacing = Field(2072)
	s3CentralizerSpacing_fields = FieldList()
	s3CentralizerSpacing_fields.append( MinSpacing )
	s3CentralizerSpacing_fields.append( MaxSpacing )

	return s3CentralizerSpacing_fields
	

def get_s3CentralizerProperties_fields():

	Spacing     = Field(2061)
	SO_Midspan  = Field(2062)
	ProdNum     = Field(2050)
	COD         = Field(2011)
	FF          = Field(2027, altBg=True, altFg=True)
	RFF         = Field(2063, altBg=True, altFg=True)
	MinPassThru = Field(2020, substitutefieldID=2010)
	StartF_CH   = Field(2064, substitutefieldID=2015)
	StartF_OH   = Field(2065)
	RestF_CH    = Field(2066, substitutefieldID=2018)
	RestF_OH    = Field(2067)
	s3CentralizerProperties_fields = FieldList()
	s3CentralizerProperties_fields.append( Spacing     )
	s3CentralizerProperties_fields.append( SO_Midspan  )
	s3CentralizerProperties_fields.append( ProdNum     )
	s3CentralizerProperties_fields.append( COD         )
	s3CentralizerProperties_fields.append( FF          )
	s3CentralizerProperties_fields.append( RFF         )
	s3CentralizerProperties_fields.append( MinPassThru )
	s3CentralizerProperties_fields.append( StartF_CH   )
	s3CentralizerProperties_fields.append( StartF_OH   )
	s3CentralizerProperties_fields.append( RestF_CH    )
	s3CentralizerProperties_fields.append( RestF_OH    )
	
	return s3CentralizerProperties_fields


def get_s3PipeProperties_fields():

	Desc            = Field(2055)
	AdjustedWeight  = Field(2032)
	OD              = Field(2030)
	ID              = Field(2031)
	TensileLim      = Field(2034)
	TorsionalLim    = Field(2070)
	Density         = Field(2039)
	E               = Field(2040)
	FFReduction     = Field(2028)
	InnerMudDensity = Field(2077)
	OuterMudDensity = Field(2077)
	InnerMudDensity.set_abbreviation('InnerMudDensity')
	InnerMudDensity.set_representation('Inner Mud Density')
	OuterMudDensity.set_abbreviation('OuterMudDensity')
	OuterMudDensity.set_representation('Outer Mud Density')
	s3PipeProperties_fields = FieldList()
	s3PipeProperties_fields.append( Desc            )
	s3PipeProperties_fields.append( AdjustedWeight  )
	s3PipeProperties_fields.append( OD              )
	s3PipeProperties_fields.append( ID              )
	s3PipeProperties_fields.append( TensileLim      )
	s3PipeProperties_fields.append( TorsionalLim    )
	s3PipeProperties_fields.append( Density         )
	s3PipeProperties_fields.append( E               )
	s3PipeProperties_fields.append( FFReduction     )
	s3PipeProperties_fields.append( InnerMudDensity )
	s3PipeProperties_fields.append( OuterMudDensity )

	return s3PipeProperties_fields


def get_s3CentralizerRunningForce_fields():

	HoleID    = Field(2020, substitutefieldID=2010)
	RunForce  = Field(2016)
	s3CentralizerRunningForce_fields = FieldList()
	s3CentralizerRunningForce_fields.append( HoleID   )
	s3CentralizerRunningForce_fields.append( RunForce )
	
	s3CentralizerRunningForce_fields[0].set_representation('Hole ID')

	return s3CentralizerRunningForce_fields


def get_s3CentralizerLocation_fields():

	MD = Field(2001, altBg=True, altFg=True)
	s3CentralizerLocation_fields = FieldList()
	s3CentralizerLocation_fields.append( MD )
	
	return s3CentralizerLocation_fields


def get_s4Settings_fields():

	WOB = Field(2081)
	TOB = Field(2082)
	TAW = Field(2083)
	s4Settings_fields = FieldList()
	s4Settings_fields.append( WOB )
	s4Settings_fields.append( TOB )
	s4Settings_fields.append( TAW )
	
	return s4Settings_fields


def get_s4DragTorqueSideforce_fields():

	MD     = Field(2001, altBg=True, altFg=True)
	Inc    = Field(2002, altBg=True, altFg=True)
	Drag   = Field(2075, altBg=True, altFg=True)
	Torque = Field(2082, altBg=True, altFg=True)
	SideF  = Field(2074, altBg=True, altFg=True)
	Drag.set_representation('Drag')
	Torque.set_representation('Torque')
	s4DragTorqueSideforce_fields = FieldList()
	s4DragTorqueSideforce_fields.append( MD )
	s4DragTorqueSideforce_fields.append( Inc )
	s4DragTorqueSideforce_fields.append( Drag )
	s4DragTorqueSideforce_fields.append( Torque )
	s4DragTorqueSideforce_fields.append( SideF )
	
	return s4DragTorqueSideforce_fields


def calculate_ASCComplements( fields, tortuosity=None ):

	# Algorithm Reference:
	# 	Mahmoud F. Abughaban et al. Advanced Trajectory Computational Model Improves Calculated Borehole Positioning, Tortuosity and Rugosity.
	# 	IADC/SPE-178796-MS (2016).

	# if not tortuosity:
	# 	max_MD = max(fields.MD)
	# 	tortuosity = [{	'FromMD':mdl.physicalValue(0, fields.MD.unit ),
	# 					'ToMD'  :mdl.physicalValue(max_MD, fields.MD.unit ),
	# 					'Amplitude':mdl.physicalValue(0, fields.MD.unit ),
	# 					'Period':mdl.physicalValue(max_MD, fields.MD.unit ),
	# 					'Interval':mdl.physicalValue(max_MD/500, fields.MD.unit )  }]


	x  = np.array( fields.MD.referenceUnitConvert() )
	In = np.array( fields.Inc.referenceUnitConvert() )
	Az = np.array( fields.Azi.referenceUnitConvert() )

	lE = np.sin(In)*np.sin(Az)
	lN = np.sin(In)*np.cos(Az)
	lV = np.cos(In)
	lH = np.sin(In)

	l = np.array(list(zip(lE,lN,lV,lH)))
	h = np.array(x[1:]-x[:-1])
	u = np.array(2*(h[1:]+h[:-1]))

	v = 6*( (l[2:]-l[1:-1])/h[1:,None] - (l[1:-1]-l[:-2])/h[:-1,None] )
	m = len(v)

	# BEGIN: Tridiagonal matrix algorithm, also known as the Thomas algorithm.

	Ma = []
	Mb = []
	Mc = []

	for i in range(1,m-1):
		Ma.append( h[i] )
		Mb.append( u[i] )
		Mc.append( h[i+1] )

	Ma.insert( 0, 0 )
	Ma.append( h[-2]-h[-1]**2/h[-2] )
	Ma = np.array(Ma)
	Mb.insert( 0, u[0]+h[0]+h[0]**2/h[1] )
	Mb.append( u[-1]+h[-1]+h[-1]**2/h[-2] )
	Mb = np.array(Mb)
	Mc.insert( 0, h[1]-h[0]**2/h[1] )
	Mc.append( 0 )
	Mc = np.array(Mc)

	w = Ma[1:,None]/Mb[:-1,None]

	#

	Mb[1:,None] = Mb[1:,None]-w*Mc[:-1,None]
	v[1:] = v[1:]-w*v[:-1]

	z = [v[-1]/Mb[-1,None]]
	for i in range(2,m+1):
		z.insert( 0, (v[-i]-Mc[-i]*z[0])/Mb[-i] )

	# END: Tridiagonal matrix algorithm.

	"""
	M = np.zeros((m,m))
	M[0,0] = u[0]+h[0]+h[0]**2/h[1] #✓
	M[0,1] = h[1]-h[0]**2/h[1] #✓
	M[-1,-2] = h[-2]-h[-1]**2/h[-2] #✓
	M[-1,-1] = u[-1]+h[-1]+h[-1]**2/h[-2] #✓

	for i in range(1,m-1):
		M[i,i-1] = h[i] #h[i-1]
		M[i,i]   = u[i]
		M[i,i+1] = h[i+1] #h[i]

	M = np.matrix(M)
	z = np.array(M.I*v)
	z = list(z)
	"""

	z.insert( 0, z[0]-h[0]*(z[1]-z[0])/h[1] )   #✓
	z.append( z[-1]+h[-1]*(z[-1]-z[-2])/h[-2] ) #✓
	z = np.array(z)

	A = l[:-1]
	B = (l[1:]-l[:-1])/h[:,None] - h[:,None]*z[1:]/6 - h[:,None]*z[:-1]/3
	C = z[:-1]/2
	D = (z[1:]-z[:-1])/6/h[:,None]

	Y = [np.array([0.0,0.0,x[0],0.0])]
	
	for hi,Ai,Bi,Ci,Di in zip(h,A,B,C,D):
		Y.append( Y[-1] + hi*Ai + hi**2/2*Bi + hi**3/3*Ci + hi**4/4*Di )

	dT = lambda i,X: B[i] + 2*(X-x[i])*C[i] + 3*(X-x[i])**2*D[i]
	T  = lambda i,X: A[i] + (X-x[i])*B[i] + (X-x[i])**2*C[i] + (X-x[i])**3*D[i]
	sT = lambda i,X: (X-x[i])*A[i] + (X-x[i])**2/2*B[i] + (X-x[i])**3/3*C[i] + (X-x[i])**4/4*D[i]

	for Ei,Ni,Vi,Hi in Y:
		fields.EW.append( mdl.physicalValue(Ei, fields.EW.referenceUnit ) )
		fields.NS.append( mdl.physicalValue(Ni, fields.NS.referenceUnit ) )
		fields.TVD.append( mdl.physicalValue(Vi, fields.TVD.referenceUnit ) )
		fields.HD.append( mdl.physicalValue(Hi, fields.HD.referenceUnit ) )

	fields.MD.inverseReferenceUnitConvert()
	fields.Inc.inverseReferenceUnitConvert()
	fields.Azi.inverseReferenceUnitConvert()
	fields.EW.inverseReferenceUnitConvert()
	fields.NS.inverseReferenceUnitConvert()
	fields.TVD.inverseReferenceUnitConvert()
	fields.HD.inverseReferenceUnitConvert()

	if tortuosity:

		MD   = Field(2001)
		Inc  = Field(2002)
		Azi  = Field(2003)
		TVD  = Field(2004)
		HD   = Field(2005)
		NS   = Field(2006)
		EW   = Field(2007)
		DL   = Field(2008)

		ASCComplements = FieldList()
		ASCComplements.append( MD )
		ASCComplements.append( Inc )
		ASCComplements.append( Azi )
		ASCComplements.append( TVD )
		ASCComplements.append( HD )
		ASCComplements.append( NS )
		ASCComplements.append( EW )
		ASCComplements.append( DL )

		for item in tortuosity:
			value = item['FromMD']
			item['FromMD'] = mdl.referenceUnitConvert_value( value, value.unit )
			value = item['ToMD']
			item['ToMD'] = mdl.referenceUnitConvert_value( value, value.unit )
			value = item['Amplitude']
			item['Amplitude'] = mdl.referenceUnitConvert_value( value, value.unit )
			value = item['Period']
			item['Period'] = mdl.referenceUnitConvert_value( value, value.unit )
			value = item['Interval']
			item['Interval'] = mdl.referenceUnitConvert_value( value, value.unit )
		dx = tortuosity[0]['Interval']

		for i,Yi in enumerate(Y[:-1]):
			value = mdl.physicalValue( la.norm(dT(i,x[i])[:-1]), fields.DL.referenceUnit )
			fields.DL.append( value )
			X_ = np.linspace( x[i], x[i+1], np.floor(x[i+1]-x[i])/dx )[:-1]
			if len(X_)==0:
				X_ = [ x[i] ]
			
			for X in X_:
				
				YX = Yi + sT(i,X)
				D2YX = dT(i,X)

				tangentVector = T(i,X)
				enVector = np.array([tangentVector[1],-tangentVector[0],0,0])

				enSize = la.norm(enVector)
				if enSize: enVector = enVector/enSize

				for item in tortuosity:
					a = item['Amplitude']
					w = 2*np.pi/item['Period']

					if X>=item['FromMD'] and X<item['ToMD']:
						YX += enVector*a*np.sin(w*X)
						D2YX -= enVector*a*w**2*np.sin(w*X)
			
				value = mdl.physicalValue( X, MD.referenceUnit )
				MD.append( value )
				value = mdl.physicalValue( YX[0], EW.referenceUnit )
				EW.append( value )
				value = mdl.physicalValue( YX[1], NS.referenceUnit )
				NS.append( value )
				value = mdl.physicalValue( YX[2], TVD.referenceUnit )
				TVD.append( value )
				value = mdl.physicalValue( YX[3], HD.referenceUnit )
				HD.append( value )
				value = mdl.physicalValue( la.norm(D2YX[:-1]), DL.referenceUnit )
				DL.append( value )

		value = mdl.physicalValue( la.norm(dT(i,x[i+1])[:-1]), fields.DL.referenceUnit )
		fields.DL.append( value )
		fields.DL.inverseReferenceUnitConvert()
		MD.inverseReferenceUnitConvert()
		EW.inverseReferenceUnitConvert()
		NS.inverseReferenceUnitConvert()
		TVD.inverseReferenceUnitConvert()
		HD.inverseReferenceUnitConvert()
		DL.inverseReferenceUnitConvert()

		return ASCComplements, dT, T, sT

	else:
		for i,xi in enumerate(x[:-1]):
			value = mdl.physicalValue( la.norm(dT(i,xi)[:-1]), fields.DL.referenceUnit )
			fields.DL.append( value )
		value = mdl.physicalValue( la.norm(dT(i,x[i+1])[:-1]), fields.DL.referenceUnit )
		fields.DL.append( value )
		fields.DL.inverseReferenceUnitConvert()

		return None, dT, T, sT


def adjust_Wt( OD, ID, Wt ):

	# Equation Reference:
	# 	Tenaris Tamsa. Prontuario. p12.

	D = mdl.referenceUnitConvert_value( OD, OD.unit )
	d = mdl.referenceUnitConvert_value( ID, ID.unit )
	a = 10.68/12
	b = 0.00722/12

	t = (D-d)/2
	W = a*(D-t)*t +b*D**2

	return mdl.inverseReferenceUnitConvert_value( W, Wt.unit )


def adjust_ID( OD, ID, Wt ):

	# Equation Reference:
	# 	Tenaris Tamsa. Prontuario. p12.

	D = mdl.referenceUnitConvert_value( OD, OD.unit )
	W = mdl.referenceUnitConvert_value( Wt, Wt.unit )
	a = 10.68/12
	b = 0.00722/12

	d = np.sqrt( D**2 +4*b/a*D**2 -4*W/a )

	return mdl.inverseReferenceUnitConvert_value( d, ID.unit )


class WellboreInnerStageDataItem( dict ):
	
	def __init__(self, row):
		
		super().__init__()
		
		self['row'] = row
		self['Length'] = None
		self['MD'] = None
		self['PipeBase'] = None
		self['Centralization'] = {	'A':{'CentralizerBase':None},
									'B':{'CentralizerBase':None},
									'C':{'CentralizerBase':None},
									'Fields':None	}
		self.setup()

	def setup(self):

		CentralizerA = self['Centralization']['A']['CentralizerBase']
		CentralizerB = self['Centralization']['B']['CentralizerBase']
		CentralizerC = self['Centralization']['C']['CentralizerBase']
		CentralizationFields = self['Centralization']['Fields']

		self['PipeProps'] = None 
		self['Centralization'] = {	'Mode':None,
									'A':{	'Type':None,
											'CentralizerBase':CentralizerA,
											'CentralizerProps':None,
											'RunningForce':None},
									'B':{	'Type':None,
											'CentralizerBase':CentralizerB,
											'CentralizerProps':None,
											'RunningForce':None},
									'C':{	'Type':None,
											'CentralizerBase':CentralizerC,
											'CentralizerProps':None,
											'RunningForce':None},
									'Fields':CentralizationFields}


class WellboreOuterStageDataItem( dict ):
	
	def __init__(self, row):
		
		super().__init__()
		
		self['row'] = row
		self['WellboreProps'] = None
		self['PipeBase']  = None
		self['CaliperData'] = None

		


