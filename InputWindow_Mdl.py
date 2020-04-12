import re
import numpy as np
import numpy.linalg as la
import codecs
import copy
from MdlUtilities import Field, FieldList
import MdlUtilities as mu
import dbUtils

		 
def set_workUnits_as(unitSystem):

	defaultUnitTable = 'default_{system}_units'.format(system=unitSystem)

	query = """ update work_units,{defaultUnitTable} set work_units.unitID={defaultUnitTable}.unitID 
				where work_units.parameterID={defaultUnitTable}.parameterID """.format(defaultUnitTable=defaultUnitTable)
	dbUtils.execute_query(query)


def get_s1Info_fields():

	WellName   = Field(2055, altBg=True, altFg=True)
	Location   = Field(2055, altBg=True, altFg=True)
	Operator   = Field(2055, altBg=True, altFg=True)
	Contractor = Field(2055, altBg=True, altFg=True)
	Date       = Field(2055, altBg=True, altFg=True)
	Directory  = Field(2055, altBg=True, altFg=True)
	WellName.set_abbreviation('WellName')
	Location.set_abbreviation('Location')
	Operator.set_abbreviation('Operator')
	Contractor.set_abbreviation('Contractor')
	Date.set_abbreviation('Date')
	Directory.set_abbreviation('Directory')
	s1Info_fields = FieldList()
	s1Info_fields.append( WellName )
	s1Info_fields.append( Location )
	s1Info_fields.append( Operator )
	s1Info_fields.append( Contractor )
	s1Info_fields.append( Date )
	s1Info_fields.append( Directory )
	
	return s1Info_fields


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


def get_s2KOP_field():

	s2KOP_field = Field(2001)
	s2KOP_field.set_representation('KOP')
	return s2KOP_field


def get_s3Forces_fields():

	AxF  = Field(2075, altBg=True, altFg=True)
	SiF  = Field(2074, altBg=True, altFg=True)
	MD_  = Field(2001, altBg=True, altFg=True)
	MD_.set_abbreviation('MD_AxF')

	s3Forces_fields = FieldList()
	s3Forces_fields.append( AxF )
	s3Forces_fields.append( SiF )
	s3Forces_fields.append( MD_ )

	return s3Forces_fields


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
	Drift.set_representation('Drift / BS')
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

	Desc  = Field(2055, altBg=True, altFg=True)
	MDtop = Field(2001)
	MDbot = Field(2001)
	MDbot.set_abbreviation('MDbot')
	MDtop.set_abbreviation('MDtop')
	MDbot.set_representation('bottom MD')
	MDtop.set_representation('top MD')
	s3PipeCentralizationStage_fields = FieldList()
	s3PipeCentralizationStage_fields.append( Desc  )
	s3PipeCentralizationStage_fields.append( MDtop )
	s3PipeCentralizationStage_fields.append( MDbot )

	return s3PipeCentralizationStage_fields


def get_s3CentralizerSpacing_fields():

	MinSpacing = Field(2071)
	MaxSpacing = Field(2072)
	s3CentralizerSpacing_fields = FieldList()
	s3CentralizerSpacing_fields.append( MinSpacing )
	s3CentralizerSpacing_fields.append( MaxSpacing )

	return s3CentralizerSpacing_fields
	

def get_s3CentralizerProperties_fields():

	ProdNum     = Field(2050)
	COD         = Field(2011)
	IPOD        = Field(2009)
	Length      = Field(2014)
	FF          = Field(2027, altBg=True, altFg=True)
	MinPassThru = Field(2020, substitutefieldID=2010)
	StartF_CH   = Field(2064, substitutefieldID=2015)
	StartF_OH   = Field(2065)
	RestF_CH    = Field(2066, substitutefieldID=2018)
	RestF_OH    = Field(2067)
	s3CentralizerProperties_fields = FieldList()
	s3CentralizerProperties_fields.append( ProdNum     )
	s3CentralizerProperties_fields.append( COD         )
	#s3CentralizerProperties_fields.append( CID         )
	s3CentralizerProperties_fields.append( IPOD        )
	s3CentralizerProperties_fields.append( Length      )
	s3CentralizerProperties_fields.append( FF          )
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
	TensileLim      = Field(2034, altBg=True, altFg=True)
	TorsionalLim    = Field(2070, altBg=True, altFg=True)
	Density         = Field(2039, altBg=True, altFg=True)
	E               = Field(2040, altBg=True, altFg=True)
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

	TAW = Field(2083)
	WOB = Field(2081)
	TOB = Field(2082)
	TrV = Field(2084)
	RoR = Field(2085)
	Psi = Field(2086)
	dMD = Field(2045)
	dMD.set_abbreviation('dMD')
	s4Settings_fields = FieldList()
	s4Settings_fields.append( TAW )
	s4Settings_fields.append( WOB )
	s4Settings_fields.append( TOB )
	s4Settings_fields.append( TrV )
	s4Settings_fields.append( RoR )
	s4Settings_fields.append( Psi )
	s4Settings_fields.append( dMD )
	
	return s4Settings_fields


def get_s4TorqueDragSideforce_fields():

	MD       = Field(2001, altBg=True, altFg=True)
	Inc      = Field(2002, altBg=True, altFg=True)
	Torque_u = Field(2082, altBg=True, altFg=True)
	Torque_s = Field(2082, altBg=True, altFg=True)
	Torque_d = Field(2082, altBg=True, altFg=True)
	Drag_u   = Field(2075, altBg=True, altFg=True)
	Drag_s   = Field(2075, altBg=True, altFg=True)
	Drag_d   = Field(2075, altBg=True, altFg=True)
	SideF    = Field(2074, altBg=True, altFg=True)
	
	uncMD       = Field(2001, altBg=True, altFg=True)
	uncInc      = Field(2002, altBg=True, altFg=True)
	uncTorque_u = Field(2082, altBg=True, altFg=True)
	uncTorque_s = Field(2082, altBg=True, altFg=True)
	uncTorque_d = Field(2082, altBg=True, altFg=True)
	uncDrag_u   = Field(2075, altBg=True, altFg=True)
	uncDrag_s   = Field(2075, altBg=True, altFg=True)
	uncDrag_d   = Field(2075, altBg=True, altFg=True)
	uncSideF    = Field(2074, altBg=True, altFg=True)
	
	Torque_u.set_representation('Torque raising')
	Torque_s.set_representation('Torque static')
	Torque_d.set_representation('Torque lowering')
	Drag_u.set_representation('Drag raising')
	Drag_s.set_representation('Drag static')
	Drag_d.set_representation('Drag lowering')
	
	Torque_u.set_abbreviation('Torque_u')
	Torque_s.set_abbreviation('Torque_s')
	Torque_d.set_abbreviation('Torque_d')
	Drag_u.set_abbreviation('Drag_u')
	Drag_s.set_abbreviation('Drag_s')
	Drag_d.set_abbreviation('Drag_d')
	
	uncMD.set_abbreviation('uncMD')
	uncInc.set_abbreviation('uncInc')
	uncTorque_u.set_abbreviation('uncTorque_u')
	uncTorque_s.set_abbreviation('uncTorque_s')
	uncTorque_d.set_abbreviation('uncTorque_d')
	uncDrag_u.set_abbreviation('uncDrag_u')
	uncDrag_s.set_abbreviation('uncDrag_s')
	uncDrag_d.set_abbreviation('uncDrag_d')
	uncSideF.set_abbreviation('uncSideF')

	s4TorqueDragSideforce_fields = FieldList()
	s4TorqueDragSideforce_fields.append( MD )
	s4TorqueDragSideforce_fields.append( Inc )
	s4TorqueDragSideforce_fields.append( Torque_u )
	s4TorqueDragSideforce_fields.append( Torque_s )
	s4TorqueDragSideforce_fields.append( Torque_d )
	s4TorqueDragSideforce_fields.append( Drag_u )
	s4TorqueDragSideforce_fields.append( Drag_s )
	s4TorqueDragSideforce_fields.append( Drag_d )
	s4TorqueDragSideforce_fields.append( SideF )
	s4TorqueDragSideforce_fields.append( uncMD )
	s4TorqueDragSideforce_fields.append( uncInc )
	s4TorqueDragSideforce_fields.append( uncTorque_u )
	s4TorqueDragSideforce_fields.append( uncTorque_s )
	s4TorqueDragSideforce_fields.append( uncTorque_d )
	s4TorqueDragSideforce_fields.append( uncDrag_u )
	s4TorqueDragSideforce_fields.append( uncDrag_s )
	s4TorqueDragSideforce_fields.append( uncDrag_d )
	s4TorqueDragSideforce_fields.append( uncSideF )
	
	return s4TorqueDragSideforce_fields


