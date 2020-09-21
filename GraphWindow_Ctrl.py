from PyQt4 import QtCore, QtGui
from GraphWindow_Vst import Ui_GraphWindow
#import GraphWindow_Mdl as mdl
import CtrlUtilities as cu
import PlotUtilities as pu
import MdlUtilities as mu


class Main_GraphWindow(Ui_GraphWindow):

	def __init__(self, dialog, parent):

		Ui_GraphWindow.__init__(self)
		zp = pu.ZoomPan()
		self.setupUi(dialog)
		self.dialog = dialog
		self.parent = parent

		#self.lsAccept_pushButton.clicked.connect( self.makeResults_and_done )
		
		

		#-------------------------------------------------

		#self.lsCaliperMap_graphicsView.axes.set_position([0.2,0.15,0.75,0.8])
		

		#-------------------------------------------------
		
		EW = parent.v2ASCComplements_fields.EW
		NS = parent.v2ASCComplements_fields.NS
		VD = parent.v2ASCComplements_fields.TVD


		max_VD = max(VD)
		min_VD = min(VD)
		max_EW = max(EW)
		min_EW = min(EW)
		max_NS = max(NS)
		min_NS = min(NS)
		
		ΔVD = max_VD - min_VD
		ΔEW = max_EW - min_EW
		ΔNS = max_NS - min_NS

		Δ = max( [ΔVD, ΔEW, ΔNS] )

		if ΔVD==Δ:
			self.gwColoredWellbore_graphicsView.axes.set_xlim( min_EW-(Δ-ΔEW)/2, max_EW+(Δ-ΔEW)/2 )
			self.gwColoredWellbore_graphicsView.axes.set_ylim( min_NS-(Δ-ΔNS)/2, max_NS+(Δ-ΔNS)/2 )
			self.gwColoredWellbore_graphicsView.axes.set_zlim( max_VD, min_VD )
		elif ΔNS==Δ:
			self.gwColoredWellbore_graphicsView.axes.set_xlim( min_EW-(Δ-ΔEW)/2, max_EW+(Δ-ΔEW)/2 )
			self.gwColoredWellbore_graphicsView.axes.set_ylim( min_NS, max_NS )
			self.gwColoredWellbore_graphicsView.axes.set_zlim( max_VD+(Δ-ΔVD)/2, min_VD-(Δ-ΔVD)/2 )
		elif ΔEW==Δ:
			self.gwColoredWellbore_graphicsView.axes.set_xlim( min_EW, max_EW )
			self.gwColoredWellbore_graphicsView.axes.set_ylim( min_NS-(Δ-ΔNS)/2, max_NS+(Δ-ΔNS)/2 )
			self.gwColoredWellbore_graphicsView.axes.set_zlim( max_VD+(Δ-ΔVD)/2, min_VD-(Δ-ΔVD)/2 )


		
		X,Y,Z,C = mu.render_wellbore( parent.v2ASCComplements_fields, 100, 20 )
		SO = mu.np.interp(parent.v2ASCComplements_fields.MD, parent.v3SOs_MD, parent.v3SOs_SO)
		C = SO*C

		lis = pu.LightSource(270, 45)
		rgb = lis.shade(C, cmap=pu.cm.bwr, vert_exag=1, blend_mode='soft')
		self.gwColoredWellbore_graphicsView.axes.plot_surface(X,Y,Z, linewidth=0, facecolors=rgb, antialiased=False)


		curve, = self.gwColoredWellbore_graphicsView.axes.plot( EW, NS, VD, lw=2 )



		self.gwColoredWellbore_graphicsView.axes.set_xlabel( EW.headerName )
		self.gwColoredWellbore_graphicsView.axes.set_ylabel( NS.headerName )
		self.gwColoredWellbore_graphicsView.axes.set_zlabel( VD.headerName )
	
		self.gwColoredWellbore_graphicsView.axes.mouse_init()
		#zp.point3D_factory(self.s2TriDView_graphicsView.axes, dot, curve)
		zp.zoom3D_factory( self.gwColoredWellbore_graphicsView.axes, curve )
		#self.gwColoredWellbore_graphicsView.draw()

		dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		dialog.exec_()