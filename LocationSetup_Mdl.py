import re
import numpy as np
import numpy.linalg as la
import codecs
import InputWindow_Mdl as mdl
import MdlUtilities as mu
import CtrlUtilities as cu
import dbUtils


def get_lsCentralization_fields():

	MD    = mu.Field(2001)
	Inc   = mu.Field(2002, altBg=True, altFg=True)
	Azi   = mu.Field(2003, altBg=True, altFg=True)
	SOatC = mu.Field(2078, altBg=True, altFg=True)
	SOatM = mu.Field(2078, altBg=True, altFg=True)
	ClatC = mu.Field(2073, altBg=True, altFg=True)
	ClatM = mu.Field(2073, altBg=True, altFg=True)
	AFatC = mu.Field(2074, altBg=True, altFg=True)
	AFatM = mu.Field(2074, altBg=True, altFg=True)
	SFatC = mu.Field(2074, altBg=True, altFg=True)
	SFatM = mu.Field(2074, altBg=True, altFg=True)
	LatC  = mu.Field(2080, altBg=True, altFg=True)
	EW    = mu.Field(2007, altBg=True, altFg=True)
	NS    = mu.Field(2006, altBg=True, altFg=True)
	TVD   = mu.Field(2004, altBg=True, altFg=True)
	HD    = mu.Field(2005, altBg=True, altFg=True)
	DL    = mu.Field(2008, altBg=True, altFg=True)
	ID    = mu.Field(2031, altBg=True, altFg=True)
	avgID = mu.Field(2031, altBg=True, altFg=True)
	Stage = mu.Field(2000, altBg=True, altFg=True)

	SOatC.set_abbreviation('SOatC')
	SOatM.set_abbreviation('SOatM')
	ClatC.set_abbreviation('ClatC')
	ClatM.set_abbreviation('ClatM')
	AFatC.set_abbreviation('AFatC')
	AFatM.set_abbreviation('AFatM')
	SFatC.set_abbreviation('SFatC')
	SFatM.set_abbreviation('SFatM')
	LatC.set_abbreviation('LatC')
	avgID.set_abbreviation('avgID')
	Stage.set_abbreviation('Stage')
	SOatC.set_representation('<SO> @ centr.')
	SOatM.set_representation('SO @ mid span')
	ClatC.set_representation('<Cl> @ centr.')
	ClatM.set_representation('Cl @ mid span')
	ID.set_representation('Hole ID')
	avgID.set_representation('Average ID')
	Stage.set_representation('Stage')
	
	lsCentralization_fields = mu.FieldList()
	lsCentralization_fields.append( MD )
	lsCentralization_fields.append( Inc )
	lsCentralization_fields.append( SOatC )
	lsCentralization_fields.append( SOatM )
	lsCentralization_fields.append( Stage )
	lsCentralization_fields.append( ClatC )
	lsCentralization_fields.append( ClatM )
	lsCentralization_fields.append( AFatC )
	lsCentralization_fields.append( AFatM )
	lsCentralization_fields.append( SFatC )
	lsCentralization_fields.append( SFatM )
	lsCentralization_fields.append( LatC )
	lsCentralization_fields.append( Azi )
	lsCentralization_fields.append( EW )
	lsCentralization_fields.append( NS )
	lsCentralization_fields.append( TVD )
	lsCentralization_fields.append( HD )
	lsCentralization_fields.append( DL )
	lsCentralization_fields.append( ID )
	lsCentralization_fields.append( avgID )	

	return lsCentralization_fields


def get_LASMDandCALID_intoStage(self, stage):

	MD = self.parent.v3WorkWellboreMD
	ID = self.parent.v3WorkWellboreID
	min_MD = stage['MDtop']
	max_MD = stage['MDbot']

	try:
		min_index = np.where(MD<=min_MD)[0][-1]
	except IndexError:
		min_index = 0

	try:
		max_index = np.where(MD>=max_MD)[0][0]+1
	except IndexError:
		max_index = len(MD)

	MD = MD[min_index:max_index]
	ID = ID[min_index:max_index]

	ID[0] = (ID[0]-ID[1])/(MD[0]-MD[1])*(min_MD-MD[1]) + ID[1]
	ID[-1] = (ID[-1]-ID[-2])/(MD[-1]-MD[-2])*(max_MD-MD[-2]) + ID[-2]

	MD[0] = min_MD
	MD[-1] = max_MD

	return MD, ID


def cat_locations(self):

	self.lsCentralization_fields.clear_content()
	K = mdl.get_sortedIndexes_of_wellboreInnerStageData(self.parent)

	for k in K:
		stage = self.parent.v3WellboreInnerStageData[k]
		fields = stage['Centralization']['Fields']
		if fields==None:
			continue
		rows = [mu.physicalValue(stage['row'],None) for md in fields.MD]

		self.lsCentralization_fields.MD.extend( fields.MD )
		self.lsCentralization_fields.Inc.extend( fields.Inc )
		self.lsCentralization_fields.Azi.extend( fields.Azi )
		self.lsCentralization_fields.EW.extend( fields.EW )
		self.lsCentralization_fields.NS.extend( fields.NS )
		self.lsCentralization_fields.TVD.extend( fields.TVD )
		self.lsCentralization_fields.HD.extend( fields.HD )
		self.lsCentralization_fields.DL.extend( fields.DL )
		self.lsCentralization_fields.ID.extend( fields.ID )
		self.lsCentralization_fields.avgID.extend( fields.avgID )
		self.lsCentralization_fields.Stage.extend( rows )

	PL = mu.unitConvert_value( 480, 'in', self.lsCentralization_fields.MD.unit )
	CEL = stage['Centralization']['Ensemble']['PLfactor']*PL*0.9

	if self.lsCentralization_fields.MD[-1] + CEL > stage['MDbot']:
		
		self.lsCentralization_fields.MD.pop()
		self.lsCentralization_fields.Inc.pop()
		self.lsCentralization_fields.Azi.pop()
		self.lsCentralization_fields.EW.pop()
		self.lsCentralization_fields.NS.pop()
		self.lsCentralization_fields.TVD.pop()
		self.lsCentralization_fields.HD.pop()
		self.lsCentralization_fields.DL.pop()
		self.lsCentralization_fields.ID.pop()
		self.lsCentralization_fields.avgID.pop()
		self.lsCentralization_fields.Stage.pop()

	return len(K)


