import re
import numpy as np
import numpy.linalg as la
import codecs
from MdlUtilities import Field, FieldList
import MdlUtilities as mdl
import dbUtils


def get_lsCentralizerLocations_fields():

	MD  = Field(2001)
	Inc = Field(2002, altBg=True, altFg=True)
	SOatC  = Field(2078, altBg=True, altFg=True)
	SOatM  = Field(2078, altBg=True, altFg=True)
	EW  = Field(2007, altBg=True, altFg=True)
	NS  = Field(2006, altBg=True, altFg=True)
	TVD = Field(2004, altBg=True, altFg=True)
	DL  = Field(2008, altBg=True, altFg=True)
	AxF = Field(2075, altBg=True, altFg=True)
	SiF = Field(2074, altBg=True, altFg=True)
	MD_ = Field(2001, altBg=True, altFg=True)

	SOatC.set_abbreviation('SOatC')
	SOatM.set_abbreviation('SOatM')
	SOatC.set_representation('SO @ centralizer')
	SOatM.set_representation('SO @ mid span')
	MD_.set_abbreviation('MD_AxF')

	lsCentralizerLocations_fields = FieldList()
	lsCentralizerLocations_fields.append( MD )
	lsCentralizerLocations_fields.append( Inc )
	lsCentralizerLocations_fields.append( SOatC )
	lsCentralizerLocations_fields.append( SOatM )
	lsCentralizerLocations_fields.append( EW )
	lsCentralizerLocations_fields.append( NS )
	lsCentralizerLocations_fields.append( TVD )
	lsCentralizerLocations_fields.append( DL )
	lsCentralizerLocations_fields.append( AxF )
	lsCentralizerLocations_fields.append( SiF )
	lsCentralizerLocations_fields.append( MD_ )

	return lsCentralizerLocations_fields



def get_ASCCoordinates_from_MD(self, MD, unit=None):
	
	if unit:
		MD = mdl.unitConvert_value( MD, unit, self.parent.s2DataSurvey_fields.MD.unit )
	else:
		MD = mdl.unitConvert_value( MD, MD.unit, self.parent.s2DataSurvey_fields.MD.unit )

	MD_array = np.array( self.parent.s2DataSurvey_fields.MD )
	index = sum(MD_array[:-1]<=MD)-1
	del MD_array

	MD = mdl.referenceUnitConvert_value( MD, MD.unit )
	sT_value = self.parent.sT( index, MD)
	EW_rest = mdl.inverseReferenceUnitConvert_value( sT_value[0], self.parent.s2DataSurvey_fields.EW.unit  )
	NS_rest = mdl.inverseReferenceUnitConvert_value( sT_value[1], self.parent.s2DataSurvey_fields.NS.unit  )
	VD_rest = mdl.inverseReferenceUnitConvert_value( sT_value[2], self.parent.s2DataSurvey_fields.TVD.unit )

	EW = self.parent.s2DataSurvey_fields.EW[index] + EW_rest
	NS = self.parent.s2DataSurvey_fields.NS[index] + NS_rest
	VD = self.parent.s2DataSurvey_fields.TVD[index] + VD_rest

	return EW,NS,VD,index


def get_ASCT_from_MD(self, MD, unit=None):

	if unit:
		MD = mdl.unitConvert_value( MD, unit, self.parent.s2DataSurvey_fields.MD.unit )
	else:
		MD = mdl.unitConvert_value( MD, MD.unit, self.parent.s2DataSurvey_fields.MD.unit )

	MD_array = np.array( self.parent.s2DataSurvey_fields.MD )
	index = sum(MD_array[:-1]<=MD)-1
	del MD_array
	
	MD = mdl.referenceUnitConvert_value( MD, MD.unit )
	T_value = self.parent.T( index, MD)
	return T_value


def get_ASCDogleg_from_MD(self, MD, unit=None):

	if unit:
		MD = mdl.unitConvert_value( MD, unit, self.parent.s2DataSurvey_fields.MD.unit )
	else:
		MD = mdl.unitConvert_value( MD, MD.unit, self.parent.s2DataSurvey_fields.MD.unit )

	MD_array = np.array( self.parent.s2DataSurvey_fields.MD )
	index = sum(MD_array[:-1]<=MD)-1
	del MD_array

	MD = mdl.referenceUnitConvert_value( MD, MD.unit )
	DL = la.norm( self.parent.dT( index, MD )[:-1] )
	DL = mdl.inverseReferenceUnitConvert_value( DL, self.parent.s2DataSurvey_fields.DL.unit  )

	return DL


def get_LASMDandCALID_intoInterval(self):

	MD = self.parent.workWellboreMD
	ID = self.parent.workWellboreID

	indexes = MD>self.min_MD
	min_index = len(MD)-sum(indexes)-1
	indexes = MD<self.max_MD
	max_index = sum(indexes)+1
	del indexes

	MD = MD[min_index:max_index]
	ID = ID[min_index:max_index]

	ID[0] = (ID[0]-ID[1])/(MD[0]-MD[1])*(self.min_MD-MD[1]) + ID[1]
	ID[-1] = (ID[-1]-ID[-2])/(MD[-1]-MD[-2])*(self.max_MD-MD[-2]) + ID[-2]
	lim_ID = np.max(ID)*1.2

	MD[0] = self.min_MD
	MD[-1] = self.max_MD

	return MD, ID, lim_ID


