import sys
from PyQt5 import uic, QtGui
from PyQt5 import QtCore
from PyQt5.QtGui import QWindow
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidgetItem, QHeaderView, QApplication, QMainWindow, QListWidget, QWidget, QVBoxLayout,QHBoxLayout, QLabel, QPushButton, QListWidgetItem, QTableWidget,QTextBrowser, QMessageBox
from DATA225utils import make_connection
from PyQt5.QtCore import Qt 
from Signin import Signin

class Register(QWindow):
    """
    The Register application window.
    """
    
    def __init__(self,myCartWindow):
        """
        Load the UI and initialize its components.
        """
        super().__init__()
        self.myCartWindow = myCartWindow
        self.ui = uic.loadUi('Register.ui')
        self.ui.show();
        
        self.country_name()
        self.state_name()
        self.city_name()
        self.segment_name()
        
        self.ui.pushBtnAddDetails.clicked.connect(self.add_details)
        self.ui.comboBoxCountry.currentIndexChanged.connect(self.handle_dropdown)
        self.ui.comboBoxState.currentIndexChanged.connect(self.handle_dropdown)
        self.ui.comboBoxCity.currentIndexChanged.connect(self.handle_dropdown)
        self.ui.comboBoxSegment.currentIndexChanged.connect(self.handle_dropdown)
        
        self.country_selected = self.ui.comboBoxCountry.itemText(0)
        self.state_selected = self.ui.comboBoxState.itemText(0)
        self.city_selected = self.ui.comboBoxCity.itemText(0)
        self.segment_selected = self.ui.comboBoxSegment.itemText(0)
        
        self.validator = QtGui.QIntValidator()
        
        self.ui.lineEditpostalCode.setValidator(self.validator)
        self.ui.lineEditpostalCode.textChanged.connect(self.validate_text)
    
    def validate_text(self):
        text = self.ui.lineEditpostalCode.text()
#         if self.ui.lineEditpostalCode.hasAcceptableInput():
#             self.ui.postalCodeErrorLabel.clear()
#         else:
#             self.ui.postalCodeErrorLabel.setText("Invalid input. Please enter a number.")

        if len(text) == 0:
            self.ui.postalCodeErrorLabel.clear()
        elif len(text) == 5:
            self.ui.postalCodeErrorLabel.clear()
        elif len(text) < 5:
            self.ui.postalCodeErrorLabel.setText("It must be a 5 digit number.")
        elif len(text) > 5:
            self.ui.postalCodeErrorLabel.setText("It must be a 5 digit number.")
        else:
            self.ui.postalCodeErrorLabel.clear()
        
    def country_name(self):
        conn = make_connection(config_file = 'config_files/db_superstore.ini')
        cursor = conn.cursor()
        
        sql = "SELECT DISTINCT country FROM customer ORDER BY country ASC"
        
        cursor.execute(sql)
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        for row in rows:
            name = row[0]
            self.ui.comboBoxCountry.addItem(name, row)
            
    def state_name(self):
        conn = make_connection(config_file = 'config_files/db_superstore.ini')
        cursor = conn.cursor()
        
        sql = "SELECT DISTINCT state FROM customer ORDER BY state ASC"
        
        cursor.execute(sql)
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        for row in rows:
            name = row[0]
            self.ui.comboBoxState.addItem(name, row)
        
        
    def city_name(self):
        conn = make_connection(config_file = 'config_files/db_superstore.ini')
        cursor = conn.cursor()
        
        sql = "SELECT DISTINCT city FROM customer ORDER BY city ASC"
        
        cursor.execute(sql)
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        for row in rows:
            name = row[0]
            self.ui.comboBoxCity.addItem(name, row)
            
            
    def segment_name(self):
        conn = make_connection(config_file = 'config_files/db_superstore.ini')
        cursor = conn.cursor()
        
        sql = "SELECT DISTINCT segment FROM customer ORDER BY segment ASC"
        
        cursor.execute(sql)
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        for row in rows:
            name = row[0]
            self.ui.comboBoxSegment.addItem(name, row)
            
        
    
    def handle_dropdown(self):
        self.country_selected = self.ui.comboBoxCountry.currentText()
        self.state_selected = self.ui.comboBoxState.currentText()
        self.city_selected = self.ui.comboBoxCity.currentText()
        self.segment_selected = self.ui.comboBoxSegment.currentText()
        
        
    def add_details(self):
        firstName = self.ui.lineEditFirstName.text()
        lastName = self.ui.lineEditLastName.text()
        streetAddress = self.ui.textEditStreetAddress.toPlainText()
        postalCode = self.ui.lineEditpostalCode.text()

        val = (firstName, lastName, streetAddress, self.city_selected, self.state_selected , self.country_selected, postalCode, self.segment_selected)

        
        if firstName!="" and lastName!="" and streetAddress!="" and postalCode!="":
       
            conn = make_connection(config_file = 'config_files/db_superstore.ini')
            cursor = conn.cursor()

            sql_cu = (   """
                    INSERT INTO customer ( customer_first_name, customer_last_name, street_address, city, state, country, 
                    postal_code, segment)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """
                     )
            cursor.execute(sql_cu,val)
            conn.commit()
        
            if cursor.rowcount > 0:
                
                sql_cust = """SELECT MAX(customer_id) FROM customer"""
                
                cursor.execute(sql_cust)
                rows = cursor.fetchall()
                
                customerID = rows[0][0]
                
                
                self.myCartWindow.update_label_text('Customer Id:',str(customerID))
                self.myCartWindow.mYCartshowButton()
                self.myCartWindow.mYCarthideButton()
                self.ui.close()
               
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Information)
                msgBox.setText(f"Your Customer ID is {customerID}")
                msgBox.setWindowTitle("Customer Id")
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
            
        
    def show_dialog(self):
        """
        Show this dialog.
        """
        self.ui.show()
        
