# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UnitSettings_Vst.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
	_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
	def _fromUtf8(s):
		return s

try:
	_encoding = QtGui.QApplication.UnicodeUTF8
	def _translate(context, text, disambig):
		return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
	def _translate(context, text, disambig):
		return QtGui.QApplication.translate(context, text, disambig)

class Ui_UnitSettings(object):
	def setupUi(self, UnitSettings):
		UnitSettings.setObjectName(_fromUtf8("UnitSettings"))
		UnitSettings.resize(557, 603)
		font = QtGui.QFont()
		font.setPointSize(10)
		UnitSettings.setFont(font)
		self.usParameterUnits_tableWidget = QtGui.QTableWidget(UnitSettings)
		self.usParameterUnits_tableWidget.setGeometry(QtCore.QRect(20, 70, 441, 457))
		self.usParameterUnits_tableWidget.setAutoScroll(False)
		self.usParameterUnits_tableWidget.setRowCount(50)
		self.usParameterUnits_tableWidget.setObjectName(_fromUtf8("usParameterUnits_tableWidget"))
		self.usParameterUnits_tableWidget.setColumnCount(2)
		item = QtGui.QTableWidgetItem()
		self.usParameterUnits_tableWidget.setHorizontalHeaderItem(0, item)
		item = QtGui.QTableWidgetItem()
		self.usParameterUnits_tableWidget.setHorizontalHeaderItem(1, item)
		self.usParameterUnits_tableWidget.horizontalHeader().setDefaultSectionSize(195)
		self.usParameterUnits_tableWidget.verticalHeader().setDefaultSectionSize(25)
		self.us_buttonBox = QtGui.QDialogButtonBox(UnitSettings)
		self.us_buttonBox.setGeometry(QtCore.QRect(330, 550, 191, 31))
		self.us_buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
		self.us_buttonBox.setObjectName(_fromUtf8("us_buttonBox"))
		self.usConvertUnits_pushButton = QtGui.QPushButton(UnitSettings)
		self.usConvertUnits_pushButton.setGeometry(QtCore.QRect(20, 550, 161, 28))
		self.usConvertUnits_pushButton.setObjectName(_fromUtf8("usConvertUnits_pushButton"))
		self.layoutWidget = QtGui.QWidget(UnitSettings)
		self.layoutWidget.setGeometry(QtCore.QRect(20, 20, 531, 41))
		self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
		self.horizontalLayout = QtGui.QHBoxLayout(self.layoutWidget)
		self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
		self.usUSOF_radioButton = QtGui.QRadioButton(self.layoutWidget)
		self.usUSOF_radioButton.setObjectName(_fromUtf8("usUSOF_radioButton"))
		self.horizontalLayout.addWidget(self.usUSOF_radioButton)
		self.usMetric_radioButton = QtGui.QRadioButton(self.layoutWidget)
		self.usMetric_radioButton.setObjectName(_fromUtf8("usMetric_radioButton"))
		self.horizontalLayout.addWidget(self.usMetric_radioButton)
		self.usCustomized_radioButton = QtGui.QRadioButton(self.layoutWidget)
		self.usCustomized_radioButton.setChecked(True)
		self.usCustomized_radioButton.setObjectName(_fromUtf8("usCustomized_radioButton"))
		self.horizontalLayout.addWidget(self.usCustomized_radioButton)

		self.retranslateUi(UnitSettings)
		QtCore.QMetaObject.connectSlotsByName(UnitSettings)

	def retranslateUi(self, UnitSettings):
		UnitSettings.setWindowTitle(_translate("UnitSettings", "Unit Settings", None))
		item = self.usParameterUnits_tableWidget.horizontalHeaderItem(0)
		item.setText(_translate("UnitSettings", "Parameters", None))
		item = self.usParameterUnits_tableWidget.horizontalHeaderItem(1)
		item.setText(_translate("UnitSettings", "Units", None))
		self.usConvertUnits_pushButton.setText(_translate("UnitSettings", "Convert...", None))
		self.usUSOF_radioButton.setText(_translate("UnitSettings", "US oil field", None))
		self.usMetric_radioButton.setText(_translate("UnitSettings", "Metric", None))
		self.usCustomized_radioButton.setText(_translate("UnitSettings", "Customized", None))

