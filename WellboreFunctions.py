from PyQt4 import QtCore, QtGui
from TubularDatabase_Ctrl import Main_TubularDatabase
from CentralizerDatabase_Ctrl import Main_CentralizerDatabase
from CaliperImport_Ctrl import Main_CaliperImport
from functools import wraps
import InputWindow_Mdl as mdl
import CtrlUtilities as cu
import copy

import importlib



def init_s3CentralizerProperties_tableWidget(self, tab):

	s3CentralizerProperties_tableWidget = eval( 'self.s3CentralizerProperties_tableWidget_{tab}'.format(tab=tab) )
	s3CentralizerProperties_tableWidget.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
		
	C = cu.CopySelectedCells_action(s3CentralizerProperties_tableWidget)
	s3CentralizerProperties_tableWidget.addAction(C)
	
	V = cu.PasteToCells_action(s3CentralizerProperties_tableWidget)
	s3CentralizerProperties_tableWidget.addAction(V)

	setup_s3CentralizerProperties_tableWidget(self, tab)
	
	_update_fieldItem_and_wellboreInnerStageData = lambda item: update_fieldItem_and_wellboreInnerStageData(self, item)
	s3CentralizerProperties_tableWidget.itemChanged.connect(_update_fieldItem_and_wellboreInnerStageData)


def setup_s3CentralizerProperties_tableWidget(self, tab):

	s3CentralizerProperties_tableWidget = eval( 'self.s3CentralizerProperties_tableWidget_{tab}'.format(tab=tab) )
	s3CentralizerProperties_fields      = eval( 'self.s3CentralizerProperties_fields_{tab}'.format(tab=tab) )

	for field in s3CentralizerProperties_fields:
		
		item = QtGui.QTableWidgetItem()
		s3CentralizerProperties_tableWidget.setVerticalHeaderItem(field.pos, item)
		item.setText( cu.extend_text( field.headerName, 25 ) )
		item = cu.TableWidgetFieldItem( field, False )
		s3CentralizerProperties_tableWidget.setItem(field.pos, 0, item)


def init_s3CentralizerRunningForce_tableWidget(self, tab):

	s3CentralizerRunningForce_tableWidget = eval( 'self.s3CentralizerRunningForce_tableWidget_{tab}'.format(tab=tab) )
	s3CentralizerRunningForce_tableWidget.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
		
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


def setup_s3CentralizerRunningForce_tableWidget(self, tab):

	s3CentralizerRunningForce_tableWidget = eval( 'self.s3CentralizerRunningForce_tableWidget_{tab}'.format(tab=tab) )
	s3CentralizerRunningForce_fields      = eval( 'self.s3CentralizerRunningForce_fields_{tab}'.format(tab=tab) )

	for field in s3CentralizerRunningForce_fields:
		item = s3CentralizerRunningForce_tableWidget.horizontalHeaderItem( field.pos )
		item.setText( field.headerName )
		
		for i in range(s3CentralizerRunningForce_tableWidget.rowCount()):
			item = cu.TableWidgetFieldItem( field, i%2==0 )
			s3CentralizerRunningForce_tableWidget.setItem(i, field.pos, item)


def init_s3CentralizerLocation_tableWidget(self, tab):

	s3CentralizerLocation_tableWidget = eval( 'self.s3CentralizerLocation_tableWidget_{tab}'.format(tab=tab) )
	s3CentralizerLocation_tableWidget.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
		
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
	s3CentralizerLocation_fields      = eval( 'self.s3CentralizerLocation_fields_{tab}'.format(tab=tab) )

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
		print_wellboreInnerStageData(self)

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
		#

	return wrap_function


def update_fieldItem_and_wellboreInnerStageData(self, item):

	cu.update_fieldItem(item)
	update_wellboreInnerStageData(self)
	#print_wellboreInnerStageData(self)


def update_fieldItem_and_wellboreOuterStageData(self, item):

	cu.update_fieldItem(item)
	update_wellboreOuterStageData(self)


