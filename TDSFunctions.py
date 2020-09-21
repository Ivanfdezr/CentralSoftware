from PyQt4 import QtCore, QtGui
import InputWindow_Mdl as mdl
import CtrlUtilities as cu
import PlotUtilities as pu
import MdlUtilities as mu


def calculateAndDraw_torque_drag_sideforce(self):

	for field in self.v4TorqueDragForces_fields:
		print(field.headerName, len(field), field)
	
	calculate_TorqueAndDrag( self )

	for field in self.v4TorqueDragForces_fields:
		print(field.headerName, len(field), field)

	TDS_fields = self.v4TorqueDragForces_fields

	for field in self.v4TorqueDragForces_fields[:7]:
		for row,value in enumerate(field):
			item = self.s4TorqueDragSideforce_tableWidget.item( row, field.pos )
			item.set_text( value, value.unit )

	max_MD = max( TDS_fields.MD )

	self.s4Drag_graphicsView.axes.clear()
	self.s4Drag_graphicsView.axes.set_xlabel( TDS_fields.Drag_s.headerName )
	self.s4Drag_graphicsView.axes.set_ylabel( TDS_fields.MD.headerName )
	#self.s4Drag_graphicsView.axes.set_xlim( 0, self.max_SO )
	self.s4Drag_graphicsView.axes.set_ylim( max_MD*1.2, 0 )
	self.s4Drag_graphicsView.axes.grid()
	self.s4Drag_graphicsView.axes.plot( TDS_fields.Drag_u, TDS_fields.MD, 'C0', lw=2 )
	self.s4Drag_graphicsView.axes.plot( TDS_fields.Drag_s, TDS_fields.MD, 'C1', lw=2 )
	self.s4Drag_graphicsView.axes.plot( TDS_fields.Drag_d, TDS_fields.MD, 'C2', lw=2 )
	self.s4Drag_graphicsView.axes.plot( TDS_fields.uncDrag_u, TDS_fields.MD, 'C0--', lw=2 )
	self.s4Drag_graphicsView.axes.plot( TDS_fields.uncDrag_s, TDS_fields.MD, 'C1--', lw=2 )
	self.s4Drag_graphicsView.axes.plot( TDS_fields.uncDrag_d, TDS_fields.MD, 'C2--', lw=2 )
	self.s4Drag_graphicsView.draw()

	#---------------------------------------------
	self.s4Torque_graphicsView.axes.clear()
	self.s4Torque_graphicsView.axes.set_xlabel( TDS_fields.Torque.headerName )
	self.s4Torque_graphicsView.axes.set_ylabel( TDS_fields.MD.headerName )
	#self.s4Torque_graphicsView.axes.set_xlim( 0, self.max_SO )
	self.s4Torque_graphicsView.axes.set_ylim( max_MD*1.2, 0 )
	self.s4Torque_graphicsView.axes.grid()
	self.s4Torque_graphicsView.axes.plot( TDS_fields.Torque, TDS_fields.MD, 'C0', lw=2 )
	self.s4Torque_graphicsView.axes.plot( TDS_fields.uncTorque, TDS_fields.MD, 'C0--', lw=2 )
	self.s4Torque_graphicsView.draw()

	#---------------------------------------------
	
	self.s4Sideforce_graphicsView.axes.set_position([0.2,0.15,0.75,0.8])
	zp = pu.ZoomPan()
	zp.zoom2D_factory( self.s4Sideforce_graphicsView.axes )
	zp.pan2D_factory( self.s4Sideforce_graphicsView.axes )
	self.s4Sideforce_graphicsView.axes.clear()

	max_VD = max( self.v3Forces_fields.TVD )
	min_VD = min( self.v3Forces_fields.TVD )
	max_SF = max( self.v3Forces_fields.SideF )

	self.s4Sideforce_graphicsView.axes.axis('equal')
	self.s4Sideforce_graphicsView.axes.set_ylim( max_VD, min_VD )
	self.s4Sideforce_graphicsView.axes.set_xlabel( self.v3Forces_fields.HD.headerName )
	self.s4Sideforce_graphicsView.axes.set_ylabel( self.v3Forces_fields.TVD.headerName )
	
	self.s4Sideforce_graphicsView.axes.plot( self.v3Forces_fields.HD, self.v3Forces_fields.TVD, 'C0', lw=3 )
	factor = max(self.v3Forces_fields.HD)/max(self.v3Forces_fields.SideF)*0.5
	for i,MDi in enumerate(self.v3Forces_fields.MD):
		HDi = self.v3Forces_fields.HD[i]
		VDi = self.v3Forces_fields.TVD[i]
		DFi = self.v3Forces_fields.DLplaneF[i]
		SFi = self.v3Forces_fields.SideF[i]

		T = mdl.get_ASCT_from_MD(self, MDi, MDi.unit)
		t = mu.np.array([ T[3], T[2], 0 ])
		t = t.reshape(1,-1)
		normt = mu.np.linalg.norm(t)
		if normt!=0.0:
			t /=normt
		u = mu.np.array([ 0, 0, -DFi ])
		u = u.reshape(1,-1)
		normu = mu.np.linalg.norm(u)
		if normu!=0.0:
			u /=normu
		
		if normt==0 or normu==0:
			n = mu.np.array([ 0, 0, 0 ])
			n = n.reshape(1,-1)
		else:
			n = mu.np_cross(t,u)
			n *= SFi*factor

		self.s4Sideforce_graphicsView.axes.arrow(HDi, VDi, n[0][0], n[0][1], head_width=factor*0.1, head_length=factor*0.2, fc='C1', ec='C1')
		#self.s4Sideforce_graphicsView.axes.arrow(HDi, VDi, t[0][0], t[0][1], head_width=factor*0.1, head_length=factor*0.2, fc='C1', ec='C1')

	for stage in self.v3WellboreInnerStageData.values():
		MDbot = stage['MDbot']
		EW,NS,VD,HD,i = mdl.get_ASCCoordinates_from_MD(self, MDbot)

		T = mdl.get_ASCT_from_MD(self, MDbot, MDbot.unit)
		t = mu.np.array([ T[3], T[2], 0 ])
		t = t.reshape(1,-1)
		normt = mu.np.linalg.norm(t)
		if normt!=0.0:
			t /=normt
		u = mu.np.array([ 0, 0, 1 ])
		u = u.reshape(1,-1)
		nu = mu.np_cross(t,u)
		nu *= 1.2*max_SF*factor

		d = mu.np.array([ 0, 0, -1 ])
		d = d.reshape(1,-1)
		nd = mu.np_cross(t,d)
		nd *= 1.2*max_SF*factor

		self.s4Sideforce_graphicsView.axes.arrow(HD, VD, nu[0][0], nu[0][1], head_width=0, head_length=0, fc='k', ec='k', lw=0.5, alpha=0.5)
		self.s4Sideforce_graphicsView.axes.arrow(HD, VD, nd[0][0], nd[0][1], head_width=0, head_length=0, fc='k', ec='k', lw=0.5, alpha=0.5)


	#-------------------------------------------------

	self.s4HookLoad_graphicsView.axes.clear()
	self.s4HookLoad_graphicsView.axes.set_xlabel( TDS_fields.Drag_s.headerName )
	self.s4HookLoad_graphicsView.axes.set_ylabel( TDS_fields.MD.headerName )
	self.s4HookLoad_graphicsView.axes.set_ylim( max_MD*1.2, 0 )
	self.s4HookLoad_graphicsView.axes.grid()
	max_Drag_u = max(TDS_fields.Drag_u)
	max_Drag_s = max(TDS_fields.Drag_s)
	max_Drag_d = max(TDS_fields.Drag_d)
	max_uncDrag_u = max(TDS_fields.uncDrag_u)
	max_uncDrag_s = max(TDS_fields.uncDrag_s)
	max_uncDrag_d = max(TDS_fields.uncDrag_d)
	self.s4HookLoad_graphicsView.axes.plot( max_Drag_u-mu.array(TDS_fields.Drag_u), TDS_fields.MD, 'C0', lw=2 )
	self.s4HookLoad_graphicsView.axes.plot( max_Drag_s-mu.array(TDS_fields.Drag_s), TDS_fields.MD, 'C1', lw=2 )
	self.s4HookLoad_graphicsView.axes.plot( max_Drag_d-mu.array(TDS_fields.Drag_d), TDS_fields.MD, 'C2', lw=2 )
	self.s4HookLoad_graphicsView.axes.plot( max_uncDrag_u-mu.array(TDS_fields.uncDrag_u), TDS_fields.MD, 'C0--', lw=2 )
	self.s4HookLoad_graphicsView.axes.plot( max_uncDrag_s-mu.array(TDS_fields.uncDrag_s), TDS_fields.MD, 'C1--', lw=2 )
	self.s4HookLoad_graphicsView.axes.plot( max_uncDrag_d-mu.array(TDS_fields.uncDrag_d), TDS_fields.MD, 'C2--', lw=2 )
	self.s4HookLoad_graphicsView.draw()
	