def get_separationsInEnsemble(ensemble, PL):
	Δ = []
	aux = 0
	for join in ensemble:
		if len(join)==1:
			Δ.append( aux+PL/2 )
			aux = PL/2
		elif len(join)==2:
			Δ.append( aux+PL/4 )
			Δ.append( PL/2 )
			aux = PL/4
		elif len(join)==3:
			Δ.append( aux+PL/4 )
			Δ.append( PL/4 )
			Δ.append( PL/4 )
			aux = PL/4
		else:
			Δ.append( aux+PL )
			aux = 0
	return Δ


def calculate_standOff_at_jthCentralizer(self, j):

	Loc_field = self.lsCentralization_fields.MD
	Inc_field = self.lsCentralization_fields.Inc
	Azi_field = self.lsCentralization_fields.Azi
	SOatC_field = self.lsCentralization_fields.SOatC
	ClatC_field = self.lsCentralization_fields.ClatC
	AFatC_field = self.lsCentralization_fields.AFatC
	SFatC_field = self.lsCentralization_fields.SFatC
	LatC_field = self.lsCentralization_fields.LatC
	ID_field = self.lsCentralization_fields.ID
	avgID_field = self.lsCentralization_fields.avgID
	stage_field = self.lsCentralization_fields.Stage

	self.lsCentralization_fields.referenceUnitConvert_fields()

	def calculate_SO_per_centralizersEnsemble():
		
		SO = []
		Cc = []
		Ft = []
		Fl = []
		L  = []
		Δs = get_separationsInEnsemble( c['Ensemble']['nest'], PL )
		Δa = 0

		for x,Δ in zip(['A','B','C'],Δs):
			
			Δa += Δ
			if c[x]['Type']!=None:
				so, cc, ft, fl, l = calculate_SO_per_centralizer(x,c[x]['Type'],supports,Δa)
				SO.append( so )
				Cc.append( cc )
				Ft.append( ft )
				Fl.append( fl )
				L.append( l )

		return np.mean(SO), np.mean(Cc), np.mean(Ft), np.mean(Fl), np.mean(L)

	def get_L(MD0, MD1, MD2, inc, Hr):

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

		return L
	
	stage = self.parent.v3WellboreInnerStageData[ stage_field[j] ]
	MD1 = Loc_field[j]
	Hd  = ID_field[j]
	mHd = avgID_field[j]

	PD = stage['PipeProps'].OD[0]
	Pd = stage['PipeProps'].ID[0]
	PE = stage['PipeProps'].E[0]
	PW = stage['PipeProps'].PW[0]
	PL = stage['PipeBase'].PL[0]
	ρi = stage['PipeProps'].InnerMudDensity[0]
	ρe = stage['PipeProps'].OuterMudDensity[0]
	ρs = stage['PipeProps'].Density[0]

	PD = mu.referenceUnitConvert_value( PD, PD.unit )
	Pd = mu.referenceUnitConvert_value( Pd, Pd.unit )
	PE = mu.referenceUnitConvert_value( PE, PE.unit )
	PW = mu.referenceUnitConvert_value( PW, PW.unit )
	PL = mu.referenceUnitConvert_value( PL, PL.unit )
	ρi = mu.referenceUnitConvert_value( ρi, ρi.unit )
	ρe = mu.referenceUnitConvert_value( ρe, ρe.unit )
	ρs = mu.referenceUnitConvert_value( ρs, ρs.unit )

	if j>0:
		BEL = self.parent.v3WellboreInnerStageData[ stage_field[j-1] ]['Centralization']['Ensemble']['PLfactor']*PL*0.9

	ResF = {}
	D    = {}
	d    = {}
	CL   = {}
	B    = {}
	supports = 0
	PI = np.pi/64*(PD**4-Pd**4)
	PR = PD/2
	Hr  =  Hd/2
	mHr = mHd/2
	c = stage['Centralization']
	CEL = c['Ensemble']['PLfactor']*PL*0.9

	for x in ['A','B','C']:
		
		if c[x]['Type']=='Bow Spring':
			ResF[x] = c[x]['CentralizerProps'].ResF_CH[0]
			ResF[x] = mu.referenceUnitConvert_value( ResF[x], ResF[x].unit )
			D[x] = c[x]['CentralizerProps'].COD[0]
			D[x] = mu.referenceUnitConvert_value( D[x], D[x].unit )
			d[x] = c[x]['CentralizerProps'].IPOD[0]
			d[x] = mu.referenceUnitConvert_value( d[x], d[x].unit )
			CL[x] = c[x]['CentralizerBase'].CL[0]
			CL[x] = mu.referenceUnitConvert_value( CL[x], CL[x].unit )
			supports+=1

		elif c[x]['Type']=='Resin':
			D[x] = c[x]['CentralizerProps'].COD[0]
			D[x] = mu.referenceUnitConvert_value( D[x], D[x].unit )
			CL[x] = c[x]['CentralizerBase'].CL[0]
			CL[x] = mu.referenceUnitConvert_value( CL[x], CL[x].unit )
			B[x] = int(c[x]['CentralizerBase'].Blades[0])
			supports+=1#c[x]['CentralizerBase'].Blades[0]

	buoyancyFactor = mu.calculate_buoyancyFactor( OD=PD, ID=Pd, ρs=ρs, ρe=ρe, ρi=ρi )
	PWb = PW*buoyancyFactor

	i = j-1
	k = j+1

	In1 = Inc_field[j] + 1e-12

	if i==-1:
		MD0 = None
		In0 = None
		Az0 = None
	else:
		MD0 = Loc_field[i] + BEL
		In0 = Inc_field[i] + 1e-12
		Az0 = Azi_field[i]
		if MD0>MD1:
			self.lsCentralization_fields.inverseReferenceUnitConvert_fields()
			raise(mu.LogicalError)
	if k==len(Loc_field):
		MD2 = None
		In2 = None
		Az2 = None
	else:
		MD2 = Loc_field[k]
		In2 = Inc_field[k] + 1e-12
		Az2 = Azi_field[k]
		if MD1+CEL>MD2:
			self.lsCentralization_fields.inverseReferenceUnitConvert_fields()
			raise(mu.LogicalError)

	def calculate_SO_per_centralizer(label,ctype,supports,ΔMD1):

		# Equations Reference:
		# 	H.C. Juvkam-Wold et al. Casing Deflection and Centralizer Spacing Calculations.
		# 	SPE Drilling Engineering, December 1992.

		"""
		Define before use: MD0, MD1, MD2, inc
		Return "SO, Cc, L" in reference units.
		"""
		MD1_ = MD1 + ΔMD1
		R = D[label]/2

		if ctype=='Bow Spring':
			
			L = get_L(MD0, MD1_, MD2, In1, Hr)

			if MD0==None:
				Ft = mdl.get_axialTension_below_MD(self.parent, MD2, referenceUnit=True)
				Fl = Ft*np.sin(In1)/supports

			elif MD2==None:
				Ft = 0.0
				Fl = PWb*L*np.sin(In1)/supports

			else:
				Ft = mdl.get_axialTension_below_MD(self.parent, MD2, referenceUnit=True)
				u = np.sqrt( Ft*L**2/4/PE/PI )
				β = np.arccos( np.cos(In0)*np.cos(In2) + np.sin(In0)*np.sin(In2)*np.cos(Az2-Az0) )
				
				if β==0.0:
					Fl = 0.0
				else:
					cosγ0 = np.sin(In0)*np.sin(In2)*np.sin(Az2-Az0)/np.sin(β)
					cosγn = np.sin( abs(In0-In2)/2 )*np.sin( (In0+In2)/2 )/np.sin(β/2)

					if In0>In2:
						Fldp = PWb*L*cosγn + 2*Ft*np.sin(β/2)
					elif In0<In2:
						Fldp = PWb*L*cosγn - 2*Ft*np.sin(β/2)
					else:
						Fldp = 0.0
					Flp  = PWb*L*cosγ0
					Fl   = np.sqrt( Fldp**2 + Flp**2 )/supports

			#f = PWb*L*np.sin(In1)/supports
			resK = 2*ResF[label]/( D[label]-d[label]-0.67*(Hr*2-PD) )

			y = Fl/resK
			Rmin = PR+(R-PR)*0.1
			R = (R-y) if (R<Hr) else (Hr-y)
			R = Rmin if (R<Rmin) else R

			mHc = mHr-PR
			Cc = R-PR-(Hr-mHr)
			SO = Cc/mHc

		elif ctype=='Resin':

			SO_ = []
			Cc_ = []
			L_  = []

			for i in range(B[label]):
				L = get_L(MD0, MD1_, MD2, In1, Hr)

				mHc = mHr-PR
				cc = R-PR-(Hr-mHr)
				Cc_.append( cc )
				SO_.append( cc/mHc )
				L_.append( L )

				MD1_ += CL[label]/B[label]

			Cc = np.mean( Cc_ )
			SO = np.mean( SO_ )
			L = np.mean( L_ )

			if MD0==None:
				Ft = mdl.get_axialTension_below_MD(self.parent, MD2, referenceUnit=True)
				Fl = Ft*np.sin(In1)/supports

			elif MD2==None:
				Ft = 0.0
				Fl = PWb*L*np.sin(In1)/supports

			else:
				Ft = mdl.get_axialTension_below_MD(self.parent, MD2, referenceUnit=True)
				u = np.sqrt( Ft*L**2/4/PE/PI )
				β = np.arccos( np.cos(In0)*np.cos(In2) + np.sin(In0)*np.sin(In2)*np.cos(Az2-Az0) )
				
				if β==0.0:
					Fl = 0.0
				else:
					cosγ0 = np.sin(In0)*np.sin(In2)*np.sin(Az2-Az0)/np.sin(β)
					cosγn = np.sin( abs(In0-In2)/2 )*np.sin( (In0+In2)/2 )/np.sin(β/2)

					if In0>In2:
						Fldp = PWb*L*cosγn + 2*Ft*np.sin(β/2)
					elif In0<In2:
						Fldp = PWb*L*cosγn - 2*Ft*np.sin(β/2)
					else:
						Fldp = 0.0
					Flp  = PWb*L*cosγ0
					Fl   = np.sqrt( Fldp**2 + Flp**2 )/supports
		
		return SO, Cc, Ft, Fl, L
	
	SO, Cc, Ft, Fl, L = calculate_SO_per_centralizersEnsemble()

	SO = mu.physicalValue( SO, SOatC_field.referenceUnit )
	Cc = mu.physicalValue( Cc, ClatC_field.referenceUnit )
	Ft  = mu.physicalValue( Ft, AFatC_field.referenceUnit )
	Fl  = mu.physicalValue( Fl, SFatC_field.referenceUnit )
	L  = mu.physicalValue( L, LatC_field.referenceUnit )

	SOatC_field.put( j, SO )
	ClatC_field.put( j, Cc )
	AFatC_field.put( j, Ft )
	SFatC_field.put( j, Fl )
	LatC_field.put( j, L )

	self.lsCentralization_fields.inverseReferenceUnitConvert_fields()