def calculate_MCMComplements( fields, KOP, tortuosity=None ):

	# Equation Reference:
	#	Farah Omar Farah. Directional well design, rajectory and survey calculations, with a case study in Fiale, Asal Rift, Djibouti.
	#	United Nations University, Iceland, Reports 2013 Number 27.

	MD  = np.array( fields.MD.referenceUnitConvert() )
	Inc = np.array( fields.Inc.referenceUnitConvert() )
	Azi = np.array( fields.Azi.referenceUnitConvert() )

	θ = np.arccos( np.cos(Inc[1:])*np.cos(Inc[:-1]) + np.sin(Inc[1:])*np.sin(Inc[:-1])*np.cos(Azi[1:]-Azi[:-1]))
	RF = 2/θ*np.tan(θ/2)

	ΔMD  = MD[1:]-MD[:-1]
	ΔEW  = ΔMD/2*( np.sin(I[:-1])*np.sin(Azi[:-1]) + np.sin(I[1:])*np.sin(Azi[1:]) )*RF
	ΔNS  = ΔMD/2*( np.sin(I[:-1])*np.cos(Azi[:-1]) + np.sin(I[1:])*np.cos(Azi[1:]) )*RF
	ΔTVD = ΔMD/2*( np.cos(I[:-1]) + np.cos(I[1:]) )*RF
	ΔHD  = ΔMD/2*( np.sin(I[:-1]) + np.sin(I[1:]) )*RF
	DLS  = θ/ΔMD

	ΔY = np.array( [ΔEW, ΔNS, ΔTVD, ΔHD] )

	Y = [np.array([0.0, 0.0, 0.0, 0.0])]
	
	for i in range(ΔY.shape[1]):
		Y.append( Y[-1] + ΔY[:,i] )

	for Ei,Ni,Vi,Hi in Y:
		fields.EW.append( mu.physicalValue(Ei, fields.EW.referenceUnit ) )
		fields.NS.append( mu.physicalValue(Ni, fields.NS.referenceUnit ) )
		fields.TVD.append( mu.physicalValue(Vi, fields.TVD.referenceUnit ) )
		fields.HD.append( mu.physicalValue(Hi, fields.HD.referenceUnit ) )

	fields.DL.append( mu.physicalValue(0, fields.DL.referenceUnit ) )
	for dl in DL:
		fields.DL.append( mu.physicalValue(dl, fields.DL.referenceUnit ) )

	fields.MD.inverseReferenceUnitConvert()
	fields.Inc.inverseReferenceUnitConvert()
	fields.Azi.inverseReferenceUnitConvert()
	fields.EW.inverseReferenceUnitConvert()
	fields.NS.inverseReferenceUnitConvert()
	fields.TVD.inverseReferenceUnitConvert()
	fields.HD.inverseReferenceUnitConvert()
	fields.DL.inverseReferenceUnitConvert()



