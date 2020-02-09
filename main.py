from PyQt4 import QtCore, QtGui
from InputWindow_Ctrl import Main_InputWindow

def main():
	app = QtGui.QApplication([])
	window = QtGui.QMainWindow()
	#window.setMinimumSize(400, 300)
	main_iw = Main_InputWindow(window)
	
	window.show()
	app.exec_()

if __name__ == "__main__":
	main()