def calculate_standOff_at_ithMidspan(self, i):

	Loc_field = self.lsCentralization_fields.MD
	Inc_field = self.lsCentralization_fields.Inc
	Azi_field = self.lsCentralization_fields.Azi
	SOatM_field = self.lsCentralization_fields.SOatM
	ClatM_field = self.lsCentralization_fields.ClatM
	ClatC_field = self.lsCentralization_fields.ClatC
	AFatM_field = self.lsCentralization_fields.AFatM
	SFatM_field = self.lsCentralization_fields.SFatM
	ID_field = self.lsCentralization_fields.ID
	avgID_field = self.lsCentralization_fields.avgID
	stage_field = self.lsCentralization_fields.Stage

	self.lsCentralization_fields.referenceUnitConvert_fields()

	if i==len(self.lsCentralization_fields.MD)-1:
		
		SO = mu.physicalValue( 0, SOatM_field.referenceUnit )
		Mc = mu.physicalValue( 0, ClatM_field.referenceUnit )
		Ft = mu.physicalValue( 0, AFatM_field.referenceUnit )
		Fl = mu.physicalValue( 0, SFatM_field.referenceUnit )

		SOatM_field.put( i, SO )
		ClatM_field.put( i, Mc )
		AFatM_field.put( i, Ft )
		SFatM_field.put( i, Fl )

		self.lsCentralization_fields.inverseReferenceUnitConvert_fields()
		return

	MDs = self.lsCentralization_fields.MD.factorToReferenceUnit*self.MD
	IDs = self.lsCentralization_fields.ID.factorToReferenceUnit*self.ID

	j = i+1
	stage = self.parent.v3WellboreInnerStageData[ stage_field[i] ] # CORREGIR, ELEGIR EL STAGE ADECUADO PARA MID.

	PD = stage['PipeProps'].OD[0]
	Pd = stage['PipeProps'].ID[0]
	PE = stage['PipeProps'].E[0]
	PW = stage['PipeProps'].PW[0]
	PL = stage['PipeBase'].PL[0]
	ρi = stage['PipeProps'].InnerMudDensity[0]
	ρe = stage['PipeProps'].OuterMudDensity[0]
	ρs = stage['PipeProps'].Density[0]

	PD = mu.referenceUnitConvert_value( PD, PD.unit )
	Pd = mu.referenceUnitConvert_value( Pd, Pd.unit )
	PE = mu.referenceUnitConvert_value( PE, PE.unit )
	PW = mu.referenceUnitConvert_value( PW, PW.unit )
	PL = mu.referenceUnitConvert_value( PL, PL.unit )
	ρi = mu.referenceUnitConvert_value( ρi, ρi.unit )
	ρe = mu.referenceUnitConvert_value( ρe, ρe.unit )
	ρs = mu.referenceUnitConvert_value( ρs, ρs.unit )

	c = stage['Centralization']
	CEL = c['Ensemble']['PLfactor']*PL*0.9

	buoyancyFactor = mu.calculate_buoyancyFactor( OD=PD, ID=Pd, ρs=ρs, ρe=ρe, ρi=ρi )
	PWb = PW*buoyancyFactor
	PI = np.pi/64*(PD**4-Pd**4)
	PR = PD/2
	
	MD1 = Loc_field[i]+CEL
	MD2 = Loc_field[j]
	In1 = Inc_field[i]
	In2 = Inc_field[j]
	Az1 = Azi_field[i]
	Az2 = Azi_field[j]
	mID1 = avgID_field[i]
	mID2 = avgID_field[j]

	L = MD2-MD1
	MDm = MD1 + L/2
	mHd = (MDm-MD1)/(MD2-MD1)*(mID2-mID1)+mID1

	MDi = MDs[0]
	IDi = IDs[0]
	for MDj,IDj in zip(MDs[1:],IDs[1:]):
		if MDm<MDj:
			Hd = (MDm-MDi)/(MDj-MDi)*(IDj-IDi)+IDi
			break
		else:
			MDi = MDj
			IDi = IDj
	
	Ft = mdl.get_axialTension_below_MD(self.parent, MD2, referenceUnit=True)

	u = np.sqrt( Ft*L**2/4/PE/PI )
	β = np.arccos( np.cos(In1)*np.cos(In2) + np.sin(In1)*np.sin(In2)*np.cos(Az2-Az1) )
	
	if β==0.0:
		Fl = 0.0
		δ = 0.0
	else:
		cosγ0 = np.sin(In1)*np.sin(In2)*np.sin(Az2-Az1)/np.sin(β)
		cosγn = np.sin( abs(In1-In2)/2 )*np.sin( (In1+In2)/2 )/np.sin(β/2)

		if In1>In2:
			Fldp = PWb*L*cosγn + 2*Ft*np.sin(β/2)
		elif In1<In2:
			Fldp = PWb*L*cosγn - 2*Ft*np.sin(β/2)
		else:
			Fldp = 0.0
		Flp  = PWb*L*cosγ0
		Fl   = np.sqrt( Fldp**2 + Flp**2 )

		δ = Fl*L**3/384/PE/PI*24/u**4*(u**2/2 - u*(np.cosh(u)-1)/np.sinh(u) )

	c1 = ClatC_field[i]
	c2 = ClatC_field[j]

	Hr = Hd/2
	mHr = mHd/2
	mHc = mHr-PR
	Mc = (c1+c2)/2-δ
	xHc = mHr-Hr
	#Mc = Mc if (Mc>xHc) else xHc
	if Mc>xHc:
		Fl = -Fl
	else:
		Mc = xHc
	SO = Mc/mHc

	SO = mu.physicalValue( SO, SOatM_field.referenceUnit )
	Mc = mu.physicalValue( Mc, ClatM_field.referenceUnit )
	Ft = mu.physicalValue( Ft, AFatM_field.referenceUnit )
	Fl = mu.physicalValue( Fl, SFatM_field.referenceUnit )

	SOatM_field.put( i, SO )
	ClatM_field.put( i, Mc )
	AFatM_field.put( i, Ft )
	SFatM_field.put( i, Fl )

	self.lsCentralization_fields.inverseReferenceUnitConvert_fields()