def calculate_ASCComplements( fields, KOP, tortuosity=None ):

	# Algorithm Reference:
	# 	Mahmoud F. Abughaban et al. Advanced Trajectory Computational Model Improves Calculated Borehole Positioning, Tortuosity and Rugosity.
	# 	IADC/SPE-178796-MS (2016).

	PL = 480 # inches

	KOP = mu.referenceUnitConvert_value( KOP, KOP.unit )
	x  = np.array( fields.MD.referenceUnitConvert() )
	In = np.array( fields.Inc.referenceUnitConvert() )
	Az = np.array( fields.Azi.referenceUnitConvert() )

	ext = {}
	for i in range(len(x)):
		if x[i]<KOP:
			if (x[i+1]-x[i])>=3*PL:
				ext[i+1] = np.arange(x[i],x[i+1],PL)[1:]
		else:
			break

	K = list(ext.keys())
	K.sort()
	K.reverse()
	for k in K:
		l = len(ext[k])
		x  = np.insert(x,k,ext[k])
		In = np.insert(In,k,np.zeros(l))
		Az = np.insert(Az,k,np.zeros(l))

	lE = np.sin(In)*np.sin(Az)
	lN = np.sin(In)*np.cos(Az)
	lV = np.cos(In)
	lH = np.sin(In)

	#θ = np.arccos( np.cos(In[1:])*np.cos(In[:-1]) + np.sin(In[1:])*np.sin(In[:-1])*np.cos(Az[1:]-Az[:-1]))
	#ΔMD  = x[1:]-x[:-1]
	#DLS  = θ/ΔMD

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

	fields.clear_content()
	for i,(Ei,Ni,Vi,Hi) in enumerate(Y):
		fields.MD.append( mu.physicalValue(x[i], fields.MD.referenceUnit ) )
		fields.Inc.append( mu.physicalValue(In[i], fields.Inc.referenceUnit ) )
		fields.Azi.append( mu.physicalValue(Az[i], fields.Azi.referenceUnit ) )
		fields.EW.append( mu.physicalValue(Ei, fields.EW.referenceUnit ) )
		fields.NS.append( mu.physicalValue(Ni, fields.NS.referenceUnit ) )
		fields.TVD.append( mu.physicalValue(Vi, fields.TVD.referenceUnit ) )
		fields.HD.append( mu.physicalValue(Hi, fields.HD.referenceUnit ) )	

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
			item['FromMD'] = mu.referenceUnitConvert_value( value, value.unit )
			value = item['ToMD']
			item['ToMD'] = mu.referenceUnitConvert_value( value, value.unit )
			value = item['Amplitude']
			item['Amplitude'] = mu.referenceUnitConvert_value( value, value.unit )
			value = item['Period']
			item['Period'] = mu.referenceUnitConvert_value( value, value.unit )
			value = item['Interval']
			item['Interval'] = mu.referenceUnitConvert_value( value, value.unit )
		dx = tortuosity[0]['Interval']

		for i,Yi in enumerate(Y[:-1]):
			value = mu.physicalValue( la.norm(dT(i,x[i])[:-1]), fields.DL.referenceUnit )
			#value = mu.physicalValue( DLS[i], fields.DL.referenceUnit )
			fields.DL.append( value )
			X_ = np.linspace( x[i], x[i+1], np.floor(x[i+1]-x[i])/dx )[:-1]
			if len(X_)==0:
				X_ = [ x[i] ]
			
			for X in X_:
				
				YX = Yi + sT(i,X)
				D2YX = dT(i,X)

				tangentVector = T(i,X)
				verticalVector = np.array([0.0,0.0,1.0,0.0])
				if np.allclose( tangentVector, verticalVector, atol=1e-2 ):
					enVector = np.array([1.0,0.0,0.0,0.0])
				else:
					enVector = np.array([tangentVector[1],-tangentVector[0],0.0,0.0])

				enSize = la.norm(enVector)
				if enSize: enVector = enVector/enSize

				for item in tortuosity:
					a = item['Amplitude']
					w = 2*np.pi/item['Period']

					if X>=item['FromMD'] and X<item['ToMD']:
						YX += enVector*a*np.sin(w*X)
						D2YX -= enVector*a*w**2*np.sin(w*X)
			
				value = mu.physicalValue( X, MD.referenceUnit )
				MD.append( value )
				value = mu.physicalValue( YX[0], EW.referenceUnit )
				EW.append( value )
				value = mu.physicalValue( YX[1], NS.referenceUnit )
				NS.append( value )
				value = mu.physicalValue( YX[2], TVD.referenceUnit )
				TVD.append( value )
				value = mu.physicalValue( YX[3], HD.referenceUnit )
				HD.append( value )
				value = mu.physicalValue( la.norm(D2YX[:-1]), DL.referenceUnit )
				DL.append( value )

		value = mu.physicalValue( la.norm(dT(i,x[i+1])[:-1]), fields.DL.referenceUnit )
		#value = mu.physicalValue( DLS[i], fields.DL.referenceUnit )
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
			value = mu.physicalValue( la.norm(dT(i,xi)[:-1]), fields.DL.referenceUnit )
			fields.DL.append( value )
		value = mu.physicalValue( la.norm(dT(i,x[i+1])[:-1]), fields.DL.referenceUnit )
		fields.DL.append( value )
		fields.DL.inverseReferenceUnitConvert()

		return None, dT, T, sT


def calculate_axialForce_field(self):
	"""
	self must to point to Main_InputWindow
	"""
	print('Calculating Axial Forces...')
	self.msg_label.setText( 'Calculating Axial Forces...' )

	self.s3Forces_fields.AxialF.clear()
	self.s3Forces_fields.MD_AxF.clear()
	MD_array = np.array( self.s2DataSurvey_fields.MD )
	MD_min = mu.referenceUnitConvert_value( MD_array[ 0], self.s2DataSurvey_fields.MD.unit )
	MD_max = mu.referenceUnitConvert_value( MD_array[-1], self.s2DataSurvey_fields.MD.unit )
	del MD_array

	MDs = np.linspace(MD_min, MD_max, 100)
	cosIncs = []

	for MD in MDs:
		MD = mu.physicalValue(MD, self.s3Forces_fields.MD_AxF.referenceUnit )
		self.s3Forces_fields.MD_AxF.append( MD )
		cosIncs.append( get_ASCT_from_MD(self, MD, MD.unit)[2] )

	value = mu.physicalValue(0, self.s3Forces_fields.AxialF.referenceUnit )
	self.s3Forces_fields.AxialF.append( value )
	AxialTension = 0
	L = MDs[1]-MDs[0]

	K = list(self.wellboreInnerStageData.keys())
	K.sort()
	for i in range(len(MDs)-1):	
		for k in K:
			stage = self.wellboreInnerStageData[k]
			stageBottomMD = mu.referenceUnitConvert_value( stage['MD'], stage['MD'].unit )
			W = mu.referenceUnitConvert_value( stage['PipeProps'].PW[0], stage['PipeProps'].PW[0].unit )
			
			if MDs[-i-2]<stageBottomMD: 
				AxialTension = AxialTension + W*L*cosIncs[-i-1]
				value = mu.physicalValue(AxialTension, self.s3Forces_fields.AxialF.referenceUnit )
				self.s3Forces_fields.AxialF.insert(0, value )
				break

	self.s3Forces_fields.AxialF.inverseReferenceUnitConvert()
	self.s3Forces_fields.MD_AxF.inverseReferenceUnitConvert()
	self.s3UpdateAxialF_pushButton.setEnabled(False)
	self.s3InnerStageToolkit_tabWidget.setEnabled(True)

	self.msg_label.setText( '' )
	print('Finish')


def get_axialTension_below_MD(self, MD, unit=None, referenceUnit=False):

	if unit:
		MD = mu.unitConvert_value( MD, unit, self.s3Forces_fields.MD_AxF.unit )
	else:
		MD = mu.unitConvert_value( MD, MD.unit, self.s3Forces_fields.MD_AxF.unit )
	
	cosInc = get_ASCT_from_MD(self, MD)[2]
	MD_AxF = np.array( self.s3Forces_fields.MD_AxF )
	AxialF = np.array( self.s3Forces_fields.AxialF )
	index = np.where(MD_AxF>MD)[0][0]

	MD_AxF_i = MD_AxF[index]
	AxialF_i = AxialF[index]
	del MD_AxF
	del AxialF

	stage = self.currentWellboreInnerStageDataItem
	stageBottomMD = mu.referenceUnitConvert_value( stage['MD'], stage['MD'].unit )
	assert( MD<stageBottomMD )
	W = mu.referenceUnitConvert_value( stage['PipeProps'].PW[0], stage['PipeProps'].PW[0].unit )
	L = MD_AxF_i-MD

	AxialTension = AxialF_i + W*L*cosInc
	if referenceUnit:
		AxialTension = mu.physicalValue( AxialTension, self.s3Forces_fields.AxialF.referenceUnit )
	else:
		AxialTension = mu.inverseReferenceUnitConvert_value( AxialTension, self.s3Forces_fields.AxialF.unit )

	return AxialTension


