from PyQt4 import QtCore, QtGui
from SpacingSetup_Vst import Ui_SpacingSetup
import SpacingSetup_Vst as vst
import SpacingSetup_Mdl as mdl
import InputWindow_Mdl as mdl2
import CtrlUtilities as cu
import PlotUtilities as pu
import MdlUtilities as mu
import copy
import re, os
import importlib
importlib.reload(mdl)

import time


class Main_SpacingSetup(Ui_SpacingSetup):

	def __init__(self, dialog, parent):
		
		Ui_SpacingSetup.__init__(self)
		zp = pu.ZoomPan()
		self.setupUi(dialog)
		self.dialog = dialog
		self.parent = parent
		self.centralizerCount = 0
		self.parent.msg_label.setText( 'Initializing Spacing setup window ...' )

		self.ssAccept_pushButton.clicked.connect( self.makeResults_and_done )

		self.ssNextSpacing_fields = mdl.get_ssNextSpacing_fields()
		self.ssCentralizerLocations_fields = mdl.get_ssCentralizerLocations_fields()
		#mdl.calculate_axialForce_field(self)	

		self.__init__ssCentralizerLocations_tableWidget()
		self.__init__ssNextSpacing_tableWidget()

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

		self.ssCaliperMap_graphicsView.axes.set_position([0.2,0.15,0.75,0.8])
		self.ssCaliperMap_graphicsView_ylimits    = [None,None]
		self.ssCaliperMap_graphicsView_yselection = []

		self.ssSOVisualization_graphicsView.axes.set_position([0.2,0.15,0.75,0.8])
		self.ssSOVisualization_graphicsView_ylimits    = [None,None]
		self.ssSOVisualization_graphicsView_yselection = []
		
		zp.zoomYD_factory(	(self.ssCaliperMap_graphicsView.axes, self.ssSOVisualization_graphicsView.axes),
							(self.ssCaliperMap_graphicsView_ylimits, self.ssSOVisualization_graphicsView_ylimits)  )
		zp.panYD_factory(	(self.ssCaliperMap_graphicsView.axes, self.ssSOVisualization_graphicsView.axes), 
							(self.ssCaliperMap_graphicsView_ylimits, self.ssSOVisualization_graphicsView_ylimits), 
							(self.ssCaliperMap_graphicsView_yselection, self.ssSOVisualization_graphicsView_yselection),
							self.choose_MDlocation )

		self.ssCaliperMap_graphicsView.axes.clear()
		self.ssSOVisualization_graphicsView.axes.clear()

		#-------------------------------------------------

		self.ssCaliperMap_graphicsView.axes.fill_betweenx( MD, -ID, +ID, alpha=0.5, color='C0')
		factors = mu.np.linspace(1,2,11)
		for factor in factors[1:]:
			IPOD = self.IPOD*factor
			self.ssCaliperMap_graphicsView.axes.fill_betweenx( MD, +IPOD, +ID, where=IPOD<ID, alpha=0.05, color='C3')
			self.ssCaliperMap_graphicsView.axes.fill_betweenx( MD, -IPOD, -ID, where=IPOD<ID, alpha=0.05, color='C3')

		self.ssCaliperMap_graphicsView.axes.plot( [ -self.IPOD, -self.IPOD], [MD[0],MD[-1]], 'C1', lw=2 )
		self.ssCaliperMap_graphicsView.axes.plot( [ +self.IPOD, +self.IPOD], [MD[0],MD[-1]], 'C1', lw=2 )

		MDHeaderName = self.ssCentralizerLocations_fields.MD.headerName
		IDHeaderName = parent.currentWellboreOuterStageDataItem['WellboreProps'].ID.headerName

		self.ssCaliperMap_graphicsView.axes.set_xlabel( IDHeaderName )
		self.ssCaliperMap_graphicsView.axes.set_ylabel( MDHeaderName )
		self.ssCaliperMap_graphicsView.axes.set_xlim( -lim_ID, lim_ID )
		self.ssCaliperMap_graphicsView.axes.set_ylim( self.max_MD, self.min_MD ) 
		self.ssCaliperMap_graphicsView.draw()

		#-------------------------------------------------

		SOHeaderName = self.ssCentralizerLocations_fields.SOatC.headerName +'  &  '+ self.ssCentralizerLocations_fields.SOatM.headerName
		if self.ssCentralizerLocations_fields.SOatC.unit=='%':
			self.max_SO = 100
			self.min_SO = 67
		elif self.ssCentralizerLocations_fields.SOatC.unit=='1':
			self.max_SO = 1
			self.min_SO = 0.67

		self.ssSOVisualization_graphicsView.axes.set_xlabel( SOHeaderName )
		self.ssSOVisualization_graphicsView.axes.set_ylabel( MDHeaderName )
		self.ssSOVisualization_graphicsView.axes.set_xlim( 0, self.max_SO )
		self.ssSOVisualization_graphicsView.axes.set_ylim( self.max_MD, self.min_MD )
		#self.ssSOVisualization_graphicsView.axes.grid()
		self.ssSOVisualization_graphicsView.axes.plot( [self.min_SO, self.min_SO], [self.max_MD, self.min_MD], 'C3--', lw=2 ) 
		self.ssSOVisualization_graphicsView.draw()

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

		curve, = self.ssWellbore3D_graphicsView.axes.plot( EW, NS, VD )

		self.ssWellbore3D_graphicsView.axes.set_xlabel( parent.s2DataSurvey_fields.EW.headerName )
		self.ssWellbore3D_graphicsView.axes.set_ylabel( parent.s2DataSurvey_fields.NS.headerName )
		self.ssWellbore3D_graphicsView.axes.set_zlabel( parent.s2DataSurvey_fields.TVD.headerName )

		max_EW = max(parent.s2DataSurvey_fields.EW)
		min_EW = min(parent.s2DataSurvey_fields.EW)
		max_NS = max(parent.s2DataSurvey_fields.NS)
		min_NS = min(parent.s2DataSurvey_fields.NS)
		ΔEW = max_EW - min_EW
		ΔNS = max_NS - min_NS

		if ΔEW>ΔNS:
			self.ssWellbore3D_graphicsView.axes.set_xlim( min_EW, max_EW )
			Δ = (ΔEW-ΔNS)/2
			self.ssWellbore3D_graphicsView.axes.set_ylim( min_NS-Δ, max_NS+Δ )
		elif ΔNS>ΔEW:
			self.ssWellbore3D_graphicsView.axes.set_ylim( min_NS, max_NS )
			Δ = (ΔNS-ΔEW)/2
			self.ssWellbore3D_graphicsView.axes.set_xlim( min_EW-Δ, max_EW+Δ )
		else:
			self.ssWellbore3D_graphicsView.axes.set_xlim( min_EW, max_EW )
			self.ssWellbore3D_graphicsView.axes.set_ylim( min_NS, max_NS )


		self.ssWellbore3D_graphicsView.axes.set_zlim( max(VD), min(VD) )
		self.ssWellbore3D_graphicsView.axes.mouse_init()
		#zp.point3D_factory(self.s2TriDView_graphicsView.axes, dot, curve)
		zp.zoom3D_factory( self.ssWellbore3D_graphicsView.axes, curve )
		self.ssWellbore3D_graphicsView.draw()
		
		#-------------------------------------------------

		#if self.parent.currentWellboreInnerStageDataItem['Centralization']['Fields']!=None:
		#	for MD in self.parent.currentWellboreInnerStageDataItem['Centralization']['Fields'].MD:
		#		self.choose_MDlocation(MD, singleLocating=True)

		self.parent.msg_label.setText( 'Finish' )
		cu.sleep(0.20)
		self.parent.msg_label.setText( '' )

		dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		dialog.exec_()


	def __init__ssNextSpacing_tableWidget(self):

		field = self.ssNextSpacing_fields[0]
		item = self.ssNextSpacing_tableWidget.verticalHeaderItem( field.pos )
		item.setText( field.headerName )
		item = cu.TableWidgetFieldItem( field, 0 )
		self.ssNextSpacing_tableWidget.setItem(field.pos, 0, item)

		#def update_through_itemChange(item):
		#	call_function = lambda: self.choose_MDlocation(item.realValue, overwrite=True)
		#	cu.update_fieldItem(item, call_function)

		self.ssNextSpacing_tableWidget.itemChanged.connect(cu.update_fieldItem)


	def __init__ssCentralizerLocations_tableWidget(self):

		self.ssCentralizerLocations_tableWidget.parent = self
		self.ssCentralizerLocations_tableWidget.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
		
		#C = cu.CopySelectedCells_action(self.ssCentralizerLocations_tableWidget)
		#self.ssCentralizerLocations_tableWidget.addAction(C)
		
		#V = cu.PasteToCells_action(self.ssCentralizerLocations_tableWidget)
		#self.ssCentralizerLocations_tableWidget.addAction(V)

		D = cu.FunctionToWidget_action(self.ssCentralizerLocations_tableWidget, self.remove_location, "Delete", 'Del')
		self.ssCentralizerLocations_tableWidget.addAction(D)

		#select_row = lambda r,c : cu.select_tableWidgetRow(self.ssCentralizerLocations_tableWidget,r)

		for field in self.ssCentralizerLocations_fields[:4]:
			#
			item = self.ssCentralizerLocations_tableWidget.horizontalHeaderItem( field.pos )
			item.setText( field.headerName )
			
			for i in range(self.ssCentralizerLocations_tableWidget.rowCount()):
				item = cu.TableWidgetFieldItem( field, i%2==0 )
				self.ssCentralizerLocations_tableWidget.setItem(i, field.pos, item)

		
		def update_through_itemChange(item):
			call_function = lambda: self.choose_MDlocation(item.realValue, overwrite=True)
			cu.update_fieldItem(item, call_function)

		self.ssCentralizerLocations_tableWidget.cellPressed.connect(self.select_row)
		self.ssCentralizerLocations_tableWidget.itemChanged.connect(update_through_itemChange)
		self.ssCentralizerLocations_tableWidget.resizeColumnsToContents()
		self.ssCentralizerLocations_tableWidget.selectedRow = None


	def makeResults_and_done(self):

		self.fields = self.ssCentralizerLocations_fields
		self.dialog.done(0)


	def remove_location(self):

		self.ssCentralizerLocations_fields.Inc.clear()
		self.ssCentralizerLocations_fields.SOatC.clear()
		self.ssCentralizerLocations_fields.SOatM.clear()
		self.ssCentralizerLocations_fields.ClatC.clear()
		self.ssCentralizerLocations_fields.ClatM.clear()
		self.ssCentralizerLocations_fields.LatC.clear()

		self.ssCentralizerLocations_fields.hsInc.clear()
		self.ssCentralizerLocations_fields.hsSOatC.clear()
		self.ssCentralizerLocations_fields.hsSOatM.clear()
		self.ssCentralizerLocations_fields.hsClatC.clear()
		self.ssCentralizerLocations_fields.hsClatM.clear()

		self.ssCentralizerLocations_fields.dsInc.clear()
		self.ssCentralizerLocations_fields.dsSOatC.clear()
		self.ssCentralizerLocations_fields.dsSOatM.clear()
		self.ssCentralizerLocations_fields.dsClatC.clear()
		self.ssCentralizerLocations_fields.dsClatM.clear()		

		r = self.ssCentralizerLocations_tableWidget.selectedRow
		self.ssCentralizerLocations_tableWidget.removeRow(r)
		
		if r<self.centralizerCount:
			
			rmMD = self.ssCentralizerLocations_fields.MD[r]
			
			where = mu.np.where( mu.np.isclose(self.ssCentralizerLocations_fields.hsMD, rmMD) )[0]
			
			if len(where)>0:
				del self.ssCentralizerLocations_fields.hsMD[ where[0] ]
			
			where = mu.np.where( mu.np.isclose(self.ssCentralizerLocations_fields.dsMD, rmMD) )[0]
			
			if len(where)>0:
				del self.ssCentralizerLocations_fields.dsMD[ where[0] ]

			del self.ssCentralizerLocations_fields.MD[r]
			del self.ssCentralizerLocations_fields.EW[r]
			del self.ssCentralizerLocations_fields.NS[r]
			del self.ssCentralizerLocations_fields.TVD[r]
			del self.ssCentralizerLocations_fields.DL[r]
			self.centralizerCount-=1

			r = r-1 if (r>0) else 0

			if self.centralizerCount>0:
				MD = self.ssCentralizerLocations_fields.MD[r]
				EW = self.ssCentralizerLocations_fields.EW[r]
				NS = self.ssCentralizerLocations_fields.NS[r]
				VD = self.ssCentralizerLocations_fields.TVD[r]

				cu.select_tableWidgetRow(self.ssCentralizerLocations_tableWidget,r)
				self.update_calculations()
				self.draw_MDlocations(MD, EW, NS, VD)

			else:
				self.draw_MDlocations()


	def select_row(self, r, c):

		cu.select_tableWidgetRow(self.ssCentralizerLocations_tableWidget,r)
		
		if r<self.centralizerCount:
			MD = self.ssCentralizerLocations_fields.MD[r]
			EW = self.ssCentralizerLocations_fields.EW[r]
			NS = self.ssCentralizerLocations_fields.NS[r]
			VD = self.ssCentralizerLocations_fields.TVD[r]

			self.draw_MDlocations(MD, EW, NS, VD, False)


	def update_calculations(self):

		locations = self.ssCentralizerLocations_fields.hsMD
		SOatC_field = self.ssCentralizerLocations_fields.hsSOatC
		ClatC_field = self.ssCentralizerLocations_fields.hsClatC
		SOatM_field = self.ssCentralizerLocations_fields.hsSOatM
		ClatM_field = self.ssCentralizerLocations_fields.hsClatM

		mdl.calculate_standOff_atCentralizers(self, locations, SOatC_field, ClatC_field)
		mdl.calculate_standOff_atMidspan(self, locations, ClatC_field, SOatM_field, ClatM_field)

		locations = self.ssCentralizerLocations_fields.dsMD
		SOatC_field = self.ssCentralizerLocations_fields.dsSOatC
		ClatC_field = self.ssCentralizerLocations_fields.dsClatC
		SOatM_field = self.ssCentralizerLocations_fields.dsSOatM
		ClatM_field = self.ssCentralizerLocations_fields.dsClatM

		mdl.calculate_standOff_atCentralizers(self, locations, SOatC_field, ClatC_field)
		mdl.calculate_standOff_atMidspan(self, locations, ClatC_field, SOatM_field, ClatM_field)

		locations = self.ssCentralizerLocations_fields.MD
		SOatC_field = self.ssCentralizerLocations_fields.SOatC
		ClatC_field = self.ssCentralizerLocations_fields.ClatC
		SOatM_field = self.ssCentralizerLocations_fields.SOatM
		ClatM_field = self.ssCentralizerLocations_fields.ClatM
		LatC_field = self.ssCentralizerLocations_fields.LatC

		mdl.calculate_standOff_atCentralizers(self, locations, SOatC_field, ClatC_field, LatC_field)
		mdl.calculate_standOff_atMidspan(self, locations, ClatC_field, SOatM_field, ClatM_field)

		for i in range(self.ssCentralizerLocations_tableWidget.rowCount()):

			try:
				item = self.ssCentralizerLocations_tableWidget.item( i, self.ssCentralizerLocations_fields.Inc.pos )
				item.set_text( self.ssCentralizerLocations_fields.Inc[i] )
				item = self.ssCentralizerLocations_tableWidget.item( i, self.ssCentralizerLocations_fields.SOatC.pos )
				item.set_text( self.ssCentralizerLocations_fields.SOatC[i] )
				item = self.ssCentralizerLocations_tableWidget.item( i, self.ssCentralizerLocations_fields.SOatM.pos )
				item.set_text( self.ssCentralizerLocations_fields.SOatM[i] )

			except IndexError:
				item = self.ssCentralizerLocations_tableWidget.item( i, self.ssCentralizerLocations_fields.Inc.pos )
				item.set_text()
				item = self.ssCentralizerLocations_tableWidget.item( i, self.ssCentralizerLocations_fields.SOatC.pos )
				item.set_text()
				item = self.ssCentralizerLocations_tableWidget.item( i, self.ssCentralizerLocations_fields.SOatM.pos )
				item.set_text()


	def choose_MDlocation(self, MD, overwrite=False, singleLocating=False):

		if MD>=self.min_MD and MD<=self.max_MD:

			if overwrite:
				r = self.ssCentralizerLocations_tableWidget.selectedRow
				if r<len(self.ssCentralizerLocations_fields.MD):
					del self.ssCentralizerLocations_fields.MD[r]

			#if singleLocating:
			#	mu.create_physicalValue_and_appendTo_field( MD, self.ssCentralizerLocations_fields.MD )
			#	MD = self.ssCentralizerLocations_fields.MD[-1]
			#	self.ssCentralizerLocations_fields.MD.sort()
			#else:
			MD = mdl.set_newSpacedLocations_under_MD_with_variations(self, MD)

			self.ssCentralizerLocations_fields.EW.clear()
			self.ssCentralizerLocations_fields.NS.clear()
			self.ssCentralizerLocations_fields.TVD.clear()
			self.ssCentralizerLocations_fields.DL.clear()
			self.ssCentralizerLocations_fields.Inc.clear()
			self.ssCentralizerLocations_fields.SOatC.clear()
			self.ssCentralizerLocations_fields.SOatM.clear()
			self.ssCentralizerLocations_fields.ClatC.clear()
			self.ssCentralizerLocations_fields.ClatM.clear()
			self.ssCentralizerLocations_fields.LatC.clear()
			self.centralizerCount = len(self.ssCentralizerLocations_fields.MD)

			for i in range(self.ssCentralizerLocations_tableWidget.rowCount()):
					
				try:
					MDi = self.ssCentralizerLocations_fields.MD[i]
					EWi,NSi,VDi,_ = mdl2.get_ASCCoordinates_from_MD(self.parent, MDi)
					DLi = mdl2.get_ASCDogleg_from_MD(self.parent, MDi)
					
					mu.create_physicalValue_and_appendTo_field( EWi, self.ssCentralizerLocations_fields.EW )
					mu.create_physicalValue_and_appendTo_field( NSi, self.ssCentralizerLocations_fields.NS )
					mu.create_physicalValue_and_appendTo_field( VDi, self.ssCentralizerLocations_fields.TVD )
					mu.create_physicalValue_and_appendTo_field( DLi, self.ssCentralizerLocations_fields.DL )

					item = self.ssCentralizerLocations_tableWidget.item( i, self.ssCentralizerLocations_fields.MD.pos )
					item.set_text( MDi )
					if MDi==MD:
						EW = EWi
						NS = NSi
						VD = VDi
						cu.select_tableWidgetRow(self.ssCentralizerLocations_tableWidget,i)

				except IndexError:
					item = self.ssCentralizerLocations_tableWidget.item( i, self.ssCentralizerLocations_fields.MD.pos )
					item.set_text()

			self.update_calculations()
			self.draw_MDlocations(MD, EW, NS, VD)	


	def draw_MDlocations(self, MD=None, EW=None, NS=None, VD=None, created=True):

		xlim = self.ssCaliperMap_graphicsView.axes.get_xlim()

		del self.ssCaliperMap_graphicsView.axes.lines[2:]
		del self.ssWellbore3D_graphicsView.axes.lines[1:]
		del self.ssSOVisualization_graphicsView.axes.lines[1:]
		del self.ssSOVisualization_graphicsView.axes.collections[:]

		if MD!=None:

			for MDi in self.ssCentralizerLocations_fields.MD:
				self.ssCaliperMap_graphicsView.axes.plot( xlim, [MDi, MDi], color='C3', lw=1 )

			self.ssCaliperMap_graphicsView.axes.plot( xlim, [MD, MD], color='C3', lw=4, alpha=0.4 )
			
			self.ssWellbore3D_graphicsView.axes.plot( 	self.ssCentralizerLocations_fields.EW,
														self.ssCentralizerLocations_fields.NS,
														self.ssCentralizerLocations_fields.TVD, marker='o', color='C3', alpha=0.5, ls='' )
			
			self.ssWellbore3D_graphicsView.axes.plot( [EW],[NS],[VD], marker='o', mec='black', color='C3', ms='8' )

			MD_alt = []
			SO_alt = []
			for k in range(2*len(self.ssCentralizerLocations_fields.MD)-1):
				if k%2==0:
					MD_alt.append( self.ssCentralizerLocations_fields.MD[k//2] )
					SO_alt.append( self.ssCentralizerLocations_fields.SOatC[k//2] )
				elif k%2==1:
					MD_alt.append( (self.ssCentralizerLocations_fields.MD[(k+1)//2]+self.ssCentralizerLocations_fields.MD[(k-1)//2])/2 )
					SO_alt.append( self.ssCentralizerLocations_fields.SOatM[k//2] )

			self.ssSOVisualization_graphicsView.axes.plot(	SO_alt, MD_alt, 'C1', lw=2 )

			hsMD_alt = []
			hsSO_alt = []
			for k in range(2*len(self.ssCentralizerLocations_fields.hsMD)-1):
				if k%2==0:
					hsMD_alt.append( self.ssCentralizerLocations_fields.hsMD[k//2] )
					hsSO_alt.append( self.ssCentralizerLocations_fields.hsSOatC[k//2] )
				elif k%2==1:
					hsMD_alt.append( (self.ssCentralizerLocations_fields.hsMD[(k+1)//2]+self.ssCentralizerLocations_fields.hsMD[(k-1)//2])/2 )
					hsSO_alt.append( self.ssCentralizerLocations_fields.hsSOatM[k//2] )

			self.ssSOVisualization_graphicsView.axes.plot(	hsSO_alt, hsMD_alt, 'C2', lw=1 )

			dsMD_alt = []
			dsSO_alt = []
			for k in range(2*len(self.ssCentralizerLocations_fields.dsMD)-1):
				if k%2==0:
					dsMD_alt.append( self.ssCentralizerLocations_fields.dsMD[k//2] )
					dsSO_alt.append( self.ssCentralizerLocations_fields.dsSOatC[k//2] )
				elif k%2==1:
					dsMD_alt.append( (self.ssCentralizerLocations_fields.dsMD[(k+1)//2]+self.ssCentralizerLocations_fields.dsMD[(k-1)//2])/2 )
					dsSO_alt.append( self.ssCentralizerLocations_fields.dsSOatM[k//2] )

			#self.ssSOVisualization_graphicsView.axes.plot(	SO_alt, MD_alt, 'C0', lw=1 )

			dsSO_int = mu.np.interp(hsMD_alt, dsMD_alt, dsSO_alt)

			self.ssSOVisualization_graphicsView.axes.fill_betweenx( hsMD_alt, hsSO_alt, dsSO_int, alpha=0.5, color='C0')


			self.ssSOVisualization_graphicsView.axes.plot(	self.ssCentralizerLocations_fields.SOatC, 
															self.ssCentralizerLocations_fields.MD, marker='o', color='C3', alpha=0.5, ls='' )
			
			index = mu.np.where( mu.np.isclose(self.ssCentralizerLocations_fields.MD, MD) )[0][0]
			SOatC = self.ssCentralizerLocations_fields.SOatC[index]
			self.ssSOVisualization_graphicsView.axes.plot(	SOatC, MD, marker='o', mec='black', color='C3', ms='8' )
			if created:
				self.ssSOVisualization_graphicsView.axes.plot(	[0, self.max_SO], [MD, MD], color='C3', lw=4, alpha=0.4 )
			
			self.ssCaliperMap_graphicsView.draw()
			self.ssWellbore3D_graphicsView.draw()
			self.ssSOVisualization_graphicsView.draw()
			
			if created:
				cu.sleep(0.2)
				del self.ssSOVisualization_graphicsView.axes.lines[-1]
				self.ssSOVisualization_graphicsView.draw()
		
		else:
			self.ssCaliperMap_graphicsView.draw()
			self.ssWellbore3D_graphicsView.draw()
			self.ssSOVisualization_graphicsView.draw()

		#print(	self.ssSOVisualization_graphicsView.axes,
		#		self.ssSOVisualization_graphicsView.axes.lines,
		#		self.ssSOVisualization_graphicsView.axes.patch,
		#		self.ssSOVisualization_graphicsView.axes.collections )

