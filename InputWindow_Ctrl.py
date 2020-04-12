from PyQt4 import QtCore, QtGui
from InputWindow_Vst import Ui_InputWindow
from UnitSettings_Ctrl import Main_UnitSettings
from OneSpanAnalysis_Ctrl import Main_OneSpanAnalysis
from OutputWindow_Ctrl import Main_OutputWindow
import InputWindow_Mdl as mdl
import CtrlUtilities as cu
import MdlUtilities as mu
import SurveyFunctions as sf
import WellboreFunctions as wf
import TDSFunctions as tdsf
import importlib
import sys


class Main_InputWindow(Ui_InputWindow):

	def __init__(self, window):
		Ui_InputWindow.__init__(self)
		self.setupUi(window)

		self.wellboreInnerStageData = {}
		self.wellboreOuterStageData = {}
		self.FileLines = None
		self.filename = None

		self.s1Info_fields = mdl.get_s1Info_fields()
		item = cu.TableWidgetFieldItem( self.s1Info_fields[5], False )
		self.s1Info_tableWidget.setItem(5, 0, item)

		self.wellboreOuterStageDataIsUpdatable = True
		self.wellboreInnerStageDataIsUpdatable = True
		self.wellboreInnerStageDataIsEnabled = True
		self._PipeCentralizationStageAdjusting_isEnabled = True

		self.__init__s2DataSurvey_tableWidget()
		self.__init__s2SurveyTortuosity_tableWidget()
		self.__init__s2KOP_tableWidget()
		self.__init__s2TortuosityInterval_tableWidget()
		self.__init__s3WellboreOuterStages_tableWidget()
		self.__init__s3WellboreInnerStages_tableWidget()
		#self.__init__s3CentralizerSpacing_tableWidget()
		self.__init__s3PipeProperties_tableWidget()
		self.__init__s3CentralizerProperties_tableWidgets()
		self.__init__s3CentralizerRunningForce_tableWidgets()
		self.__init__s3CentralizerLocation_tableWidgets()
		self.__init__s4Settings_tableWidget()
		self.__init__s4TorqueDragSideforce_tableWidget()

		self.actionAbout.triggered.connect(self.about)
		self.objectsSizes = {}

		self.actionOne_Span_Analysis.triggered.connect(self.open_oneSpanAnalysisDialog)
		self.actionStar_Calculation.triggered.connect(self.open_outputWindow)
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
		
		calculate_axialForce_field = lambda: mdl.calculate_axialForce_field(self)
		self.s3UpdateInnerStages_pushButton.clicked.connect(calculate_axialForce_field)
		self.s3UpdateInnerStages_pushButton.setEnabled(False)

		adjust_Wt = lambda: wf.adjust_Wt(self)
		adjust_ID = lambda: wf.adjust_ID(self)
		self.s3ODID_pushButton.clicked.connect(adjust_Wt)
		self.s3ODWt_pushButton.clicked.connect(adjust_ID)

		open_specifyCentralization_dialog = lambda: wf.open_specifyCentralization_dialog(self)
		self.s3SpecifyCentralization_pushButton.clicked.connect(open_specifyCentralization_dialog)

		open_CDB_dialog_A = lambda: wf.open_CDB_dialog(self, 'A')
		open_CDB_dialog_B = lambda: wf.open_CDB_dialog(self, 'B')
		open_CDB_dialog_C = lambda: wf.open_CDB_dialog(self, 'C')
		self.s3CentralizerDB_pushButton_A.clicked.connect(open_CDB_dialog_A)
		self.s3CentralizerDB_pushButton_B.clicked.connect(open_CDB_dialog_B)
		self.s3CentralizerDB_pushButton_C.clicked.connect(open_CDB_dialog_C)

		setEnabled_specifySpacingToolkit = lambda: wf.setEnabled_specifySpacingToolkit(self)
		setEnabled_specifyStandoffToolkit = lambda: wf.setEnabled_specifyStandoffToolkit(self)
		setEnabled_specifyLocationToolkit = lambda: wf.setEnabled_specifyLocationToolkit(self)
		setDisabled_ABC_tabWidget = lambda: self.ABC_tabWidget.setEnabled(False)
		setDisabled_ABC_tabWidget()
		self.s3SpecifySpacingCentralization_radioButton.toggled.connect(setEnabled_specifySpacingToolkit)
		#self.s3SpecifyStandoffCentralization_radioButton.clicked.connect(setEnabled_specifyStandoffToolkit)
		self.s3SpecifyLocationCentralization_radioButton.toggled.connect(setEnabled_specifyLocationToolkit)
		self.s3NoneCentralization_radioButton.clicked.connect(setDisabled_ABC_tabWidget)

		setEnabled_bowSpringToolkit_A = lambda: wf.setEnabled_bowSpringToolkit(self, 'A')
		setEnabled_rigidToolkit_A = lambda: wf.setEnabled_rigidToolkit(self, 'A')
		self.s3BowSpringCentralizer_radioButton_A.clicked.connect(setEnabled_bowSpringToolkit_A)
		self.s3RigidCentralizer_radioButton_A.clicked.connect(setEnabled_rigidToolkit_A)

		setEnabled_bowSpringToolkit_B = lambda: wf.setEnabled_bowSpringToolkit(self, 'B')
		setEnabled_rigidToolkit_B = lambda: wf.setEnabled_rigidToolkit(self, 'B')
		setDisabled_centralizerToolkit_B = lambda: wf.setDisabled_centralizerToolkit(self, 'B')
		self.s3BowSpringCentralizer_radioButton_B.clicked.connect(setEnabled_bowSpringToolkit_B)
		self.s3RigidCentralizer_radioButton_B.clicked.connect(setEnabled_rigidToolkit_B)
		self.s3NoneCentralizer_radioButton_B.clicked.connect(setDisabled_centralizerToolkit_B)

		setEnabled_bowSpringToolkit_C = lambda: wf.setEnabled_bowSpringToolkit(self, 'C')
		setEnabled_rigidToolkit_C = lambda: wf.setEnabled_rigidToolkit(self, 'C')
		setDisabled_centralizerToolkit_C = lambda: wf.setDisabled_centralizerToolkit(self, 'C')
		self.s3BowSpringCentralizer_radioButton_C.clicked.connect(setEnabled_bowSpringToolkit_C)
		self.s3RigidCentralizer_radioButton_C.clicked.connect(setEnabled_rigidToolkit_C)
		self.s3NoneCentralizer_radioButton_C.clicked.connect(setDisabled_centralizerToolkit_C)

		calculateAndDraw_torque_drag_sideforce = lambda: tdsf.calculateAndDraw_torque_drag_sideforce(self)
		self.s4Calculate_pushButton.clicked.connect(calculateAndDraw_torque_drag_sideforce)


	def about(self):

		importlib.reload(mdl)
		importlib.reload(cu)
		importlib.reload(mu)
		importlib.reload(wf)
		importlib.reload(sf)
		importlib.reload(tdsf)

		print('---------------------------------------------------------')
		for i,attr in enumerate(dir(self)):
			size = eval('cu.size_object(self.'+attr+')')
			if attr in self.objectsSizes and attr!="objectsSizes":
				#if self.objectsSizes[attr]!=size:
				eval('cu.count_nestedObjects(self.'+attr+',name="self.'+attr+'")')
				print( '======================================' )
			
			self.objectsSizes[attr] = size


	def set_workUnits_as(self, unitSystem):
		
		mdl.set_workUnits_as(unitSystem)
		self.wellboreInnerStageData = {}
		self.wellboreOuterStageData = {}

		self.wellboreOuterStageDataIsUpdatable = False
		self.wellboreInnerStageDataIsUpdatable = False
		self.wellboreInnerStageDataIsEnabled = False
		self._PipeCentralizationStageAdjusting_isEnabled = False

		self.setup_s2DataSurvey_tableWidget()
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
		tdsf.s4Settings_tableWidget()
		tdsf.s4TorqueDragSideforce_tableWidget()

		self.wellboreOuterStageDataIsUpdatable = True
		self.wellboreInnerStageDataIsUpdatable = True
		self.wellboreInnerStageDataIsEnabled = True
		self._PipeCentralizationStageAdjusting_isEnabled = True


	def open_selectWorkingDirectoryDialog(self):
		
		self.workingDirectory = QtGui.QFileDialog.getExistingDirectory( self.s1Info_tableWidget, 'Select the working directory', 'c:\\' )
		print(self.workingDirectory)
		item = self.s1Info_tableWidget.item( 5,0 )
		item.setText( self.workingDirectory )


	def open_unitSettingsDialog(self):
		dialog = QtGui.QDialog(self.s1UnitSetting_pushButton)
		Main_UnitSettings(dialog)
		self.s1Customized_radioButton.click()
		

	def open_oneSpanAnalysisDialog(self):
		dialog = QtGui.QDialog(self.iw_toolBar)
		Main_OneSpanAnalysis(dialog)


	def open_outputWindow(self):
		

		cu.savetable( 	self.s1Info_tableWidget,
						self.s1Info_fields,
						["tmp/GeneralInformation.csv",
						self.workingDirectory+"/GeneralInformation.csv"],
						orientation='v' )

		cu.savetable( 	self.s2DataSurvey_tableWidget,
						self.s2DataSurvey_fields,
						["tmp/DataSurvey.csv",
						self.workingDirectory+"/DataSurvey.csv"] )

		cu.savetable( 	self.s2SurveyTortuosity_tableWidget,
						self.s2SurveyTortuosity_fields,
						["tmp/SurveyTortuosity.csv",
						self.workingDirectory+"/SurveyTortuosity.csv"] )
		
		self.s2SectionView_graphicsView.figure.savefig( "tmp/SectionView.png", dpi=300 )

		self.s2PlanView_graphicsView.figure.savefig( "tmp/PlanView.png", dpi=300 )

		self.s2TriDView_graphicsView.figure.savefig( "tmp/TriDView.png", dpi=300 )

		self.s2Dogleg_graphicsView.figure.savefig( "tmp/Dogleg.png", dpi=300 )

		self.s2SectionView_graphicsView.figure.savefig( self.workingDirectory+"/SectionView.png", dpi=300 )

		self.s2PlanView_graphicsView.figure.savefig( self.workingDirectory+"/PlanView.png", dpi=300 )

		self.s2TriDView_graphicsView.figure.savefig( self.workingDirectory+"/TriDView.png", dpi=300 )

		self.s2Dogleg_graphicsView.figure.savefig( self.workingDirectory+"/Dogleg.png", dpi=300 )

		cu.savetable( 	self.s3WellboreOuterStages_tableWidget,
						self.s3WellboreOuterStages_fields,
						["tmp/WellboreOuterStages.csv",
						self.workingDirectory+"/WellboreOuterStages.csv"] )

		cu.savetable( 	self.s3WellboreInnerStages_tableWidget,
						self.s3WellboreInnerStages_fields,
						["tmp/WellboreInnerStages.csv",
						self.workingDirectory+"/WellboreInnerStages.csv"] )

		cu.savetable( 	self.s3PipeProperties_tableWidget,
						self.s3PipeProperties_fields,
						["tmp/PipeProperties.csv",
						self.workingDirectory+"/PipeProperties.csv"],
						orientation='v' )

		cu.savetable( 	self.s3CentralizerProperties_tableWidget_A,
						self.s3CentralizerProperties_fields_A,
						["tmp/CentralizerProperties_A.csv",
						self.workingDirectory+"/CentralizerProperties_A.csv"],
						orientation='v' )

		cu.savetable( 	self.s3CentralizerProperties_tableWidget_B,
						self.s3CentralizerProperties_fields_B,
						["tmp/CentralizerProperties_B.csv",
						self.workingDirectory+"/CentralizerProperties_B.csv"],
						orientation='v' )

		cu.savetable( 	self.s3CentralizerProperties_tableWidget_C,
						self.s3CentralizerProperties_fields_C,
						["tmp/CentralizerProperties_C.csv",
						self.workingDirectory+"/CentralizerProperties_C.csv"],
						orientation='v' )

		cu.savetable( 	self.s3CentralizerLocation_tableWidget_A,
						self.s3CentralizerLocation_fields_A,
						["tmp/CentralizerLocation.csv",
						self.workingDirectory+"/CentralizerLocation.csv"] )

		
	def __init__s2DataSurvey_tableWidget(self):
		
		self.s2DataSurvey_tableWidget.parent = self
		self.s2DataSurvey_tableWidget.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
		
		C = cu.CopySelectedCells_action(self.s2DataSurvey_tableWidget)
		self.s2DataSurvey_tableWidget.addAction(C)
		
		V = cu.PasteToCells_action(self.s2DataSurvey_tableWidget)
		self.s2DataSurvey_tableWidget.addAction(V)

		insert_row = lambda: cu.insert_tableWidgetRow(self.s2DataSurvey_tableWidget, self.s2DataSurvey_fields)
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

		self.s2DataSurvey_fields = mdl.get_s2DataSurvey_fields()
		self.s3Forces_fields = mdl.get_s3Forces_fields()
		for field in self.s2DataSurvey_fields:
			item = self.s2DataSurvey_tableWidget.horizontalHeaderItem( field.pos )
			item.setText( field.headerName )
			
			for i in range(self.s2DataSurvey_tableWidget.rowCount()):
				item = cu.TableWidgetFieldItem( field, i%2==0 )
				self.s2DataSurvey_tableWidget.setItem(i, field.pos, item)


	def __init__s2KOP_tableWidget(self):
		
		self.s2KOP_tableWidget.parent = self
		self.s2KOP_tableWidget.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
		
		C = cu.CopySelectedCells_action(self.s2KOP_tableWidget)
		self.s2KOP_tableWidget.addAction(C)
		
		V = cu.PasteToCells_action(self.s2KOP_tableWidget)
		self.s2KOP_tableWidget.addAction(V)
		
		self.setup_s2KOP_tableWidget()

		select_row = lambda r,c : cu.select_tableWidgetRow(self.s2KOP_tableWidget,r)
		self.s2KOP_tableWidget.cellPressed.connect(select_row)
		self.s2KOP_tableWidget.itemChanged.connect(cu.update_fieldItem)


	def setup_s2KOP_tableWidget(self):

		self.s2KOP_field = mdl.get_s2KOP_field()
		item = self.s2KOP_tableWidget.verticalHeaderItem( 0 )
		item.setText( self.s2KOP_field.headerName )
		item = cu.TableWidgetFieldItem( self.s2KOP_field, True )
		self.s2KOP_tableWidget.setItem(0, 0, item)


	def __init__s2SurveyTortuosity_tableWidget(self):
		
		self.s2SurveyTortuosity_tableWidget.parent = self
		self.s2SurveyTortuosity_tableWidget.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
		
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

		self.s2SurveyTortuosity_fields = mdl.get_s2SurveyTortuosity_fields()
		for field in self.s2SurveyTortuosity_fields[:-1]:
			item = self.s2SurveyTortuosity_tableWidget.horizontalHeaderItem( field.pos )
			item.setText( field.headerName )
			
			for i in range(self.s2SurveyTortuosity_tableWidget.rowCount()):
				item = cu.TableWidgetFieldItem( field, i%2==0 )
				self.s2SurveyTortuosity_tableWidget.setItem(i, field.pos, item)


	def __init__s2TortuosityInterval_tableWidget(self):
		
		self.s2TortuosityInterval_tableWidget.parent = self
		self.s2TortuosityInterval_tableWidget.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
		
		C = cu.CopySelectedCells_action(self.s2TortuosityInterval_tableWidget)
		self.s2TortuosityInterval_tableWidget.addAction(C)
		
		V = cu.PasteToCells_action(self.s2TortuosityInterval_tableWidget)
		self.s2TortuosityInterval_tableWidget.addAction(V)
		
		self.setup_s2TortuosityInterval_tableWidget()

		select_row = lambda r,c : cu.select_tableWidgetRow(self.s2TortuosityInterval_tableWidget,r)
		self.s2TortuosityInterval_tableWidget.cellPressed.connect(select_row)
		self.s2TortuosityInterval_tableWidget.itemChanged.connect(cu.update_fieldItem)


	def setup_s2TortuosityInterval_tableWidget(self):

		self.s2TortuosityInterval_field = mdl.get_s2TortuosityInterval_field()
		item = self.s2TortuosityInterval_tableWidget.verticalHeaderItem( 0 )
		item.setText( self.s2TortuosityInterval_field.headerName )
		item = cu.TableWidgetFieldItem( self.s2TortuosityInterval_field, True )
		self.s2TortuosityInterval_tableWidget.setItem(0, 0, item)
	
		
	def __init__s3WellboreOuterStages_tableWidget(self):
			
		self.s3WellboreOuterStages_tableWidget.parent = self
		self.s3WellboreOuterStages_tableWidget.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
		
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

		self.s3WellboreOuterStages_fields = mdl.get_s3WellboreOuterStages_fields()
		for field in self.s3WellboreOuterStages_fields:
			item = self.s3WellboreOuterStages_tableWidget.horizontalHeaderItem( field.pos )
			item.setText( field.headerName )
			
			for i in range(self.s3WellboreOuterStages_tableWidget.rowCount()):
				item = cu.TableWidgetFieldItem( field, i%2==0 )
				self.s3WellboreOuterStages_tableWidget.setItem(i, field.pos, item)

	
	def __init__s3WellboreInnerStages_tableWidget(self):
		
		self.s3WellboreInnerStages_tableWidget.parent = self
		self.s3WellboreInnerStages_tableWidget.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

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

		select_innerStageRow_and_prepare_innerStageObjects = lambda r,c : wf.select_innerStageRow_and_prepare_innerStageObjects(self, r)
		#adjust_Length_and_MD = lambda item: wf.adjust_Length_and_MD(self, item)
		updateMD_wellboreInnerStageData = lambda item: wf.updateMD_wellboreInnerStageData(self, item)
		self._PipeCentralizationStageAdjusting_isEnabled = True
		self.s3WellboreInnerStages_tableWidget.cellPressed.connect(select_innerStageRow_and_prepare_innerStageObjects)
		#self.s3WellboreInnerStages_tableWidget.itemChanged.connect(adjust_Length_and_MD)
		self.s3WellboreInnerStages_tableWidget.itemChanged.connect(updateMD_wellboreInnerStageData)

		self.s3WellboreInnerStages_tableWidget.resizeColumnsToContents()


	def setup_s3WellboreInnerStages_tableWidget(self):

		self.s3WellboreInnerStages_fields = mdl.get_s3WellboreInnerStages_fields()
		for size,field in zip([46,20,20], self.s3WellboreInnerStages_fields):
			item = self.s3WellboreInnerStages_tableWidget.horizontalHeaderItem( field.pos )
			item.setText( cu.extend_text( field.headerName, size, mode='center' ) )
			
			for i in range(self.s3WellboreInnerStages_tableWidget.rowCount()):
				item = cu.TableWidgetFieldItem( field, i%2==0 )
				self.s3WellboreInnerStages_tableWidget.setItem(i, field.pos, item)


	def __init__s3CentralizerSpacing_tableWidget(self):

		self.s3CentralizerSpacing_tableWidget.parent = self
		self.s3CentralizerSpacing_tableWidget.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
		
		C = cu.CopySelectedCells_action(self.s3CentralizerSpacing_tableWidget)
		self.s3CentralizerSpacing_tableWidget.addAction(C)
		
		V = cu.PasteToCells_action(self.s3CentralizerSpacing_tableWidget)
		self.s3CentralizerSpacing_tableWidget.addAction(V)
		
		self.setup_s3CentralizerSpacing_tableWidget()

		self.s3CentralizerSpacing_tableWidget.itemChanged.connect(cu.update_fieldItem)


	def setup_s3CentralizerSpacing_tableWidget(self):

		self.s3CentralizerSpacing_fields = mdl.get_s3CentralizerSpacing_fields()
		for field in self.s3CentralizerSpacing_fields:
			
			item = QtGui.QTableWidgetItem()
			self.s3CentralizerSpacing_tableWidget.setVerticalHeaderItem(field.pos, item)
			item.setText( cu.extend_text( field.headerName, 40 ) )
			item = cu.TableWidgetFieldItem( field, False )
			self.s3CentralizerSpacing_tableWidget.setItem(field.pos, 0, item)


	def __init__s3PipeProperties_tableWidget(self):

		self.s3PipeProperties_tableWidget.parent = self
		self.s3PipeProperties_tableWidget.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
		
		C = cu.CopySelectedCells_action(self.s3PipeProperties_tableWidget)
		self.s3PipeProperties_tableWidget.addAction(C)
		
		V = cu.PasteToCells_action(self.s3PipeProperties_tableWidget)
		self.s3PipeProperties_tableWidget.addAction(V)
		
		self.setup_s3PipeProperties_tableWidget()

		update_fieldItem_and_wellboreInnerStageData = lambda item: wf.update_fieldItem_and_wellboreInnerStageData(self, item)
		self.s3PipeProperties_tableWidget.itemChanged.connect(update_fieldItem_and_wellboreInnerStageData)


	def setup_s3PipeProperties_tableWidget(self):

		self.s3PipeProperties_fields = mdl.get_s3PipeProperties_fields()
		for field in self.s3PipeProperties_fields:
			
			item = QtGui.QTableWidgetItem()
			self.s3PipeProperties_tableWidget.setVerticalHeaderItem(field.pos, item)
			item.setText( cu.extend_text( field.headerName, 30 ) )
			item = cu.TableWidgetFieldItem( field, False )
			self.s3PipeProperties_tableWidget.setItem(field.pos, 0, item)

	
	def __init__s3CentralizerProperties_tableWidgets(self):

		self.s3CentralizerProperties_fields_A = mdl.get_s3CentralizerProperties_fields()
		self.s3CentralizerProperties_tableWidget_A.parent = self
		wf.init_s3CentralizerProperties_tableWidget(self, 'A')
		#wf.setup2_s3CentralizerProperties_tableWidget(self, 'A')

		self.s3CentralizerProperties_fields_B = mdl.get_s3CentralizerProperties_fields()
		self.s3CentralizerProperties_tableWidget_B.parent = self
		wf.init_s3CentralizerProperties_tableWidget(self, 'B')
		#wf.setup2_s3CentralizerProperties_tableWidget(self, 'B')

		self.s3CentralizerProperties_fields_C = mdl.get_s3CentralizerProperties_fields()
		self.s3CentralizerProperties_tableWidget_C.parent = self
		wf.init_s3CentralizerProperties_tableWidget(self, 'C')
		#wf.setup2_s3CentralizerProperties_tableWidget(self, 'C')


	def __init__s3CentralizerRunningForce_tableWidgets(self):

		self.s3CentralizerRunningForce_fields_A = mdl.get_s3CentralizerRunningForce_fields()
		self.s3CentralizerRunningForce_tableWidget_A.parent = self
		wf.init_s3CentralizerRunningForce_tableWidget(self, 'A')
		#wf.setup2_s3CentralizerRunningForce_tableWidget(self, 'A')

		self.s3CentralizerRunningForce_fields_B = mdl.get_s3CentralizerRunningForce_fields()
		self.s3CentralizerRunningForce_tableWidget_B.parent = self
		wf.init_s3CentralizerRunningForce_tableWidget(self, 'B')
		#wf.setup2_s3CentralizerRunningForce_tableWidget(self, 'B')

		self.s3CentralizerRunningForce_fields_C = mdl.get_s3CentralizerRunningForce_fields()
		self.s3CentralizerRunningForce_tableWidget_C.parent = self
		wf.init_s3CentralizerRunningForce_tableWidget(self, 'C')
		#wf.setup2_s3CentralizerRunningForce_tableWidget(self, 'C')


	def __init__s3CentralizerLocation_tableWidgets(self):

		self.s3CentralizerLocation_fields_A = mdl.get_s3CentralizerLocation_fields()
		self.s3CentralizerLocation_tableWidget_A.parent = self
		wf.init_s3CentralizerLocation_tableWidget(self, 'A')
		#wf.setup2_s3CentralizerLocation_tableWidget(self, 'A')

		self.s3CentralizerLocation_fields_B = mdl.get_s3CentralizerLocation_fields()
		self.s3CentralizerLocation_tableWidget_B.parent = self
		wf.init_s3CentralizerLocation_tableWidget(self, 'B')
		#wf.setup2_s3CentralizerLocation_tableWidget(self, 'B')

		self.s3CentralizerLocation_fields_C = mdl.get_s3CentralizerLocation_fields()
		self.s3CentralizerLocation_tableWidget_C.parent = self
		wf.init_s3CentralizerLocation_tableWidget(self, 'C')
		#wf.setup2_s3CentralizerLocation_tableWidget(self, 'C')


	def __init__s4Settings_tableWidget(self):

		self.s4Settings_tableWidget.parent = self
		self.s4Settings_tableWidget.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
		
		C = cu.CopySelectedCells_action(self.s4Settings_tableWidget)
		self.s4Settings_tableWidget.addAction(C)
		
		V = cu.PasteToCells_action(self.s4Settings_tableWidget)
		self.s4Settings_tableWidget.addAction(V)

		self.setup_s4Settings_tableWidget()

		def auxiliar_function(item):
			item.field.clear()
			item.field.append( item.realValue )

		def update_through_itemChange(item):
			call_function = lambda: auxiliar_function(item)
			cu.update_fieldItem(item, call_function)

		self.s4Settings_tableWidget.itemChanged.connect(update_through_itemChange)


	def setup_s4Settings_tableWidget(self):

		self.s4Settings_fields = mdl.get_s4Settings_fields()
		for field in self.s4Settings_fields:
			item = QtGui.QTableWidgetItem()
			self.s4Settings_tableWidget.setVerticalHeaderItem(field.pos, item)
			item.setText( cu.extend_text( field.headerName, 40 ) )
			item = cu.TableWidgetFieldItem( field, False )
			self.s4Settings_tableWidget.setItem(field.pos, 0, item)


	def __init__s4TorqueDragSideforce_tableWidget(self):
		
		self.s4TorqueDragSideforce_tableWidget.parent = self
		self.s4TorqueDragSideforce_tableWidget.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

		C = cu.CopySelectedCells_action(self.s4TorqueDragSideforce_tableWidget)
		self.s4TorqueDragSideforce_tableWidget.addAction(C)
		
		self.setup_s4TorqueDragSideforce_tableWidget()

		select_row = lambda r,c : cu.select_tableWidgetRow(self.s4TorqueDragSideforce_tableWidget,r)
		self.s4TorqueDragSideforce_tableWidget.cellPressed.connect(select_row)

		self.s4TorqueDragSideforce_tableWidget.resizeColumnsToContents()


	def setup_s4TorqueDragSideforce_tableWidget(self):

		self.s4TorqueDragSideforce_fields = mdl.get_s4TorqueDragSideforce_fields()
		for size,field in zip([20,20,20,20,20,20,20,20,20], self.s4TorqueDragSideforce_fields):
			item = self.s4TorqueDragSideforce_tableWidget.horizontalHeaderItem( field.pos )
			item.setText( cu.extend_text( field.headerName, size, mode='center' ) )
			
			for i in range(self.s4TorqueDragSideforce_tableWidget.rowCount()):
				item = cu.TableWidgetFieldItem( field, i%2==0 )
				self.s4TorqueDragSideforce_tableWidget.setItem(i, field.pos, item)

"""
def main():
	app = QtGui.QApplication([])
	window = QtGui.QMainWindow()
	#window.setMinimumSize(400, 300)
	main_iw = Main_InputWindow(window)
	
	window.show()
	app.exec_()


if __name__ == "__main__":
	main()
"""