def adjust_Wt( OD, ID, Wt ):

	# Equation Reference:
	# 	Tenaris Tamsa. Prontuario. p12.

	D = mu.referenceUnitConvert_value( OD, OD.unit )
	d = mu.referenceUnitConvert_value( ID, ID.unit )
	a = 10.68/12
	b = 0.00722/12

	t = (D-d)/2
	W = a*(D-t)*t +b*D**2

	return mu.inverseReferenceUnitConvert_value( W, Wt.unit )


def adjust_ID( OD, ID, Wt ):

	# Equation Reference:
	# 	Tenaris Tamsa. Prontuario. p12.

	D = mu.referenceUnitConvert_value( OD, OD.unit )
	W = mu.referenceUnitConvert_value( Wt, Wt.unit )
	a = 10.68/12
	b = 0.00722/12

	d = np.sqrt( D**2 +4*b/a*D**2 -4*W/a )

	return mu.inverseReferenceUnitConvert_value( d, ID.unit )


def get_ASCCoordinates_from_MD(self, MD, unit=None):
	"""
	self must to point to Main_InputWindow
	"""
	if unit:
		MD = mu.unitConvert_value( MD, unit, self.s2DataSurvey_fields.MD.unit )
	else:
		MD = mu.unitConvert_value( MD, MD.unit, self.s2DataSurvey_fields.MD.unit )

	MD_array = np.array( self.s2DataSurvey_fields.MD )
	try:
		index = np.where(MD_array[:-1]<=MD)[0][-1]
	except IndexError:
		index = 0
	del MD_array

	MD = mu.referenceUnitConvert_value( MD, MD.unit )
	sT_value = self.sT( index, MD)
	EW_rest = mu.inverseReferenceUnitConvert_value( sT_value[0], self.s2DataSurvey_fields.EW.unit  )
	NS_rest = mu.inverseReferenceUnitConvert_value( sT_value[1], self.s2DataSurvey_fields.NS.unit  )
	VD_rest = mu.inverseReferenceUnitConvert_value( sT_value[2], self.s2DataSurvey_fields.TVD.unit )

	EW = self.s2DataSurvey_fields.EW[index] + EW_rest
	NS = self.s2DataSurvey_fields.NS[index] + NS_rest
	VD = self.s2DataSurvey_fields.TVD[index] + VD_rest

	return EW,NS,VD,index


def get_ASCT_from_MD(self, MD, unit=None):
	"""
	self must to point to Main_InputWindow
	"""
	if unit:
		MD = mu.unitConvert_value( MD, unit, self.s2DataSurvey_fields.MD.unit )
	else:
		MD = mu.unitConvert_value( MD, MD.unit, self.s2DataSurvey_fields.MD.unit )

	MD_array = np.array( self.s2DataSurvey_fields.MD )
	try:
		index = np.where(MD_array[:-1]<=MD)[0][-1]
	except IndexError:
		index = 0
	del MD_array
	
	MD = mu.referenceUnitConvert_value( MD, MD.unit )
	T_value = self.T( index, MD)
	return T_value


def get_ASCDogleg_from_MD(self, MD, unit=None):
	"""
	self must to point to Main_InputWindow
	"""
	if unit:
		MD = mu.unitConvert_value( MD, unit, self.s2DataSurvey_fields.MD.unit )
	else:
		MD = mu.unitConvert_value( MD, MD.unit, self.s2DataSurvey_fields.MD.unit )

	MD_array = np.array( self.s2DataSurvey_fields.MD )
	try:
		index = np.where(MD_array[:-1]<=MD)[0][-1]
	except IndexError:
		index = 0
	del MD_array

	MD = mu.referenceUnitConvert_value( MD, MD.unit )
	DL = la.norm( self.dT( index, MD )[:-1] )
	DL = mu.inverseReferenceUnitConvert_value( DL, self.s2DataSurvey_fields.DL.unit  )

	return DL


def get_inclination_and_azimuth_from_locations(self, locations):
	"""
	self must to point to Main_InputWindow
	"""
	"""
	Return "Inc" and "Azi" array objects in reference units.
	"""
	Inc = []
	Azi = []
	for MD in locations:
		T_values = get_ASCT_from_MD(self, MD)
		aux = 1.0 if np.isclose(T_values[2],1.0,rtol=1e-3,atol=0) else T_values[2]
		inc = np.arccos( aux )

		if inc==0.0:
			azi = 0.0
		else:
			sinazi = T_values[0]/np.sin(inc)
			cosazi = T_values[1]/np.sin(inc)

			if sinazi>=0:
				azi = np.arccos( cosazi )
			elif sinazi<0:
				azi = 2*np.pi-np.arccos( cosazi )

		Inc.append(inc)
		Azi.append(azi)

	return np.array(Inc), np.array(Azi)


def get_centralizersEnsembleLength(self):

	gap = mu.referenceUnitConvert_value( 2.0, 'm' )

	CEL = 0
	for x, c in self.centralizers.items():
		if c['Type']!=None:
			CL = c['CentralizerBase'].CL[0]
			mu.referenceUnitConvert_value( CL, CL.unit )
			CEL += CL + gap

	return CEL


