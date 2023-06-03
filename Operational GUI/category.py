import sys
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidgetItem, QHeaderView, QApplication, QMainWindow, QListWidget, QWidget, QVBoxLayout,QHBoxLayout, QLabel, QPushButton, QListWidgetItem, QTableWidget, QMessageBox
from DATA225utils import make_connection
from PyQt5.QtCore import Qt 
from MyCart import MyCart
from SignInOrder import SignInOrder

class category(QDialog):
    '''
    The Category dialog
    '''
    
    def __init__(self,AppWindowData):
        """
        Load the UI and initialize its components.
        """
        super().__init__()
        
        self.AppWindowData = AppWindowData
        
        self.checklist = []
        self.website_names = ["Amazon","Costco","Ikea","Target","Walmart"]
        self.minimum = 0
        self.maximum = 3000
        self.category_names = self.AppWindowData.get_category()
        #self.ui.comboBoxCategory.setCurrentText(str(self.category_names))
        self.searchKeyword = ""  
        self.productIdList = []
        self.productOrderedCount = 0
        
        self.ui = uic.loadUi('newCategory.ui')
        self.setButton()
        
        
        
        
        # Radio handles
        self.ui.radioAll.toggled.connect(self.handle_radio) 
        self.ui.radio0_25.toggled.connect(self.handle_radio) 
        self.ui.radio25_100.toggled.connect(self.handle_radio) 
        self.ui.radio100_500.toggled.connect(self.handle_radio) 
        self.ui.radio500_1000.toggled.connect(self.handle_radio) 
        self.ui.radio1000.toggled.connect(self.handle_radio)
        
        
        # Check Box Handles 
        self.ui.checkAmazon.stateChanged.connect(self.handle_checkbox)
        self.ui.checkCostco.stateChanged.connect(self.handle_checkbox)
        self.ui.checkIkea.stateChanged.connect(self.handle_checkbox)
        self.ui.checkTarget.stateChanged.connect(self.handle_checkbox)
        self.ui.checkWalmart.stateChanged.connect(self.handle_checkbox)


        # Initialize of different data
        self._initialize_category_menu()
        self._initialize_table()
        self._enter_product_data()
        
        # PushButton Handles
        self.ui.pushBtnMyCart.clicked.connect(self.my_cart)
        self.ui.pushBtnApplyFilter.clicked.connect(self._apply_filter)
        self.ui.pushBtnSearch.clicked.connect(self.search_product_data)
        self.ui.pushBtnMyOrder.clicked.connect(self.showMyOrders)
        
        # Combobox Handle
        self.ui.comboBoxCategory.currentIndexChanged.connect(self.handle_dropdown)
        
                       
    def show_dialog(self):
        """
        Show this dialog.
        """
        self.ui.show()
    
    def setButton(self):
        conn = make_connection(config_file = 'config_files/db_superstore.ini')
        cursor = conn.cursor()
        
        sql = "SELECT COUNT(*) FROM temp_cart"
        
        cursor.execute(sql)
        row_count = cursor.fetchone()[0]
        
        if row_count > 0:
            self.ui.pushBtnMyCart.setEnabled(True)
        else:
            self.ui.pushBtnMyCart.setEnabled(False)

        cursor.close()
        conn.close()
        
            
    def _adjust_column_widths(self):
        """
        Adjust the column widths of the product table to fit the contents.
        """
        header = self.ui.tableWidgetProduct.horizontalHeader();
        #header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        #header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.Stretch)
        
        
    def _initialize_table(self):
        """
        Clear the table and set the column headers.
        """
        self.ui.tableWidgetProduct.clear()
        
        headers = ["Product Name", "Category", "Product Price", "Website Name", "Quantity", "Action"]
        self.ui.tableWidgetProduct.setHorizontalHeaderLabels(headers)    
        
        self._adjust_column_widths()
        
        
    def _apply_filter(self):