def update_wellboreInnerStageData(self):

	if self.wellboreInnerStageDataIsUpdatable and self.wellboreInnerStageDataIsEnabled:

		self.currentWellboreInnerStageDataItem.setup()
		self.s3PipeProperties_fields.clear_content()

		for field in self.s3PipeProperties_fields:

			item = self.s3PipeProperties_tableWidget.item(field.pos, 0)
			field.append(item.realValue)

		row = self.s3PipeCentralizationStage_tableWidget.selectedRow
		description = self.s3PipeCentralizationStage_fields.Desc
		descriptionItem = self.s3PipeCentralizationStage_tableWidget.item(row, description.pos)

		self.currentWellboreInnerStageDataItem['PipeProps'] = copy.deepcopy(self.s3PipeProperties_fields)

		K = list(self.wellboreInnerStageData.keys())
		K.sort()
		for k in K:
			stage = self.wellboreInnerStageData[k]
			if stage['PipeProps']==None:
				del stage

		if self.s3SpecifySpacingCentralization_radioButton.isChecked():
			label = 'by Spacing'
		
		elif self.s3SpecifyLocationCentralization_radioButton.isChecked():
			label = 'by Location'

		#elif self.s3SpecifyStandoffCentralization_radioButton.isChecked():
		#	label = 'by Standoff'

		elif self.s3NoneCentralization_radioButton.isChecked():
			descriptionItem.set_text( self.s3PipeProperties_fields.Desc[0] +'\nwithout Centralization'  )
			return

		self.currentWellboreInnerStageDataItem['Centralization']['Mode'] = label
		descriptionItem.set_text( self.s3PipeProperties_fields.Desc[0] +'\nwith Centralization '+label  )

		for tab in ['A','B','C']:

			if eval( 'self.s3BowSpringCentralizer_radioButton_{tab}.isChecked()'.format(tab=tab) ):
				self.currentWellboreInnerStageDataItem['Centralization'][tab]['Type'] = 'Bow Spring'
			
			elif eval( 'self.s3RigidCentralizer_radioButton_{tab}.isChecked()'.format(tab=tab) ):
				self.currentWellboreInnerStageDataItem['Centralization'][tab]['Type'] = 'Rigid'
			
			else:
				continue

			s3CentralizerProperties_fields = eval( 'self.s3CentralizerProperties_fields_{tab}'.format(tab=tab) )
			s3CentralizerProperties_tableWidget = eval( 'self.s3CentralizerProperties_tableWidget_{tab}'.format(tab=tab) )
			s3CentralizerProperties_fields.clear_content()

			for field in s3CentralizerProperties_fields:

				item = s3CentralizerProperties_tableWidget.item(field.pos, 0)
				field.append(item.realValue)

			self.currentWellboreInnerStageDataItem['Centralization'][tab]['CentralizerProps'] = copy.deepcopy(s3CentralizerProperties_fields)

			s3CentralizerRunningForce_fields = eval( 'self.s3CentralizerRunningForce_fields_{tab}'.format(tab=tab) )
			s3CentralizerRunningForce_tableWidget = eval( 'self.s3CentralizerRunningForce_tableWidget_{tab}'.format(tab=tab) )
			s3CentralizerRunningForce_fields.clear_content()

			for field in s3CentralizerRunningForce_fields:
				for i in range(s3CentralizerRunningForce_tableWidget.rowCount()):
					item = s3CentralizerRunningForce_tableWidget.item(i,field.pos)
					field.append(item.realValue)

			self.currentWellboreInnerStageDataItem['Centralization'][tab]['RunningForce'] = copy.deepcopy(s3CentralizerRunningForce_fields)

			s3CentralizerLocation_fields = eval( 'self.s3CentralizerLocation_fields_{tab}'.format(tab=tab) )
			s3CentralizerLocation_tableWidget = eval( 'self.s3CentralizerLocation_tableWidget_{tab}'.format(tab=tab) )
			s3CentralizerLocation_fields.clear_content()

			for field in s3CentralizerLocation_fields:
				for i in range(s3CentralizerLocation_tableWidget.rowCount()):
					item = s3CentralizerLocation_tableWidget.item(i,field.pos)
					field.append(item.realValue)

			self.currentWellboreInnerStageDataItem['Centralization'][tab]['Location'] = copy.deepcopy(s3CentralizerLocation_fields)