def calculate_standOff_atCentralizers(self, locations, SOatC_field, ClatC_field, LatC_field):

	locations.referenceUnitConvert()
	SOatC_field.referenceUnitConvert()
	ClatC_field.referenceUnitConvert()
	numofLocations = len(locations)

	Inc, Azi = get_inclination_and_azimuth_from_locations(self.parent, locations)
	MDs = locations.factorToReferenceUnit*self.MD
	IDs = self.parent.s3WellboreIntervals_fields.ID.factorToReferenceUnit*self.ID
	meanIDs = self.parent.s3WellboreIntervals_fields.ID.factorToReferenceUnit*self.mean_ID

	PD = self.stage['PipeProps'].OD[0]
	Pd = self.stage['PipeProps'].ID[0]
	PE = self.stage['PipeProps'].E[0]
	PW = self.stage['PipeProps'].PW[0]
	PL = self.stage['PipeBase'].PL[0]
	ρi = self.stage['PipeProps'].InnerMudDensity[0]
	ρe = self.stage['PipeProps'].OuterMudDensity[0]
	ρs = self.stage['PipeProps'].Density[0]

	PD = mu.referenceUnitConvert_value( PD, PD.unit )
	Pd = mu.referenceUnitConvert_value( Pd, Pd.unit )
	PE = mu.referenceUnitConvert_value( PE, PE.unit )
	PW = mu.referenceUnitConvert_value( PW, PW.unit )
	PL = mu.referenceUnitConvert_value( PL, PL.unit )
	ρi = mu.referenceUnitConvert_value( ρi, ρi.unit )
	ρe = mu.referenceUnitConvert_value( ρe, ρe.unit )
	ρs = mu.referenceUnitConvert_value( ρs, ρs.unit )

	ResF = {}
	D = {}
	d = {}
	CL = {}
	B = {}
	supports = 0

	for x, c in self.centralizers.items():
		if c['Type']=='Bow Spring':
			ResF[x] = c['CentralizerProps'].ResF_CH[0]
			ResF[x] = mu.referenceUnitConvert_value( ResF[x], ResF[x].unit )
			D[x] = c['CentralizerProps'].COD[0]
			D[x] = mu.referenceUnitConvert_value( D[x], D[x].unit )
			d[x] = c['CentralizerProps'].IPOD[0]
			d[x] = mu.referenceUnitConvert_value( d[x], d[x].unit )
			CL[x] = c['CentralizerBase'].CL[0]
			CL[x] = mu.referenceUnitConvert_value( CL[x], CL[x].unit )
			supports+=1

		elif c['Type']=='Rigid':
			D[x] = c['CentralizerProps'].COD[0]
			D[x] = mu.referenceUnitConvert_value( D[x], D[x].unit )
			CL[x] = c['CentralizerBase'].CL[0]
			CL[x] = mu.referenceUnitConvert_value( CL[x], CL[x].unit )
			B[x] = int(c['CentralizerBase'].Blades[0])
			supports+=1#c['CentralizerBase'].Blades[0]

	buoyancyFactor = mu.calculate_buoyancyFactor( OD=PD, ID=Pd, ρs=ρs, ρe=ρe, ρi=ρi )
	PW *= buoyancyFactor/supports
	PI = np.pi/64*(PD**4-Pd**4)
	PR = PD/2
	CEL = get_centralizersEnsembleLength(self)

	def calculate_SO_per_centralizersEnsemble():
		SO = []
		Cc = []
		L = []
		Δ = 0
		for x, c in self.centralizers.items():
			#if c['Type']=='Bow Spring':
			if c['Type']!=None:
				so, cc, l = calculate_SO_per_centralizer(x,c['Type'],supports,Δ)
				Δ += CL[x]
				SO.append( so )
				Cc.append( cc )
				L.append( l )
			#elif c['Type']=='Rigid':
			#	so, cc, l = calculate_SO_per_centralizer(x)
			#	SO += so/supports #*c['CentralizerBase'].Blades[0]/supports
			#	Cc += cc/supports #*c['CentralizerBase'].Blades[0]/supports
			#	L.append(l)
		return np.mean(SO), np.mean(Cc), np.mean(L)

	def get_Hr_mHr_R_L(label, MD0, MD1, MD2, inc):

		MDi = MDs[0]
		IDi = IDs[0]
		mIDi = meanIDs[0]
		for MDj,IDj,mIDj in zip(MDs,IDs,meanIDs):
			if MD1<MDj:
				Hd = (MD1-MDi)/(MDj-MDi)*(IDj-IDi)+IDi
				mHd = (MD1-MDi)/(MDj-MDi)*(mIDj-mIDi)+mIDi
				break
			else:
				MDi = MDj
				IDi = IDj
				mIDi = mIDj

		Hr = Hd/2
		mHr = mHd/2
		R = D[label]/2
		δ = Hr-PR

		if MD0==None and MD2==None:
			L = (384*PE*PI*δ/PW/np.sin(inc))**0.25
		elif MD0==None:
			Lalt = (384*PE*PI*δ/PW/np.sin(inc))**0.25/2
			L21 = (MD2-MD1)/2
			L21 = L21 if (L21<Lalt) else Lalt
			L = L21 + Lalt
		elif MD2==None:
			Lalt = (384*PE*PI*δ/PW/np.sin(inc))**0.25/2
			L10 = (MD1-MD0)/2
			L10 = L10 if (L10<Lalt) else Lalt
			L = L10 + Lalt
		else:
			Lalt = (384*PE*PI*δ/PW/np.sin(inc))**0.25/2
			L21 = (MD2-MD1)/2
			L21 = L21 if (L21<Lalt) else Lalt
			L10 = (MD1-MD0)/2
			L10 = L10 if (L10<Lalt) else Lalt
			L = L21 + L10

		return Hr,mHr,R,L
		
	for j, (MD1,inc) in enumerate(zip(locations,Inc)):

		if MD1+CEL>MDs[-1]:
			locations.pop()
			Inc.pop()
			break

		inc += 1e-12
		i = j-1
		k = j+1
		if i==-1:
			MD0 = None
		else:
			MD0 = locations[i]+CEL
			if MD0>MD1:
				raise(mu.LogicalError)
		if k==numofLocations:
			MD2 = None
		else:
			MD2 = locations[k]
			if MD1+CEL>MD2:
				raise(mu.LogicalError)

		def calculate_SO_per_centralizer(label,ctype,supports,ΔMD1):
			"""
			Define before use: MD0, MD1, MD2, inc
			Return "SO, Cc, L" in reference units.
			"""
			MD1_ = MD1 + ΔMD1

			if ctype=='Bow Spring':
				
				Hr,mHr,R,L = get_Hr_mHr_R_L(label, MD0, MD1_, MD2, inc)

				f = PW*L*np.sin(inc)/supports
				resK = 2*ResF[label]/( D[label]-d[label]-0.67*(Hr*2-PD) )

				y = f/resK
				Rmin = PR+(R-PR)*0.1
				R = (R-y) if (R<Hr) else (Hr-y)
				R = Rmin if (R<Rmin) else R

				mHc = mHr-PR
				Cc = R-PR-(Hr-mHr)
				SO = Cc/mHc

			elif ctype=='Rigid':

				SO_ = []
				Cc_ = []
				L_  = []

				for i in range(B[label]):
					Hr,mHr,R,L = get_Hr_mHr_R_L(label, MD0, MD1_, MD2, inc)

					mHc = mHr-PR
					cc = R-PR-(Hr-mHr)
					Cc_.append( cc )
					SO_.append( cc/mHc )
					L_.append( L )

					MD1_ += CL[label]/B[label]

				Cc = np.mean( Cc_ )
				SO = np.mean( SO_ )
				L = np.mean( L_ )
			
			return SO, Cc, L
		
		SO, Cc, L = calculate_SO_per_centralizersEnsemble()

		mu.create_physicalValue_and_appendTo_field( SO, SOatC_field, SOatC_field.referenceUnit )
		mu.create_physicalValue_and_appendTo_field( Cc, ClatC_field, ClatC_field.referenceUnit )
		if LatC_field!=None:
			mu.create_physicalValue_and_appendTo_field( L, LatC_field, LatC_field.referenceUnit )

	SOatC_field.inverseReferenceUnitConvert()
	ClatC_field.inverseReferenceUnitConvert()
	if LatC_field!=None:
		LatC_field.inverseReferenceUnitConvert()
	locations.inverseReferenceUnitConvert()