def calculate_standOff_at_Centralizers(self):

	"""
	fieldlen = len(self.lsCentralization_fields.MD)
	print('MD',fieldlen)
	for field in self.lsCentralization_fields[1:]:
		print(field.abbreviation,len(field))
	print('-------------------------------------')
	"""

	Loc_field = self.lsCentralization_fields.MD
	Inc_field = self.lsCentralization_fields.Inc
	Azi_field = self.lsCentralization_fields.Azi
	SOatC_field = self.lsCentralization_fields.SOatC
	ClatC_field = self.lsCentralization_fields.ClatC
	AFatC_field = self.lsCentralization_fields.AFatC
	SFatC_field = self.lsCentralization_fields.SFatC
	LatC_field = self.lsCentralization_fields.LatC
	ID_field = self.lsCentralization_fields.ID
	avgID_field = self.lsCentralization_fields.avgID
	stage_field = self.lsCentralization_fields.Stage

	self.lsCentralization_fields.referenceUnitConvert_fields()


	def calculate_SO_per_centralizersEnsemble():
			SO = []
			Cc = []
			Ft = []
			Fl = []
			L = []
			Δs = get_separationsInEnsemble( c['Ensemble']['nest'], PL )
			Δa = 0

			for x,Δ in zip(['A','B','C'],Δs):
				
				Δa += Δ
				if c[x]['Type']!=None:
					so, cc, ft, fl, l = calculate_SO_per_centralizer(x,c[x]['Type'],supports,Δa)
					SO.append( so )
					Cc.append( cc )
					Ft.append( ft )
					Fl.append( fl )
					L.append( l )

			return np.mean(SO), np.mean(Cc), np.mean(Ft), np.mean(Fl), np.mean(L)

	def get_L(MD0, MD1, MD2, inc, Hr):

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

			return L

	stageRow = None
	BEL = None
	for j, (MD1,Hd,mHd) in enumerate(zip(Loc_field, ID_field, avgID_field)):

		stage = self.parent.v3WellboreInnerStageData[ stage_field[j] ]

		if stageRow!=stage['row']:
			stageRow = stage['row']

			PD = stage['PipeProps'].OD[0]
			Pd = stage['PipeProps'].ID[0]
			PE = stage['PipeProps'].E[0]
			PW = stage['PipeProps'].PW[0]
			PL = stage['PipeBase'].PL[0]
			ρi = stage['PipeProps'].InnerMudDensity[0]
			ρe = stage['PipeProps'].OuterMudDensity[0]
			ρs = stage['PipeProps'].Density[0]

			PD = mu.referenceUnitConvert_value( PD, PD.unit )
			Pd = mu.referenceUnitConvert_value( Pd, Pd.unit )
			PE = mu.referenceUnitConvert_value( PE, PE.unit )
			PW = mu.referenceUnitConvert_value( PW, PW.unit )
			PL = mu.referenceUnitConvert_value( PL, PL.unit )
			ρi = mu.referenceUnitConvert_value( ρi, ρi.unit )
			ρe = mu.referenceUnitConvert_value( ρe, ρe.unit )
			ρs = mu.referenceUnitConvert_value( ρs, ρs.unit )

		ResF = {}
		D    = {}
		d    = {}
		CL   = {}
		B    = {}
		supports = 0
		PI = np.pi/64*(PD**4-Pd**4)
		PR = PD/2
		Hr  =  Hd/2
		mHr = mHd/2
		c = stage['Centralization']
		CEL = c['Ensemble']['PLfactor']*PL*0.9

		for x in ['A','B','C']:
			
			if c[x]['Type']=='Bow Spring':
				ResF[x] = c[x]['CentralizerProps'].ResF_CH[0]
				ResF[x] = mu.referenceUnitConvert_value( ResF[x], ResF[x].unit )
				D[x] = c[x]['CentralizerProps'].COD[0]
				D[x] = mu.referenceUnitConvert_value( D[x], D[x].unit )
				d[x] = c[x]['CentralizerProps'].IPOD[0]
				d[x] = mu.referenceUnitConvert_value( d[x], d[x].unit )
				CL[x] = c[x]['CentralizerBase'].CL[0]
				CL[x] = mu.referenceUnitConvert_value( CL[x], CL[x].unit )
				supports+=1

			elif c[x]['Type']=='Resin':
				D[x] = c[x]['CentralizerProps'].COD[0]
				D[x] = mu.referenceUnitConvert_value( D[x], D[x].unit )
				CL[x] = c[x]['CentralizerBase'].CL[0]
				CL[x] = mu.referenceUnitConvert_value( CL[x], CL[x].unit )
				B[x] = int(c[x]['CentralizerBase'].Blades[0])
				supports+=1#c[x]['CentralizerBase'].Blades[0]

		buoyancyFactor = mu.calculate_buoyancyFactor( OD=PD, ID=Pd, ρs=ρs, ρe=ρe, ρi=ρi )
		PWb = PW*buoyancyFactor

		i = j-1
		k = j+1

		In1 = Inc_field[j] + 1e-12

		if i==-1:
			MD0 = None
			In0 = None
			Az0 = None
		else:
			MD0 = Loc_field[i] + BEL
			In0 = Inc_field[i] + 1e-12
			Az0 = Azi_field[i]
			if MD0>MD1:
				self.lsCentralization_fields.inverseReferenceUnitConvert_fields()
				raise(mu.LogicalError)
		if k==len(Loc_field):
			MD2 = None
			In2 = None
			Az2 = None
		else:
			MD2 = Loc_field[k]
			In2 = Inc_field[k] + 1e-12
			Az2 = Azi_field[k]
			if MD1+CEL>MD2:
				self.lsCentralization_fields.inverseReferenceUnitConvert_fields()
				raise(mu.LogicalError)

		BEL = CEL

		def calculate_SO_per_centralizer(label,ctype,supports,ΔMD1):

			# Equations Reference:
			# 	H.C. Juvkam-Wold et al. Casing Deflection and Centralizer Spacing Calculations.
			# 	SPE Drilling Engineering, December 1992.

			"""
			Define before use: MD0, MD1, MD2, inc
			Return "SO, Cc, L" in reference units.
			"""
			MD1_ = MD1 + ΔMD1
			R = D[label]/2

			if ctype=='Bow Spring':
				
				L = get_L(MD0, MD1_, MD2, In1, Hr)

				if MD0==None:
					Ft = mdl.get_axialTension_below_MD(self.parent, MD2, referenceUnit=True)
					Fl = Ft*np.sin(In1)/supports

				elif MD2==None:
					Ft = 0.0
					Fl = PWb*L*np.sin(In1)/supports

				else:
					Ft = mdl.get_axialTension_below_MD(self.parent, MD2, referenceUnit=True)
					u = np.sqrt( Ft*L**2/4/PE/PI )
					β = np.arccos( np.cos(In0)*np.cos(In2) + np.sin(In0)*np.sin(In2)*np.cos(Az2-Az0) )
					
					if β==0.0:
						Fl = 0.0
					else:
						cosγ0 = np.sin(In0)*np.sin(In2)*np.sin(Az2-Az0)/np.sin(β)
						cosγn = np.sin( abs(In0-In2)/2 )*np.sin( (In0+In2)/2 )/np.sin(β/2)

						if In0>In2:
							Fldp = PWb*L*cosγn + 2*Ft*np.sin(β/2)
						elif In0<In2:
							Fldp = PWb*L*cosγn - 2*Ft*np.sin(β/2)
						else:
							Fldp = 0.0
						Flp  = PWb*L*cosγ0
						Fl   = np.sqrt( Fldp**2 + Flp**2 )/supports

				#f = PWb*L*np.sin(In1)/supports
				resK = 2*ResF[label]/( D[label]-d[label]-0.67*(Hr*2-PD) )

				y = Fl/resK
				Rmin = PR+(R-PR)*0.1
				R = (R-y) if (R<Hr) else (Hr-y)
				R = Rmin if (R<Rmin) else R

				mHc = mHr-PR
				Cc = R-PR-(Hr-mHr)
				SO = Cc/mHc

			elif ctype=='Resin':

				SO_ = []
				Cc_ = []
				L_  = []

				for i in range(B[label]):
					L = get_L(MD0, MD1_, MD2, In1, Hr)

					mHc = mHr-PR
					cc = R-PR-(Hr-mHr)
					Cc_.append( cc )
					SO_.append( cc/mHc )
					L_.append( L )

					MD1_ += CL[label]/B[label]

				Cc = np.mean( Cc_ )
				SO = np.mean( SO_ )
				L = np.mean( L_ )

				if MD0==None:
					Ft = mdl.get_axialTension_below_MD(self.parent, MD2, referenceUnit=True)
					Fl = Ft*np.sin(In1)/supports

				elif MD2==None:
					Ft = 0.0
					Fl = PWb*L*np.sin(In1)/supports

				else:
					Ft = mdl.get_axialTension_below_MD(self.parent, MD2, referenceUnit=True)
					u = np.sqrt( Ft*L**2/4/PE/PI )
					β = np.arccos( np.cos(In0)*np.cos(In2) + np.sin(In0)*np.sin(In2)*np.cos(Az2-Az0) )
					
					if β==0.0:
						Fl = 0.0
					else:
						cosγ0 = np.sin(In0)*np.sin(In2)*np.sin(Az2-Az0)/np.sin(β)
						cosγn = np.sin( abs(In0-In2)/2 )*np.sin( (In0+In2)/2 )/np.sin(β/2)

						if In0>In2:
							Fldp = PWb*L*cosγn + 2*Ft*np.sin(β/2)
						elif In0<In2:
							Fldp = PWb*L*cosγn - 2*Ft*np.sin(β/2)
						else:
							Fldp = 0.0
						Flp  = PWb*L*cosγ0
						Fl   = np.sqrt( Fldp**2 + Flp**2 )/supports
			
			return SO, Cc, Ft, Fl, L
		
		SO, Cc, Ft, Fl, L = calculate_SO_per_centralizersEnsemble()

		mu.create_physicalValue_and_appendTo_field( SO, SOatC_field, SOatC_field.referenceUnit )
		mu.create_physicalValue_and_appendTo_field( Cc, ClatC_field, ClatC_field.referenceUnit )
		mu.create_physicalValue_and_appendTo_field( Ft, AFatC_field, AFatC_field.referenceUnit )
		mu.create_physicalValue_and_appendTo_field( Fl, SFatC_field, SFatC_field.referenceUnit )
		mu.create_physicalValue_and_appendTo_field( L, LatC_field, LatC_field.referenceUnit )

	self.lsCentralization_fields.inverseReferenceUnitConvert_fields()


