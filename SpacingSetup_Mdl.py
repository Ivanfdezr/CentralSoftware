import re
import numpy as np
import numpy.linalg as la
import codecs
import InputWindow_Mdl as mdl
from MdlUtilities import Field, FieldList
import MdlUtilities as mu
import CtrlUtilities as cu
import dbUtils

import time


def get_ssNextSpacing_fields():

	Spacing  = Field(2061)

	Spacing.set_representation('Next stage spacing')
	ssNextSpacing_fields = FieldList()
	ssNextSpacing_fields.append( Spacing )

	return ssNextSpacing_fields


def get_ssCentralizerLocations_fields():

	MD  = Field(2001)
	Inc = Field(2002, altBg=True, altFg=True)
	SOatC = Field(2078, altBg=True, altFg=True)
	SOatM = Field(2078, altBg=True, altFg=True)
	ClatC = Field(2073, altBg=True, altFg=True)
	ClatM = Field(2073, altBg=True, altFg=True)

	hsMD  = Field(2001)
	hsInc = Field(2002, altBg=True, altFg=True)
	hsSOatC = Field(2078, altBg=True, altFg=True)
	hsSOatM = Field(2078, altBg=True, altFg=True)
	hsClatC = Field(2073, altBg=True, altFg=True)
	hsClatM = Field(2073, altBg=True, altFg=True)

	dsMD  = Field(2001)
	dsInc = Field(2002, altBg=True, altFg=True)
	dsSOatC = Field(2078, altBg=True, altFg=True)
	dsSOatM = Field(2078, altBg=True, altFg=True)
	dsClatC = Field(2073, altBg=True, altFg=True)
	dsClatM = Field(2073, altBg=True, altFg=True)

	EW  = Field(2007, altBg=True, altFg=True)
	NS  = Field(2006, altBg=True, altFg=True)
	TVD = Field(2004, altBg=True, altFg=True)
	DL  = Field(2008, altBg=True, altFg=True)

	SOatC.set_abbreviation('SOatC')
	SOatM.set_abbreviation('SOatM')
	ClatC.set_abbreviation('ClatC')
	ClatM.set_abbreviation('ClatM')

	hsMD.set_abbreviation('hsMD')
	hsInc.set_abbreviation('hsInc')
	hsSOatC.set_abbreviation('hsSOatC')
	hsSOatM.set_abbreviation('hsSOatM')
	hsClatC.set_abbreviation('hsClatC')
	hsClatM.set_abbreviation('hsClatM')

	dsMD.set_abbreviation('dsMD')
	dsInc.set_abbreviation('dsInc')
	dsSOatC.set_abbreviation('dsSOatC')
	dsSOatM.set_abbreviation('dsSOatM')	
	dsClatC.set_abbreviation('dsClatC')
	dsClatM.set_abbreviation('dsClatM')

	SOatC.set_representation('<SO> @ centr.')
	SOatM.set_representation('SO @ mid span')
	ClatC.set_representation('<Cl> @ centr.')
	ClatM.set_representation('Cl @ mid span')

	ssCentralizerLocations_fields = FieldList()
	ssCentralizerLocations_fields.append( MD )
	ssCentralizerLocations_fields.append( Inc )
	ssCentralizerLocations_fields.append( SOatC )
	ssCentralizerLocations_fields.append( SOatM )
	ssCentralizerLocations_fields.append( ClatC )
	ssCentralizerLocations_fields.append( ClatM )

	ssCentralizerLocations_fields.append( hsMD )
	ssCentralizerLocations_fields.append( hsInc )
	ssCentralizerLocations_fields.append( hsSOatC )
	ssCentralizerLocations_fields.append( hsSOatM )
	ssCentralizerLocations_fields.append( hsClatC )
	ssCentralizerLocations_fields.append( hsClatM )

	ssCentralizerLocations_fields.append( dsMD )
	ssCentralizerLocations_fields.append( dsInc )
	ssCentralizerLocations_fields.append( dsSOatC )
	ssCentralizerLocations_fields.append( dsSOatM )
	ssCentralizerLocations_fields.append( dsClatC )
	ssCentralizerLocations_fields.append( dsClatM )

	ssCentralizerLocations_fields.append( EW )
	ssCentralizerLocations_fields.append( NS )
	ssCentralizerLocations_fields.append( TVD )
	ssCentralizerLocations_fields.append( DL )

	return ssCentralizerLocations_fields


def get_LASMDandCALID_intoInterval(self):

	MD = self.parent.workWellboreMD
	ID = self.parent.workWellboreID

	min_index = np.where(MD<=self.min_MD)[0][-1]
	max_index = np.where(MD>=self.max_MD)[0][0]+1

	MD = MD[min_index:max_index]
	ID = ID[min_index:max_index]

	ID[0] = (ID[0]-ID[1])/(MD[0]-MD[1])*(self.min_MD-MD[1]) + ID[1]
	ID[-1] = (ID[-1]-ID[-2])/(MD[-1]-MD[-2])*(self.max_MD-MD[-2]) + ID[-2]
	lim_ID = np.max(ID)*1.2

	MD[0] = self.min_MD
	MD[-1] = self.max_MD

	K = list(self.parent.wellboreOuterStageData.keys())
	K.sort()
	mean_ID = []
	for md in MD:
		for k in K:
			stage = self.parent.wellboreOuterStageData[k]
			if md>=stage['WellboreProps'].MDtop and md<=stage['WellboreProps'].MDbot:
				mean_ID.append( stage['WellboreProps'].ID[0] )
				break
	mean_ID = np.array( mean_ID )

	return MD, ID, mean_ID, lim_ID