def calculate_TorqueAndDrag( self ):
	
	#self.v4TorqueDragForces_fields.MD.clear()
	self.v4TorqueDragForces_fields.Torque.clear()
	self.v4TorqueDragForces_fields.Drag_u.clear()
	self.v4TorqueDragForces_fields.Drag_s.clear()
	self.v4TorqueDragForces_fields.Drag_d.clear()
	self.v4TorqueDragForces_fields.uncTorque.clear()
	self.v4TorqueDragForces_fields.uncDrag_u.clear()
	self.v4TorqueDragForces_fields.uncDrag_s.clear()
	self.v4TorqueDragForces_fields.uncDrag_d.clear()
	self.v4Settings_fields.Psi.clear()
	self.v4Settings_fields.dMD.clear()

	#for field in self.v4Settings_fields[:5]:
	#	value = self.s4Settings_tableWidget.item(field.pos,0).realValue
	#	field.append( value )

	#if len(self.v3WellboreInnerStageData):
	#	msg = "Any inner wellbore stage completed. Can not proceed."
	#	QtGui.QMessageBox.critical(self.s4TorqueDragSideforce_tableWidget, 'Error', msg)
	#	return
	
	K = list( mdl.get_sortedIndexes_of_wellboreInnerStageData(self) )
	K.reverse()
	set_initial_TDSConditions_to_fields( self, self.v3WellboreInnerStageData[K[0]]['PipeProps'].OD[0] )
	mdl.calculate_TDS(self)
	

	"""

	K = get_sortedIndexes_of_wellboreInnerStageData(self)
	K.reverse()

	for k in K:
		stage = self.v3WellboreInnerStageData[k]
		
		if stage['Centralization']['Fields']==None or len(stage['Centralization']['Fields'].MD)==0:
			mdl.calculate_TDS_for_uncentralizedStage(self, stage)
		else:
			mdl.calculate_TDS_for_centralizedStage(self, stage)
			mdl.calculate_TDS_for_uncentralizedStage(self, stage)
	"""


