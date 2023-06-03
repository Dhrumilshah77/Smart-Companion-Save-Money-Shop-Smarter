import sys
from PyQt5 import uic, QtGui
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QWindow
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidgetItem, QHeaderView, QApplication, QMainWindow, QListWidget, QWidget, QVBoxLayout,QHBoxLayout, QLabel, QPushButton, QListWidgetItem, QTableWidget,QTextBrowser, QMessageBox
from DATA225utils import make_connection
from PyQt5.QtCore import Qt 
from MyOrder import MyOrder

class SignInOrder(QWindow):
    """
    The Register application window.
    """
    
    def __init__(self):
        """
        Load the UI and initialize its components.
        """
        super().__init__()
        
        
        self.ui = uic.loadUi('Signin.ui')
        self.ui.show();
        
        self.ui.pushBtnSignIn.clicked.connect(self.check_signinorder)
               
        
    def check_signinorder(self):
        
        
        customerId = self.ui.lineEditcustomerId.text()

        if len(customerId) == 6:
            
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
               
                self.show_myorderWindow = MyOrder(self)
                self.show_myorderWindow.show_dialog()
                self.ui.close()
         
            else:
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Information)
                msgBox.setText("No Such Customer Id exists")
                msgBox.setWindowTitle("Failure")
                msgBox.setStandardButtons(QMessageBox.Cancel)
                msgBox.exec_() 
                
            cursor.close()
            conn.close()
            
        elif len(customerId)<6:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("It must be 6 digit number")
            msgBox.setWindowTitle("Failure")
            msgBox.setStandardButtons(QMessageBox.Cancel)
            msgBox.exec_() 
                
        elif len(customerId)>6:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("It must be 6 digit number")
            msgBox.setWindowTitle("Failure")
            msgBox.setStandardButtons(QMessageBox.Cancel)
            msgBox.exec_() 
        
        else:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Please Enter Customer ID")
            msgBox.setWindowTitle("Failure")
            msgBox.setStandardButtons(QMessageBox.Cancel)
            msgBox.exec_()        

        
    def show_dialog(self):
        """
        Show this dialog.
        """
        self.ui.show()
     
    def get_cutomer_id(self):
        customerId = self.ui.lineEditcustomerId.text()
        return customerId