def update_wellboreOuterStageData(self):

	importlib.reload(cu)

	if self.wellboreOuterStageDataIsUpdatable:

		self.currentWellboreOuterStageDataItem['WellboreProps'] = None
		self.s3WellboreIntervals_fields.clear_content()
		row = self.s3WellboreIntervals_tableWidget.selectedRow

		for field in self.s3WellboreIntervals_fields:

			item = self.s3WellboreIntervals_tableWidget.item(row,field.pos)
			field.append(item.realValue)

		self.currentWellboreOuterStageDataItem['WellboreProps'] = copy.deepcopy(self.s3WellboreIntervals_fields)

		workWellbore_exist = False
		K = list(self.wellboreOuterStageData.keys())
		K.sort()
		for k in K:
			stage = self.wellboreOuterStageData[k]

			if stage['CaliperData']!=None:
				MD = stage['CaliperData']['MD_array']
				ID = stage['CaliperData']['CALmax_array']
			elif stage['WellboreProps']!=None:
				MD = cu.mdl.array( [stage['WellboreProps'].MDtop[0], stage['WellboreProps'].MDbot[0]] )
				ID = cu.mdl.array( [stage['WellboreProps'].DriftID[0], stage['WellboreProps'].DriftID[0]] )
			else:
				del self.wellboreOuterStageData[k]
				MD = cu.mdl.array([])
				ID = cu.mdl.array([])
				
			if workWellbore_exist:
				self.workWellboreMD = cu.mdl.np.hstack( (self.workWellboreMD, MD) )
				self.workWellboreID = cu.mdl.np.hstack( (self.workWellboreID, ID) )
			else:
				self.workWellboreMD = MD
				self.workWellboreID = ID
				workWellbore_exist = True

		print_wellboreOuterStageData(self)
		print('>> MD ID =',len(self.workWellboreMD),len(self.workWellboreID))


@disableByBlock_currentWellboreInnerStageDataItem
def select_innerStageRow_and_prepare_innerStageObjects(self, row):

	self.currentWellboreInnerStageDataItem = None

	cu.select_tableWidgetRow(self.s3PipeCentralizationStage_tableWidget, row)
	self.s3InnerStageToolkit_tabWidget.setEnabled(True)

	clear_wellboreInnerStageToolkit(self)
	if row in self.wellboreInnerStageData:
		self.currentWellboreInnerStageDataItem = self.wellboreInnerStageData[row]
		load_wellboreInnerStageToolkit(self, self.wellboreInnerStageData[row])
	else:
		self.wellboreInnerStageData[row] = mdl.WellboreInnerStageDataItem(row)
		self.currentWellboreInnerStageDataItem = self.wellboreInnerStageData[row]


def select_outerStageRow_and_prepare_outerStageObjects(self, row):

	self.currentWellboreOuterStageDataItem = None
	cu.select_tableWidgetRow(self.s3WellboreIntervals_tableWidget, row)

	if not row in self.wellboreOuterStageData:
		self.wellboreOuterStageData[row] = mdl.WellboreOuterStageDataItem(row)
		
	self.currentWellboreOuterStageDataItem = self.wellboreOuterStageData[row]


@updateByBlock_currentWellboreOuterStageDataItem
def delete_outerStageObjects(self):

	row = cu.clear_tableWidgetRow(self.s3WellboreIntervals_tableWidget)
	del self.wellboreOuterStageData[row]
	#assert( row in self.wellboreOuterStageData )


@disableByBlock_currentWellboreInnerStageDataItem 
def delete_innerStageObjects(self):

	row = cu.clear_tableWidgetRow(self.s3PipeCentralizationStage_tableWidget)
	clear_wellboreInnerStageToolkit(self)
	del self.wellboreInnerStageData[row]


