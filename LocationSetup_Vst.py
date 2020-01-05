# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LocationSetup_Vst.ui'
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

class Ui_LocationSetup(object):
	def setupUi(self, LocationSetup):
		LocationSetup.setObjectName(_fromUtf8("LocationSetup"))
		LocationSetup.resize(1316, 567)
		LocationSetup.setWindowOpacity(1.0)
		self.lsCaliperMap_graphicsView = MatplotlibWidget(LocationSetup)
		self.lsCaliperMap_graphicsView.setGeometry(QtCore.QRect(40, 40, 350, 450))
		self.lsCaliperMap_graphicsView.setObjectName(_fromUtf8("lsCaliperMap_graphicsView"))
		self.lsWellbore3D_graphicsView = Matplotlib3DWidget(LocationSetup)
		self.lsWellbore3D_graphicsView.setGeometry(QtCore.QRect(410, 40, 450, 450))
		self.lsWellbore3D_graphicsView.setObjectName(_fromUtf8("lsWellbore3D_graphicsView"))
		self.lsCentralizerLocations_tableWidget = QtGui.QTableWidget(LocationSetup)
		self.lsCentralizerLocations_tableWidget.setGeometry(QtCore.QRect(880, 40, 400, 450))
		self.lsCentralizerLocations_tableWidget.setRowCount(1000)
		self.lsCentralizerLocations_tableWidget.setColumnCount(4)
		self.lsCentralizerLocations_tableWidget.setObjectName(_fromUtf8("lsCentralizerLocations_tableWidget"))
		item = QtGui.QTableWidgetItem()
		self.lsCentralizerLocations_tableWidget.setHorizontalHeaderItem(0, item)
		item = QtGui.QTableWidgetItem()
		self.lsCentralizerLocations_tableWidget.setHorizontalHeaderItem(1, item)
		item = QtGui.QTableWidgetItem()
		self.lsCentralizerLocations_tableWidget.setHorizontalHeaderItem(2, item)
		item = QtGui.QTableWidgetItem()
		self.lsCentralizerLocations_tableWidget.setHorizontalHeaderItem(3, item)
		self.lsCentralizerLocations_tableWidget.horizontalHeader().setDefaultSectionSize(110)
		self.lsCentralizerLocations_tableWidget.horizontalHeader().setMinimumSectionSize(30)
		self.lsAccept_pushButton = QtGui.QPushButton(LocationSetup)
		self.lsAccept_pushButton.setGeometry(QtCore.QRect(1190, 510, 93, 30))
		font = QtGui.QFont()
		font.setPointSize(10)
		self.lsAccept_pushButton.setFont(font)
		self.lsAccept_pushButton.setObjectName(_fromUtf8("lsAccept_pushButton"))

		self.retranslateUi(LocationSetup)
		QtCore.QMetaObject.connectSlotsByName(LocationSetup)

	def retranslateUi(self, LocationSetup):
		LocationSetup.setWindowTitle(_translate("LocationSetup", "Centralizers Location Setup", None))
		item = self.lsCentralizerLocations_tableWidget.horizontalHeaderItem(0)
		item.setText(_translate("LocationSetup", "MD", None))
		item = self.lsCentralizerLocations_tableWidget.horizontalHeaderItem(1)
		item.setText(_translate("LocationSetup", "Inc", None))
		item = self.lsCentralizerLocations_tableWidget.horizontalHeaderItem(2)
		item.setText(_translate("LocationSetup", "SO at\\ncentralizer", None))
		item = self.lsCentralizerLocations_tableWidget.horizontalHeaderItem(3)
		item.setText(_translate("LocationSetup", "SO at\\nmidspan", None))
		self.lsAccept_pushButton.setText(_translate("LocationSetup", "Accept", None))

from matplotlibwidget import Matplotlib3DWidget, MatplotlibWidget
