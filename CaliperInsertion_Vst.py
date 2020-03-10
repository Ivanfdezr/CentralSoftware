# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CaliperInsertion_Vst.ui'
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

class Ui_CaliperInsertion(object):
	def setupUi(self, CaliperInsertion):
		CaliperInsertion.setObjectName(_fromUtf8("CaliperInsertion"))
		CaliperInsertion.resize(562, 821)
		self.csvCal_tableWidget = QtGui.QTableWidget(CaliperInsertion)
		self.csvCal_tableWidget.setGeometry(QtCore.QRect(20, 30, 381, 771))
		self.csvCal_tableWidget.setRowCount(1000)
		self.csvCal_tableWidget.setColumnCount(3)
		self.csvCal_tableWidget.setObjectName(_fromUtf8("csvCal_tableWidget"))
		item = QtGui.QTableWidgetItem()
		self.csvCal_tableWidget.setHorizontalHeaderItem(0, item)
		item = QtGui.QTableWidgetItem()
		self.csvCal_tableWidget.setHorizontalHeaderItem(1, item)
		item = QtGui.QTableWidgetItem()
		self.csvCal_tableWidget.setHorizontalHeaderItem(2, item)
		self.csvCal_tableWidget.horizontalHeader().setVisible(True)
		self.csvAccept_pushButton = QtGui.QPushButton(CaliperInsertion)
		self.csvAccept_pushButton.setGeometry(QtCore.QRect(430, 40, 111, 41))
		font = QtGui.QFont()
		font.setPointSize(10)
		self.csvAccept_pushButton.setFont(font)
		self.csvAccept_pushButton.setObjectName(_fromUtf8("csvAccept_pushButton"))
		self.csvClose_pushButton = QtGui.QPushButton(CaliperInsertion)
		self.csvClose_pushButton.setGeometry(QtCore.QRect(430, 160, 111, 41))
		font = QtGui.QFont()
		font.setPointSize(10)
		self.csvClose_pushButton.setFont(font)
		self.csvClose_pushButton.setObjectName(_fromUtf8("csvClose_pushButton"))
		self.csvClearAll_pushButton = QtGui.QPushButton(CaliperInsertion)
		self.csvClearAll_pushButton.setGeometry(QtCore.QRect(430, 100, 111, 41))
		font = QtGui.QFont()
		font.setPointSize(10)
		self.csvClearAll_pushButton.setFont(font)
		self.csvClearAll_pushButton.setObjectName(_fromUtf8("csvClearAll_pushButton"))

		self.retranslateUi(CaliperInsertion)
		QtCore.QObject.connect(self.csvClose_pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), CaliperInsertion.close)
		QtCore.QMetaObject.connectSlotsByName(CaliperInsertion)

	def retranslateUi(self, CaliperInsertion):
		CaliperInsertion.setWindowTitle(_translate("CaliperInsertion", "Caliper Insertion", None))
		item = self.csvCal_tableWidget.horizontalHeaderItem(0)
		item.setText(_translate("CaliperInsertion", "MD top", None))
		item = self.csvCal_tableWidget.horizontalHeaderItem(1)
		item.setText(_translate("CaliperInsertion", "MD bottom", None))
		item = self.csvCal_tableWidget.horizontalHeaderItem(2)
		item.setText(_translate("CaliperInsertion", "Hole ID", None))
		self.csvAccept_pushButton.setText(_translate("CaliperInsertion", "Accept", None))
		self.csvClose_pushButton.setText(_translate("CaliperInsertion", "Close", None))
		self.csvClearAll_pushButton.setText(_translate("CaliperInsertion", "Clear All", None))

