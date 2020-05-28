from PyQt4 import QtCore, QtGui
from SurveyImport_Vst import Ui_SurveyImport
import SurveyImport_Mdl as mdl
import CtrlUtilities as cu
import PlotUtilities as pu
import MdlUtilities as mu
import copy
import re, os
import time


class Main_SurveyImport(Ui_SurveyImport):

	def __init__(self, dialog):
		
		Ui_SurveyImport.__init__(self)
		self.setupUi(dialog)
		self.dialog = dialog		
		
		self.siSurveyData_fields = mdl.get_siSurveyData_fields()
		self.__init__siSurveyReport_tableWidget()
		self.siOpenFile_pushButton.clicked.connect(self.open_file)
		self.siValueDecimalPoint_radioButton.clicked.connect(self.setup_valueDecimalPoint)
		self.siValueDecimalComma_radioButton.clicked.connect(self.setup_valueDecimalComma)
		
		unitRepresentations = mdl.get_lengthUnits()
		self.siMDvalueUnit_comboBox.addItems( unitRepresentations )
		i = unitRepresentations.index( self.siSurveyData_fields.MD.unit )
		self.siMDvalueUnit_comboBox.setCurrentIndex(i)

		unitRepresentations = mdl.get_inclinationUnits()
		self.siAnglesvalueUnit_comboBox.addItems( unitRepresentations )
		i = unitRepresentations.index( self.siSurveyData_fields.Inc.unit )
		self.siAnglesvalueUnit_comboBox.setCurrentIndex(i)
		
		self.siExtract_pushButton.clicked.connect( self.export_surveyData )
		self.siCommaDelimiter_checkBox.stateChanged.connect( self.set_numberPattern )
		self.siAccept_pushButton.clicked.connect( self.makeResults_and_done )

		self.setup_valueDecimalPoint()
		
		dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		dialog.exec_()


	def __init__siSurveyReport_tableWidget(self):
		
		self.siSurveyReport_tableWidget.parent = self
		self.siSurveyReport_tableWidget.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
		
		C = cu.CopySelectedCells_action(self.siSurveyReport_tableWidget)
		self.siSurveyReport_tableWidget.addAction(C)
		
		#V = cu.PasteToCells_action(self.siSurveyReport_tableWidget)
		#self.siSurveyReport_tableWidget.addAction(V)

		#clear_row = lambda: cu.clear_tableWidgetRow(self.siSurveyReport_tableWidget)
		#D = cu.FunctionToWidget_action(self.siSurveyReport_tableWidget, clear_row, "Delete", 'Del')
		#self.siSurveyReport_tableWidget.addAction(D)
		
		for field in self.siSurveyData_fields:
			item = self.siSurveyReport_tableWidget.horizontalHeaderItem( field.pos )
			item.setText( field.headerName )
			
			for i in range(self.siSurveyReport_tableWidget.rowCount()):
				item = cu.TableWidgetFieldItem( field, i%2==0 )
				self.siSurveyReport_tableWidget.setItem(i, field.pos, item)

		select_row = lambda r,c : cu.select_tableWidgetRow(self.siSurveyReport_tableWidget,r)
		self.siSurveyReport_tableWidget.cellPressed.connect(select_row)

		#self.siSurveyReport_tableWidget.resizeColumnsToContents()


	def makeResults_and_done(self):

		self.data = self.siSurveyData_fields.extract_data_from_row( 0 )
		self.fields = self.siSurveyData_fields
		self.dialog.done(0)


	def set_numberPattern(self, state=None):

		if self.siValueDecimalPoint_radioButton.isChecked():
			if state == QtCore.Qt.Checked:
				self.numberPattern = mu.get_decimalPointPattern()
			else:
				self.numberPattern = mu.get_decimalPointWithThousandsCommaPattern()

		elif self.siValueDecimalComma_radioButton.isChecked():
			self.numberPattern = mu.get_decimalCommaPattern()


	def setup_valueDecimalPoint(self):
		self.siCommaDelimiter_checkBox.setEnabled(True)
		self.text2float = mu.get_decimalFloatPointFunction()
		self.set_numberPattern()


	def setup_valueDecimalComma(self):
		self.siCommaDelimiter_checkBox.setEnabled(False)
		self.siCommaDelimiter_checkBox.setCheckState(QtCore.Qt.Unchecked)
		self.text2float = mu.get_decimalFloatCommaFunction()
		self.set_numberPattern()


	def open_file(self):
		
		filepath = QtGui.QFileDialog.getOpenFileName(self.dialog, 'Open file', 'c:\\',"SURVEY files (*.las *.txt)")
		head,filename = os.path.split( filepath )
		self.siFilename_label.setText( filename )

		tic = time.time()

		with open(filepath,'r') as file:
			self.lines = file.readlines()
		
		toc = time.time(); print('ET: ',toc-tic); tic = time.time()

		self.numofRows = len(self.lines)
		for row, line in enumerate(self.lines):
			text = str(row+1)+'\t'+line
			self.siFileText_textEdit.insertPlainText(text)
			if row%int(self.numofRows/20)==0:
				self.siStatus_label.setText( 'Loading ... {val}%'.format(val=int(row/self.numofRows*100)) )
				cu.idleFunction()

		toc = time.time(); print('ET: ',toc-tic); tic = time.time()

		self.siStatus_label.setText('')
		self.setEnabled_parsingSurveyToolkit()
		


	def setEnabled_parsingSurveyToolkit(self, boolean=True):

		self.siValueFeatures_groupBox.setEnabled(boolean)
		self.siDelimiters_groupBox.setEnabled(boolean)
		self.siColumnIndexes_groupBox.setEnabled(boolean)
		self.siFilter_groupBox.setEnabled(boolean)
		self.siExtract_pushButton.setEnabled(boolean)
		self.siSurveyReport_tableWidget.setEnabled(boolean)
		self.siAccept_pushButton.setEnabled(boolean)


	def export_surveyData(self):

		self.setEnabled_parsingSurveyToolkit(False)
		cu.idleFunction()

		fileTextStartingRow   = (self.siStartingRow_spinBox.value()-1)%self.numofRows#self.siFileText_tableWidget.rowCount()
		fileTextEndingRow     =   (self.siEndingRow_spinBox.value()-1)%self.numofRows#self.siFileText_tableWidget.rowCount()
		fileTextMDcolumnIndex = (self.siMDcolumnIndex_spinBox.value()-1)%99
		fileTextInccolumnIndex = (self.siInccolumnIndex_spinBox.value()-1)%99
		fileTextAzicolumnIndex = (self.siAzicolumnIndex_spinBox.value()-1)%99
		MDUnitRepresentation = self.siMDvalueUnit_comboBox.currentText()
		IncUnitRepresentation = self.siAnglesvalueUnit_comboBox.currentText()

		#self.siSurveyData_fields.MD.set_unit(  MDUnitRepresentation  )
		#self.siSurveyData_fields.Inc.set_unit( IncUnitRepresentation )
		#self.siSurveyData_fields.Azi.set_unit( IncUnitRepresentation )

		self.siSurveyData_fields.clear_content()

		self.feasibleFlagMDIncAzi = True

		try:
			minimumMDvalue = float(self.siMinimumMD_entry.text())
		except ValueError:
			self.siMinimumMD_entry.setText('')
			minimumMDvalue = 0.0 #float('-inf')

		try:
			maximumMDvalue = float(self.siMaximumMD_entry.text())
		except ValueError:
			self.siMaximumMD_entry.setText('')
			maximumMDvalue = float('inf')

		try:
			minimumIncvalue = float(self.siMinimumInc_entry.text())
		except ValueError:
			self.siMinimumInc_entry.setText('')
			minimumIncvalue = 0.0 #float('-inf')

		try:
			maximumIncvalue = float(self.siMaximumInc_entry.text())
		except ValueError:
			self.siMaximumInc_entry.setText('')
			maximumIncvalue = float('inf')

		try:
			minimumAzivalue = float(self.siMinimumAzi_entry.text())
		except ValueError:
			self.siMinimumAzi_entry.setText('')
			minimumAzivalue = 0.0 #float('-inf')

		try:
			maximumAzivalue = float(self.siMaximumAzi_entry.text())
		except ValueError:
			self.siMaximumAzi_entry.setText('')
			maximumAzivalue = float('inf')
		
		delimiterPattern = ''
		if self.siTabDelimiter_checkBox.checkState() == QtCore.Qt.Checked:
			delimiterPattern += '\t'
		if self.siSemicolonDelimiter_checkBox.checkState() == QtCore.Qt.Checked:
			delimiterPattern += ';'
		if self.siSpacesDelimiter_checkBox.checkState() == QtCore.Qt.Checked:
			delimiterPattern += ' '
		if self.siCommaDelimiter_checkBox.checkState() == QtCore.Qt.Checked:
			delimiterPattern += ','
		columnPattern = '((?<=['+delimiterPattern+'])'+self.numberPattern+')|('+self.numberPattern+'(?=['+delimiterPattern+']))'

		#hrt = mdl.HtmlRichText()

		for row, beforeStylingText in enumerate(self.lines):

			#widget = self.siFileText_tableWidget.cellWidget(row, 0)
			
			try:
				assert( row>=fileTextStartingRow and row<=fileTextEndingRow )
				#widget.setEnabled(True)
				matches = list(re.finditer( columnPattern, beforeStylingText ))
				
				#afterStylingText = ''
				#i = 0
				for index, match in enumerate(matches):
					#j = match.start()
					#afterStylingText += hrt.get_styledText( '.'*(j-i), pu.Colors['CW'] ) #'<font color='+pu.Colors['CW']+'>'+ '.'*(j-i) +'</font>'
					# = match.end()
					
					if index==fileTextMDcolumnIndex:
						value = self.text2float( match.group() )
						assert( value>=minimumMDvalue and value<=maximumMDvalue )
						#afterStylingText += hrt.get_styledText( match.group(), pu.Colors['C3'], True) #'<b><font color='+pu.Colors['C3']+'>'+ match.group() +'</font></b>'
					
					elif index==fileTextInccolumnIndex:
						value = self.text2float( match.group() )
						assert( value>=minimumIncvalue and value<=maximumIncvalue )
						#afterStylingText += hrt.get_styledText( match.group(), pu.Colors['C0'], True) #'<b><font color='+pu.Colors['C0']+'>'+ match.group() +'</font></b>'

					elif index==fileTextAzicolumnIndex:
						value = self.text2float( match.group() )
						assert( value>=minimumAzivalue and value<=maximumAzivalue )
						#afterStylingText += hrt.get_styledText( match.group(), pu.Colors['C2'], True) #'<b><font color='+pu.Colors['C2']+'>'+ match.group() +'</font></b>'

					#else:
						#afterStylingText += match.group()

				try:
					MDvalue = self.text2float( matches[fileTextMDcolumnIndex].group() )
					Incvalue = self.text2float( matches[fileTextInccolumnIndex].group() )
					Azivalue = self.text2float( matches[fileTextAzicolumnIndex].group() )
					mu.create_physicalValue_and_appendTo_field( MDvalue, self.siSurveyData_fields.MD, unit=MDUnitRepresentation )
					mu.create_physicalValue_and_appendTo_field( Incvalue, self.siSurveyData_fields.Inc, unit=IncUnitRepresentation )
					mu.create_physicalValue_and_appendTo_field( Azivalue, self.siSurveyData_fields.Azi, unit=IncUnitRepresentation )
				except IndexError:
					self.feasibleFlagMDIncAzi = False

				#widget.setText(afterStylingText)
				#hrt.add_line(str(row+1)+'\t'+afterStylingText)

			except AssertionError:
				continue
				#widget.setText(beforeStylingText[:-1])
				#widget.setEnabled(False)
				#hrt.add_line(str(row+1)+'\t'+beforeStylingText[:-1])

		#html = hrt.get_html()
		#self.textEdit.setHtml(html)

		if self.check_conditionsForDraw():
			self.set_fieldsData_to_siSurveyReport_tableWidget()

		self.setEnabled_parsingSurveyToolkit(True)

	
	def check_conditionsForDraw(self):
		try:
			assert( self.feasibleFlagMDIncAzi )
			assert( len(self.siSurveyData_fields.MD)>0 )
			return True
		except AssertionError:
			self.feasibleFlagMDIncAzi = False
			return False


	def set_fieldsData_to_siSurveyReport_tableWidget(self):

		self.siSurveyReport_tableWidget.setRowCount(len(self.siSurveyData_fields.MD))

		for i in range(self.siSurveyReport_tableWidget.rowCount()):
			try:
				for field in self.siSurveyData_fields:
					self.siSurveyReport_tableWidget.item(i, field.pos).set_text( field[i], field[i].unit )
			except AttributeError:
				for field in self.siSurveyData_fields:
					item = cu.TableWidgetFieldItem( field, i%2==0 )
					item.set_text( field[i] )
					self.siSurveyReport_tableWidget.setItem(i, field.pos, item)
	


	