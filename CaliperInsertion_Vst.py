# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CaliperInsertion_Vst.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_CaliperInsertion(object):
	def setupUi(self, CaliperInsertion):
		CaliperInsertion.setObjectName("CaliperInsertion")
		CaliperInsertion.resize(562, 821)
		self.csvCal_tableWidget = QtWidgets.QTableWidget(CaliperInsertion)
		self.csvCal_tableWidget.setGeometry(QtCore.QRect(20, 30, 381, 771))
		self.csvCal_tableWidget.setRowCount(1000)
		self.csvCal_tableWidget.setColumnCount(3)
		self.csvCal_tableWidget.setObjectName("csvCal_tableWidget")
		item = QtWidgets.QTableWidgetItem()
		self.csvCal_tableWidget.setHorizontalHeaderItem(0, item)
		item = QtWidgets.QTableWidgetItem()
		self.csvCal_tableWidget.setHorizontalHeaderItem(1, item)
		item = QtWidgets.QTableWidgetItem()
		self.csvCal_tableWidget.setHorizontalHeaderItem(2, item)
		self.csvCal_tableWidget.horizontalHeader().setVisible(True)
		self.csvAccept_pushButton = QtWidgets.QPushButton(CaliperInsertion)
		self.csvAccept_pushButton.setGeometry(QtCore.QRect(430, 40, 111, 41))
		font = QtGui.QFont()
		font.setPointSize(10)
		self.csvAccept_pushButton.setFont(font)
		self.csvAccept_pushButton.setObjectName("csvAccept_pushButton")
		self.csvClose_pushButton = QtWidgets.QPushButton(CaliperInsertion)
		self.csvClose_pushButton.setGeometry(QtCore.QRect(430, 160, 111, 41))
		font = QtGui.QFont()
		font.setPointSize(10)
		self.csvClose_pushButton.setFont(font)
		self.csvClose_pushButton.setObjectName("csvClose_pushButton")
		self.csvClearAll_pushButton = QtWidgets.QPushButton(CaliperInsertion)
		self.csvClearAll_pushButton.setGeometry(QtCore.QRect(430, 100, 111, 41))
		font = QtGui.QFont()
		font.setPointSize(10)
		self.csvClearAll_pushButton.setFont(font)
		self.csvClearAll_pushButton.setObjectName("csvClearAll_pushButton")

		self.retranslateUi(CaliperInsertion)
		self.csvClose_pushButton.clicked.connect(CaliperInsertion.close)
		QtCore.QMetaObject.connectSlotsByName(CaliperInsertion)

	def retranslateUi(self, CaliperInsertion):
		_translate = QtCore.QCoreApplication.translate
		CaliperInsertion.setWindowTitle(_translate("CaliperInsertion", "Caliper Insertion"))
		item = self.csvCal_tableWidget.horizontalHeaderItem(0)
		item.setText(_translate("CaliperInsertion", "MD top"))
		item = self.csvCal_tableWidget.horizontalHeaderItem(1)
		item.setText(_translate("CaliperInsertion", "MD bottom"))
		item = self.csvCal_tableWidget.horizontalHeaderItem(2)
		item.setText(_translate("CaliperInsertion", "Hole ID"))
		self.csvAccept_pushButton.setText(_translate("CaliperInsertion", "Accept"))
		self.csvClose_pushButton.setText(_translate("CaliperInsertion", "Close"))
		self.csvClearAll_pushButton.setText(_translate("CaliperInsertion", "Clear All"))

