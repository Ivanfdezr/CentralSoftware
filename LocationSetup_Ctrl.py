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


class Main_LocationSetup(Ui_LocationSetup):

	@cu.waiting_effects
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
		
		zp.zoomYD_factory(	(self.lsCaliperMap_graphicsView.axes, self.lsSOVisualization_graphicsView.axes),
							(self.lsCaliperMap_graphicsView_ylimits, self.lsSOVisualization_graphicsView_ylimits)  )
		zp.panYD_factory(	(self.lsCaliperMap_graphicsView.axes, self.lsSOVisualization_graphicsView.axes), 
							(self.lsCaliperMap_graphicsView_ylimits, self.lsSOVisualization_graphicsView_ylimits), 
							(self.lsCaliperMap_graphicsView_yselection, self.lsSOVisualization_graphicsView_yselection),
							ypressfunction1=self.highlight_MDlocation,
							ypressfunction3=self.choose_MDlocation )

		self.lsCaliperMap_graphicsView.axes.clear()
		self.lsSOVisualization_graphicsView.axes.clear()

		#-------------------------------------------------

		self.lsCaliperMap_graphicsView.axes.fill_betweenx( self.MD, -self.ID, +self.ID, alpha=0.5, color='C0')
		factors = mu.np.linspace(1.2,1.6,8)

		for stage in self.parent.v3WellboreInnerStageData.values():
			
			MDstage,IDstage = mdl.get_LASMDandCALID_intoStage(self, stage)
			IPODstage = stage['PipeProps'].OD[0]

			for factor in factors[1:]:
				IPOD = IPODstage*factor
				self.lsCaliperMap_graphicsView.axes.fill_betweenx( MDstage, +IPOD, +IDstage, where=IPOD<IDstage, alpha=0.15, color='C3')
				self.lsCaliperMap_graphicsView.axes.fill_betweenx( MDstage, -IPOD, -IDstage, where=IPOD<IDstage, alpha=0.15, color='C3')

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
		#self.lsSOVisualization_graphicsView.draw()

		#-------------------------------------------------
		
		EW = parent.v2ASCComplements_fields.EW
		NS = parent.v2ASCComplements_fields.NS
		VD = parent.v2ASCComplements_fields.TVD

		curve, = self.lsWellbore3D_graphicsView.axes.plot( EW, NS, VD )

		self.lsWellbore3D_graphicsView.axes.set_xlabel( EW.headerName )
		self.lsWellbore3D_graphicsView.axes.set_ylabel( NS.headerName )
		self.lsWellbore3D_graphicsView.axes.set_zlabel( VD.headerName )

		max_EW = max(EW)
		min_EW = min(EW)
		max_NS = max(NS)
		min_NS = min(NS)
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
		#self.lsWellbore3D_graphicsView.draw()
		
		#-------------------------------------------------

		
		self.draw_MDlocations( initial=True )

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

		for field in self.lsCentralization_fields[:4]:
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

		cu.savetable( 	self.lsCentralizerLocations_tableWidget,
						self.lsCentralization_fields[:4],
						["tmp/CentralizerLocationsAndSO_'{stagerow}'.csv"
						.format(stagerow=self.stage['row']),
						self.parent.workingDirectory+"/CentralizerLocationsAndSO_'{stagerow}'.csv"
						.format(stagerow=self.stage['row'])] )

		self.lsCaliperMap_graphicsView.figure.savefig( "tmp/CaliperMap_'{stagerow}'.png"
			.format(stagerow=self.stage['row']), dpi=300 )

		self.lsSOVisualization_graphicsView.figure.savefig( "tmp/SOVisualization_'{stagerow}'.png"
			.format(stagerow=self.stage['row']), dpi=300 )

		self.lsWellbore3D_graphicsView.figure.savefig( "tmp/Wellbore3D_'{stagerow}'.png"
			.format(stagerow=self.stage['row']), dpi=300 )

		self.lsCaliperMap_graphicsView.figure.savefig( self.parent.workingDirectory+"/CaliperMap_'{stagerow}'.png"
			.format(stagerow=self.stage['row']), dpi=300 )

		self.lsSOVisualization_graphicsView.figure.savefig( self.parent.workingDirectory+"/SOVisualization_'{stagerow}'.png"
			.format(stagerow=self.stage['row']), dpi=300 )

		self.lsWellbore3D_graphicsView.figure.savefig( self.parent.workingDirectory+"/Wellbore3D_'{stagerow}'.png"
			.format(stagerow=self.stage['row']), dpi=300 )

		self.fields = self.lsCentralization_fields
		self.parent.centralizationChanged_flag = False

		self.dialog.done(0)


	def select_row(self, r, c, alltherow=False ):

		cu.select_tableWidgetRow(self.lsCentralizerLocations_tableWidget, r, alltherow)
		
		if r<self.centralizerCount:
			MD = self.lsCentralization_fields.MD[r]
			EW = self.lsCentralization_fields.EW[r]
			NS = self.lsCentralization_fields.NS[r]
			VD = self.lsCentralization_fields.TVD[r]

			self.draw_MDlocations(MD, EW, NS, VD, created=False)


	def update_calculations(self, indexes=None):
		
		locations = self.lsCentralization_fields.MD
		SOatC_field = self.lsCentralization_fields.SOatC
		#ClatC_field = self.lsCentralization_fields.ClatC
		SOatM_field = self.lsCentralization_fields.SOatM
		#ClatM_field = self.lsCentralization_fields.ClatM
		#LatC_field = self.lsCentralization_fields.LatC
		Inc_field = self.lsCentralization_fields.Inc

		#mdl2.calculate_standOff_atCentralizers(self, locations, SOatC_field, ClatC_field, LatC_field)
		#mdl2.calculate_standOff_atMidspan(self, locations, ClatC_field, SOatM_field, ClatM_field, Inc_field)

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

			except IndexError:
				item = self.lsCentralizerLocations_tableWidget.item( i, self.lsCentralization_fields.MD.pos )
				item.set_text()
				item = self.lsCentralizerLocations_tableWidget.item( i, self.lsCentralization_fields.Inc.pos )
				item.set_text()
				item = self.lsCentralizerLocations_tableWidget.item( i, self.lsCentralization_fields.SOatC.pos )
				item.set_text()
				item = self.lsCentralizerLocations_tableWidget.item( i, self.lsCentralization_fields.SOatM.pos )
				item.set_text()

		self.meanSOatC = mu.np.round( mu.np.mean(SOatC_field), 1 )
		self.meanSOatM = mu.np.round( mu.np.mean(SOatM_field), 1 )
		self.lsMeanSOatC_label.setText( 'Mean SO at centralizers:\t{mSOatC} {unit}'.format( mSOatC=self.meanSOatC, 
																							unit=SOatC_field.unit ) )
		self.lsMeanSOatM_label.setText( 'Mean SO at minspan:\t{mSOatM} {unit}'.format(  mSOatM=self.meanSOatM,
																						unit=SOatM_field.unit ) )
		cu.idleFunction()

	"""
	@cu.waiting_effects
	def choose_MDlocation(self, MD, overwrite=False):

		if MD>=self.min_MD and MD<=self.max_MD:

			if overwrite:
				r = self.lsCentralizerLocations_tableWidget.selectedRow
				if r<len(self.lsCentralization_fields.MD):
					del self.lsCentralization_fields.MD[r]

			mu.create_physicalValue_and_appendTo_field( MD, self.lsCentralization_fields.MD )
			MD = self.lsCentralization_fields.MD[-1]
			self.lsCentralization_fields.MD.sort()
			self.lsCentralization_fields.EW.clear()
			self.lsCentralization_fields.NS.clear()
			self.lsCentralization_fields.TVD.clear()
			self.lsCentralization_fields.DL.clear()
			self.lsCentralization_fields.Inc.clear()
			self.lsCentralization_fields.SOatC.clear()
			self.lsCentralization_fields.SOatM.clear()
			self.lsCentralization_fields.ClatC.clear()
			self.lsCentralization_fields.ClatM.clear()
			self.lsCentralization_fields.LatC.clear()
			self.centralizerCount = len(self.lsCentralization_fields.MD)

			for i, MDi in enumerate(self.lsCentralization_fields.MD):
					
				EWi,NSi,VDi,_ = mdl2.get_ASCCoordinates_from_MD(self.parent, MDi)
				DLi = mdl2.get_ASCDogleg_from_MD(self.parent, MDi)
				
				#mu.create_physicalValue_and_appendTo_field( EWi, self.lsCentralization_fields.EW )
				#mu.create_physicalValue_and_appendTo_field( NSi, self.lsCentralization_fields.NS )
				#mu.create_physicalValue_and_appendTo_field( VDi, self.lsCentralization_fields.TVD )
				#mu.create_physicalValue_and_appendTo_field( DLi, self.lsCentralization_fields.DL )

				item = self.lsCentralizerLocations_tableWidget.item( i, self.lsCentralization_fields.MD.pos )
				item.set_text( MDi )
				if MD==MDi:
					EW = EWi
					NS = NSi
					VD = VDi
					DL = DLi
					cu.select_tableWidgetRow(self.lsCentralizerLocations_tableWidget, i, alltherow=True)

			try:
				self.update_calculations()
			except mu.LogicalError:
				msg = "There is a logical error between centralizer locations and length.\nThe last entered location will be removed."
				QtGui.QMessageBox.critical(self.ssCentralizerLocations_tableWidget, 'Error', msg)
				self.lsCentralization_fields.MD.remove(MD)
				self.lsCentralization_fields.EW.remove(EW)
				self.lsCentralization_fields.NS.remove(NS)
				self.lsCentralization_fields.TVD.remove(VD)
				self.lsCentralization_fields.DL.remove(LD)
				self.centralizerCount = len(self.lsCentralization_fields.MD)
				self.update_calculations()
				return
			self.draw_MDlocations(MD, EW, NS, VD)
	"""

	def choose_MDlocation(self, MD, overwrite=False):

		if MD<self.min_MD or MD>self.max_MD:
			return

		if overwrite:
			r = self.lsCentralizerLocations_tableWidget.selectedRow
			#if r<len(self.lsCentralization_fields.MD):
				#self.lsCentralization_fields.MD.pop(r)
				#self.lsCentralization_fields.Inc.pop(r)
				#self.lsCentralization_fields.SOatC.pop(r)
				#self.lsCentralization_fields.SOatM.pop(r)
				#self.lsCentralization_fields.ClatC.pop(r)
				#self.lsCentralization_fields.ClatM.pop(r)
				#self.lsCentralization_fields.LatC.pop(r)
				#self.lsCentralization_fields.EW.pop(r)
				#self.lsCentralization_fields.NS.pop(r)
				#self.lsCentralization_fields.TVD.pop(r)
				#self.lsCentralization_fields.DL.pop(r)
				#self.lsCentralization_fields.ID.pop(r)
				#self.lsCentralization_fields.avgID.pop(r)
				#self.lsCentralization_fields.Azi.pop(r)
				#self.lsCentralization_fields.Stage.pop(r)

			mdl.put_location_to_CentralizationFields(self, r, MD)
			
		else:
			r = mu.np.where(mu.np.array(self.lsCentralization_fields.MD)>MD)[0][0]
			mdl.insert_location_to_CentralizationFields(self, r, MD)
			self.lsCentralization_fields.SOatC.pop(r)

		try:
			indexes = mdl.get_indexes_for_shoosing(self, r)
			self.update_calculations(indexes=indexes)
			cu.select_tableWidgetRow(self.lsCentralizerLocations_tableWidget, r, alltherow=True)
		except mu.LogicalError:
			msg = "There is a logical error between centralizer locations and length.\nThe last entered location will be removed."
			QtGui.QMessageBox.critical(self.ssCentralizerLocations_tableWidget, 'Error', msg)
			self.lsCentralization_fields.MD.pop(r)
			self.lsCentralization_fields.Inc.pop(r)
			self.lsCentralization_fields.SOatC.pop(r)
			self.lsCentralization_fields.SOatM.pop(r)
			self.lsCentralization_fields.ClatC.pop(r)
			self.lsCentralization_fields.ClatM.pop(r)
			self.lsCentralization_fields.LatC.pop(r)
			self.lsCentralization_fields.EW.pop(r)
			self.lsCentralization_fields.NS.pop(r)
			self.lsCentralization_fields.TVD.pop(r)
			self.lsCentralization_fields.DL.pop(r)
			self.lsCentralization_fields.ID.pop(r)
			self.lsCentralization_fields.avgID.pop(r)
			self.lsCentralization_fields.Azi.pop(r)
			self.lsCentralization_fields.Stage.pop(r)
			self.centralizerCount = len(self.lsCentralization_fields.MD)
			self.update_calculations()
			return

		MD = self.lsCentralization_fields.MD[r]
		EW = self.lsCentralization_fields.EW[r]
		NS = self.lsCentralization_fields.NS[r]
		VD = self.lsCentralization_fields.TVD[r]
		self.draw_MDlocations(MD, EW, NS, VD)	


	def remove_location(self):

		#for field in self.lsCentralization_fields:
		#	print('br:',field.abbreviation,len(field))

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
			self.lsCentralization_fields.LatC.pop(r)
			self.lsCentralization_fields.EW.pop(r)
			self.lsCentralization_fields.NS.pop(r)
			self.lsCentralization_fields.TVD.pop(r)
			self.lsCentralization_fields.DL.pop(r)
			self.lsCentralization_fields.ID.pop(r)
			self.lsCentralization_fields.avgID.pop(r)
			self.lsCentralization_fields.Azi.pop(r)
			self.lsCentralization_fields.Stage.pop(r)

			self.centralizerCount-=1

			#self.lsCentralization_fields.SOatC.clear()
			#self.lsCentralization_fields.SOatM.clear()
			#self.lsCentralization_fields.ClatC.clear()
			#self.lsCentralization_fields.ClatM.clear()
			#self.lsCentralization_fields.LatC.clear()

			s = r-1 if (r>0) else 0

			if self.centralizerCount>0:
				MD = self.lsCentralization_fields.MD[s]
				EW = self.lsCentralization_fields.EW[s]
				NS = self.lsCentralization_fields.NS[s]
				VD = self.lsCentralization_fields.TVD[s]

				cu.select_tableWidgetRow(self.lsCentralizerLocations_tableWidget,s)
				indexes = mdl.get_indexes_for_removing(self, r)
				self.update_calculations(indexes=indexes)
				self.draw_MDlocations(MD, EW, NS, VD)

			else:
				self.draw_MDlocations()

		#for field in self.lsCentralization_fields:
		#	print('ar:',field.abbreviation,len(field))


	def highlight_MDlocation(self, MD):

		index = mu.np.argmin( abs(mu.array(self.lsCentralization_fields.MD)-MD) )
		self.select_row( index, 0, alltherow=True )


	def draw_MDlocations(self, MD=None, EW=None, NS=None, VD=None, created=True, initial=False ):

		fieldlen = len(self.lsCentralization_fields.MD)
		print( ':MD', fieldlen )
		for field in self.lsCentralization_fields[1:]:
			print( field.abbreviation, len(field) )
			#assert( fieldlen==len(field) )

		xlim = self.lsCaliperMap_graphicsView.axes.get_xlim()	

		if MD!=None:

			del self.lsCaliperMap_graphicsView.axes.lines[2*self.numofStages:]
			del self.lsWellbore3D_graphicsView.axes.lines[1:]
			del self.lsSOVisualization_graphicsView.axes.lines[3:]

			for MDi in self.lsCentralization_fields.MD:
				self.lsCaliperMap_graphicsView.axes.plot( xlim, [MDi, MDi], color='C3', lw=1 )

			self.lsCaliperMap_graphicsView.axes.plot( xlim, [MD, MD], color='C3', lw=4, alpha=0.4 )
			
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
			#SOatC = self.lsCentralization_fields.SOatC[self.lsCentralization_fields.MD.index(MD) ]
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

			for MDi in self.lsCentralization_fields.MD:
				self.lsCaliperMap_graphicsView.axes.plot( xlim, [MDi, MDi], color='C3', lw=1 )

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


		else:
			self.lsCaliperMap_graphicsView.draw()
			self.lsWellbore3D_graphicsView.draw()
			self.lsSOVisualization_graphicsView.draw()

