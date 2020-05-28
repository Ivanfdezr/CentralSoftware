import numpy as np
import numpy.linalg as la
from MdlUtilities import Field, FieldList
import MdlUtilities as mdl


def get_osaCasing_fields():

	Weight  = Field(2032)
	OD      = Field(2030)
	ID      = Field(2031)
	E       = Field(2040)
	Density = Field(2039)
	osaCasing_fields = FieldList()
	osaCasing_fields.append( Weight  )
	osaCasing_fields.append( OD      )
	osaCasing_fields.append( ID      )
	osaCasing_fields.append( E       )
	osaCasing_fields.append( Density )
	
	return osaCasing_fields


def get_osaCent_fields():

	RestForce      = Field(2018)
	CentOD         = Field(2011)
	CentID         = Field(2012)
	IPOD           = Field(2009)
	MinPassThru    = Field(2020)
	RestForce.set_representation('Restoring force')
	IPOD.set_representation('Inner pipe OD')
	osaCent_fields = FieldList()
	osaCent_fields.append( RestForce   )
	osaCent_fields.append( CentOD      )
	osaCent_fields.append( CentID      )
	osaCent_fields.append( IPOD        )
	osaCent_fields.append( MinPassThru )
	
	return osaCent_fields


def get_osaWellbore_fields():

	HoleID        = Field(2010)
	MaxSpan       = Field(2061)
	MudIPDensity  = Field(2077)
	MudOPDensity  = Field(2077)
	HoleID.set_representation('Hole ID')
	HoleID.set_abbreviation('HoleID')
	MaxSpan.set_representation('Max span')
	MaxSpan.set_abbreviation('MaxSpan')
	MudIPDensity.set_representation('Mud inside pipe')
	MudIPDensity.set_abbreviation('MudIPDensity')
	MudOPDensity.set_representation('Mud in annulus')
	MudOPDensity.set_abbreviation('MudOPDensity')
	osaWellbore_fields = FieldList()
	osaWellbore_fields.append( HoleID       )
	osaWellbore_fields.append( MaxSpan      )
	osaWellbore_fields.append( MudIPDensity )
	osaWellbore_fields.append( MudOPDensity )
	
	return osaWellbore_fields


def get_osaOutputdata1_fields():

	clearanceA  = Field(2073, altBg=True, altFg=True)
	clearanceB  = Field(2073, altBg=True, altFg=True)
	clearanceM  = Field(2073, altBg=True, altFg=True)
	sideForceA  = Field(2074, altBg=True, altFg=True)
	sideForceB  = Field(2074, altBg=True, altFg=True)
	sideForceM  = Field(2074, altBg=True, altFg=True)
	standoffA   = Field(2078, altBg=True, altFg=True)
	standoffB   = Field(2078, altBg=True, altFg=True)
	standoffM   = Field(2078, altBg=True, altFg=True)
	clearanceA.set_representation('Annular clearance @ cent. A')
	clearanceA.set_abbreviation('ClearanceA')
	clearanceB.set_representation('Annular clearance @ cent. B')
	clearanceB.set_abbreviation('ClearanceB')
	clearanceM.set_representation('Annular clearance @ mid span')
	clearanceM.set_abbreviation('ClearanceM')
	sideForceA.set_representation('Side force @ cent. A')
	sideForceA.set_abbreviation('SideForceA')
	sideForceB.set_representation('Side force @ cent. B')
	sideForceB.set_abbreviation('SideForceB')
	sideForceM.set_representation('Side force @ mid span')
	sideForceM.set_abbreviation('SideForceM')
	standoffA.set_representation('Standoff @ cent. A')
	standoffA.set_abbreviation('StandoffA')
	standoffB.set_representation('Standoff @ cent. B')
	standoffB.set_abbreviation('StandoffB')
	standoffM.set_representation('Standoff @ mid span')
	standoffM.set_abbreviation('StandoffM')
	osaOutputdata1_fields = FieldList()
	osaOutputdata1_fields.append( clearanceA )
	osaOutputdata1_fields.append( clearanceB )
	osaOutputdata1_fields.append( clearanceM )
	osaOutputdata1_fields.append( sideForceA )
	osaOutputdata1_fields.append( sideForceB )
	osaOutputdata1_fields.append( sideForceM )
	osaOutputdata1_fields.append( standoffA  )
	osaOutputdata1_fields.append( standoffB  )
	osaOutputdata1_fields.append( standoffM  )
	
	return osaOutputdata1_fields


