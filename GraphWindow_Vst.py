# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GraphWindow_Vst.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_GraphWindow(object):
	def setupUi(self, GraphWindow):
		GraphWindow.setObjectName("GraphWindow")
		GraphWindow.resize(920, 828)
		self.gwColoredWellbore_graphicsView = Matplotlib3DWidget(GraphWindow)
		self.gwColoredWellbore_graphicsView.setGeometry(QtCore.QRect(9, 9, 901, 801))
		self.gwColoredWellbore_graphicsView.setObjectName("gwColoredWellbore_graphicsView")

		self.retranslateUi(GraphWindow)
		QtCore.QMetaObject.connectSlotsByName(GraphWindow)

	def retranslateUi(self, GraphWindow):
		_translate = QtCore.QCoreApplication.translate
		GraphWindow.setWindowTitle(_translate("GraphWindow", "3D Centralization Visualization"))

from matplotlibwidget import Matplotlib3DWidget
