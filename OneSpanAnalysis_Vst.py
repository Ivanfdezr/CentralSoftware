# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'OneSpanAnalysis_Vst.ui'
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

class Ui_OneSpanAnalysis(object):
	def setupUi(self, OneSpanAnalysis):
		OneSpanAnalysis.setObjectName(_fromUtf8("OneSpanAnalysis"))
		OneSpanAnalysis.resize(1097, 852)
		self.groupBox = QtGui.QGroupBox(OneSpanAnalysis)
		self.groupBox.setGeometry(QtCore.QRect(10, 18, 401, 801))
		font = QtGui.QFont()
		font.setPointSize(10)
		self.groupBox.setFont(font)
		self.groupBox.setTitle(_fromUtf8(""))
		self.groupBox.setObjectName(_fromUtf8("groupBox"))
		self.osaCasing_tableWidget = QtGui.QTableWidget(self.groupBox)
		self.osaCasing_tableWidget.setGeometry(QtCore.QRect(20, 59, 340, 127))
		font = QtGui.QFont()
		font.setPointSize(9)
		self.osaCasing_tableWidget.setFont(font)
		self.osaCasing_tableWidget.setAutoFillBackground(False)
		self.osaCasing_tableWidget.setFrameShadow(QtGui.QFrame.Sunken)
		self.osaCasing_tableWidget.setColumnCount(1)
		self.osaCasing_tableWidget.setObjectName(_fromUtf8("osaCasing_tableWidget"))
		self.osaCasing_tableWidget.setRowCount(5)
		item = QtGui.QTableWidgetItem()
		self.osaCasing_tableWidget.setVerticalHeaderItem(0, item)
		item = QtGui.QTableWidgetItem()
		self.osaCasing_tableWidget.setVerticalHeaderItem(1, item)
		item = QtGui.QTableWidgetItem()
		self.osaCasing_tableWidget.setVerticalHeaderItem(2, item)
		item = QtGui.QTableWidgetItem()
		self.osaCasing_tableWidget.setVerticalHeaderItem(3, item)
		item = QtGui.QTableWidgetItem()
		self.osaCasing_tableWidget.setVerticalHeaderItem(4, item)
		self.osaCasing_tableWidget.horizontalHeader().setVisible(False)
		self.osaCasing_tableWidget.horizontalHeader().setCascadingSectionResizes(False)
		self.osaCasing_tableWidget.horizontalHeader().setDefaultSectionSize(150)
		self.osaCasing_tableWidget.horizontalHeader().setHighlightSections(True)
		self.osaCasing_tableWidget.horizontalHeader().setMinimumSectionSize(120)
		self.osaCasing_tableWidget.horizontalHeader().setSortIndicatorShown(False)
		self.osaCasing_tableWidget.horizontalHeader().setStretchLastSection(False)
		self.osaCasing_tableWidget.verticalHeader().setDefaultSectionSize(25)
		self.osaCasing_tableWidget.verticalHeader().setMinimumSectionSize(25)
		self.osaCasing_tableWidget.verticalHeader().setSortIndicatorShown(False)
		self.label = QtGui.QLabel(self.groupBox)
		self.label.setGeometry(QtCore.QRect(20, 19, 61, 21))
		self.label.setObjectName(_fromUtf8("label"))
		self.label_2 = QtGui.QLabel(self.groupBox)
		self.label_2.setGeometry(QtCore.QRect(20, 200, 151, 31))
		self.label_2.setObjectName(_fromUtf8("label_2"))
		self.osaCentA_tableWidget = QtGui.QTableWidget(self.groupBox)
		self.osaCentA_tableWidget.setGeometry(QtCore.QRect(20, 240, 340, 102))
		font = QtGui.QFont()
		font.setPointSize(9)
		self.osaCentA_tableWidget.setFont(font)
		self.osaCentA_tableWidget.setAutoFillBackground(False)
		self.osaCentA_tableWidget.setFrameShadow(QtGui.QFrame.Sunken)
		self.osaCentA_tableWidget.setColumnCount(1)
		self.osaCentA_tableWidget.setObjectName(_fromUtf8("osaCentA_tableWidget"))
		self.osaCentA_tableWidget.setRowCount(4)
		item = QtGui.QTableWidgetItem()
		self.osaCentA_tableWidget.setVerticalHeaderItem(0, item)
		item = QtGui.QTableWidgetItem()
		self.osaCentA_tableWidget.setVerticalHeaderItem(1, item)
		item = QtGui.QTableWidgetItem()
		self.osaCentA_tableWidget.setVerticalHeaderItem(2, item)
		item = QtGui.QTableWidgetItem()
		self.osaCentA_tableWidget.setVerticalHeaderItem(3, item)
		self.osaCentA_tableWidget.horizontalHeader().setVisible(False)
		self.osaCentA_tableWidget.horizontalHeader().setCascadingSectionResizes(False)
		self.osaCentA_tableWidget.horizontalHeader().setDefaultSectionSize(150)
		self.osaCentA_tableWidget.horizontalHeader().setHighlightSections(True)
		self.osaCentA_tableWidget.horizontalHeader().setMinimumSectionSize(120)
		self.osaCentA_tableWidget.horizontalHeader().setSortIndicatorShown(False)
		self.osaCentA_tableWidget.horizontalHeader().setStretchLastSection(False)
		self.osaCentA_tableWidget.verticalHeader().setDefaultSectionSize(25)
		self.osaCentA_tableWidget.verticalHeader().setMinimumSectionSize(25)
		self.osaCentA_tableWidget.verticalHeader().setSortIndicatorShown(False)
		self.label_3 = QtGui.QLabel(self.groupBox)
		self.label_3.setGeometry(QtCore.QRect(20, 520, 81, 31))
		self.label_3.setObjectName(_fromUtf8("label_3"))
		self.osaWellbore_tableWidget = QtGui.QTableWidget(self.groupBox)
		self.osaWellbore_tableWidget.setGeometry(QtCore.QRect(20, 550, 340, 102))
		font = QtGui.QFont()
		font.setPointSize(9)
		self.osaWellbore_tableWidget.setFont(font)
		self.osaWellbore_tableWidget.setAutoFillBackground(False)
		self.osaWellbore_tableWidget.setFrameShadow(QtGui.QFrame.Sunken)
		self.osaWellbore_tableWidget.setRowCount(4)
		self.osaWellbore_tableWidget.setColumnCount(1)
		self.osaWellbore_tableWidget.setObjectName(_fromUtf8("osaWellbore_tableWidget"))
		item = QtGui.QTableWidgetItem()
		self.osaWellbore_tableWidget.setVerticalHeaderItem(0, item)
		item = QtGui.QTableWidgetItem()
		self.osaWellbore_tableWidget.setVerticalHeaderItem(1, item)
		item = QtGui.QTableWidgetItem()
		self.osaWellbore_tableWidget.setVerticalHeaderItem(2, item)
		item = QtGui.QTableWidgetItem()
		self.osaWellbore_tableWidget.setVerticalHeaderItem(3, item)
		self.osaWellbore_tableWidget.horizontalHeader().setVisible(False)
		self.osaWellbore_tableWidget.horizontalHeader().setCascadingSectionResizes(False)
		self.osaWellbore_tableWidget.horizontalHeader().setDefaultSectionSize(150)
		self.osaWellbore_tableWidget.horizontalHeader().setHighlightSections(True)
		self.osaWellbore_tableWidget.horizontalHeader().setMinimumSectionSize(120)
		self.osaWellbore_tableWidget.horizontalHeader().setSortIndicatorShown(False)
		self.osaWellbore_tableWidget.horizontalHeader().setStretchLastSection(False)
		self.osaWellbore_tableWidget.verticalHeader().setDefaultSectionSize(25)
		self.osaWellbore_tableWidget.verticalHeader().setMinimumSectionSize(25)
		self.osaWellbore_tableWidget.verticalHeader().setSortIndicatorShown(False)
		self.osaCasing_pushButton = QtGui.QPushButton(self.groupBox)
		self.osaCasing_pushButton.setGeometry(QtCore.QRect(189, 19, 171, 30))
		self.osaCasing_pushButton.setObjectName(_fromUtf8("osaCasing_pushButton"))
		self.osaCentA_pushButton = QtGui.QPushButton(self.groupBox)
		self.osaCentA_pushButton.setGeometry(QtCore.QRect(199, 200, 161, 30))
		self.osaCentA_pushButton.setObjectName(_fromUtf8("osaCentA_pushButton"))
		self.label_5 = QtGui.QLabel(self.groupBox)
		self.label_5.setGeometry(QtCore.QRect(20, 360, 171, 31))
		self.label_5.setObjectName(_fromUtf8("label_5"))
		self.osaCentB_pushButton = QtGui.QPushButton(self.groupBox)
		self.osaCentB_pushButton.setGeometry(QtCore.QRect(199, 360, 161, 30))
		self.osaCentB_pushButton.setObjectName(_fromUtf8("osaCentB_pushButton"))
		self.osaInclination_slider = QtGui.QSlider(self.groupBox)
		self.osaInclination_slider.setGeometry(QtCore.QRect(20, 670, 341, 22))
		self.osaInclination_slider.setMaximum(180)
		self.osaInclination_slider.setPageStep(5)
		self.osaInclination_slider.setProperty("value", 90)
		self.osaInclination_slider.setSliderPosition(90)
		self.osaInclination_slider.setOrientation(QtCore.Qt.Horizontal)
		self.osaInclination_slider.setInvertedAppearance(False)
		self.osaInclination_slider.setInvertedControls(False)
		self.osaInclination_slider.setTickPosition(QtGui.QSlider.TicksAbove)
		self.osaInclination_slider.setTickInterval(10)
		self.osaInclination_slider.setObjectName(_fromUtf8("osaInclination_slider"))
		self.osaSpacing_slider = QtGui.QSlider(self.groupBox)
		self.osaSpacing_slider.setGeometry(QtCore.QRect(20, 740, 341, 22))
		self.osaSpacing_slider.setMinimum(10)
		self.osaSpacing_slider.setMaximum(100)
		self.osaSpacing_slider.setProperty("value", 55)
		self.osaSpacing_slider.setSliderPosition(55)
		self.osaSpacing_slider.setOrientation(QtCore.Qt.Horizontal)
		self.osaSpacing_slider.setInvertedAppearance(False)
		self.osaSpacing_slider.setInvertedControls(False)
		self.osaSpacing_slider.setTickPosition(QtGui.QSlider.NoTicks)
		self.osaSpacing_slider.setTickInterval(10)
		self.osaSpacing_slider.setObjectName(_fromUtf8("osaSpacing_slider"))
		self.osaInclination_label = QtGui.QLabel(self.groupBox)
		self.osaInclination_label.setGeometry(QtCore.QRect(150, 700, 211, 21))
		self.osaInclination_label.setObjectName(_fromUtf8("osaInclination_label"))
		self.osaSpacing_label = QtGui.QLabel(self.groupBox)
		self.osaSpacing_label.setGeometry(QtCore.QRect(160, 770, 201, 21))
		self.osaSpacing_label.setObjectName(_fromUtf8("osaSpacing_label"))
		self.osaCentB_tableWidget = QtGui.QTableWidget(self.groupBox)
		self.osaCentB_tableWidget.setGeometry(QtCore.QRect(20, 400, 340, 102))
		font = QtGui.QFont()
		font.setPointSize(9)
		self.osaCentB_tableWidget.setFont(font)
		self.osaCentB_tableWidget.setAutoFillBackground(False)
		self.osaCentB_tableWidget.setFrameShadow(QtGui.QFrame.Sunken)
		self.osaCentB_tableWidget.setColumnCount(1)
		self.osaCentB_tableWidget.setObjectName(_fromUtf8("osaCentB_tableWidget"))
		self.osaCentB_tableWidget.setRowCount(4)
		item = QtGui.QTableWidgetItem()
		self.osaCentB_tableWidget.setVerticalHeaderItem(0, item)
		item = QtGui.QTableWidgetItem()
		self.osaCentB_tableWidget.setVerticalHeaderItem(1, item)
		item = QtGui.QTableWidgetItem()
		self.osaCentB_tableWidget.setVerticalHeaderItem(2, item)
		item = QtGui.QTableWidgetItem()
		self.osaCentB_tableWidget.setVerticalHeaderItem(3, item)
		self.osaCentB_tableWidget.horizontalHeader().setVisible(False)
		self.osaCentB_tableWidget.horizontalHeader().setCascadingSectionResizes(False)
		self.osaCentB_tableWidget.horizontalHeader().setDefaultSectionSize(150)
		self.osaCentB_tableWidget.horizontalHeader().setHighlightSections(True)
		self.osaCentB_tableWidget.horizontalHeader().setMinimumSectionSize(120)
		self.osaCentB_tableWidget.horizontalHeader().setSortIndicatorShown(False)
		self.osaCentB_tableWidget.horizontalHeader().setStretchLastSection(False)
		self.osaCentB_tableWidget.verticalHeader().setDefaultSectionSize(25)
		self.osaCentB_tableWidget.verticalHeader().setMinimumSectionSize(25)
		self.osaCentB_tableWidget.verticalHeader().setSortIndicatorShown(False)
		self.tabWidget = QtGui.QTabWidget(OneSpanAnalysis)
		self.tabWidget.setGeometry(QtCore.QRect(430, 10, 651, 811))
		font = QtGui.QFont()
		font.setPointSize(10)
		self.tabWidget.setFont(font)
		self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
		self.tab = QtGui.QWidget()
		self.tab.setObjectName(_fromUtf8("tab"))
		self.osaOutputdata1_tableWidget = QtGui.QTableWidget(self.tab)
		self.osaOutputdata1_tableWidget.setGeometry(QtCore.QRect(110, 30, 424, 227))
		font = QtGui.QFont()
		font.setPointSize(9)
		self.osaOutputdata1_tableWidget.setFont(font)
		self.osaOutputdata1_tableWidget.setAutoFillBackground(False)
		self.osaOutputdata1_tableWidget.setFrameShadow(QtGui.QFrame.Sunken)
		self.osaOutputdata1_tableWidget.setColumnCount(1)
		self.osaOutputdata1_tableWidget.setObjectName(_fromUtf8("osaOutputdata1_tableWidget"))
		self.osaOutputdata1_tableWidget.setRowCount(9)
		item = QtGui.QTableWidgetItem()
		self.osaOutputdata1_tableWidget.setVerticalHeaderItem(0, item)
		item = QtGui.QTableWidgetItem()
		self.osaOutputdata1_tableWidget.setVerticalHeaderItem(1, item)
		item = QtGui.QTableWidgetItem()
		self.osaOutputdata1_tableWidget.setVerticalHeaderItem(2, item)
		item = QtGui.QTableWidgetItem()
		self.osaOutputdata1_tableWidget.setVerticalHeaderItem(3, item)
		item = QtGui.QTableWidgetItem()
		self.osaOutputdata1_tableWidget.setVerticalHeaderItem(4, item)
		item = QtGui.QTableWidgetItem()
		self.osaOutputdata1_tableWidget.setVerticalHeaderItem(5, item)
		item = QtGui.QTableWidgetItem()
		self.osaOutputdata1_tableWidget.setVerticalHeaderItem(6, item)
		item = QtGui.QTableWidgetItem()
		self.osaOutputdata1_tableWidget.setVerticalHeaderItem(7, item)
		item = QtGui.QTableWidgetItem()
		self.osaOutputdata1_tableWidget.setVerticalHeaderItem(8, item)
		self.osaOutputdata1_tableWidget.horizontalHeader().setVisible(False)
		self.osaOutputdata1_tableWidget.horizontalHeader().setCascadingSectionResizes(False)
		self.osaOutputdata1_tableWidget.horizontalHeader().setDefaultSectionSize(150)
		self.osaOutputdata1_tableWidget.horizontalHeader().setHighlightSections(True)
		self.osaOutputdata1_tableWidget.horizontalHeader().setMinimumSectionSize(120)
		self.osaOutputdata1_tableWidget.horizontalHeader().setSortIndicatorShown(False)
		self.osaOutputdata1_tableWidget.horizontalHeader().setStretchLastSection(False)
		self.osaOutputdata1_tableWidget.verticalHeader().setDefaultSectionSize(25)
		self.osaOutputdata1_tableWidget.verticalHeader().setMinimumSectionSize(25)
		self.osaOutputdata1_tableWidget.verticalHeader().setSortIndicatorShown(False)
		self.tabWidget_2 = QtGui.QTabWidget(self.tab)
		self.tabWidget_2.setGeometry(QtCore.QRect(20, 280, 611, 481))
		self.tabWidget_2.setTabPosition(QtGui.QTabWidget.West)
		self.tabWidget_2.setObjectName(_fromUtf8("tabWidget_2"))
		self.tabA = QtGui.QWidget()
		self.tabA.setObjectName(_fromUtf8("tabA"))
		self.osaClearanceAnalysisA_graphicsView = MatplotlibWidget(self.tabA)
		self.osaClearanceAnalysisA_graphicsView.setGeometry(QtCore.QRect(60, 10, 450, 450))
		self.osaClearanceAnalysisA_graphicsView.setObjectName(_fromUtf8("osaClearanceAnalysisA_graphicsView"))
		self.tabWidget_2.addTab(self.tabA, _fromUtf8(""))
		self.tabB = QtGui.QWidget()
		self.tabB.setObjectName(_fromUtf8("tabB"))
		self.osaClearanceAnalysisB_graphicsView = MatplotlibWidget(self.tabB)
		self.osaClearanceAnalysisB_graphicsView.setGeometry(QtCore.QRect(60, 10, 450, 450))
		self.osaClearanceAnalysisB_graphicsView.setObjectName(_fromUtf8("osaClearanceAnalysisB_graphicsView"))
		self.tabWidget_2.addTab(self.tabB, _fromUtf8(""))
		self.tabM = QtGui.QWidget()
		self.tabM.setObjectName(_fromUtf8("tabM"))
		self.osaClearanceAnalysisM_graphicsView = MatplotlibWidget(self.tabM)
		self.osaClearanceAnalysisM_graphicsView.setGeometry(QtCore.QRect(60, 10, 450, 450))
		self.osaClearanceAnalysisM_graphicsView.setObjectName(_fromUtf8("osaClearanceAnalysisM_graphicsView"))
		self.tabWidget_2.addTab(self.tabM, _fromUtf8(""))
		self.tabWidget.addTab(self.tab, _fromUtf8(""))
		self.tab_2 = QtGui.QWidget()
		self.tab_2.setObjectName(_fromUtf8("tab_2"))
		self.osaSpacingSentivity_graphicsView = MatplotlibWidget(self.tab_2)
		self.osaSpacingSentivity_graphicsView.setGeometry(QtCore.QRect(10, 140, 630, 630))
		self.osaSpacingSentivity_graphicsView.setObjectName(_fromUtf8("osaSpacingSentivity_graphicsView"))
		self.osaOutputdata2_tableWidget = QtGui.QTableWidget(self.tab_2)
		self.osaOutputdata2_tableWidget.setGeometry(QtCore.QRect(110, 30, 390, 102))
		font = QtGui.QFont()
		font.setPointSize(9)
		self.osaOutputdata2_tableWidget.setFont(font)
		self.osaOutputdata2_tableWidget.setAutoFillBackground(False)
		self.osaOutputdata2_tableWidget.setFrameShadow(QtGui.QFrame.Sunken)
		self.osaOutputdata2_tableWidget.setColumnCount(1)
		self.osaOutputdata2_tableWidget.setObjectName(_fromUtf8("osaOutputdata2_tableWidget"))
		self.osaOutputdata2_tableWidget.setRowCount(4)
		item = QtGui.QTableWidgetItem()
		self.osaOutputdata2_tableWidget.setVerticalHeaderItem(0, item)
		item = QtGui.QTableWidgetItem()
		self.osaOutputdata2_tableWidget.setVerticalHeaderItem(1, item)
		item = QtGui.QTableWidgetItem()
		self.osaOutputdata2_tableWidget.setVerticalHeaderItem(2, item)
		item = QtGui.QTableWidgetItem()
		self.osaOutputdata2_tableWidget.setVerticalHeaderItem(3, item)
		self.osaOutputdata2_tableWidget.horizontalHeader().setVisible(False)
		self.osaOutputdata2_tableWidget.horizontalHeader().setCascadingSectionResizes(False)
		self.osaOutputdata2_tableWidget.horizontalHeader().setDefaultSectionSize(150)
		self.osaOutputdata2_tableWidget.horizontalHeader().setHighlightSections(True)
		self.osaOutputdata2_tableWidget.horizontalHeader().setMinimumSectionSize(120)
		self.osaOutputdata2_tableWidget.horizontalHeader().setSortIndicatorShown(False)
		self.osaOutputdata2_tableWidget.horizontalHeader().setStretchLastSection(False)
		self.osaOutputdata2_tableWidget.verticalHeader().setDefaultSectionSize(25)
		self.osaOutputdata2_tableWidget.verticalHeader().setMinimumSectionSize(25)
		self.osaOutputdata2_tableWidget.verticalHeader().setSortIndicatorShown(False)
		self.tabWidget.addTab(self.tab_2, _fromUtf8(""))

		self.retranslateUi(OneSpanAnalysis)
		self.tabWidget.setCurrentIndex(0)
		self.tabWidget_2.setCurrentIndex(0)
		QtCore.QMetaObject.connectSlotsByName(OneSpanAnalysis)

	def retranslateUi(self, OneSpanAnalysis):
		OneSpanAnalysis.setWindowTitle(_translate("OneSpanAnalysis", "One Span Analysis", None))
		self.osaCasing_tableWidget.setSortingEnabled(False)
		item = self.osaCasing_tableWidget.verticalHeaderItem(0)
		item.setText(_translate("OneSpanAnalysis", "Wt", None))
		item = self.osaCasing_tableWidget.verticalHeaderItem(1)
		item.setText(_translate("OneSpanAnalysis", "OD", None))
		item = self.osaCasing_tableWidget.verticalHeaderItem(2)
		item.setText(_translate("OneSpanAnalysis", "ID", None))
		item = self.osaCasing_tableWidget.verticalHeaderItem(3)
		item.setText(_translate("OneSpanAnalysis", "E", None))
		item = self.osaCasing_tableWidget.verticalHeaderItem(4)
		item.setText(_translate("OneSpanAnalysis", "Density                                       ", None))
		self.label.setText(_translate("OneSpanAnalysis", "Casing:", None))
		self.label_2.setText(_translate("OneSpanAnalysis", "Centralizer A (top):", None))
		self.osaCentA_tableWidget.setSortingEnabled(False)
		item = self.osaCentA_tableWidget.verticalHeaderItem(0)
		item.setText(_translate("OneSpanAnalysis", "Restoring F.", None))
		item = self.osaCentA_tableWidget.verticalHeaderItem(1)
		item.setText(_translate("OneSpanAnalysis", "Centralized OD", None))
		item = self.osaCentA_tableWidget.verticalHeaderItem(2)
		item.setText(_translate("OneSpanAnalysis", "IP OD", None))
		item = self.osaCentA_tableWidget.verticalHeaderItem(3)
		item.setText(_translate("OneSpanAnalysis", "Min. pass thru                           ", None))
		self.label_3.setText(_translate("OneSpanAnalysis", "Wellbore:", None))
		self.osaWellbore_tableWidget.setSortingEnabled(False)
		item = self.osaWellbore_tableWidget.verticalHeaderItem(0)
		item.setText(_translate("OneSpanAnalysis", "Hole ID", None))
		item = self.osaWellbore_tableWidget.verticalHeaderItem(1)
		item.setText(_translate("OneSpanAnalysis", "Max span", None))
		item = self.osaWellbore_tableWidget.verticalHeaderItem(2)
		item.setText(_translate("OneSpanAnalysis", "Mud inside pipe                        ", None))
		item = self.osaWellbore_tableWidget.verticalHeaderItem(3)
		item.setText(_translate("OneSpanAnalysis", "Mud in annulus", None))
		self.osaCasing_pushButton.setText(_translate("OneSpanAnalysis", "Pipe DB ...", None))
		self.osaCentA_pushButton.setText(_translate("OneSpanAnalysis", "Centralizer DB ...", None))
		self.label_5.setText(_translate("OneSpanAnalysis", "Centralizer B (bottom):", None))
		self.osaCentB_pushButton.setText(_translate("OneSpanAnalysis", "Centralizer DB ...", None))
		self.osaInclination_label.setText(_translate("OneSpanAnalysis", "Inclination", None))
		self.osaSpacing_label.setText(_translate("OneSpanAnalysis", "Spacing", None))
		self.osaCentB_tableWidget.setSortingEnabled(False)
		item = self.osaCentB_tableWidget.verticalHeaderItem(0)
		item.setText(_translate("OneSpanAnalysis", "Restoring F.", None))
		item = self.osaCentB_tableWidget.verticalHeaderItem(1)
		item.setText(_translate("OneSpanAnalysis", "Centralized OD", None))
		item = self.osaCentB_tableWidget.verticalHeaderItem(2)
		item.setText(_translate("OneSpanAnalysis", "IP OD", None))
		item = self.osaCentB_tableWidget.verticalHeaderItem(3)
		item.setText(_translate("OneSpanAnalysis", "Min. pass thru                           ", None))
		self.osaOutputdata1_tableWidget.setSortingEnabled(False)
		item = self.osaOutputdata1_tableWidget.verticalHeaderItem(0)
		item.setText(_translate("OneSpanAnalysis", "Annular clearance @ cent. A", None))
		item = self.osaOutputdata1_tableWidget.verticalHeaderItem(1)
		item.setText(_translate("OneSpanAnalysis", "Annular clearance @ cent. B", None))
		item = self.osaOutputdata1_tableWidget.verticalHeaderItem(2)
		item.setText(_translate("OneSpanAnalysis", "Annular clearance @ mid span                    ", None))
		item = self.osaOutputdata1_tableWidget.verticalHeaderItem(3)
		item.setText(_translate("OneSpanAnalysis", "Side force @ cent. A", None))
		item = self.osaOutputdata1_tableWidget.verticalHeaderItem(4)
		item.setText(_translate("OneSpanAnalysis", "Side force @ cent. B", None))
		item = self.osaOutputdata1_tableWidget.verticalHeaderItem(5)
		item.setText(_translate("OneSpanAnalysis", "Side force @ mid span", None))
		item = self.osaOutputdata1_tableWidget.verticalHeaderItem(6)
		item.setText(_translate("OneSpanAnalysis", "Standoff @ cent. A", None))
		item = self.osaOutputdata1_tableWidget.verticalHeaderItem(7)
		item.setText(_translate("OneSpanAnalysis", "Standoff @ cent. B", None))
		item = self.osaOutputdata1_tableWidget.verticalHeaderItem(8)
		item.setText(_translate("OneSpanAnalysis", "Standoff @ mid span", None))
		self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tabA), _translate("OneSpanAnalysis", "At centralizer A", None))
		self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tabB), _translate("OneSpanAnalysis", "At centralizer B", None))
		self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tabM), _translate("OneSpanAnalysis", "At mid span", None))
		self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("OneSpanAnalysis", "Clearance analysis", None))
		self.osaOutputdata2_tableWidget.setSortingEnabled(False)
		item = self.osaOutputdata2_tableWidget.verticalHeaderItem(0)
		item.setText(_translate("OneSpanAnalysis", "Axial extra force @ top                        ", None))
		item = self.osaOutputdata2_tableWidget.verticalHeaderItem(1)
		item.setText(_translate("OneSpanAnalysis", "Max pipe deflection", None))
		item = self.osaOutputdata2_tableWidget.verticalHeaderItem(2)
		item.setText(_translate("OneSpanAnalysis", "Mean wellbore clearance", None))
		item = self.osaOutputdata2_tableWidget.verticalHeaderItem(3)
		item.setText(_translate("OneSpanAnalysis", "Mean wellbore standoff", None))
		self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("OneSpanAnalysis", "Spacing sensitivity", None))

from matplotlibwidget import MatplotlibWidget