#@updateByBlock_currentWellboreInnerStageDataItem
def clear_wellboreInnerStageToolkit(self):

	cu.clear_tableWidgetContent(self.s3PipeProperties_tableWidget)
	self.s3NoneCentralization_radioButton.setChecked(True)
	self.s3BowSpringCentralizer_radioButton_A.setChecked(True)
	self.s3NoneCentralizer_radioButton_B.setChecked(True)
	self.s3NoneCentralizer_radioButton_C.setChecked(True)
	self.ABC_tabWidget.setEnabled(False)

	for tab in ['A','B','C']:

		cu.clear_tableWidgetContent( eval( 'self.s3CentralizerProperties_tableWidget_{tab}'.format(tab=tab)) )
		cu.clear_tableWidgetContent( eval( 'self.s3CentralizerRunningForce_tableWidget_{tab}'.format(tab=tab)) )
		cu.clear_tableWidgetContent( eval( 'self.s3CentralizerLocation_tableWidget_{tab}'.format(tab=tab)) )


#@updateByBlock_currentWellboreInnerStageDataItem
def load_wellboreInnerStageToolkit(self, dataItem):

	if dataItem['PipeProps']:
		for field in dataItem['PipeProps']:
			
			item = self.s3PipeProperties_tableWidget.item(field.pos,0)
			item.set_text( field[0], field[0].unit )
	
	if dataItem['Centralization']['Mode']:
		
		if dataItem['Centralization']['Mode'] == 'by Spacing':
			self.s3SpecifySpacingCentralization_radioButton.setChecked(True)
			setEnabled_specifySpacingToolkit(self)
		#elif dataItem['Centralization']['Mode'] == 'by Standoff':
		#	self.s3SpecifyStandoffCentralization_radioButton.setChecked(True)
		#	setEnabled_specifyStandoffToolkit(self)
		elif dataItem['Centralization']['Mode'] == 'by Location':
			self.s3SpecifyLocationCentralization_radioButton.setChecked(True)
			setEnabled_specifyLocationToolkit(self)

		for tab in ['A','B','C']:

			if dataItem['Centralization'][tab]['Type']:
				
				if dataItem['Centralization'][tab]['Type'] == 'Bow Spring':
					eval( 'self.s3BowSpringCentralizer_radioButton_{tab}.setChecked(True)'.format(tab=tab) )
					setEnabled_bowSpringToolkit(self, tab)
				elif dataItem['Centralization'][tab]['Type'] == 'Rigid':
					eval( 'self.s3RigidCentralizer_radioButton_{tab}.setChecked(True)'.format(tab=tab) )
					setEnabled_rigidToolkit(self, tab)

				if dataItem['Centralization'][tab]['CentralizerProps']:
					for field in dataItem['Centralization'][tab]['CentralizerProps']:
						item = eval( 'self.s3CentralizerProperties_tableWidget_{tab}.item(field.pos,0)'.format(tab=tab) )
						item.set_text( field[0], field[0].unit )

				if dataItem['Centralization'][tab]['RunningForce']:
					for field in dataItem['Centralization'][tab]['RunningForce']:	
						for i,value in enumerate(field):
							item = eval( 'self.s3CentralizerRunningForce_tableWidget_{tab}.item(i,field.pos)'.format(tab=tab) )
							item.set_text( value, value.unit )

				if dataItem['Centralization'][tab]['Location']:
					for field in dataItem['Centralization'][tab]['Location']:
						for i,value in enumerate(field):
							item = eval( 'self.s3CentralizerLocation_tableWidget_{tab}.item(i,field.pos)'.format(tab=tab) )
							item.set_text( value, value.unit )	

			else: 
				eval( 'self.s3NoneCentralizer_radioButton_{tab}.setChecked(True)'.format(tab=tab) )
				setDisabled_centralizerToolkit(self, tab)
				continue
	else:
		self.s3NoneCentralization_radioButton.setChecked(True)
		self.ABC_tabWidget.setEnabled(False)