def calculate_standOff_atMidspan(self, locations, ClatC_field, SOatM_field, ClatM_field, Inc_field):

	locations.referenceUnitConvert()
	ClatC_field.referenceUnitConvert()
	SOatM_field.referenceUnitConvert()
	ClatM_field.referenceUnitConvert()
	Inc_field.clear()

	Inc, Azi = get_inclination_and_azimuth_from_locations(self.parent, locations)

	MDs = locations.factorToReferenceUnit*self.MD
	IDs = self.parent.s3WellboreIntervals_fields.ID.factorToReferenceUnit*self.ID
	meanIDs = self.parent.s3WellboreIntervals_fields.ID.factorToReferenceUnit*self.mean_ID

	PD = self.stage['PipeProps'].OD[0]
	Pd = self.stage['PipeProps'].ID[0]
	PE = self.stage['PipeProps'].E[0]
	PW = self.stage['PipeProps'].PW[0]
	PL = self.stage['PipeBase'].PL[0]
	ρi = self.stage['PipeProps'].InnerMudDensity[0]
	ρe = self.stage['PipeProps'].OuterMudDensity[0]
	ρs = self.stage['PipeProps'].Density[0]

	PD = mu.referenceUnitConvert_value( PD, PD.unit )
	Pd = mu.referenceUnitConvert_value( Pd, Pd.unit )
	PE = mu.referenceUnitConvert_value( PE, PE.unit )
	PW = mu.referenceUnitConvert_value( PW, PW.unit )
	PL = mu.referenceUnitConvert_value( PL, PL.unit )
	gap = mu.referenceUnitConvert_value( 2.0, 'm' )

	CEL = get_centralizersEnsembleLength(self)

	buoyancyFactor = mu.calculate_buoyancyFactor( OD=PD, ID=Pd, ρs=ρs, ρe=ρe, ρi=ρi )
	PW *= buoyancyFactor
	PI = np.pi/64*(PD**4-Pd**4)
	PR = PD/2

	mu.create_physicalValue_and_appendTo_field( Inc[0], Inc_field, Inc_field.referenceUnit )

	for i in range(len(locations)-1):
		j = i+1
		MD1 = locations[i]+CEL
		MD2 = locations[j]
		In1 = Inc[i]
		In2 = Inc[j]
		Az1 = Azi[i]
		Az2 = Azi[j]
		L = MD2-MD1
		MDm = MD1 + L/2

		MDi = MDs[0]
		IDi = IDs[0]
		mIDi = meanIDs[0]
		for MDj,IDj,mIDj in zip(MDs,IDs,meanIDs):
			if MDm<MDj:
				Hd = (MDm-MDi)/(MDj-MDi)*(IDj-IDi)+IDi
				mHd = (MDm-MDi)/(MDj-MDi)*(mIDj-mIDi)+mIDi
				break
			else:
				MDi = MDj
				IDi = IDj
				mIDi = mIDj
		
		Ft = get_axialTension_below_MD(self.parent, MD2, referenceUnit=True)

		u = np.sqrt( Ft*L**2/4/PE/PI )
		β = np.arccos( np.cos(In1)*np.cos(In2) + np.sin(In1)*np.sin(In2)*np.cos(Az2-Az1) )
		
		if β==0.0:
			δ = 0.0
		else:
			cosγ0 = np.sin(In1)*np.sin(In2)*np.sin(Az2-Az1)/np.sin(β)
			cosγn = np.sin( (In1-In2)/2 )*np.sin( (In1+In2)/2 )/np.sin(β/2)

			Fldp = PW*L*cosγn + 2*Ft*np.sin(β/2)
			Flp  = PW*L*cosγ0
			Fl   = np.sqrt( Fldp**2 + Flp**2 )

			δ = Fl*L**3/384/PE/PI*24/u**4*(u**2/2 - u*(np.cosh(u)-1)/np.sinh(u) )
		
		c1 = ClatC_field[i]
		c2 = ClatC_field[j]

		Hr = Hd/2
		mHr = mHd/2
		mHc = mHr-PR
		Mc = (c1+c2)/2-δ
		xHc = mHr-Hr
		Mc = Mc if (Mc>xHc) else xHc
		SO = Mc/mHc

		mu.create_physicalValue_and_appendTo_field( In2, Inc_field, Inc_field.referenceUnit )
		mu.create_physicalValue_and_appendTo_field( SO, SOatM_field, SOatM_field.referenceUnit )
		mu.create_physicalValue_and_appendTo_field( Mc, ClatM_field, ClatM_field.referenceUnit )

	mu.create_physicalValue_and_appendTo_field( 0, SOatM_field, SOatM_field.referenceUnit )
	mu.create_physicalValue_and_appendTo_field( 0, ClatM_field, ClatM_field.referenceUnit )

	locations.inverseReferenceUnitConvert()
	ClatC_field.inverseReferenceUnitConvert()
	SOatM_field.inverseReferenceUnitConvert()
	ClatM_field.inverseReferenceUnitConvert()
	Inc_field.inverseReferenceUnitConvert()


def calculate_psiAngle( self, diameter ):

	self.s4Settings_fields.TrV.referenceUnitConvert()
	self.s4Settings_fields.RoR.referenceUnitConvert()
	radius = mu.referenceUnitConvert_value( diameter/2, diameter.unit )

	Psi = np.arctan( self.s4Settings_fields.TrV[0]/self.s4Settings_fields.RoR[0]/radius )
	Psi = mu.physicalValue( Psi, self.s4Settings_fields.Psi.referenceUnit )
	self.s4Settings_fields.Psi.append( Psi )

	self.s4Settings_fields.TrV.inverseReferenceUnitConvert()
	self.s4Settings_fields.RoR.inverseReferenceUnitConvert()


def set_stepMD( self ):

	step = self.wellboreInnerStageData[0]['PipeBase'].PL[0]
	step = mu.referenceUnitConvert_value( step*2, step.unit )
	self.s4Settings_fields.dMD.append( step )


