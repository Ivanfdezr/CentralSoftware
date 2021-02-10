from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from UnitSettings_Vst import Ui_UnitSettings
import UnitSettings_Mdl as mdl
import CtrlUtilities as cu


class OwnQComboBox(QComboBox):
    def __init__(self, scrollWidget=None, *args, **kwargs):
        super().__init__(*args, **kwargs) #OwnQComboBox, self

    def wheelEvent(self, *args, **kwargs):
        return None

	
class Main_UnitSettings(Ui_UnitSettings):

	def __init__(self, dialog ):
		
		Ui_UnitSettings.__init__(self)
		self.setupUi(dialog)
		self.dialog = dialog		
		
		self.__init__usParameterUnits_tableWidget('cu')
		setup_usParameterUSUnits_tableWidget = lambda: self.setup_usParameterUnits_tableWidget('us')
		setup_usParameterSIUnits_tableWidget = lambda: self.setup_usParameterUnits_tableWidget('si')
		setup_usParameterCuUnits_tableWidget = lambda: self.setup_usParameterUnits_tableWidget('cu')
		self.usUSOF_radioButton.clicked.connect(setup_usParameterUSUnits_tableWidget)
		self.usMetric_radioButton.clicked.connect(setup_usParameterSIUnits_tableWidget)
		self.usCustomized_radioButton.clicked.connect(setup_usParameterCuUnits_tableWidget)

		self.us_buttonBox.accepted.connect( self.update_customizedUnits )
		close_dialog = lambda: self.dialog.done(0)
		self.us_buttonBox.rejected.connect( close_dialog )
		
		dialog.setAttribute(Qt.WA_DeleteOnClose)
		dialog.exec_()
	
	
	def __init__usParameterUnits_tableWidget(self, unitSystem):
		
		parameters, Units = mdl.get_parametersAndUnits(unitSystem)
		self.usParameterUnits_tableWidget.setRowCount(len(parameters))

		item = QTableWidgetItem()
		self.usParameterUnits_tableWidget.setHorizontalHeaderItem(0, item)
		item.setText( 'Parameter' )
		item = QTableWidgetItem()
		self.usParameterUnits_tableWidget.setHorizontalHeaderItem(1, item)
		item.setText( 'Unit' )
		
		for row, (parameter, units) in enumerate( zip(parameters, Units) ):
			item = QTableWidgetItem()
			self.usParameterUnits_tableWidget.setItem(row, 0, item)
			item.setText( parameter )
			combo = OwnQComboBox() # QComboBox()
			self.usParameterUnits_tableWidget.setCellWidget(row, 1, combo)
			combo.addItems( units )

		#self.usParameterUnits_tableWidget.cellPressed.connect( self.print_parameterunitid )


	def setup_usParameterUnits_tableWidget(self, unitSystem):

		parameters, Units = mdl.get_parametersAndUnits(unitSystem)
		for row, (parameter, units) in enumerate( zip(parameters, Units) ):
			item = self.usParameterUnits_tableWidget.item(row, 0)
			item.setText( parameter )
			combo = self.usParameterUnits_tableWidget.cellWidget(row, 1)
			combo.clear()
			combo.addItems( units )


	def update_customizedUnits(self):

		parameters = []
		units = []
		for row in range(self.usParameterUnits_tableWidget.rowCount()):
			item = self.usParameterUnits_tableWidget.item(row, 0)
			parameters.append( item.text() )
			combo = self.usParameterUnits_tableWidget.cellWidget(row, 1)
			units.append( combo.currentText() )

		mdl.update_customizedUnits( parameters, units )

		msg = "Current unit profile were successfully updated as Customized profile unit."
		QMessageBox.information(self.usParameterUnits_tableWidget, 'Warning', msg)
		cu.sleep(0.25)
		self.dialog.done(0)

	

	def print_parameterunitid(self, row, column):

		parameterName = self.usParameterUnits_tableWidget.item(row,0).text()
		parameterID = mdl.get_parameterID(parameterName)

		unitName = self.usParameterUnits_tableWidget.cellWidget(row,1).currentText()
		unitID = mdl.get_unitID(unitName)
