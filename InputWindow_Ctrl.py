from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from InputWindow_Vst import Ui_InputWindow
from UnitSettings_Ctrl import Main_UnitSettings
from OneSpanAnalysis_Ctrl import Main_OneSpanAnalysis
from OutputWindow_Ctrl import Main_OutputWindow
from DiagramWindow_Ctrl import Main_DiagramWindow
from GraphWindow_Ctrl import Main_GraphWindow
import InputWindow_Mdl as mdl
import CtrlUtilities as cu
#import MdlUtilities as mu
import SurveyFunctions as sf
import WellboreFunctions as wf
import TDSFunctions as tdsf
import importlib
import sys, copy
import re, inspect


class Main_InputWindow(Ui_InputWindow):

	def __init__(self, window):
		Ui_InputWindow.__init__(self)
		self.setupUi(window)

		self.v1WorkingDirectory = ''
		self.v1UnitSystem = 'cu'
		self.v3WellboreInnerStageData = {}
		self.v3WellboreOuterStageData = {}
		self.v3WorkWellboreMD = []
		self.v3WorkWellboreID = []

		self.wellboreOuterStageDataIsUpdatable = True
		self.wellboreInnerStageDataIsUpdatable = True
		self.wellboreInnerStageDataIsEnabled   = True
		self._PipeCentralizationStageAdjusting_isEnabled = True
		self.v3CentralizationChanged_flag   = False
		self.v3CentralizationProcessed_flag = False

		self.v3SOs_fields = mdl.get_v3SOs_fields()

		self.__init__s1Info_tableWidget()
		self.__init__s2DataSurvey_tableWidget()
		self.__init__s2SurveyTortuosity_tableWidget()
		self.__init__s2KOP_tableWidget()
		self.__init__s2TortuosityInterval_tableWidget()
		self.__init__s3WellboreOuterStages_tableWidget()
		self.__init__s3WellboreInnerStages_tableWidget()
		self.__init__s3PipeProperties_tableWidget()
		self.__init__s3CentralizerProperties_tableWidgets()
		self.__init__s3CentralizerLocation_tableWidgets()
		self.__init__s4Settings_tableWidget()
		self.__init__s4TorqueDragSideforce_tableWidget()

		self.Open_action.triggered.connect(self.load_file)
		self.Save_action.triggered.connect(self.save_file)
		self.SchematicDiagram_action.triggered.connect(self.open_schematicDiagramDialog)
		self.OneSpanAnalysis_action.triggered.connect(self.open_oneSpanAnalysisDialog)
		self.MakeReport_action.triggered.connect(self.save_src_and_make_report)
		self.About_action.triggered.connect(self.about)

		self.s1SelectDirectory_pushButton.clicked.connect(self.open_selectWorkingDirectoryDialog)
		self.s1UnitSetting_pushButton.clicked.connect(self.open_unitSettingsDialog)
		
		set_workUnits_as_us = lambda: self.set_workUnits_as('us')
		set_workUnits_as_si = lambda: self.set_workUnits_as('si')
		set_workUnits_as_cu = lambda: self.set_workUnits_as('cu')
		self.s1USOF_radioButton.clicked.connect(set_workUnits_as_us)
		self.s1Metric_radioButton.clicked.connect(set_workUnits_as_si)
		self.s1Customized_radioButton.clicked.connect(set_workUnits_as_cu)

		set_survey_to_table = lambda: sf.set_survey_to_table(self)
		self.s2Import_pushButton.clicked.connect(set_survey_to_table)
		remove_all = lambda: sf.remove_all(self)
		self.s2Remove_pushButton.clicked.connect(remove_all)
		set_survey_outcomes = lambda: sf.set_survey_outcomes(self)
		self.s2Calculate_pushButton.clicked.connect(set_survey_outcomes)
		activate_SurveyTortuosity = lambda: self.s2SurveyTortuosity_groupBox.setDisabled( self.s2SurveyTortuosity_groupBox.isEnabled() )
		self.s2SurveyTortuosity_checkBox.clicked.connect(activate_SurveyTortuosity)
		
		#open_TDB_dialog_for_innerStages = lambda: wf.open_TDB_dialog_for_innerStages(self)
		#self.s3PipeDB_pushButton.clicked.connect(open_TDB_dialog_for_innerStages)
		
		calculate_theForces = lambda: mdl.calculate_theForces(self)
		self.s3UpdateInnerStages_pushButton.clicked.connect(calculate_theForces)
		self.s3UpdateInnerStages_pushButton.setEnabled(False)

		adjust_Wt = lambda: wf.adjust_Wt(self)
		adjust_ID = lambda: wf.adjust_ID(self)
		self.s3ODID_pushButton.clicked.connect(adjust_Wt)
		self.s3ODWt_pushButton.clicked.connect(adjust_ID)

		open_LS_dialog = lambda: wf.open_LS_dialog(self)
		self.s3ManageLocations_pushButton.clicked.connect(open_LS_dialog)

		self.s3Plot3DSO_pushButton.clicked.connect(self.open_graphWindow_dialog)

		valueChangedAction = lambda v: wf.valueChangedAction(self, v)
		self.s3CentralizationPattern_spinBox.valueChanged.connect(valueChangedAction)
		self.s3CentralizationOffset_spinBox.valueChanged.connect(valueChangedAction)

		open_CDB_dialog_A = lambda: wf.open_CDB_dialog(self, 'A')
		open_CDB_dialog_B = lambda: wf.open_CDB_dialog(self, 'B')
		open_CDB_dialog_C = lambda: wf.open_CDB_dialog(self, 'C')
		self.s3CentralizerDB_pushButton_A.clicked.connect(open_CDB_dialog_A)
		self.s3CentralizerDB_pushButton_B.clicked.connect(open_CDB_dialog_B)
		self.s3CentralizerDB_pushButton_C.clicked.connect(open_CDB_dialog_C)

		#setEnabled_specifySpacingToolkit = lambda: wf.setEnabled_specifySpacingToolkit(self)
		#setEnabled_specifyStandoffToolkit = lambda: wf.setEnabled_specifyStandoffToolkit(self)
		#setEnabled_specifyLocationToolkit = lambda: wf.setEnabled_specifyLocationToolkit(self)
		#setDisabled_ABC_tabWidget = lambda: self.ABC_tabWidget.setEnabled(False)
		#setDisabled_ABC_tabWidget()
		#self.s3SpecifySpacingCentralization_radioButton.toggled.connect(setEnabled_specifySpacingToolkit)
		#self.s3SpecifyStandoffCentralization_radioButton.clicked.connect(setEnabled_specifyStandoffToolkit)
		#self.s3SpecifyLocationCentralization_radioButton.toggled.connect(setEnabled_specifyLocationToolkit)
		#self.s3NoneCentralization_radioButton.clicked.connect(setDisabled_ABC_tabWidget)

		setEnabled_specifySpacingToolkit = lambda: wf.setEnabled_specifySpacingToolkit(self)
		self.s3EnableCentralization_checkBox.toggled.connect(setEnabled_specifySpacingToolkit)

		setEnabled_bowSpringToolkit_A = lambda: wf.setEnabled_bowSpringToolkit(self, 'A')
		setEnabled_rigidToolkit_A = lambda: wf.setEnabled_rigidToolkit(self, 'A')
		self.s3BowSpringCentralizer_radioButton_A.clicked.connect(setEnabled_bowSpringToolkit_A)
		self.s3ResinCentralizer_radioButton_A.clicked.connect(setEnabled_rigidToolkit_A)

		setEnabled_bowSpringToolkit_B = lambda: wf.setEnabled_bowSpringToolkit(self, 'B')
		setEnabled_rigidToolkit_B = lambda: wf.setEnabled_rigidToolkit(self, 'B')
		setDisabled_centralizerToolkit_B = lambda: wf.setDisabled_centralizerToolkit(self, 'B')
		self.s3BowSpringCentralizer_radioButton_B.clicked.connect(setEnabled_bowSpringToolkit_B)
		self.s3ResinCentralizer_radioButton_B.clicked.connect(setEnabled_rigidToolkit_B)
		self.s3NoneCentralizer_radioButton_B.clicked.connect(setDisabled_centralizerToolkit_B)

		setEnabled_bowSpringToolkit_C = lambda: wf.setEnabled_bowSpringToolkit(self, 'C')
		setEnabled_rigidToolkit_C = lambda: wf.setEnabled_rigidToolkit(self, 'C')
		setDisabled_centralizerToolkit_C = lambda: wf.setDisabled_centralizerToolkit(self, 'C')
		self.s3BowSpringCentralizer_radioButton_C.clicked.connect(setEnabled_bowSpringToolkit_C)
		self.s3ResinCentralizer_radioButton_C.clicked.connect(setEnabled_rigidToolkit_C)
		self.s3NoneCentralizer_radioButton_C.clicked.connect(setDisabled_centralizerToolkit_C)

		calculateAndDraw_torque_drag_sideforce = lambda: tdsf.calculateAndDraw_torque_drag_sideforce(self)
		self.s4Calculate_pushButton.clicked.connect(calculateAndDraw_torque_drag_sideforce)

		# TEST
		#self.load_file()


	def save_file(self):

		print('---------------------------------------------------------')
		filename = QFileDialog.getSaveFileName( self.s1Info_tableWidget, 'Save File ...', self.v1WorkingDirectory+'/untitled.csf', 'Central-Soft File (*.csf)' )[0]
		
		OBJ = {}
		for attrname in dir(self):

			if not re.match('v[1234]+',attrname):
				continue

			OBJ[attrname] = getattr(self,attrname)

		OBJ['v2SurveyTortuosity'] = self.s2SurveyTortuosity_checkBox.isChecked()

		with open(filename,'wb') as File:
			mdl.save_obj( OBJ, File )

		print(OBJ)
		print(filename,' saved!')
		print('---------------------------------------------------------')
		

	def load_file(self):

		filename = QFileDialog.getOpenFileName( self.s1Info_tableWidget, 'Open File ...', self.v1WorkingDirectory, 'Central-Soft File (*.csf)' )[0]
		#filename = 'C:/Users/arcad/Documents/__WORKS__/AZTECATROL/CENTRAL-SOFTWARE/CentralSoftware/tmp/test1.csf'

		with open(filename,'rb') as File:
			OBJ = mdl.load_obj( File )

		print('=========================================================')
		print(OBJ)

		"""
		if OBJ['v1UnitSystem'] == 'us':
			self.s1USOF_radioButton.click()
		elif OBJ['v1UnitSystem'] == 'si':
			self.s1Metric_radioButton.click()
		elif OBJ['v1UnitSystem'] == 'cu':
			self.s1Customized_radioButton.click()
		"""

		if OBJ['v2SurveyTortuosity']:
			self.s2SurveyTortuosity_checkBox.click()

		for attrname, attr in OBJ.items():
			setattr( self, attrname, attr )
			print(attrname)

		self.load_fields_to_vTableWidget( self.v1Info_fields, self.s1Info_tableWidget )
		self.load_fields_to_hTableWidget( self.v2DataSurvey_fields, self.s2DataSurvey_tableWidget )
		self.load_fields_to_vTableWidget( self.v2KOP_fields, self.s2KOP_tableWidget)
		self.load_fields_to_hTableWidget( self.v2SurveyTortuosity_fields[:-1], self.s2SurveyTortuosity_tableWidget )
		self.load_fields_to_vTableWidget( self.v2TortuosityInterval_fields, self.s2TortuosityInterval_tableWidget )
		self.s2Calculate_pushButton.click()
		self.load_wellboreOuterStages_tableWidget()
		self.load_wellboreInnerStages_tableWidget()
		self.s3UpdateInnerStages_pushButton.setEnabled(True)
		self.s3UpdateInnerStages_pushButton.click()

		"""
		self.load_fields_to_vTableWidget( self.v3PipeProperties_fields, self.s3PipeProperties_tableWidget )
		self.load_fields_to_hTableWidget( self.v3CentralizerLocation_fields_A, self.s3CentralizerLocation_tableWidget_A )
		self.load_fields_to_hTableWidget( self.v3CentralizerLocation_fields_B, self.s3CentralizerLocation_tableWidget_B )
		self.load_fields_to_hTableWidget( self.v3CentralizerLocation_fields_C, self.s3CentralizerLocation_tableWidget_C )
		self.load_fields_to_vTableWidget( self.v3CentralizerProperties_fields_A, self.s3CentralizerProperties_tableWidget_A )
		self.load_fields_to_vTableWidget( self.v3CentralizerProperties_fields_B, self.s3CentralizerProperties_tableWidget_B )
		self.load_fields_to_vTableWidget( self.v3CentralizerProperties_fields_C, self.s3CentralizerProperties_tableWidget_C )		
		"""

		self.load_fields_to_vTableWidget( self.v4Settings_fields[:5], self.s4Settings_tableWidget )
		self.load_fields_to_hTableWidget( self.v4TorqueDragForces_fields[:7], self.s4TorqueDragSideforce_tableWidget )
		print(filename,' loaded!')
		print('=========================================================')


	def load_fields_to_hTableWidget( self, fields, tableWidget ):

		for i in range(len(fields[0])):

			#item = cu.TableWidgetFieldItem( self.v1Info_fields[0], False )
			#tableWidget.setItem(0, 0, item)
			
			tableWidget.cellPressed.emit( i, 0 )
			for field in fields:
				item = tableWidget.item(i, field.pos)
				item.set_text( field[i] )


	def load_fields_to_vTableWidget( self, fields, tableWidget ):

		for i in range(len(fields[0])):
			
			tableWidget.cellPressed.emit( 0, i )
			for field in fields:
				item = tableWidget.item(field.pos, i)
				item.set_text( field[i] )


	def load_wellboreOuterStages_tableWidget( self ):

		for i,stage in self.v3WellboreOuterStageData.items():
			
			if stage['WellboreProps'] == None:
				continue

			else:
				self.wellboreOuterStageDataIsUpdatable = False
				self.s3WellboreOuterStages_tableWidget.cellPressed.emit( i, 0 )
				
				for field in stage['WellboreProps']:
					item = self.s3WellboreOuterStages_tableWidget.item(i, field.pos)
					item.set_text( field[0] )
					if not field._altFg_:
						item.alt_backgroundColor()
						item.alt_flags()

				self.wellboreOuterStageDataIsUpdatable = True

		#print(self.v3WellboreOuterStageData)


	def load_wellboreInnerStages_tableWidget( self ):

		for i,stage in self.v3WellboreInnerStageData.items():
			
			if stage['PipeBase'] == None:
				continue

			else:
				self.wellboreInnerStageDataIsUpdatable = False
				self.s3WellboreInnerStages_tableWidget.cellPressed.emit( i, 0 )
				
				self.s3WellboreInnerStages_tableWidget.item(i, 0).set_text( stage['Desc'] )
				self.s3WellboreInnerStages_tableWidget.item(i, 1).set_text( stage['MDtop'] )
				self.s3WellboreInnerStages_tableWidget.item(i, 2).set_text( stage['MDbot'] )

				self.wellboreInnerStageDataIsUpdatable = True

		#print(self.v3WellboreInnerStageData)


	def about(self):

		importlib.reload(mdl)
		importlib.reload(cu)
		importlib.reload(wf)
		importlib.reload(sf)
		importlib.reload(tdsf)

		print('=========================================================')
		
		for attrname in dir(self):

			#if not re.match('v[1234]+',attrname):
			#	continue

			attr = getattr(self,attrname)
			print(type(attr),attrname)

			"""
			for subattrname in dir(attr):

				subattr = getattr(attr,subattrname)
				flag = inspect.ismethod(subattr) or inspect.isbuiltin(subattr) or inspect.isroutine(subattr) or inspect.isfunction(subattr) or inspect.ismethoddescriptor(subattr)

				if flag or re.match('__[\w]+__',subattrname):
					continue
				else:
					print('>>  ',type(subattr),' > ',subattrname)
			
			with open('objfiles/'+attrname+'.obj','wb') as File:
				mdl.save_obj( attr, File )
			print(attrname,' saved!')

			print('---------------------------------------------------------')
			"""		

		print('=========================================================')


	@cu.waiting_effects	
	def set_workUnits_as(self, unitSystem):
		
		self.v1UnitSystem = unitSystem
		mdl.set_workUnits_as(unitSystem)
		self.v3WellboreInnerStageData = {}
		self.v3WellboreOuterStageData = {}

		self.wellboreOuterStageDataIsUpdatable = False
		self.wellboreInnerStageDataIsUpdatable = False
		self.wellboreInnerStageDataIsEnabled = False
		self._PipeCentralizationStageAdjusting_isEnabled = False

		self.setup_s2DataSurvey_tableWidget()
		self.setup_s2KOP_tableWidget()
		self.setup_s2SurveyTortuosity_tableWidget()
		self.setup_s2TortuosityInterval_tableWidget()
		self.setup_s3WellboreOuterStages_tableWidget()
		self.setup_s3WellboreInnerStages_tableWidget()
		#self.setup_s3CentralizerSpacing_tableWidget()
		self.setup_s3PipeProperties_tableWidget()
		wf.setup_s3CentralizerProperties_tableWidget(self,'A')
		wf.setup_s3CentralizerProperties_tableWidget(self,'B')
		wf.setup_s3CentralizerProperties_tableWidget(self,'C')
		#wf.setup_s3CentralizerRunningForce_tableWidget(self,'A')
		#wf.setup_s3CentralizerRunningForce_tableWidget(self,'B')
		#wf.setup_s3CentralizerRunningForce_tableWidget(self,'C')
		wf.setup_s3CentralizerLocation_tableWidget(self,'A')
		wf.setup_s3CentralizerLocation_tableWidget(self,'B')
		wf.setup_s3CentralizerLocation_tableWidget(self,'C')
		self.setup_s4Settings_tableWidget()
		self.setup_s4TorqueDragSideforce_tableWidget()

		self.wellboreOuterStageDataIsUpdatable = True
		self.wellboreInnerStageDataIsUpdatable = True
		self.wellboreInnerStageDataIsEnabled = True
		self._PipeCentralizationStageAdjusting_isEnabled = True


	def open_selectWorkingDirectoryDialog(self):
		
		self.v1WorkingDirectory = QFileDialog.getExistingDirectory( self.s1Info_tableWidget, 'Select the working directory', 'C:\\' )
		items = re.split(r'\\',self.v1WorkingDirectory)
		self.v1WorkingDirectory = '/'.join(items)
		print(self.v1WorkingDirectory)
		item = self.s1Info_tableWidget.item( 5,0 )
		item.setText( self.v1WorkingDirectory )


	def open_unitSettingsDialog(self):
		dialog = QDialog(self.s1UnitSetting_pushButton)
		Main_UnitSettings(dialog)
		self.s1Customized_radioButton.click()
		del dialog
		

	def open_oneSpanAnalysisDialog(self):
		dialog = QDialog(self.iw_toolBar)
		Main_OneSpanAnalysis(dialog)
		del dialog


	def open_schematicDiagramDialog(self):
		dialog = QDialog(self.iw_toolBar)
		DW = Main_DiagramWindow(dialog, self)
		DW.dwWellboreSchematic_graphicsView.figure.savefig( self.parent.v1WorkingDirectory+"WellboreSchematic.png", dpi=300 )
		del DW
		del dialog


	def open_graphWindow_dialog(self):
		dialog = QDialog(self.s3Plot3DSO_pushButton)
		GW = Main_GraphWindow(dialog, self)
		GW.gwColoredWellbore_graphicsView.figure.savefig( self.parent.v1WorkingDirectory+"WellboreCentralization3D.png", dpi=300 )
		del GW
		del dialog


	def save_src_and_make_report(self):
		

		cu.savetable( 	self.s1Info_tableWidget,
						self.v1Info_fields,
						self.v1WorkingDirectory+"/GeneralInformation.csv",
						orientation='v' )

		cu.savetable( 	self.s2DataSurvey_tableWidget,
						self.v2DataSurvey_fields,
						self.v1WorkingDirectory+"/DataSurvey.csv" )

		cu.savetable( 	self.s2SurveyTortuosity_tableWidget,
						self.v2SurveyTortuosity_fields,
						self.v1WorkingDirectory+"/SurveyTortuosity.csv" )
		
		self.s2SectionView_graphicsView.figure.savefig( self.v1WorkingDirectory+"/SectionView.png", dpi=300 )

		self.s2PlanView_graphicsView.figure.savefig( self.v1WorkingDirectory+"/PlanView.png", dpi=300 )

		self.s2TriDView_graphicsView.figure.savefig( self.v1WorkingDirectory+"/TriDView.png", dpi=300 )

		self.s2Dogleg_graphicsView.figure.savefig( self.v1WorkingDirectory+"/Dogleg.png", dpi=300 )

		cu.savetable( 	self.s3WellboreOuterStages_tableWidget,
						self.v3WellboreOuterStages_fields,
						self.v1WorkingDirectory+"/WellboreOuterStages.csv" )

		cu.savetable( 	self.s3WellboreInnerStages_tableWidget,
						self.v3WellboreInnerStages_fields,
						self.v1WorkingDirectory+"/WellboreInnerStages.csv" )

		cu.savetable( 	self.s4Settings_tableWidget,
						self.s4Settings_tableWidget,
						self.v1WorkingDirectory+"/TorqueAndDragSettings.csv",
						orientation='v' )

		self.s4Drag_graphicsView.figure.savefig( self.v1WorkingDirectory+"/Drag.png", dpi=300 )
		self.s4Torque_graphicsView.figure.savefig( self.v1WorkingDirectory+"/Torque.png", dpi=300 )
		self.s4Sideforce_graphicsView.figure.savefig( self.v1WorkingDirectory+"/SideForce.png", dpi=300 )
		self.s4HookLoad_graphicsView.figure.savefig( self.v1WorkingDirectory+"/HookLoad.png", dpi=300 )

	
	def __init__s1Info_tableWidget(self):

		self.s1Info_tableWidget.parent = self
		self.s1Info_tableWidget.setContextMenuPolicy(Qt.ActionsContextMenu)
		
		C = cu.CopySelectedCells_action(self.s1Info_tableWidget)
		self.s1Info_tableWidget.addAction(C)
		
		V = cu.PasteToCells_action(self.s1Info_tableWidget)
		self.s1Info_tableWidget.addAction(V)
		
		self.v1Info_fields = mdl.get_v1Info_fields()
		item = cu.TableWidgetFieldItem( self.v1Info_fields[0], False )
		self.s1Info_tableWidget.setItem(0, 0, item)
		item = cu.TableWidgetFieldItem( self.v1Info_fields[1], False )
		self.s1Info_tableWidget.setItem(1, 0, item)
		item = cu.TableWidgetFieldItem( self.v1Info_fields[2], False )
		self.s1Info_tableWidget.setItem(2, 0, item)
		item = cu.TableWidgetFieldItem( self.v1Info_fields[3], False )
		self.s1Info_tableWidget.setItem(3, 0, item)
		item = cu.TableWidgetFieldItem( self.v1Info_fields[4], False )
		self.s1Info_tableWidget.setItem(4, 0, item)
		item = cu.TableWidgetFieldItem( self.v1Info_fields[5], False )
		self.s1Info_tableWidget.setItem(5, 0, item)

		select_row = lambda r,c : cu.select_tableWidgetRow(self.s1Info_tableWidget,r)
		def update_fieldItem( item ):
			value = cu.mdl.physicalValue( item.text(), '' )
			call = lambda : item.field.put( 0, value )
			cu.update_fieldItem( item, call )
		self.s1Info_tableWidget.cellPressed.connect(select_row)
		self.s1Info_tableWidget.itemChanged.connect(update_fieldItem)	


	def __init__s2DataSurvey_tableWidget(self):
		
		self.s2DataSurvey_tableWidget.parent = self
		self.s2DataSurvey_tableWidget.setContextMenuPolicy(Qt.ActionsContextMenu)
		
		C = cu.CopySelectedCells_action(self.s2DataSurvey_tableWidget)
		self.s2DataSurvey_tableWidget.addAction(C)
		
		V = cu.PasteToCells_action(self.s2DataSurvey_tableWidget)
		self.s2DataSurvey_tableWidget.addAction(V)

		insert_row = lambda: cu.insert_tableWidgetRow(self.s2DataSurvey_tableWidget, self.v2DataSurvey_fields)
		I = cu.FunctionToWidget_action(self.s2DataSurvey_tableWidget, insert_row, "Insert above row")
		self.s2DataSurvey_tableWidget.addAction(I)

		remove_row = lambda: cu.remove_tableWidgetRow(self.s2DataSurvey_tableWidget)
		R = cu.FunctionToWidget_action(self.s2DataSurvey_tableWidget, remove_row, "Remove row")
		self.s2DataSurvey_tableWidget.addAction(R)

		clear_row = lambda: cu.clear_tableWidgetRow(self.s2DataSurvey_tableWidget)
		D = cu.FunctionToWidget_action(self.s2DataSurvey_tableWidget, clear_row, "Clear row", 'Del')
		self.s2DataSurvey_tableWidget.addAction(D)
		
		self.setup_s2DataSurvey_tableWidget()

		select_row = lambda r,c : cu.select_tableWidgetRow(self.s2DataSurvey_tableWidget,r)
		self.s2DataSurvey_tableWidget.cellPressed.connect(select_row)
		self.s2DataSurvey_tableWidget.itemChanged.connect(cu.update_fieldItem)

		self.s2DataSurvey_tableWidget.resizeColumnsToContents()


	def setup_s2DataSurvey_tableWidget(self):

		self.v2DataSurvey_fields = mdl.get_v2DataSurvey_fields()
		self.v3Forces_fields     = mdl.get_v3Forces_fields()
		for field in self.v2DataSurvey_fields:
			item = self.s2DataSurvey_tableWidget.horizontalHeaderItem( field.pos )
			item.setText( field.headerName )
			
			for i in range(self.s2DataSurvey_tableWidget.rowCount()):
				item = cu.TableWidgetFieldItem( field, i%2==0 )
				self.s2DataSurvey_tableWidget.setItem(i, field.pos, item)


	def __init__s2KOP_tableWidget(self):
		
		self.s2KOP_tableWidget.parent = self
		self.s2KOP_tableWidget.setContextMenuPolicy(Qt.ActionsContextMenu)
		
		C = cu.CopySelectedCells_action(self.s2KOP_tableWidget)
		self.s2KOP_tableWidget.addAction(C)
		
		V = cu.PasteToCells_action(self.s2KOP_tableWidget)
		self.s2KOP_tableWidget.addAction(V)
		
		self.setup_s2KOP_tableWidget()

		select_row = lambda r,c : cu.select_tableWidgetRow(self.s2KOP_tableWidget,r)
		self.s2KOP_tableWidget.cellPressed.connect(select_row)
		self.s2KOP_tableWidget.itemChanged.connect(cu.update_fieldItem)


	def setup_s2KOP_tableWidget(self):

		self.v2KOP_fields = mdl.get_v2KOP_fields()
		item = self.s2KOP_tableWidget.verticalHeaderItem( 0 )
		item.setText( self.v2KOP_fields[0].headerName )
		item = cu.TableWidgetFieldItem( self.v2KOP_fields[0], True )
		self.s2KOP_tableWidget.setItem(0, 0, item)


	def __init__s2SurveyTortuosity_tableWidget(self):
		
		self.s2SurveyTortuosity_tableWidget.parent = self
		self.s2SurveyTortuosity_tableWidget.setContextMenuPolicy(Qt.ActionsContextMenu)
		
		C = cu.CopySelectedCells_action(self.s2SurveyTortuosity_tableWidget)
		self.s2SurveyTortuosity_tableWidget.addAction(C)
		
		V = cu.PasteToCells_action(self.s2SurveyTortuosity_tableWidget)
		self.s2SurveyTortuosity_tableWidget.addAction(V)

		clear_row = lambda: cu.clear_tableWidgetRow(self.s2SurveyTortuosity_tableWidget)
		D = cu.FunctionToWidget_action(self.s2SurveyTortuosity_tableWidget, clear_row, "Delete", 'Del')
		self.s2SurveyTortuosity_tableWidget.addAction(D)
		
		self.setup_s2SurveyTortuosity_tableWidget()

		select_row = lambda r,c : cu.select_tableWidgetRow(self.s2SurveyTortuosity_tableWidget,r)
		self.s2SurveyTortuosity_tableWidget.cellPressed.connect(select_row)
		self.s2SurveyTortuosity_tableWidget.itemChanged.connect(cu.update_fieldItem)


	def setup_s2SurveyTortuosity_tableWidget(self):

		self.v2SurveyTortuosity_fields = mdl.get_v2SurveyTortuosity_fields()
		for field in self.v2SurveyTortuosity_fields[:-1]:
			item = self.s2SurveyTortuosity_tableWidget.horizontalHeaderItem( field.pos )
			item.setText( field.headerName )
			
			for i in range(self.s2SurveyTortuosity_tableWidget.rowCount()):
				item = cu.TableWidgetFieldItem( field, i%2==0 )
				self.s2SurveyTortuosity_tableWidget.setItem(i, field.pos, item)


	def __init__s2TortuosityInterval_tableWidget(self):
		
		self.s2TortuosityInterval_tableWidget.parent = self
		self.s2TortuosityInterval_tableWidget.setContextMenuPolicy(Qt.ActionsContextMenu)
		
		C = cu.CopySelectedCells_action(self.s2TortuosityInterval_tableWidget)
		self.s2TortuosityInterval_tableWidget.addAction(C)
		
		V = cu.PasteToCells_action(self.s2TortuosityInterval_tableWidget)
		self.s2TortuosityInterval_tableWidget.addAction(V)
		
		self.setup_s2TortuosityInterval_tableWidget()

		select_row = lambda r,c : cu.select_tableWidgetRow(self.s2TortuosityInterval_tableWidget,r)
		self.s2TortuosityInterval_tableWidget.cellPressed.connect(select_row)
		self.s2TortuosityInterval_tableWidget.itemChanged.connect(cu.update_fieldItem)


	def setup_s2TortuosityInterval_tableWidget(self):

		self.v2TortuosityInterval_fields = mdl.get_v2TortuosityInterval_fields()
		item = self.s2TortuosityInterval_tableWidget.verticalHeaderItem( 0 )
		item.setText( self.v2TortuosityInterval_fields[0].headerName )
		item = cu.TableWidgetFieldItem( self.v2TortuosityInterval_fields[0], True )
		self.s2TortuosityInterval_tableWidget.setItem(0, 0, item)
	
		
	def __init__s3WellboreOuterStages_tableWidget(self):
			
		self.s3WellboreOuterStages_tableWidget.parent = self
		self.s3WellboreOuterStages_tableWidget.setContextMenuPolicy(Qt.ActionsContextMenu)
		
		#C = cu.CopySelectedCells_action(self.s3WellboreOuterStages_tableWidget)
		#self.s3WellboreOuterStages_tableWidget.addAction(C)
		
		#V = cu.PasteToCells_action(self.s3WellboreOuterStages_tableWidget)
		#self.s3WellboreOuterStages_tableWidget.addAction(V)
		
		open_TDB_dialog_for_outerStages = lambda: wf.open_TDB_dialog_for_outerStages(self)
		A = cu.FunctionToWidget_action(self.s3WellboreOuterStages_tableWidget, open_TDB_dialog_for_outerStages, "Add outer pipe")
		self.s3WellboreOuterStages_tableWidget.addAction(A)

		open_caliper_dialog = lambda: wf.open_caliper_dialog(self)
		A = cu.FunctionToWidget_action(self.s3WellboreOuterStages_tableWidget, open_caliper_dialog, "Import DR-CAL")
		self.s3WellboreOuterStages_tableWidget.addAction(A)

		open_csv_dialog = lambda: wf.open_csv_dialog(self)
		A = cu.FunctionToWidget_action(self.s3WellboreOuterStages_tableWidget, open_csv_dialog, "Insert CAL data")
		self.s3WellboreOuterStages_tableWidget.addAction(A)

		set_row_as_freeCH = lambda: wf.set_row_as_free(self)#, 'Casing Hole')
		F = cu.FunctionToWidget_action(self.s3WellboreOuterStages_tableWidget, set_row_as_freeCH, "Add as free stage")
		self.s3WellboreOuterStages_tableWidget.addAction(F)

		#set_row_as_freeOH = lambda: wf.set_row_as_free(self, 'Open Hole')
		#F = cu.FunctionToWidget_action(self.s3WellboreOuterStages_tableWidget, set_row_as_freeOH, "Add as free OH")
		#self.s3WellboreOuterStages_tableWidget.addAction(F)

		delete_outerStageObjects = lambda: wf.delete_outerStageObjects(self)
		D = cu.FunctionToWidget_action(self.s3WellboreOuterStages_tableWidget, delete_outerStageObjects, "Delete stage", 'Del')
		self.s3WellboreOuterStages_tableWidget.addAction(D)

		#unlock_tableWidget = lambda: wf.unlock_tableWidget(self)
		#U = cu.FunctionToWidget_action(self.s3WellboreOuterStages_tableWidget, unlock_tableWidget, "Unlock all the table", 'Del')
		#self.s3WellboreOuterStages_tableWidget.addAction(U)
		
		self.setup_s3WellboreOuterStages_tableWidget()

		select_outerStageRow_and_prepare_outerStageObjects = lambda r,c : wf.select_outerStageRow_and_prepare_outerStageObjects(self, r)
		update_fieldItem_and_wellboreOuterStageData = lambda item: wf.update_fieldItem_and_wellboreOuterStageData(self, item)
		self.s3WellboreOuterStages_tableWidget.cellPressed.connect(select_outerStageRow_and_prepare_outerStageObjects)
		self.s3WellboreOuterStages_tableWidget.itemChanged.connect(update_fieldItem_and_wellboreOuterStageData)


	def setup_s3WellboreOuterStages_tableWidget(self):

		self.v3WellboreOuterStages_fields = mdl.get_v3WellboreOuterStages_fields()
		for field in self.v3WellboreOuterStages_fields:
			item = self.s3WellboreOuterStages_tableWidget.horizontalHeaderItem( field.pos )
			item.setText( field.headerName )
			
			for i in range(self.s3WellboreOuterStages_tableWidget.rowCount()):
				item = cu.TableWidgetFieldItem( field, i%2==0 )
				self.s3WellboreOuterStages_tableWidget.setItem(i, field.pos, item)

	
	def __init__s3WellboreInnerStages_tableWidget(self):
		
		self.s3WellboreInnerStages_tableWidget.parent = self
		self.s3WellboreInnerStages_tableWidget.setContextMenuPolicy(Qt.ActionsContextMenu)

		#C = cu.CopySelectedCells_action(self.s3WellboreInnerStages_tableWidget)
		#self.s3WellboreInnerStages_tableWidget.addAction(C)
		
		#V = cu.PasteToCells_action(self.s3WellboreInnerStages_tableWidget)
		#self.s3WellboreInnerStages_tableWidget.addAction(V)

		open_TDB_dialog_for_innerStages = lambda: wf.open_TDB_dialog_for_innerStages(self)
		P = cu.FunctionToWidget_action(self.s3WellboreInnerStages_tableWidget, open_TDB_dialog_for_innerStages, "Import Pipe ...", '')
		self.s3WellboreInnerStages_tableWidget.addAction(P)

		adjust_MD_to_wellboreDeep = lambda: wf.adjust_MD_to_wellboreDeep(self)
		A = cu.FunctionToWidget_action(self.s3WellboreInnerStages_tableWidget, adjust_MD_to_wellboreDeep, "Adjust stage to depth", '')
		self.s3WellboreInnerStages_tableWidget.addAction(A)

		delete_innerStageObjects = lambda: wf.delete_innerStageObjects(self)
		D = cu.FunctionToWidget_action(self.s3WellboreInnerStages_tableWidget, delete_innerStageObjects, "Delete stage", 'Del')
		self.s3WellboreInnerStages_tableWidget.addAction(D)
		
		self.setup_s3WellboreInnerStages_tableWidget()

		self._PipeCentralizationStageAdjusting_isEnabled = True

		select_innerStageRow_and_prepare_innerStageObjects = lambda r,c : wf.select_innerStageRow_and_prepare_innerStageObjects(self, r)
		self.s3WellboreInnerStages_tableWidget.cellPressed.connect(select_innerStageRow_and_prepare_innerStageObjects)

		updateMD_wellboreInnerStageData = lambda item: wf.updateMD_wellboreInnerStageData(self, item)
		self.s3WellboreInnerStages_tableWidget.itemChanged.connect(updateMD_wellboreInnerStageData)

		self.s3WellboreInnerStages_tableWidget.resizeColumnsToContents()


	def setup_s3WellboreInnerStages_tableWidget(self):

		self.v3WellboreInnerStages_fields = mdl.get_v3WellboreInnerStages_fields()
		for size,field in zip([40,20,20], self.v3WellboreInnerStages_fields):
			item = self.s3WellboreInnerStages_tableWidget.horizontalHeaderItem( field.pos )
			item.setText( cu.extend_text( field.headerName, size, mode='center' ) )
			
			for i in range(self.s3WellboreInnerStages_tableWidget.rowCount()):
				item = cu.TableWidgetFieldItem( field, i%2==0 )
				self.s3WellboreInnerStages_tableWidget.setItem(i, field.pos, item)


	def __init__s3PipeProperties_tableWidget(self):

		self.s3PipeProperties_tableWidget.parent = self
		self.s3PipeProperties_tableWidget.setContextMenuPolicy(Qt.ActionsContextMenu)
		
		C = cu.CopySelectedCells_action(self.s3PipeProperties_tableWidget)
		self.s3PipeProperties_tableWidget.addAction(C)
		
		V = cu.PasteToCells_action(self.s3PipeProperties_tableWidget)
		self.s3PipeProperties_tableWidget.addAction(V)
		
		self.setup_s3PipeProperties_tableWidget()

		update_fieldItem_and_wellboreInnerStageData = lambda item: wf.update_fieldItem_and_wellboreInnerStageData(self, item)
		self.s3PipeProperties_tableWidget.itemChanged.connect(update_fieldItem_and_wellboreInnerStageData)


	def setup_s3PipeProperties_tableWidget(self):

		self.v3PipeProperties_fields = mdl.get_v3PipeProperties_fields()
		for field in self.v3PipeProperties_fields:
			
			item = QTableWidgetItem()
			self.s3PipeProperties_tableWidget.setVerticalHeaderItem(field.pos, item)
			item.setText( cu.extend_text( field.headerName, 30 ) )
			item = cu.TableWidgetFieldItem( field, False )
			self.s3PipeProperties_tableWidget.setItem(field.pos, 0, item)

	
	def __init__s3CentralizerProperties_tableWidgets(self):

		self.v3CentralizerProperties_fields_A = mdl.get_v3CentralizerProperties_fields()
		self.s3CentralizerProperties_tableWidget_A.parent = self
		wf.init_s3CentralizerProperties_tableWidget(self, 'A')
		#wf.setup2_s3CentralizerProperties_tableWidget(self, 'A')

		self.v3CentralizerProperties_fields_B = mdl.get_v3CentralizerProperties_fields()
		self.s3CentralizerProperties_tableWidget_B.parent = self
		wf.init_s3CentralizerProperties_tableWidget(self, 'B')
		#wf.setup2_s3CentralizerProperties_tableWidget(self, 'B')

		self.v3CentralizerProperties_fields_C = mdl.get_v3CentralizerProperties_fields()
		self.s3CentralizerProperties_tableWidget_C.parent = self
		wf.init_s3CentralizerProperties_tableWidget(self, 'C')
		#wf.setup2_s3CentralizerProperties_tableWidget(self, 'C')


	def __init__s3CentralizerLocation_tableWidgets(self):

		self.v3CentralizerLocation_fields_A = mdl.get_v3CentralizerLocation_fields()
		self.s3CentralizerLocation_tableWidget_A.parent = self
		wf.init_s3CentralizerLocation_tableWidget(self, 'A')
		#wf.setup2_s3CentralizerLocation_tableWidget(self, 'A')

		self.v3CentralizerLocation_fields_B = mdl.get_v3CentralizerLocation_fields()
		self.s3CentralizerLocation_tableWidget_B.parent = self
		wf.init_s3CentralizerLocation_tableWidget(self, 'B')
		#wf.setup2_s3CentralizerLocation_tableWidget(self, 'B')

		self.v3CentralizerLocation_fields_C = mdl.get_v3CentralizerLocation_fields()
		self.s3CentralizerLocation_tableWidget_C.parent = self
		wf.init_s3CentralizerLocation_tableWidget(self, 'C')
		#wf.setup2_s3CentralizerLocation_tableWidget(self, 'C')


	def __init__s4Settings_tableWidget(self):

		self.s4Settings_tableWidget.parent = self
		self.s4Settings_tableWidget.setContextMenuPolicy(Qt.ActionsContextMenu)
		
		C = cu.CopySelectedCells_action(self.s4Settings_tableWidget)
		self.s4Settings_tableWidget.addAction(C)
		
		V = cu.PasteToCells_action(self.s4Settings_tableWidget)
		self.s4Settings_tableWidget.addAction(V)

		self.setup_s4Settings_tableWidget()

		#def auxiliar_function(item):
		#	item.field.put( 0, item.realValue )
		#	print( item.realValue, id(item.field), self.v4Settings_fields, id(self.v4Settings_fields[item.field.pos]) )

		def update_through_itemChange(item):
			cu.update_fieldItem(item)
			self.v4Settings_fields[item.field.pos].put( 0, item.realValue )

		self.s4Settings_tableWidget.itemChanged.connect(update_through_itemChange)


	def setup_s4Settings_tableWidget(self):

		self.v4Settings_fields = mdl.get_v4Settings_fields()
		for field in self.v4Settings_fields[:5]:
			item = QTableWidgetItem()
			self.s4Settings_tableWidget.setVerticalHeaderItem(field.pos, item)
			item.setText( cu.extend_text( field.headerName, 40 ) )
			item = cu.TableWidgetFieldItem( field, False )
			self.s4Settings_tableWidget.setItem(field.pos, 0, item)


	def __init__s4TorqueDragSideforce_tableWidget(self):
		
		self.s4TorqueDragSideforce_tableWidget.parent = self
		self.s4TorqueDragSideforce_tableWidget.setContextMenuPolicy(Qt.ActionsContextMenu)

		C = cu.CopySelectedCells_action(self.s4TorqueDragSideforce_tableWidget)
		self.s4TorqueDragSideforce_tableWidget.addAction(C)
		
		self.setup_s4TorqueDragSideforce_tableWidget()

		select_row = lambda r,c : cu.select_tableWidgetRow(self.s4TorqueDragSideforce_tableWidget,r)
		self.s4TorqueDragSideforce_tableWidget.cellPressed.connect(select_row)

		self.s4TorqueDragSideforce_tableWidget.resizeColumnsToContents()


	def setup_s4TorqueDragSideforce_tableWidget(self):

		self.v4TorqueDragForces_fields = mdl.get_v4TorqueDragForces_fields()
		
		for size,field in zip([20,20,20,20,20,20,20], self.v4TorqueDragForces_fields[:7]):
			item = self.s4TorqueDragSideforce_tableWidget.horizontalHeaderItem( field.pos )
			item.setText( cu.extend_text( field.headerName, size, mode='center' ) )
			
			for i in range(self.s4TorqueDragSideforce_tableWidget.rowCount()):
				item = cu.TableWidgetFieldItem( field, i%2==0 )
				self.s4TorqueDragSideforce_tableWidget.setItem(i, field.pos, item)