def calculate_standOff_atCentralizers(self, locations, SOatC_field, ClatC_field):

	locations.referenceUnitConvert()
	SOatC_field.referenceUnitConvert()
	ClatC_field.referenceUnitConvert()
	numofLocations = len(locations)

	Inc, Azi = mdl.get_inclination_and_azimuth_from_locations(self.parent, locations)
	MDs = self.ssCentralizerLocations_fields.MD.factorToReferenceUnit*self.MD
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

	ResF = {}
	D = {}
	supports = 0

	for x, c in self.centralizers.items():
		if c['Type']=='Bow Spring':
			ResF[x] = c['CentralizerProps'].ResF_CH[0]
			ResF[x] = mu.referenceUnitConvert_value( ResF[x], ResF[x].unit )
			D[x] = c['CentralizerProps'].COD[0]
			D[x] = mu.referenceUnitConvert_value( D[x], D[x].unit )
			supports+=1

		elif c['Type']=='Rigid':
			D[x] = c['CentralizerProps'].COD[0]
			D[x] = mu.referenceUnitConvert_value( D[x], D[x].unit )
			supports+=c['CentralizerBase'].Blades[0]

	buoyancyFactor = mu.calculate_buoyancyFactor( OD=PD, ID=Pd, ρs=ρs, ρe=ρe, ρi=ρi )
	PW *= buoyancyFactor
	PI = np.pi/64*(PD**4-Pd**4)
	PR = PD/2

	def calculate_SO_per_centralizersEnsemble():
		SO = 0
		Cc = 0
		for x, c in self.centralizers.items():
			if c['Type']=='Bow Spring':
				so, cc = calculate_SO_per_centralizer(x)
				SO += so/supports
				Cc += cc/supports
			elif c['Type']=='Rigid':
				so, cc = calculate_SO_per_centralizer(x)
				SO += so*c['CentralizerBase'].Blades[0]/supports
				Cc += cc*c['CentralizerBase'].Blades[0]/supports
		return SO, Cc
		
	for j, (MD1,inc) in enumerate(zip(locations,Inc)):
		i = j-1
		k = j+1
		if i==-1:
			MD0 = None
		else:
			MD0 = locations[i]
		if k==numofLocations:
			MD2 = None
		else:
			MD2 = locations[k]

		def calculate_SO_per_centralizer(label):
			"""
			Define before use: MD0, MD1, MD2, inc
			Return "y" in reference units.
			"""
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
				δ = Hr-PR
				L = L10 + Lalt
			else:
				Lalt = (384*PE*PI*δ/PW/np.sin(inc))**0.25/2
				L21 = (MD2-MD1)/2
				L21 = L21 if (L21<Lalt) else Lalt
				L10 = (MD1-MD0)/2
				L10 = L10 if (L10<Lalt) else Lalt
				L = L21 + L10

			if self.centralizers[label]['Type']=='Bow Spring':
				f = PW*L*np.sin(inc)/supports
				resK = ResF[label]/(D[label]/2-0.335*(D[label]-PD))
				y = f/resK
				Rmin = PR+(R-PR)*0.1
				R = (R-y) if (R<Hr) else (Hr-y)
				R = Rmin if (R<Rmin) else R

			mHc = mHr-PR
			Cc = R-PR-(Hr-mHr)
			SO = Cc/mHc
			
			return SO, Cc
		
		SO, Cc = calculate_SO_per_centralizersEnsemble()

		cu.create_physicalValue_and_appendTo_field( SO, SOatC_field, SOatC_field.referenceUnit )
		cu.create_physicalValue_and_appendTo_field( Cc, ClatC_field, ClatC_field.referenceUnit )

	SOatC_field.inverseReferenceUnitConvert()
	ClatC_field.inverseReferenceUnitConvert()
	locations.inverseReferenceUnitConvert()


