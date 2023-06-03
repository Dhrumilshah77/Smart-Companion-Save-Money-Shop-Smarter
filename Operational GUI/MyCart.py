import sys
import sqlite3
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QWindow
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidgetItem, QHeaderView, QApplication, QMainWindow, QListWidget, QWidget, QVBoxLayout,QHBoxLayout, QLabel, QPushButton, QListWidgetItem, QTableWidget,QTextBrowser, QMessageBox
from DATA225utils import make_connection, dataframe_query
from PyQt5.QtCore import Qt 
from Register import Register
from Signin import Signin

class MyCart(QWindow):
    """
    The main application window.
    """
    
    def __init__(self):
        """
        Load the UI and initialize its components.
        """
        super().__init__()
        
        self.ui = uic.loadUi('MyCart.ui')
        self.ui.show();   
        
        totalAmount = 0
        self.finalTotalAmount = 0
        self.myCartProducts = []
        
        self._initialize_table()
        self._enter_product_data()
        self._initialize_shipping()
        self.ui.labelCustomerid.setText("")
        
        #selected_index = self.ui.comboBoxShipping.currentIndex()
        self.ui.pushBtnBuyNow.hide()
        self.ui.comboBoxShipping.currentIndexChanged.connect(self.update_query)
        self.ui.pushBtnExistingNo.clicked.connect(self.add_customer)
        self.ui.pushBtnExistingYes.clicked.connect(self.signin_customer)
        self.ui.pushBtnBuyNow.clicked.connect(self.buy_now)
        #self.ui.pushBtnMyCart.clicked.connect(self.my_cart)
        
        
    def _adjust_column_widths(self):
        """
        Adjust the column widths of the product table to fit the contents.
        """
        header = self.ui.tableMyCart.horizontalHeader();
        #header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
