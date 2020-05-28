from PyQt4 import QtCore, QtGui
from CaliperInsertion_Vst import Ui_CaliperInsertion
import CaliperInsertion_Mdl as mdl
import CtrlUtilities as cu
import MdlUtilities as mu


class Main_CaliperInsertion(Ui_CaliperInsertion):

	def __init__(self, dialog):
		
		Ui_CaliperInsertion.__init__(self)
		self.setupUi(dialog)
		self.dialog = dialog

		self.__init__csvCal_tableWidget()

		self.csvAccept_pushButton.clicked.connect( self.makeResults_and_done )
		self.csvClearAll_pushButton.clicked.connect( self.clear_all )

		dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		dialog.exec_()


	def __init__csvCal_tableWidget(self):
		
		self.csvCal_tableWidget.parent = self
		self.csvCal_tableWidget.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
		
		C = cu.CopySelectedCells_action(self.csvCal_tableWidget)
		self.csvCal_tableWidget.addAction(C)
		
		V = cu.PasteToCells_action(self.csvCal_tableWidget)
		self.csvCal_tableWidget.addAction(V)

		insert_row = lambda: cu.insert_tableWidgetRow(self.csvCal_tableWidget, self.csvCal_fields)
		I = cu.FunctionToWidget_action(self.csvCal_tableWidget, insert_row, "Insert above row")
		self.csvCal_tableWidget.addAction(I)

		remove_row = lambda: cu.remove_tableWidgetRow(self.csvCal_tableWidget)
		R = cu.FunctionToWidget_action(self.csvCal_tableWidget, remove_row, "Remove row")
		self.csvCal_tableWidget.addAction(R)

		clear_row = lambda: cu.clear_tableWidgetRow(self.csvCal_tableWidget)
		D = cu.FunctionToWidget_action(self.csvCal_tableWidget, clear_row, "Clear row", 'Del')
		self.csvCal_tableWidget.addAction(D)
		
		self.setup_csvCal_tableWidget()

		select_row = lambda r,c : cu.select_tableWidgetRow(self.csvCal_tableWidget,r)
		self.csvCal_tableWidget.cellPressed.connect(select_row)
		self.csvCal_tableWidget.itemChanged.connect(cu.update_fieldItem)

		self.csvCal_tableWidget.resizeColumnsToContents()


	def setup_csvCal_tableWidget(self):

		self.csvCal_fields = mdl.get_csvCal_fields()
		for field in self.csvCal_fields[:3]:
			item = self.csvCal_tableWidget.horizontalHeaderItem( field.pos )
			item.setText( field.headerName )
			
			for i in range(self.csvCal_tableWidget.rowCount()):
				item = cu.TableWidgetFieldItem( field, i%2==0 )
				self.csvCal_tableWidget.setItem(i, field.pos, item)


	def makeResults_and_done(self):

		self.csvCal_fields.clear_content()

		i=0
		while True:
		
			if i == self.csvCal_tableWidget.rowCount():
				break

			top  = self.csvCal_tableWidget.item(i, self.csvCal_fields.MDtop.pos ).realValue
			bot = self.csvCal_tableWidget.item(i, self.csvCal_fields.MDbot.pos).realValue
			hid = self.csvCal_tableWidget.item(i, self.csvCal_fields.HID.pos).realValue
			
			i+=1
			if mu.isNoneEntry(top) or mu.isNoneEntry(bot) or mu.isNoneEntry(hid):
				continue

			self.csvCal_fields.MDtop.append( top )
			self.csvCal_fields.MDbot.append( bot )
			self.csvCal_fields.MD.append( top )
			self.csvCal_fields.MD.append( bot )
			self.csvCal_fields.HID.append( hid )
			self.csvCal_fields.HID.append( hid )
		
		id_mean = mdl.make_weightedAverage( self.csvCal_fields )

		self.HID = mu.array( self.csvCal_fields.HID )
		self.MD  = mu.array( self.csvCal_fields.MD )

		self.csvCaliperReport_fields = mdl.get_csvCaliperReport_fields()
		max_MD = max(self.csvCal_fields.MD)
		min_MD = min(self.csvCal_fields.MD)

		mu.create_physicalValue_and_appendTo_field( 'Manual-CAL', self.csvCaliperReport_fields.Desc    )
		mu.create_physicalValue_and_appendTo_field( id_mean,  self.csvCaliperReport_fields.ID      )
		#mu.create_physicalValue_and_appendTo_field( bs_mean,  self.csvCaliperReport_fields.DriftID )
		mu.create_physicalValue_and_appendTo_field( min_MD,   self.csvCaliperReport_fields.MDtop   )
		mu.create_physicalValue_and_appendTo_field( max_MD,   self.csvCaliperReport_fields.MDbot   )

		##
		self.data = self.csvCaliperReport_fields.extract_data_from_row( 0 )
		self.fields = self.csvCaliperReport_fields
		self.dialog.done(0)


	def clear_all(self):

		self.csvCal_fields.clear_content()
		for i in range(self.csvCal_tableWidget.rowCount()):
			for field in self.csvCal_fields:
				self.csvCal_tableWidget.item(i, field.pos).set_text()