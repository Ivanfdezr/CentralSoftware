import InputWindow_Mdl as mdl
import CtrlUtilities as cu
import PlotUtilities as pu
import MdlUtilities as mu


def calculateAndDraw_drag_torque_sideforce(self):

	calculate_inclination_drag_torque_sideforce( self )

	for field in self.s4DragTorqueSideforce_fields:
		for row,value in enumerate(field):
			item = self.s4DragTorqueSideforce_tableWidget.item( row, field.pos, row%2 )
			item.set_text( value, value.unit )

	self.s4Drag_graphicsView.axes.clear()
	self.s4Drag_graphicsView.axes.set_xlabel( self.s4Settings_fields.Drag.headerName )
	self.s4Drag_graphicsView.axes.set_ylabel( self.s4Settings_fields.MD.headerName )
	#self.s4Drag_graphicsView.axes.set_xlim( 0, self.max_SO )
	#self.s4Drag_graphicsView.axes.set_ylim( self.max_MD, self.min_MD )
	self.s4Drag_graphicsView.axes.grid()
	self.s4Drag_graphicsView.axes.plot( self.s4Settings_fields.Drag, self.s4Settings_fields.MD, 'C0', lw=2 ) 
	self.s4Drag_graphicsView.draw()

	#---------------------------------------------
	self.s4Torque_graphicsView.axes.clear()
	self.s4Torque_graphicsView.axes.set_xlabel( self.s4Settings_fields.Torque.headerName )
	self.s4Torque_graphicsView.axes.set_ylabel( self.s4Settings_fields.MD.headerName )
	#self.s4Torque_graphicsView.axes.set_xlim( 0, self.max_SO )
	#self.s4Torque_graphicsView.axes.set_ylim( self.max_MD, self.min_MD )
	self.s4Torque_graphicsView.axes.grid()
	self.s4Torque_graphicsView.axes.plot( self.s4Settings_fields.Torque, self.s4Settings_fields.MD, 'C0', lw=2 ) 
	self.s4Torque_graphicsView.draw()

	#---------------------------------------------
	self.s4Sideforce_graphicsView.axes.clear()
	self.s4Sideforce_graphicsView.axes.set_xlabel( self.s4Settings_fields.SideF.headerName )
	self.s4Sideforce_graphicsView.axes.set_ylabel( self.s4Settings_fields.MD.headerName )
	#self.s4Sideforce_graphicsView.axes.set_xlim( 0, self.max_SO )
	#self.s4Sideforce_graphicsView.axes.set_ylim( self.max_MD, self.min_MD )
	self.s4Sideforce_graphicsView.axes.grid()
	self.s4Sideforce_graphicsView.axes.plot( self.s4Settings_fields.SideF, self.s4Settings_fields.MD, 'C0', lw=2 ) 
	self.s4Sideforce_graphicsView.draw()


def calculate_inclination_drag_torque_sideforce( self ):
	
	K = list(self.wellboreInnerStageData.keys())
	K.sort()
	K.reverse()

	set_initial_TDSConditions_to_fields(self)

	for k in K:
		stage = self.wellboreInnerStageData[k]
		
		if stage['Centralization']['Fields']==None or len(currentStage['Centralization']['Fields'].MD)==0:
			calculate_TDS_for_uncentralizedStage(self, stage)
		else:
			calculate_TDS_for_centralizedStage(self, stage)


def set_initial_TDSConditions_to_fields(self):

	# Verify WOB, TOB, TAW if they are not filled set 0
	
	if self.s4Settings_fields.WOB==[]:
		WOB = mu.physicalValue( 0, self.s4Settings_fields.WOB.unit )
	else:
		WOB = self.s4Settings_fields.WOB[0]

	if self.s4Settings_fields.TOB==[]:
		TOB = mu.physicalValue( 0, self.s4Settings_fields.TOB.unit )
	else:
		TOB = self.s4Settings_fields.TOB[0]

	if self.s4Settings_fields.TAW==[]:
		TAW = mu.physicalValue( 0, self.s4Settings_fields.TAW.unit )
	else:
		TAW = self.s4Settings_fields.TAW[0]

	if self.s4Settings_fields.TrV==[]:
		TrV = mu.physicalValue( 0, self.s4Settings_fields.TrV.unit )
	else:
		TrV = self.s4Settings_fields.TrV[0]

	if self.s4Settings_fields.RoR==[]:
		RoR = mu.physicalValue( 0, self.s4Settings_fields.RoR.unit )
	else:
		RoR = self.s4Settings_fields.RoR[0]


	
	