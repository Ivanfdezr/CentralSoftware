from PyQt4 import QtCore, QtGui
from OutputWindow_Vst import Ui_OutputWindow
from UnitSettings_Ctrl import Main_UnitSettings
from OneSpanAnalysis_Ctrl import Main_OneSpanAnalysis
#import OutputWindow_Mdl as mdl
import CtrlUtilities as cu


class Main_OutputWindow(Ui_OutputWindow):

	def __init__(self, window):
		Ui_OutputWindow.__init__(self)
		self.setupUi(window)