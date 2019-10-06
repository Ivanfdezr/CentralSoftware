from PyQt4 import QtCore, QtGui
from TubularDatabase_Vst import Ui_TubularDatabase
import TubularDatabase_Mdl as mdl
import CtrlUtilities as cu

	
class Main_TubularDatabase(Ui_TubularDatabase):

	def __init__(self, dialog):
		
		Ui_TubularDatabase.__init__(self)
		self.setupUi(dialog)
		self.dialog = dialog
		self.__init__TDBPipeOD_listWidget()
		self.__init__TDB_tableWidget()
		
		dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		#
		dialog.exec_()
	
	
	def __init__TDBPipeOD_listWidget(self):
		
		ODs = mdl.get_pipeODList()
		for OD in ODs:
			self.TDBPipeOD_listWidget.addItem(OD)
		self.TDBPipeOD_listWidget.itemClicked.connect(self.update_TDB_tableWidget)
		
	
	def __init__TDB_tableWidget(self):
		
		item = self.TDBPipeOD_listWidget.item(0)
		item.setSelected(True)
		OD = item.text()
		self.TDBPipeOD_listWidget.selectedItem = item
		self.TDB_fields = mdl.get_TDB_fields()
		mdl.set_TDB_data_to_fields(OD, self.TDB_fields)

		for field in self.TDB_fields[:-2]:
			item = QtGui.QTableWidgetItem()
			self.TDB_tableWidget.setHorizontalHeaderItem( field.pos, item )
			item.setText( field.headerName )
			
		self.__update_TDB_tableWidget()
		self._update_TDB_tableWidget = cu.handle_sorting_table(self, self.TDB_tableWidget, self.__update_TDB_tableWidget )
		self.TDB_tableWidget.resizeColumnsToContents()
		
		self.TDB_tableWidget.cellPressed.connect(self.fetch_selectedPosition)
		self.TDB_tableWidget.itemChanged.connect(cu.update_fieldItem)

		self.TDB_tableWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.TDB_tableWidget.customContextMenuRequested.connect(self.open_menu)
	

	def fetch_selectedPosition(self,r,c):
		self.TDB_tableWidget.selectedRow    = r
		self.TDB_tableWidget.selectedColumn = c
		
	
	def open_menu(self, position):

		menu = QtGui.QMenu()

		ready = True
		try:
			for field in self.TDB_fields[:-2]:
				if self.TDB_tableWidget.item(self.TDB_tableWidget.selectedRow,field.pos).altFg:
					ready = False
					break
		except AttributeError:
			ready = False

		item = self.TDB_tableWidget.item(self.TDB_tableWidget.selectedRow,self.TDB_tableWidget.selectedColumn)

		C = cu.CopySelectedCells_action(self.TDB_tableWidget)
		menu.addAction(C)
		
		V = cu.PasteToCells_action(self.TDB_tableWidget)
		menu.addAction(V)
		
		X = cu.FunctionToWidget_action(self.TDB_tableWidget, self.export_pipe, "Export pipe")
		X.setEnabled( ready )
		menu.addAction(X)

		E = cu.FunctionToWidget_action(self.TDB_tableWidget, self.edit_pipe, "Edit property")
		menu.addAction(E)

		S = cu.FunctionToWidget_action(self.TDB_tableWidget, self.save_pipe, "Save to DB")
		S.setDisabled( ready )
		menu.addAction(S)

		action = menu.exec_(self.TDB_tableWidget.viewport().mapToGlobal(position))


	def export_pipe(self):
		
		cu.select_tableWidgetRow(self.TDB_tableWidget,self.TDB_tableWidget.selectedRow)
		cu.sleep(0.25)
		self.data   = self.TDB_fields.extract_data_from_row( self.TDB_tableWidget.selectedRow, representation=True )
		self.fields = self.TDB_fields.extract_fields_from_row( self.TDB_tableWidget.selectedRow )
		
		self.dialog.done(0)
	

	def edit_pipe(self):

		item = self.TDB_tableWidget.item(self.TDB_tableWidget.selectedRow,self.TDB_tableWidget.selectedColumn)
		if isinstance(item, cu.TableWidgetFieldItem):
			item.alt_backgroundColor()
			item.alt_flags()
		else:
			item = QtGui.QTableWidgetItem()
			self.TDB_tableWidget.setItem(self.TDB_tableWidget.selectedRow, field.pos, item)
		self.TDB_tableWidget.editItem(item)


	def save_pipe(self):
		
		pipeItems = []

		for field in self.TDB_fields[:-2]:
			
			text = self.TDB_tableWidget.item(self.TDB_tableWidget.selectedRow, field.pos).text()
			item = cu.TableWidgetFieldItem( field, self.TDB_tableWidget.selectedRow%2==0 )
			
			try:
				if item.field.mandatory:
					if text:
						if not item.set_text(text):
							raise(cu.MandatoryError)
					else:
						raise(cu.MandatoryError)
				else:
					if text:
						if not item.set_text(text):
							raise(cu.ValueWarning)
					else:
						raise(cu.ValueWarning)

			except cu.MandatoryError:
				msg = "'{representation}' is a mandatory property for any pipe.".format(representation=item.field.representation)
				QtGui.QMessageBox.critical(self.TDB_tableWidget, 'Error', msg)
				return False

			except cu.ValueWarning:
				msg = "Incorrect value in '{representation}'. This is a non-mandatory property.".format(representation=item.field.representation)
				QtGui.QMessageBox.information(self.TDB_tableWidget, 'Warning', msg)

			pipeItems.append( item )

		try:
			pipeID = self.TDB_fields[-1][self.TDB_tableWidget.selectedRow]
		except IndexError:
			pipeID = None
		
		mdl.save_pipe_to_DB( pipeItems, pipeID )

		self.update_TDB_tableWidget(self.TDBPipeOD_listWidget.selectedItem)

	
	def __update_TDB_tableWidget(self):
		
		self.TDB_tableWidget.clearContents()

		for i in range(self.TDB_tableWidget.rowCount()):
			try:
				data = self.TDB_fields.extract_data_from_row(i,representation=True)
				
				for field in self.TDB_fields[:-2]:
					item = cu.TableWidgetFieldItem( field, i%2==0 )
					self.TDB_tableWidget.setItem(i, field.pos, item)
					self.TDB_tableWidget.item(i, field.pos).set_text( data[ field.abbreviation ] )
			except IndexError:
				break
	
		
	def update_TDB_tableWidget(self, item):
		
		OD = item.text()
		self.TDBPipeOD_listWidget.selectedItem = item
		mdl.set_TDB_data_to_fields(OD, self.TDB_fields)
		self._update_TDB_tableWidget()
				