#         header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
#         header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
#         header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        
        
    def _initialize_table(self):
        """
        Clear the table and set the column headers.
        """
        self.ui.tableMyCart.clear()
        
        headers = ["Product Name", "Website Name", "Quantity Ordered", "Total", "Action"]
        self.ui.tableMyCart.setHorizontalHeaderLabels(headers)    
        
        self._adjust_column_widths()    

    
    def _enter_product_data(self):  
        self.ui.tableMyCart.clear()
        self._initialize_table()
        
        conn = make_connection(config_file = 'config_files/db_superstore.ini')
        cursor = conn.cursor()

        sql = ( """
            SELECT tc.product_name,tc.website_name, tc.quantity_ordered, FORMAT(tc.quantity_ordered*tc.price,2), ''
            from temp_cart tc 
            """
          )  

        total_amount_sql = ( """
            SELECT FORMAT(SUM(tc.quantity_ordered*tc.price),2) as total_amount
            FROM temp_cart tc
            """
          ) 

        cursor.execute(sql)
        rows = cursor.fetchall()

        cursor.execute(total_amount_sql)
        total_amount = cursor.fetchall()

        cursor.close()
        conn.close()

        self.ui.tableMyCart.setRowCount(10)
        records = []
        row_index = 0
        for row in rows:
            column_index = 0
            record = []
            for data in row:
                record.append(data)
                column_index += 1
            records.append(record)

        self.myCartProducts = records
        self.ui.tableMyCart.setRowCount(len(records))

        for row in total_amount:
            for data in row:
                if data:
                    total_amount = float(data.replace(",", "")) + float(5)
                    self.ui.textTotalAmount.setText(str(total_amount))
                    self.finalTotalAmount = float(total_amount) 
                else: 
                    self.ui.close()

        for row in range(len(records)):
            for col in range(len(records[row])):
                item = QTableWidgetItem(str(records[row][col]))
                self.ui.tableMyCart.setItem(row, col, item)

                #Add a button to the last column of each row
                remove_button = QPushButton("Remove")

                remove_button.setStyleSheet("""
                QPushButton {
                            border-radius: 6px;
                            padding: 5px;
                            background-color: #DC143C;
                            color: white;
                        }

                QPushButton:hover {
                            background-color: #DA012D;
                        }

                QPushButton:pressed {
                            background-color: #006666;
                        }

                """

                )
                remove_button.clicked.connect(lambda _, row=row: self.remove_from_cart(row))


            layout = QHBoxLayout()
            layout.addWidget(remove_button)

            layout.setAlignment(remove_button, QtCore.Qt.AlignCenter)
            widget = QWidget()
            widget.setLayout(layout)
            self.ui.tableMyCart.setCellWidget(row, 4, widget)     



        self.ui.tableMyCart.verticalHeader().setDefaultSectionSize(50)  
    
    def remove_from_cart(self,index):
        
        button = self.sender()
        
        product_name = self.ui.tableMyCart.item(index, 0).text()
        website_name = self.ui.tableMyCart.item(index, 1).text()
        quantity_ordered = self.ui.tableMyCart.item(index, 2).text()
        totalPrice = float(self.ui.tableMyCart.item(index, 3).text().replace(",", ""))
        
        val = (product_name,website_name,quantity_ordered,totalPrice)
        
        conn = make_connection(config_file = 'config_files/db_superstore.ini')
        cursor = conn.cursor()
        
        sql_remove = f"""DELETE FROM temp_cart 
                        WHERE product_name='{product_name}'
                        AND website_name = '{website_name}'
                        AND quantity_ordered = {int(quantity_ordered)}"""
        
        # Execute a query that might raise an exception
        cursor.execute('SET SQL_SAFE_UPDATES = 0;')
        conn.commit()

        # Delete all rows from the table
        cursor.execute(sql_remove)

        # Re-enable safe mode
        cursor.execute('SET SQL_SAFE_UPDATES = 1;')
        conn.commit()
       
        cursor.close()
        conn.close()
        
        self._enter_product_data()
        
        

    def _initialize_shipping(self):
            conn = make_connection(config_file = 'config_files/db_superstore.ini')
            cursor = conn.cursor()

            sql = "SELECT ship_mode,shipping_fee FROM ship_mode ORDER BY no_of_days_for_ship DESC"

            cursor.execute(sql)
            rows = cursor.fetchall()

            cursor.close()
            conn.close()

            for row in rows:
                mode = row[0] + f' ( ${row[1]} Ship Fee )'
                self.ui.comboBoxShipping.addItem(mode, row)
                
                
    def update_query(self):
        # Construct the SQL query based on the selected category
        selected_Text = self.ui.comboBoxShipping.currentText()
        selected_Text, _ = selected_Text.split('(')
        
        
        conn = make_connection(config_file = 'config_files/db_superstore.ini')
        
        
        try:
            # Create a cursor object
            cursor = conn.cursor()

            # Execute a query that might raise an exception
            total_amount_sql = ( """
                SELECT FORMAT(SUM(tc.quantity_ordered*tc.price),2) as total_amount
                FROM temp_cart tc
                """
              ) 

            cursor.execute(total_amount_sql)
            total_amount = cursor.fetchall()

        except sqlite3.Error as e:
            # Handle the exception
            print('An error occurred:', e)

        finally:
            # Close the connection
            cursor.close()
            conn.close()
               
        for row in total_amount:
            for data in row:
                totalAmount = data.replace(",", "")
                self.ui.textTotalAmount.setText(str(totalAmount))
        
        if selected_Text:      
            
            conn = make_connection(config_file = 'config_files/db_superstore.ini')
            cursor = conn.cursor()
            ship_fee_sql = ( f"""
                SELECT shipping_fee as ship_fee
                FROM ship_mode
                WHERE ship_mode = '{selected_Text[:-1]}'
                """
              ) 
            
            cursor.execute(ship_fee_sql)
            rows = cursor.fetchall()                   
              
            cursor.close()
            conn.close()
            
            for row in rows:
                for data in row:
                    
                    self.finalTotalAmount = float(totalAmount) + float(data)
                    self.ui.textTotalAmount.setText(f"{str(self.finalTotalAmount)}")
                    
                                            
        else:
            self.finalTotalAmount = float(totalAmount)
            self.ui.textTotalAmount.setText(f"{str(self.finalTotalAmount)}")
                
    def add_customer(self):
        self.add_customer_dialog = Register(self)
        self.add_customer_dialog.show_dialog()
        
    def signin_customer(self):
        self.signin_customer_dialog = Signin(self)
        self.signin_customer_dialog.show_dialog()
        
    def update_label_text(self, text1, text2):
        self.ui.labelCustomerid.setText(text1)
        self.ui.customerIdValue.setText(text2)
        
        
    def buy_now(self):
        
        
        customerId = self.ui.customerIdValue.text()
        totalAmountFinal = self.finalTotalAmount
        shipMode,_ = self.ui.comboBoxShipping.currentText().split('(')
        shipMode = shipMode[:-1]
        
        
        conn = make_connection(config_file = 'config_files/db_superstore.ini')
        
        try:
            # Create a cursor object
            cursor = conn.cursor()
            
            sql_temp_cart = """SELECT * 
                     FROM temp_cart"""
            
            _, df = dataframe_query(conn,sql_temp_cart)
            
            
