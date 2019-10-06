from PyQt4 import QtCore, QtGui
from UnitConversion_Vst import Ui_Dialog
import UnitConversion_Mdl as mdl

class Main_UnitConversion(Ui_Dialog):

	def __init__(self, window):
		Ui_Dialog.__init__(self)
		self.setupUi(window)

		L = mdl.read_parameters()
		#

		self.comboBox.addItems(L)
		
		DecimalPlaces = list(map(str,range(1,9)))
		self.comboBox_4.addItems(DecimalPlaces)
		self.parameter_selected(0)
		self.unit_origin(0)
		self.unit_target(0)
		self.decimal_places_selected(0)
		
		self.comboBox.currentIndexChanged.connect(self.parameter_selected)
		self.comboBox_2.currentIndexChanged.connect(self.unit_origin)
		self.comboBox_3.currentIndexChanged.connect(self.unit_target)
		self.comboBox_4.currentIndexChanged.connect(self.decimal_places_selected)
		self.convert.clicked.connect(self.calculate)
		
		
	def decimal_places_selected(self,index):
		self.decimal_places = index + 1

		# 

	def parameter_selected(self,index):
		self.Parameter = self.comboBox.itemText(index)
		print (self.Parameter)
		units = mdl.read_units(self.Parameter)
		
		self.comboBox_2.clear()
		self.comboBox_3.clear()

		self.comboBox_2.addItems(units)
		self.comboBox_3.addItems(units)


	def unit_origin(self, index):
		self.origin = self.comboBox_2.itemText(index)

	def unit_target(self,index):	
		self.target = self.comboBox_3.itemText(index)

	def calculate(self):
		result = mdl.calculate(self.origin,self.target,self.lineEdit.text(),self.decimal_places)
		self.lineEdit_2.setText(str(result))

		#mdl.generate_binnacle(self.Parameter,self.origin,self.target,self.lineEdit.text(),self.decimal_places, result)



if __name__ == "__main__":
	app = QtGui.QApplication([])
	window = QtGui.QMainWindow()
	
	main_uc = Main_UnitConversion(window)
	#main_uc.connect_signals()

	window.show()
	app.exec_()

		 
