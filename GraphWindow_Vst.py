# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GraphWindow_Vst.ui'
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

class Ui_GraphWindow(object):
	def setupUi(self, GraphWindow):
		GraphWindow.setObjectName(_fromUtf8("GraphWindow"))
		GraphWindow.resize(920, 828)
		self.gwColoredWellbore_graphicsView = Matplotlib3DWidget(GraphWindow)
		self.gwColoredWellbore_graphicsView.setGeometry(QtCore.QRect(9, 9, 901, 801))
		self.gwColoredWellbore_graphicsView.setObjectName(_fromUtf8("gwColoredWellbore_graphicsView"))

		self.retranslateUi(GraphWindow)
		QtCore.QMetaObject.connectSlotsByName(GraphWindow)

	def retranslateUi(self, GraphWindow):
		GraphWindow.setWindowTitle(_translate("GraphWindow", "3D Centralization Visualization", None))

from matplotlibwidget import Matplotlib3DWidget