def get_osaOutputdata2_fields():

	axialForce  = Field(2075, altBg=True, altFg=True)
	deflection  = Field(2076, altBg=True, altFg=True)
	wClearance  = Field(2073, altBg=True, altFg=True)
	wStandoff   = Field(2078, altBg=True, altFg=True)
	axialForce.set_representation('Axial extra force @ top')
	axialForce.set_abbreviation('AxialForce')
	deflection.set_representation('Max. pipe deflection')
	deflection.set_abbreviation('MaxDeflection')
	wClearance.set_representation('Mean wellbore clearance')
	wClearance.set_abbreviation('WellboreClearance')
	wStandoff.set_representation('Mean wellbore standoff')
	wStandoff.set_abbreviation('WellboreStandoff')
	osaOutputdata2_fields = FieldList()
	osaOutputdata2_fields.append( axialForce )
	osaOutputdata2_fields.append( deflection )
	osaOutputdata2_fields.append( wClearance )
	osaOutputdata2_fields.append( wStandoff )
	
	return osaOutputdata2_fields


def get_casingDeflectionCurve(self):

	# Equation(s) Reference 1:
	# 	Hans C. Juvkam-Wold, Jiang Wu. Casing Deflection and Centralizer Spacing Calculations.
	# 	SPE Drilling Engineering (December 1992).

	# Equation(s) Reference 2:
	# 	Hans C. Juvkam-Wold, Richard L. Baxter. Discussion of Optimal Spacing for Casing Centralizers.
	# 	SPE Drilling Engineering (December 1988).

	# Equation(s) Reference 3:
	# 	Carlos F. H. Fonseca, Jacques Braile. Optimizing of Centralizer Distribution.
	# 	SPE Latin American Petroleum Engineering Conference (October 1990).

	self.osaCasing_fields.referenceUnitConvert_fields()
	self.osaCentA_fields.referenceUnitConvert_fields()
	self.osaCentB_fields.referenceUnitConvert_fields()
	self.osaWellbore_fields.referenceUnitConvert_fields()

	Rot = lambda φ: np.array( [[np.cos(φ),-np.sin(φ)],[np.sin(φ),np.cos(φ)]] )

	dH = self.osaWellbore_fields.HoleID[0]
	L = self.osaWellbore_fields.MaxSpan[0]*self.osaSpacing_slider.sliderPosition()/100
	ρe = self.osaWellbore_fields.MudOPDensity[0]
	ρi = self.osaWellbore_fields.MudIPDensity[0]
	ρs = self.osaCasing_fields.Density[0]
	E = self.osaCasing_fields.E[0]
	w = self.osaCasing_fields.PW[0]
	D = self.osaCasing_fields.OD[0]
	d = self.osaCasing_fields.ID[0]
	ResFA = self.osaCentA_fields.ResF_SO67[0]
	ResFB = self.osaCentB_fields.ResF_SO67[0]
	DA = self.osaCentA_fields.COD[0]
	DB = self.osaCentB_fields.COD[0]
	dA = self.osaCentA_fields.CID[0]
	dB = self.osaCentB_fields.CID[0]
	#kA = ResFA/(DA/2-0.335*(DA-D)) # Con esto se calculan los coeficientes de los resortes ( 0.335=0.67/2 )
	#kB = ResFB/(DB/2-0.335*(DB-D))

	θ = np.pi*self.osaInclination_slider.sliderPosition()/180
	I = np.pi/64*(D**4-d**4) # [Ref.3] Momento de inercia diferente a momento de inercia polar.
	F = 30000 # [Ref.1]
	Radio = L*1e6
	aspr = L*0.02

	buoyancyFactor = mdl.calculate_buoyancyFactor( OD=D, ID=d, ρs=ρs, ρe=ρe, ρi=ρi ) # [Ref.2]
	w *= buoyancyFactor
	fC = w*L*np.sin(θ)/2

	if mdl.isNoneEntry(ResFA):
		yA = 0
		dA = d
	else:
		kA = 2*ResFA/( DA-dA-0.67*(dH-D) )
		yA = fC/kA
		

	if mdl.isNoneEntry(ResFB):
		yB = 0
		dB = d
	else:
		kB = 2*ResFB/( DB-dB-0.67*(dH-D) )
		yB = fC/kB
		

	R = D/2
	rH = dH/2
	rA_min = R+(DA/2-R)*0.1
	rB_min = R+(DB/2-R)*0.1
	rA = (DA/2-yA) if (DA<dH) else (rH-yA)
	rB = (DB/2-yB) if (DB<dH) else (rH-yB)

	rA = rA_min if (rA<=rA_min) else rA
	rB = rB_min if (rB<=rB_min) else rB

	α  = np.arctan( (rB-rA)/L )
	Lα = L/np.cos(α)
	x = np.linspace( 0, Lα, 101 )

	K = np.sqrt(F/E/I)
	y = (Lα/2/Radio/K + w*Lα*np.sin(θ)/2/K/F)*( (np.cosh(K*x)-1)/np.tanh(K*Lα/2) + K*x - np.sinh(K*x) ) - w*np.sin(θ)/2/F*x**2 # [Ref.1]
	Rα = Rot(α)
	xy = np.array([x,y])
	x,y = np.dot(Rα,xy)
	Δy = rH-rB
	y += Δy

	cH = rH-R
	cA = rA-R
	cB = rB-R
	
	indexes = y>cH
	y[indexes] = cH
	cy = cH-y

	rM = rH-y[50]
	if y[50]==cH:
		fM = fC
		fC = 0
	else:
		fM = 0
	cM = rM-R

	x -= L/2
	yoh = y*0
	ohc = np.array([x, yoh])
	ohp = np.array([x, (yoh+rH)*aspr])
	ohm = np.array([x, (yoh-rH)*aspr])

	xyc = np.array([x, y*aspr])
	xyp = np.array([x, (y+R)*aspr])
	xym = np.array([x, (y-R)*aspr])

	φ = θ + np.pi/2
	Rφ = Rot(φ)

	OHc = np.dot(Rφ,ohc)
	OHp = np.dot(Rφ,ohp)
	OHm = np.dot(Rφ,ohm)

	XYc = np.dot(Rφ,xyc)
	XYp = np.dot(Rφ,xyp)
	XYm = np.dot(Rφ,xym)

	SA = cA/cH
	SB = cB/cH
	SM = cM/cH
	Sy = cy/cH
	δ  = (cA+cB)/2-cM

	self.osaOutputdata1_fields.clear_content()
	self.osaOutputdata2_fields.clear_content()

	self.osaOutputdata1_fields.ClearanceA.append( mdl.physicalValue( cA, self.osaOutputdata1_fields.ClearanceA.referenceUnit ) )
	self.osaOutputdata1_fields.ClearanceB.append( mdl.physicalValue( cB, self.osaOutputdata1_fields.ClearanceB.referenceUnit ) )
	self.osaOutputdata1_fields.ClearanceM.append( mdl.physicalValue( cM, self.osaOutputdata1_fields.ClearanceM.referenceUnit ) )

	self.osaOutputdata1_fields.SideForceA.append( mdl.physicalValue( fC, self.osaOutputdata1_fields.SideForceA.referenceUnit ) )
	self.osaOutputdata1_fields.SideForceB.append( mdl.physicalValue( fC, self.osaOutputdata1_fields.SideForceB.referenceUnit ) )
	self.osaOutputdata1_fields.SideForceM.append( mdl.physicalValue( fM, self.osaOutputdata1_fields.SideForceM.referenceUnit ) )

	self.osaOutputdata1_fields.StandoffA.append( mdl.physicalValue( SA, self.osaOutputdata1_fields.StandoffA.referenceUnit ) )
	self.osaOutputdata1_fields.StandoffB.append( mdl.physicalValue( SB, self.osaOutputdata1_fields.StandoffB.referenceUnit ) )
	self.osaOutputdata1_fields.StandoffM.append( mdl.physicalValue( SM, self.osaOutputdata1_fields.StandoffM.referenceUnit ) )

	self.osaOutputdata2_fields.AxialForce.append( mdl.physicalValue( w*L*np.cos(θ), self.osaOutputdata2_fields.AxialForce.referenceUnit ) )
	self.osaOutputdata2_fields.MaxDeflection.append( mdl.physicalValue( δ, self.osaOutputdata2_fields.MaxDeflection.referenceUnit ) )
	self.osaOutputdata2_fields.WellboreClearance.append( mdl.physicalValue( np.mean(cy), self.osaOutputdata2_fields.WellboreClearance.referenceUnit ) )
	self.osaOutputdata2_fields.WellboreStandoff.append( mdl.physicalValue( np.mean(Sy), self.osaOutputdata2_fields.WellboreStandoff.referenceUnit ) )

	self.osaCasing_fields.inverseReferenceUnitConvert_fields()
	self.osaCentA_fields.inverseReferenceUnitConvert_fields()
	self.osaCentB_fields.inverseReferenceUnitConvert_fields()
	self.osaWellbore_fields.inverseReferenceUnitConvert_fields()
	self.osaOutputdata1_fields.inverseReferenceUnitConvert_fields()
	self.osaOutputdata2_fields.inverseReferenceUnitConvert_fields()

	lim = L/2*1.05



	return OHc, OHp, OHm, XYc, XYp, XYm, lim, rA, rB, rM