def calculate_standOff_atMidspan(self, locations, ClatC_field, SOatM_field, ClatM_field):

	t0 = time.time()
	
	locations.referenceUnitConvert()
	ClatC_field.referenceUnitConvert()
	SOatM_field.referenceUnitConvert()
	ClatM_field.referenceUnitConvert()
	Inc_field = self.ssCentralizerLocations_fields.Inc
	Inc_field.clear()

	Inc, Azi = mdl.get_inclination_and_azimuth_from_locations(self.parent, locations)
	t01 = time.time()

	MDs = self.ssCentralizerLocations_fields.MD.factorToReferenceUnit*self.MD
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

	firstCent = None
	lastCent  = None
	for x, c in self.centralizers.items():
		if firstCent==None and c['Type']!=None:
			firstCent = x
		elif firstCent!=None and c['Type']!=None:
			lastCent = x
	if lastCent==None:
		lastCent = firstCent

	CL = 0
	numofCent = 0
	for x, c in self.centralizers.items():
		if c['Type']!=None:
			CL += c['CentralizerBase'].CL[0]
			numofCent +=1

	if numofCent==2:
		if firstCent=='A' and lastCent=='C':
			CL = PL
		else:
			CL += gap

	if numofCent==3:
		CL += gap

	if CL>PL:
		print('SIZE ERROR in CENTRALIZERS ENSEMBLE')

	buoyancyFactor = mu.calculate_buoyancyFactor( OD=PD, ID=Pd, ρs=ρs, ρe=ρe, ρi=ρi )
	PW *= buoyancyFactor
	PI = np.pi/64*(PD**4-Pd**4)
	PR = PD/2

	cu.create_physicalValue_and_appendTo_field( Inc[0], Inc_field, Inc_field.referenceUnit )

	t1 = time.time()
	t12 = []
	for i in range(len(locations)-1):
		j = i+1
		MD1 = locations[i]+CL
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
			if MD1<MDj:
				Hd = (MD1-MDi)/(MDj-MDi)*(IDj-IDi)+IDi
				mHd = (MD1-MDi)/(MDj-MDi)*(mIDj-mIDi)+mIDi
				break
			else:
				MDi = MDj
				IDi = IDj
				mIDi = mIDj
		t120 = time.time()
		Ft = mdl.get_axialTension_below_MD(self.parent, MD2, referenceUnit=True)
		t121 = time.time()
		t12.append(t121-t120)

		u = np.sqrt( Ft*L**2/4/PE/PI )
		β = np.arccos( np.cos(In1)*np.cos(In2) + np.sin(In1)*np.sin(In2)*np.cos(Az2-Az1) )
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

		cu.create_physicalValue_and_appendTo_field( In2, Inc_field, Inc_field.referenceUnit )
		cu.create_physicalValue_and_appendTo_field( SO, SOatM_field, SOatM_field.referenceUnit )
		cu.create_physicalValue_and_appendTo_field( Mc, ClatM_field, ClatM_field.referenceUnit )

	t12 = np.mean(t12)

	cu.create_physicalValue_and_appendTo_field( 0, SOatM_field, SOatM_field.referenceUnit )
	cu.create_physicalValue_and_appendTo_field( 0, ClatM_field, ClatM_field.referenceUnit )

	t2 = time.time()
	locations.inverseReferenceUnitConvert()
	ClatC_field.inverseReferenceUnitConvert()
	SOatM_field.inverseReferenceUnitConvert()
	ClatM_field.inverseReferenceUnitConvert()
	Inc_field.inverseReferenceUnitConvert()
	t3 = time.time()

	print(t01-t0, t1-t01, t12, t3-t2)


def set_newSpacedLocations_under_MD_with_variations(self, MD):

	item = self.ssNextSpacing_tableWidget.item(0,0)
	space = mu.unitConvert_value(	item.realValue, item.realValue.unit,
									self.ssCentralizerLocations_fields.MD.unit )

	auxarray = np.array(self.ssCentralizerLocations_fields.hsMD)
	indexes = np.where( auxarray<MD )[0]
	auxarray = np.append( 	auxarray[indexes],
							np.arange(MD, self.max_MD, space/2) )

	self.ssCentralizerLocations_fields.hsMD.clear()
	for value in auxarray:
		cu.create_physicalValue_and_appendTo_field( value, self.ssCentralizerLocations_fields.hsMD, 
													self.ssCentralizerLocations_fields.hsMD.unit )

	auxarray = np.array(self.ssCentralizerLocations_fields.dsMD)
	indexes = np.where( auxarray<MD )[0]
	auxarray = np.append( 	auxarray[indexes],
							np.arange(MD, self.max_MD, space*2) )
	
	self.ssCentralizerLocations_fields.dsMD.clear()
	for value in auxarray:
		cu.create_physicalValue_and_appendTo_field( value, self.ssCentralizerLocations_fields.dsMD, 
													self.ssCentralizerLocations_fields.dsMD.unit )

	auxarray = np.array(self.ssCentralizerLocations_fields.MD)
	indexes = np.where( auxarray<MD )[0]
	auxarray = np.append( 	auxarray[indexes],
							np.arange(MD, self.max_MD, space) )
	
	self.ssCentralizerLocations_fields.MD.clear()
	for value in auxarray:
		cu.create_physicalValue_and_appendTo_field( value, self.ssCentralizerLocations_fields.MD, 
													self.ssCentralizerLocations_fields.MD.unit )

	try:
		return self.ssCentralizerLocations_fields.MD[indexes[-1]+1]
	except IndexError:
		return self.ssCentralizerLocations_fields.MD[0]












