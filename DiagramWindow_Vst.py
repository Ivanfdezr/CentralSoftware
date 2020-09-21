# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DiagramWindow_Vst.ui'
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

class Ui_DiagramWindow(object):
	def setupUi(self, DiagramWindow):
		DiagramWindow.setObjectName(_fromUtf8("DiagramWindow"))
		DiagramWindow.resize(920, 828)
		self.dwWellboreSchematic_graphicsView = MatplotlibWidget(DiagramWindow)
		self.dwWellboreSchematic_graphicsView.setGeometry(QtCore.QRect(9, 9, 901, 801))
		self.dwWellboreSchematic_graphicsView.setObjectName(_fromUtf8("dwWellboreSchematic_graphicsView"))

		self.retranslateUi(DiagramWindow)
		QtCore.QMetaObject.connectSlotsByName(DiagramWindow)

	def retranslateUi(self, DiagramWindow):
		DiagramWindow.setWindowTitle(_translate("DiagramWindow", "Schematic Diagram Visualization", None))

from matplotlibwidget import MatplotlibWidget