def calculate_standOff_at_Midspans(self):

	Loc_field = self.lsCentralization_fields.MD
	Inc_field = self.lsCentralization_fields.Inc
	Azi_field = self.lsCentralization_fields.Azi
	SOatM_field = self.lsCentralization_fields.SOatM
	ClatM_field = self.lsCentralization_fields.ClatM
	AFatM_field = self.lsCentralization_fields.AFatM
	SFatM_field = self.lsCentralization_fields.SFatM
	ClatC_field = self.lsCentralization_fields.ClatC
	ID_field = self.lsCentralization_fields.ID
	avgID_field = self.lsCentralization_fields.avgID
	stage_field = self.lsCentralization_fields.Stage

	self.lsCentralization_fields.referenceUnitConvert_fields()

	MDs = self.lsCentralization_fields.MD.factorToReferenceUnit*self.MD
	IDs = self.lsCentralization_fields.ID.factorToReferenceUnit*self.ID
	stageRow = None

	for i in range(len(Loc_field)-1):
		
		j = i+1
		stage = self.parent.v3WellboreInnerStageData[ stage_field[j] ]

		if stageRow!=stage['row']:
			stageRow = stage['row']

			PD = stage['PipeProps'].OD[0]
			Pd = stage['PipeProps'].ID[0]
			PE = stage['PipeProps'].E[0]
			PW = stage['PipeProps'].PW[0]
			PL = stage['PipeBase'].PL[0]
			ρi = stage['PipeProps'].InnerMudDensity[0]
			ρe = stage['PipeProps'].OuterMudDensity[0]
			ρs = stage['PipeProps'].Density[0]

			PD = mu.referenceUnitConvert_value( PD, PD.unit )
			Pd = mu.referenceUnitConvert_value( Pd, Pd.unit )
			PE = mu.referenceUnitConvert_value( PE, PE.unit )
			PW = mu.referenceUnitConvert_value( PW, PW.unit )
			PL = mu.referenceUnitConvert_value( PL, PL.unit )
			ρi = mu.referenceUnitConvert_value( ρi, ρi.unit )
			ρe = mu.referenceUnitConvert_value( ρe, ρe.unit )
			ρs = mu.referenceUnitConvert_value( ρs, ρs.unit )

		c = stage['Centralization']
		CEL = c['Ensemble']['PLfactor']*PL*0.9

		buoyancyFactor = mu.calculate_buoyancyFactor( OD=PD, ID=Pd, ρs=ρs, ρe=ρe, ρi=ρi )
		PWb = PW*buoyancyFactor
		PI = np.pi/64*(PD**4-Pd**4)
		PR = PD/2
		
		MD1 = Loc_field[i]+CEL
		MD2 = Loc_field[j]
		In1 = Inc_field[i]
		In2 = Inc_field[j]
		Az1 = Azi_field[i]
		Az2 = Azi_field[j]
		mID1 = avgID_field[i]
		mID2 = avgID_field[j]

		L = MD2-MD1
		MDm = MD1 + L/2
		mHd = (MDm-MD1)/(MD2-MD1)*(mID2-mID1)+mID1

		MDi = MDs[0]
		IDi = IDs[0]
		for MDj,IDj in zip(MDs[1:],IDs[1:]):
			if MDm<MDj:
				Hd = (MDm-MDi)/(MDj-MDi)*(IDj-IDi)+IDi
				break
			else:
				MDi = MDj
				IDi = IDj
		
		Ft = mdl.get_axialTension_below_MD(self.parent, MD2, referenceUnit=True)

		u = np.sqrt( Ft*L**2/4/PE/PI )
		β = np.arccos( np.cos(In1)*np.cos(In2) + np.sin(In1)*np.sin(In2)*np.cos(Az2-Az1) )
		
		if β==0.0:
			Fl = 0.0
			δ = 0.0
		else:
			cosγ0 = np.sin(In1)*np.sin(In2)*np.sin(Az2-Az1)/np.sin(β)
			cosγn = np.sin( abs(In1-In2)/2 )*np.sin( (In1+In2)/2 )/np.sin(β/2)

			if In1>In2:
				Fldp = PWb*L*cosγn + 2*Ft*np.sin(β/2)
			elif In1<In2:
				Fldp = PWb*L*cosγn - 2*Ft*np.sin(β/2)
			else:
				Fldp = 0.0
			Flp  = PWb*L*cosγ0
			Fl   = np.sqrt( Fldp**2 + Flp**2 )

			δ = Fl*L**3/384/PE/PI*24/u**4*(u**2/2 - u*(np.cosh(u)-1)/np.sinh(u) )

		c1 = ClatC_field[i]
		c2 = ClatC_field[j]

		Hr = Hd/2
		mHr = mHd/2
		mHc = mHr-PR
		Mc = (c1+c2)/2-δ
		xHc = mHr-Hr
		#Mc = Mc if (Mc>xHc) else xHc
		if Mc>xHc:
			Fl = -Fl
		else:
			Mc = xHc
		SO = Mc/mHc

		mu.create_physicalValue_and_appendTo_field( SO, SOatM_field, SOatM_field.referenceUnit )
		mu.create_physicalValue_and_appendTo_field( Mc, ClatM_field, ClatM_field.referenceUnit )
		mu.create_physicalValue_and_appendTo_field( Ft, AFatM_field, AFatM_field.referenceUnit )
		mu.create_physicalValue_and_appendTo_field( Fl, SFatM_field, SFatM_field.referenceUnit )

	mu.create_physicalValue_and_appendTo_field( 0, SOatM_field, SOatM_field.referenceUnit )
	mu.create_physicalValue_and_appendTo_field( 0, ClatM_field, ClatM_field.referenceUnit )
	mu.create_physicalValue_and_appendTo_field( 0, AFatM_field, AFatM_field.referenceUnit )
	mu.create_physicalValue_and_appendTo_field( 0, SFatM_field, SFatM_field.referenceUnit )

	self.lsCentralization_fields.inverseReferenceUnitConvert_fields()


