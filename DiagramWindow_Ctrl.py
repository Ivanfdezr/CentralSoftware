from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from DiagramWindow_Vst import Ui_DiagramWindow
import InputWindow_Mdl as mdl
import CtrlUtilities as cu
import PlotUtilities as pu
import MdlUtilities as mu


class Main_DiagramWindow(Ui_DiagramWindow):

	def __init__(self, dialog, parent):

		Ui_DiagramWindow.__init__(self)
		#zp = pu.ZoomPan()
		self.setupUi(dialog)
		self.dialog = dialog
		self.parent = parent

		self.dwWellboreSchematic_graphicsView

		self.dwWellboreSchematic_graphicsView.axes.set_position([0.2,0.15,0.75,0.8])
		zp = pu.ZoomPan()
		zp.zoom2D_factory( self.dwWellboreSchematic_graphicsView.axes )
		zp.pan2D_factory( self.dwWellboreSchematic_graphicsView.axes )
		self.dwWellboreSchematic_graphicsView.axes.clear()

		MDs = self.parent.v3Forces_fields.MD[:]

		for stage in self.parent.v3WellboreInnerStageData.values():
			MDbot = stage['MDbot']
			MDs.append(MDbot)

		for stage in self.parent.v3WellboreOuterStageData.values():
			MDbot = stage['WellboreProps'].MDbot[0]
			MDs.append(MDbot)

		MDs.sort()
		MDunit = MDbot.unit
		factor = max(self.parent.v3Forces_fields.HD)/mdl.get_outerStage_at_MD( self.parent, 0.0, MDunit )['WellboreProps'].ID[0]*0.2

		HDu_i = []
		VDu_i = []
		HDd_i = []
		VDd_i = []
		HDu_o = []
		VDu_o = []
		HDd_o = []
		VDd_o = []

		for MD in MDs:
			ew,ns,VD,HD,i = mdl.get_ASCCoordinates_from_MD(self.parent, MD, MDunit)

			T = mdl.get_ASCT_from_MD(self.parent, MD, MDunit)
			t = mu.np.array([ T[3], T[2], 0 ])
			t = t.reshape(1,-1)
			normt = mu.np.linalg.norm(t)
			if normt!=0.0:
				t /=normt
			u = mu.np.array([ 0, 0, 1 ])
			u = u.reshape(1,-1)
			nu = mu.np_cross(t,u)

			d = mu.np.array([ 0, 0, -1 ])
			d = d.reshape(1,-1)
			nd = mu.np_cross(t,d)

			innerStage = mdl.get_innerStage_at_MD(self.parent, MD, MDunit)
			factor_i = factor*innerStage['PipeProps'].OD[0]

			outerStage = mdl.get_outerStage_at_MD(self.parent, MD, MDunit)
			if outerStage['PipeBase']==None:
				noise = 0.1*(mu.np.random.rand()-0.5)+1
			else:
				noise = 1
			factor_o = factor*outerStage['WellboreProps'].ID[0]*noise

			HDu_i.append( HD+nu[0][0]*factor_i )
			VDu_i.append( VD+nu[0][1]*factor_i )
			HDd_i.append( HD+nd[0][0]*factor_i )
			VDd_i.append( VD+nd[0][1]*factor_i )
			HDu_o.append( HD+nu[0][0]*factor_o )
			VDu_o.append( VD+nu[0][1]*factor_o )
			HDd_o.append( HD+nd[0][0]*factor_o )
			VDd_o.append( VD+nd[0][1]*factor_o )

		max_VD = max( self.parent.v3Forces_fields.TVD )
		min_VD = min( self.parent.v3Forces_fields.TVD )
		delta = (max_VD-min_VD)*0.55

		self.dwWellboreSchematic_graphicsView.axes.axis('equal')
		self.dwWellboreSchematic_graphicsView.axes.set_ylim( max_VD+delta, min_VD-delta )
		self.dwWellboreSchematic_graphicsView.axes.set_xlabel( self.parent.v3Forces_fields.HD.headerName )
		self.dwWellboreSchematic_graphicsView.axes.set_ylabel( self.parent.v3Forces_fields.TVD.headerName )
		
		self.dwWellboreSchematic_graphicsView.axes.plot( self.parent.v3Forces_fields.HD, self.parent.v3Forces_fields.TVD, 'k--', lw=1 )
		self.dwWellboreSchematic_graphicsView.axes.plot( HDu_i, VDu_i, 'C1', lw=3 )
		self.dwWellboreSchematic_graphicsView.axes.plot( HDd_i, VDd_i, 'C1', lw=3 )
		self.dwWellboreSchematic_graphicsView.axes.plot( HDu_o, VDu_o, 'C0', lw=3 )
		self.dwWellboreSchematic_graphicsView.axes.plot( HDd_o, VDd_o, 'C0', lw=3 )

		for stage in self.parent.v3WellboreInnerStageData.values():
			MDbot = stage['MDbot']

			EW,NS,VD,HD,i = mdl.get_ASCCoordinates_from_MD(self.parent, MDbot)

			T = mdl.get_ASCT_from_MD(self.parent, MDbot, MDbot.unit)
			t = mu.np.array([ T[3], T[2], 0 ])
			t = t.reshape(1,-1)
			normt = mu.np.linalg.norm(t)
			if normt!=0.0:
				t /=normt
			u = mu.np.array([ 0, 0, 1 ])
			u = u.reshape(1,-1)
			nu = mu.np_cross(t,u)
			nu *= 0.3*max_VD

			d = mu.np.array([ 0, 0, -1 ])
			d = d.reshape(1,-1)
			nd = mu.np_cross(t,d)
			nd *= 0.3*max_VD

			self.dwWellboreSchematic_graphicsView.axes.arrow(HD, VD, nu[0][0], nu[0][1], head_width=0, head_length=0, fc='k', ec='k', lw=0.5, alpha=0.5)
			self.dwWellboreSchematic_graphicsView.axes.arrow(HD, VD, nd[0][0], nd[0][1], head_width=0, head_length=0, fc='k', ec='k', lw=0.5, alpha=0.5)
			

		dialog.setAttribute(Qt.WA_DeleteOnClose)
		dialog.exec_()