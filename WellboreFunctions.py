from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
#from TubularDatabase_Ctrl import Main_TubularDatabase
#from CentralizerDatabase_Ctrl import Main_CentralizerDatabase
#from CaliperImport_Ctrl import Main_CaliperImport
#from CaliperInsertion_Ctrl import Main_CaliperInsertion
#from LocationSetup_Ctrl import Main_LocationSetup

import TubularDatabase_Ctrl as tdb
import CentralizerDatabase_Ctrl as cdb
import CaliperImport_Ctrl as cim
import CaliperInsertion_Ctrl as cin
import LocationSetup_Ctrl as ls
import SpacingSetup_Ctrl as ss
from functools import wraps
import InputWindow_Mdl as mdl
import CtrlUtilities as cu
import copy

import importlib



def init_s3CentralizerProperties_tableWidget(self, tab):

	s3CentralizerProperties_tableWidget = eval( 'self.s3CentralizerProperties_tableWidget_{tab}'.format(tab=tab) )
	s3CentralizerProperties_tableWidget.setContextMenuPolicy(Qt.ActionsContextMenu)
		
	C = cu.CopySelectedCells_action(s3CentralizerProperties_tableWidget)
	s3CentralizerProperties_tableWidget.addAction(C)
	
	V = cu.PasteToCells_action(s3CentralizerProperties_tableWidget)
	s3CentralizerProperties_tableWidget.addAction(V)

	setup_s3CentralizerProperties_tableWidget(self, tab)
	
	_update_fieldItem_and_wellboreInnerStageData = lambda item: update_fieldItem_and_wellboreInnerStageData(self, item)
	s3CentralizerProperties_tableWidget.itemChanged.connect(_update_fieldItem_and_wellboreInnerStageData)


def setup_s3CentralizerProperties_tableWidget(self, tab):

	s3CentralizerProperties_tableWidget = eval( 'self.s3CentralizerProperties_tableWidget_{tab}'.format(tab=tab) )
	s3CentralizerProperties_fields      = eval( 'self.v3CentralizerProperties_fields_{tab}'.format(tab=tab) )

	for field in s3CentralizerProperties_fields:
		
		item = QTableWidgetItem()
		s3CentralizerProperties_tableWidget.setVerticalHeaderItem(field.pos, item)
		item.setText( cu.extend_text( field.headerName, 25 ) )
		item = cu.TableWidgetFieldItem( field, False )
		s3CentralizerProperties_tableWidget.setItem(field.pos, 0, item)

"""
def init_s3CentralizerRunningForce_tableWidget(self, tab):

	s3CentralizerRunningForce_tableWidget = eval( 'self.s3CentralizerRunningForce_tableWidget_{tab}'.format(tab=tab) )
	s3CentralizerRunningForce_tableWidget.setContextMenuPolicy(Qt.ActionsContextMenu)
		
	C = cu.CopySelectedCells_action(s3CentralizerRunningForce_tableWidget)
	s3CentralizerRunningForce_tableWidget.addAction(C)
	
	V = cu.PasteToCells_action(s3CentralizerRunningForce_tableWidget)
	s3CentralizerRunningForce_tableWidget.addAction(V)

	clear_row = lambda: cu.clear_tableWidgetRow( s3CentralizerRunningForce_tableWidget)
	D = cu.FunctionToWidget_action(s3CentralizerRunningForce_tableWidget, clear_row, "Delete", "Del")
	s3CentralizerRunningForce_tableWidget.addAction(D)

	setup_s3CentralizerRunningForce_tableWidget(self, tab)

	s3CentralizerRunningForce_tableWidget.resizeColumnsToContents()
	_update_fieldItem_and_wellboreInnerStageData = lambda item: update_fieldItem_and_wellboreInnerStageData(self, item)
	s3CentralizerRunningForce_tableWidget.itemChanged.connect(_update_fieldItem_and_wellboreInnerStageData)
	select_row = lambda r,c : cu.select_tableWidgetRow(s3CentralizerRunningForce_tableWidget,r)
	s3CentralizerRunningForce_tableWidget.cellPressed.connect(select_row)
"""
"""
def setup_s3CentralizerRunningForce_tableWidget(self, tab):

	s3CentralizerRunningForce_tableWidget = eval( 'self.s3CentralizerRunningForce_tableWidget_{tab}'.format(tab=tab) )
	s3CentralizerRunningForce_fields      = eval( 'self.v3CentralizerRunningForce_fields_{tab}'.format(tab=tab) )

	for field in s3CentralizerRunningForce_fields:
		item = s3CentralizerRunningForce_tableWidget.horizontalHeaderItem( field.pos )
		item.setText( field.headerName )
		
		for i in range(s3CentralizerRunningForce_tableWidget.rowCount()):
			item = cu.TableWidgetFieldItem( field, i%2==0 )
			s3CentralizerRunningForce_tableWidget.setItem(i, field.pos, item)
"""

def init_s3CentralizerLocation_tableWidget(self, tab):

	s3CentralizerLocation_tableWidget = eval( 'self.s3CentralizerLocation_tableWidget_{tab}'.format(tab=tab) )
	s3CentralizerLocation_tableWidget.setContextMenuPolicy(Qt.ActionsContextMenu)
		
	C = cu.CopySelectedCells_action(s3CentralizerLocation_tableWidget)
	s3CentralizerLocation_tableWidget.addAction(C)
	
	V = cu.PasteToCells_action(s3CentralizerLocation_tableWidget)
	s3CentralizerLocation_tableWidget.addAction(V)

	clear_row = lambda: cu.clear_tableWidgetRow(s3CentralizerLocation_tableWidget)
	D = cu.FunctionToWidget_action(s3CentralizerLocation_tableWidget, clear_row, "Delete", "Del")
	s3CentralizerLocation_tableWidget.addAction(D)

	setup_s3CentralizerLocation_tableWidget(self, tab)

	_update_fieldItem_and_wellboreInnerStageData = lambda item: update_fieldItem_and_wellboreInnerStageData(self, item)
	s3CentralizerLocation_tableWidget.itemChanged.connect(_update_fieldItem_and_wellboreInnerStageData)
	select_row = lambda r,c : cu.select_tableWidgetRow(s3CentralizerLocation_tableWidget,r)
	s3CentralizerLocation_tableWidget.cellPressed.connect(select_row)