def calculate_axialForce_field(self):

	MD_array = np.array( self.parent.s2DataSurvey_fields.MD )
	MD_min = mdl.referenceUnitConvert_value( MD_array[ 0], self.parent.s2DataSurvey_fields.MD.unit )
	MD_max = mdl.referenceUnitConvert_value( MD_array[-1], self.parent.s2DataSurvey_fields.MD.unit )
	del MD_array

	MDs = np.linspace(MD_min, MD_max, 100)
	cosIncs = []

	for MD in MDs:
		MD = mdl.physicalValue(MD, self.lsCentralizerLocations_fields.MD_AxF.referenceUnit )
		self.lsCentralizerLocations_fields.MD_AxF.append( MD )
		cosIncs.append( get_ASCT_from_MD(self, MD, MD.unit)[2] )

	value = mdl.physicalValue(0, self.lsCentralizerLocations_fields.AxialF.referenceUnit )
	self.lsCentralizerLocations_fields.AxialF.append( value )
	AxialTension = 0
	L = MDs[1]-MDs[0]

	for i in range(len(MDs)-1):
		for j in range(len(self.parent.wellboreInnerStageData)):
		
			stage = self.parent.wellboreInnerStageData[j]
			stageTopMD = mdl.referenceUnitConvert_value( stage['MD'], stage['MD'].unit )
			W = mdl.referenceUnitConvert_value( stage['PipeProps'].W[0], stage['PipeProps'].W[0].unit )
			
			if MDs[-i-2]<stageTopMD: 
				AxialTension = AxialTension + W*L*cosIncs[-i-1]
				value = mdl.physicalValue(AxialTension, self.lsCentralizerLocations_fields.AxialF.referenceUnit )
				self.lsCentralizerLocations_fields.AxialF.insert(0, value )
				break

	self.lsCentralizerLocations_fields.AxialF.inverseReferenceUnitConvert()
	self.lsCentralizerLocations_fields.MD_AxF.inverseReferenceUnitConvert()


def get_axialTension_below_MD(self, MD, unit=None, referenceUnit=False):

	if unit:
		MD = mdl.unitConvert_value( MD, unit, self.lsCentralizerLocations_fields.MD_AxF.unit )
	else:
		MD = mdl.unitConvert_value( MD, MD.unit, self.lsCentralizerLocations_fields.MD_AxF.unit )
	
	cosInc = get_ASCT_from_MD(self, MD)[2]
	MD_AxF = np.array( self.lsCentralizerLocations_fields.MD_AxF )
	AxialF = np.array( self.lsCentralizerLocations_fields.AxialF )
	index = sum(MD_AxF[:-1]<=MD)

	MD_AxF_i = MD_AxF[index]
	AxialF_i = AxialF[index]
	del MD_AxF
	del AxialF

	stage = self.parent.currentWellboreInnerStageDataItem
	stageTopMD = mdl.referenceUnitConvert_value( stage['MD'], stage['MD'].unit )
	assert( MD<stageTopMD )
	W = mdl.referenceUnitConvert_value( stage['PipeProps'].W[0], stage['PipeProps'].W[0].unit )
	L = MD_AxF_i-MD

	AxialTension = AxialF_i + W*L*cosInc
	if referenceUnit:
		AxialTension = mdl.physicalValue( AxialTension, self.lsCentralizerLocations_fields.AxialF.referenceUnit )
	else:
		AxialTension = mdl.inverseReferenceUnitConvert_value( AxialTension, self.lsCentralizerLocations_fields.AxialF.unit )

	return AxialTension


def get_inclination_and_azimuth(self, MD, unit=None, referenceUnit=False):

	if unit:
		MD = mdl.unitConvert_value( MD, unit, self.lsCentralizerLocations_fields.MD_AxF.unit )
	else:
		MD = mdl.unitConvert_value( MD, MD.unit, self.lsCentralizerLocations_fields.MD_AxF.unit )

	T_values = get_ASCT_from_MD(self, MD)
	inc = np.arccos( T_values[2] )
	sinazi = T_values[0]/np.sin(inc)
	cosazi = T_values[1]/np.sin(inc)

	if sinazi>=0:
		azi = np.arccos( cosazi )
	elif sinazi<0:
		azi = 2*np.pi-np.arccos( cosazi )

	if referenceUnit:
		inc = mdl.physicalValue( inc, self.parent.s2DataSurvey_fields.Inc.referenceUnit )
		azi = mdl.physicalValue( azi, self.parent.s2DataSurvey_fields.Azi.referenceUnit )
		return inc, azi
	else:
		inc = mdl.inverseReferenceUnitConvert_value( inc, self.parent.s2DataSurvey_fields.Inc.unit )
		azi = mdl.inverseReferenceUnitConvert_value( azi, self.parent.s2DataSurvey_fields.Azi.unit )
		return inc, azi


