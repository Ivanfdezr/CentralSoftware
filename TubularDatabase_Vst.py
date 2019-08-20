# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TubularDatabase_Vst.ui'
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

class Ui_TubularDatabase(object):
	def setupUi(self, TubularDatabase):
		TubularDatabase.setObjectName(_fromUtf8("TubularDatabase"))
		TubularDatabase.resize(996, 535)
		font = QtGui.QFont()
		font.setPointSize(10)
		TubularDatabase.setFont(font)
		self.TDBPipes_label = QtGui.QLabel(TubularDatabase)
		self.TDBPipes_label.setGeometry(QtCore.QRect(20, 16, 81, 20))
		font = QtGui.QFont()
		font.setPointSize(10)
		self.TDBPipes_label.setFont(font)
		self.TDBPipes_label.setObjectName(_fromUtf8("TDBPipes_label"))
		self.TDBPipes_comboBox = QtGui.QComboBox(TubularDatabase)
		self.TDBPipes_comboBox.setGeometry(QtCore.QRect(120, 15, 341, 27))
		self.TDBPipes_comboBox.setObjectName(_fromUtf8("TDBPipes_comboBox"))
		self.TDBPipeOD_label = QtGui.QLabel(TubularDatabase)
		self.TDBPipeOD_label.setGeometry(QtCore.QRect(20, 50, 81, 20))
		self.TDBPipeOD_label.setObjectName(_fromUtf8("TDBPipeOD_label"))
		self.TDBPipeOD_listWidget = QtGui.QListWidget(TubularDatabase)
		self.TDBPipeOD_listWidget.setGeometry(QtCore.QRect(20, 80, 101, 441))
		self.TDBPipeOD_listWidget.setFrameShape(QtGui.QFrame.Panel)
		self.TDBPipeOD_listWidget.setFrameShadow(QtGui.QFrame.Sunken)
		self.TDBPipeOD_listWidget.setObjectName(_fromUtf8("TDBPipeOD_listWidget"))
		self.TDBAccept_pushButton = QtGui.QPushButton(TubularDatabase)
		self.TDBAccept_pushButton.setGeometry(QtCore.QRect(880, 12, 93, 28))
		self.TDBAccept_pushButton.setObjectName(_fromUtf8("TDBAccept_pushButton"))
		self.TDBClose_pushButton = QtGui.QPushButton(TubularDatabase)
		self.TDBClose_pushButton.setGeometry(QtCore.QRect(880, 44, 93, 28))
		self.TDBClose_pushButton.setObjectName(_fromUtf8("TDBClose_pushButton"))
		self.TDB_tableWidget = QtGui.QTableWidget(TubularDatabase)
		self.TDB_tableWidget.setGeometry(QtCore.QRect(130, 80, 851, 441))
		self.TDB_tableWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
		self.TDB_tableWidget.setEditTriggers(QtGui.QAbstractItemView.AnyKeyPressed|QtGui.QAbstractItemView.DoubleClicked|QtGui.QAbstractItemView.EditKeyPressed|QtGui.QAbstractItemView.SelectedClicked)
		self.TDB_tableWidget.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
		self.TDB_tableWidget.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
		self.TDB_tableWidget.setRowCount(200)
		self.TDB_tableWidget.setColumnCount(29)
		self.TDB_tableWidget.setObjectName(_fromUtf8("TDB_tableWidget"))
		self.TDB_tableWidget.horizontalHeader().setCascadingSectionResizes(False)
		self.TDB_tableWidget.horizontalHeader().setDefaultSectionSize(120)
		self.TDB_tableWidget.horizontalHeader().setStretchLastSection(False)
		self.TDB_tableWidget.verticalHeader().setCascadingSectionResizes(False)
		self.TDB_tableWidget.verticalHeader().setStretchLastSection(False)

		self.retranslateUi(TubularDatabase)
		QtCore.QObject.connect(self.TDBClose_pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), TubularDatabase.close)
		QtCore.QMetaObject.connectSlotsByName(TubularDatabase)

	def retranslateUi(self, TubularDatabase):
		TubularDatabase.setWindowTitle(_translate("TubularDatabase", "Tubular Database", None))
		self.TDBPipes_label.setText(_translate("TubularDatabase", "Pipe type:", None))
		self.TDBPipeOD_label.setText(_translate("TubularDatabase", "Pipe OD: ", None))
		self.TDBAccept_pushButton.setText(_translate("TubularDatabase", "Insert", None))
		self.TDBClose_pushButton.setText(_translate("TubularDatabase", "Close", None))
		self.TDB_tableWidget.setSortingEnabled(True)

