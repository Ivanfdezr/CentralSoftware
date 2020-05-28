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
	SOatC = mu.Field(2078, altBg=True, altFg=True)
	SOatM = mu.Field(2078, altBg=True, altFg=True)
	ClatC = mu.Field(2073, altBg=True, altFg=True)
	ClatM = mu.Field(2073, altBg=True, altFg=True)
	LatC  = mu.Field(2080, altBg=True, altFg=True)
	EW    = mu.Field(2007, altBg=True, altFg=True)
	NS    = mu.Field(2006, altBg=True, altFg=True)
	TVD   = mu.Field(2004, altBg=True, altFg=True)
	DL    = mu.Field(2008, altBg=True, altFg=True)
	ID    = mu.Field(2031, altBg=True, altFg=True)
	avgID = mu.Field(2031, altBg=True, altFg=True)
	Azi   = mu.Field(2003, altBg=True, altFg=True)
	Stage = mu.Field(2000, altBg=True, altFg=True)

	SOatC.set_abbreviation('SOatC')
	SOatM.set_abbreviation('SOatM')
	ClatC.set_abbreviation('ClatC')
	ClatM.set_abbreviation('ClatM')
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
	lsCentralization_fields.append( ClatC )
	lsCentralization_fields.append( ClatM )
	lsCentralization_fields.append( LatC )
	lsCentralization_fields.append( EW )
	lsCentralization_fields.append( NS )
	lsCentralization_fields.append( TVD )
	lsCentralization_fields.append( DL )
	lsCentralization_fields.append( ID )
	lsCentralization_fields.append( avgID )
	lsCentralization_fields.append( Azi )
	lsCentralization_fields.append( Stage )

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
		rows = [mu.physicalValue(stage['row'],'1') for md in fields.MD]

		self.lsCentralization_fields.MD.extend( fields.MD )
		self.lsCentralization_fields.Inc.extend( fields.Inc )
		self.lsCentralization_fields.Azi.extend( fields.Azi )
		self.lsCentralization_fields.EW.extend( fields.EW )
		self.lsCentralization_fields.NS.extend( fields.NS )
		self.lsCentralization_fields.TVD.extend( fields.TVD )
		self.lsCentralization_fields.DL.extend( fields.DL )
		self.lsCentralization_fields.ID.extend( fields.ID )
		self.lsCentralization_fields.avgID.extend( fields.avgID )
		self.lsCentralization_fields.Stage.extend( rows )

	PL  = stage['PipeBase'].PL[0]
	CEL = stage['Centralization']['Ensemble']['PLfactor']*PL*0.9
	if self.lsCentralization_fields.MD[-1] + CEL > stage['MDbot']:
		self.lsCentralization_fields.MD.pop()
		self.lsCentralization_fields.Inc.pop()
		self.lsCentralization_fields.Azi.pop()
		self.lsCentralization_fields.EW.pop()
		self.lsCentralization_fields.NS.pop()
		self.lsCentralization_fields.TVD.pop()
		self.lsCentralization_fields.DL.pop()
		self.lsCentralization_fields.ID.pop()
		self.lsCentralization_fields.avgID.pop()
		self.lsCentralization_fields.Stage.pop()

	for field in self.lsCentralization_fields:
		print(field.abbreviation,len(field))

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