def insert_location_to_CentralizationFields(self, pos, MD):

	MD = mu.physicalValue( MD, self.lsCentralization_fields.MD.unit )
	innerStage = mdl.get_innerStage_at_MD(self.parent, MD)
	if not innerStage['Centralization']['Mode']:
		return False
	outerStage = mdl.get_outerStage_at_MD(self.parent, MD)
	Inc, Azi = mdl.get_ASCIncAzi_from_MD(self.parent, MD)
	EW,NS,VD,HD,i = mdl.get_ASCCoordinates_from_MD(self.parent, MD)
	DL = mdl.get_ASCDogleg_from_MD(self.parent, MD)
	ID = mdl.get_wellboreID_at_MD(self.parent, MD) 
	avgID = outerStage['WellboreProps'].ID[0]
	row = mu.physicalValue(innerStage['row'],None)

	self.lsCentralization_fields.MD.insert( pos, MD )
	self.lsCentralization_fields.Inc.insert( pos, Inc )
	self.lsCentralization_fields.Azi.insert( pos, Azi )
	self.lsCentralization_fields.SOatC.insert( pos, None )
	self.lsCentralization_fields.SOatM.insert( pos, None )
	self.lsCentralization_fields.ClatC.insert( pos, None )
	self.lsCentralization_fields.ClatM.insert( pos, None )
	self.lsCentralization_fields.AFatC.insert( pos, None )
	self.lsCentralization_fields.AFatM.insert( pos, None )
	self.lsCentralization_fields.SFatC.insert( pos, None )
	self.lsCentralization_fields.SFatM.insert( pos, None )
	self.lsCentralization_fields.LatC.insert( pos, None )
	self.lsCentralization_fields.EW.insert( pos, EW )
	self.lsCentralization_fields.NS.insert( pos, NS )
	self.lsCentralization_fields.TVD.insert( pos, VD )
	self.lsCentralization_fields.HD.insert( pos, HD )
	self.lsCentralization_fields.DL.insert( pos, DL )
	self.lsCentralization_fields.ID.insert( pos, ID )
	self.lsCentralization_fields.avgID.insert( pos, avgID )
	self.lsCentralization_fields.Stage.insert( pos, row )

	return True