def get_standOff_for_MD(self, MD1, MD2, unit=None):

	self.stage['PipeProps'].referenceUnitConvert()
	D = self.stage['PipeProps'].OD[0]
	d = self.stage['PipeProps'].ID[0]
	E = self.stage['PipeProps'].E[0]
	W = self.stage['PipeProps'].W[0]
	self.stage['PipeProps'].inverseReferenceUnitConvert()

	self.centralizer1['CentralizerProps'].referenceUnitConvert()
	self.centralizer2['CentralizerProps'].referenceUnitConvert()
	ResF1 = self.centralizer1['CentralizerProps'].ResF_CH[0]
	ResF2 = self.centralizer2['CentralizerProps'].ResF_CH[0]
	D1 = self.centralizer1['CentralizerProps'].COD[0]
	D2 = self.centralizer2['CentralizerProps'].COD[0]
	self.centralizer1['CentralizerProps'].inverseReferenceUnitConvert()
	self.centralizer2['CentralizerProps'].inverseReferenceUnitConvert()

	Ft = get_axialTension_below_MD(self, MD2, referenceUnit=True)
	In1, Az1 = get_inclination_and_azimuth(self, MD1, referenceUnit=True)
	In2, Az2 = get_inclination_and_azimuth(self, MD2, referenceUnit=True)
	MD1 = mdl.referenceUnitConvert_value( MD1, MD1.unit )
	MD2 = mdl.referenceUnitConvert_value( MD2, MD2.unit )

	k1 = ResF1/(D1/2-0.335*(D1-D))
	k2 = ResF2/(D2/2-0.335*(D2-D))

	doverDsq = (d/D)**2
	buoyancyFactor = 1 #( (1-ρe/ρs)-doverDsq*(1-ρi/ρs) )/( 1-doverDsq )
	w *= buoyancyFactor

	fC = w*L*np.sin(θ)/2
	y1 = fC/k1
	y2 = fC/k2

	

	I = np.pi/64*(D**4-d**4)

	
	L = MD2-MD1

	u = np.sqrt( Ft*L**2/4/E/I )
	β = np.arccos( np.cos(In1)*np.cos(In2) + np.sin(In1)*np.sin(In2)*np.cos(Az2-Az1) )
	cosγ0 = np.sin(In1)*np.sin(In2)*np.sin(Az2-Az1)/np.sin(β)
	cosγn = np.sin( (In1-In2)/2 )*np.sin( (In1+In2)/2 )/np.sin(β/2)

	Fldp = W*L*cosγn + 2*Ft*np.sin(β/2)
	Flp  = W*L*cosγ0
	Fl   = np.sqrt( Fldp**2 + Flp**2 )

	δ = Fl*L**3/384/E/I*24/u**4*(u**2/2 - u*(np.cosh(u)-1)/np.sinh(u) )


def calculate_standOff_atCentralizers(self):

	self.stage['PipeProps'].referenceUnitConvert()
	D = self.stage['PipeProps'].OD[0]
	d = self.stage['PipeProps'].ID[0]
	E = self.stage['PipeProps'].E[0]
	W = self.stage['PipeProps'].W[0]
	self.stage['PipeProps'].inverseReferenceUnitConvert()

	self.centralizer1['CentralizerProps'].referenceUnitConvert()
	self.centralizer2['CentralizerProps'].referenceUnitConvert()
	ResF1 = self.centralizer1['CentralizerProps'].ResF_CH[0]
	ResF2 = self.centralizer2['CentralizerProps'].ResF_CH[0]
	D1 = self.centralizer1['CentralizerProps'].COD[0]
	D2 = self.centralizer2['CentralizerProps'].COD[0]
	self.centralizer1['CentralizerProps'].inverseReferenceUnitConvert()
	self.centralizer2['CentralizerProps'].inverseReferenceUnitConvert()

	


def calculate_standOff_atMidspan(self):

	self.stage['PipeProps'].referenceUnitConvert()
	D = self.stage['PipeProps'].OD[0]
	d = self.stage['PipeProps'].ID[0]
	E = self.stage['PipeProps'].E[0]
	W = self.stage['PipeProps'].W[0]
	self.stage['PipeProps'].inverseReferenceUnitConvert()

	self.centralizer1['CentralizerProps'].referenceUnitConvert()
	self.centralizer2['CentralizerProps'].referenceUnitConvert()
	ResF1 = self.centralizer1['CentralizerProps'].ResF_CH[0]
	ResF2 = self.centralizer2['CentralizerProps'].ResF_CH[0]
	D1 = self.centralizer1['CentralizerProps'].COD[0]
	D2 = self.centralizer2['CentralizerProps'].COD[0]
	self.centralizer1['CentralizerProps'].inverseReferenceUnitConvert()
	self.centralizer2['CentralizerProps'].inverseReferenceUnitConvert()


	