#             sql_inner = f"""SELECT no_of_days_for_ship FROM ship_mode WHERE ship_mode = {shipMode}"""
            
#             cursor.execute(sql_inner)
            
#             row = cursor.fetchall()
            
#             numOfDays = int(row[0][0])
            
            
            sql_order = f"""INSERT INTO orders (order_date, order_total, ship_mode, ship_date, customer_id) 
            VALUES (DATE_FORMAT(CURDATE(), '%Y-%m-%d'),{totalAmountFinal}, '{shipMode}', 
            DATE_FORMAT(CURDATE() + (SELECT no_of_days_for_ship FROM ship_mode WHERE ship_mode = '{shipMode}'), '%Y-%m-%d'), {customerId});"""

            cursor.execute(sql_order)
            
            conn.commit()
            
            for i in df.iterrows():
                

                
                productId = i[1][0]
                quantityOrdered = int(i[1][5])
                websiteName = i[1][4]
                
                
                sql_shopping_cart=f"""INSERT INTO shopping_cart
             VALUES ( '{productId}', (SELECT MAX(order_id) FROM orders),  {quantityOrdered}, '{websiteName}');"""


                cursor.execute(sql_shopping_cart)
                conn.commit()
                
                sql = f"""(SELECT quantity_available-{quantityOrdered} FROM product WHERE product_id = '{productId}')"""
                
                cursor.execute(sql)
                
                rows = cursor.fetchall()
                cursor.execute('SET SQL_SAFE_UPDATES = 0;')
                sql_query=f"""UPDATE product 
                            SET quantity_available = {int(rows[0][0])}
                            WHERE product_id = '{productId}';"""
            

                cursor.execute(sql_query)
                
                cursor.execute('SET SQL_SAFE_UPDATES = 1;')
                conn.commit()
            
           

            # Execute a query that might raise an exception
            cursor.execute('SET SQL_SAFE_UPDATES = 0;')

            # Delete all rows from the table
            cursor.execute('DELETE FROM temp_cart;')

            # Re-enable safe mode
            cursor.execute('SET SQL_SAFE_UPDATES = 1;')

            # Commit the changes
            conn.commit()
            
            
            sql_check_data = "SELECT COUNT(*) FROM temp_cart"
            
            cursor.execute(sql_check_data)
            
            row = cursor.fetchall()
            
            if row[0][0] == 0:
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Information)
                msgBox.setText("Thank You! \nYour Ordered has been placed Successfully")
                msgBox.setWindowTitle("Success")
                msgBox.setStandardButtons(QMessageBox.Ok)
                msgBox.exec_() 
            else:
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Information)
                msgBox.setText("Sorry! \nYour Ordered has been Failed")
                msgBox.setWindowTitle("Failure")
                msgBox.setStandardButtons(QMessageBox.Ok)
                msgBox.exec_() 

            self.ui.close()

        except sqlite3.Error as e:
            # Handle the exception
            print('An error occurred:', e)

        finally:
            # Close the connection
            cursor.close()
            conn.close()
        
        
        
    def show_dialog(self):
        """
        Show this dialog.
        """
        self.ui.show()

    def mYCarthideButton(self):
        self.ui.labelExistingCustomer.hide()
        self.ui.pushBtnExistingYes.hide()
        self.ui.pushBtnExistingNo.hide()
        
    def mYCartshowButton(self):
        self.ui.pushBtnBuyNow.show()