def setup_s3CentralizerLocation_tableWidget(self, tab):

	s3CentralizerLocation_tableWidget = eval( 'self.s3CentralizerLocation_tableWidget_{tab}'.format(tab=tab) )
	s3CentralizerLocation_fields      = eval( 'self.v3CentralizerLocation_fields_{tab}'.format(tab=tab) )

	for field in s3CentralizerLocation_fields:
		item = s3CentralizerLocation_tableWidget.horizontalHeaderItem( field.pos )
		item.setText( field.headerName )
		
		for i in range(s3CentralizerLocation_tableWidget.rowCount()):
			item = cu.TableWidgetFieldItem( field, i%2==0 )
			s3CentralizerLocation_tableWidget.setItem(i, field.pos, item)

# DECORATOR
def updateByBlock_currentWellboreInnerStageDataItem(function):
	@wraps(function)
	def wrap_function(*args, **kwargs):
		self = args[0]
		self.wellboreInnerStageDataIsUpdatable = False
		function(*args, **kwargs)
		self.wellboreInnerStageDataIsUpdatable = True
		update_wellboreInnerStageData(self)

	return wrap_function

# DECORATOR
def updateByBlock_currentWellboreOuterStageDataItem(function):
	@wraps(function)
	def wrap_function(*args, **kwargs):
		self = args[0]
		self.wellboreOuterStageDataIsUpdatable = False
		function(*args, **kwargs)
		self.wellboreOuterStageDataIsUpdatable = True
		update_wellboreOuterStageData(self)
		
	return wrap_function

# DECORATOR
def disableByBlock_currentWellboreInnerStageDataItem(function):
	@wraps(function)
	def wrap_function(*args, **kwargs):
		self = args[0]
		self.wellboreInnerStageDataIsEnabled = False
		function(*args, **kwargs)
		self.wellboreInnerStageDataIsEnabled = True

	return wrap_function


def update_fieldItem_and_wellboreInnerStageData(self, item):

	cu.update_fieldItem(item)
	update_wellboreInnerStageData(self)


def update_fieldItem_and_wellboreOuterStageData(self, item):

	cu.update_fieldItem(item)
	update_wellboreOuterStageData(self)


def update_wellboreInnerStageData(self):

	if self.wellboreInnerStageDataIsUpdatable and self.wellboreInnerStageDataIsEnabled:

		self.currentWellboreInnerStageDataItem.setup()
		self.v3PipeProperties_fields.clear_content()

		for field in self.v3PipeProperties_fields:

			item = self.s3PipeProperties_tableWidget.item(field.pos, 0)
			field.append(item.realValue)

		row = self.s3WellboreInnerStages_tableWidget.selectedRow
		description = self.v3WellboreInnerStages_fields.Desc
		descriptionItem = self.s3WellboreInnerStages_tableWidget.item(row, description.pos)

		self.currentWellboreInnerStageDataItem['PipeProps'] = copy.deepcopy(self.v3PipeProperties_fields)

		#K = list(self.v3WellboreInnerStageData.keys())
		#K.sort()

		K = mdl.get_sortedIndexes_of_wellboreInnerStageData(self)
		for k in K:
			stage = self.v3WellboreInnerStageData[k]
			if stage['PipeProps']==None:
				del stage

		if not self.s3EnableCentralization_checkBox.isChecked():
			descriptionItem.set_text( self.v3PipeProperties_fields.Desc[0] +'\nwithout Centralization'  )
			self.currentWellboreInnerStageDataItem['Desc'] = descriptionItem.text()
			self.ABC_tabWidget.setEnabled(False)
			return

		self.currentWellboreInnerStageDataItem['Centralization']['Mode'] = True
		descriptionItem.set_text( self.v3PipeProperties_fields.Desc[0] +'\nwith Centralization'  )
		self.currentWellboreInnerStageDataItem['Desc'] = descriptionItem.text()

		for tab in ['A','B','C']:

			if eval( 'self.s3BowSpringCentralizer_radioButton_{tab}.isChecked()'.format(tab=tab) ):
				self.currentWellboreInnerStageDataItem['Centralization'][tab]['Type'] = 'Bow Spring'
			
			elif eval( 'self.s3ResinCentralizer_radioButton_{tab}.isChecked()'.format(tab=tab) ):
				self.currentWellboreInnerStageDataItem['Centralization'][tab]['Type'] = 'Resin'
			
			else:
				continue

			s3CentralizerProperties_fields = eval( 'self.v3CentralizerProperties_fields_{tab}'.format(tab=tab) )
			s3CentralizerProperties_tableWidget = eval( 'self.s3CentralizerProperties_tableWidget_{tab}'.format(tab=tab) )
			s3CentralizerProperties_fields.clear_content()

			for field in s3CentralizerProperties_fields:

				item = s3CentralizerProperties_tableWidget.item(field.pos, 0)
				field.append(item.realValue)

			self.currentWellboreInnerStageDataItem['Centralization'][tab]['CentralizerProps'] = copy.deepcopy(s3CentralizerProperties_fields)

		mdl.setup_ensembles_fromConfiguration( self )
		self.s3StageEnsemble_label.setText( self.currentWellboreInnerStageDataItem['Centralization']['Ensemble']['label'] )
		numofJoins = len( self.currentWellboreInnerStageDataItem['Centralization']['Ensemble']['nest'])
		self.s3CentralizationPattern_spinBox.setMinimum( numofJoins )
		self.currentWellboreInnerStageDataItem['Centralization']['Pattern'] = self.s3CentralizationPattern_spinBox.value()
		self.currentWellboreInnerStageDataItem['Centralization']['Offset'] = self.s3CentralizationOffset_spinBox.value()

		if self.v3CentralizationProcessed_flag:
			self.v3CentralizationChanged_flag   = False
			self.v3CentralizationProcessed_flag = False
		else:
			self.v3CentralizationChanged_flag   = True
			self.v3CentralizationProcessed_flag = False


