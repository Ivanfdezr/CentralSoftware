from PyQt4 import QtCore, QtGui
from LocationSetup_Vst import Ui_LocationSetup
import LocationSetup_Vst as vst
import LocationSetup_Mdl as mdl
import CtrlUtilities as cu
import PlotUtilities as pu
import MdlUtilities as mu
import copy
import re, os

import importlib

class Main_LocationSetup(Ui_LocationSetup):

	def __init__(self, dialog, parent):
		
		importlib.reload(pu)
		importlib.reload(mdl)
		importlib.reload(vst)

		Ui_LocationSetup.__init__(self)
		self.setupUi(dialog)
		self.dialog = dialog
		self.parent = parent
		self.centralizerCount = 0

		self.lsCentralizerLocations_fields = mdl.get_lsCentralizerLocations_fields()
		mdl.calculate_axialForce_field(self)	

		self.__init__lsCentralizerLocations_tableWidget()
		self.lsCalculate_pushButton.clicked.connect( self.calculate_SO )

		self.stage = parent.currentWellboreInnerStageDataItem
		#if self.stage['row']>=1:
		#	row = self.stage['row']-1
		#	self.previousStage = parent.wellboreInnerStageData[row]
		#else:
		#	self.previousStage = None

		self.max_MD = self.stage['MD']
		self.min_MD = self.max_MD-self.stage['Length']
		self.IPOD = self.stage['PipeProps'].OD[0]
		#self.COD = parent.currentWellboreInnerStageDataItem['Centralization']['A']['CentralizerProps'].COD[0]

		centralizers = []
		centralizers.append( self.stage['Centralization']['A'] )
		centralizers.append( self.stage['Centralization']['B'] )
		centralizers.append( self.stage['Centralization']['C'] )

		self.centralizer1 = None
		self.centralizer2 = None
		for c in centralizers:
			if not self.centralizer1 and c:
				self.centralizer1 = c
			elif self.centralizer1 and c:
				self.centralizer2 = c
		if not self.centralizer2:
			self.centralizer2 = self.centralizer1

		MD, ID, lim_ID = mdl.get_LASMDandCALID_intoInterval(self)
		self.MD = MD
		self.ID = ID

		#self.lsCaliperMap_graphicsView.axes.set_position([0.23,0.1,0.7,0.85])
		self.lsCaliperMap_graphicsView_ylimits    = [None,None]
		self.lsCaliperMap_graphicsView_yselection = []
		zp = pu.ZoomPan()
		zp.zoomYD_factory(self.lsCaliperMap_graphicsView.axes, self.lsCaliperMap_graphicsView_ylimits)
		zp.panYD_factory( self.lsCaliperMap_graphicsView.axes, self.lsCaliperMap_graphicsView_ylimits, 
						  self.lsCaliperMap_graphicsView_yselection, self.choose_MDlocation )

		self.lsCaliperMap_graphicsView.axes.clear()
		#self.lsCaliperMap_graphicsView.axes.plot( +ID, MD, 'C0', alpha=0.6 )
		#self.lsCaliperMap_graphicsView.axes.plot( -ID, MD, 'C0', alpha=0.6 )

		self.lsCaliperMap_graphicsView.axes.fill_betweenx( MD, -ID, +ID, alpha=0.5, color='C0')
		factors = mu.np.linspace(1,2,11)
		for factor in factors[1:]:
			IPOD = self.IPOD*factor
			self.lsCaliperMap_graphicsView.axes.fill_betweenx( MD, +IPOD, +ID, where=IPOD<ID, alpha=0.05, color='C3')
			self.lsCaliperMap_graphicsView.axes.fill_betweenx( MD, -IPOD, -ID, where=IPOD<ID, alpha=0.05, color='C3')

		self.lsCaliperMap_graphicsView.axes.plot( [ -self.IPOD, -self.IPOD], [MD[0],MD[-1]], 'C1', lw=2 )
		self.lsCaliperMap_graphicsView.axes.plot( [ +self.IPOD, +self.IPOD], [MD[0],MD[-1]], 'C1', lw=2 )
		#self.lsCaliperMap_graphicsView.axes.plot( [ -self.COD,  -self.COD],  [MD[0],MD[-1]], 'C3--' )
		#self.lsCaliperMap_graphicsView.axes.plot( [ +self.COD,  +self.COD],  [MD[0],MD[-1]], 'C3--' )

		IDHeaderName = parent.currentWellboreOuterStageDataItem['WellboreProps'].MDtop.headerName
		MDHeaderName = parent.currentWellboreOuterStageDataItem['WellboreProps'].DriftID.headerName

		self.lsCaliperMap_graphicsView.axes.set_xlabel( IDHeaderName )
		self.lsCaliperMap_graphicsView.axes.set_ylabel( MDHeaderName )
		self.lsCaliperMap_graphicsView.axes.set_xlim( -lim_ID, lim_ID )
		self.lsCaliperMap_graphicsView.axes.set_ylim( self.max_MD, self.min_MD ) 
		self.lsCaliperMap_graphicsView.draw()

		min_EW,min_NS,min_VD,min_index = mdl.get_ASCCoordinates_from_MD(self, self.min_MD, unit=parent.s2DataSurvey_fields.MD.unit)
		max_EW,max_NS,max_VD,max_index = mdl.get_ASCCoordinates_from_MD(self, self.max_MD, unit=parent.s2DataSurvey_fields.MD.unit)
		EW = parent.s2DataSurvey_fields.EW[min_index:max_index+1]
		NS = parent.s2DataSurvey_fields.NS[min_index:max_index+1]
		VD = parent.s2DataSurvey_fields.TVD[min_index:max_index+1]
		
		print(self.min_MD, self.max_MD, min_index,max_index,parent.s2DataSurvey_fields)

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
		#zp = pu.ZoomPan()
		#zp.point3D_factory(self.s2TriDView_graphicsView.axes, dot, curve)
		zp.zoom3D_factory( self.lsWellbore3D_graphicsView.axes, curve )
		self.lsWellbore3D_graphicsView.draw()
		
		dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		dialog.exec_()


	def __init__lsCentralizerLocations_tableWidget(self):

		self.lsCentralizerLocations_tableWidget.parent = self
		self.lsCentralizerLocations_tableWidget.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
		
		C = cu.CopySelectedCells_action(self.lsCentralizerLocations_tableWidget)
		self.lsCentralizerLocations_tableWidget.addAction(C)
		
		V = cu.PasteToCells_action(self.lsCentralizerLocations_tableWidget)
		self.lsCentralizerLocations_tableWidget.addAction(V)

		clear_row = lambda: cu.clear_tableWidgetRow(self.lsCentralizerLocations_tableWidget)
		D = cu.FunctionToWidget_action(self.lsCentralizerLocations_tableWidget, clear_row, "Delete", 'Del')
		self.lsCentralizerLocations_tableWidget.addAction(D)

		#select_row = lambda r,c : cu.select_tableWidgetRow(self.lsCentralizerLocations_tableWidget,r)
		self.lsCentralizerLocations_tableWidget.cellPressed.connect(self.select_row)
		self.lsCentralizerLocations_tableWidget.itemChanged.connect(cu.update_fieldItem)

		for field in self.lsCentralizerLocations_fields[:4]:
			#
			item = self.lsCentralizerLocations_tableWidget.horizontalHeaderItem( field.pos )
			item.setText( field.headerName )
			
			for i in range(self.lsCentralizerLocations_tableWidget.rowCount()):
				item = cu.TableWidgetFieldItem( field, i%2==0 )
				self.lsCentralizerLocations_tableWidget.setItem(i, field.pos, item)

		self.lsCentralizerLocations_tableWidget.resizeColumnsToContents()


	def select_row(self, r, c):

		cu.select_tableWidgetRow(self.lsCentralizerLocations_tableWidget,r)
		
		if r<self.centralizerCount:
			del self.lsCaliperMap_graphicsView.axes.lines[-1]
			del self.lsWellbore3D_graphicsView.axes.lines[-1]

			MD = self.lsCentralizerLocations_fields.MD[r]
			EW = self.lsCentralizerLocations_fields.EW[r]
			NS = self.lsCentralizerLocations_fields.NS[r]
			TVD = self.lsCentralizerLocations_fields.TVD[r]

			xlim = self.lsCaliperMap_graphicsView.axes.get_xlim()
			self.lsCaliperMap_graphicsView.axes.plot( xlim, [MD, MD], 'C3', lw=4, alpha=0.4 )
			self.lsWellbore3D_graphicsView.axes.plot( [EW],[NS],[TVD], marker='o', mec='black', color='C3', ms='8' )
			self.lsCaliperMap_graphicsView.draw()
			self.lsWellbore3D_graphicsView.draw()


	def choose_MDlocation(self, MD):

		xlim = self.lsCaliperMap_graphicsView.axes.get_xlim()

		if MD>=self.min_MD and MD<=self.max_MD:

			if self.centralizerCount>0:
				del self.lsCaliperMap_graphicsView.axes.lines[-self.centralizerCount-1:]
				del self.lsWellbore3D_graphicsView.axes.lines[-2:]

			cu.create_physicalValue_and_appendTo_field( MD, self.lsCentralizerLocations_fields.MD )
			MD = self.lsCentralizerLocations_fields.MD[-1]
			self.lsCentralizerLocations_fields.MD.sort()
			self.lsCentralizerLocations_fields.EW.clear()
			self.lsCentralizerLocations_fields.NS.clear()
			self.lsCentralizerLocations_fields.TVD.clear()
			self.lsCentralizerLocations_fields.DL.clear()
			self.lsCentralizerLocations_fields.SOatC.clear()
			self.lsCentralizerLocations_fields.SOatM.clear()
			self.lsCentralizerLocations_fields.AxialF.clear()
			self.lsCentralizerLocations_fields.SideF.clear()
			self.centralizerCount = len(self.lsCentralizerLocations_fields.MD)

			#F = mdl.get_axialTension_below_MD(self, MD)
			##
			
			#mdl.calculate_standOff_atCentralizers(self)
			#mdl.calculate_standOff_atMidspan(self)

			for i, MDi in enumerate(self.lsCentralizerLocations_fields.MD):
				
				EWi,NSi,VDi,_ = mdl.get_ASCCoordinates_from_MD(self, MDi)
				DLi = mdl.get_ASCDogleg_from_MD(self, MDi)
				#SOi = mdl.get_standOff_for_MD(self, previousMDi, MDi)
				cu.create_physicalValue_and_appendTo_field( EWi, self.lsCentralizerLocations_fields.EW )
				cu.create_physicalValue_and_appendTo_field( NSi, self.lsCentralizerLocations_fields.NS )
				cu.create_physicalValue_and_appendTo_field( VDi, self.lsCentralizerLocations_fields.TVD )
				cu.create_physicalValue_and_appendTo_field( DLi, self.lsCentralizerLocations_fields.DL )

				item = self.lsCentralizerLocations_tableWidget.item( i, self.lsCentralizerLocations_fields.MD.pos )
				item.set_text( MDi )

				#item = self.lsCentralizerLocations_tableWidget.item( i, self.lsCentralizerLocations_fields.DL.pos )
				#item.set_text( DLi )

				self.lsCaliperMap_graphicsView.axes.plot( xlim, [MDi, MDi], color='C3', lw=1 )

				if MDi==MD:
					EW = EWi
					NS = NSi
					VD = VDi
					cu.select_tableWidgetRow(self.lsCentralizerLocations_tableWidget,i)

				previousMDi = MDi

			self.lsCaliperMap_graphicsView.axes.plot( xlim, [MD, MD], color='C3', lw=4, alpha=0.4 )
			#
			
			self.lsWellbore3D_graphicsView.axes.plot( 	self.lsCentralizerLocations_fields.EW,
														self.lsCentralizerLocations_fields.NS,
														self.lsCentralizerLocations_fields.TVD, marker='o', color='C3', alpha=0.5, ls='' )
			
			self.lsWellbore3D_graphicsView.axes.plot( [EW],[NS],[VD], marker='o', mec='black', color='C3', ms='8' )
			self.lsWellbore3D_graphicsView.draw()


	def calculate_SO(self):

		pass

		# self.lsCentralizerLocations_fields.MD.sort()
		# self.lsCentralizerLocations_fields.DL.clear()

		# for i,MD in enumerate(self.lsCentralizerLocations_fields.MD):
			
		# 	DL = mdl.get_ASCDogleg_from_MD(self, MD)
		# 	cu.create_physicalValue_and_appendTo_field( DL, self.lsCentralizerLocations_fields.DL )

		# 	item = self.lsCentralizerLocations_tableWidget.item( i, self.lsCentralizerLocations_fields.MD.pos )
		# 	item.set_text( MD )

		# 	item = self.lsCentralizerLocations_tableWidget.item( i, self.lsCentralizerLocations_fields.DL.pos )
		# 	item.set_text( DL)