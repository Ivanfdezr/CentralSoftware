from PyQt4 import QtCore, QtGui
from CentralizerDatabase_Vst import Ui_CentralizerDatabase
import CentralizerDatabase_Mdl as mdl
import CtrlUtilities as cu

	
class Main_CentralizerDatabase(Ui_CentralizerDatabase):

	def __init__(self, dialog, centralizerType=None):
		
		Ui_CentralizerDatabase.__init__(self)
		self.setupUi(dialog)
		self.dialog = dialog		
		
		self.centralizerTypeList = []
		for i in range(self.CDB_tabWidget.count()):
			self.centralizerTypeList.append( self.CDB_tabWidget.tabText(i) )

		self.__init__CDB_tabWidget(centralizerType)
		self.__init__CDBBowSpring_tableWidget()
		self.__init__CDBRigid_tableWidget()
		self.__init__CDBCasingOD_listWidget()

		def export_centralizer():
			if self.CDB_tabWidget.currentTabText == "Bow Spring":
				self.export_centralizer(self.CDBBowSpring_tableWidget, self.CDBBowSpring_fields)
			elif self.CDB_tabWidget.currentTabText == "Rigid":
				self.export_centralizer(self.CDBRigid_tableWidget, self.CDBRigid_fields)
		self.CDBAccept_pushButton.clicked.connect(export_centralizer)
		
		dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		dialog.exec_()
	
	
	def __init__CDB_tabWidget(self, centralizerType):

		if centralizerType:
			self.centralizerType = centralizerType

			for i,centralizerType in enumerate(self.centralizerTypeList):
				if self.centralizerType == centralizerType:
					self.CDB_tabWidget.setCurrentIndex(i)
				else:
					self.CDB_tabWidget.setTabEnabled(i,False)
		else:
			self.centralizerType = self.CDB_tabWidget.tabText( self.CDB_tabWidget.currentIndex() )
		
		self.CDB_tabWidget.currentChanged.connect(self.update_CDBCasingOD_listWidget)


	def __init__CDBCasingOD_listWidget(self):
		
		if self.centralizerType == 'Bow Spring':
			ODs = mdl.get_BowSpringCasingODList()
		elif self.centralizerType == 'Rigid':
			ODs = mdl.get_RigidCasingODList()

		for OD in ODs:
			self.CDBCasingOD_listWidget.addItem(OD)
		item = self.CDBCasingOD_listWidget.item(0)
		item.setSelected(True)
		
		self.CDBCasingOD_listWidget.selectedItem = item
		self.CDBCasingOD_listWidget.itemClicked.connect(self.update_CDB_tableWidget)
		
	
	def __init__CDBBowSpring_tableWidget(self):
		
		OD = mdl.get_BowSpringCasingODList()[0]
		self.CDBBowSpring_fields = mdl.get_CDBBowSpring_fields()
		mdl.set_CDBBowSpring_data_to_fields(OD, self.CDBBowSpring_fields)

		for field in self.CDBBowSpring_fields[:-2]:
			item = QtGui.QTableWidgetItem()
			self.CDBBowSpring_tableWidget.setHorizontalHeaderItem(field.pos, item)
			item.setText( field.headerName )

		__update_CDBBowSpring_tableWidget = lambda: self.__update_CDB_tableWidget(self.CDBBowSpring_tableWidget, self.CDBBowSpring_fields)
		__update_CDBBowSpring_tableWidget()
		self._update_CDBBowSpring_tableWidget = cu.handle_sorting_table(self, self.CDBBowSpring_tableWidget, __update_CDBBowSpring_tableWidget )
		self.CDBBowSpring_tableWidget.resizeColumnsToContents()
		
		#select_row = lambda r,c : cu.select_tableWidgetRow(self.CDBBowSpring_tableWidget,r,True)
		#self.CDBBowSpring_tableWidget.cellPressed.connect(select_row)
		__fetch_selectedPosition = lambda r, c: self.fetch_selectedPosition(self.CDBBowSpring_tableWidget, r, c)
		self.CDBBowSpring_tableWidget.cellPressed.connect(__fetch_selectedPosition)
		self.CDBBowSpring_tableWidget.itemChanged.connect(cu.update_fieldItem)
		
		__open_menu = lambda pos: self.open_menu(self.CDBBowSpring_tableWidget, self.CDBBowSpring_fields, pos)
		self.CDBBowSpring_tableWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.CDBBowSpring_tableWidget.customContextMenuRequested.connect(__open_menu)	


	def __init__CDBRigid_tableWidget(self):
		
		OD = mdl.get_RigidCasingODList()[0]
		self.CDBRigid_fields = mdl.get_CDBRigid_fields()
		mdl.set_CDBRigid_data_to_fields(OD, self.CDBRigid_fields)
		
		for field in self.CDBRigid_fields[:-2]:
			item = QtGui.QTableWidgetItem()
			self.CDBRigid_tableWidget.setHorizontalHeaderItem(field.pos, item)
			item.setText( field.headerName )

		__update_CDBRigid_tableWidget = lambda: self.__update_CDB_tableWidget(self.CDBRigid_tableWidget, self.CDBRigid_fields)
		__update_CDBRigid_tableWidget()
		self._update_CDBRigid_tableWidget = cu.handle_sorting_table(self, self.CDBRigid_tableWidget, __update_CDBRigid_tableWidget )
		self.CDBRigid_tableWidget.resizeColumnsToContents()
		
		#select_row = lambda r,c : cu.select_tableWidgetRow(self.CDBRigid_tableWidget,r,True)
		#self.CDBRigid_tableWidget.cellPressed.connect(select_row)
		__fetch_selectedPosition = lambda r, c: self.fetch_selectedPosition(self.CDBRigid_tableWidget, r, c)
		self.CDBRigid_tableWidget.cellPressed.connect(__fetch_selectedPosition)
		self.CDBRigid_tableWidget.itemChanged.connect(cu.update_fieldItem)
		
		__open_menu = lambda pos: self.open_menu(self.CDBRigid_tableWidget, self.CDBRigid_fields, pos)
		self.CDBRigid_tableWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.CDBRigid_tableWidget.customContextMenuRequested.connect(__open_menu)


	def fetch_selectedPosition(self, CDB_tableWidget, r, c):
		CDB_tableWidget.selectedRow    = r
		CDB_tableWidget.selectedColumn = c
		
	
	def open_menu(self, CDB_tableWidget, CDB_fields, position):

		menu = QtGui.QMenu()

		ready = True
		try:
			for field in CDB_fields[:-2]:
				if CDB_tableWidget.item(CDB_tableWidget.selectedRow,field.pos).altFg:
					ready = False
					break
		except AttributeError:
			ready = False

		#item = CDB_tableWidget.item(CDB_tableWidget.selectedRow,CDB_tableWidget.selectedColumn)

		C = cu.CopySelectedCells_action(CDB_tableWidget)
		menu.addAction(C)
		
		V = cu.PasteToCells_action(CDB_tableWidget)
		menu.addAction(V)
		
		export_centralizer = lambda: self.export_centralizer(CDB_tableWidget, CDB_fields)
		X = cu.FunctionToWidget_action(CDB_tableWidget, export_centralizer, "Export centralizer")
		X.setEnabled( ready )
		menu.addAction(X)

		edit_centralizer = lambda: self.edit_centralizer(CDB_tableWidget)
		E = cu.FunctionToWidget_action(CDB_tableWidget, edit_centralizer, "Edit property")
		menu.addAction(E)

		save_centralizer = lambda: self.save_centralizer(CDB_tableWidget, CDB_fields)
		S = cu.FunctionToWidget_action(CDB_tableWidget, save_centralizer, "Save to DB")
		S.setDisabled( ready )
		menu.addAction(S)

		action = menu.exec_(CDB_tableWidget.viewport().mapToGlobal(position))


	def export_centralizer(self, CDB_tableWidget, CDB_fields):
		
		cu.select_tableWidgetRow(CDB_tableWidget, CDB_tableWidget.selectedRow, True)
		cu.sleep(0.25)
		self.data = CDB_fields.extract_data_from_row( CDB_tableWidget.selectedRow, representation=True )
		self.fields = CDB_fields.extract_fields_from_row( CDB_tableWidget.selectedRow )
		
		self.dialog.done(0)
	

	def edit_centralizer(self, CDB_tableWidget):

		item = CDB_tableWidget.item(CDB_tableWidget.selectedRow,CDB_tableWidget.selectedColumn)
		if isinstance(item, cu.TableWidgetFieldItem):
			item.alt_backgroundColor()
			item.alt_flags()
		else:
			item = QtGui.QTableWidgetItem()
			CDB_tableWidget.setItem(CDB_tableWidget.selectedRow, field.pos, item)
		CDB_tableWidget.editItem(item)


	def save_centralizer(self, CDB_tableWidget, CDB_fields):
		
		centralizerItems = []

		for field in CDB_fields[:-2]:
			
			text = CDB_tableWidget.item(CDB_tableWidget.selectedRow, field.pos).text()
			item = cu.TableWidgetFieldItem( field, CDB_tableWidget.selectedRow%2==0 )
			
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
				msg = "'{representation}' is a mandatory property for any centralizer.".format(representation=item.field.representation)
				QtGui.QMessageBox.critical(CDB_tableWidget, 'Error', msg)
				return False

			except cu.ValueWarning:
				msg = "Incorrect value in '{representation}'. This is a non-mandatory property.".format(representation=item.field.representation)
				QtGui.QMessageBox.information(CDB_tableWidget, 'Warning', msg)

			centralizerItems.append( item )

		try:
			centralizerID = CDB_fields[-1][CDB_tableWidget.selectedRow]
		except IndexError:
			centralizerID = None
		
		mdl.save_centralizer_to_DB( centralizerItems, centralizerID )

		self.update_CDB_tableWidget(self.CDBCasingOD_listWidget.selectedItem)


	def __update_CDB_tableWidget(self, CDB_tableWidget, CDB_fields):
		
		CDB_tableWidget.clearContents()

		for i in range(CDB_tableWidget.rowCount()):
			try:
				data = CDB_fields.extract_data_from_row(i,representation=True)
				
				for field in CDB_fields[:-2]:
					item = cu.TableWidgetFieldItem( field, i%2==0 )
					CDB_tableWidget.setItem(i, field.pos, item)
					CDB_tableWidget.item(i, field.pos).set_text( data[ field.abbreviation ] )
			except IndexError:
				break
	
		
	def update_CDB_tableWidget(self, item):
		
		OD = item.text()
		self.CDBCasingOD_listWidget.selectedItem = item
		
		if self.centralizerType=='Bow Spring':
			mdl.set_CDBBowSpring_data_to_fields(OD, self.CDBBowSpring_fields)
			self._update_CDBBowSpring_tableWidget()
		
		elif self.centralizerType=='Rigid':
			mdl.set_CDBRigid_data_to_fields(OD, self.CDBRigid_fields)
			self._update_CDBRigid_tableWidget()


	def update_CDBCasingOD_listWidget(self, index):

		self.centralizerType = self.CDB_tabWidget.tabText( index )

		if self.centralizerType == 'Bow Spring':
			ODs = mdl.get_BowSpringCasingODList()
			theOD = self.CDBBowSpring_fields.OD
		elif self.centralizerType == 'Rigid':
			ODs = mdl.get_RigidCasingODList()
			theOD = self.CDBRigid_fields.OD

		self.CDBCasingOD_listWidget.clear()
		for OD in ODs:
			self.CDBCasingOD_listWidget.addItem(OD)
		item = self.CDBCasingOD_listWidget.item( ODs.index(theOD) )
		self.CDBCasingOD_listWidget.selectedItem=item
		item.setSelected(True)
		
		