def update_wellboreOuterStageData(self):

	if self.wellboreOuterStageDataIsUpdatable:

		self.currentWellboreOuterStageDataItem['WellboreProps'] = None
		self.v3WellboreOuterStages_fields.clear_content()
		row = self.s3WellboreOuterStages_tableWidget.selectedRow

		for field in self.v3WellboreOuterStages_fields:

			item = self.s3WellboreOuterStages_tableWidget.item(row,field.pos)
			field.append(item.realValue)

		self.currentWellboreOuterStageDataItem['WellboreProps'] = copy.deepcopy(self.v3WellboreOuterStages_fields)

		workWellbore_exist = False

		K = mdl.get_sortedIndexes_of_wellboreOuterStageData(self)

		#K = list(self.v3WellboreOuterStageData.keys())
		#K.sort()
		for k in K:
			stage = self.v3WellboreOuterStageData[k]

			if stage['CaliperData']!=None:
				MD = stage['CaliperData']['MD_array']
				ID = stage['CaliperData']['CALmax_array']
			elif stage['WellboreProps']!=None:
				MD = cu.mdl.array( [stage['WellboreProps'].MDtop[0], stage['WellboreProps'].MDbot[0]] )
				ID = cu.mdl.array( [stage['WellboreProps'].DriftID[0], stage['WellboreProps'].DriftID[0]] )
			else:
				del self.v3WellboreOuterStageData[k]
				MD = cu.mdl.array([])
				ID = cu.mdl.array([])
				
			if workWellbore_exist:
				self.v3WorkWellboreMD = mdl.np.hstack( (self.v3WorkWellboreMD, MD) )
				self.v3WorkWellboreID = mdl.np.hstack( (self.v3WorkWellboreID, ID) )
			else:
				self.v3WorkWellboreMD = MD
				self.v3WorkWellboreID = ID
				workWellbore_exist = True

		#print_wellboreOuterStageData(self)
		#print('>> MD ID =',len(self.v3WorkWellboreMD),len(self.v3WorkWellboreID))


def save_information(self, row):

	row_=row+1

	cu.savetable( 	self.s3PipeProperties_tableWidget,
					self.v3PipeProperties_fields,
					self.v1WorkingDirectory+f"/PipeProperties_{row_}.csv",
					orientation='v' )

	cu.savetable( 	self.s3CentralizerProperties_tableWidget_A,
					self.v3CentralizerProperties_fields_A,
					self.v1WorkingDirectory+f"/CentralizerProperties_A_{row_}.csv",
					orientation='v' )

	cu.savetable( 	self.s3CentralizerProperties_tableWidget_B,
					self.v3CentralizerProperties_fields_B,
					self.v1WorkingDirectory+f"/CentralizerProperties_B_{row_}.csv",
					orientation='v' )

	cu.savetable( 	self.s3CentralizerProperties_tableWidget_C,
					self.v3CentralizerProperties_fields_C,
					self.v1WorkingDirectory+f"/CentralizerProperties_C_{row_}.csv",
					orientation='v' )

	cu.savetable( 	self.s3CentralizerLocation_tableWidget_A,
					self.v3WellboreInnerStageData[row]['Centralization']['Fields'].MD,
					self.v1WorkingDirectory+f"/CentralizerLocation_{row_}.csv" )

	try:
		stageLabel = self.currentWellboreInnerStageDataItem['Centralization']['Ensemble']['label']	
	except (KeyError, TypeError):
		stageLabel = '=\n|\n|\n|\n='
	self.s3StageEnsemble_label.setText( stageLabel )

	self.s3StageNumber_label1.setText( f"STAGE {row_}" )
	self.s3StageNumber_label2.setText( f"STAGE {row_}" )


@disableByBlock_currentWellboreInnerStageDataItem
def select_innerStageRow_and_prepare_innerStageObjects(self, row):

	self.currentWellboreInnerStageDataItem = None

	cu.select_tableWidgetRow(self.s3WellboreInnerStages_tableWidget, row)
	#self.s3InnerStageToolkit_tabWidget.setEnabled(False)

	clear_wellboreInnerStageToolkit(self)
	if row in self.v3WellboreInnerStageData:
		self.currentWellboreInnerStageDataItem = self.v3WellboreInnerStageData[row]
		load_wellboreInnerStageToolkit(self, self.v3WellboreInnerStageData[row])
	else:
		self.v3WellboreInnerStageData[row] = mdl.WellboreInnerStageDataItem(row)
		self.currentWellboreInnerStageDataItem = self.v3WellboreInnerStageData[row]

	"""
	try:
		stageLabel = self.currentWellboreInnerStageDataItem['Centralization']['Ensemble']['label']	
	except (KeyError, TypeError):
		stageLabel = '=\n|\n|\n|\n='
	self.s3StageEnsemble_label.setText( stageLabel )
	"""

	save_information(self, row)

	cu.idleFunction()
	print_wellboreInnerStageData(self)


