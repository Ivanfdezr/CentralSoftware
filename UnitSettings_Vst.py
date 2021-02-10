# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UnitSettings_Vst.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_UnitSettings(object):
	def setupUi(self, UnitSettings):
		UnitSettings.setObjectName("UnitSettings")
		UnitSettings.resize(557, 603)
		font = QtGui.QFont()
		font.setPointSize(10)
		UnitSettings.setFont(font)
		self.usParameterUnits_tableWidget = QtWidgets.QTableWidget(UnitSettings)
		self.usParameterUnits_tableWidget.setGeometry(QtCore.QRect(20, 70, 441, 457))
		self.usParameterUnits_tableWidget.setAutoScroll(False)
		self.usParameterUnits_tableWidget.setRowCount(50)
		self.usParameterUnits_tableWidget.setObjectName("usParameterUnits_tableWidget")
		self.usParameterUnits_tableWidget.setColumnCount(2)
		item = QtWidgets.QTableWidgetItem()
		self.usParameterUnits_tableWidget.setHorizontalHeaderItem(0, item)
		item = QtWidgets.QTableWidgetItem()
		self.usParameterUnits_tableWidget.setHorizontalHeaderItem(1, item)
		self.usParameterUnits_tableWidget.horizontalHeader().setDefaultSectionSize(195)
		self.usParameterUnits_tableWidget.verticalHeader().setDefaultSectionSize(25)
		self.us_buttonBox = QtWidgets.QDialogButtonBox(UnitSettings)
		self.us_buttonBox.setGeometry(QtCore.QRect(330, 550, 191, 31))
		self.us_buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
		self.us_buttonBox.setObjectName("us_buttonBox")
		self.usConvertUnits_pushButton = QtWidgets.QPushButton(UnitSettings)
		self.usConvertUnits_pushButton.setGeometry(QtCore.QRect(20, 550, 161, 28))
		self.usConvertUnits_pushButton.setObjectName("usConvertUnits_pushButton")
		self.layoutWidget = QtWidgets.QWidget(UnitSettings)
		self.layoutWidget.setGeometry(QtCore.QRect(20, 20, 531, 41))
		self.layoutWidget.setObjectName("layoutWidget")
		self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
		self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
		self.horizontalLayout.setObjectName("horizontalLayout")
		self.usUSOF_radioButton = QtWidgets.QRadioButton(self.layoutWidget)
		self.usUSOF_radioButton.setObjectName("usUSOF_radioButton")
		self.horizontalLayout.addWidget(self.usUSOF_radioButton)
		self.usMetric_radioButton = QtWidgets.QRadioButton(self.layoutWidget)
		self.usMetric_radioButton.setObjectName("usMetric_radioButton")
		self.horizontalLayout.addWidget(self.usMetric_radioButton)
		self.usCustomized_radioButton = QtWidgets.QRadioButton(self.layoutWidget)
		self.usCustomized_radioButton.setChecked(True)
		self.usCustomized_radioButton.setObjectName("usCustomized_radioButton")
		self.horizontalLayout.addWidget(self.usCustomized_radioButton)

		self.retranslateUi(UnitSettings)
		QtCore.QMetaObject.connectSlotsByName(UnitSettings)

	def retranslateUi(self, UnitSettings):
		_translate = QtCore.QCoreApplication.translate
		UnitSettings.setWindowTitle(_translate("UnitSettings", "Unit Settings"))
		item = self.usParameterUnits_tableWidget.horizontalHeaderItem(0)
		item.setText(_translate("UnitSettings", "Parameters"))
		item = self.usParameterUnits_tableWidget.horizontalHeaderItem(1)
		item.setText(_translate("UnitSettings", "Units"))
		self.usConvertUnits_pushButton.setText(_translate("UnitSettings", "Convert..."))
		self.usUSOF_radioButton.setText(_translate("UnitSettings", "US oil field"))
		self.usMetric_radioButton.setText(_translate("UnitSettings", "Metric"))
		self.usCustomized_radioButton.setText(_translate("UnitSettings", "Customized"))

