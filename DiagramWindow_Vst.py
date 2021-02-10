# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DiagramWindow_Vst.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DiagramWindow(object):
	def setupUi(self, DiagramWindow):
		DiagramWindow.setObjectName("DiagramWindow")
		DiagramWindow.resize(920, 828)
		self.dwWellboreSchematic_graphicsView = MatplotlibWidget(DiagramWindow)
		self.dwWellboreSchematic_graphicsView.setGeometry(QtCore.QRect(9, 9, 901, 801))
		self.dwWellboreSchematic_graphicsView.setObjectName("dwWellboreSchematic_graphicsView")

		self.retranslateUi(DiagramWindow)
		QtCore.QMetaObject.connectSlotsByName(DiagramWindow)

	def retranslateUi(self, DiagramWindow):
		_translate = QtCore.QCoreApplication.translate
		DiagramWindow.setWindowTitle(_translate("DiagramWindow", "Schematic Diagram Visualization"))

from matplotlibwidget import MatplotlibWidget