def select_outerStageRow_and_prepare_outerStageObjects(self, row):

	self.currentWellboreOuterStageDataItem = None
	cu.select_tableWidgetRow(self.s3WellboreOuterStages_tableWidget, row)

	if not row in self.v3WellboreOuterStageData:
		self.v3WellboreOuterStageData[row] = mdl.WellboreOuterStageDataItem(row)
		
	self.currentWellboreOuterStageDataItem = self.v3WellboreOuterStageData[row]
	print_wellboreOuterStageData(self)


@updateByBlock_currentWellboreOuterStageDataItem
def delete_outerStageObjects(self):

	row = cu.clear_tableWidgetRow(self.s3WellboreOuterStages_tableWidget)
	del self.v3WellboreOuterStageData[row]
	#assert( row in self.v3WellboreOuterStageData )


@disableByBlock_currentWellboreInnerStageDataItem 
def delete_innerStageObjects(self):

	row = cu.clear_tableWidgetRow(self.s3WellboreInnerStages_tableWidget)
	clear_wellboreInnerStageToolkit(self)
	del self.v3WellboreInnerStageData[row]


#@updateByBlock_currentWellboreInnerStageDataItem
def clear_wellboreInnerStageToolkit(self):

	cu.clear_tableWidgetContent(self.s3PipeProperties_tableWidget)
	self.s3EnableCentralization_checkBox.setChecked(False)
	self.s3BowSpringCentralizer_radioButton_A.setChecked(True)
	self.s3NoneCentralizer_radioButton_B.setChecked(True)
	self.s3NoneCentralizer_radioButton_C.setChecked(True)
	self.ABC_tabWidget.setEnabled(False)

	for tab in ['A','B','C']:

		cu.clear_tableWidgetContent( eval( 'self.s3CentralizerProperties_tableWidget_{tab}'.format(tab=tab)) )
		#cu.clear_tableWidgetContent( eval( 'self.s3CentralizerRunningForce_tableWidget_{tab}'.format(tab=tab)) )
		cu.clear_tableWidgetContent( eval( 'self.s3CentralizerLocation_tableWidget_{tab}'.format(tab=tab)) )


#@updateByBlock_currentWellboreInnerStageDataItem
def load_wellboreInnerStageToolkit(self, dataItem):

	if dataItem['PipeProps']:
		for field in dataItem['PipeProps']:
			
			item = self.s3PipeProperties_tableWidget.item(field.pos,0)
			item.set_text( field[0], field[0].unit )
	
	if dataItem['Centralization']['Mode']:
		
		self.s3EnableCentralization_checkBox.setChecked(True)
		self.ABC_tabWidget.setEnabled(True)
		self.s3CentralizationPattern_spinBox.setValue( dataItem['Centralization']['Pattern'] )
		self.s3CentralizationOffset_spinBox.setValue( dataItem['Centralization']['Offset'] )
		#setEnabled_specifySpacingToolkit(self)
		#setEnabled_specifyLocationToolkit(self)

		for tab in ['A','B','C']:

			if dataItem['Centralization'][tab]['Type']:
				
				if dataItem['Centralization'][tab]['Type'] == 'Bow Spring':
					eval( 'self.s3BowSpringCentralizer_radioButton_{tab}.setChecked(True)'.format(tab=tab) )
					setEnabled_bowSpringToolkit(self, tab)
				elif dataItem['Centralization'][tab]['Type'] == 'Resin':
					eval( 'self.s3ResinCentralizer_radioButton_{tab}.setChecked(True)'.format(tab=tab) )
					setEnabled_rigidToolkit(self, tab)

				if dataItem['Centralization'][tab]['CentralizerProps']:
					for field in dataItem['Centralization'][tab]['CentralizerProps']:
						item = eval( 'self.s3CentralizerProperties_tableWidget_{tab}.item(field.pos,0)'.format(tab=tab) )
						item.set_text( field[0], field[0].unit )

				if dataItem['Centralization']['Fields']:
					for i,value in enumerate(dataItem['Centralization']['Fields'].MD):
						item = eval( 'self.s3CentralizerLocation_tableWidget_{tab}.item(i,0)'.format(tab=tab) )
						item.set_text( value, value.unit )

				"""
				if dataItem['Centralization'][tab]['RunningForce']:
					for field in dataItem['Centralization'][tab]['RunningForce']:	
						for i,value in enumerate(field):
							item = eval( 'self.s3CentralizerRunningForce_tableWidget_{tab}.item(i,field.pos)'.format(tab=tab) )
							item.set_text( value, value.unit )	
				"""

			else: 
				eval( 'self.s3NoneCentralizer_radioButton_{tab}.setChecked(True)'.format(tab=tab) )
				setDisabled_centralizerToolkit(self, tab)
				continue

	else:
		self.s3EnableCentralization_checkBox.setChecked(False)
		self.s3CentralizationPattern_spinBox.setValue( 1 )
		self.s3CentralizationOffset_spinBox.setValue( 0 )
		self.ABC_tabWidget.setEnabled(False)