def put_location_to_CentralizationFields(self, pos, MD):

	MD = mu.physicalValue( MD, self.lsCentralization_fields.MD.unit )
	innerStage = mdl.get_innerStage_at_MD(self.parent, MD)
	if not innerStage['Centralization']['Mode']:
		return False
	outerStage = mdl.get_outerStage_at_MD(self.parent, MD)
	Inc, Azi = mdl.get_ASCIncAzi_from_MD(self.parent, MD)
	EW,NS,VD,HD,i = mdl.get_ASCCoordinates_from_MD(self.parent, MD)
	DL = mdl.get_ASCDogleg_from_MD(self.parent, MD)
	ID = mdl.get_wellboreID_at_MD(self.parent, MD) 
	avgID = outerStage['WellboreProps'].ID[0]
	row = mu.physicalValue(innerStage['row'],None)

	self.lsCentralization_fields.MD.put( pos, MD )
	self.lsCentralization_fields.Inc.put( pos, Inc )
	self.lsCentralization_fields.Azi.put( pos, Azi )
	self.lsCentralization_fields.EW.put( pos, EW )
	self.lsCentralization_fields.NS.put( pos, NS )
	self.lsCentralization_fields.TVD.put( pos, VD )
	self.lsCentralization_fields.HD.put( pos, HD )
	self.lsCentralization_fields.DL.put( pos, DL )
	self.lsCentralization_fields.ID.put( pos, ID )
	self.lsCentralization_fields.avgID.put( pos, avgID )
	self.lsCentralization_fields.Stage.put( pos, row )

	return True


