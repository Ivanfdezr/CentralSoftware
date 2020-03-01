from PyQt4 import QtGui
import InputWindow_Mdl as mdl
from SurveyImport_Ctrl import Main_SurveyImport
import CtrlUtilities as cu
import MdlUtilities as mu
import PlotUtilities as pu


def set_survey_to_table(self):
		
	#MD, Inc, Azi = mdl.get_survey([0,1,2])
	dialog = QtGui.QDialog(self.s2DataSurvey_tableWidget)
	SI = Main_SurveyImport(dialog)

	self.s2DataSurvey_fields.clear_content()
	self.s2DataSurvey_tableWidget.setRowCount(len(SI.fields.MD))
	
	for i in range(self.s2DataSurvey_tableWidget.rowCount()):
		try:
			for sifield in SI.fields:
				dsfield = getattr(self.s2DataSurvey_fields,sifield.abbreviation)
				self.s2DataSurvey_tableWidget.item(i, dsfield.pos).set_text( sifield[i], sifield[i].unit )
		except AttributeError:
			for field in self.s2DataSurvey_fields:
				item = cu.TableWidgetFieldItem( field, i%2==0 )
				self.s2DataSurvey_tableWidget.setItem(i, field.pos, item)
			for sifield in SI.fields:
				dsfield = getattr(self.s2DataSurvey_fields,sifield.abbreviation)
				self.s2DataSurvey_tableWidget.item(i, dsfield.pos).set_text( sifield[i], sifield[i].unit )

	self.FileLines = SI.FileLines
	self.filename = SI.filename
	del SI


def remove_all(self):

	self.s2DataSurvey_fields.clear_content()
	for i in range(self.s2DataSurvey_tableWidget.rowCount()):
		for field in self.s2DataSurvey_fields:
			self.s2DataSurvey_tableWidget.item(i, field.pos).set_text()


def get_tortuosity_data(self):

	self.s2SurveyTortuosity_fields.clear_content()
	Interval = self.s2TortuosityInterval_tableWidget.item(0,0).realValue
	if mu.isNoneEntry( Interval ):
		raise(cu.MandatoryError)
	if Interval<=0.0:
		raise(cu.MandatoryError)

	i=0
	j=0
	while True:
	
		if i == self.s2SurveyTortuosity_tableWidget.rowCount():
			break

		From      = self.s2SurveyTortuosity_tableWidget.item(i, self.s2SurveyTortuosity_fields.FromMD.pos    ).realValue
		To        = self.s2SurveyTortuosity_tableWidget.item(i, self.s2SurveyTortuosity_fields.ToMD.pos      ).realValue
		Amplitude = self.s2SurveyTortuosity_tableWidget.item(i, self.s2SurveyTortuosity_fields.Amplitude.pos ).realValue
		Period    = self.s2SurveyTortuosity_tableWidget.item(i, self.s2SurveyTortuosity_fields.Period.pos    ).realValue
		
		i+=1
		if all( [mu.isNoneEntry(From), mu.isNoneEntry(To), mu.isNoneEntry(Amplitude), mu.isNoneEntry(Period)] ):
			continue
		elif any( [mu.isNoneEntry(From), mu.isNoneEntry(To), mu.isNoneEntry(Amplitude), mu.isNoneEntry(Period)] ):
			msg = "Incomplete tortuosity parameters. This tortuosity stage will be ignored."
			QtGui.QMessageBox.information(self.s2SurveyTortuosity_tableWidget, 'Warning', msg)
			continue
		
		self.s2SurveyTortuosity_fields.FromMD.append(  From  )
		self.s2SurveyTortuosity_fields.ToMD.append( To )
		self.s2SurveyTortuosity_fields.Amplitude.append( Amplitude )
		self.s2SurveyTortuosity_fields.Period.append( Period )
		self.s2SurveyTortuosity_fields.Interval.append( Interval )
		j+=1

	data = []
	for i in range(j):
		data.append( self.s2SurveyTortuosity_fields.extract_data_from_row(i) )

	return data

