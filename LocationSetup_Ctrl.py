from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from LocationSetup_Vst import Ui_LocationSetup
import LocationSetup_Vst as vst
import LocationSetup_Mdl as mdl
import CtrlUtilities as cu
import PlotUtilities as pu
import MdlUtilities as mu
import copy
import re, os, sys
import datetime as dt


class Main_LocationSetup(Ui_LocationSetup):

	def __init__(self, dialog, parent):

		Ui_LocationSetup.__init__(self)
		zp = pu.ZoomPan()
		self.setupUi(dialog)
		self.dialog = dialog
		self.parent = parent

		self.lsAccept_pushButton.clicked.connect( self.makeResults_and_done )
		self.lsCentralization_fields = mdl.get_lsCentralization_fields()
		self.__init__lsCentralizerLocations_tableWidget()

		self.MD = self.parent.v3WorkWellboreMD
		self.ID = self.parent.v3WorkWellboreID
		self.max_MD = mu.np.max( self.MD )
		self.min_MD = mu.np.min( self.MD )
		self.lim_ID = mu.np.max( self.ID )*1.2

		self.numofStages = mdl.cat_locations(self)
		self.centralizerCount = len(self.lsCentralization_fields.MD)
		self.update_calculations()
		

		#-------------------------------------------------

		self.lsCaliperMap_graphicsView.axes.set_position([0.2,0.15,0.75,0.8])
		self.lsCaliperMap_graphicsView_ylimits    = [None,None]
		self.lsCaliperMap_graphicsView_yselection = []

		self.lsSOVisualization_graphicsView.axes.set_position([0.2,0.15,0.75,0.8])
		self.lsSOVisualization_graphicsView_ylimits    = [None,None]
		self.lsSOVisualization_graphicsView_yselection = []

		self.lsSideForces_graphicsView.axes.set_position([0.2,0.15,0.75,0.8])
		#self.lsSideForces_graphicsView_ylimits    = [None,None]
		#self.lsSideForces_graphicsView_yselection = []
		
		zp.zoomYD_factory(	(self.lsCaliperMap_graphicsView.axes, self.lsSOVisualization_graphicsView.axes),
							(self.lsCaliperMap_graphicsView_ylimits, self.lsSOVisualization_graphicsView_ylimits)  )
		zp.panYD_factory(	(self.lsCaliperMap_graphicsView.axes, self.lsSOVisualization_graphicsView.axes), 
							(self.lsCaliperMap_graphicsView_ylimits, self.lsSOVisualization_graphicsView_ylimits), 
							(self.lsCaliperMap_graphicsView_yselection, self.lsSOVisualization_graphicsView_yselection),
							ypressfunction1=self.highlight_MDlocation,
							ypressfunction3=self.choose_MDlocation )
		zp.zoom2D_factory( self.lsSideForces_graphicsView.axes )
		zp.pan2D_factory( self.lsSideForces_graphicsView.axes )

		self.lsCaliperMap_graphicsView.axes.clear()
		self.lsSOVisualization_graphicsView.axes.clear()
		self.lsSideForces_graphicsView.axes.clear()

		#-------------------------------------------------

		self.lsCaliperMap_graphicsView.axes.fill_betweenx( self.MD, -self.ID, +self.ID, alpha=0.5, color='C0')
		factors = mu.np.linspace(1.2,1.6,8)

		for stage in self.parent.v3WellboreInnerStageData.values():
			
			MDstage,IDstage = mdl.get_LASMDandCALID_intoStage(self, stage)
			IPODstage = stage['PipeProps'].OD[0]

			"""
			for factor in factors[1:]:
				IPOD = IPODstage*factor
				self.lsCaliperMap_graphicsView.axes.fill_betweenx( MDstage, +IPOD, +IDstage, where=IPOD<IDstage, alpha=0.15, color='C3')
				self.lsCaliperMap_graphicsView.axes.fill_betweenx( MDstage, -IPOD, -IDstage, where=IPOD<IDstage, alpha=0.15, color='C3')
			"""

			if stage['Centralization']['Mode']==False:
				self.lsCaliperMap_graphicsView.axes.fill_betweenx( MDstage, -IDstage, +IDstage, alpha=0.5, color='white')

			self.lsCaliperMap_graphicsView.axes.plot( [ -self.lim_ID, self.lim_ID ], [stage['MDbot'],stage['MDbot']], 'k-', lw=0.5, alpha=0.5 )
			self.lsCaliperMap_graphicsView.axes.plot( [ -IPODstage, -IPODstage], [MDstage[0],MDstage[-1]], 'C1', lw=2 )
			self.lsCaliperMap_graphicsView.axes.plot( [ +IPODstage, +IPODstage], [MDstage[0],MDstage[-1]], 'C1', lw=2 )

		MDHeaderName = self.lsCentralization_fields.MD.headerName
		IDHeaderName = self.lsCentralization_fields.ID.headerName

		self.lsCaliperMap_graphicsView.axes.set_xlabel( IDHeaderName )
		self.lsCaliperMap_graphicsView.axes.set_ylabel( MDHeaderName )
		self.lsCaliperMap_graphicsView.axes.set_xlim( -self.lim_ID, self.lim_ID )
		self.lsCaliperMap_graphicsView.axes.set_ylim( self.max_MD, self.min_MD ) 
		#self.lsCaliperMap_graphicsView.draw()

		#-------------------------------------------------

		max_VD = max( self.parent.v3Forces_fields.TVD )
		min_VD = min( self.parent.v3Forces_fields.TVD )
		max_SF = max( self.parent.v3Forces_fields.SideF )

		self.lsSideForces_graphicsView.axes.axis('equal')
		self.lsSideForces_graphicsView.axes.set_ylim( max_VD, min_VD )
		self.lsSideForces_graphicsView.axes.set_xlabel( self.parent.v3Forces_fields.HD.headerName )
		self.lsSideForces_graphicsView.axes.set_ylabel( self.parent.v3Forces_fields.TVD.headerName )
		
		self.lsSideForces_graphicsView.axes.plot( self.parent.v3Forces_fields.HD, self.parent.v3Forces_fields.TVD, 'C0', lw=3 )
		factor = max(self.parent.v3Forces_fields.HD)/max(self.parent.v3Forces_fields.SideF)*0.5
		for i,MDi in enumerate(self.parent.v3Forces_fields.MD):
			HDi = self.parent.v3Forces_fields.HD[i]
			VDi = self.parent.v3Forces_fields.TVD[i]
			DFi = self.parent.v3Forces_fields.DLplaneF[i]
			SFi = self.parent.v3Forces_fields.SideF[i]

			T = mdl.mdl.get_ASCT_from_MD(self.parent, MDi, MDi.unit)
			t = mu.np.array([ T[3], T[2], 0 ])
			t = t.reshape(1,-1)
			normt = mu.np.linalg.norm(t)
			if normt!=0.0:
				t /=normt
			u = mu.np.array([ 0, 0, -DFi ])
			u = u.reshape(1,-1)
			normu = mu.np.linalg.norm(u)
			if normu!=0.0:
				u /=normu
			
			if normt==0 or normu==0:
				n = mu.np.array([ 0, 0, 0 ])
				n = n.reshape(1,-1)
			else:
				n = mu.np_cross(t,u)
				n *= SFi*factor

			self.lsSideForces_graphicsView.axes.arrow(HDi, VDi, n[0][0], n[0][1], head_width=factor*0.1, head_length=factor*0.2, fc='C1', ec='C1')
			#self.lsSideForces_graphicsView.axes.arrow(HDi, VDi, t[0][0], t[0][1], head_width=factor*0.1, head_length=factor*0.2, fc='C1', ec='C1')

		for stage in self.parent.v3WellboreInnerStageData.values():
			MDbot = stage['MDbot']
			EW,NS,VD,HD,i = mdl.mdl.get_ASCCoordinates_from_MD(self.parent, MDbot)

			T = mdl.mdl.get_ASCT_from_MD(self.parent, MDbot, MDbot.unit)
			t = mu.np.array([ T[3], T[2], 0 ])
			t = t.reshape(1,-1)
			normt = mu.np.linalg.norm(t)
			if normt!=0.0:
				t /=normt
			u = mu.np.array([ 0, 0, 1 ])
			u = u.reshape(1,-1)
			nu = mu.np_cross(t,u)
			nu *= 1.2*max_SF*factor

			d = mu.np.array([ 0, 0, -1 ])
			d = d.reshape(1,-1)
			nd = mu.np_cross(t,d)
			nd *= 1.2*max_SF*factor

			self.lsSideForces_graphicsView.axes.arrow(HD, VD, nu[0][0], nu[0][1], head_width=0, head_length=0, fc='k', ec='k', lw=0.5, alpha=0.5)
			self.lsSideForces_graphicsView.axes.arrow(HD, VD, nd[0][0], nd[0][1], head_width=0, head_length=0, fc='k', ec='k', lw=0.5, alpha=0.5)


		#-------------------------------------------------

		SOHeaderName = self.lsCentralization_fields.SOatC.headerName +'  &  '+ self.lsCentralization_fields.SOatM.headerName
		if self.lsCentralization_fields.SOatC.unit=='%':
			self.max_SO = 100
			self.min_SO = 67
			self.ΔSO = 10
		elif self.lsCentralization_fields.SOatC.unit=='1':
			self.max_SO = 1
			self.min_SO = 0.67
			self.ΔSO = 0.1

		self.lsSOVisualization_graphicsView.axes.set_xlabel( SOHeaderName )
		self.lsSOVisualization_graphicsView.axes.set_ylabel( MDHeaderName )
		self.lsSOVisualization_graphicsView.axes.set_xlim( -self.ΔSO, self.max_SO+self.ΔSO )
		self.lsSOVisualization_graphicsView.axes.set_ylim( self.max_MD, self.min_MD )
		#self.lsSOVisualization_graphicsView.axes.grid()
		self.lsSOVisualization_graphicsView.axes.plot( [self.min_SO, self.min_SO], [self.max_MD, self.min_MD], 'C3--', lw=2 )
		self.lsSOVisualization_graphicsView.axes.plot( [0, 0], [self.max_MD, self.min_MD], 'k-', lw=1, alpha=0.3 )
		self.lsSOVisualization_graphicsView.axes.plot( [self.max_SO, self.max_SO], [self.max_MD, self.min_MD], 'k-', lw=1, alpha=0.3 ) 
		for stage in self.parent.v3WellboreInnerStageData.values():
			self.lsSOVisualization_graphicsView.axes.plot( [0, self.max_SO], [stage['MDbot'], stage['MDbot']], 'k-', lw=0.5, alpha=0.5 )

		#self.lsSOVisualization_graphicsView.draw()

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
			self.lsWellbore3D_graphicsView.axes.set_xlim( min_EW-(Δ-ΔEW)/2, max_EW+(Δ-ΔEW)/2 )
			self.lsWellbore3D_graphicsView.axes.set_ylim( min_NS-(Δ-ΔNS)/2, max_NS+(Δ-ΔNS)/2 )
			self.lsWellbore3D_graphicsView.axes.set_zlim( max_VD, min_VD )
		elif ΔNS==Δ:
			self.lsWellbore3D_graphicsView.axes.set_xlim( min_EW-(Δ-ΔEW)/2, max_EW+(Δ-ΔEW)/2 )
			self.lsWellbore3D_graphicsView.axes.set_ylim( min_NS, max_NS )
			self.lsWellbore3D_graphicsView.axes.set_zlim( max_VD+(Δ-ΔVD)/2, min_VD-(Δ-ΔVD)/2 )
		elif ΔEW==Δ:
			self.lsWellbore3D_graphicsView.axes.set_xlim( min_EW, max_EW )
			self.lsWellbore3D_graphicsView.axes.set_ylim( min_NS-(Δ-ΔNS)/2, max_NS+(Δ-ΔNS)/2 )
			self.lsWellbore3D_graphicsView.axes.set_zlim( max_VD+(Δ-ΔVD)/2, min_VD-(Δ-ΔVD)/2 )


		curve, = self.lsWellbore3D_graphicsView.axes.plot( EW, NS, VD, lw=2 )

		self.lsWellbore3D_graphicsView.axes.set_xlabel( EW.headerName )
		self.lsWellbore3D_graphicsView.axes.set_ylabel( NS.headerName )
		self.lsWellbore3D_graphicsView.axes.set_zlabel( VD.headerName )
	
		self.lsWellbore3D_graphicsView.axes.mouse_init()
		#zp.point3D_factory(self.s2TriDView_graphicsView.axes, dot, curve)
		zp.zoom3D_factory( self.lsWellbore3D_graphicsView.axes, curve )
		#self.lsWellbore3D_graphicsView.draw()
		
		#-------------------------------------------------

		self.draw_MDlocations( initial=True )
		self.parent.v3CentralizationProcessed_flag = True
		
		dialog.setAttribute(Qt.WA_DeleteOnClose)
		dialog.exec_()


	def __init__lsCentralizerLocations_tableWidget(self):

		self.lsCentralizerLocations_tableWidget.parent = self
		self.lsCentralizerLocations_tableWidget.setContextMenuPolicy(Qt.ActionsContextMenu)
		
		#C = cu.CopySelectedCells_action(self.lsCentralizerLocations_tableWidget)
		#self.lsCentralizerLocations_tableWidget.addAction(C)
		
		#V = cu.PasteToCells_action(self.lsCentralizerLocations_tableWidget)
		#self.lsCentralizerLocations_tableWidget.addAction(V)

		D = cu.FunctionToWidget_action(self.lsCentralizerLocations_tableWidget, self.remove_location, "Delete", 'Del')
		self.lsCentralizerLocations_tableWidget.addAction(D)

		#select_row = lambda r,c : cu.select_tableWidgetRow(self.lsCentralizerLocations_tableWidget,r)

		for field in self.lsCentralization_fields[:5]:
			#
			item = self.lsCentralizerLocations_tableWidget.horizontalHeaderItem( field.pos )
			item.setText( field.headerName )
			
			for i in range(self.lsCentralizerLocations_tableWidget.rowCount()):
				item = cu.TableWidgetFieldItem( field, i%2==0 )
				self.lsCentralizerLocations_tableWidget.setItem(i, field.pos, item)

		def update_through_itemChange(item):
			call_function = lambda: self.choose_MDlocation(item.realValue, overwrite=True)
			cu.update_fieldItem(item, call_function)

		self.lsCentralizerLocations_tableWidget.cellPressed.connect(self.select_row)
		self.lsCentralizerLocations_tableWidget.itemChanged.connect(update_through_itemChange)
		self.lsCentralizerLocations_tableWidget.resizeColumnsToContents()
		self.lsCentralizerLocations_tableWidget.selectedRow = None


	def makeResults_and_done(self):

		"""
		DT = str(dt.datetime.now())
		items = re.split('[\:]+',DT)
		DT = ''.join(items)
		items = re.split('[ \.]+',DT)
		DT = '_'.join(items[:-1])
		"""

		cu.savetable( 	self.lsCentralizerLocations_tableWidget,
						self.lsCentralization_fields[:5],
						self.parent.v1WorkingDirectory+"/Centralization_LocationsAndSO.csv" )

		self.lsCaliperMap_graphicsView.figure.savefig( self.parent.v1WorkingDirectory+"/Centralization_CaliperMap.png", dpi=300 )

		self.lsSOVisualization_graphicsView.figure.savefig( self.parent.v1WorkingDirectory+"/Centralization_SOVisualization.png", dpi=300 )

		self.lsWellbore3D_graphicsView.figure.savefig( self.parent.v1WorkingDirectory+"/Centralization_Wellbore3D.png", dpi=300 )

		self.lsSideForces_graphicsView.figure.savefig( self.parent.v1WorkingDirectory+"/Centralization_SideForces.png", dpi=300 )

		self.fields = self.lsCentralization_fields

		self.dialog.done(0)


	def select_row(self, r, c, alltherow=False ):

		cu.select_tableWidgetRow(self.lsCentralizerLocations_tableWidget, r, alltherow)
		
		if r<self.centralizerCount:
			MD = self.lsCentralization_fields.MD[r]
			EW = self.lsCentralization_fields.EW[r]
			NS = self.lsCentralization_fields.NS[r]
			VD = self.lsCentralization_fields.TVD[r]
			HD = self.lsCentralization_fields.HD[r]
			ID = self.lsCentralization_fields.ID[r]

			self.draw_MDlocations(MD, EW, NS, VD, HD, ID, created=False)

	@cu.waiting_effects
	def update_calculations(self, indexes=None):
		
		locations = self.lsCentralization_fields.MD
		SOatC_field = self.lsCentralization_fields.SOatC
		SOatM_field = self.lsCentralization_fields.SOatM
		Inc_field = self.lsCentralization_fields.Inc

		if indexes==None:
			mdl.calculate_standOff_at_Centralizers(self)
			mdl.calculate_standOff_at_Midspans(self)
		else:
			for jth in indexes['@c']:
				mdl.calculate_standOff_at_jthCentralizer(self, jth)
			for ith in indexes['@m']:
				mdl.calculate_standOff_at_ithMidspan(self, ith)

		for i in range(self.lsCentralizerLocations_tableWidget.rowCount()):

			try:
				item = self.lsCentralizerLocations_tableWidget.item( i, self.lsCentralization_fields.MD.pos )
				item.set_text( self.lsCentralization_fields.MD[i] )
				item = self.lsCentralizerLocations_tableWidget.item( i, self.lsCentralization_fields.Inc.pos )
				item.set_text( self.lsCentralization_fields.Inc[i] )
				item = self.lsCentralizerLocations_tableWidget.item( i, self.lsCentralization_fields.SOatC.pos )
				item.set_text( self.lsCentralization_fields.SOatC[i] )
				item = self.lsCentralizerLocations_tableWidget.item( i, self.lsCentralization_fields.SOatM.pos )
				item.set_text( self.lsCentralization_fields.SOatM[i] )
				item = self.lsCentralizerLocations_tableWidget.item( i, self.lsCentralization_fields.Stage.pos )
				item.set_text( self.lsCentralization_fields.Stage[i] )

			except IndexError:
				item = self.lsCentralizerLocations_tableWidget.item( i, self.lsCentralization_fields.MD.pos )
				item.set_text()
				item = self.lsCentralizerLocations_tableWidget.item( i, self.lsCentralization_fields.Inc.pos )
				item.set_text()
				item = self.lsCentralizerLocations_tableWidget.item( i, self.lsCentralization_fields.SOatC.pos )
				item.set_text()
				item = self.lsCentralizerLocations_tableWidget.item( i, self.lsCentralization_fields.SOatM.pos )
				item.set_text()
				item = self.lsCentralizerLocations_tableWidget.item( i, self.lsCentralization_fields.Stage.pos )
				item.set_text()

		print(SOatC_field)
		print(SOatM_field)

		self.meanSOatC = mu.np.round( mu.np.mean(SOatC_field), 1 )
		self.meanSOatM = mu.np.round( mu.np.mean(SOatM_field), 1 )
		self.lsMeanSOatC_label.setText( 'Mean SO at centralizers:\t{mSOatC} {unit}'.format( mSOatC=self.meanSOatC, 
																							unit=SOatC_field.unit ) )
		self.lsMeanSOatM_label.setText( 'Mean SO at minspan:\t{mSOatM} {unit}'.format(  mSOatM=self.meanSOatM,
																						unit=SOatM_field.unit ) )
		cu.idleFunction()


	def choose_MDlocation(self, MD, overwrite=False):

		PL = mu.unitConvert_value( 480, 'in', self.lsCentralization_fields.MD.unit )
		MD = round(MD/PL)*PL

		if MD<self.min_MD or MD>self.max_MD:
			return

		if overwrite:
			r = self.lsCentralizerLocations_tableWidget.selectedRow
			gooD = mdl.put_location_to_CentralizationFields(self, r, MD)
			
		else:
			try:
				r = mu.np.where(mu.np.array(self.lsCentralization_fields.MD)>MD)[0][0]
			except IndexError:
				r = mu.np.where(mu.np.array(self.lsCentralization_fields.MD)<MD)[0][-1]+1
			gooD = mdl.insert_location_to_CentralizationFields(self, r, MD)
			self.centralizerCount+=1

		try:
			if gooD:
				indexes = mdl.get_indexes_for_shoosing(self, r)
				self.update_calculations(indexes=indexes)
				cu.select_tableWidgetRow(self.lsCentralizerLocations_tableWidget, r, alltherow=True)
				MD = self.lsCentralization_fields.MD[r]
				EW = self.lsCentralization_fields.EW[r]
				NS = self.lsCentralization_fields.NS[r]
				VD = self.lsCentralization_fields.TVD[r]
				HD = self.lsCentralization_fields.HD[r]
				ID = self.lsCentralization_fields.ID[r]
				self.draw_MDlocations(MD, EW, NS, VD, HD, ID)

			else:
				msg = "There are not centralizers defined in this region. \nThis action is going to be ignored."
				QMessageBox.critical(self.lsCentralizerLocations_tableWidget, 'Error', msg)
				return

		except mu.LogicalError:
			msg = "There is a logical error between centralizer locations and length.\nThe last entered location will be removed."
			QMessageBox.critical(self.lsCentralizerLocations_tableWidget, 'Error', msg)
			self.lsCentralization_fields.MD.pop(r)
			self.lsCentralization_fields.Inc.pop(r)
			self.lsCentralization_fields.SOatC.pop(r)
			self.lsCentralization_fields.SOatM.pop(r)
			self.lsCentralization_fields.ClatC.pop(r)
			self.lsCentralization_fields.ClatM.pop(r)
			self.lsCentralization_fields.AFatC.pop(r)
			self.lsCentralization_fields.AFatM.pop(r)
			self.lsCentralization_fields.SFatC.pop(r)
			self.lsCentralization_fields.SFatM.pop(r)
			self.lsCentralization_fields.LatC.pop(r)
			self.lsCentralization_fields.EW.pop(r)
			self.lsCentralization_fields.NS.pop(r)
			self.lsCentralization_fields.TVD.pop(r)
			self.lsCentralization_fields.HD.pop(r)
			self.lsCentralization_fields.DL.pop(r)
			self.lsCentralization_fields.ID.pop(r)
			self.lsCentralization_fields.avgID.pop(r)
			self.lsCentralization_fields.Azi.pop(r)
			self.lsCentralization_fields.Stage.pop(r)
			self.centralizerCount = len(self.lsCentralization_fields.MD)
			return
		

	def remove_location(self):

		r = self.lsCentralizerLocations_tableWidget.selectedRow
		self.lsCentralizerLocations_tableWidget.removeRow(r)

		print('removed',r)
		
		if r<self.centralizerCount:

			self.lsCentralization_fields.MD.pop(r)
			self.lsCentralization_fields.Inc.pop(r)
			self.lsCentralization_fields.SOatC.pop(r)
			self.lsCentralization_fields.SOatM.pop(r)
			self.lsCentralization_fields.ClatC.pop(r)
			self.lsCentralization_fields.ClatM.pop(r)
			self.lsCentralization_fields.AFatC.pop(r)
			self.lsCentralization_fields.AFatM.pop(r)
			self.lsCentralization_fields.SFatC.pop(r)
			self.lsCentralization_fields.SFatM.pop(r)
			self.lsCentralization_fields.LatC.pop(r)
			self.lsCentralization_fields.EW.pop(r)
			self.lsCentralization_fields.NS.pop(r)
			self.lsCentralization_fields.TVD.pop(r)
			self.lsCentralization_fields.HD.pop(r)
			self.lsCentralization_fields.DL.pop(r)
			self.lsCentralization_fields.ID.pop(r)
			self.lsCentralization_fields.avgID.pop(r)
			self.lsCentralization_fields.Azi.pop(r)
			self.lsCentralization_fields.Stage.pop(r)

			self.centralizerCount-=1

			s = r-1 if (r>0) else 0

			if self.centralizerCount>0:
				MD = self.lsCentralization_fields.MD[s]
				EW = self.lsCentralization_fields.EW[s]
				NS = self.lsCentralization_fields.NS[s]
				VD = self.lsCentralization_fields.TVD[s]
				HD = self.lsCentralization_fields.HD[s]
				ID = self.lsCentralization_fields.ID[s]

				cu.select_tableWidgetRow(self.lsCentralizerLocations_tableWidget,s)
				indexes = mdl.get_indexes_for_removing(self, r)
				self.update_calculations(indexes=indexes)
				self.draw_MDlocations(MD, EW, NS, VD, HD, ID)

			else:
				self.draw_MDlocations()


	def highlight_MDlocation(self, MD):

		index = mu.np.argmin( abs(mu.array(self.lsCentralization_fields.MD)-MD) )
		self.select_row( index, 0, alltherow=True )


	def draw_MDlocations(self, MD=None, EW=None, NS=None, VD=None, HD=None, ID=None, created=True, initial=False ):

		"""
		fieldlen = len(self.lsCentralization_fields.MD)
		print('MD',fieldlen)
		for field in self.lsCentralization_fields[1:]:
			print(field.abbreviation,len(field))
			assert( fieldlen==len(field) )
		print('-------------------------------------')
		"""

		xlim = self.lsCaliperMap_graphicsView.axes.get_xlim()	

		if MD!=None:

			del self.lsCaliperMap_graphicsView.axes.lines[3*self.numofStages:]
			del self.lsWellbore3D_graphicsView.axes.lines[1:]
			del self.lsSOVisualization_graphicsView.axes.lines[self.numofStages+3:]

			for MDi,IDi in zip(self.lsCentralization_fields.MD,self.lsCentralization_fields.ID):
				self.lsCaliperMap_graphicsView.axes.plot( [-IDi, +IDi], [MDi, MDi], color='C3', lw=1 ) #xlim

			self.lsCaliperMap_graphicsView.axes.plot( [-ID, +ID], [MD, MD], color='C3', lw=4, alpha=0.4 )
			
			self.lsWellbore3D_graphicsView.axes.plot( 	self.lsCentralization_fields.EW,
														self.lsCentralization_fields.NS,
														self.lsCentralization_fields.TVD, marker='o', color='C3', alpha=0.5, ls='' )
			
			self.lsWellbore3D_graphicsView.axes.plot( [EW],[NS],[VD], marker='o', mec='black', color='C3', ms='8' )

			MD_alt = []
			SO_alt = []
			for k in range(2*len(self.lsCentralization_fields.MD)-1):
				if k%2==0:
					MD_alt.append( self.lsCentralization_fields.MD[k//2] )
					SO_alt.append( self.lsCentralization_fields.SOatC[k//2] )
				elif k%2==1:
					MD_alt.append( (self.lsCentralization_fields.MD[(k+1)//2]+self.lsCentralization_fields.MD[(k-1)//2])/2 )
					SO_alt.append( self.lsCentralization_fields.SOatM[k//2] )

			self.lsSOVisualization_graphicsView.axes.plot(	SO_alt, MD_alt, marker='s', ms=5, color='C1', lw=1.5, alpha=0.7 )
			self.lsSOVisualization_graphicsView.axes.plot(	self.lsCentralization_fields.SOatC, 
															self.lsCentralization_fields.MD, marker='o', color='C3', alpha=0.5, ls='' )
				
			index = mu.np.where( mu.np.isclose(self.lsCentralization_fields.MD, MD) )[0][0]
			SOatC = self.lsCentralization_fields.SOatC[index]
			self.lsSOVisualization_graphicsView.axes.plot(	SOatC, MD, marker='o', mec='black', color='C3', ms='8' )
			if created:
				self.lsSOVisualization_graphicsView.axes.plot(	[0, self.max_SO], [MD, MD], color='C3', lw=4, alpha=0.4 )
			
			self.lsCaliperMap_graphicsView.draw()
			self.lsWellbore3D_graphicsView.draw()
			self.lsSOVisualization_graphicsView.draw()
			
			if created:
				cu.sleep(0.2)
				del self.lsSOVisualization_graphicsView.axes.lines[-1]
				self.lsSOVisualization_graphicsView.draw()
		
		elif initial:

			for MDi, IDi in zip( self.lsCentralization_fields.MD, self.lsCentralization_fields.ID):
				self.lsCaliperMap_graphicsView.axes.plot( [-IDi, +IDi], [MDi, MDi], color='C3', lw=1 )

			self.lsWellbore3D_graphicsView.axes.plot( 	self.lsCentralization_fields.EW,
														self.lsCentralization_fields.NS,
														self.lsCentralization_fields.TVD, marker='o', color='C3', alpha=0.5, ls='' )
			
			MD_alt = []
			SO_alt = []
			for k in range(2*len(self.lsCentralization_fields.MD)-1):
				if k%2==0:
					MD_alt.append( self.lsCentralization_fields.MD[k//2] )
					SO_alt.append( self.lsCentralization_fields.SOatC[k//2] )
				elif k%2==1:
					MD_alt.append( (self.lsCentralization_fields.MD[(k+1)//2]+self.lsCentralization_fields.MD[(k-1)//2])/2 )
					SO_alt.append( self.lsCentralization_fields.SOatM[k//2] )

			self.lsSOVisualization_graphicsView.axes.plot(	SO_alt, MD_alt, marker='s', ms=5, color='C1', lw=1.5, alpha=0.7 )
			self.lsSOVisualization_graphicsView.axes.plot(	self.lsCentralization_fields.SOatC, 
															self.lsCentralization_fields.MD, marker='o', color='C3', alpha=0.5, ls='' )
				
			self.lsCaliperMap_graphicsView.draw()
			self.lsWellbore3D_graphicsView.draw()
			self.lsSOVisualization_graphicsView.draw()
			self.lsSideForces_graphicsView.draw()

		else:
			self.lsCaliperMap_graphicsView.draw()
			self.lsWellbore3D_graphicsView.draw()
			self.lsSOVisualization_graphicsView.draw()
			self.lsSideForces_graphicsView.draw()

