import sys
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QWindow
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidgetItem, QHeaderView, QApplication, QMainWindow, QListWidget, QWidget, QVBoxLayout,QHBoxLayout, QLabel, QPushButton, QListWidgetItem, QTableWidget,QTextBrowser
from DATA225utils import make_connection, dataframe_query
from PyQt5.QtCore import Qt 

class MyOrder(QWindow):
    """
    The main application window.
    """
    
    def __init__(self, myOrderWindow):
        """
        Load the UI and initialize its components.
        """
        super().__init__()
        
        self.ui = uic.loadUi('myOrders.ui')
        self.ui.show();   
        
        self.myOrderWindow = myOrderWindow
        self.customerId = self.myOrderWindow.get_cutomer_id()
        self.ui.customerIdValue.setText(str(self.customerId))
        self.ui.pushButtonBack.clicked.connect(self.pushButton)
        
        self.show_ordered_data()

    
    def show_ordered_data(self):    
        
            conn = make_connection(config_file = 'config_files/db_superstore.ini')
            cursor = conn.cursor()

            sql = ( f"""
                SELECT o.order_date, p.product_name, sc.quantity_ordered, sc.website_name , o.ship_mode, o.ship_date, FORMAT(sc.quantity_ordered*p.base_price , 2) as total
                FROM customer c 
                JOIN orders o ON c.customer_id = o.customer_id 
                JOIN shopping_cart sc ON o.order_id = sc.order_id 
                JOIN product p ON sc.product_id = p.product_id
                WHERE c.customer_id = {int(self.customerId)}
                """
              )  
            
            cursor.execute(sql)
            rows = cursor.fetchall()
            
            _, df = dataframe_query(conn,sql)
            
            grandtotal = 0

            for i in range(len(df)):
                grandtotal = grandtotal + float(df['total'][i].replace(",",""))


            cursor.close()
            conn.close()
        
            self.ui.tableMyOrderWidget.setRowCount(10)
            records = []
            row_index = 0
            for row in rows:
                column_index = 0
                record = []
                for data in row:
                    record.append(data)
                    column_index += 1
                records.append(record)
            
            self.ui.tableMyOrderWidget.setRowCount(len(records))

            
            for row in range(len(records)):
                for col in range(len(records[row])):
                    item = QTableWidgetItem(str(records[row][col]))
                    self.ui.tableMyOrderWidget.setItem(row, col, item)
          
            self.ui.tableMyOrderWidget.verticalHeader().setDefaultSectionSize(50)  
                 
    def pushButton(self):
        self.ui.close()
        
    def show_dialog(self):
        """
        Show this dialog.
        """
        self.ui.show()

    