def calculate_TDS_for_uncentralizedStage(self, stage, FT1=None, MDLims=None, centralizedStage=False ):

	TDS_fields = self.s4TorqueDragSideforce_fields

	PD = stage['PipeProps'].OD[0]
	Pd = stage['PipeProps'].ID[0]
	PW = stage['PipeProps'].PW[0]
	ρi = stage['PipeProps'].InnerMudDensity[0]
	ρe = stage['PipeProps'].OuterMudDensity[0]
	ρs = stage['PipeProps'].Density[0]
	ff = stage['PipeBase'].FF[0]

	PD = mu.referenceUnitConvert_value( PD, PD.unit )
	Pd = mu.referenceUnitConvert_value( Pd, Pd.unit )
	PW = mu.referenceUnitConvert_value( PW, PW.unit )
	ρi = mu.referenceUnitConvert_value( ρi, ρi.unit )
	ρe = mu.referenceUnitConvert_value( ρe, ρe.unit )
	ρs = mu.referenceUnitConvert_value( ρs, ρs.unit )
	ff = mu.referenceUnitConvert_value( ff, ff.unit )

	if MDLims==None:
		stageBottomMD = mu.referenceUnitConvert_value( stage['MD'], stage['MD'].unit )
		stageTopMD = stageBottomMD - mu.referenceUnitConvert_value( stage['Length'], stage['Length'].unit )
	else:
		stageBottomMD = MDLims[1]
		stageTopMD = MDLims[0]

	if FT1==None:
		self.s4Settings_fields.WOB.referenceUnitConvert()
		self.s4Settings_fields.TOB.referenceUnitConvert()
		self.s4Settings_fields.TAW.referenceUnitConvert()

		F1 = -self.s4Settings_fields.WOB[0] -self.s4Settings_fields.TAW[0]
		T1 = self.s4Settings_fields.TOB[0]
		Fu = [F1]
		Fs = [F1]
		Fd = [F1]
		Tu = [T1]
		Ts = [T1]
		Td = [T1]

		self.s4Settings_fields.WOB.inverseReferenceUnitConvert()
		self.s4Settings_fields.TOB.inverseReferenceUnitConvert()
		self.s4Settings_fields.TAW.inverseReferenceUnitConvert()
	else:
		Fu = [FT1['Fu']]
		Fs = [FT1['Fs']]
		Fd = [FT1['Fd']]
		Tu = [FT1['Tu']]
		Ts = [FT1['Ts']]
		Td = [FT1['Td']]
	SF = [0]

	buoyancyFactor = mu.calculate_buoyancyFactor( OD=PD, ID=Pd, ρs=ρs, ρe=ρe, ρi=ρi )
	ffReduction = mu.referenceUnitConvert_value( 	stage['PipeProps'].FFReduction[0], 
													stage['PipeProps'].FFReduction[0].unit )
	ff = ff*(1-ffReduction)

	n = np.ceil( (stageBottomMD-stageTopMD)/self.s4Settings_fields.dMD[0] )
	MD = np.linspace( stageTopMD, stageBottomMD, n+1 )
	MD = list(MD)
	L = MD[1]-MD[0]
	MD.reverse()
	physicalMD_function = lambda md: mu.physicalValue(md, TDS_fields.MD.referenceUnit)
	physicalMD = map(physicalMD_function, MD)
	
	Inc, Azi = get_inclination_and_azimuth_from_locations(self, physicalMD)
	DL = np.arccos( np.sin(Inc[:-1])*np.sin(Inc[1:])*np.cos(Azi[1:]-Azi[:-1]) + np.cos(Inc[:-1])*np.cos(Inc[1:]) )

	dlThreshold = 1.5/180*np.pi
	floatedW = buoyancyFactor*L*PW
	sinPsi = np.sin(self.s4Settings_fields.Psi[0])
	cosPsi = np.cos(self.s4Settings_fields.Psi[0])
	r = PD/2

	i = 1
	for DLi in DL:
		
		absDLi = abs(DLi)
		
		if absDLi>dlThreshold:
			
			axialForce = floatedW*( np.sin(Inc[i])-np.sin(Inc[i-1]) )/(Inc[i]-Inc[i-1])
			normalForce = Fs[-1]*absDLi
			raisingNormalForce  = Fu[-1]*( np.exp(+ff*absDLi) -1)*sinPsi
			loweringNormalForce = Fd[-1]*( np.exp(-ff*absDLi) -1)*sinPsi
			unForcedCurveTorque = ff*r*absDLi*cosPsi
			
			SF.append( normalForce )

			Tu.append( Tu[-1] + Fu[-1]*unForcedCurveTorque )
			Ts.append( Ts[-1] + Fs[-1]*unForcedCurveTorque )
			Td.append( Td[-1] + Fd[-1]*unForcedCurveTorque )

			Fu.append( Fu[-1] + raisingNormalForce + axialForce)
			Fs.append( Fs[-1] + axialForce)
			Fd.append( Fd[-1] + loweringNormalForce + axialForce)
			
		else:	
			axialForce  = floatedW*np.cos( Inc[i] )
			normalForce = floatedW*np.sin( Inc[i] )
			raisingNormalForce  = normalForce*ff*sinPsi
			loweringNormalForce = -raisingNormalForce
			straightTorque = ff*r*normalForce*cosPsi

			SF.append( normalForce )
			
			Tu.append( Tu[-1] + straightTorque )
			Ts.append( Ts[-1] + straightTorque )
			Td.append( Td[-1] + straightTorque )

			Fu.append( Fu[-1] + raisingNormalForce + axialForce)
			Fs.append( Fs[-1] + axialForce)
			Fd.append( Fd[-1] + loweringNormalForce + axialForce)

		i+=1

	for i in range(len(DL)):
		
		if centralizedStage:
			mu.create_physicalValue_and_appendTo_field( MD[i], TDS_fields.MD, 'referenceUnit' )
			mu.create_physicalValue_and_appendTo_field( Inc[i], TDS_fields.Inc, 'referenceUnit' )
			mu.create_physicalValue_and_appendTo_field( SF[i], TDS_fields.SideF, 'referenceUnit' )
			mu.create_physicalValue_and_appendTo_field( Tu[i], TDS_fields.Torque_u, 'referenceUnit' )
			mu.create_physicalValue_and_appendTo_field( Ts[i], TDS_fields.Torque_s, 'referenceUnit' )
			mu.create_physicalValue_and_appendTo_field( Td[i], TDS_fields.Torque_d, 'referenceUnit' )
			mu.create_physicalValue_and_appendTo_field( Fu[i], TDS_fields.Drag_u, 'referenceUnit' )
			mu.create_physicalValue_and_appendTo_field( Fs[i], TDS_fields.Drag_s, 'referenceUnit' )
			mu.create_physicalValue_and_appendTo_field( Fd[i], TDS_fields.Drag_d, 'referenceUnit' )
		else:
			mu.create_physicalValue_and_appendTo_field( MD[i], TDS_fields.uncMD, 'referenceUnit' )
			mu.create_physicalValue_and_appendTo_field( Inc[i], TDS_fields.uncInc, 'referenceUnit' )
			mu.create_physicalValue_and_appendTo_field( SF[i], TDS_fields.uncSideF, 'referenceUnit' )
			mu.create_physicalValue_and_appendTo_field( Tu[i], TDS_fields.uncTorque_u, 'referenceUnit' )
			mu.create_physicalValue_and_appendTo_field( Ts[i], TDS_fields.uncTorque_s, 'referenceUnit' )
			mu.create_physicalValue_and_appendTo_field( Td[i], TDS_fields.uncTorque_d, 'referenceUnit' )
			mu.create_physicalValue_and_appendTo_field( Fu[i], TDS_fields.uncDrag_u, 'referenceUnit' )
			mu.create_physicalValue_and_appendTo_field( Fs[i], TDS_fields.uncDrag_s, 'referenceUnit' )
			mu.create_physicalValue_and_appendTo_field( Fd[i], TDS_fields.uncDrag_d, 'referenceUnit' )