def calculate_standOff_at_Centralizers(self):

	Loc_field = self.lsCentralization_fields.MD
	Inc_field = self.lsCentralization_fields.Inc
	Azi_field = self.lsCentralization_fields.Azi
	SOatC_field = self.lsCentralization_fields.SOatC
	ClatC_field = self.lsCentralization_fields.ClatC
	LatC_field = self.lsCentralization_fields.LatC
	ID_field = self.lsCentralization_fields.ID
	avgID_field = self.lsCentralization_fields.avgID
	stage_field = self.lsCentralization_fields.Stage

	Loc_field.referenceUnitConvert()
	Inc_field.referenceUnitConvert()
	Azi_field.referenceUnitConvert()
	SOatC_field.referenceUnitConvert()
	ClatC_field.referenceUnitConvert()
	LatC_field.referenceUnitConvert()
	ID_field.referenceUnitConvert()
	avgID_field.referenceUnitConvert()

	def calculate_SO_per_centralizersEnsemble():
			SO = []
			Cc = []
			L = []
			Δs = get_separationsInEnsemble( c['Ensemble']['nest'], PL )
			Δa = 0

			for x,Δ in zip(['A','B','C'],Δs):
				
				Δa += Δ
				if c[x]['Type']!=None:
					so, cc, l = calculate_SO_per_centralizer(x,c[x]['Type'],supports,Δ)
					SO.append( so )
					Cc.append( cc )
					L.append( l )

			return np.mean(SO), np.mean(Cc), np.mean(L)

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
	for j, (MD1,Hd,mHd) in enumerate(zip(Loc_field, ID_field, avgID_field)):
		#stageRow = SOcalculation_job( j, MD1 ,Hd, mHd, stageRow )

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

			elif c[x]['Type']=='Rigid':
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
			MD0 = Loc_field[i] + CEL
			In0 = Inc_field[i] + 1e-12
			Az0 = Azi_field[i]
			if MD0>MD1:
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
					f = Ft*np.sin(In1)/supports

				elif MD2==None:
					f = PWb*L*np.sin(In1)/supports

				else:
					Ft = mdl.get_axialTension_below_MD(self.parent, MD2, referenceUnit=True)
					u = np.sqrt( Ft*L**2/4/PE/PI )
					β = np.arccos( np.cos(In0)*np.cos(In2) + np.sin(In0)*np.sin(In2)*np.cos(Az2-Az0) )
					
					if β==0.0:
						f = 0.0
					else:
						cosγ0 = np.sin(In0)*np.sin(In2)*np.sin(Az2-Az0)/np.sin(β)
						cosγn = np.sin( (In0-In2)/2 )*np.sin( (In0+In2)/2 )/np.sin(β/2)

						Fldp = PWb*L*cosγn + 2*Ft*np.sin(β/2)
						Flp  = PWb*L*cosγ0
						f   = np.sqrt( Fldp**2 + Flp**2 )/supports

				#f = PWb*L*np.sin(In1)/supports
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
			
			return SO, Cc, L
		
		SO, Cc, L = calculate_SO_per_centralizersEnsemble()

		#SO = mu.physicalValue( SO, SOatC_field.referenceUnit )
		#Cc = mu.physicalValue( Cc, ClatC_field.referenceUnit )
		#L  = mu.physicalValue( L, LatC_field.referenceUnit )

		#SOatC_field.put( j, SO )
		#ClatC_field.put( j, Cc )
		#LatC_field.put( j, L )

		mu.create_physicalValue_and_appendTo_field( SO, SOatC_field, SOatC_field.referenceUnit )
		mu.create_physicalValue_and_appendTo_field( Cc, ClatC_field, ClatC_field.referenceUnit )
		mu.create_physicalValue_and_appendTo_field( L, LatC_field, LatC_field.referenceUnit )

	Loc_field.inverseReferenceUnitConvert()
	Inc_field.inverseReferenceUnitConvert()
	SOatC_field.inverseReferenceUnitConvert()
	ClatC_field.inverseReferenceUnitConvert()
	LatC_field.inverseReferenceUnitConvert()
	ID_field.inverseReferenceUnitConvert()
	avgID_field.inverseReferenceUnitConvert()

	print('............................................')
	print('C: ',len(Loc_field),len(SOatC_field),len(Inc_field))
	assert(len(Loc_field)==len(SOatC_field)==len(Inc_field))
	#for x,s,i in zip(Loc_field,SOatC_field,Inc_field):
	#	print(x,'\t',s,'\t',i)
	


def calculate_standOff_at_Midspans(self):

	Loc_field = self.lsCentralization_fields.MD
	Inc_field = self.lsCentralization_fields.Inc
	Azi_field = self.lsCentralization_fields.Azi
	SOatM_field = self.lsCentralization_fields.SOatM
	ClatM_field = self.lsCentralization_fields.ClatM
	ClatC_field = self.lsCentralization_fields.ClatC
	ID_field = self.lsCentralization_fields.ID
	avgID_field = self.lsCentralization_fields.avgID
	stage_field = self.lsCentralization_fields.Stage

	Loc_field.referenceUnitConvert()
	ClatC_field.referenceUnitConvert()
	SOatM_field.referenceUnitConvert()
	ClatM_field.referenceUnitConvert()
	Inc_field.referenceUnitConvert()
	Azi_field.referenceUnitConvert()
	ID_field.referenceUnitConvert()
	avgID_field.referenceUnitConvert()

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
			cosγn = np.sin( (In1-In2)/2 )*np.sin( (In1+In2)/2 )/np.sin(β/2)

			Fldp = PWb*L*cosγn + 2*Ft*np.sin(β/2)
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
		Mc = Mc if (Mc>xHc) else xHc
		SO = Mc/mHc

		mu.create_physicalValue_and_appendTo_field( SO, SOatM_field, SOatM_field.referenceUnit )
		mu.create_physicalValue_and_appendTo_field( Mc, ClatM_field, ClatM_field.referenceUnit )

	mu.create_physicalValue_and_appendTo_field( 0, SOatM_field, SOatM_field.referenceUnit )
	mu.create_physicalValue_and_appendTo_field( 0, ClatM_field, ClatM_field.referenceUnit )

	Loc_field.inverseReferenceUnitConvert()
	ClatC_field.inverseReferenceUnitConvert()
	SOatM_field.inverseReferenceUnitConvert()
	ClatM_field.inverseReferenceUnitConvert()
	Inc_field.inverseReferenceUnitConvert()
	Azi_field.inverseReferenceUnitConvert()
	ID_field.inverseReferenceUnitConvert()
	avgID_field.inverseReferenceUnitConvert()

	print('............................................')
	print('M: ',len(Loc_field),len(SOatM_field),len(Inc_field))
	assert(len(Loc_field)==len(SOatM_field)==len(Inc_field))
	#for x,s,i in zip(Loc_field,SOatM_field,Inc_field):
	#	print(x,'\t',s,'\t',i)


def get_stage_at_MD(self, MD):

	for stage in self.parent.v3WellboreInnerStageData.values():

		if MD>=stage['MDtop'] and MD<=stage['MDbot']:
			return stage

	raise( mu.LogicalError )








