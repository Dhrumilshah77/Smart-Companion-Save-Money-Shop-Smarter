import sys
from PyQt5 import uic,QtGui
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QWindow
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidgetItem, QHeaderView, QApplication, QMainWindow, QListWidget, QWidget, QVBoxLayout,QHBoxLayout, QLabel, QPushButton, QListWidgetItem, QTableWidget,QTextBrowser, QMessageBox
from DATA225utils import make_connection
from PyQt5.QtCore import Qt 

class Signin(QWindow):
    """
    The Register application window.
    """
    
    def __init__(self, myCartWindow):
        """
        Load the UI and initialize its components.
        """
        super().__init__()
        
        self.myCartWindow = myCartWindow
        
        self.ui = uic.loadUi('Signin.ui')
        self.ui.show();
        
        self.ui.pushBtnSignIn.clicked.connect(self.check_signin)
    
        
    def check_signin(self):
        customerId = self.ui.lineEditcustomerId.text()
        
        if len(customerId) == 6:
            
            if customerId!="":

                conn = make_connection(config_file = 'config_files/db_superstore.ini')
                cursor = conn.cursor()

                sql_cu = (f"""
                            SELECT * FROM customer 
                            WHERE customer_id='{customerId}'
                            """
                         )
                cursor.execute(sql_cu)

                record = cursor.fetchall()


                if len(record) > 0:
                    self.myCartWindow.update_label_text('Customer Id:',customerId)
                    self.myCartWindow.mYCartshowButton()
                    self.myCartWindow.mYCarthideButton()
                    self.ui.close()

                else:
                    msgBox = QMessageBox()
                    msgBox.setIcon(QMessageBox.Information)
                    msgBox.setText("No Such Customer Id exists")
                    msgBox.setWindowTitle("Failure")
                    msgBox.setStandardButtons(QMessageBox.Ok)
                    msgBox.exec_() 

                cursor.close()
                conn.close()

            else:
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Information)
                msgBox.setText("All Fields are mandatory.")
                msgBox.setWindowTitle("Failure")
                msgBox.setStandardButtons(QMessageBox.Ok)
                msgBox.exec_()        

        elif len(customerId) > 6:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("It must be 6 digit number")
            msgBox.setWindowTitle("Failure")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec_()
        else:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("It must be 6 digit number")
            msgBox.setWindowTitle("Failure")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec_()
  
        
    def show_dialog(self):
        """
        Show this dialog.
        """
        self.ui.show()
        
    