from PyQt4 import QtCore, QtGui
import MdlUtilities as mdl
import re, time, sys
from functools import wraps

"""
def savetable(table, fields, filenames, orientation='h'):

	csvtext = ''
	
	for field in fields:
		csvtext += field.headerName +','
	csvtext = csvtext[:-1] +'\n'

	for i in range(len(fields[0])):
		for field in fields:
			if orientation=='h':
				item = table.item( i, field.pos )
			elif orientation=='v':
				item = table.item( field.pos, i )
			csvtext += item.text() +','
		csvtext = csvtext[:-1] +'\n'
	csvtext = csvtext[:-1]

	for filename in filenames:
		with open(filename,'w') as FILE:
			FILE.write(csvtext)
"""

def savetable(table, fields, filenames, orientation='h'):

	csvtext = ''
	
	if orientation=='h':

		for field in fields:
			csvtext += field.headerName +','
		csvtext = csvtext[:-1] +'\n'

		for i in range(len(fields[0])):
			for field in fields:
				item = table.item( i, field.pos )
				parts = re.split('\n',item.text())
				text = ''.join(parts)
				csvtext += text +','
			csvtext = csvtext[:-1] +'\n'
		csvtext = csvtext[:-1]

	elif orientation=='v':

		for field in fields:
			csvtext += field.headerName +','
			for i in range(len(fields[0])):
				item = table.item( field.pos, i )
				parts = re.split('\n',item.text())
				text = ''.join(parts)
				csvtext += text +','
			csvtext = csvtext[:-1] +'\n'
		csvtext = csvtext[:-1]

	for filename in filenames:
		with open(filename,'w',encoding='utf-8') as FILE:
			FILE.write(csvtext)



def waiting_effects(function):
	@wraps(function)
	def wrap_function(*args, **kwargs):
		QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
		try:
			function(*args, **kwargs)
		except Exception as e:
			raise e
			print("Error {}".format(e.args[0]))
		finally:
			QtGui.QApplication.restoreOverrideCursor()
	return wrap_function


def sleep(seconds):
	QtCore.QCoreApplication.processEvents()
	QtCore.QCoreApplication.flush()
	time.sleep(seconds)


idleFunction = lambda: sleep(0.01)


def size_object(obj, seen=None):
	"""Recursively finds size of objects and print lengths"""
	size = sys.getsizeof(obj)
	if seen is None:
		seen = set()
	obj_id = id(obj)
	if obj_id in seen:
		return 0
	
	seen.add(obj_id)
	if isinstance(obj, list):
		for i in obj:
			si = size_object(i, seen)
			size += si
	elif isinstance(obj, dict):
		for (k,v) in obj.items():
			if k!="parent" and k!="objectsSizes":
				sk = size_object(k, seen)
				sv = size_object(v, seen)
				size += sk+sv
	if hasattr(obj, '__dict__'):
		size += size_object(obj.__dict__, seen)
	return size


def count_nestedObjects(obj, seen=None, name=''):
	"""Recursively counts the number of objects in obj"""
	
	if re.match('[\w\.]*\._[\w]+',name):
		return 0

	count = 0
	if seen is None:
		seen = set()
	obj_id = id(obj)
	if obj_id in seen:
		return 0
	
	seen.add(obj_id)
	try:
		obj_len = len(obj)
	except TypeError:
		obj_len = 0

	if isinstance(obj, list):
		#print(name,'[] ',obj_len,'items')
		count += obj_len
		
	elif isinstance(obj, dict):
		#print(name,'{} ',obj_len,'items')
		#count += obj_len
		for (k,v) in obj.items():
			if k!="parent" and k!="objectsSizes":
				cv = count_nestedObjects(v, seen, name+'.'+str(k))
				if cv>0: print( name+'.'+str(k),cv,'items' )
				count += cv

	if hasattr(obj, '__dict__'):
		count += count_nestedObjects(obj.__dict__, seen, name)
	
	return count