def set_initial_TDSConditions_to_fields(self, diameter):

	# Verify WOB, TOB, TAW if they are not filled set 0
	
	if self.v4Settings_fields.WOB==[]:
		mu.create_physicalValue_and_appendTo_field( 0, self.v4Settings_fields.WOB )
	#self.v4Settings_fields.WOB.referenceUnitConvert()

	if self.v4Settings_fields.TOB==[]:
		mu.create_physicalValue_and_appendTo_field( 0, self.v4Settings_fields.TOB )
	#self.v4Settings_fields.TOB.referenceUnitConvert()

	if self.v4Settings_fields.TAW==[]:
		mu.create_physicalValue_and_appendTo_field( 0, self.v4Settings_fields.TAW )
	#self.v4Settings_fields.TAW.referenceUnitConvert()

	if self.v4Settings_fields.TrV==[]:
		mu.create_physicalValue_and_appendTo_field( 0, self.v4Settings_fields.TrV )
	#self.v4Settings_fields.TrV.referenceUnitConvert()

	if self.v4Settings_fields.RoR==[]:
		mu.create_physicalValue_and_appendTo_field( 0, self.v4Settings_fields.RoR )
	#self.v4Settings_fields.RoR.referenceUnitConvert()

	mdl.calculate_psiAngle( self, diameter )
	mdl.set_stepMD( self )


		








	
	