#         if len(self.checklist) == 0:
#             self._enter_product_data()
            
#         else:
         self.update_product_data()
            
        
    
    def _initialize_category_menu(self):
        conn = make_connection(config_file = 'config_files/db_superstore.ini')
        cursor = conn.cursor()
        
        sql = "SELECT category_name FROM category"
        
        cursor.execute(sql)
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        for row in rows:
            name = row[0]
            self.ui.comboBoxCategory.addItem(name, row)
            
            
    def handle_dropdown(self):
        self.category_names = self.ui.comboBoxCategory.currentText()
      
        self.update_product_data()
        
        
    def handle_radio(self):
        if self.ui.radioAll.isChecked():
            self.minimum = 0
            self.maximum = 3000
        elif self.ui.radio0_25.isChecked():
            self.minimum = 0
            self.maximum = 25
        elif self.ui.radio25_100.isChecked():
            self.minimum = 25
            self.maximum = 100
        elif self.ui.radio100_500.isChecked():
            self.minimum = 100
            self.maximum = 500
        elif self.ui.radio500_1000.isChecked():
            self.minimum = 500
            self.maximum = 1000
        elif self.ui.radio1000.isChecked():
            self.minimum = 1000
            self.maximum = 3000
    
        #self._enter_product_data()
        
    def handle_checkbox(self, state):
        sender = self.sender()
        checkbox_name = sender.objectName().replace("check", "")
        if state == Qt.Checked:
            self.checklist.append(checkbox_name)
        else:
            self.checklist.remove(checkbox_name)

        #self._enter_product_data()
        
        
    def _enter_product_data(self):    
        """
        Enter product data from the query into 
        the product and takes tables.
        """    
        self.ui.tableWidgetProduct.clearContents()
                    
        website_name = tuple(self.website_names)

        conn = make_connection(config_file = 'config_files/db_superstore.ini')
        cursor = conn.cursor()
        
        if self.category_names == "All":
            sql = ( f"""
            SELECT p.product_name, c.category_name, l.price, l.website_name, p.quantity_available, '', p.product_id
            FROM listed l, product p, category c 
            WHERE l.product_id = p.product_id 
            AND p.category_id = c.category_id 
            AND p.product_name LIKE '%{self.searchKeyword}%'
            AND l.price > {self.minimum} 
            AND l.price < {self.maximum}
            AND website_name IN {website_name}
           """
              )   
        else:
            sql = ( f"""
            SELECT p.product_name, c.category_name, l.price, l.website_name, p.quantity_available, '', p.product_id
            FROM listed l, product p, category c 
            WHERE l.product_id = p.product_id 
            AND p.category_id = c.category_id 
            AND c.category_name = '{self.category_names}'
            AND p.product_name LIKE '%{self.searchKeyword}%'
            AND l.price > {self.minimum} 
            AND l.price < {self.maximum}
            AND website_name IN {website_name}
           """
          )   

        cursor.execute(sql)
        rows = cursor.fetchall()
        
        self.productIdList = rows

        cursor.close()
        conn.close()

        self.ui.tableWidgetProduct.setRowCount(10)
        records = []
        row_index = 0
        for row in rows:
            column_index = 0
            record = []
            for data in row:
                record.append(data)
                column_index += 1
            records.append(record)

        self.ui.tableWidgetProduct.setRowCount(len(records))

        for row in range(len(records)):
            for col in range(0,len(records[row])-1):
                item = QTableWidgetItem(str(records[row][col]))
                self.ui.tableWidgetProduct.setItem(row, col, item)

                #Add a button to the last column of each row
                add_button = QPushButton("Add to Cart")
                add_button.setStyleSheet("""
                QPushButton {
                    border-radius: 2px;
                    padding: 5px;
                    background-color: #009688;
                    color: white;
                }

                QPushButton:hover {
                    background-color: #008080;
                }

                QPushButton:pressed {
                    background-color: #006666;
                }""")

                add_button.clicked.connect(lambda _, row=row: self.add_to_cart(row))


            layout = QHBoxLayout()
            layout.addWidget(add_button)
            layout.setAlignment(add_button, QtCore.Qt.AlignCenter)
            widget = QWidget()
            widget.setLayout(layout)
            self.ui.tableWidgetProduct.setCellWidget(row, 5, widget)                

        self.ui.tableWidgetProduct.verticalHeader().setDefaultSectionSize(50)  


    def update_product_data(self):    
            """
            Enter product data from the query into 
            the product and takes tables.
            """    
            self.ui.tableWidgetProduct.clearContents()
            self.searchKeyword = self.ui.lineEditSearch.text()
            
            
            if len(self.checklist)==0:
                website_name = tuple(self.website_names)
            else:
                temp_tuple = tuple(self.checklist)
                websites = str(temp_tuple)

                # remove comma if it exists at the end
                if websites.endswith(',)'):
                    if len(temp_tuple)==1:
                        website_name =  "('"+ temp_tuple[0] +"')"
                    else:
                        websites = websites[:-2] + ')'
                        website_name = eval(websites)
                else:
                    website_name = tuple(self.checklist)
                
            
            conn = make_connection(config_file = 'config_files/db_superstore.ini')
            cursor = conn.cursor()
            
            
            if self.category_names == "All":
                sql = ( f"""
                    SELECT DISTINCT p.product_name, c.category_name, l.price, l.website_name, p.quantity_available, '', p.product_id
                    FROM listed l, product p, category c 
                    WHERE l.product_id = p.product_id 
                    AND p.category_id = c.category_id 
                    AND p.product_name LIKE '%{self.searchKeyword}%'
                    AND l.price > {self.minimum} 
                    AND l.price < {self.maximum}
                    AND website_name IN {website_name}
                    """
                    ) 
            else:
                sql = ( f"""
                    SELECT DISTINCT p.product_name, c.category_name, l.price, l.website_name, p.quantity_available, '', p.product_id
                    FROM listed l, product p, category c 
                    WHERE l.product_id = p.product_id 
                    AND p.category_id = c.category_id 
                    AND p.product_name LIKE '%{self.searchKeyword} %'
                    AND l.price > {self.minimum} 
                    AND l.price < {self.maximum}
                    AND c.category_name = '{self.category_names}'
                    AND website_name IN {website_name}
                    """
                    ) 

            cursor.execute(sql)
            rows = cursor.fetchall()

            cursor.close()
            conn.close()
            
            self.productIdList = rows
            
            self.ui.tableWidgetProduct.setRowCount(10)
            
            records = []
            row_index = 0
            for row in rows:
                column_index = 0
                record = []
                for data in row:
                    record.append(data)
                    column_index += 1
                records.append(record)

            self.ui.tableWidgetProduct.setRowCount(len(records))

            for row in range(len(records)):
                for col in range(len(records[row])):
                    item = QTableWidgetItem(str(records[row][col]))
                    self.ui.tableWidgetProduct.setItem(row, col, item)

                    #Add a button to the last column of each row
                    add_button = QPushButton("Add to Cart")
                    add_button.setStyleSheet("""
                    QPushButton {
                        border-radius: 2px;
                        padding: 5px;
                        background-color: #009688;
                        color: white;
                    }

                    QPushButton:hover {
                        background-color: #008080;
                    }

                    QPushButton:pressed {
                        background-color: #006666;
                    }""")

                    add_button.clicked.connect(lambda _, row=row: self.add_to_cart(row))


                layout = QHBoxLayout()
                layout.addWidget(add_button)
                layout.setAlignment(add_button, QtCore.Qt.AlignCenter)
                widget = QWidget()
                widget.setLayout(layout)
                self.ui.tableWidgetProduct.setCellWidget(row, 5, widget)                

            self.ui.tableWidgetProduct.verticalHeader().setDefaultSectionSize(50)  
            
            
    def search_product_data(self):    
            """
            Enter product data from the query into 
            the product and takes tables.
            """    
            self.ui.tableWidgetProduct.clearContents()
            
            self.searchKeyword = self.ui.lineEditSearch.text()
            
          
            if len(self.checklist)==0:
                website_name = tuple(self.website_names)
            else:
                temp_tuple = tuple(self.checklist)
                
                websites = str(temp_tuple)

                # remove comma if it exists at the end
                if websites.endswith(',)'):
                    
                    if len(temp_tuple)==1:
                        website_name =  "('"+ temp_tuple[0] +"')"
                        
                    else:
                        websites = websites[:-2] + ')'
                        website_name = eval(websites)
                else:
                    website_name = tuple(self.checklist)
            
            conn = make_connection(config_file = 'config_files/db_superstore.ini')
            cursor = conn.cursor()
    
            if self.category_names == "All":
                sql = ( f"""
                    SELECT DISTINCT p.product_name, c.category_name, l.price, l.website_name, p.quantity_available, '', p.product_id
                    FROM listed l, product p, category c 
                    WHERE l.product_id = p.product_id 
                    AND p.category_id = c.category_id 
                    AND p.product_name LIKE '%{self.searchKeyword}%'
                    AND l.price > {self.minimum} 
                    AND l.price < {self.maximum}
                    AND website_name IN {website_name}
                    """
                    ) 
            else:
                sql = ( f"""
                    SELECT DISTINCT p.product_name, c.category_name, l.price, l.website_name, p.quantity_available, '', p.product_id
                    FROM listed l, product p, category c 
                    WHERE l.product_id = p.product_id 
                    AND p.category_id = c.category_id 
                    AND p.product_name LIKE '%{self.searchKeyword}%'
                    AND l.price > {self.minimum} 
                    AND l.price < {self.maximum}
                    AND c.category_name = '{self.category_names}'
                    AND website_name IN {website_name}
                    """
                    ) 
        

            cursor.execute(sql)
            rows = cursor.fetchall()

            cursor.close()
            conn.close()
            
            self.productIdList = rows 
            
            self.ui.tableWidgetProduct.setRowCount(10)
            records = []
            row_index = 0
            for row in rows:
                column_index = 0
                record = []
                for data in row:
                    record.append(data)
                    column_index += 1
                records.append(record)

            self.ui.tableWidgetProduct.setRowCount(len(records))
            
            
            if len(records)!=0:
                self.ui.tableWidgetProduct.show()
                for row in range(len(records)):
                    for col in range(len(records[row])):
                        item = QTableWidgetItem(str(records[row][col]))
                        self.ui.tableWidgetProduct.setItem(row, col, item)

                        #Add a button to the last column of each row
                        add_button = QPushButton("Add to Cart")
                        add_button.setStyleSheet("""
                        QPushButton {
                            border-radius: 2px;
                            padding: 5px;
                            background-color: #009688;
                            color: white;
                        }

                        QPushButton:hover {
                            background-color: #008080;
                        }

                        QPushButton:pressed {
                            background-color: #006666;
                        }""")

                        add_button.clicked.connect(lambda _, row=row: self.add_to_cart(row))


                    layout = QHBoxLayout()
                    layout.addWidget(add_button)
                    
                    layout.setAlignment(add_button, QtCore.Qt.AlignCenter)
                    widget = QWidget()
                    widget.setLayout(layout)
                    self.ui.tableWidgetProduct.setCellWidget(row, 5, widget)     
                
                self.ui.tableWidgetProduct.verticalHeader().setDefaultSectionSize(50)  
                self.ui.labelSearchMessage.setText("")
                            
            else:
                self.ui.labelSearchMessage.setText("Sorry! No Products Found")
                self.ui.tableWidgetProduct.hide()
                
            

    def add_to_cart(self,index):
        
        self.ui.pushBtnMyCart.setEnabled(True)
        # Get the row and column of the button that was clicked
        button = self.sender()
        # Get the data from the table for that row
        product_name = self.ui.tableWidgetProduct.item(index, 0).text()
        category = self.ui.tableWidgetProduct.item(index, 1).text()
        price = self.ui.tableWidgetProduct.item(index, 2).text()
        website_name = self.ui.tableWidgetProduct.item(index, 3).text()
        quantity = self.ui.tableWidgetProduct.item(index, 4).text()
        productid = str(self.productIdList[index][-1])
        
        val = (productid, product_name, category, price, website_name, 1)
        
        conn = make_connection(config_file = 'config_files/db_superstore.ini')
        cursor = conn.cursor()
                
        sql_check = ( f"""
                SELECT COUNT(*) 
                from temp_cart tc 
                WHERE tc.product_id = '{productid}'
                AND tc.website_name = '{website_name}';
                """
              ) 
        
        cursor.execute(sql_check)
        count = cursor.fetchone()[0]
        
        
        if count>0:
            
            sql_query = ( f"""
                SELECT tc.quantity_ordered as quantityNumber 
                from temp_cart tc 
                WHERE tc.product_id = '{productid}'
                AND tc.website_name = '{website_name}';
                """
              ) 
        
            cursor.execute(sql_query)
            resultCheck = cursor.fetchall()
            
            for row in resultCheck:
                column_index = 0
                record = []
                for data in row:
                    record.append(data)

            self.productOrderedCount = record[0] + 1
            
            
            
            # Execute a query that might raise an exception
            cursor.execute('SET SQL_SAFE_UPDATES = 0;')

            # Update row from the table
            sql_update = f"""
                        UPDATE temp_cart tc
                        SET tc.quantity_ordered = {record[0]+1} 
                        WHERE tc.product_id = '{productid}'
                        AND tc.website_name = '{website_name}';
                      """

            cursor.execute(sql_update)

            if cursor.execute(sql_update) == None:            
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Information)
                msgBox.setText("Product Added to Cart successfully.")
                msgBox.setWindowTitle("Success")
                msgBox.setStandardButtons(QMessageBox.Ok)
                msgBox.exec_()
            else:
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Information)
                msgBox.setText("Sorry! There is some Internal Error.")
                msgBox.setWindowTitle("Success")
                msgBox.setStandardButtons(QMessageBox.Cancel)
                msgBox.exec_()
                
            # Re-enable safe mode
            cursor.execute('SET SQL_SAFE_UPDATES = 1;')
            conn.commit()
            
            
        else:
            sql_insert = ( """
             INSERT INTO temp_cart 
             VALUES (%s, %s, %s, %s, %s, %s);"""
            )
            cursor.execute(sql_insert, val)
            conn.commit()
            if cursor.rowcount > 0:            
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Information)
                msgBox.setText("Product Added to Cart successfully.")
                msgBox.setWindowTitle("Success")
                msgBox.setStandardButtons(QMessageBox.Ok)
                msgBox.exec_()
            else:
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Information)
                msgBox.setText("Sorry! There is some Internal Error.")
                msgBox.setWindowTitle("Success")
                msgBox.setStandardButtons(QMessageBox.Cancel)
                msgBox.exec_()
         
        #conn.commit()
        cursor.close()
        conn.close()

        
    def my_cart(self):

        """
        Show the My Cart dialog.
        """
        if self.ui.pushBtnMyCart.isEnabled():
            self._mycart_dialog = MyCart()
            self._mycart_dialog.show_dialog()
        else:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Sorry! Your Cart is Empty.\Please Add prdoducts to the cart")
            msgBox.setWindowTitle("Message")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec_()
            
        
        
        
    def showMyOrders(self):
        self.signinorder_customer_dialog = SignInOrder()
        self.signinorder_customer_dialog.show_dialog()
        
       
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = category()
    form.show_dialog()
    sys.exit(app.exec_())        