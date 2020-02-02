from PyQt4 import QtCore, QtGui
from LocationSetup_Vst import Ui_LocationSetup
import LocationSetup_Vst as vst
import LocationSetup_Mdl as mdl
import InputWindow_Mdl as mdl2
import CtrlUtilities as cu
import PlotUtilities as pu
import MdlUtilities as mu
import copy
import re, os

import time

class Main_LocationSetup(Ui_LocationSetup):

	def __init__(self, dialog, parent):

		Ui_LocationSetup.__init__(self)
		zp = pu.ZoomPan()
		self.setupUi(dialog)
		self.dialog = dialog
		self.parent = parent
		self.centralizerCount = 0

		self.lsAccept_pushButton.clicked.connect( self.makeResults_and_done )

		self.lsCentralizerLocations_fields = mdl.get_lsCentralizerLocations_fields()
		#mdl.calculate_axialForce_field(self)	

		self.__init__lsCentralizerLocations_tableWidget()
		#self.lsCalculate_pushButton.clicked.connect( self.calculate_SO )

		self.stage = parent.currentWellboreInnerStageDataItem

		self.max_MD = self.stage['MD']
		self.min_MD = self.max_MD-self.stage['Length']
		self.IPOD = self.stage['PipeProps'].OD[0]

		self.centralizers = copy.deepcopy(self.stage['Centralization'])
		del self.centralizers['Mode']
		del self.centralizers['Fields']

		MD, ID, mean_ID, lim_ID = mdl.get_LASMDandCALID_intoInterval(self)
		self.MD = MD
		self.ID = ID
		self.mean_ID = mean_ID

		#-------------------------------------------------

		self.lsCaliperMap_graphicsView.axes.set_position([0.2,0.15,0.75,0.8])
		self.lsCaliperMap_graphicsView_ylimits    = [None,None]
		self.lsCaliperMap_graphicsView_yselection = []

		self.lsSOVisualization_graphicsView.axes.set_position([0.2,0.15,0.75,0.8])
		self.lsSOVisualization_graphicsView_ylimits    = [None,None]
		self.lsSOVisualization_graphicsView_yselection = []
		
		zp.zoomYD_factory(	(self.lsCaliperMap_graphicsView.axes, self.lsSOVisualization_graphicsView.axes),
							(self.lsCaliperMap_graphicsView_ylimits, self.lsSOVisualization_graphicsView_ylimits)  )
		zp.panYD_factory(	(self.lsCaliperMap_graphicsView.axes, self.lsSOVisualization_graphicsView.axes), 
							(self.lsCaliperMap_graphicsView_ylimits, self.lsSOVisualization_graphicsView_ylimits), 
							(self.lsCaliperMap_graphicsView_yselection, self.lsSOVisualization_graphicsView_yselection),
							self.choose_MDlocation )

		self.lsCaliperMap_graphicsView.axes.clear()
		self.lsSOVisualization_graphicsView.axes.clear()

		#-------------------------------------------------

		self.lsCaliperMap_graphicsView.axes.fill_betweenx( MD, -ID, +ID, alpha=0.5, color='C0')
		factors = mu.np.linspace(1,2,11)
		for factor in factors[1:]:
			IPOD = self.IPOD*factor
			self.lsCaliperMap_graphicsView.axes.fill_betweenx( MD, +IPOD, +ID, where=IPOD<ID, alpha=0.05, color='C3')
			self.lsCaliperMap_graphicsView.axes.fill_betweenx( MD, -IPOD, -ID, where=IPOD<ID, alpha=0.05, color='C3')

		self.lsCaliperMap_graphicsView.axes.plot( [ -self.IPOD, -self.IPOD], [MD[0],MD[-1]], 'C1', lw=2 )
		self.lsCaliperMap_graphicsView.axes.plot( [ +self.IPOD, +self.IPOD], [MD[0],MD[-1]], 'C1', lw=2 )

		MDHeaderName = self.lsCentralizerLocations_fields.MD.headerName
		IDHeaderName = parent.currentWellboreOuterStageDataItem['WellboreProps'].ID.headerName

		self.lsCaliperMap_graphicsView.axes.set_xlabel( IDHeaderName )
		self.lsCaliperMap_graphicsView.axes.set_ylabel( MDHeaderName )
		self.lsCaliperMap_graphicsView.axes.set_xlim( -lim_ID, lim_ID )
		self.lsCaliperMap_graphicsView.axes.set_ylim( self.max_MD, self.min_MD ) 
		self.lsCaliperMap_graphicsView.draw()

		#-------------------------------------------------

		SOHeaderName = self.lsCentralizerLocations_fields.SOatC.headerName +'  &  '+ self.lsCentralizerLocations_fields.SOatM.headerName
		if self.lsCentralizerLocations_fields.SOatC.unit=='%':
			self.max_SO = 100
			self.min_SO = 67
		elif self.lsCentralizerLocations_fields.SOatC.unit=='1':
			self.max_SO = 1
			self.min_SO = 0.67

		self.lsSOVisualization_graphicsView.axes.set_xlabel( SOHeaderName )
		self.lsSOVisualization_graphicsView.axes.set_ylabel( MDHeaderName )
		self.lsSOVisualization_graphicsView.axes.set_xlim( 0, self.max_SO )
		self.lsSOVisualization_graphicsView.axes.set_ylim( self.max_MD, self.min_MD )
		#self.lsSOVisualization_graphicsView.axes.grid()
		self.lsSOVisualization_graphicsView.axes.plot( [self.min_SO, self.min_SO], [self.max_MD, self.min_MD], 'C3--', lw=2 ) 
		self.lsSOVisualization_graphicsView.draw()

		#-------------------------------------------------

		min_EW,min_NS,min_VD,min_index = mdl2.get_ASCCoordinates_from_MD(parent, self.min_MD, unit=parent.s2DataSurvey_fields.MD.unit)
		max_EW,max_NS,max_VD,max_index = mdl2.get_ASCCoordinates_from_MD(parent, self.max_MD, unit=parent.s2DataSurvey_fields.MD.unit)
		EW = parent.s2DataSurvey_fields.EW[min_index:max_index+1]
		NS = parent.s2DataSurvey_fields.NS[min_index:max_index+1]
		VD = parent.s2DataSurvey_fields.TVD[min_index:max_index+1]
		
		EW[0] = min_EW
		NS[0] = min_NS
		VD[0] = min_VD
		EW[-1] = max_EW
		NS[-1] = max_NS
		VD[-1] = max_VD

		curve, = self.lsWellbore3D_graphicsView.axes.plot( EW, NS, VD )

		self.lsWellbore3D_graphicsView.axes.set_xlabel( parent.s2DataSurvey_fields.EW.headerName )
		self.lsWellbore3D_graphicsView.axes.set_ylabel( parent.s2DataSurvey_fields.NS.headerName )
		self.lsWellbore3D_graphicsView.axes.set_zlabel( parent.s2DataSurvey_fields.TVD.headerName )

		max_EW = max(parent.s2DataSurvey_fields.EW)
		min_EW = min(parent.s2DataSurvey_fields.EW)
		max_NS = max(parent.s2DataSurvey_fields.NS)
		min_NS = min(parent.s2DataSurvey_fields.NS)
		ΔEW = max_EW - min_EW
		ΔNS = max_NS - min_NS

		if ΔEW>ΔNS:
			self.lsWellbore3D_graphicsView.axes.set_xlim( min_EW, max_EW )
			Δ = (ΔEW-ΔNS)/2
			self.lsWellbore3D_graphicsView.axes.set_ylim( min_NS-Δ, max_NS+Δ )
		elif ΔNS>ΔEW:
			self.lsWellbore3D_graphicsView.axes.set_ylim( min_NS, max_NS )
			Δ = (ΔNS-ΔEW)/2
			self.lsWellbore3D_graphicsView.axes.set_xlim( min_EW-Δ, max_EW+Δ )
		else:
			self.lsWellbore3D_graphicsView.axes.set_xlim( min_EW, max_EW )
			self.lsWellbore3D_graphicsView.axes.set_ylim( min_NS, max_NS )


		self.lsWellbore3D_graphicsView.axes.set_zlim( max(VD), min(VD) )
		self.lsWellbore3D_graphicsView.axes.mouse_init()
		#zp.point3D_factory(self.s2TriDView_graphicsView.axes, dot, curve)
		zp.zoom3D_factory( self.lsWellbore3D_graphicsView.axes, curve )
		self.lsWellbore3D_graphicsView.draw()
		
		#-------------------------------------------------

		if self.parent.currentWellboreInnerStageDataItem['Centralization']['Fields']!=None:
			for MD in self.parent.currentWellboreInnerStageDataItem['Centralization']['Fields'].MD:
				self.choose_MDlocation(MD)

		dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		dialog.exec_()


	def __init__lsCentralizerLocations_tableWidget(self):

		self.lsCentralizerLocations_tableWidget.parent = self
		self.lsCentralizerLocations_tableWidget.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
		
		#C = cu.CopySelectedCells_action(self.lsCentralizerLocations_tableWidget)
		#self.lsCentralizerLocations_tableWidget.addAction(C)
		
		#V = cu.PasteToCells_action(self.lsCentralizerLocations_tableWidget)
		#self.lsCentralizerLocations_tableWidget.addAction(V)

		D = cu.FunctionToWidget_action(self.lsCentralizerLocations_tableWidget, self.remove_location, "Delete", 'Del')
		self.lsCentralizerLocations_tableWidget.addAction(D)

		#select_row = lambda r,c : cu.select_tableWidgetRow(self.lsCentralizerLocations_tableWidget,r)

		for field in self.lsCentralizerLocations_fields[:4]:
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

		self.fields = self.lsCentralizerLocations_fields
		self.dialog.done(0)


	def remove_location(self):

		self.lsCentralizerLocations_fields.Inc.clear()
		self.lsCentralizerLocations_fields.SOatC.clear()
		self.lsCentralizerLocations_fields.SOatM.clear()
		self.lsCentralizerLocations_fields.ClatC.clear()
		self.lsCentralizerLocations_fields.ClatM.clear()
		r = self.lsCentralizerLocations_tableWidget.selectedRow
		self.lsCentralizerLocations_tableWidget.removeRow(r)
		
		if r<self.centralizerCount:
			del self.lsCentralizerLocations_fields.MD[r]
			del self.lsCentralizerLocations_fields.EW[r]
			del self.lsCentralizerLocations_fields.NS[r]
			del self.lsCentralizerLocations_fields.TVD[r]
			del self.lsCentralizerLocations_fields.DL[r]
			self.centralizerCount-=1

			r = r-1 if (r>0) else 0

			if self.centralizerCount>0:
				MD = self.lsCentralizerLocations_fields.MD[r]
				EW = self.lsCentralizerLocations_fields.EW[r]
				NS = self.lsCentralizerLocations_fields.NS[r]
				VD = self.lsCentralizerLocations_fields.TVD[r]

				cu.select_tableWidgetRow(self.lsCentralizerLocations_tableWidget,r)
				self.update_calculations()
				self.draw_MDlocations(MD, EW, NS, VD)

			else:
				self.draw_MDlocations()


	def select_row(self, r, c):

		cu.select_tableWidgetRow(self.lsCentralizerLocations_tableWidget,r)
		
		if r<self.centralizerCount:
			MD = self.lsCentralizerLocations_fields.MD[r]
			EW = self.lsCentralizerLocations_fields.EW[r]
			NS = self.lsCentralizerLocations_fields.NS[r]
			VD = self.lsCentralizerLocations_fields.TVD[r]

			self.draw_MDlocations(MD, EW, NS, VD, False)


	def update_calculations(self):
		tic = time.time()
		mdl.calculate_standOff_atCentralizers(self)
		tac = time.time()
		mdl.calculate_standOff_atMidspan(self)
		toc = time.time()

		print('mid:',toc-tac,'cent:',tac-tic)

		for i, inc in enumerate(self.lsCentralizerLocations_fields.Inc):

			SOatCi = self.lsCentralizerLocations_fields.SOatC[i]
			SOatMi = self.lsCentralizerLocations_fields.SOatM[i]

			item = self.lsCentralizerLocations_tableWidget.item( i, self.lsCentralizerLocations_fields.Inc.pos )
			item.set_text( inc )
			item = self.lsCentralizerLocations_tableWidget.item( i, self.lsCentralizerLocations_fields.SOatC.pos )
			item.set_text( SOatCi )
			item = self.lsCentralizerLocations_tableWidget.item( i, self.lsCentralizerLocations_fields.SOatM.pos )
			item.set_text( SOatMi )	


	def choose_MDlocation(self, MD, overwrite=False):

		if MD>=self.min_MD and MD<=self.max_MD:

			if overwrite:
				r = self.lsCentralizerLocations_tableWidget.selectedRow
				if r<len(self.lsCentralizerLocations_fields.MD):
					del self.lsCentralizerLocations_fields.MD[r]

			cu.create_physicalValue_and_appendTo_field( MD, self.lsCentralizerLocations_fields.MD )
			MD = self.lsCentralizerLocations_fields.MD[-1]
			self.lsCentralizerLocations_fields.MD.sort()
			self.lsCentralizerLocations_fields.EW.clear()
			self.lsCentralizerLocations_fields.NS.clear()
			self.lsCentralizerLocations_fields.TVD.clear()
			self.lsCentralizerLocations_fields.DL.clear()
			self.lsCentralizerLocations_fields.Inc.clear()
			self.lsCentralizerLocations_fields.SOatC.clear()
			self.lsCentralizerLocations_fields.SOatM.clear()
			self.lsCentralizerLocations_fields.ClatC.clear()
			self.lsCentralizerLocations_fields.ClatM.clear()
			self.centralizerCount = len(self.lsCentralizerLocations_fields.MD)

			for i, MDi in enumerate(self.lsCentralizerLocations_fields.MD):
					
				EWi,NSi,VDi,_ = mdl2.get_ASCCoordinates_from_MD(self.parent, MDi)
				DLi = mdl2.get_ASCDogleg_from_MD(self.parent, MDi)
				
				cu.create_physicalValue_and_appendTo_field( EWi, self.lsCentralizerLocations_fields.EW )
				cu.create_physicalValue_and_appendTo_field( NSi, self.lsCentralizerLocations_fields.NS )
				cu.create_physicalValue_and_appendTo_field( VDi, self.lsCentralizerLocations_fields.TVD )
				cu.create_physicalValue_and_appendTo_field( DLi, self.lsCentralizerLocations_fields.DL )

				item = self.lsCentralizerLocations_tableWidget.item( i, self.lsCentralizerLocations_fields.MD.pos )
				item.set_text( MDi )
				if MDi==MD:
					EW = EWi
					NS = NSi
					VD = VDi
					cu.select_tableWidgetRow(self.lsCentralizerLocations_tableWidget,i)

			self.update_calculations()
			self.draw_MDlocations(MD, EW, NS, VD)


			#F = mdl.get_axialTension_below_MD(self, MD)
			##
			
			#mdl.calculate_standOff_atCentralizers(self)
			#mdl.calculate_standOff_atMidspan(self)		


	def draw_MDlocations(self, MD=None, EW=None, NS=None, VD=None, created=True):

		xlim = self.lsCaliperMap_graphicsView.axes.get_xlim()

		del self.lsCaliperMap_graphicsView.axes.lines[2:]
		del self.lsWellbore3D_graphicsView.axes.lines[1:]
		del self.lsSOVisualization_graphicsView.axes.lines[1:]

		if MD!=None:

			for MDi in self.lsCentralizerLocations_fields.MD:
				self.lsCaliperMap_graphicsView.axes.plot( xlim, [MDi, MDi], color='C3', lw=1 )

			self.lsCaliperMap_graphicsView.axes.plot( xlim, [MD, MD], color='C3', lw=4, alpha=0.4 )
			
			self.lsWellbore3D_graphicsView.axes.plot( 	self.lsCentralizerLocations_fields.EW,
														self.lsCentralizerLocations_fields.NS,
														self.lsCentralizerLocations_fields.TVD, marker='o', color='C3', alpha=0.5, ls='' )
			
			self.lsWellbore3D_graphicsView.axes.plot( [EW],[NS],[VD], marker='o', mec='black', color='C3', ms='8' )

			MD_alt = []
			SO_alt = []
			for k in range(2*len(self.lsCentralizerLocations_fields.MD)-1):
				if k%2==0:
					MD_alt.append( self.lsCentralizerLocations_fields.MD[k//2] )
					SO_alt.append( self.lsCentralizerLocations_fields.SOatC[k//2] )
				elif k%2==1:
					MD_alt.append( (self.lsCentralizerLocations_fields.MD[(k+1)//2]+self.lsCentralizerLocations_fields.MD[(k-1)//2])/2 )
					SO_alt.append( self.lsCentralizerLocations_fields.SOatM[(k+1)//2] )

			self.lsSOVisualization_graphicsView.axes.plot(	SO_alt, MD_alt, 'C1', lw=2 )
			self.lsSOVisualization_graphicsView.axes.plot(	self.lsCentralizerLocations_fields.SOatC, 
															self.lsCentralizerLocations_fields.MD, marker='o', color='C3', alpha=0.5, ls='' )
				
			index = mu.np.where( mu.np.isclose(self.lsCentralizerLocations_fields.MD, MD) )[0][0]
			SOatC = self.lsCentralizerLocations_fields.SOatC[index]
			#SOatC = self.lsCentralizerLocations_fields.SOatC[self.lsCentralizerLocations_fields.MD.index(MD) ]
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

		
		else:
			self.lsCaliperMap_graphicsView.draw()
			self.lsWellbore3D_graphicsView.draw()
			self.lsSOVisualization_graphicsView.draw()

