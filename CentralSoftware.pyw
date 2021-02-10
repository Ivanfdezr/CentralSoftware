from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from InputWindow_Ctrl import Main_InputWindow

def main():
	app = QApplication([])
	window = QMainWindow()
	#window.setMinimumSize(400, 300)
	main_iw = Main_InputWindow(window)
	
	window.show()
	app.exec_()

if __name__ == "__main__":
	main()