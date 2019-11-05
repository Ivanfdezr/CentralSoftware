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
	SOatC1  = Field(2078, altBg=True, altFg=True)
	SOatC2  = Field(2078, altBg=True, altFg=True)
	SOatM  = Field(2078, altBg=True, altFg=True)
	EW  = Field(2007, altBg=True, altFg=True)
	NS  = Field(2006, altBg=True, altFg=True)
	TVD = Field(2004, altBg=True, altFg=True)
	DL  = Field(2008, altBg=True, altFg=True)
	AxF = Field(2075, altBg=True, altFg=True)
	SiF = Field(2074, altBg=True, altFg=True)
	MD_ = Field(2001, altBg=True, altFg=True)

	SOatC1.set_abbreviation('SOatC1')
	SOatC2.set_abbreviation('SOatC2')
	SOatM.set_abbreviation('SOatM')
	SOatC1.set_representation('SO @ centralizer1')
	SOatC2.set_representation('SO @ centralizer2')
	SOatM.set_representation('SO @ mid span')
	MD_.set_abbreviation('MD_AxF')

	lsCentralizerLocations_fields = FieldList()
	lsCentralizerLocations_fields.append( MD )
	lsCentralizerLocations_fields.append( Inc )
	lsCentralizerLocations_fields.append( SOatC1 )
	lsCentralizerLocations_fields.append( SOatC2 )
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
		K = list(self.parent.wellboreInnerStageData.keys())
		K.sort()
		for k in K:
			stage = self.parent.wellboreInnerStageData[k]
			stageTopMD = mdl.referenceUnitConvert_value( stage['MD'], stage['MD'].unit )
			W = mdl.referenceUnitConvert_value( stage['PipeProps'].PW[0], stage['PipeProps'].PW[0].unit )
			
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
	W = mdl.referenceUnitConvert_value( stage['PipeProps'].PW[0], stage['PipeProps'].PW[0].unit )
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

	D = self.stage['PipeProps'].OD.referenceUnitConvert()[0]
	d = self.stage['PipeProps'].ID.referenceUnitConvert()[0]
	E = self.stage['PipeProps'].E.referenceUnitConvert()[0]
	W = self.stage['PipeProps'].PW.referenceUnitConvert()[0]
	PL = self.stage['PipeBase'].PL[0]

	if self.centralizer1['Type']=='Bow Spring':
		ResF1 = self.centralizer1['CentralizerProps'].ResF_CH[0]
		ResF1 = mdl.referenceUnitConvert_value( ResF1, ResF1.unit )
	if self.centralizer2['Type']=='Bow Spring':
		ResF2 = self.centralizer2['CentralizerProps'].ResF_CH[0]
		ResF2 = mdl.referenceUnitConvert_value( ResF2, ResF2.unit )
	D1 = self.centralizer1['CentralizerProps'].COD[0]
	D2 = self.centralizer2['CentralizerProps'].COD[0]

	Ft = get_axialTension_below_MD(self, MD2, referenceUnit=True)
	In1, Az1 = get_inclination_and_azimuth(self, MD1, referenceUnit=True)
	In2, Az2 = get_inclination_and_azimuth(self, MD2, referenceUnit=True)
	
	D = mdl.referenceUnitConvert_value( D, D.unit )
	d = mdl.referenceUnitConvert_value( d, d.unit )
	E = mdl.referenceUnitConvert_value( E, E.unit )
	W = mdl.referenceUnitConvert_value( W, W.unit )
	MD1 = mdl.referenceUnitConvert_value( MD1, MD1.unit )
	MD2 = mdl.referenceUnitConvert_value( MD2, MD2.unit )
	PL  = mdl.referenceUnitConvert_value( PL,  PL.unit  )
	D1 = mdl.referenceUnitConvert_value( D1, D1.unit )
	D2 = mdl.referenceUnitConvert_value( D2, D2.unit )

	supports = 0
	numofRigCent = 0
	numofBowCent = 0
	for X in ['A','B','C']:
		if self.stage['Centralization'][X]['Type']=='Bow Spring':
			supports+=1
			numofBowCent+=1
		elif self.stage['Centralization'][X]['Type']=='Rigid':
			supports+=self.stage['Centralization'][X]['CentralizerBase'].Blades[0]
			numofRigCent+=1
	numofCent = numofBowCent+numofRigCent

	doverDsq = (d/D)**2
	buoyancyFactor = 1 #( (1-ρe/ρs)-doverDsq*(1-ρi/ρs) )/( 1-doverDsq )
	W *= buoyancyFactor
	L = MD2-MD1
	f1 = W*L*np.sin(In1)/supports
	f2 = W*L*np.sin(In2)/supports
	gap = mdl.referenceUnitConvert_value( 2.0, 'm' )

	y1 = y2 = 0
	ε1 = ε2 = 0
	if numofCent==1:
		if self.centralizer1['Type']=='Bow Spring':
			CL = 0
			kA = ResF1/(D1/2-0.335*(D1-D))
			y1 = f1/kA
			y2 = f2/kA
			ε1 = ε2 = 0
		elif self.centralizer1['Type']=='Rigid':
			CL = self.centralizer1['CentralizerBase'].CL
	
	elif numofCent==2:
		if self.stage['Centralization']['B']['Type']==None:
			CL = PL
			if self.stage['Centralization']['A']['Type']=='Rigid':
				if self.stage['Centralization']['C']['Type']=='Bow Spring':
					efectiveL = PL-self.stage['Centralization']['A']['CentralizerBase'].CL
					kC = ResF2/(D2/2-0.335*(D2-D))
					yC = f1/kC
					y1 = yC/2
					ε1 = 0
					yC = f2/kC
					y2 = yC/2
					ε2 = yC/efectiveL

			elif self.stage['Centralization']['A']['Type']=='Bow Spring':
				if self.stage['Centralization']['C']['Type']=='Rigid':
					efectiveL = PL-self.stage['Centralization']['C']['CentralizerBase'].CL
					kA = ResF1/(D1/2-0.335*(D1-D))
					yA = f1/kA
					y1 = yA/2
					ε1 = -yA/efectiveL
					yA = f2/kA
					y2 = yA/2
					ε2 = 0

				elif self.stage['Centralization']['C']['Type']=='Bow Spring':
					kA = ResF1/(D1/2-0.335*(D1-D))
					kC = ResF2/(D2/2-0.335*(D2-D))
					yA = f1/kA
					yC = f1/kC
					y1 = (yA+yC)/2
					ε1 = (yC-yA)/PL
					yA = f2/kA
					yC = f2/kC
					y2 = (yA+yC)/2
					ε2 = (yC-yA)/PL

		elif numofBowCent==1:
			if self.centralizer1['Type']=='Bow Spring':
				CL = self.centralizer2['CentralizerBase'].CL +gap
				kA = ResF1/(D1/2-0.335*(D1-D))
				yA = f1/kA
				y1 = yA/2
				ε1 = -yA/gap
				yA = f2/kA
				y2 = yA/2
				ε2 = 0

			elif self.centralizer2['Type']=='Bow Spring':
				CL = self.centralizer1['CentralizerBase'].CL +gap
				kB = ResF2/(D2/2-0.335*(D2-D))
				yB = f1/kB
				y1 = yB/2
				ε1 = 0
				yB = f2/kB
				y2 = yB/2
				ε2 = yB/gap

		elif numofBowCent==2:
			CL = PL/2
			efectiveL = PL/2
			kA = ResF1/(D1/2-0.335*(D1-D))
			kB = ResF2/(D2/2-0.335*(D2-D))
			yA = f1/kA
			yB = f1/kB
			y1 = (yA+yB)/2
			ε1 = (yB-yA)/efectiveL
			yA = f2/kA
			yB = f2/kB
			y2 = (yA+yB)/2
			ε2 = (yB-yA)/efectiveL

	elif numofCent==3:
		CL = PL
		if numofBowCent==1:
			if self.stage['Centralization']['A']['Type']=='Bow Spring':
				efectiveL = PL-gap
				efectiveL -= self.stage['Centralization']['B']['CentralizerBase'].CL
				efectiveL -= self.stage['Centralization']['C']['CentralizerBase'].CL
				kA = ResF1/(D1/2-0.335*(D1-D))
				yA = f1/kA
				y1 = yA/2
				ε1 = -yA/efectiveL
				y2 = 0
				ε2 = 0

			elif self.stage['Centralization']['C']['Type']=='Bow Spring':
				efectiveL = PL-gap
				efectiveL -= self.stage['Centralization']['A']['CentralizerBase'].CL
				efectiveL -= self.stage['Centralization']['B']['CentralizerBase'].CL
				kC = ResF2/(D2/2-0.335*(D2-D))
				y1 = 0
				ε1 = 0
				yC = f2/kC
				y2 = yC/2
				ε2 = yC/efectiveL

		elif numofBowCent==2:
			if self.stage['Centralization']['A']['Type']=='Rigid':
				efectiveL = PL-gap
				efectiveL -= self.stage['Centralization']['A']['CentralizerBase'].CL
				ResFB = self.stage['Centralization']['B']['CentralizerProps'].ResF_CH[0]
				DB = self.stage['Centralization']['B']['CentralizerProps'].COD[0]
				kB = ResFB/(DB/2-0.335*(DB-D))
				kC = ResF2/(D2/2-0.335*(D2-D))
				yB = f1/kB
				y1 = yB/2
				ε1 = 0
				yB = f2/kB
				yC = f2/kC
				y2 = (yB+yC)/2
				ε2 = (yC-yB)/efectiveL

			elif self.stage['Centralization']['C']['Type']=='Rigid':
				efectiveL = PL-gap
				efectiveL -= self.stage['Centralization']['C']['CentralizerBase'].CL
				ResFB = self.stage['Centralization']['B']['CentralizerProps'].ResF_CH[0]
				DB = self.stage['Centralization']['B']['CentralizerProps'].COD[0]
				kB = ResFB/(DB/2-0.335*(DB-D))
				kA = ResF1/(D1/2-0.335*(D1-D))
				yB = f1/kB
				yA = f1/kA
				y1 = (yA+yB)/2
				ε1 = (yB-yA)/efectiveL
				yB = f2/kB
				y2 = yB/2
				ε2 = 0

			elif self.stage['Centralization']['B']['Type']=='Rigid':
				efectiveL = PL-gap
				efectiveL -= self.stage['Centralization']['B']['CentralizerBase'].CL
				efectiveL /=2
				kA = ResF1/(D1/2-0.335*(D1-D))
				kC = ResF2/(D2/2-0.335*(D2-D))
				yA = f1/kA
				y1 = yA/2
				ε1 = -yA/efectiveL
				yC = f2/kC
				y2 = yC/2
				ε2 = yC/efectiveL

		elif numofBowCent==3:
			efectiveL = PL/2
			ResFB = self.stage['Centralization']['B']['CentralizerProps'].ResF_CH[0]
			DB = self.stage['Centralization']['B']['CentralizerProps'].COD[0]
			kA = ResF1/(D1/2-0.335*(D1-D))
			kB = ResFB/(DB/2-0.335*(DB-D))
			kC = ResF2/(D2/2-0.335*(D2-D))
			yA = f1/kA
			yB = f1/kB
			y1 = (yA+yB)/2
			ε1 = (yB-yA)/efectiveL
			yB = f2/kB
			yC = f2/kC
			y2 = (yB+yC)/2
			ε2 = (yC-yB)/efectiveL

	Inc1 += ε1
	Inc2 += ε2
	MD1 += CL

	MDi = self.MD[0]
	IDi = self.ID[0]
	for MDj,IDj in zip(self.MD,self.ID):
		if MD1<MDj:
			dH1 = (MD1-MDi)/(MDj-MDi)*(IDj-IDi)+IDi
			break
		else:
			MDi = MDj
			IDi = IDj

	MDi = self.MD[0]
	IDi = self.ID[0]
	for MDj,IDj in zip(self.MD,self.ID):
		if MD2<MDj:
			dH2 = (MD2-MDi)/(MDj-MDi)*(IDj-IDi)+IDi
			break
		else:
			MDi = MDj
			IDi = IDj

	L = MD2-MD1
	MDm = MD1 + L/2

	MDi = self.MD[0]
	IDi = self.ID[0]
	for MDj,IDj in zip(self.MD,self.ID):
		if MDm<MDj:
			dHm = (MDm-MDi)/(MDj-MDi)*(IDj-IDi)+IDi
			break
		else:
			MDi = MDj
			IDi = IDj

	I = np.pi/64*(D**4-d**4)
	u = np.sqrt( Ft*L**2/4/E/I )
	β = np.arccos( np.cos(In1)*np.cos(In2) + np.sin(In1)*np.sin(In2)*np.cos(Az2-Az1) )
	cosγ0 = np.sin(In1)*np.sin(In2)*np.sin(Az2-Az1)/np.sin(β)
	cosγn = np.sin( (In1-In2)/2 )*np.sin( (In1+In2)/2 )/np.sin(β/2)

	Fldp = W*L*cosγn + 2*Ft*np.sin(β/2)
	Flp  = W*L*cosγ0
	Fl   = np.sqrt( Fldp**2 + Flp**2 )

	δ = Fl*L**3/384/E/I*24/u**4*(u**2/2 - u*(np.cosh(u)-1)/np.sinh(u) )

	R = D/2
	rH1 = dH1/2
	rH2 = dH2/2
	rHm = dHm/2
	r1_min = R+(D1/2-R)*0.1
	r2_min = R+(D2/2-R)*0.1
	r1 = (D1/2-y1) if (D1<dH1) else (rH1-y1)
	r2 = (D2/2-y2) if (D2<dH2) else (rH2-y2)
	r1 = r1_min if (r1<r1_min) else r1
	r2 = r2_min if (r2<r2_min) else r2

	cH1 = rH1-R
	cH2 = rH2-R
	cHm = rHm-R
	c1 = r1-R
	c2 = r2-R
	cm = (c1+c2)/2-δ
	cm = cm if (cm>0) else 0 
	S1 = c1/cH1
	S2 = c2/cH2
	Sm = cm/cHm

	S1 = mdl.inverseReferenceUnitConvert_value( S1, self.lsCentralizerLocations_fields.SOatC1.unit )
	S2 = mdl.inverseReferenceUnitConvert_value( S2, self.lsCentralizerLocations_fields.SOatC2.unit )
	Sm = mdl.inverseReferenceUnitConvert_value( Sm, self.lsCentralizerLocations_fields.SOatM.unit )

	return S1, S2, Sm

	


	




def calculate_standOff_atCentralizers(self):

	self.stage['PipeProps'].referenceUnitConvert()
	D = self.stage['PipeProps'].OD[0]
	d = self.stage['PipeProps'].ID[0]
	E = self.stage['PipeProps'].E[0]
	W = self.stage['PipeProps'].PW[0]
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
	W = self.stage['PipeProps'].PW[0]
	self.stage['PipeProps'].inverseReferenceUnitConvert()

	self.centralizer1['CentralizerProps'].referenceUnitConvert()
	self.centralizer2['CentralizerProps'].referenceUnitConvert()
	ResF1 = self.centralizer1['CentralizerProps'].ResF_CH[0]
	ResF2 = self.centralizer2['CentralizerProps'].ResF_CH[0]
	D1 = self.centralizer1['CentralizerProps'].COD[0]
	D2 = self.centralizer2['CentralizerProps'].COD[0]
	self.centralizer1['CentralizerProps'].inverseReferenceUnitConvert()
	self.centralizer2['CentralizerProps'].inverseReferenceUnitConvert()


	







