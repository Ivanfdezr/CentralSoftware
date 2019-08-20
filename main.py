from PyQt4.QtGui import QApplication, QMainWindow, QStyleFactory
#from untitled import Ui_MainWindow
from input_window import Ui_InputWindow
if __name__ == "__main__":
    app = QApplication([])
    #app.setStyle(QWindowsStyle)
    QApplication.setStyle(QStyleFactory.create('Plastique'))
    window = QMainWindow()
    #main_window = Ui_MainWindow()
    main_window = Ui_InputWindow()
    main_window.setupUi(window)
    window.show()
    app.exec_()