@cu.waiting_effects
def set_survey_outcomes(self):
	
	self.s2DataSurvey_fields.clear_content()
	KOP = self.s2KOP_tableWidget.item(0,0).realValue
	if mu.isNoneEntry( KOP ):
		raise(cu.MandatoryError)
	if KOP<=0.0:
		raise(cu.MandatoryError)

	i=0
	while True:
	
		if i == self.s2DataSurvey_tableWidget.rowCount():
			break

		md  = self.s2DataSurvey_tableWidget.item(i, self.s2DataSurvey_fields.MD.pos ).realValue
		inc = self.s2DataSurvey_tableWidget.item(i, self.s2DataSurvey_fields.Inc.pos).realValue
		azi = self.s2DataSurvey_tableWidget.item(i, self.s2DataSurvey_fields.Azi.pos).realValue
		
		i+=1
		if mu.isNoneEntry(md) or mu.isNoneEntry(inc) or mu.isNoneEntry(azi):
			continue
		
		self.s2DataSurvey_fields.MD.append(  md  )
		self.s2DataSurvey_fields.Inc.append( inc )
		self.s2DataSurvey_fields.Azi.append( azi )	

	if self.s2SurveyTortuosity_checkBox.isChecked():
		
		try:
			self.tortuosity_data = get_tortuosity_data(self)
			self.ASCComplements, self.dT, self.T, self.sT = mdl.calculate_ASCComplements( self.s2DataSurvey_fields, KOP, self.tortuosity_data )
		except cu.MandatoryError:
			msg = "MD Interval value is non-assigned or incorrect. Can not proceed."
			QtGui.QMessageBox.critical(self.s2TortuosityInterval_tableWidget, 'Error', msg)
			return

	else:
		self.ASCComplements, self.dT, self.T, self.sT = mdl.calculate_ASCComplements( self.s2DataSurvey_fields, KOP )
	
	for i in range(self.s2DataSurvey_tableWidget.rowCount()):
		try:
			for field in self.s2DataSurvey_fields:
				self.s2DataSurvey_tableWidget.item(i, field.pos).set_text( field[i] )
		except IndexError:
			for field in self.s2DataSurvey_fields:
				self.s2DataSurvey_tableWidget.item(i, field.pos).set_text()

	if self.ASCComplements != None:
		self.s2DataSurvey_fields.clear_content()
		self.s2DataSurvey_fields.MD[:]  = self.ASCComplements.MD
		self.s2DataSurvey_fields.Inc[:] = self.ASCComplements.Inc
		self.s2DataSurvey_fields.Azi[:] = self.ASCComplements.Azi
		self.s2DataSurvey_fields.TVD[:] = self.ASCComplements.TVD
		self.s2DataSurvey_fields.HD[:]  = self.ASCComplements.HD
		self.s2DataSurvey_fields.NS[:]  = self.ASCComplements.NS
		self.s2DataSurvey_fields.EW[:]  = self.ASCComplements.EW
		self.s2DataSurvey_fields.DL[:]  = self.ASCComplements.DL

	draw_survey_plots( self )

	msg = "Calculation proceeded successfully."
	QtGui.QMessageBox.information(self.s2SurveyTortuosity_tableWidget, 'Information', msg)