@updateByBlock_currentWellboreInnerStageDataItem
def setEnabled_bowSpringToolkit(self, tab):

	s3CentralizerDB_pushButton            = eval( 'self.s3CentralizerDB_pushButton_{tab}'.format(tab=tab) )
	s3CentralizerProperties_tableWidget   = eval( 'self.s3CentralizerProperties_tableWidget_{tab}'.format(tab=tab) )
	s3CentralizerProperties_fields        = eval( 'self.s3CentralizerProperties_fields_{tab}'.format(tab=tab) )
	s3CentralizerRunningForce_tableWidget = eval( 'self.s3CentralizerRunningForce_tableWidget_{tab}'.format(tab=tab) )
	s3CentralizerLocation_tableWidget     = eval( 'self.s3CentralizerLocation_tableWidget_{tab}'.format(tab=tab) )

	cu.clear_tableWidgetContent(s3CentralizerProperties_tableWidget)

	s3CentralizerDB_pushButton.setEnabled(True)
	s3CentralizerProperties_tableWidget.setEnabled(True)
	s3CentralizerRunningForce_tableWidget.setEnabled(True)
	if self.s3SpecifyLocationCentralization_radioButton.isChecked():
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
	s3CentralizerProperties_fields        = eval( 'self.s3CentralizerProperties_fields_{tab}'.format(tab=tab) )
	s3CentralizerRunningForce_tableWidget = eval( 'self.s3CentralizerRunningForce_tableWidget_{tab}'.format(tab=tab) )
	s3CentralizerLocation_tableWidget     = eval( 'self.s3CentralizerLocation_tableWidget_{tab}'.format(tab=tab) )

	cu.clear_tableWidgetContent(s3CentralizerProperties_tableWidget)

	s3CentralizerDB_pushButton.setEnabled(True)
	s3CentralizerProperties_tableWidget.setEnabled(True)
	s3CentralizerRunningForce_tableWidget.setEnabled(False)
	if self.s3SpecifyLocationCentralization_radioButton.isChecked():
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
	s3CentralizerRunningForce_tableWidget  = eval( 'self.s3CentralizerRunningForce_tableWidget_{tab}'.format(tab=tab) )
	s3CentralizerLocation_tableWidget      = eval( 'self.s3CentralizerLocation_tableWidget_{tab}'.format(tab=tab) )

	cu.clear_tableWidgetContent(s3CentralizerProperties_tableWidget)
	s3CentralizerDB_pushButton.setEnabled(False)
	s3CentralizerProperties_tableWidget.setEnabled(False)
	s3CentralizerRunningForce_tableWidget.setEnabled(False)
	s3CentralizerLocation_tableWidget.setEnabled(False)


@updateByBlock_currentWellboreInnerStageDataItem
def setEnabled_specifySpacingToolkit(self):

	self.ABC_tabWidget.setEnabled(True)

	for tab in ['A','B','C']:

		s3CentralizerProperties_tableWidget = eval( 'self.s3CentralizerProperties_tableWidget_{tab}'.format(tab=tab) )
		s3CentralizerProperties_fields      = eval( 'self.s3CentralizerProperties_fields_{tab}'.format(tab=tab) )
		s3CentralizerLocation_tableWidget   = eval( 'self.s3CentralizerLocation_tableWidget_{tab}'.format(tab=tab) )

		s3CentralizerLocation_tableWidget.setEnabled(False)
		field = s3CentralizerProperties_fields.Spacing
		item = s3CentralizerProperties_tableWidget.item(field.pos,0)
		item.set_text()
		item.alt_backgroundColor(False)
		item.alt_flags(False)
		field = s3CentralizerProperties_fields.SO_midSpan
		item = s3CentralizerProperties_tableWidget.item(field.pos,0)
		item.set_text()
		item.alt_backgroundColor()
		item.alt_flags()