@updateByBlock_currentWellboreInnerStageDataItem
def setEnabled_bowSpringToolkit(self, tab):

	s3CentralizerDB_pushButton            = eval( 'self.s3CentralizerDB_pushButton_{tab}'.format(tab=tab) )
	s3CentralizerProperties_tableWidget   = eval( 'self.s3CentralizerProperties_tableWidget_{tab}'.format(tab=tab) )
	s3CentralizerProperties_fields        = eval( 'self.v3CentralizerProperties_fields_{tab}'.format(tab=tab) )
	#s3CentralizerRunningForce_tableWidget = eval( 'self.s3CentralizerRunningForce_tableWidget_{tab}'.format(tab=tab) )
	s3CentralizerLocation_tableWidget     = eval( 'self.s3CentralizerLocation_tableWidget_{tab}'.format(tab=tab) )

	cu.clear_tableWidgetContent(s3CentralizerProperties_tableWidget)

	s3CentralizerDB_pushButton.setEnabled(True)
	s3CentralizerProperties_tableWidget.setEnabled(True)
	#s3CentralizerRunningForce_tableWidget.setEnabled(True)
	s3CentralizerLocation_tableWidget.setEnabled(True)

	field = s3CentralizerProperties_fields.FF
	item = s3CentralizerProperties_tableWidget.item(field.pos,0)
	item.alt_backgroundColor(False)
	item.alt_flags(False)

	field = s3CentralizerProperties_fields.StartF_CH
	item = s3CentralizerProperties_tableWidget.item(field.pos,0)
	item.alt_backgroundColor(False)
	item.alt_flags(False)

	field = s3CentralizerProperties_fields.StartF_OH
	item = s3CentralizerProperties_tableWidget.item(field.pos,0)
	item.alt_backgroundColor(False)
	item.alt_flags(False)

	field = s3CentralizerProperties_fields.ResF_CH
	item = s3CentralizerProperties_tableWidget.item(field.pos,0)
	item.alt_backgroundColor(False)
	item.alt_flags(False)

	field = s3CentralizerProperties_fields.ResF_OH
	item = s3CentralizerProperties_tableWidget.item(field.pos,0)
	item.alt_backgroundColor(False)
	item.alt_flags(False)


@updateByBlock_currentWellboreInnerStageDataItem
def setEnabled_rigidToolkit(self, tab):

	s3CentralizerDB_pushButton            = eval( 'self.s3CentralizerDB_pushButton_{tab}'.format(tab=tab) )
	s3CentralizerProperties_tableWidget   = eval( 'self.s3CentralizerProperties_tableWidget_{tab}'.format(tab=tab) )
	s3CentralizerProperties_fields        = eval( 'self.v3CentralizerProperties_fields_{tab}'.format(tab=tab) )
	#s3CentralizerRunningForce_tableWidget = eval( 'self.s3CentralizerRunningForce_tableWidget_{tab}'.format(tab=tab) )
	s3CentralizerLocation_tableWidget     = eval( 'self.s3CentralizerLocation_tableWidget_{tab}'.format(tab=tab) )

	cu.clear_tableWidgetContent(s3CentralizerProperties_tableWidget)

	s3CentralizerDB_pushButton.setEnabled(True)
	s3CentralizerProperties_tableWidget.setEnabled(True)
	#s3CentralizerRunningForce_tableWidget.setEnabled(False)
	s3CentralizerLocation_tableWidget.setEnabled(True)

	field = s3CentralizerProperties_fields.FF
	item = s3CentralizerProperties_tableWidget.item(field.pos,0)
	item.alt_backgroundColor()
	item.alt_flags()

	field = s3CentralizerProperties_fields.StartF_CH
	item = s3CentralizerProperties_tableWidget.item(field.pos,0)
	item.alt_backgroundColor()
	item.alt_flags()

	field = s3CentralizerProperties_fields.StartF_OH
	item = s3CentralizerProperties_tableWidget.item(field.pos,0)
	item.alt_backgroundColor()
	item.alt_flags()

	field = s3CentralizerProperties_fields.ResF_CH
	item = s3CentralizerProperties_tableWidget.item(field.pos,0)
	item.alt_backgroundColor()
	item.alt_flags()

	field = s3CentralizerProperties_fields.ResF_OH
	item = s3CentralizerProperties_tableWidget.item(field.pos,0)
	item.alt_backgroundColor()
	item.alt_flags()


@updateByBlock_currentWellboreInnerStageDataItem
def setDisabled_centralizerToolkit(self, tab):

	s3CentralizerDB_pushButton             = eval( 'self.s3CentralizerDB_pushButton_{tab}'.format(tab=tab) )
	s3CentralizerProperties_tableWidget    = eval( 'self.s3CentralizerProperties_tableWidget_{tab}'.format(tab=tab) )
	#s3CentralizerRunningForce_tableWidget  = eval( 'self.s3CentralizerRunningForce_tableWidget_{tab}'.format(tab=tab) )
	s3CentralizerLocation_tableWidget      = eval( 'self.s3CentralizerLocation_tableWidget_{tab}'.format(tab=tab) )

	cu.clear_tableWidgetContent(s3CentralizerProperties_tableWidget)
	s3CentralizerDB_pushButton.setEnabled(False)
	s3CentralizerProperties_tableWidget.setEnabled(False)
	#s3CentralizerRunningForce_tableWidget.setEnabled(False)
	s3CentralizerLocation_tableWidget.setEnabled(False)


@updateByBlock_currentWellboreInnerStageDataItem
def setEnabled_specifySpacingToolkit(self):

	self.ABC_tabWidget.setEnabled(True)

	for tab in ['A','B','C']:

		s3CentralizerLocation_tableWidget = eval( 'self.s3CentralizerLocation_tableWidget_{tab}'.format(tab=tab) )
		s3CentralizerLocation_tableWidget.setEnabled(True)


@updateByBlock_currentWellboreInnerStageDataItem
def setEnabled_specifyLocationToolkit(self):

	self.ABC_tabWidget.setEnabled(True)

	for tab in ['A','B','C']:

		s3CentralizerLocation_tableWidget   = eval( 'self.s3CentralizerLocation_tableWidget_{tab}'.format(tab=tab) )
		s3BowSpringCentralizer_radioButton  = eval( 'self.s3BowSpringCentralizer_radioButton_{tab}'.format(tab=tab) )
		s3ResinCentralizer_radioButton      = eval( 'self.s3ResinCentralizer_radioButton_{tab}'.format(tab=tab) )

		if s3BowSpringCentralizer_radioButton.isChecked() or s3ResinCentralizer_radioButton.isChecked():
			s3CentralizerLocation_tableWidget.setEnabled(True)


