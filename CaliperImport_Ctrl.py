from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from CaliperImport_Vst import Ui_CaliperImport
import CaliperImport_Mdl as mdl
import CtrlUtilities as cu
import PlotUtilities as pu
import MdlUtilities as mu
import copy
import re, os

 
class Main_CaliperImport(Ui_CaliperImport):

	def __init__(self, dialog, parent):
		
		Ui_CaliperImport.__init__(self)
		self.setupUi(dialog)
		self.dialog = dialog
		self.parent = parent		
		
		self.ciLASData_fields = mdl.get_ciLASData_fields()
		self.ciOpenFile_pushButton.clicked.connect(self.open_file)
		self.ciValueDecimalPoint_radioButton.clicked.connect(self.setup_valueDecimalPoint)
		self.ciValueDecimalComma_radioButton.clicked.connect(self.setup_valueDecimalComma)

		self.unitRepresentations = mdl.get_lengthUnits()

		self.ciMDvalueUnit_comboBox.addItems( self.unitRepresentations )
		i = self.unitRepresentations.index( self.ciLASData_fields.MD.unit )
		self.ciMDvalueUnit_comboBox.setCurrentIndex(i)

		self.ciIDvalueUnit_comboBox.addItems( self.unitRepresentations )
		i = self.unitRepresentations.index( self.ciLASData_fields.CD.unit )
		self.ciIDvalueUnit_comboBox.setCurrentIndex(i)

		self.ciApplyAndDraw_pushButton.clicked.connect( self.applyAndDraw_caliperData )
		self.ciCommaDelimiter_checkBox.stateChanged.connect( self.setNumberPattern )
		self.ciHoleIDsmoothing_slider.valueChanged.connect( self.update_ciHoleIDsmoothing_label )
		self.ciHoleIDsmoothing_slider.sliderReleased.connect( self.draw_caliperData )
		#self.ciHoleIDsmoothing_slider.actionTriggered.connect( self.update_sliderValue )
		self.ciAccept_pushButton.clicked.connect( self.makeResults_and_done )

		self.ciHoleIDsmoothing_graphicsView.axes.set_position([0.23,0.1,0.7,0.85])
		self.ciHoleIDsmoothing_graphicsView_ylimits    = [None,None]
		self.ciHoleIDsmoothing_graphicsView_yselection = []
		zp = pu.ZoomPan()
		zp.zoomYD_factory(self.ciHoleIDsmoothing_graphicsView.axes, self.ciHoleIDsmoothing_graphicsView_ylimits )
		zp.panYD_factory( self.ciHoleIDsmoothing_graphicsView.axes, self.ciHoleIDsmoothing_graphicsView_ylimits ) 
						  #ypressfunction3=self.snapshot )

		self.setup_valueDecimalPoint()

		dialog.setAttribute(Qt.WA_DeleteOnClose)
		dialog.exec_()


	def snapshot(self,x):

		self.ciHoleIDsmoothing_graphicsView.figure.savefig( self.parent.v1WorkingDirectory+"DR-CAL.png", dpi=300 )
		self.ciHoleIDsmoothing_graphicsView.axes.set_visible(False)
		self.ciHoleIDsmoothing_graphicsView.draw()
		cu.idleFunction()
		self.ciHoleIDsmoothing_graphicsView.axes.set_visible(True)
		self.ciHoleIDsmoothing_graphicsView.draw()
		cu.idleFunction()




	def update_sliderValue(self, intAction):
		
		self.ciHoleIDsmoothing_slider.setValue( self.ciHoleIDsmoothing_slider.sliderPosition() )


	def update_ciHoleIDsmoothing_label(self, value=None):

		if not value:
			value = self.ciHoleIDsmoothing_slider.value()
		self.ciHoleIDsmoothing_label.setText( str(value)+'%' )

		return value


	def setNumberPattern(self, state=None):

		if self.ciValueDecimalPoint_radioButton.isChecked():
			if state == Qt.Checked:
				self.numberPattern = mu.get_decimalPointPattern()
			else:
				self.numberPattern = mu.get_decimalPointWithThousandsCommaPattern()

		elif self.ciValueDecimalComma_radioButton.isChecked():
			self.numberPattern = mu.get_decimalCommaPattern()


	def setup_valueDecimalPoint(self):
		self.ciCommaDelimiter_checkBox.setEnabled(True)
		self.text2float = mu.get_decimalFloatPointFunction()
		self.setNumberPattern()


	def setup_valueDecimalComma(self):
		self.ciCommaDelimiter_checkBox.setEnabled(False)
		self.ciCommaDelimiter_checkBox.setCheckState(Qt.Unchecked)
		self.text2float = mu.get_decimalFloatCommaFunction()
		self.setNumberPattern()


	def open_file(self):
		
		filepath = QFileDialog.getOpenFileName(self.dialog, 'Open file', 'c:\\',"DR-CAL files (*.las *.txt)")[0]
		head,filename = os.path.split( filepath )
		self.ciFilename_label.setText( filename )
		with open(filepath, 'r', encoding='windows-1252') as file:
			self.lines = file.readlines()

		self.numofRows = len(self.lines)
		for row, line in enumerate(self.lines):
			text = str(row+1)+'\t'+line
			self.ciFileText_textEdit.insertPlainText(text)
			self.ciStatus_label.setText( 'Loading ... {val}%'.format(val=int(row/self.numofRows*100)) )
			if row%int(self.numofRows/20)==0:
				cu.idleFunction()
		
		self.ciStatus_label.setText('')
		self.setEnabled_parsingDRCalToolkit()


	def setEnabled_parsingDRCalToolkit(self, boolean=True):

		self.ciValueFeatures_groupBox.setEnabled(boolean)
		self.ciDelimiters_groupBox.setEnabled(boolean)
		self.ciColumnIndexes_groupBox.setEnabled(boolean)
		self.ciFilter_groupBox.setEnabled(boolean)
		self.ciApplyAndDraw_pushButton.setEnabled(boolean)


	def setEnabled_smoothingDRCalToolkit(self, boolean=True):
		self.ciHoleIDsmoothing_slider.setEnabled(boolean)
		self.ciHoleIDsmoothing_graphicsView.setEnabled(boolean)
		self.ciHoleIDsmoothing_label.setEnabled(boolean)
		self.ciAccept_pushButton.setEnabled(boolean)


	def applyAndDraw_caliperData(self):

		self.setEnabled_parsingDRCalToolkit(False)
		self.setEnabled_smoothingDRCalToolkit(False)
		cu.idleFunction()

		fileTextStartingRow   = (self.ciStartingRow_spinBox.value()-1)%self.numofRows #self.ciFileText_tableWidget.rowCount()
		fileTextEndingRow     = (self.ciEndingRow_spinBox.value() - 1)%self.numofRows #self.ciFileText_tableWidget.rowCount()
		fileTextMDcolumnIndex = (self.ciMDcolumnIndex_spinBox.value()-1)#%99
		fileTextH1columnIndex = (self.ciH1columnIndex_spinBox.value()-1)#%99
		fileTextH2columnIndex = (self.ciH2columnIndex_spinBox.value()-1)#%99

		self.ciCALData_fields = mdl.get_ciCALData_fields(fileTextH2columnIndex-fileTextH1columnIndex+1)
		MDUnitRepresentation = self.ciMDvalueUnit_comboBox.currentText()
		IDUnitRepresentation = self.ciIDvalueUnit_comboBox.currentText()
		self.ciLASData_fields.MD.set_unit(  MDUnitRepresentation )
		for field in self.ciCALData_fields:
			field.set_unit(  IDUnitRepresentation )
		#self.ciLASData_fields.CD.set_unit(  IDUnitRepresentation )
		self.ciLASData_fields.selectedMD.set_unit( MDUnitRepresentation )
		self.ciLASData_fields.clear_content()
		self.ciCALData_fields.clear_content()

		self.feasibleDrawFlagMDID = True
		self.feasibleDrawFlagOD  = True

		try:
			minimumIDvalue = float(self.ciMinimumID_entry.text())
		except ValueError:
			self.ciMinimumID_entry.setText('')
			minimumIDvalue = 0.0 #float('-inf')

		try:
			maximumIDvalue = float(self.ciMaximumID_entry.text())
		except ValueError:
			self.ciMaximumID_entry.setText('')
			maximumIDvalue = float('inf')

		try:
			minimumMDvalue = float(self.ciMinimumMD_entry.text())
		except ValueError:
			self.ciMinimumMD_entry.setText('')
			minimumMDvalue = 0.0 #float('-inf')

		try:
			maximumMDvalue = float(self.ciMaximumMD_entry.text())
		except ValueError:
			self.ciMaximumMD_entry.setText('')
			maximumMDvalue = float('inf')
		
		delimiterPattern = ''
		if self.ciTabDelimiter_checkBox.checkState() == Qt.Checked:
			delimiterPattern += '\t'
		if self.ciSemicolonDelimiter_checkBox.checkState() == Qt.Checked:
			delimiterPattern += ';'
		if self.ciSpacesDelimiter_checkBox.checkState() == Qt.Checked:
			delimiterPattern += ' '
		if self.ciCommaDelimiter_checkBox.checkState() == Qt.Checked:
			delimiterPattern += ','
		columnPattern = '((?<=['+delimiterPattern+'])'+self.numberPattern+')|('+self.numberPattern+'(?=['+delimiterPattern+']))'

		for row, beforeStylingText in enumerate(self.lines):
			
			try:
				assert( row>=fileTextStartingRow and row<=fileTextEndingRow )
				matches = list(re.finditer( columnPattern, beforeStylingText ))
				
				for index, match in enumerate(matches):
					
					if index==fileTextMDcolumnIndex:
						value = self.text2float( match.group() )
						assert( value>=minimumMDvalue and value<=maximumMDvalue )
					
					elif index==fileTextH1columnIndex:
						value = self.text2float( match.group() )
						assert( value>=minimumIDvalue and value<=maximumIDvalue )

					elif fileTextH1columnIndex<fileTextH2columnIndex:
						if index>fileTextH1columnIndex and index<=fileTextH2columnIndex:
							value = self.text2float( match.group() )
							assert( value>=minimumIDvalue and value<=maximumIDvalue )

				try:
					MDvalue = self.text2float( matches[fileTextMDcolumnIndex].group() )
					mu.create_physicalValue_and_appendTo_field( MDvalue, self.ciLASData_fields.MD )
					if fileTextH1columnIndex<=fileTextH2columnIndex:
						for index in range(fileTextH1columnIndex,fileTextH2columnIndex+1):
							IDvalue = self.text2float( matches[index].group() )
							fieldIndex = index-fileTextH1columnIndex
							mu.create_physicalValue_and_appendTo_field( IDvalue, self.ciCALData_fields[fieldIndex] )
					elif fileTextH1columnIndex>fileTextH2columnIndex and fileTextH2columnIndex==-1:
						IDvalue = self.text2float( matches[fileTextH1columnIndex].group() )
						mu.create_physicalValue_and_appendTo_field( IDvalue, self.ciCALData_fields[0] )
				except IndexError:
					self.feasibleDrawFlagMDID = False


			except AssertionError:
				continue

			self.ciStatus_label.setText( 'Drawing ... {val}%'.format(val=int(row/self.numofRows*100)) )
			if row%500==0:
				cu.idleFunction()

		self.ciStatus_label.setText('')

		if self.check_conditionsForDraw(): #True
			self.wasPushedApplyAndDrawButton = True
			self.draw_caliperData()

		self.setEnabled_parsingDRCalToolkit(True)
		self.setEnabled_smoothingDRCalToolkit(True)
		self.wasPushedApplyAndDrawButton = False

	
	def check_conditionsForDraw(self):
		try:
			assert( self.feasibleDrawFlagMDID )
			assert( len(self.ciLASData_fields.MD)>0 )
			return True
		except AssertionError:
			self.feasibleDrawFlagMDID = False
			self.feasibleDrawFlagOD  = False
			return False
	

	def choose_MDlocation(self, MDposition):
		xlim = self.ciHoleIDsmoothing_graphicsView.axes.get_xlim()
		self.ciHoleIDsmoothing_graphicsView.axes.plot( xlim, [MDposition,MDposition], 'C3' )
		self.ciLocationsCount_label.setText( 'Number of locations: '+str(len(self.ciHoleIDsmoothing_graphicsView_yselection)) )


	def draw_caliperData(self, value=None):

		#if not value:
		#	value = self.ciHoleIDsmoothing_slider.value()
		#self.ciHoleIDsmoothing_label.setText( str(value)+'%' )

		value = self.update_ciHoleIDsmoothing_label(value)

		if self.wasPushedApplyAndDrawButton:
			self.DLM = mdl.DerivativeLevelsMatrix( self.ciLASData_fields.MD, self.ciCALData_fields )
		self.DLM.get_leveredID(value)

		self.ciHoleIDsmoothing_graphicsView_yselection.clear()
		self.ciHoleIDsmoothing_graphicsView.axes.clear()
		#self.ciHoleIDsmoothing_graphicsView.axes.plot( self.DLM.IDmaxOrig, self.ciLASData_fields.MD, 'C0' )
		#self.ciHoleIDsmoothing_graphicsView.axes.plot( self.DLM.IDminOrig, self.ciLASData_fields.MD, 'C0', alpha=0.5 )
		
		#self.DLM.IDmaxOrig = list(self.DLM.IDmaxOrig)
		MD_array = mu.array(self.ciLASData_fields.MD)
		
		self.ciHoleIDsmoothing_graphicsView.axes.fill_betweenx( MD_array, -self.DLM.IDmaxOrig, +self.DLM.IDmaxOrig, alpha=0.3)
		self.ciHoleIDsmoothing_graphicsView.axes.fill_betweenx( MD_array, -self.DLM.IDminOrig, -self.DLM.IDmaxOrig, alpha=0.6, color='C0')
		self.ciHoleIDsmoothing_graphicsView.axes.fill_betweenx( MD_array, +self.DLM.IDminOrig, +self.DLM.IDmaxOrig, alpha=0.6, color='C0')
		self.ciHoleIDsmoothing_graphicsView.axes.plot( -self.DLM.IDmax, self.ciLASData_fields.MD, 'C1', lw=1.5 )
		self.ciHoleIDsmoothing_graphicsView.axes.plot( +self.DLM.IDmax, self.ciLASData_fields.MD, 'C1', lw=1.5 )

		#if self.feasibleDrawFlagOD:
		#	self.ciHoleIDsmoothing_graphicsView.axes.plot( -self.OD, self.ciLASData_fields.MD, 'C4' )
		#	self.ciHoleIDsmoothing_graphicsView.axes.plot( +self.OD, self.ciLASData_fields.MD, 'C4' )

		self.ciHoleIDsmoothing_graphicsView.axes.set_xlabel( self.ciCALData_fields.CAL1.headerName )
		self.ciHoleIDsmoothing_graphicsView.axes.set_ylabel( self.ciLASData_fields.MD.headerName )

		lim_ID = max(self.DLM.IDmaxOrig)*1.2	
		self.ciHoleIDsmoothing_graphicsView.axes.set_xlim( -lim_ID, lim_ID )
		if self.wasPushedApplyAndDrawButton:
			self.ciHoleIDsmoothing_graphicsView.axes.set_ylim( max(self.ciLASData_fields.MD), min(self.ciLASData_fields.MD) )
			self.ciHoleIDsmoothing_graphicsView_ylimits[:] = self.ciHoleIDsmoothing_graphicsView.axes.get_ylim()
		else:
			self.ciHoleIDsmoothing_graphicsView.axes.set_ylim( self.ciHoleIDsmoothing_graphicsView_ylimits )

		self.ciHoleIDsmoothing_graphicsView.axes.grid()
		self.ciHoleIDsmoothing_graphicsView.draw()
		self.ciLocationsCount_label.setText( 'Number of locations: 0' )

		# l, b, w, h 
		##


	def makeResults_and_done(self):

		self.ciLASData_fields.selectedMD.clear()
		for MDvalue in self.ciHoleIDsmoothing_graphicsView_yselection:
			mu.create_physicalValue_and_appendTo_field( MDvalue, self.ciLASData_fields.selectedMD )

		for arm,ID in enumerate(self.DLM.ID):
			ID = mdl.reduce_ID( ID )
			field = self.ciCALData_fields[arm]
			field.clear()
			for IDvalue in ID:
				mu.create_physicalValue_and_appendTo_field( IDvalue, field )
		
		id_mean = mu.make_cleanAverage( self.DLM.IDmax )
		self.CALID_max, self.MD = mdl.reduce_IDandMD( self.DLM.IDmax, self.ciLASData_fields.MD )

		self.ciLASData_fields.MD.clear()
		for MDvalue in self.MD:
			mu.create_physicalValue_and_appendTo_field( MDvalue, self.ciLASData_fields.MD )

		self.ciCaliperReport_fields = mdl.get_ciCaliperReport_fields()
		max_MD = max(self.ciLASData_fields.MD)
		min_MD = min(self.ciLASData_fields.MD)

		mu.create_physicalValue_and_appendTo_field( 'DR-CAL', self.ciCaliperReport_fields.Desc    )
		mu.create_physicalValue_and_appendTo_field( id_mean,  self.ciCaliperReport_fields.ID      )
		mu.create_physicalValue_and_appendTo_field( min_MD,   self.ciCaliperReport_fields.MDtop   )
		mu.create_physicalValue_and_appendTo_field( max_MD,   self.ciCaliperReport_fields.MDbot   )

		##
		self.ciHoleIDsmoothing_graphicsView.figure.savefig( self.parent.v1WorkingDirectory+"DR-CAL.png", dpi=300 )
		
		self.data = self.ciCaliperReport_fields.extract_data_from_row( 0 )
		self.fields = self.ciCaliperReport_fields
		self.dialog.done(0)
	