@updateByBlock_currentWellboreInnerStageDataItem
def setEnabled_specifyStandoffToolkit(self):

	self.ABC_tabWidget.setEnabled(True)

	for tab in ['A','B','C']:

		s3CentralizerProperties_tableWidget = eval( 'self.s3CentralizerProperties_tableWidget_{tab}'.format(tab=tab) )
		s3CentralizerProperties_fields      = eval( 'self.s3CentralizerProperties_fields_{tab}'.format(tab=tab) )
		s3CentralizerLocation_tableWidget   = eval( 'self.s3CentralizerLocation_tableWidget_{tab}'.format(tab=tab) )

		s3CentralizerLocation_tableWidget.setEnabled(False)
		field = s3CentralizerProperties_fields.Spacing
		item = s3CentralizerProperties_tableWidget.item(field.pos,0)
		item.set_text()
		item.alt_backgroundColor()
		item.alt_flags()
		field = s3CentralizerProperties_fields.SO_midSpan
		item = s3CentralizerProperties_tableWidget.item(field.pos,0)
		item.set_text()
		item.alt_backgroundColor(False)
		item.alt_flags(False)


@updateByBlock_currentWellboreInnerStageDataItem
def setEnabled_specifyLocationToolkit(self):

	self.ABC_tabWidget.setEnabled(True)

	for tab in ['A','B','C']:

		s3CentralizerProperties_tableWidget = eval( 'self.s3CentralizerProperties_tableWidget_{tab}'.format(tab=tab) )
		s3CentralizerProperties_fields      = eval( 'self.s3CentralizerProperties_fields_{tab}'.format(tab=tab) )
		s3CentralizerLocation_tableWidget   = eval( 'self.s3CentralizerLocation_tableWidget_{tab}'.format(tab=tab) )
		s3BowSpringCentralizer_radioButton  = eval( 'self.s3BowSpringCentralizer_radioButton_{tab}'.format(tab=tab) )
		s3RigidCentralizer_radioButton      = eval( 'self.s3RigidCentralizer_radioButton_{tab}'.format(tab=tab) )

		if s3BowSpringCentralizer_radioButton.isChecked() or s3RigidCentralizer_radioButton.isChecked():
			s3CentralizerLocation_tableWidget.setEnabled(True)

		field = s3CentralizerProperties_fields.Spacing
		item = s3CentralizerProperties_tableWidget.item(field.pos,0)
		item.set_text()
		item.alt_backgroundColor()
		item.alt_flags()
		field = s3CentralizerProperties_fields.SO_midSpan
		item = s3CentralizerProperties_tableWidget.item(field.pos,0)
		item.set_text()
		item.alt_backgroundColor()
		item.alt_flags()


@updateByBlock_currentWellboreInnerStageDataItem
def open_TDB_dialog_for_innerStages(self):
	
	dialog = QtGui.QDialog(self.s3PipeProperties_tableWidget)
	TDB = Main_TubularDatabase(dialog)
	if 'fields' not in dir(TDB): return
	self.currentWellboreInnerStageDataItem['PipeBase'] = TDB.fields

	for field in self.s3PipeProperties_fields:

		item = self.s3PipeProperties_tableWidget.item(field.pos,0)

		if field.abbreviation in TDB.data:
			value = TDB.data[field.abbreviation]
			item.set_text( value, value.unit )
		else:
			item.set_text()
			self.s3PipeProperties_tableWidget.editItem(item)