@updateByBlock_currentWellboreInnerStageDataItem
def valueChangedAction(self, value):
	
	pass


@updateByBlock_currentWellboreInnerStageDataItem
def open_TDB_dialog_for_innerStages(self):
	
	importlib.reload(tdb)

	dialog = QDialog(self.s3PipeProperties_tableWidget)
	TDB = tdb.Main_TubularDatabase(dialog)
	if 'fields' not in dir(TDB): return
	self.currentWellboreInnerStageDataItem['PipeBase'] = TDB.fields

	for field in self.v3PipeProperties_fields:

		item = self.s3PipeProperties_tableWidget.item(field.pos,0)

		if field.abbreviation in TDB.data:
			value = TDB.data[field.abbreviation]
			item.set_text( value, value.unit )
		else:
			item.set_text()
			self.s3PipeProperties_tableWidget.editItem(item)


@updateByBlock_currentWellboreInnerStageDataItem
def open_CDB_dialog(self, tab):
	
	importlib.reload(cdb)

	s3BowSpringCentralizer_radioButton    = eval( 'self.s3BowSpringCentralizer_radioButton_{tab}'.format(tab=tab) )
	s3ResinCentralizer_radioButton        = eval( 'self.s3ResinCentralizer_radioButton_{tab}'.format(tab=tab) )
	s3CentralizerProperties_tableWidget   = eval( 'self.s3CentralizerProperties_tableWidget_{tab}'.format(tab=tab) )
	s3CentralizerProperties_fields        = eval( 'self.v3CentralizerProperties_fields_{tab}'.format(tab=tab) )
	#s3CentralizerRunningForce_tableWidget = eval( 'self.s3CentralizerRunningForce_tableWidget_{tab}'.format(tab=tab) )	
	#s3CentralizerRunningForce_fields      = eval( 'self.v3CentralizerRunningForce_fields_{tab}'.format(tab=tab) )

	dialog = QDialog(self.ABC_tabWidget)
	
	if s3BowSpringCentralizer_radioButton.isChecked():
		CDB = cdb.Main_CentralizerDatabase(dialog, 'Bow Spring' )
	elif s3ResinCentralizer_radioButton.isChecked():
		CDB = cdb.Main_CentralizerDatabase(dialog, 'Resin' )
	
	if 'fields' not in dir(CDB): return
	self.currentWellboreInnerStageDataItem['Centralization'][tab]['CentralizerBase'] = CDB.fields

	for field in s3CentralizerProperties_fields:

		item = s3CentralizerProperties_tableWidget.item(field.pos,0)

		if field.abbreviation in CDB.data:
			value = CDB.data[field.abbreviation]
			if value:
				item.set_text( value, value.unit )
			else:
				value = CDB.data[field.substitute]
				item.set_text( value, value.unit )
		elif field.substitute in CDB.data:
			value = CDB.data[field.substitute]
			item.set_text( value, value.unit )
		else:
			item.set_text()
			s3CentralizerProperties_tableWidget.editItem(item)


@updateByBlock_currentWellboreInnerStageDataItem
def open_specifyCentralization_dialog(self):
	
	#try:
	mdl.get_centralizationLocations( self )
	print_wellboreInnerStageData(self)
	open_LS_dialog(self)
	#except (AssertionError, IndexError):
	#	msg = 'Some Pattern and Offset combinations are not suitable\nfor the number of joins in the stages.'
	#	QMessageBox.critical(self.s3WellboreInnerStages_tableWidget, 'Error', msg)
	