def get_indexes_for_shoosing(self, r):

	cIndexes = np.array( [r-1,r,r+1] )
	where = np.where( np.logical_and(cIndexes>=0, cIndexes<self.centralizerCount) )
	cIndexes = cIndexes[where]

	mIndexes = np.array( [r-2,r-1,r,r+1] )
	where = np.where( np.logical_and(mIndexes>=0, mIndexes<self.centralizerCount) )
	mIndexes = mIndexes[where]

	indexes={'@c':cIndexes,'@m':mIndexes}

	return indexes


def get_indexes_for_removing(self, r):

	cIndexes = np.array( [r-1,r] )
	where = np.where( np.logical_and(cIndexes>=0, cIndexes<self.centralizerCount) )
	cIndexes = cIndexes[where]

	mIndexes = np.array( [r-2,r-1,r] )
	where = np.where( np.logical_and(mIndexes>=0, mIndexes<self.centralizerCount) )
	mIndexes = mIndexes[where]

	indexes={'@c':cIndexes,'@m':mIndexes}

	return indexes

	"""
	if r-2>=0:
		self.update_calculations(indexes={'@c':[r-1,r],'@m':[r-2,r-1,r]})
	elif r-1>=0:
		self.update_calculations(indexes={'@c':[r-1,r],'@m':[r-1,r]})
	else:
		self.update_calculations(indexes={'@c':[r],'@m':[r]})
	"""







