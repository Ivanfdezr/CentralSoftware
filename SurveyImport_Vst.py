# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SurveyImport_Vst.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
	_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
	def _fromUtf8(s):
		return s

try:
	_encoding = QtGui.QApplication.UnicodeUTF8
	def _translate(context, text, disambig):
		return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
	def _translate(context, text, disambig):
		return QtGui.QApplication.translate(context, text, disambig)

class Ui_SurveyImport(object):
	def setupUi(self, SurveyImport):
		SurveyImport.setObjectName(_fromUtf8("SurveyImport"))
		SurveyImport.resize(1202, 822)
		self.siAccept_pushButton = QtGui.QPushButton(SurveyImport)
		self.siAccept_pushButton.setGeometry(QtCore.QRect(1039, 740, 141, 31))
		font = QtGui.QFont()
		font.setPointSize(10)
		self.siAccept_pushButton.setFont(font)
		self.siAccept_pushButton.setObjectName(_fromUtf8("siAccept_pushButton"))
		self.siOpenFile_pushButton = QtGui.QPushButton(SurveyImport)
		self.siOpenFile_pushButton.setGeometry(QtCore.QRect(30, 30, 130, 31))
		font = QtGui.QFont()
		font.setPointSize(10)
		self.siOpenFile_pushButton.setFont(font)
		self.siOpenFile_pushButton.setObjectName(_fromUtf8("siOpenFile_pushButton"))
		self.siSurveyReport_tableWidget = QtGui.QTableWidget(SurveyImport)
		self.siSurveyReport_tableWidget.setGeometry(QtCore.QRect(850, 70, 331, 651))
		self.siSurveyReport_tableWidget.setStyleSheet(_fromUtf8("background-color: rgb(241, 241, 241);\n"
"alternate-background-color: rgb(255, 255, 255);"))
		self.siSurveyReport_tableWidget.setFrameShape(QtGui.QFrame.WinPanel)
		self.siSurveyReport_tableWidget.setAlternatingRowColors(True)
		self.siSurveyReport_tableWidget.setRowCount(1000)
		self.siSurveyReport_tableWidget.setColumnCount(3)
		self.siSurveyReport_tableWidget.setObjectName(_fromUtf8("siSurveyReport_tableWidget"))
		item = QtGui.QTableWidgetItem()
		self.siSurveyReport_tableWidget.setHorizontalHeaderItem(0, item)
		item = QtGui.QTableWidgetItem()
		self.siSurveyReport_tableWidget.setHorizontalHeaderItem(1, item)
		item = QtGui.QTableWidgetItem()
		self.siSurveyReport_tableWidget.setHorizontalHeaderItem(2, item)
		self.siSurveyReport_tableWidget.horizontalHeader().setVisible(True)
		self.siSurveyReport_tableWidget.horizontalHeader().setDefaultSectionSize(86)
		self.siSurveyReport_tableWidget.verticalHeader().setDefaultSectionSize(25)
		self.siExtract_pushButton = QtGui.QPushButton(SurveyImport)
		self.siExtract_pushButton.setEnabled(False)
		self.siExtract_pushButton.setGeometry(QtCore.QRect(680, 740, 151, 31))
		font = QtGui.QFont()
		font.setPointSize(10)
		self.siExtract_pushButton.setFont(font)
		self.siExtract_pushButton.setObjectName(_fromUtf8("siExtract_pushButton"))
		self.siDelimiters_groupBox = QtGui.QGroupBox(SurveyImport)
		self.siDelimiters_groupBox.setEnabled(False)
		self.siDelimiters_groupBox.setGeometry(QtCore.QRect(530, 330, 301, 101))
		font = QtGui.QFont()
		font.setPointSize(10)
		self.siDelimiters_groupBox.setFont(font)
		self.siDelimiters_groupBox.setObjectName(_fromUtf8("siDelimiters_groupBox"))
		self.siSpacesDelimiter_checkBox = QtGui.QCheckBox(self.siDelimiters_groupBox)
		self.siSpacesDelimiter_checkBox.setGeometry(QtCore.QRect(20, 60, 120, 25))
		self.siSpacesDelimiter_checkBox.setChecked(True)
		self.siSpacesDelimiter_checkBox.setObjectName(_fromUtf8("siSpacesDelimiter_checkBox"))
		self.siSemicolonDelimiter_checkBox = QtGui.QCheckBox(self.siDelimiters_groupBox)
		self.siSemicolonDelimiter_checkBox.setGeometry(QtCore.QRect(160, 30, 120, 25))
		self.siSemicolonDelimiter_checkBox.setObjectName(_fromUtf8("siSemicolonDelimiter_checkBox"))
		self.siTabDelimiter_checkBox = QtGui.QCheckBox(self.siDelimiters_groupBox)
		self.siTabDelimiter_checkBox.setGeometry(QtCore.QRect(20, 30, 120, 25))
		self.siTabDelimiter_checkBox.setObjectName(_fromUtf8("siTabDelimiter_checkBox"))
		self.siCommaDelimiter_checkBox = QtGui.QCheckBox(self.siDelimiters_groupBox)
		self.siCommaDelimiter_checkBox.setGeometry(QtCore.QRect(160, 60, 120, 25))
		self.siCommaDelimiter_checkBox.setObjectName(_fromUtf8("siCommaDelimiter_checkBox"))
		self.siColumnIndexes_groupBox = QtGui.QGroupBox(SurveyImport)
		self.siColumnIndexes_groupBox.setEnabled(False)
		self.siColumnIndexes_groupBox.setGeometry(QtCore.QRect(530, 440, 301, 111))
		font = QtGui.QFont()
		font.setPointSize(10)
		self.siColumnIndexes_groupBox.setFont(font)
		self.siColumnIndexes_groupBox.setToolTip(_fromUtf8(""))
		self.siColumnIndexes_groupBox.setObjectName(_fromUtf8("siColumnIndexes_groupBox"))
		self.label_5 = QtGui.QLabel(self.siColumnIndexes_groupBox)
		self.label_5.setGeometry(QtCore.QRect(20, 35, 31, 21))
		self.label_5.setObjectName(_fromUtf8("label_5"))
		self.label_6 = QtGui.QLabel(self.siColumnIndexes_groupBox)
		self.label_6.setGeometry(QtCore.QRect(110, 35, 71, 21))
		self.label_6.setObjectName(_fromUtf8("label_6"))
		self.siMDcolumnIndex_spinBox = QtGui.QSpinBox(self.siColumnIndexes_groupBox)
		self.siMDcolumnIndex_spinBox.setGeometry(QtCore.QRect(20, 60, 70, 27))
		self.siMDcolumnIndex_spinBox.setLayoutDirection(QtCore.Qt.LeftToRight)
		self.siMDcolumnIndex_spinBox.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
		self.siMDcolumnIndex_spinBox.setMinimum(1)
		self.siMDcolumnIndex_spinBox.setObjectName(_fromUtf8("siMDcolumnIndex_spinBox"))
		self.siInccolumnIndex_spinBox = QtGui.QSpinBox(self.siColumnIndexes_groupBox)
		self.siInccolumnIndex_spinBox.setGeometry(QtCore.QRect(110, 60, 70, 27))
		self.siInccolumnIndex_spinBox.setMinimum(1)
		self.siInccolumnIndex_spinBox.setProperty("value", 2)
		self.siInccolumnIndex_spinBox.setObjectName(_fromUtf8("siInccolumnIndex_spinBox"))
		self.siAzicolumnIndex_spinBox = QtGui.QSpinBox(self.siColumnIndexes_groupBox)
		self.siAzicolumnIndex_spinBox.setGeometry(QtCore.QRect(200, 60, 70, 27))
		self.siAzicolumnIndex_spinBox.setMinimum(1)
		self.siAzicolumnIndex_spinBox.setProperty("value", 3)
		self.siAzicolumnIndex_spinBox.setObjectName(_fromUtf8("siAzicolumnIndex_spinBox"))
		self.label_8 = QtGui.QLabel(self.siColumnIndexes_groupBox)
		self.label_8.setGeometry(QtCore.QRect(200, 35, 71, 21))
		self.label_8.setObjectName(_fromUtf8("label_8"))
		self.siValueFeatures_groupBox = QtGui.QGroupBox(SurveyImport)
		self.siValueFeatures_groupBox.setEnabled(False)
		self.siValueFeatures_groupBox.setGeometry(QtCore.QRect(530, 60, 301, 261))
		font = QtGui.QFont()
		font.setPointSize(10)
		self.siValueFeatures_groupBox.setFont(font)
		self.siValueFeatures_groupBox.setObjectName(_fromUtf8("siValueFeatures_groupBox"))
		self.layoutWidget = QtGui.QWidget(self.siValueFeatures_groupBox)
		self.layoutWidget.setGeometry(QtCore.QRect(10, 30, 281, 71))
		self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
		self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
		self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
		self.siValueDecimalPoint_radioButton = QtGui.QRadioButton(self.layoutWidget)
		self.siValueDecimalPoint_radioButton.setChecked(True)
		self.siValueDecimalPoint_radioButton.setObjectName(_fromUtf8("siValueDecimalPoint_radioButton"))
		self.verticalLayout.addWidget(self.siValueDecimalPoint_radioButton)
		self.siValueDecimalComma_radioButton = QtGui.QRadioButton(self.layoutWidget)
		self.siValueDecimalComma_radioButton.setObjectName(_fromUtf8("siValueDecimalComma_radioButton"))
		self.verticalLayout.addWidget(self.siValueDecimalComma_radioButton)
		self.formLayoutWidget_2 = QtGui.QWidget(self.siValueFeatures_groupBox)
		self.formLayoutWidget_2.setGeometry(QtCore.QRect(10, 110, 281, 151))
		self.formLayoutWidget_2.setObjectName(_fromUtf8("formLayoutWidget_2"))
		self.formLayout_2 = QtGui.QFormLayout(self.formLayoutWidget_2)
		self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
		self.formLayout_2.setHorizontalSpacing(15)
		self.formLayout_2.setVerticalSpacing(10)
		self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
		self.siAnglesvalueUnit_comboBox = QtGui.QComboBox(self.formLayoutWidget_2)
		font = QtGui.QFont()
		font.setPointSize(10)
		self.siAnglesvalueUnit_comboBox.setFont(font)
		self.siAnglesvalueUnit_comboBox.setObjectName(_fromUtf8("siAnglesvalueUnit_comboBox"))
		self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.siAnglesvalueUnit_comboBox)
		self.label_11 = QtGui.QLabel(self.formLayoutWidget_2)
		font = QtGui.QFont()
		font.setPointSize(10)
		self.label_11.setFont(font)
		self.label_11.setObjectName(_fromUtf8("label_11"))
		self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_11)
		self.label_12 = QtGui.QLabel(self.formLayoutWidget_2)
		font = QtGui.QFont()
		font.setPointSize(10)
		self.label_12.setFont(font)
		self.label_12.setObjectName(_fromUtf8("label_12"))
		self.formLayout_2.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_12)
		self.label_13 = QtGui.QLabel(self.formLayoutWidget_2)
		font = QtGui.QFont()
		font.setPointSize(10)
		self.label_13.setFont(font)
		self.label_13.setObjectName(_fromUtf8("label_13"))
		self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_13)
		self.label_7 = QtGui.QLabel(self.formLayoutWidget_2)
		font = QtGui.QFont()
		font.setPointSize(10)
		self.label_7.setFont(font)
		self.label_7.setObjectName(_fromUtf8("label_7"))
		self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_7)
		self.siMDvalueUnit_comboBox = QtGui.QComboBox(self.formLayoutWidget_2)
		font = QtGui.QFont()
		font.setPointSize(10)
		self.siMDvalueUnit_comboBox.setFont(font)
		self.siMDvalueUnit_comboBox.setObjectName(_fromUtf8("siMDvalueUnit_comboBox"))
		self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.siMDvalueUnit_comboBox)
		self.siStartingRow_spinBox = QtGui.QSpinBox(self.formLayoutWidget_2)
		self.siStartingRow_spinBox.setMinimum(1)
		self.siStartingRow_spinBox.setMaximum(50000)
		self.siStartingRow_spinBox.setSingleStep(1)
		self.siStartingRow_spinBox.setProperty("value", 1)
		self.siStartingRow_spinBox.setObjectName(_fromUtf8("siStartingRow_spinBox"))
		self.formLayout_2.setWidget(2, QtGui.QFormLayout.FieldRole, self.siStartingRow_spinBox)
		self.siEndingRow_spinBox = QtGui.QSpinBox(self.formLayoutWidget_2)
		self.siEndingRow_spinBox.setMinimum(0)
		self.siEndingRow_spinBox.setMaximum(50000)
		self.siEndingRow_spinBox.setSingleStep(1)
		self.siEndingRow_spinBox.setProperty("value", 0)
		self.siEndingRow_spinBox.setObjectName(_fromUtf8("siEndingRow_spinBox"))
		self.formLayout_2.setWidget(3, QtGui.QFormLayout.FieldRole, self.siEndingRow_spinBox)
		self.siFilter_groupBox = QtGui.QGroupBox(SurveyImport)
		self.siFilter_groupBox.setEnabled(False)
		self.siFilter_groupBox.setGeometry(QtCore.QRect(530, 560, 301, 161))
		font = QtGui.QFont()
		font.setPointSize(10)
		self.siFilter_groupBox.setFont(font)
		self.siFilter_groupBox.setObjectName(_fromUtf8("siFilter_groupBox"))
		self.siMinimumMD_entry = QtGui.QLineEdit(self.siFilter_groupBox)
		self.siMinimumMD_entry.setGeometry(QtCore.QRect(20, 40, 80, 27))
		self.siMinimumMD_entry.setAccessibleDescription(_fromUtf8(""))
		self.siMinimumMD_entry.setObjectName(_fromUtf8("siMinimumMD_entry"))
		self.siMaximumMD_entry = QtGui.QLineEdit(self.siFilter_groupBox)
		self.siMaximumMD_entry.setGeometry(QtCore.QRect(190, 40, 80, 27))
		self.siMaximumMD_entry.setObjectName(_fromUtf8("siMaximumMD_entry"))
		self.siMinimumInc_entry = QtGui.QLineEdit(self.siFilter_groupBox)
		self.siMinimumInc_entry.setGeometry(QtCore.QRect(20, 80, 80, 27))
		self.siMinimumInc_entry.setWhatsThis(_fromUtf8(""))
		self.siMinimumInc_entry.setObjectName(_fromUtf8("siMinimumInc_entry"))
		self.siMaximumInc_entry = QtGui.QLineEdit(self.siFilter_groupBox)
		self.siMaximumInc_entry.setGeometry(QtCore.QRect(190, 80, 80, 27))
		self.siMaximumInc_entry.setStatusTip(_fromUtf8(""))
		self.siMaximumInc_entry.setObjectName(_fromUtf8("siMaximumInc_entry"))
		self.label_3 = QtGui.QLabel(self.siFilter_groupBox)
		self.label_3.setGeometry(QtCore.QRect(110, 40, 71, 27))
		font = QtGui.QFont()
		font.setFamily(_fromUtf8("Consolas"))
		font.setPointSize(11)
		self.label_3.setFont(font)
		self.label_3.setObjectName(_fromUtf8("label_3"))
		self.label_4 = QtGui.QLabel(self.siFilter_groupBox)
		self.label_4.setGeometry(QtCore.QRect(110, 80, 71, 27))
		font = QtGui.QFont()
		font.setFamily(_fromUtf8("Consolas"))
		font.setPointSize(11)
		self.label_4.setFont(font)
		self.label_4.setObjectName(_fromUtf8("label_4"))
		self.siMinimumAzi_entry = QtGui.QLineEdit(self.siFilter_groupBox)
		self.siMinimumAzi_entry.setGeometry(QtCore.QRect(20, 120, 80, 27))
		self.siMinimumAzi_entry.setWhatsThis(_fromUtf8(""))
		self.siMinimumAzi_entry.setObjectName(_fromUtf8("siMinimumAzi_entry"))
		self.label_9 = QtGui.QLabel(self.siFilter_groupBox)
		self.label_9.setGeometry(QtCore.QRect(110, 120, 71, 27))
		font = QtGui.QFont()
		font.setFamily(_fromUtf8("Consolas"))
		font.setPointSize(11)
		self.label_9.setFont(font)
		self.label_9.setObjectName(_fromUtf8("label_9"))
		self.siMaximumAzi_entry = QtGui.QLineEdit(self.siFilter_groupBox)
		self.siMaximumAzi_entry.setGeometry(QtCore.QRect(190, 120, 80, 27))
		self.siMaximumAzi_entry.setStatusTip(_fromUtf8(""))
		self.siMaximumAzi_entry.setObjectName(_fromUtf8("siMaximumAzi_entry"))
		self.siFilename_label = QtGui.QLabel(SurveyImport)
		self.siFilename_label.setGeometry(QtCore.QRect(190, 30, 671, 30))
		font = QtGui.QFont()
		font.setPointSize(9)
		font.setUnderline(False)
		font.setStrikeOut(False)
		self.siFilename_label.setFont(font)
		self.siFilename_label.setObjectName(_fromUtf8("siFilename_label"))
		self.siFileText_textEdit = QtGui.QTextEdit(SurveyImport)
		self.siFileText_textEdit.setGeometry(QtCore.QRect(30, 70, 490, 651))
		font = QtGui.QFont()
		font.setFamily(_fromUtf8("Consolas"))
		font.setPointSize(9)
		self.siFileText_textEdit.setFont(font)
		self.siFileText_textEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
		self.siFileText_textEdit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
		self.siFileText_textEdit.setLineWrapMode(QtGui.QTextEdit.NoWrap)
		self.siFileText_textEdit.setReadOnly(True)
		self.siFileText_textEdit.setTabStopWidth(40)
		self.siFileText_textEdit.setObjectName(_fromUtf8("siFileText_textEdit"))
		self.siStatus_label = QtGui.QLabel(SurveyImport)
		self.siStatus_label.setGeometry(QtCore.QRect(30, 750, 521, 21))
		font = QtGui.QFont()
		font.setPointSize(10)
		font.setBold(True)
		font.setWeight(75)
		self.siStatus_label.setFont(font)
		self.siStatus_label.setText(_fromUtf8(""))
		self.siStatus_label.setObjectName(_fromUtf8("siStatus_label"))

		self.retranslateUi(SurveyImport)
		QtCore.QMetaObject.connectSlotsByName(SurveyImport)

	def retranslateUi(self, SurveyImport):
		SurveyImport.setWindowTitle(_translate("SurveyImport", "Survey Data Import", None))
		self.siAccept_pushButton.setText(_translate("SurveyImport", "Accept", None))
		self.siOpenFile_pushButton.setText(_translate("SurveyImport", "Open...", None))
		item = self.siSurveyReport_tableWidget.horizontalHeaderItem(0)
		item.setText(_translate("SurveyImport", "MD", None))
		item = self.siSurveyReport_tableWidget.horizontalHeaderItem(1)
		item.setText(_translate("SurveyImport", "Inc", None))
		item = self.siSurveyReport_tableWidget.horizontalHeaderItem(2)
		item.setText(_translate("SurveyImport", "Azi", None))
		self.siExtract_pushButton.setText(_translate("SurveyImport", "Extract", None))
		self.siDelimiters_groupBox.setToolTip(_translate("SurveyImport", "It is mandatory to select one delimiter at least.", None))
		self.siDelimiters_groupBox.setTitle(_translate("SurveyImport", "Delimiters", None))
		self.siSpacesDelimiter_checkBox.setText(_translate("SurveyImport", "Space(s)", None))
		self.siSemicolonDelimiter_checkBox.setText(_translate("SurveyImport", "Semicolon", None))
		self.siTabDelimiter_checkBox.setText(_translate("SurveyImport", "Tab", None))
		self.siCommaDelimiter_checkBox.setText(_translate("SurveyImport", "Comma", None))
		self.siColumnIndexes_groupBox.setTitle(_translate("SurveyImport", "Column Indexes", None))
		self.label_5.setToolTip(_translate("SurveyImport", "MD index is a mandatory selection.", None))
		self.label_5.setText(_translate("SurveyImport", "<html><head/><body><p><span style=\" font-weight:600; color:#d62728;\">MD</span></p></body></html>", None))
		self.label_6.setToolTip(_translate("SurveyImport", "Hole ID index is a mandatory selection.", None))
		self.label_6.setText(_translate("SurveyImport", "<html><head/><body><p><span style=\" font-weight:600; color:#1f77b4;\">Inc</span></p></body></html>", None))
		self.siMDcolumnIndex_spinBox.setToolTip(_translate("SurveyImport", "MD and Hole ID indexes have to be different.", None))
		self.siInccolumnIndex_spinBox.setToolTip(_translate("SurveyImport", "MD and Hole ID indexes have to be different.", None))
		self.siAzicolumnIndex_spinBox.setToolTip(_translate("SurveyImport", "0 means that any column is selected.", None))
		self.label_8.setToolTip(_translate("SurveyImport", "BS unit must be the same as Hole ID unit,\n"
"in order to show a congruet graph. (optional)", None))
		self.label_8.setText(_translate("SurveyImport", "<html><head/><body><p><span style=\" font-weight:600; color:#00aa00;\">Azi</span></p></body></html>", None))
		self.siValueFeatures_groupBox.setTitle(_translate("SurveyImport", "Value features", None))
		self.siValueDecimalPoint_radioButton.setText(_translate("SurveyImport", "Decimal point ( . )", None))
		self.siValueDecimalComma_radioButton.setText(_translate("SurveyImport", "Decimal comma ( , )", None))
		self.label_11.setText(_translate("SurveyImport", "Starting row:", None))
		self.label_12.setText(_translate("SurveyImport", "End row: (max 50000)", None))
		self.label_13.setText(_translate("SurveyImport", "MD unit:", None))
		self.label_7.setText(_translate("SurveyImport", "Inc / Azi unit:", None))
		self.siEndingRow_spinBox.setToolTip(_translate("SurveyImport", "0 means that last row is selected.", None))
		self.siFilter_groupBox.setTitle(_translate("SurveyImport", "Filter", None))
		self.siMinimumMD_entry.setToolTip(_translate("SurveyImport", "Empty means 0.", None))
		self.siMaximumMD_entry.setToolTip(_translate("SurveyImport", "Empty means no maximum limit.", None))
		self.siMinimumInc_entry.setToolTip(_translate("SurveyImport", "Empty means 0.", None))
		self.siMaximumInc_entry.setToolTip(_translate("SurveyImport", "Empty means no maximum limit.", None))
		self.label_3.setText(_translate("SurveyImport", "< MD  <", None))
		self.label_4.setText(_translate("SurveyImport", "< Inc <", None))
		self.siMinimumAzi_entry.setToolTip(_translate("SurveyImport", "Empty means 0.", None))
		self.label_9.setText(_translate("SurveyImport", "< Azi <", None))
		self.siMaximumAzi_entry.setToolTip(_translate("SurveyImport", "Empty means no maximum limit.", None))
		self.siFilename_label.setText(_translate("SurveyImport", "<html><head/><body><p><span style=\" color:#646464;\">-- ANY CURRENT FILE --</span></p></body></html>", None))
		self.siFileText_textEdit.setHtml(_translate("SurveyImport", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Consolas\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))

