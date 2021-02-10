# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TubularDatabase_Vst.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TubularDatabase(object):
	def setupUi(self, TubularDatabase):
		TubularDatabase.setObjectName("TubularDatabase")
		TubularDatabase.resize(996, 535)
		font = QtGui.QFont()
		font.setPointSize(10)
		TubularDatabase.setFont(font)
		self.TDBPipeOD_label = QtWidgets.QLabel(TubularDatabase)
		self.TDBPipeOD_label.setGeometry(QtCore.QRect(20, 50, 81, 20))
		self.TDBPipeOD_label.setObjectName("TDBPipeOD_label")
		self.TDBPipeOD_listWidget = QtWidgets.QListWidget(TubularDatabase)
		self.TDBPipeOD_listWidget.setGeometry(QtCore.QRect(20, 80, 101, 441))
		self.TDBPipeOD_listWidget.setFrameShape(QtWidgets.QFrame.Panel)
		self.TDBPipeOD_listWidget.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.TDBPipeOD_listWidget.setObjectName("TDBPipeOD_listWidget")
		self.TDBAccept_pushButton = QtWidgets.QPushButton(TubularDatabase)
		self.TDBAccept_pushButton.setGeometry(QtCore.QRect(880, 12, 93, 28))
		self.TDBAccept_pushButton.setObjectName("TDBAccept_pushButton")
		self.TDBClose_pushButton = QtWidgets.QPushButton(TubularDatabase)
		self.TDBClose_pushButton.setGeometry(QtCore.QRect(880, 44, 93, 28))
		self.TDBClose_pushButton.setObjectName("TDBClose_pushButton")
		self.TDB_tableWidget = QtWidgets.QTableWidget(TubularDatabase)
		self.TDB_tableWidget.setGeometry(QtCore.QRect(130, 80, 851, 441))
		self.TDB_tableWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
		self.TDB_tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.AnyKeyPressed|QtWidgets.QAbstractItemView.DoubleClicked|QtWidgets.QAbstractItemView.EditKeyPressed|QtWidgets.QAbstractItemView.SelectedClicked)
		self.TDB_tableWidget.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
		self.TDB_tableWidget.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
		self.TDB_tableWidget.setRowCount(200)
		self.TDB_tableWidget.setColumnCount(28)
		self.TDB_tableWidget.setObjectName("TDB_tableWidget")
		self.TDB_tableWidget.horizontalHeader().setCascadingSectionResizes(False)
		self.TDB_tableWidget.horizontalHeader().setDefaultSectionSize(120)
		self.TDB_tableWidget.horizontalHeader().setStretchLastSection(False)
		self.TDB_tableWidget.verticalHeader().setCascadingSectionResizes(False)
		self.TDB_tableWidget.verticalHeader().setStretchLastSection(False)

		self.retranslateUi(TubularDatabase)
		self.TDBClose_pushButton.clicked.connect(TubularDatabase.close)
		QtCore.QMetaObject.connectSlotsByName(TubularDatabase)

	def retranslateUi(self, TubularDatabase):
		_translate = QtCore.QCoreApplication.translate
		TubularDatabase.setWindowTitle(_translate("TubularDatabase", "Tubular Database"))
		self.TDBPipeOD_label.setText(_translate("TubularDatabase", "Pipe OD: "))
		self.TDBAccept_pushButton.setText(_translate("TubularDatabase", "Insert"))
		self.TDBClose_pushButton.setText(_translate("TubularDatabase", "Close"))
		self.TDB_tableWidget.setSortingEnabled(True)