@updateByBlock_currentWellboreInnerStageDataItem
def open_CDB_dialog(self, tab):
	
	s3BowSpringCentralizer_radioButton    = eval( 'self.s3BowSpringCentralizer_radioButton_{tab}'.format(tab=tab) )
	s3RigidCentralizer_radioButton        = eval( 'self.s3RigidCentralizer_radioButton_{tab}'.format(tab=tab) )
	s3CentralizerProperties_tableWidget   = eval( 'self.s3CentralizerProperties_tableWidget_{tab}'.format(tab=tab) )
	s3CentralizerProperties_fields        = eval( 'self.s3CentralizerProperties_fields_{tab}'.format(tab=tab) )
	s3CentralizerRunningForce_tableWidget = eval( 'self.s3CentralizerRunningForce_tableWidget_{tab}'.format(tab=tab) )	
	s3CentralizerRunningForce_fields      = eval( 'self.s3CentralizerRunningForce_fields_{tab}'.format(tab=tab) )

	dialog = QtGui.QDialog(self.ABC_tabWidget)
	
	if s3BowSpringCentralizer_radioButton.isChecked():
		CDB = Main_CentralizerDatabase(dialog, 'Bow Spring' )
	elif s3RigidCentralizer_radioButton.isChecked():
		CDB = Main_CentralizerDatabase(dialog, 'Rigid' )
	
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

	if s3BowSpringCentralizer_radioButton.isChecked():

		for field in s3CentralizerRunningForce_fields:

			item = s3CentralizerRunningForce_tableWidget.item(0,field.pos)

			if field.abbreviation in CDB.data:
				value = CDB.data[field.abbreviation]
				if value:
					item.set_text( value, value.unit )
				else:
					value = CDB.data[field.substitute]
					item.set_text( value, value.unit )
			else:
				break


@updateByBlock_currentWellboreOuterStageDataItem
def open_caliper_dialog(self):

	dialog = QtGui.QDialog(self.s3WellboreIntervals_tableWidget)
	CI = Main_CaliperImport(dialog)
	if 'data' not in dir(CI): return

	row = self.s3WellboreIntervals_tableWidget.selectedRow
	self.currentWellboreOuterStageDataItem['CaliperData'] = {	'CAL_fields': CI.ciCALData_fields, 
																'MD_field': CI.ciLASData_fields.MD,
																'CALmax_array': CI.CALID_max,
																'MD_array': CI.MD 
															}
	for field in self.s3WellboreIntervals_fields:

		item = self.s3WellboreIntervals_tableWidget.item(row, field.pos)

		if field.abbreviation in CI.data:
			value = CI.data[field.abbreviation]
			item.set_text( value, value.unit )
		else:
			item.set_text()
			item.alt_backgroundColor()
			item.alt_flags()
			self.s3WellboreIntervals_tableWidget.editItem(item)


@updateByBlock_currentWellboreOuterStageDataItem
def open_TDB_dialog_for_outerStages(self):
	
	dialog = QtGui.QDialog(self.s3WellboreIntervals_tableWidget)
	TDB = Main_TubularDatabase(dialog)
	row = self.s3WellboreIntervals_tableWidget.selectedRow
	self.currentWellboreOuterStageDataItem['PipeBase'] = TDB.fields

	for field in self.s3WellboreIntervals_fields:

		item = self.s3WellboreIntervals_tableWidget.item(row, field.pos)

		if field.abbreviation in TDB.data:
			value = TDB.data[field.abbreviation]
			item.set_text( value, value.unit )
		else:
			item.set_text()
			item.alt_backgroundColor()
			item.alt_flags()
			self.s3WellboreIntervals_tableWidget.editItem(item)


def set_row_as_free(self, description):

	row = self.s3WellboreIntervals_tableWidget.selectedRow
	self.s3WellboreIntervals_tableWidget.item(row, 0).set_text( description )
	
	for column in [4,3,2,1]:
		item = self.s3WellboreIntervals_tableWidget.item(row, column)
		item.set_text()
		item.alt_backgroundColor()
		item.alt_flags()
	
	self.s3WellboreIntervals_tableWidget.editItem(item)


