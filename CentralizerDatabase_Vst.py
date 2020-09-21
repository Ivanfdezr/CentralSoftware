# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CentralizerDatabase_Vst.ui'
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

class Ui_CentralizerDatabase(object):
	def setupUi(self, CentralizerDatabase):
		CentralizerDatabase.setObjectName(_fromUtf8("CentralizerDatabase"))
		CentralizerDatabase.resize(996, 535)
		font = QtGui.QFont()
		font.setPointSize(10)
		CentralizerDatabase.setFont(font)
		self.label = QtGui.QLabel(CentralizerDatabase)
		self.label.setGeometry(QtCore.QRect(20, 20, 151, 16))
		font = QtGui.QFont()
		font.setPointSize(10)
		self.label.setFont(font)
		self.label.setObjectName(_fromUtf8("label"))
		self.CDBVendor_comboBox = QtGui.QComboBox(CentralizerDatabase)
		self.CDBVendor_comboBox.setGeometry(QtCore.QRect(180, 14, 341, 27))
		font = QtGui.QFont()
		font.setPointSize(10)
		self.CDBVendor_comboBox.setFont(font)
		self.CDBVendor_comboBox.setObjectName(_fromUtf8("CDBVendor_comboBox"))
		self.CDBEditCentralizerDB_pushButton = QtGui.QPushButton(CentralizerDatabase)
		self.CDBEditCentralizerDB_pushButton.setGeometry(QtCore.QRect(540, 13, 251, 28))
		self.CDBEditCentralizerDB_pushButton.setObjectName(_fromUtf8("CDBEditCentralizerDB_pushButton"))
		self.label_2 = QtGui.QLabel(CentralizerDatabase)
		self.label_2.setGeometry(QtCore.QRect(20, 55, 91, 21))
		self.label_2.setObjectName(_fromUtf8("label_2"))
		self.CDBCasingOD_listWidget = QtGui.QListWidget(CentralizerDatabase)
		self.CDBCasingOD_listWidget.setGeometry(QtCore.QRect(20, 90, 121, 431))
		self.CDBCasingOD_listWidget.setObjectName(_fromUtf8("CDBCasingOD_listWidget"))
		self.CDB_tabWidget = QtGui.QTabWidget(CentralizerDatabase)
		self.CDB_tabWidget.setGeometry(QtCore.QRect(150, 60, 821, 462))
		self.CDB_tabWidget.setTabShape(QtGui.QTabWidget.Rounded)
		self.CDB_tabWidget.setObjectName(_fromUtf8("CDB_tabWidget"))
		self.tab = QtGui.QWidget()
		self.tab.setObjectName(_fromUtf8("tab"))
		self.CDBBowSpring_tableWidget = QtGui.QTableWidget(self.tab)
		self.CDBBowSpring_tableWidget.setGeometry(QtCore.QRect(2, 3, 810, 425))
		self.CDBBowSpring_tableWidget.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
		self.CDBBowSpring_tableWidget.setGridStyle(QtCore.Qt.SolidLine)
		self.CDBBowSpring_tableWidget.setWordWrap(True)
		self.CDBBowSpring_tableWidget.setCornerButtonEnabled(True)
		self.CDBBowSpring_tableWidget.setRowCount(200)
		self.CDBBowSpring_tableWidget.setColumnCount(16)
		self.CDBBowSpring_tableWidget.setObjectName(_fromUtf8("CDBBowSpring_tableWidget"))
		self.CDB_tabWidget.addTab(self.tab, _fromUtf8(""))
		self.tab_2 = QtGui.QWidget()
		self.tab_2.setObjectName(_fromUtf8("tab_2"))
		self.CDBResin_tableWidget = QtGui.QTableWidget(self.tab_2)
		self.CDBResin_tableWidget.setGeometry(QtCore.QRect(2, 3, 810, 425))
		self.CDBResin_tableWidget.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
		self.CDBResin_tableWidget.setRowCount(200)
		self.CDBResin_tableWidget.setColumnCount(14)
		self.CDBResin_tableWidget.setObjectName(_fromUtf8("CDBResin_tableWidget"))
		self.CDB_tabWidget.addTab(self.tab_2, _fromUtf8(""))
		self.CDBAccept_pushButton = QtGui.QPushButton(CentralizerDatabase)
		self.CDBAccept_pushButton.setGeometry(QtCore.QRect(870, 18, 93, 28))
		self.CDBAccept_pushButton.setObjectName(_fromUtf8("CDBAccept_pushButton"))
		self.CDBClose_pushButton = QtGui.QPushButton(CentralizerDatabase)
		self.CDBClose_pushButton.setGeometry(QtCore.QRect(870, 50, 93, 28))
		self.CDBClose_pushButton.setObjectName(_fromUtf8("CDBClose_pushButton"))

		self.retranslateUi(CentralizerDatabase)
		self.CDB_tabWidget.setCurrentIndex(1)
		QtCore.QObject.connect(self.CDBClose_pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), CentralizerDatabase.close)
		QtCore.QMetaObject.connectSlotsByName(CentralizerDatabase)

	def retranslateUi(self, CentralizerDatabase):
		CentralizerDatabase.setWindowTitle(_translate("CentralizerDatabase", "Centralizer Database", None))
		self.label.setText(_translate("CentralizerDatabase", "Centralizer vendor:", None))
		self.CDBEditCentralizerDB_pushButton.setText(_translate("CentralizerDatabase", "Edit Centralizer Database...", None))
		self.label_2.setText(_translate("CentralizerDatabase", "Casing OD:", None))
		self.CDB_tabWidget.setTabText(self.CDB_tabWidget.indexOf(self.tab), _translate("CentralizerDatabase", "Bow Spring", None))
		self.CDB_tabWidget.setTabText(self.CDB_tabWidget.indexOf(self.tab_2), _translate("CentralizerDatabase", "Resin", None))
		self.CDBAccept_pushButton.setText(_translate("CentralizerDatabase", "Accept", None))
		self.CDBClose_pushButton.setText(_translate("CentralizerDatabase", "Close", None))

