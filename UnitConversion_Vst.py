# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UnitConversion_Vst.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
	def setupUi(self, Dialog):
		Dialog.setObjectName("Dialog")
		Dialog.resize(650, 229)
		font = QtGui.QFont()
		font.setPointSize(10)
		Dialog.setFont(font)
		self.comboBox = QtWidgets.QComboBox(Dialog)
		self.comboBox.setGeometry(QtCore.QRect(360, 30, 271, 31))
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
		self.comboBox.setSizePolicy(sizePolicy)
		self.comboBox.setObjectName("comboBox")
		self.label = QtWidgets.QLabel(Dialog)
		self.label.setGeometry(QtCore.QRect(230, 32, 121, 21))
		font = QtGui.QFont()
		font.setPointSize(10)
		self.label.setFont(font)
		self.label.setObjectName("label")
		self.pushButton = QtWidgets.QPushButton(Dialog)
		self.pushButton.setGeometry(QtCore.QRect(280, 180, 93, 31))
		self.pushButton.setObjectName("pushButton")
		self.comboBox_4 = QtWidgets.QComboBox(Dialog)
		self.comboBox_4.setGeometry(QtCore.QRect(543, 140, 87, 27))
		self.comboBox_4.setObjectName("comboBox_4")
		self.label_2 = QtWidgets.QLabel(Dialog)
		self.label_2.setGeometry(QtCore.QRect(416, 133, 121, 39))
		self.label_2.setObjectName("label_2")
		self.comboBox_3 = QtWidgets.QComboBox(Dialog)
		self.comboBox_3.setGeometry(QtCore.QRect(530, 90, 100, 27))
		self.comboBox_3.setObjectName("comboBox_3")
		self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
		self.lineEdit_2.setGeometry(QtCore.QRect(410, 90, 110, 27))
		self.lineEdit_2.setObjectName("lineEdit_2")
		self.comboBox_2 = QtWidgets.QComboBox(Dialog)
		self.comboBox_2.setGeometry(QtCore.QRect(140, 90, 100, 27))
		self.comboBox_2.setObjectName("comboBox_2")
		self.lineEdit = QtWidgets.QLineEdit(Dialog)
		self.lineEdit.setGeometry(QtCore.QRect(20, 90, 110, 27))
		self.lineEdit.setObjectName("lineEdit")
		self.convert = QtWidgets.QPushButton(Dialog)
		self.convert.setGeometry(QtCore.QRect(270, 90, 111, 30))
		self.convert.setAutoDefault(True)
		self.convert.setDefault(False)
		self.convert.setFlat(False)
		self.convert.setObjectName("convert")

		self.retranslateUi(Dialog)
		self.pushButton.clicked.connect(Dialog.close)
		QtCore.QMetaObject.connectSlotsByName(Dialog)

	def retranslateUi(self, Dialog):
		_translate = QtCore.QCoreApplication.translate
		Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
		self.label.setText(_translate("Dialog", "Parameter type:"))
		self.pushButton.setText(_translate("Dialog", "Close"))
		self.label_2.setText(_translate("Dialog", "Decimal places:"))
		self.convert.setText(_translate("Dialog", "calculate"))

