# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UnitConversion_Vst.ui'
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
		Dialog.resize(650, 229)
		font = QtGui.QFont()
		font.setPointSize(10)
		Dialog.setFont(font)
		self.comboBox = QtGui.QComboBox(Dialog)
		self.comboBox.setGeometry(QtCore.QRect(360, 30, 271, 31))
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
		self.comboBox.setSizePolicy(sizePolicy)
		self.comboBox.setObjectName(_fromUtf8("comboBox"))
		self.label = QtGui.QLabel(Dialog)
		self.label.setGeometry(QtCore.QRect(230, 32, 121, 21))
		font = QtGui.QFont()
		font.setPointSize(10)
		self.label.setFont(font)
		self.label.setObjectName(_fromUtf8("label"))
		self.pushButton = QtGui.QPushButton(Dialog)
		self.pushButton.setGeometry(QtCore.QRect(280, 180, 93, 31))
		self.pushButton.setObjectName(_fromUtf8("pushButton"))
		self.comboBox_4 = QtGui.QComboBox(Dialog)
		self.comboBox_4.setGeometry(QtCore.QRect(543, 140, 87, 27))
		self.comboBox_4.setObjectName(_fromUtf8("comboBox_4"))
		self.label_2 = QtGui.QLabel(Dialog)
		self.label_2.setGeometry(QtCore.QRect(416, 133, 121, 39))
		self.label_2.setObjectName(_fromUtf8("label_2"))
		self.comboBox_3 = QtGui.QComboBox(Dialog)
		self.comboBox_3.setGeometry(QtCore.QRect(530, 90, 100, 27))
		self.comboBox_3.setObjectName(_fromUtf8("comboBox_3"))
		self.lineEdit_2 = QtGui.QLineEdit(Dialog)
		self.lineEdit_2.setGeometry(QtCore.QRect(410, 90, 110, 27))
		self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
		self.comboBox_2 = QtGui.QComboBox(Dialog)
		self.comboBox_2.setGeometry(QtCore.QRect(140, 90, 100, 27))
		self.comboBox_2.setObjectName(_fromUtf8("comboBox_2"))
		self.lineEdit = QtGui.QLineEdit(Dialog)
		self.lineEdit.setGeometry(QtCore.QRect(20, 90, 110, 27))
		self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
		self.convert = QtGui.QPushButton(Dialog)
		self.convert.setGeometry(QtCore.QRect(270, 90, 111, 30))
		self.convert.setAutoDefault(True)
		self.convert.setDefault(False)
		self.convert.setFlat(False)
		self.convert.setObjectName(_fromUtf8("convert"))

		self.retranslateUi(Dialog)
		QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.close)
		QtCore.QMetaObject.connectSlotsByName(Dialog)

	def retranslateUi(self, Dialog):
		Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
		self.label.setText(_translate("Dialog", "Parameter type:", None))
		self.pushButton.setText(_translate("Dialog", "Close", None))
		self.label_2.setText(_translate("Dialog", "Decimal places:", None))
		self.convert.setText(_translate("Dialog", "calculate", None))

