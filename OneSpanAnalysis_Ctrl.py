from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from OneSpanAnalysis_Vst import Ui_OneSpanAnalysis
from TubularDatabase_Ctrl import Main_TubularDatabase
from CentralizerDatabase_Ctrl import Main_CentralizerDatabase
import OneSpanAnalysis_Mdl as mdl
import CtrlUtilities as cu
import MdlUtilities as mu


class Main_OneSpanAnalysis(Ui_OneSpanAnalysis):

	def __init__(self, dialog ):
		
		Ui_OneSpanAnalysis.__init__(self)
		self.setupUi(dialog)
		self.dialog = dialog		
		
		self.__init__osaCasing_tableWidget()
		self.__init__osaCentA_tableWidget()
		self.__init__osaCentB_tableWidget()
		self.__init__osaWellbore_tableWidget()
		self.__init__osaOutputdata1_tableWidget()
		self.__init__osaOutputdata2_tableWidget()

		self.spacingUnit = self.osaWellbore_fields.MaxSpan.unit

		
		# self.usUSOF_radioButton.clicked.connect(setup_usParameterUSUnits_tableWidget)
		# self.usMetric_radioButton.clicked.connect(setup_usParameterSIUnits_tableWidget)
		# self.usCustomized_radioButton.clicked.connect(setup_usParameterCuUnits_tableWidget)

		self.osaCasing_pushButton.clicked.connect(self.open_TDB_dialog)
		self.osaCentA_pushButton.clicked.connect(self.open_CDB_dialog_forA)
		self.osaCentB_pushButton.clicked.connect(self.open_CDB_dialog_forB)

		self.osaInclination_slider.valueChanged.connect( self.update_analysisWithInclination )
		self.osaInclination_slider.actionTriggered.connect( self.update_inclinationSliderValue )

		self.osaSpacing_slider.setValue( 50 )
		self.osaSpacing_slider.valueChanged.connect( self.update_analysisWithSpacing )
		self.osaSpacing_slider.actionTriggered.connect( self.update_spacingSliderValue )

		self.osaSpacingSentivity_graphicsView.axes.set_position([0.1,0.1,0.8,0.8])
		self.osaSpacingSentivity_graphicsView.axes.set_xticks([])
		self.osaSpacingSentivity_graphicsView.axes.set_yticks([])
		
		dialog.setAttribute(Qt.WA_DeleteOnClose)
		dialog.exec_()

		#self.dialog.done(0)


	def __init__osaCasing_tableWidget(self):
		
		self.osaCasing_tableWidget.parent = self
		self.osaCasing_tableWidget.setContextMenuPolicy(Qt.ActionsContextMenu)

		self.osaCasing_fields = mdl.get_osaCasing_fields()
		for field in self.osaCasing_fields:
			item = self.osaCasing_tableWidget.verticalHeaderItem( field.pos )
			item.setText( cu.extend_text( field.headerName, 38 ) )
			item = cu.TableWidgetFieldItem( field, False )
			self.osaCasing_tableWidget.setItem(field.pos, 0, item)

		self.osaCasing_tableWidget.itemChanged.connect(self.update_analysisWithFieldItem)


	def __init__osaCentA_tableWidget(self):
		
		self.osaCentA_tableWidget.parent = self
		self.osaCentA_tableWidget.setContextMenuPolicy(Qt.ActionsContextMenu)

		self.osaCentA_fields = mdl.get_osaCent_fields()
		for field in self.osaCentA_fields:
			item = self.osaCentA_tableWidget.verticalHeaderItem( field.pos )
			item.setText( cu.extend_text( field.headerName, 34 ) )
			item = cu.TableWidgetFieldItem( field, False )
			self.osaCentA_tableWidget.setItem(field.pos, 0, item)

		self.osaCentA_tableWidget.itemChanged.connect(self.update_analysisWithFieldItem)


	def __init__osaCentB_tableWidget(self):
		
		self.osaCentB_tableWidget.parent = self
		self.osaCentB_tableWidget.setContextMenuPolicy(Qt.ActionsContextMenu)

		self.osaCentB_fields = mdl.get_osaCent_fields()
		for field in self.osaCentB_fields:
			item = self.osaCentB_tableWidget.verticalHeaderItem( field.pos )
			item.setText( cu.extend_text( field.headerName, 34 ) )
			item = cu.TableWidgetFieldItem( field, False )
			self.osaCentB_tableWidget.setItem(field.pos, 0, item)

		self.osaCentB_tableWidget.itemChanged.connect(self.update_analysisWithFieldItem)


	def __init__osaWellbore_tableWidget(self):
		
		self.osaWellbore_tableWidget.parent = self
		self.osaWellbore_tableWidget.setContextMenuPolicy(Qt.ActionsContextMenu)

		self.osaWellbore_fields = mdl.get_osaWellbore_fields()
		for field in self.osaWellbore_fields:
			item = self.osaWellbore_tableWidget.verticalHeaderItem( field.pos )
			item.setText( cu.extend_text( field.headerName, 31 ) )
			item = cu.TableWidgetFieldItem( field, False )
			self.osaWellbore_tableWidget.setItem(field.pos, 0, item)

		self.osaWellbore_tableWidget.itemChanged.connect(self.update_analysisWithFieldItem)


	def __init__osaOutputdata1_tableWidget(self):
		
		self.osaOutputdata1_tableWidget.parent = self
		self.osaOutputdata1_tableWidget.setContextMenuPolicy(Qt.ActionsContextMenu)

		self.osaOutputdata1_fields = mdl.get_osaOutputdata1_fields()
		for field in self.osaOutputdata1_fields:
			item = self.osaOutputdata1_tableWidget.verticalHeaderItem( field.pos )
			item.setText( cu.extend_text( field.headerName, 43 ) )
			item = cu.TableWidgetFieldItem( field, False )
			self.osaOutputdata1_tableWidget.setItem(field.pos, 0, item)


	def __init__osaOutputdata2_tableWidget(self):
		
		self.osaOutputdata2_tableWidget.parent = self
		self.osaOutputdata2_tableWidget.setContextMenuPolicy(Qt.ActionsContextMenu)

		self.osaOutputdata2_fields = mdl.get_osaOutputdata2_fields()
		for field in self.osaOutputdata2_fields:
			item = self.osaOutputdata2_tableWidget.verticalHeaderItem( field.pos )
			item.setText( cu.extend_text( field.headerName, 38 ) )
			item = cu.TableWidgetFieldItem( field, False )
			self.osaOutputdata2_tableWidget.setItem(field.pos, 0, item)
		

	def open_TDB_dialog(self):

		dialog = QDialog(self.osaCasing_tableWidget)
		self.TDB = Main_TubularDatabase(dialog)

		for field in self.osaCasing_fields:

			item = self.osaCasing_tableWidget.item(field.pos,0)

			if field.abbreviation in self.TDB.data:
				value = self.TDB.data[field.abbreviation]
				item.set_text( value, value.unit )
			else:
				item.set_text()
				item.alt_backgroundColor()
				item.alt_flags()
				#self.osaCasing_tableWidget.editItem(item)


	def open_CDB_dialog_forA(self):

		dialog = QDialog(self.osaCentA_tableWidget)
		self.CDB_A = Main_CentralizerDatabase(dialog)

		for field in self.osaCentA_fields:

			item = self.osaCentA_tableWidget.item(field.pos,0)

			if field.abbreviation in self.CDB_A.data:
				value = self.CDB_A.data[field.abbreviation]
				item.set_text( value, value.unit )
			else:
				item.set_text()
				item.alt_backgroundColor()
				item.alt_flags()
				#self.osaCentA_tableWidget.editItem(item)


	def open_CDB_dialog_forB(self):

		dialog = QDialog(self.osaCentB_tableWidget)
		self.CDB_B = Main_CentralizerDatabase(dialog)

		for field in self.osaCentB_fields:

			item = self.osaCentB_tableWidget.item(field.pos,0)

			if field.abbreviation in self.CDB_B.data:
				value = self.CDB_B.data[field.abbreviation]
				item.set_text( value, value.unit )
			else:
				item.set_text()
				item.alt_backgroundColor()
				item.alt_flags()
				#self.osaCentA_tableWidget.editItem(item)


	def update_inclinationSliderValue(self, intAction):
		self.osaInclination_slider.setValue( self.osaInclination_slider.sliderPosition() )

	
	def update_spacingSliderValue(self, intAction):
		self.osaSpacing_slider.setValue( self.osaSpacing_slider.sliderPosition() )

	
	def update_analysisWithInclination(self, value=None):

		if not value:
			value = self.osaInclination_slider.value()
		self.osaInclination_label.setText( 'Inclination'+cu.extend_text(str(value)+'°', 20, mode='rigth') )
		self.draw_casingDeflectionCurve()


	def update_analysisWithSpacing(self, value=None):

		if not value:
			value = self.osaSpacing_slider.value()
		
		try:
			value = self.osaWellbore_fields.MaxSpan[0]*value/100
		except KeyError:
			pass

		self.osaSpacing_label.setText( 'Spacing'+cu.extend_text(str(value)+' '+self.spacingUnit, 20, mode='rigth') )
		self.draw_casingDeflectionCurve()


	def update_analysisWithFieldItem(self, item):

		cu.update_fieldItem(item)
		self.update_fields()
		self.draw_casingDeflectionCurve()


	def update_fields(self):

		self.osaCasing_fields.clear_content()
		for field in self.osaCasing_fields:
			value = self.osaCasing_tableWidget.item(field.pos,0).realValue
			field.append(value)

		self.osaCentA_fields.clear_content()
		for field in self.osaCentA_fields:
			value = self.osaCentA_tableWidget.item(field.pos,0).realValue
			field.append(value)

		self.osaCentB_fields.clear_content()
		for field in self.osaCentB_fields:
			value = self.osaCentB_tableWidget.item(field.pos,0).realValue
			field.append(value)

		self.osaWellbore_fields.clear_content()
		for field in self.osaWellbore_fields:
			value = self.osaWellbore_tableWidget.item(field.pos,0).realValue
			field.append(value)


	def draw_casingDeflectionCurve(self):

		try:
			OHc, OHp, OHm, XYc, XYp, XYm, lim, rA, rB, rM = mdl.get_casingDeflectionCurve(self)

			for field in self.osaOutputdata1_fields:
				item = self.osaOutputdata1_tableWidget.item(field.pos,0)
				value = field[0]
				item.set_text( value, value.unit )

			for field in self.osaOutputdata2_fields:
				item = self.osaOutputdata2_tableWidget.item(field.pos,0)
				value = field[0]
				item.set_text( value, value.unit )

			self.osaSpacingSentivity_graphicsView.axes.clear()
			self.osaClearanceAnalysisA_graphicsView.axes.clear()
			self.osaClearanceAnalysisB_graphicsView.axes.clear()
			self.osaClearanceAnalysisM_graphicsView.axes.clear()

			self.osaSpacingSentivity_graphicsView.axes.plot(OHc[0],OHc[1],'C0--')
			self.osaSpacingSentivity_graphicsView.axes.plot(OHp[0],OHp[1],'C0')
			self.osaSpacingSentivity_graphicsView.axes.plot(OHm[0],OHm[1],'C0')

			self.osaSpacingSentivity_graphicsView.axes.plot(XYc[0],XYc[1],'C1--')
			self.osaSpacingSentivity_graphicsView.axes.plot(XYp[0],XYp[1],'C1')
			self.osaSpacingSentivity_graphicsView.axes.plot(XYm[0],XYm[1],'C1')

			self.osaSpacingSentivity_graphicsView.axes.set_xlim(-lim, lim)
			self.osaSpacingSentivity_graphicsView.axes.set_ylim(-lim, lim)

			self.osaSpacingSentivity_graphicsView.axes.set_xticks([])
			self.osaSpacingSentivity_graphicsView.axes.set_yticks([])
			self.osaSpacingSentivity_graphicsView.draw()

			rH = self.osaWellbore_fields.HoleID[0]/2
			R  = self.osaCasing_fields.OD[0]/2
			RA = self.osaCentA_fields.COD[0]/2
			RB = self.osaCentB_fields.COD[0]/2

			thick = R/20
			hole  = mu.render_circle( (0,0), rH )
			pipeA = mu.render_circle( (0,rA-rH), R )
			pipeB = mu.render_circle( (0,rB-rH), R )
			pipeM = mu.render_circle( (0,rM-rH), R )
			centAi = mu.render_circle( (0,rA-rH), R+thick)
			centAe = mu.render_circle( (0,rA-rH), RA-thick)
			centA  = mu.render_circle( (0,rA-rH), RA-thick)
			centBi = mu.render_circle( (0,rB-rH), R+thick)
			centBe = mu.render_circle( (0,rB-rH), RB-thick)
			centB  = mu.render_circle( (0,rB-rH), RB-thick)
			

			self.osaClearanceAnalysisM_graphicsView.axes.plot(hole[0],hole[1],'C0')
			self.osaClearanceAnalysisM_graphicsView.axes.plot([-rH,rH],[0,0],'C0--')
			self.osaClearanceAnalysisM_graphicsView.axes.plot([0,0],[-rH,rH],'C0--')
			self.osaClearanceAnalysisM_graphicsView.axes.plot(pipeM[0],pipeM[1],'C1')
			self.osaClearanceAnalysisM_graphicsView.axes.plot([-R,R],[rM-rH,rM-rH],'C1--')
			self.osaClearanceAnalysisM_graphicsView.axes.plot([0,0],[rM-rH-R,rM-rH+R],'C1--')


			radios = mu.np.sqrt(mu.np.sum(centA**2,axis=0))
			indexes = radios>rH
			costh = centA.T[indexes].T[0]/radios[indexes]
			sinth = centA.T[indexes].T[1]/radios[indexes]
			centA_ = centA.T[indexes].T
			aux = mu.np.array([(rH-thick)*costh,(rH-thick)*sinth])
			centA.T[indexes] = aux.T

			self.osaClearanceAnalysisA_graphicsView.axes.plot(hole[0],hole[1],'C0')
			self.osaClearanceAnalysisA_graphicsView.axes.plot([-rH,rH],[0,0],'C0--')
			self.osaClearanceAnalysisA_graphicsView.axes.plot([0,0],[-rH,rH],'C0--')
			self.osaClearanceAnalysisA_graphicsView.axes.plot(pipeA[0],pipeA[1],'C1')
			self.osaClearanceAnalysisA_graphicsView.axes.plot([-R,R],[rA-rH,rA-rH],'C1--')
			self.osaClearanceAnalysisA_graphicsView.axes.plot([0,0],[rA-rH-R,rA-rH+R],'C1--')
			self.osaClearanceAnalysisA_graphicsView.axes.plot(centAe[0],centAe[1],'C3--')
			self.osaClearanceAnalysisA_graphicsView.axes.plot(centAi[0],centAi[1],'C3')

			for i in [0,20,40,60,80,100]:
				j = 6
				k = 2
				x = [centAi[0][i-j],centA[0][i+k],centA[0][i-k],centAi[0][i+j]]
				y = [centAi[1][i-j],centA[1][i+k],centA[1][i-k],centAi[1][i+j]]
				self.osaClearanceAnalysisA_graphicsView.axes.plot(x,y,'C3')


			radios = mu.np.sqrt(mu.np.sum(centB**2,axis=0))
			indexes = radios>rH
			costh = centB.T[indexes].T[0]/radios[indexes]
			sinth = centB.T[indexes].T[1]/radios[indexes]
			centB_ = centB.T[indexes].T
			aux = mu.np.array([(rH-thick)*costh,(rH-thick)*sinth])
			centB.T[indexes] = aux.T

			self.osaClearanceAnalysisB_graphicsView.axes.plot(hole[0],hole[1],'C0')
			self.osaClearanceAnalysisB_graphicsView.axes.plot([-rH,rH],[0,0],'C0--')
			self.osaClearanceAnalysisB_graphicsView.axes.plot([0,0],[-rH,rH],'C0--')
			self.osaClearanceAnalysisB_graphicsView.axes.plot(pipeB[0],pipeB[1],'C1')
			self.osaClearanceAnalysisB_graphicsView.axes.plot([-R,R],[rB-rH,rB-rH],'C1--')
			self.osaClearanceAnalysisB_graphicsView.axes.plot([0,0],[rB-rH-R,rB-rH+R],'C1--')
			self.osaClearanceAnalysisB_graphicsView.axes.plot(centBe[0],centBe[1],'C3--')
			self.osaClearanceAnalysisB_graphicsView.axes.plot(centBi[0],centBi[1],'C3')

			for i in [0,20,40,60,80,100]:
				j = 6
				k = 2
				x = [centBi[0][i-j],centB[0][i+k],centB[0][i-k],centBi[0][i+j]]
				y = [centBi[1][i-j],centB[1][i+k],centB[1][i-k],centBi[1][i+j]]
				self.osaClearanceAnalysisB_graphicsView.axes.plot(x,y,'C3')

			lim = rH*1.2
			unit = self.osaWellbore_fields.HoleID.unit
			self.osaClearanceAnalysisA_graphicsView.axes.set_xlim(-lim, lim)
			self.osaClearanceAnalysisA_graphicsView.axes.set_ylim(-lim, lim)
			self.osaClearanceAnalysisB_graphicsView.axes.set_xlim(-lim, lim)
			self.osaClearanceAnalysisB_graphicsView.axes.set_ylim(-lim, lim)
			self.osaClearanceAnalysisM_graphicsView.axes.set_xlim(-lim, lim)
			self.osaClearanceAnalysisM_graphicsView.axes.set_ylim(-lim, lim)

			self.osaClearanceAnalysisA_graphicsView.axes.set_ylabel('['+unit+']')
			self.osaClearanceAnalysisB_graphicsView.axes.set_ylabel('['+unit+']')
			self.osaClearanceAnalysisM_graphicsView.axes.set_ylabel('['+unit+']')
			self.osaClearanceAnalysisA_graphicsView.draw()
			self.osaClearanceAnalysisB_graphicsView.draw()
			self.osaClearanceAnalysisM_graphicsView.draw()


		except (NameError, TypeError):

			self.osaCasing_fields.inverseReferenceUnitConvert_fields()
			self.osaCentA_fields.inverseReferenceUnitConvert_fields()
			self.osaCentB_fields.inverseReferenceUnitConvert_fields()
			self.osaWellbore_fields.inverseReferenceUnitConvert_fields()
			self.osaSpacingSentivity_graphicsView.axes.clear()
			self.osaClearanceAnalysisA_graphicsView.axes.clear()
			self.osaClearanceAnalysisB_graphicsView.axes.clear()
			self.osaClearanceAnalysisM_graphicsView.axes.clear()
			self.osaSpacingSentivity_graphicsView.axes.set_xticks([])
			self.osaSpacingSentivity_graphicsView.axes.set_yticks([])
			self.osaSpacingSentivity_graphicsView.draw()
			self.osaClearanceAnalysisA_graphicsView.draw()
			self.osaClearanceAnalysisB_graphicsView.draw()
			self.osaClearanceAnalysisM_graphicsView.draw()