def adjust_Length_and_MD(self, item):

	cu.update_fieldItem(item)

	if self._PipeCentralizationStageAdjusting_isEnabled:

		self._PipeCentralizationStageAdjusting_isEnabled = False	
		
		row = self.s3PipeCentralizationStage_tableWidget.selectedRow

		if item.field.pos == self.s3PipeCentralizationStage_fields.L.pos:
			self.s3PipeCentralizationStage_tableWidget.item(row, self.s3PipeCentralizationStage_fields.MD.pos).set_text()

		elif item.field.pos == self.s3PipeCentralizationStage_fields.MD.pos:
			self.s3PipeCentralizationStage_tableWidget.item(row, self.s3PipeCentralizationStage_fields.L.pos).set_text()
		
		try:
			lastMD = min(self.workWellboreMD)
		except ValueError:
			msg = "Any top MD has been assigned yet in Wellbore intervals. Can not proceed."
			QtGui.QMessageBox.critical(self.s3PipeCentralizationStage_tableWidget, 'Error', msg)
			self._PipeCentralizationStageAdjusting_isEnabled = True
			return

		cumLT  = 0.0

		for i in range(self.s3PipeCentralizationStage_tableWidget.rowCount()):
			
			LTitem = self.s3PipeCentralizationStage_tableWidget.item(i, self.s3PipeCentralizationStage_fields.L.pos)
			LT = LTitem.realValue
			MDitem = self.s3PipeCentralizationStage_tableWidget.item(i, self.s3PipeCentralizationStage_fields.MD.pos)
			MD = MDitem.realValue

			if LT:
				lastMD += LT
				cumLT += LT
				MDitem.set_text( lastMD )
				LTitem.set_text( LT )
				self.wellboreInnerStageData[i]['MD'] = MDitem.realValue
				self.wellboreInnerStageData[i]['Length'] = LTitem.realValue
			elif MD:
				LT = MD -lastMD
				cumLT += LT
				lastMD = MD
				MDitem.set_text( lastMD )
				LTitem.set_text( LT )
				self.wellboreInnerStageData[i]['MD'] = MDitem.realValue
				self.wellboreInnerStageData[i]['Length'] = LTitem.realValue
		
		self._PipeCentralizationStageAdjusting_isEnabled = True
		print_wellboreInnerStageData(self)


def adjust_MD_to_wellboreDeep(self):

	try:
		deepestMD = max(self.workWellboreMD)
	except ValueError:
		msg = "Any bottom MD has been assigned yet in Wellbore intervals. Can not proceed."
		QtGui.QMessageBox.critical(self.s3PipeCentralizationStage_tableWidget, 'Error', msg)
		self._PipeCentralizationStageAdjusting_isEnabled = True
		return

	row  = self.s3PipeCentralizationStage_tableWidget.selectedRow
	item = self.s3PipeCentralizationStage_tableWidget.item(row, self.s3PipeCentralizationStage_fields.MD.pos)
	item.set_text( deepestMD )


def adjust_Wt(self):

	OD = self.s3PipeProperties_tableWidget.item(self.s3PipeProperties_fields.OD.pos,0).realValue
	ID = self.s3PipeProperties_tableWidget.item(self.s3PipeProperties_fields.ID.pos,0).realValue
	Wt = self.s3PipeProperties_tableWidget.item(self.s3PipeProperties_fields.PipeW.pos,0).realValue
	Wt = mdl.adjust_Wt( OD, ID, Wt )
	self.s3PipeProperties_tableWidget.item(self.s3PipeProperties_fields.PipeW.pos,0).set_text(Wt)


def adjust_ID(self):

	OD = self.s3PipeProperties_tableWidget.item(self.s3PipeProperties_fields.OD.pos,0).realValue
	ID = self.s3PipeProperties_tableWidget.item(self.s3PipeProperties_fields.ID.pos,0).realValue
	Wt = self.s3PipeProperties_tableWidget.item(self.s3PipeProperties_fields.PipeW.pos,0).realValue
	ID = mdl.adjust_ID( OD, ID, Wt )
	self.s3PipeProperties_tableWidget.item(self.s3PipeProperties_fields.ID.pos,0).set_text(ID)




def print_wellboreInnerStageData(self):

	print('-----------------------------------------')
	K = list(self.wellboreInnerStageData.keys())
	K.sort()
	for k in K:
		print('\n',self.wellboreInnerStageData[k],'\n')
	print('-----------------------------------------\n')
	pass

def print_wellboreOuterStageData(self):
	
	print('vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv')
	K = list(self.wellboreOuterStageData.keys())
	K.sort()
	for k in K:
		print('\n',self.wellboreOuterStageData[k],'\n')
	print('vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv\n')
	pass