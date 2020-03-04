# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CSV_Vst.ui'
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

class Ui_Dialog(object):
	def setupUi(self, Dialog):
		Dialog.setObjectName(_fromUtf8("Dialog"))
		Dialog.resize(539, 821)
		self.csv_buttonBox = QtGui.QDialogButtonBox(Dialog)
		self.csv_buttonBox.setGeometry(QtCore.QRect(410, 30, 101, 81))
		self.csv_buttonBox.setOrientation(QtCore.Qt.Vertical)
		self.csv_buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
		self.csv_buttonBox.setObjectName(_fromUtf8("csv_buttonBox"))
		self.csvCal_tableWidget = QtGui.QTableWidget(Dialog)
		self.csvCal_tableWidget.setGeometry(QtCore.QRect(20, 30, 371, 771))
		self.csvCal_tableWidget.setRowCount(1000)
		self.csvCal_tableWidget.setColumnCount(3)
		self.csvCal_tableWidget.setObjectName(_fromUtf8("csvCal_tableWidget"))

		self.retranslateUi(Dialog)
		QtCore.QObject.connect(self.csv_buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
		QtCore.QObject.connect(self.csv_buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
		QtCore.QMetaObject.connectSlotsByName(Dialog)

	def retranslateUi(self, Dialog):
		Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))