def extend_text(text, size, mode='left'):
	
	L = size-len(text)

	if L>0:
		if mode=='left':
			s = ' '*L
			return text+s
		elif mode=='rigth':
			s = ' '*L
			return s+text
		elif mode=='center':
			sl = ' '*(L//2)
			sr = ' '*(L-L//2)
			return sl+text+sr
	else:
		return text


def handle_sorting_table(parent, tableWidget, __update_tableWidget):
	
	def _sort_tableWidget(newindex):
		
		if parent.sortIndicators[0] == newindex and parent.sortIndicators[1] ==1:
			_update_tableWidget()
		else:
			parent.sortIndicators = [newindex, tableWidgetHeader.sortIndicatorOrder()]
			tableWidgetHeader.setSortIndicator(*parent.sortIndicators)			
			
	def _update_tableWidget():
		
		parent.sortIndicators = [-1, 0]
		tableWidgetHeader.setSortIndicator(*parent.sortIndicators)
		tableWidget.setSortingEnabled(False)
		
		__update_tableWidget()
					
		tableWidget.setSortingEnabled(True)
		
	tableWidgetHeader = tableWidget.horizontalHeader()
	tableWidgetHeader.sectionClicked.connect(_sort_tableWidget)
	parent.sortIndicators = [-1, 0]
	tableWidgetHeader.setSortIndicator(*parent.sortIndicators)
	
	return _update_tableWidget


def clear_tableWidgetContent(tableWidget):

	for row in range(tableWidget.rowCount()):
		for column in range(tableWidget.columnCount()):
			item = tableWidget.item(row, column)
			item.set_text()


def clear_tableWidgetRow(tableWidget):

	row = tableWidget.selectedRow
	for column in range(tableWidget.columnCount()):
		item = tableWidget.item(row, column)
		item.set_text()
		item.alt_backgroundColor(False)
		item.alt_flags(False)

	return row


def remove_tableWidgetRow(tableWidget):

	row = tableWidget.selectedRow
	tableWidget.removeRow(row)


def insert_tableWidgetRow(tableWidget, fields):

	row = tableWidget.selectedRow
	tableWidget.insertRow(row)

	for field in fields:
		item = TableWidgetFieldItem( field, row%2==0 )
		tableWidget.setItem(row, field.pos, item)

	return row
	

def select_tableWidgetRow(tableWidget, row, alltherow=False):
	if alltherow:
		tableWidget.selectRow(row)
	tableWidget.selectedRow = row


def update_fieldItem(item, call=None):
	
	"""
	print('?',type(item))
	print('-',item.text(),item.field.unit,item.field.dataType,item.currentChangebyVst)
	print('??',TableWidgetFieldItem,isinstance(item,TableWidgetFieldItem))
	if isinstance(item,TableWidgetFieldItem):
		print('>')
		if item.currentChangebyVst:
			print('>>')
			item.set_text(item.text())

		item.currentChangebyVst = True
	"""
	if 'text' in dir(item):
		if item.currentChangebyVst:
			item.set_text(item.text())
			if call!=None:
				call()
		item.currentChangebyVst = True


class MandatoryError( Exception ): pass


class ValueWarning( Exception ): pass


class TableWidgetFieldItem( QtGui.QTableWidgetItem ):
	
	def __init__(self, field, isPar, altBg=False, altTx=False, altFg=False ):
		
		self.field = field
		self.isPar = isPar
		self.altBg = altBg
		self.altTx = altTx
		self.altFg = altFg
		super().__init__('')
		
		if altFg:
			self.setFlags(QtCore.Qt.ItemFlags(field.altFlag))
		else:
			self.setFlags(QtCore.Qt.ItemFlags(field.flag))
		if altTx:
			self.setTextColor(QtGui.QColor(*field.altTextColor))
		else:
			self.setTextColor(QtGui.QColor(*field.textColor))
		if altBg:	
			self.setBackgroundColor(QtGui.QColor(*field.altBackgroundColor-isPar*10))
		else:	
			self.setBackgroundColor(QtGui.QColor(*field.backgroundColor-isPar*10))
		self.realValue = mdl.physicalValue(None, field.unit)

		self.currentChangebyVst = True
		
	
	def set_text(self, value=None, unit=None):
		try:
			if value!=None:
				if value=='':
					raise(ValueError)

				# NEW{
				# if unit==None:
				# 	try:
				# 		unit = value.unit
				# 	except AttributeError:
				# 		unit = None
				# }

				if unit==self.field.unit or unit==None:
					value = self.field.dataType(value)
					realValue = mdl.physicalValue(value, self.field.unit)

					if isinstance(value, float):
						try:
							text = value.fraction
						except AttributeError:
							text = str( round(value, self.field.precision) )
					else:
						text = str( value )

				else:
					value = self.field.dataType(value)
					realValue = mdl.unitConvert_value( value, unit, self.field.unit )
					text = str( round(realValue, self.field.precision) )

				self.realValue = realValue
				self.currentChangebyVst = False
				super().setText( text )
				return True	
				
			else:
				raise(ValueError)
				
		except (ValueError,NameError,SyntaxError):
			self.realValue = mdl.physicalValue(None, self.field.unit)
			self.currentChangebyVst = False
			super().setText('')
			return False

		finally:
			self.currentChangebyVst = True
			
	
	def flip_backgroundColor(self):
		if self.altBg:	
			self.setBackgroundColor(QtGui.QColor(*self.field.backgroundColor-self.isPar*10))
			self.altBg = False
		else:	
			self.setBackgroundColor(QtGui.QColor(*self.field.altBackgroundColor-self.isPar*10))
			self.altBg = True
			
	
	def flip_textColor(self):
		if self.altTx:	
			self.setTextColor(QtGui.QColor(*self.field.textColor))
			self.altTx = False
		else:	
			self.setTextColor(QtGui.QColor(*self.field.altTextColor))
			self.altTx = True
			
	
	def flip_flags(self):
		if self.altFg:	
			self.setFlags(QtCore.Qt.ItemFlags(self.field.flag))
			self.altFg = False
		else:	
			self.setFlags(QtCore.Qt.ItemFlags(self.field.altFlag))
			self.altFg = True


	def alt_backgroundColor(self, alt=True):
		if alt and not self.altBg:
			self.setBackgroundColor(QtGui.QColor(*self.field.altBackgroundColor-self.isPar*10))
			self.altBg = True
		elif not alt and self.altBg:
			self.setBackgroundColor(QtGui.QColor(*self.field.backgroundColor-self.isPar*10))
			self.altBg = False
			
	
	def alt_textColor(self, alt=True):
		if alt and not self.altTx:
			self.setTextColor(QtGui.QColor(*self.field.altTextColor))
			self.altTx = True
		elif not alt and self.altTx:
			self.setTextColor(QtGui.QColor(*self.field.textColor))
			self.altTx = False
			
	
	def alt_flags(self, alt=True):
		if alt and not self.altFg:
			self.setFlags(QtCore.Qt.ItemFlags(self.field.altFlag))
			self.altFg = True
		elif not alt and self.altFg:
			self.setFlags(QtCore.Qt.ItemFlags(self.field.flag))
			self.altFg = False
			

class TableClipboard():

	def __init__(self, tableWidget):
		
		self.tableWidget = tableWidget
		self.selection = tableWidget.selectionModel().selectedIndexes()
		self.selectionDict = {}
		self.sys_clip = QtGui.QApplication.clipboard()
		self.text = None
		
	def selection_to_clipboard(self):
		
		if self.selection:
			for item in self.selection:
				self.selectionDict[(item.row(),item.column())] = item.data()
			
			rows	= [item.row()	for item in self.selection]
			columns = [item.column() for item in self.selection]
		
			self.text = ''
		
			for row in range( min(rows), max(rows)+1 ):
				for column in range( min(columns), max(columns)+1 ):
					self.text += str(self.selectionDict[(row,column)]) + '\t'
				self.text = self.text[:-1] + '\n'
			
			self.text = self.text[:-1]
			self.sys_clip.setText(self.text)
		
	def clipboard_to_selection(self):
	
		if self.selection:
	
			therow	= min(index.row()	for index in self.selection)
			thecolumn = min(index.column() for index in self.selection)
		
			self.text = self.sys_clip.text()
				
			for i,line in enumerate(re.split('[\n\r]+',self.text)[:-1]):
				for j,value in enumerate(re.split('\t',line)):
					item = self.tableWidget.item(therow+i,thecolumn+j)
					if item:
						try:
							if not item.field._altFg_:
								item.set_text(str(value))
						except AttributeError:
							item.setText(str(value))
					else:
						item = QtGui.QTableWidgetItem(str(value))
						self.tableWidget.setItem(therow+i,thecolumn+j, item)
					self.tableWidget.setItemSelected(item, True)


class CopySelectedCells_action(QtGui.QAction):
	
	def __init__(self, tableWidget):
		if not isinstance(tableWidget, QtGui.QTableWidget):
			raise ValueError(str('This action must be initialised with a QTableWidget. A %s was given.' % type(tableWidget)))
		super().__init__("Copy", tableWidget)
		self.setShortcut('Ctrl+C')
		self.setShortcutContext(QtCore.Qt.WidgetShortcut)
		self.triggered.connect(self.copy_cells_to_clipboard)
		self.tableWidget = tableWidget

	def copy_cells_to_clipboard(self):
		
		tc = TableClipboard(self.tableWidget)
		tc.selection_to_clipboard()


class PasteToCells_action(QtGui.QAction):
	
	def __init__(self, tableWidget):
		if not isinstance(tableWidget, QtGui.QTableWidget):
			raise ValueError(str('This action must be initialised with a QTableWidget. A %s was given.' % type(tableWidget)))
		super().__init__("Paste", tableWidget)
		self.setShortcut('Ctrl+V')
		self.setShortcutContext(QtCore.Qt.WidgetShortcut)
		self.triggered.connect(self.paste_clipboard_to_cells)
		self.tableWidget = tableWidget

	def paste_clipboard_to_cells(self):
		
		tc = TableClipboard(self.tableWidget)
		tc.clipboard_to_selection()


class FunctionToWidget_action(QtGui.QAction):
	
	def __init__(self, widget, function, menuDescription, shortcut=None):
		super().__init__(menuDescription, widget)
		if shortcut:
			self.setShortcut(shortcut)
			self.setShortcutContext(QtCore.Qt.WidgetShortcut)
		self.triggered.connect(function)