@updateByBlock_currentWellboreInnerStageDataItem
def open_LS_dialog(self):

	importlib.reload(ls)

	mdl.get_centralizationLocations( self )
	print_wellboreInnerStageData(self)

	dialog = QDialog(self.s3ManageLocations_pushButton)
	LS = ls.Main_LocationSetup(dialog, self)
	del dialog 

	if not hasattr(LS, 'fields'):
		self.v3CentralizationChanged_flag = False
		return

	K = mdl.get_sortedIndexes_of_wellboreInnerStageData(self)
	for k in K:
		datafields = self.v3WellboreInnerStageData[k]['Centralization']['Fields']
		if datafields==None:
			continue
		datafields.clear_content()

	for i,row in enumerate(LS.fields.Stage):
		datafields = self.v3WellboreInnerStageData[row]['Centralization']['Fields']
		for lsfield in LS.fields:
			if lsfield.abbreviation!='Stage':
				datafield = getattr( datafields, lsfield.abbreviation )
				datafield.append( lsfield[i] )

		
	currfields = self.currentWellboreInnerStageDataItem['Centralization']['Fields']

	for tab in ['A','B','C']:
		s3CentralizerLocation_tableWidget = eval( 'self.s3CentralizerLocation_tableWidget_{tab}'.format(tab=tab) )	
		s3CentralizerLocation_fields      = eval( 'self.v3CentralizerLocation_fields_{tab}'.format(tab=tab) )

		field = s3CentralizerLocation_fields.MD
		if self.currentWellboreInnerStageDataItem['Centralization'][tab]['Type']!=None:
			for i in range(s3CentralizerLocation_tableWidget.rowCount()):
				item = s3CentralizerLocation_tableWidget.item(i,field.pos)
				try:
					value = currfields.MD[i]
					item.set_text( value, value.unit )
				except IndexError:
					item.set_text()

	self.meanSOatC = LS.meanSOatC
	self.meanSOatM = LS.meanSOatM

	self.v4TorqueDragForces_fields.MD[:]     = LS.fields.MD
	self.v4TorqueDragForces_fields.AxialF[:] = LS.fields.AFatC
	self.v4TorqueDragForces_fields.SideF[:]  = LS.fields.SFatC

	print('+++++++++++++++++++++++++++++++++++++++++++')
	for field in LS.fields:
		print(field.abbreviation,len(field))
	print('+++++++++++++++++++++++++++++++++++++++++++')


	self.v3SOs_MD = []
	self.v3SOs_SO = []
	
	for k in range(2*len(LS.fields.MD)-1):
		if k%2==0:
			self.v3SOs_MD.append( LS.fields.MD[k//2] )
			self.v3SOs_SO.append( LS.fields.SOatC[k//2] )
		elif k%2==1:
			self.v3SOs_MD.append( (LS.fields.MD[(k+1)//2]+LS.fields.MD[(k-1)//2])/2 )
			self.v3SOs_SO.append( LS.fields.SOatM[k//2] )


	for i, (AF, SF) in enumerate(zip(LS.fields.AFatM[:-1], LS.fields.SFatM[:-1])):
		MD0 = LS.fields.MD[i]
		MD1 = LS.fields.MD[i+1]
		MDm = mdl.mu.physicalValue( (MD1+MD0)/2, LS.fields.MD.unit )
		self.v4TorqueDragForces_fields.MD.insert(i*2+1, MDm)
		self.v4TorqueDragForces_fields.AxialF.insert(i*2+1, AF)
		self.v4TorqueDragForces_fields.SideF.insert(i*2+1, SF)

	if self.v4TorqueDragForces_fields.MD[0]!=self.v3Forces_fields.MD[0]:
		self.v4TorqueDragForces_fields.MD.insert( 0, self.v3Forces_fields.MD[0])
		self.v4TorqueDragForces_fields.AxialF.insert( 0, self.v3Forces_fields.AxialF[0] )
		self.v4TorqueDragForces_fields.SideF.insert( 0, self.v3Forces_fields.SideF[0] )

	if self.v4TorqueDragForces_fields.MD[-1]!=self.v3Forces_fields.MD[-1]:
		self.v4TorqueDragForces_fields.MD.append( self.v3Forces_fields.MD[-1])
		self.v4TorqueDragForces_fields.AxialF.append( self.v3Forces_fields.AxialF[-1] )
		self.v4TorqueDragForces_fields.SideF.append( self.v3Forces_fields.SideF[-1] )

	self.msg_label.setText( 'Mean SO at centralizers:   {meanSOatC} {unit} ,   Mean SO at minspan:   {meanSOatM} {unit}'.format(
							meanSOatC=LS.meanSOatC, meanSOatM=LS.meanSOatM, unit=LS.fields.SOatC.unit ) )
	del LS
	cu.idleFunction()


@updateByBlock_currentWellboreInnerStageDataItem
def open_SS_dialog(self):

	importlib.reload(ss)
	
	dialog = QDialog(self.s3ManageLocations_pushButton)
	SS = ss.Main_SpacingSetup(dialog, self)
	self.currentWellboreInnerStageDataItem['Centralization']['Fields'] = SS.fields

	for tab in ['A','B','C']:
		s3CentralizerLocation_tableWidget = eval( 'self.s3CentralizerLocation_tableWidget_{tab}'.format(tab=tab) )	
		s3CentralizerLocation_fields      = eval( 'self.v3CentralizerLocation_fields_{tab}'.format(tab=tab) )

		field = s3CentralizerLocation_fields.MD
		if self.currentWellboreInnerStageDataItem['Centralization'][tab]['Type']!=None:
			for i in range(s3CentralizerLocation_tableWidget.rowCount()):
				item = s3CentralizerLocation_tableWidget.item(i,field.pos)
				try:
					value = SS.fields.MD[i]
					item.set_text( value, value.unit )
				except IndexError:
					item.set_text()

	self.msg_label.setText( 'Mean SO at centralizers:   {meanSOatC} {unit} ,   Mean SO at minspan:   {meanSOatM} {unit}'.format(
							meanSOatC=SS.meanSOatC, meanSOatM=SS.meanSOatM, unit=SS.fields.SOatC.unit ) )
	cu.idleFunction()
	self.meanSOatC = SS.meanSOatC
	self.meanSOatM = SS.meanSOatM


@updateByBlock_currentWellboreOuterStageDataItem
def open_caliper_dialog(self):

	importlib.reload(cim)

	dialog = QDialog(self.s3WellboreOuterStages_tableWidget)
	CI = cim.Main_CaliperImport(dialog, self)
	if 'data' not in dir(CI): return

	row = self.s3WellboreOuterStages_tableWidget.selectedRow
	self.currentWellboreOuterStageDataItem['CaliperData'] = {	'CAL_fields': CI.ciCALData_fields, 
																'MD_field': CI.ciLASData_fields.MD,
																'CALmax_array': CI.CALID_max,
																'MD_array': CI.MD 
															}
	for field in self.v3WellboreOuterStages_fields:

		item = self.s3WellboreOuterStages_tableWidget.item(row, field.pos)

		if field.abbreviation in CI.data:
			value = CI.data[field.abbreviation]
			item.set_text( value, value.unit )
			field._altFg_ = True
		else:
			item.set_text()
			item.alt_backgroundColor()
			item.alt_flags()
			self.s3WellboreOuterStages_tableWidget.editItem(item)
			field._altFg_ = False


@updateByBlock_currentWellboreOuterStageDataItem
def open_csv_dialog(self):

	importlib.reload(cin)

	dialog = QDialog(self.s3WellboreOuterStages_tableWidget)
	CI = cin.Main_CaliperInsertion(dialog)
	if 'data' not in dir(CI): return

	row = self.s3WellboreOuterStages_tableWidget.selectedRow
	self.currentWellboreOuterStageDataItem['CaliperData'] = {	'CAL_fields': [CI.csvCal_fields.HID], 
																'MD_field': CI.csvCal_fields.MD,
																'CALmax_array': CI.HID,
																'MD_array': CI.MD 
															}
	for field in self.v3WellboreOuterStages_fields:

		item = self.s3WellboreOuterStages_tableWidget.item(row, field.pos)

		if field.abbreviation in CI.data:
			value = CI.data[field.abbreviation]
			item.set_text( value, value.unit )
			field._altFg_ = True
		else:
			item.set_text()
			item.alt_backgroundColor()
			item.alt_flags()
			self.s3WellboreOuterStages_tableWidget.editItem(item)
			field._altFg_ = False


@updateByBlock_currentWellboreOuterStageDataItem
def open_TDB_dialog_for_outerStages(self):
	
	importlib.reload(tdb)

	dialog = QDialog(self.s3WellboreOuterStages_tableWidget)
	TDB = tdb.Main_TubularDatabase(dialog)
	row = self.s3WellboreOuterStages_tableWidget.selectedRow
	self.currentWellboreOuterStageDataItem['PipeBase'] = TDB.fields

	for field in self.v3WellboreOuterStages_fields:

		item = self.s3WellboreOuterStages_tableWidget.item(row, field.pos)

		if field.abbreviation in TDB.data:
			value = TDB.data[field.abbreviation]
			item.set_text( value, value.unit )
			field._altFg_ = True
		else:
			item.set_text()
			item.alt_backgroundColor()
			item.alt_flags()
			self.s3WellboreOuterStages_tableWidget.editItem(item)
			field._altFg_ = False


def set_row_as_free(self): #, description):

	row = self.s3WellboreOuterStages_tableWidget.selectedRow
	#self.s3WellboreOuterStages_tableWidget.item(row, 0).set_text( description )
	
	for column in [5,4,3,2,1,0]:
		item = self.s3WellboreOuterStages_tableWidget.item(row, column)
		item.set_text()
		item.alt_backgroundColor()
		item.alt_flags()
		item.field._altFg_ = False
	
	self.s3WellboreOuterStages_tableWidget.editItem(item)


def updateMD_wellboreInnerStageData(self, item):

	if self.wellboreInnerStageDataIsUpdatable:

		cu.update_fieldItem(item)
		self.s3UpdateInnerStages_pushButton.setEnabled(True)

		row = self.s3WellboreInnerStages_tableWidget.selectedRow

		if item.field.pos == self.v3WellboreInnerStages_fields.MDtop.pos:
			self.v3WellboreInnerStageData[row]['MDtop'] = item.realValue

		elif item.field.pos == self.v3WellboreInnerStages_fields.MDbot.pos:
			self.v3WellboreInnerStageData[row]['MDbot'] = item.realValue

		else:
			self.v3WellboreInnerStageData[row]['Desc'] = item.text()


def adjust_MD_to_wellboreDeep(self):

	try:
		deepestMD = max(self.v3WorkWellboreMD)
	except ValueError:
		msg = "Any bottom MD has been assigned yet in Wellbore intervals. Can not proceed."
		QMessageBox.critical(self.s3WellboreInnerStages_tableWidget, 'Error', msg)
		self._PipeCentralizationStageAdjusting_isEnabled = True
		return

	row  = self.s3WellboreInnerStages_tableWidget.selectedRow
	item = self.s3WellboreInnerStages_tableWidget.item(row, self.v3WellboreInnerStages_fields.MDbot.pos)
	item.set_text( deepestMD )


def adjust_Wt(self):

	OD = self.s3PipeProperties_tableWidget.item(self.v3PipeProperties_fields.OD.pos,0).realValue
	ID = self.s3PipeProperties_tableWidget.item(self.v3PipeProperties_fields.ID.pos,0).realValue
	Wt = self.s3PipeProperties_tableWidget.item(self.v3PipeProperties_fields.PipeW.pos,0).realValue
	Wt = mdl.adjust_Wt( OD, ID, Wt )
	self.s3PipeProperties_tableWidget.item(self.v3PipeProperties_fields.PipeW.pos,0).set_text(Wt)


def adjust_ID(self):

	OD = self.s3PipeProperties_tableWidget.item(self.v3PipeProperties_fields.OD.pos,0).realValue
	ID = self.s3PipeProperties_tableWidget.item(self.v3PipeProperties_fields.ID.pos,0).realValue
	Wt = self.s3PipeProperties_tableWidget.item(self.v3PipeProperties_fields.PipeW.pos,0).realValue
	ID = mdl.adjust_ID( OD, ID, Wt )
	self.s3PipeProperties_tableWidget.item(self.v3PipeProperties_fields.ID.pos,0).set_text(ID)
	


def print_wellboreInnerStageData(self):

	print('-----------------------------------------')
	K = mdl.get_sortedIndexes_of_wellboreInnerStageData(self)
	#K = self.v3WellboreInnerStageData.keys()
	#K.sort()
	for k in K:
		print('\n',self.v3WellboreInnerStageData[k],'\n')
	print('-----------------------------------------\n')
	pass

def print_wellboreOuterStageData(self):
	
	print('vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv')
	K = mdl.get_sortedIndexes_of_wellboreOuterStageData(self)
	#K = self.v3WellboreOuterStageData.keys()
	#K.sort()
	for k in K:
		print('\n',self.v3WellboreOuterStageData[k],'\n')
	print('vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv\n')
	pass






