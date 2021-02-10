# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CentralizerDatabase_Vst.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_CentralizerDatabase(object):
	def setupUi(self, CentralizerDatabase):
		CentralizerDatabase.setObjectName("CentralizerDatabase")
		CentralizerDatabase.resize(996, 535)
		font = QtGui.QFont()
		font.setPointSize(10)
		CentralizerDatabase.setFont(font)
		self.label = QtWidgets.QLabel(CentralizerDatabase)
		self.label.setGeometry(QtCore.QRect(20, 20, 151, 16))
		font = QtGui.QFont()
		font.setPointSize(10)
		self.label.setFont(font)
		self.label.setObjectName("label")
		self.CDBVendor_comboBox = QtWidgets.QComboBox(CentralizerDatabase)
		self.CDBVendor_comboBox.setGeometry(QtCore.QRect(180, 14, 341, 27))
		font = QtGui.QFont()
		font.setPointSize(10)
		self.CDBVendor_comboBox.setFont(font)
		self.CDBVendor_comboBox.setObjectName("CDBVendor_comboBox")
		self.CDBEditCentralizerDB_pushButton = QtWidgets.QPushButton(CentralizerDatabase)
		self.CDBEditCentralizerDB_pushButton.setGeometry(QtCore.QRect(540, 13, 251, 28))
		self.CDBEditCentralizerDB_pushButton.setObjectName("CDBEditCentralizerDB_pushButton")
		self.label_2 = QtWidgets.QLabel(CentralizerDatabase)
		self.label_2.setGeometry(QtCore.QRect(20, 55, 91, 21))
		self.label_2.setObjectName("label_2")
		self.CDBCasingOD_listWidget = QtWidgets.QListWidget(CentralizerDatabase)
		self.CDBCasingOD_listWidget.setGeometry(QtCore.QRect(20, 90, 121, 431))
		self.CDBCasingOD_listWidget.setObjectName("CDBCasingOD_listWidget")
		self.CDB_tabWidget = QtWidgets.QTabWidget(CentralizerDatabase)
		self.CDB_tabWidget.setGeometry(QtCore.QRect(150, 60, 821, 462))
		self.CDB_tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
		self.CDB_tabWidget.setObjectName("CDB_tabWidget")
		self.tab = QtWidgets.QWidget()
		self.tab.setObjectName("tab")
		self.CDBBowSpring_tableWidget = QtWidgets.QTableWidget(self.tab)
		self.CDBBowSpring_tableWidget.setGeometry(QtCore.QRect(2, 3, 810, 425))
		self.CDBBowSpring_tableWidget.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
		self.CDBBowSpring_tableWidget.setGridStyle(QtCore.Qt.SolidLine)
		self.CDBBowSpring_tableWidget.setWordWrap(True)
		self.CDBBowSpring_tableWidget.setCornerButtonEnabled(True)
		self.CDBBowSpring_tableWidget.setRowCount(200)
		self.CDBBowSpring_tableWidget.setColumnCount(16)
		self.CDBBowSpring_tableWidget.setObjectName("CDBBowSpring_tableWidget")
		self.CDB_tabWidget.addTab(self.tab, "")
		self.tab_2 = QtWidgets.QWidget()
		self.tab_2.setObjectName("tab_2")
		self.CDBResin_tableWidget = QtWidgets.QTableWidget(self.tab_2)
		self.CDBResin_tableWidget.setGeometry(QtCore.QRect(2, 3, 810, 425))
		self.CDBResin_tableWidget.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
		self.CDBResin_tableWidget.setRowCount(200)
		self.CDBResin_tableWidget.setColumnCount(14)
		self.CDBResin_tableWidget.setObjectName("CDBResin_tableWidget")
		self.CDB_tabWidget.addTab(self.tab_2, "")
		self.CDBAccept_pushButton = QtWidgets.QPushButton(CentralizerDatabase)
		self.CDBAccept_pushButton.setGeometry(QtCore.QRect(870, 18, 93, 28))
		self.CDBAccept_pushButton.setObjectName("CDBAccept_pushButton")
		self.CDBClose_pushButton = QtWidgets.QPushButton(CentralizerDatabase)
		self.CDBClose_pushButton.setGeometry(QtCore.QRect(870, 50, 93, 28))
		self.CDBClose_pushButton.setObjectName("CDBClose_pushButton")

		self.retranslateUi(CentralizerDatabase)
		self.CDB_tabWidget.setCurrentIndex(1)
		self.CDBClose_pushButton.clicked.connect(CentralizerDatabase.close)
		QtCore.QMetaObject.connectSlotsByName(CentralizerDatabase)

	def retranslateUi(self, CentralizerDatabase):
		_translate = QtCore.QCoreApplication.translate
		CentralizerDatabase.setWindowTitle(_translate("CentralizerDatabase", "Centralizer Database"))
		self.label.setText(_translate("CentralizerDatabase", "Centralizer vendor:"))
		self.CDBEditCentralizerDB_pushButton.setText(_translate("CentralizerDatabase", "Edit Centralizer Database..."))
		self.label_2.setText(_translate("CentralizerDatabase", "Casing OD:"))
		self.CDB_tabWidget.setTabText(self.CDB_tabWidget.indexOf(self.tab), _translate("CentralizerDatabase", "Bow Spring"))
		self.CDB_tabWidget.setTabText(self.CDB_tabWidget.indexOf(self.tab_2), _translate("CentralizerDatabase", "Resin"))
		self.CDBAccept_pushButton.setText(_translate("CentralizerDatabase", "Accept"))
		self.CDBClose_pushButton.setText(_translate("CentralizerDatabase", "Close"))