def calculate_TDS_for_centralizedStage(self, stage ):

	PD = stage['PipeProps'].OD[0]
	Pd = stage['PipeProps'].ID[0]
	PW = stage['PipeProps'].PW[0]
	PL = stage['PipeBase'].PL[0]
	ρi = stage['PipeProps'].InnerMudDensity[0]
	ρe = stage['PipeProps'].OuterMudDensity[0]
	ρs = stage['PipeProps'].Density[0]
	ff = stage['PipeBase'].FF[0]

	PD = mu.referenceUnitConvert_value( PD, PD.unit )
	Pd = mu.referenceUnitConvert_value( Pd, Pd.unit )
	PW = mu.referenceUnitConvert_value( PW, PW.unit )
	PL = mu.referenceUnitConvert_value( PL, PL.unit )
	ρi = mu.referenceUnitConvert_value( ρi, ρi.unit )
	ρe = mu.referenceUnitConvert_value( ρe, ρe.unit )
	ρs = mu.referenceUnitConvert_value( ρs, ρs.unit )
	ff = mu.referenceUnitConvert_value( ff, ff.unit )

	stageBottomMD = mu.referenceUnitConvert_value( stage['MD'], stage['MD'].unit )
	stageTopMD = stageBottomMD - mu.referenceUnitConvert_value( stage['Length'], stage['Length'].unit )

	self.s4Settings_fields.WOB.referenceUnitConvert()
	self.s4Settings_fields.TOB.referenceUnitConvert()
	self.s4Settings_fields.TAW.referenceUnitConvert()

	F1 = -self.s4Settings_fields.WOB[0] -self.s4Settings_fields.TAW[0]
	T1 = self.s4Settings_fields.TOB[0]
	FT1 = {	'Fu':F1,
			'Fs':F1,
			'Fd':F1,
			'Tu':T1,
			'Ts':T1,
			'Td':T1	 }

	self.s4Settings_fields.WOB.inverseReferenceUnitConvert()
	self.s4Settings_fields.TOB.inverseReferenceUnitConvert()
	self.s4Settings_fields.TAW.inverseReferenceUnitConvert()
	
	SF = [0]

	buoyancyFactor = mu.calculate_buoyancyFactor( OD=PD, ID=Pd, ρs=ρs, ρe=ρe, ρi=ρi )
	ffReduction = mu.referenceUnitConvert_value( 	stage['PipeProps'].FFReduction[0], 
													stage['PipeProps'].FFReduction[0].unit )
	ff = ff*(1-ffReduction)

	sinPsi = np.sin(self.s4Settings_fields.Psi[0])
	cosPsi = np.cos(self.s4Settings_fields.Psi[0])
	r = PD/2

	MD = copy.deepcopy( stage['Centralization']['Fields'].MD )
	Inc = copy.deepcopy( stage['Centralization']['Fields'].Inc )
	L  = copy.deepcopy( stage['Centralization']['Fields'].LatC )
	SO = copy.deepcopy( stage['Centralization']['Fields'].SOatM )
	MD.referenceUnitConvert()
	Inc.referenceUnitConvert()
	L.referenceUnitConvert()
	SO.referenceUnitConvert()
	numofC = len(MD)

	TDS_fields = self.s4TorqueDragSideforce_fields

	MDLims = ( MD[-1], stageBottomMD )
	calculate_TDS_for_uncentralizedStage(self, stage, FT1=FT1, MDLims=MDLims, centralizedStage=True )

	Tu = [ TDS_fields.Torque_u[-1] ]
	Ts = [ TDS_fields.Torque_s[-1] ]
	Td = [ TDS_fields.Torque_d[-1] ]
	Fu = [ TDS_fields.Drag_u[-1] ]
	Fs = [ TDS_fields.Drag_s[-1] ]
	Fd = [ TDS_fields.Drag_d[-1] ]

	for i in range(-1,-numofC-1,-1):
		
		floatedW = buoyancyFactor*L[i]*PW

		axialForce  = floatedW*np.cos( Inc[i] )
		normalForce = floatedW*np.sin( Inc[i] )
		raisingNormalForce  = normalForce*ff*sinPsi
		loweringNormalForce = -raisingNormalForce
		straightTorque = ff*r*normalForce*cosPsi

		SF.append( normalForce )
		
		Tu.append( Tu[-1] + straightTorque )
		Ts.append( Ts[-1] + straightTorque )
		Td.append( Td[-1] + straightTorque )

		Fu.append( Fu[-1] + raisingNormalForce + axialForce)
		Fs.append( Fs[-1] + axialForce)
		Fd.append( Fd[-1] + loweringNormalForce + axialForce)

		mu.create_physicalValue_and_appendTo_field( MD[i], TDS_fields.MD, 'referenceUnit' )
		mu.create_physicalValue_and_appendTo_field( Inc[i], TDS_fields.Inc, 'referenceUnit' )
		mu.create_physicalValue_and_appendTo_field( Tu[-1], TDS_fields.Torque_u, 'referenceUnit' )
		mu.create_physicalValue_and_appendTo_field( Ts[-1], TDS_fields.Torque_s, 'referenceUnit' )
		mu.create_physicalValue_and_appendTo_field( Td[-1], TDS_fields.Torque_d, 'referenceUnit' )
		mu.create_physicalValue_and_appendTo_field( Fu[-1], TDS_fields.Drag_u, 'referenceUnit' )
		mu.create_physicalValue_and_appendTo_field( Fs[-1], TDS_fields.Drag_s, 'referenceUnit' )
		mu.create_physicalValue_and_appendTo_field( Fd[-1], TDS_fields.Drag_d, 'referenceUnit' )
		mu.create_physicalValue_and_appendTo_field( SF[-1], TDS_fields.SideF, 'referenceUnit' )

		FT1 = {	'Fu':Fu[-1],
				'Fs':Fs[-1],
				'Fd':Fd[-1],
				'Tu':Tu[-1],
				'Ts':Ts[-1],
				'Td':Td[-1]	 }

		if i>-numofC:
			if SO[i-1]<=0:
				MDLims = ( MD[i-1]+PL/2, MD[i]-PL/2 )
				calculate_TDS_for_uncentralizedStage(self, stage, FT1=FT1, MDLims=MDLims, centralizedStage=True )
				Tu.append( TDS_fields.Torque_u[-1] )
				Ts.append( TDS_fields.Torque_s[-1] )
				Td.append( TDS_fields.Torque_d[-1] )
				Fu.append( TDS_fields.Drag_u[-1] )
				Fs.append( TDS_fields.Drag_s[-1] )
				Fd.append( TDS_fields.Drag_d[-1] )
		else:
			MDLims = ( stageTopMD, MD[i]-PL/2 )
			calculate_TDS_for_uncentralizedStage(self, stage, FT1=FT1, MDLims=MDLims, centralizedStage=True )


def get_sortedIndexes_of_wellboreOuterStageData(self):

	stages = list(self.wellboreOuterStageData.values())
	print('s:',stages)
	mapfunction = lambda stage: stage['WellboreProps'].MDtop[0]
	MDtops = list(map( mapfunction, stages ))
	print('m:',MDtops)
	sortedIndexes = np.argsort( MDtops )
	print('i:',sortedIndexes)

	return sortedIndexes



class WellboreInnerStageDataItem( dict ):
	
	def __init__(self, row):
		
		super().__init__()
		
		self['row'] = row
		self['MDtop'] = None
		self['MDbot'] = None
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

		