def draw_survey_plots( self ):

	self.s2SectionView_graphicsView.axes.clear()
	self.s2PlanView_graphicsView.axes.clear()
	self.s2TriDView_graphicsView.axes.clear()
	self.s2Dogleg_graphicsView.axes.clear()

	color='C1' if self.ASCComplements else 'C0'
	self.s2SectionView_graphicsView.axes.plot( self.s2DataSurvey_fields.HD, self.s2DataSurvey_fields.TVD, color=color )
	self.s2SectionView_graphicsView.axes.set_xlabel( self.s2DataSurvey_fields.HD.headerName )
	self.s2SectionView_graphicsView.axes.set_ylabel( self.s2DataSurvey_fields.TVD.headerName )
	self.s2SectionView_graphicsView.axes.set_ylim( max(self.s2DataSurvey_fields.TVD), min(self.s2DataSurvey_fields.TVD) )
	self.s2SectionView_graphicsView.axes.grid()
	self.s2SectionView_graphicsView.draw()
	
	self.s2PlanView_graphicsView.axes.plot( self.s2DataSurvey_fields.EW, self.s2DataSurvey_fields.NS, color=color )
	self.s2PlanView_graphicsView.axes.set_xlabel( self.s2DataSurvey_fields.EW.headerName )
	self.s2PlanView_graphicsView.axes.set_ylabel( self.s2DataSurvey_fields.NS.headerName )
	self.s2PlanView_graphicsView.axes.grid()
	self.s2PlanView_graphicsView.draw()
	
	#X,Y,Z,triangles = mu.render_wellbore( self.ASCComplements, 0.1, 20 )
	#ls = pu.LightSource(270, 45)
	#rgb = ls.shade(-Z, cmap=pu.cm.gist_earth, vert_exag=0.1, blend_mode='soft')
	#self.s2TriDView_graphicsView.axes.plot_surface(X,Y,Z, linewidth=0, facecolors=rgb, antialiased=False, shade=True)
	
	##self.s2TriDView_graphicsView.axes.plot_trisurf(X,Y,Z, triangles=triangles, cmap=pu.cm.copper)
	##self.s2TriDView_graphicsView.axes.plot(X,Y,Z,'.',markersize=2)

	curve, = self.s2TriDView_graphicsView.axes.plot( self.s2DataSurvey_fields.EW, self.s2DataSurvey_fields.NS, self.s2DataSurvey_fields.TVD, color=color )
	#dot,   = self.s2TriDView_graphicsView.axes.plot( [0],[0],[0],'bo' )
	self.s2TriDView_graphicsView.axes.set_xlabel( self.s2DataSurvey_fields.EW.headerName )
	self.s2TriDView_graphicsView.axes.set_ylabel( self.s2DataSurvey_fields.NS.headerName )
	self.s2TriDView_graphicsView.axes.set_zlabel( self.s2DataSurvey_fields.TVD.headerName )

	max_EW = max(self.s2DataSurvey_fields.EW)
	min_EW = min(self.s2DataSurvey_fields.EW)

	max_NS = max(self.s2DataSurvey_fields.NS)
	min_NS = min(self.s2DataSurvey_fields.NS)

	ΔEW = max_EW - min_EW
	ΔNS = max_NS - min_NS

	if ΔEW>ΔNS:
		self.s2TriDView_graphicsView.axes.set_xlim( min_EW, max_EW )
		Δ = (ΔEW-ΔNS)/2
		self.s2TriDView_graphicsView.axes.set_ylim( min_NS-Δ, max_NS+Δ )
	elif ΔNS>ΔEW:
		self.s2TriDView_graphicsView.axes.set_ylim( min_NS, max_NS )
		Δ = (ΔNS-ΔEW)/2
		self.s2TriDView_graphicsView.axes.set_xlim( min_EW-Δ, max_EW+Δ )
	else:
		self.s2TriDView_graphicsView.axes.set_xlim( min_EW, max_EW )
		self.s2TriDView_graphicsView.axes.set_ylim( min_NS, max_NS )


	self.s2TriDView_graphicsView.axes.set_zlim( max(self.s2DataSurvey_fields.TVD), min(self.s2DataSurvey_fields.TVD) )
	self.s2TriDView_graphicsView.axes.mouse_init()
	zp = pu.ZoomPan()
	#zp.point3D_factory(self.s2TriDView_graphicsView.axes, dot, curve)
	zp.zoom3D_factory( self.s2TriDView_graphicsView.axes, curve )
	self.s2TriDView_graphicsView.draw()
	
	self.s2Dogleg_graphicsView.axes.plot( self.s2DataSurvey_fields.DL, self.s2DataSurvey_fields.MD, color=color )
	self.s2Dogleg_graphicsView.axes.set_xlabel( self.s2DataSurvey_fields.DL.headerName )
	self.s2Dogleg_graphicsView.axes.set_ylabel( self.s2DataSurvey_fields.MD.headerName )
	self.s2Dogleg_graphicsView.axes.set_ylim( max(self.s2DataSurvey_fields.MD), min(self.s2DataSurvey_fields.MD) )
	self.s2Dogleg_graphicsView.axes.grid()
	self.s2Dogleg_graphicsView.draw()

