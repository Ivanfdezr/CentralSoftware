# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SpacingSetup_Vst.ui'
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

class Ui_SpacingSetup(object):
	def setupUi(self, SpacingSetup):
		SpacingSetup.setObjectName(_fromUtf8("SpacingSetup"))
		SpacingSetup.resize(1417, 585)
		SpacingSetup.setWindowOpacity(1.0)
		self.ssCaliperMap_graphicsView = MatplotlibWidget(SpacingSetup)
		self.ssCaliperMap_graphicsView.setGeometry(QtCore.QRect(40, 40, 350, 450))
		self.ssCaliperMap_graphicsView.setObjectName(_fromUtf8("ssCaliperMap_graphicsView"))
		self.ssCentralizerLocations_tableWidget = QtGui.QTableWidget(SpacingSetup)
		self.ssCentralizerLocations_tableWidget.setGeometry(QtCore.QRect(880, 40, 511, 450))
		self.ssCentralizerLocations_tableWidget.setRowCount(1000)
		self.ssCentralizerLocations_tableWidget.setColumnCount(4)
		self.ssCentralizerLocations_tableWidget.setObjectName(_fromUtf8("ssCentralizerLocations_tableWidget"))
		item = QtGui.QTableWidgetItem()
		self.ssCentralizerLocations_tableWidget.setHorizontalHeaderItem(0, item)
		item = QtGui.QTableWidgetItem()
		self.ssCentralizerLocations_tableWidget.setHorizontalHeaderItem(1, item)
		item = QtGui.QTableWidgetItem()
		self.ssCentralizerLocations_tableWidget.setHorizontalHeaderItem(2, item)
		item = QtGui.QTableWidgetItem()
		self.ssCentralizerLocations_tableWidget.setHorizontalHeaderItem(3, item)
		self.ssCentralizerLocations_tableWidget.horizontalHeader().setDefaultSectionSize(110)
		self.ssCentralizerLocations_tableWidget.horizontalHeader().setMinimumSectionSize(30)
		self.ssAccept_pushButton = QtGui.QPushButton(SpacingSetup)
		self.ssAccept_pushButton.setGeometry(QtCore.QRect(1300, 530, 93, 30))
		font = QtGui.QFont()
		font.setPointSize(10)
		self.ssAccept_pushButton.setFont(font)
		self.ssAccept_pushButton.setObjectName(_fromUtf8("ssAccept_pushButton"))
		self.tabWidget = QtGui.QTabWidget(SpacingSetup)
		self.tabWidget.setGeometry(QtCore.QRect(410, 40, 450, 470))
		font = QtGui.QFont()
		font.setPointSize(10)
		font.setBold(False)
		font.setWeight(50)
		self.tabWidget.setFont(font)
		self.tabWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
		self.tabWidget.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
		self.tabWidget.setTabPosition(QtGui.QTabWidget.South)
		self.tabWidget.setTabShape(QtGui.QTabWidget.Triangular)
		self.tabWidget.setElideMode(QtCore.Qt.ElideNone)
		self.tabWidget.setDocumentMode(True)
		self.tabWidget.setTabsClosable(False)
		self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
		self.tab = QtGui.QWidget()
		self.tab.setObjectName(_fromUtf8("tab"))
		self.ssWellbore3D_graphicsView = Matplotlib3DWidget(self.tab)
		self.ssWellbore3D_graphicsView.setGeometry(QtCore.QRect(0, 0, 450, 450))
		self.ssWellbore3D_graphicsView.setObjectName(_fromUtf8("ssWellbore3D_graphicsView"))
		self.tabWidget.addTab(self.tab, _fromUtf8(""))
		self.tab_2 = QtGui.QWidget()
		self.tab_2.setObjectName(_fromUtf8("tab_2"))
		self.ssSOVisualization_graphicsView = MatplotlibWidget(self.tab_2)
		self.ssSOVisualization_graphicsView.setGeometry(QtCore.QRect(0, 0, 450, 450))
		self.ssSOVisualization_graphicsView.setObjectName(_fromUtf8("ssSOVisualization_graphicsView"))
		self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
		self.ssNextSpacing_tableWidget = QtGui.QTableWidget(SpacingSetup)
		self.ssNextSpacing_tableWidget.setGeometry(QtCore.QRect(40, 500, 351, 32))
		font = QtGui.QFont()
		font.setPointSize(10)
		self.ssNextSpacing_tableWidget.setFont(font)
		self.ssNextSpacing_tableWidget.setAutoFillBackground(False)
		self.ssNextSpacing_tableWidget.setFrameShadow(QtGui.QFrame.Sunken)
		self.ssNextSpacing_tableWidget.setColumnCount(1)
		self.ssNextSpacing_tableWidget.setObjectName(_fromUtf8("ssNextSpacing_tableWidget"))
		self.ssNextSpacing_tableWidget.setRowCount(1)
		item = QtGui.QTableWidgetItem()
		self.ssNextSpacing_tableWidget.setVerticalHeaderItem(0, item)
		self.ssNextSpacing_tableWidget.horizontalHeader().setVisible(False)
		self.ssNextSpacing_tableWidget.horizontalHeader().setCascadingSectionResizes(False)
		self.ssNextSpacing_tableWidget.horizontalHeader().setDefaultSectionSize(125)
		self.ssNextSpacing_tableWidget.horizontalHeader().setHighlightSections(True)
		self.ssNextSpacing_tableWidget.horizontalHeader().setSortIndicatorShown(False)
		self.ssNextSpacing_tableWidget.horizontalHeader().setStretchLastSection(False)
		self.ssNextSpacing_tableWidget.verticalHeader().setDefaultSectionSize(30)
		self.ssNextSpacing_tableWidget.verticalHeader().setMinimumSectionSize(28)
		self.ssNextSpacing_tableWidget.verticalHeader().setSortIndicatorShown(False)
		self.ssMeanSOatC_label = QtGui.QLabel(SpacingSetup)
		self.ssMeanSOatC_label.setGeometry(QtCore.QRect(880, 510, 331, 21))
		font = QtGui.QFont()
		font.setPointSize(9)
		font.setBold(True)
		font.setWeight(75)
		self.ssMeanSOatC_label.setFont(font)
		self.ssMeanSOatC_label.setObjectName(_fromUtf8("ssMeanSOatC_label"))
		self.ssMeanSOatM_label = QtGui.QLabel(SpacingSetup)
		self.ssMeanSOatM_label.setGeometry(QtCore.QRect(880, 540, 331, 21))
		font = QtGui.QFont()
		font.setPointSize(9)
		font.setBold(True)
		font.setWeight(75)
		self.ssMeanSOatM_label.setFont(font)
		self.ssMeanSOatM_label.setObjectName(_fromUtf8("ssMeanSOatM_label"))

		self.retranslateUi(SpacingSetup)
		self.tabWidget.setCurrentIndex(0)
		QtCore.QMetaObject.connectSlotsByName(SpacingSetup)

	def retranslateUi(self, SpacingSetup):
		SpacingSetup.setWindowTitle(_translate("SpacingSetup", "Centralizers Spacing Setup", None))
		item = self.ssCentralizerLocations_tableWidget.horizontalHeaderItem(0)
		item.setText(_translate("SpacingSetup", "MD", None))
		item = self.ssCentralizerLocations_tableWidget.horizontalHeaderItem(1)
		item.setText(_translate("SpacingSetup", "Inc", None))
		item = self.ssCentralizerLocations_tableWidget.horizontalHeaderItem(2)
		item.setText(_translate("SpacingSetup", "SO at\\ncentralizer", None))
		item = self.ssCentralizerLocations_tableWidget.horizontalHeaderItem(3)
		item.setText(_translate("SpacingSetup", "SO at\\nmidspan", None))
		self.ssAccept_pushButton.setText(_translate("SpacingSetup", "Accept", None))
		self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("SpacingSetup", "3D View", None))
		self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("SpacingSetup", "SO Visualization", None))
		self.ssNextSpacing_tableWidget.setSortingEnabled(False)
		item = self.ssNextSpacing_tableWidget.verticalHeaderItem(0)
		item.setText(_translate("SpacingSetup", "Next stage spacing           ", None))
		self.ssMeanSOatC_label.setText(_translate("SpacingSetup", "Mean SO at centralizers: ", None))
		self.ssMeanSOatM_label.setText(_translate("SpacingSetup", "Mean SO at midspan:", None))

from matplotlibwidget import Matplotlib3DWidget, MatplotlibWidget
