import InputWindow_Mdl as mdl
import CtrlUtilities as cu
import PlotUtilities as pu
import MdlUtilities as mu


def calculateAndDraw_torque_drag_sideforce(self):

	print( '!!!',self.s4Settings_fields )

	calculate_inclination_torque_drag_sideforce( self )

	TDS_fields = self.s4TorqueDragSideforce_fields

	for field in self.s4TorqueDragSideforce_fields[:9]:
		for row,value in enumerate(field):
			item = self.s4TorqueDragSideforce_tableWidget.item( row, field.pos )
			item.set_text( value, value.unit )

	max_MD = max( [max( TDS_fields.MD ), max( TDS_fields.uncMD )] )

	self.s4Drag_graphicsView.axes.clear()
	self.s4Drag_graphicsView.axes.set_xlabel( TDS_fields.Drag_s.headerName )
	self.s4Drag_graphicsView.axes.set_ylabel( TDS_fields.MD.headerName )
	#self.s4Drag_graphicsView.axes.set_xlim( 0, self.max_SO )
	self.s4Drag_graphicsView.axes.set_ylim( max_MD*1.2, 0 )
	self.s4Drag_graphicsView.axes.grid()
	self.s4Drag_graphicsView.axes.semilogx( TDS_fields.Drag_u, TDS_fields.MD, 'C0', lw=2 )
	self.s4Drag_graphicsView.axes.semilogx( TDS_fields.Drag_s, TDS_fields.MD, 'C1', lw=2 )
	self.s4Drag_graphicsView.axes.semilogx( TDS_fields.Drag_d, TDS_fields.MD, 'C2', lw=2 )
	self.s4Drag_graphicsView.axes.semilogx( TDS_fields.uncDrag_u, TDS_fields.uncMD, 'C0--', lw=2 )
	self.s4Drag_graphicsView.axes.semilogx( TDS_fields.uncDrag_s, TDS_fields.uncMD, 'C1--', lw=2 )
	self.s4Drag_graphicsView.axes.semilogx( TDS_fields.uncDrag_d, TDS_fields.uncMD, 'C2--', lw=2 )
	self.s4Drag_graphicsView.draw()

	#---------------------------------------------
	self.s4Torque_graphicsView.axes.clear()
	self.s4Torque_graphicsView.axes.set_xlabel( TDS_fields.Torque_s.headerName )
	self.s4Torque_graphicsView.axes.set_ylabel( TDS_fields.MD.headerName )
	#self.s4Torque_graphicsView.axes.set_xlim( 0, self.max_SO )
	self.s4Torque_graphicsView.axes.set_ylim( max_MD*1.2, 0 )
	self.s4Torque_graphicsView.axes.grid()
	self.s4Torque_graphicsView.axes.plot( TDS_fields.Torque_u, TDS_fields.MD, 'C0', lw=2 )
	self.s4Torque_graphicsView.axes.plot( TDS_fields.Torque_s, TDS_fields.MD, 'C1', lw=2 )
	self.s4Torque_graphicsView.axes.plot( TDS_fields.Torque_d, TDS_fields.MD, 'C2', lw=2 )
	self.s4Torque_graphicsView.axes.plot( TDS_fields.uncTorque_u, TDS_fields.uncMD, 'C0--', lw=2 )
	self.s4Torque_graphicsView.axes.plot( TDS_fields.uncTorque_s, TDS_fields.uncMD, 'C1--', lw=2 )
	self.s4Torque_graphicsView.axes.plot( TDS_fields.uncTorque_d, TDS_fields.uncMD, 'C2--', lw=2 ) 
	self.s4Torque_graphicsView.draw()

	#---------------------------------------------
	self.s4Sideforce_graphicsView.axes.clear()
	self.s4Sideforce_graphicsView.axes.set_xlabel( TDS_fields.SideF.headerName )
	self.s4Sideforce_graphicsView.axes.set_ylabel( TDS_fields.MD.headerName )
	#self.s4Sideforce_graphicsView.axes.set_xlim( 0, self.max_SO )
	self.s4Sideforce_graphicsView.axes.set_ylim( max_MD*1.2, 0 )
	self.s4Sideforce_graphicsView.axes.grid()
	self.s4Sideforce_graphicsView.axes.plot( TDS_fields.SideF, TDS_fields.MD, 'C0', lw=2 )
	self.s4Sideforce_graphicsView.axes.plot( TDS_fields.uncSideF, TDS_fields.uncMD, 'C0--', lw=2 ) 
	self.s4Sideforce_graphicsView.draw()

	for field in self.s4TorqueDragSideforce_fields:
		print(field.headerName, len(field), field)


def calculate_inclination_torque_drag_sideforce( self ):
	
	self.s4TorqueDragSideforce_fields.clear_content()
	self.s4Settings_fields.Psi.clear()
	self.s4Settings_fields.dMD.clear()

	#for field in self.s4Settings_fields[:5]:
	#	value = self.s4Settings_tableWidget.item(field.pos,0).realValue
	#	field.append( value )

	K = list(self.wellboreInnerStageData.keys())
	if K==[]:
		msg = "Any inner wellbore stage completed. Can not proceed."
		QtGui.QMessageBox.critical(self.s4TorqueDragSideforce_tableWidget, 'Error', msg)
		return
	K.sort()
	K.reverse()

	set_initial_TDSConditions_to_fields( self, self.wellboreInnerStageData[K[0]]['PipeProps'].OD[0] )

	for k in K:
		stage = self.wellboreInnerStageData[k]
		
		if stage['Centralization']['Fields']==None or len(stage['Centralization']['Fields'].MD)==0:
			mdl.calculate_TDS_for_uncentralizedStage(self, stage)
		else:
			mdl.calculate_TDS_for_centralizedStage(self, stage)
			mdl.calculate_TDS_for_uncentralizedStage(self, stage)

	self.s4TorqueDragSideforce_fields.inverseReferenceUnitConvert_fields()


def set_initial_TDSConditions_to_fields(self, diameter):

	# Verify WOB, TOB, TAW if they are not filled set 0
	
	if self.s4Settings_fields.WOB==[]:
		mu.create_physicalValue_and_appendTo_field( 0, self.s4Settings_fields.WOB )
	#self.s4Settings_fields.WOB.referenceUnitConvert()

	if self.s4Settings_fields.TOB==[]:
		mu.create_physicalValue_and_appendTo_field( 0, self.s4Settings_fields.TOB )
	#self.s4Settings_fields.TOB.referenceUnitConvert()

	if self.s4Settings_fields.TAW==[]:
		mu.create_physicalValue_and_appendTo_field( 0, self.s4Settings_fields.TAW )
	#self.s4Settings_fields.TAW.referenceUnitConvert()

	if self.s4Settings_fields.TrV==[]:
		mu.create_physicalValue_and_appendTo_field( 0, self.s4Settings_fields.TrV )
	#self.s4Settings_fields.TrV.referenceUnitConvert()

	if self.s4Settings_fields.RoR==[]:
		mu.create_physicalValue_and_appendTo_field( 1e-6, self.s4Settings_fields.RoR )
	elif self.s4Settings_fields.RoR[0]==0.0:
		del self.s4Settings_fields.RoR[0]
		mu.create_physicalValue_and_appendTo_field( 1e-6, self.s4Settings_fields.RoR )
	#self.s4Settings_fields.RoR.referenceUnitConvert()

	mdl.calculate_psiAngle( self, diameter )
	mdl.set_stepMD( self )


		








	
	