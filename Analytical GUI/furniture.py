import sys
import random
import numpy as np
from PyQt5 import uic, QtWidgets
from PyQt5.QtGui import QWindow
from PyQt5.QtWidgets import QApplication, QHeaderView, \
                            QTableWidget, QTableWidgetItem
from PyQt5 import uic
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidgetItem, QHeaderView, QApplication, QMainWindow, QListWidget, QWidget, QVBoxLayout,QHBoxLayout, QLabel, QPushButton, QListWidgetItem, QTableWidget
from DATA225utils import make_connection
from PyQt5.QtCore import Qt 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvas


class furniture(QDialog):
    '''
    The furniture dialog
    '''
    
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('furniture.ui')
        
        
        
        
        self._initialize_state_menu()
        self.ui.applybutton.clicked.connect(self._update_graph)
        self.ui.applybutton.clicked.connect(self._update_graph1)
        self.ui.applybutton.clicked.connect(self._update_graph2)
        self.ui.applybutton.clicked.connect(self._update_graph3)
        self._update_graph()
        self._update_graph1()
        self._update_graph2()
        self._update_graph3()
        
    
    def show_dialog(self):
        """
        Show this dialog.
        """
        self.ui.show()
        
   
    
    def _initialize_graph(self):
        """
        Remove all the plots from the graph.
        """
        children = []

        # Gather children which are the plots in the layout.
        for i in range(self.ui.layout1.count()):
            child = self.ui.layout1.itemAt(i).widget()
            if child:
                children.append(child)

        # Delete the plots.
        for child in children:
            child.deleteLater()
            
    def _update_graph(self):
        """
        Plot the closing prices and the
        exponentially smoothed prices.
        """        
        self._initialize_graph()
        
        # Add the figure to the UI.
        self.ui.layout1.addWidget(FigureCanvas(plt.figure()))
        state = self.ui.state_menu.currentData()[0]
        conn = make_connection(config_file = 'config_files/wh_superstore.ini')
        cursor = conn.cursor()

        sql = (f"""
                select product_dim.product_name, SUM(sales) AS sales
                from sales_fact, product_dim, customer_dim
                WHERE customer_dim.state = '{state}'
                and product_dim.productkey = sales_fact.productkey
                and category_name = "Furniture"
                and customer_dim.customerkey = sales_fact.customerkey
                GROUP by product_dim.productkey
                order by sales DESC
                limit 5
        """)

        cursor.execute(sql)
        rows = cursor.fetchall()

        x = []
        y = []
        for row in rows:
            x.append(row[0])
            y.append(row[1])

        cursor.close()
        conn.close()

        
        plt.pie(y, autopct='%1.1f%%')
        plt.legend(x, loc = 'lower center')

        title = ("Top products")

        plt.title(title)
#-----------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------
    def _initialize_graph1(self):
        """
        Remove all the plots from the graph.
        """
        children = []

        # Gather children which are the plots in the layout.
        for i in range(self.ui.layout2.count()):
            child = self.ui.layout2.itemAt(i).widget()
            if child:
                children.append(child)

        # Delete the plots.
        for child in children:
            child.deleteLater()
            
    def _initialize_state_menu(self):
        """
        Initialize the player menu with player names from the database.
        """
        conn = make_connection(config_file = 'config_files/wh_superstore.ini')
        cursor = conn.cursor()
        
        sql = """
            select distinct customer_dim.state
            from customer_dim
            order by customer_dim.state
                
            """
        
        cursor.execute(sql)
        rows = cursor.fetchall()
        
        for row in rows:
            name = row[0]
            self.ui.state_menu.addItem(name, row)  
       
        
        cursor.close()
        conn.close()
        
       
        
    def _update_graph1(self):
        """
        Plot the closing prices and the
        exponentially smoothed prices.
        """    
        #self.ui.layout2.clear()
        self._initialize_graph1()
        
        # Add the figure to the UI.
        self.ui.layout2.addWidget(FigureCanvas(plt.figure()))
        
        state = self.ui.state_menu.currentData()[0]
        
        conn = make_connection(config_file = 'config_files/wh_superstore.ini')
        cursor = conn.cursor()

        sql = (f"""
        select customer_dim.city, Sum(sales) as Sales 
        from sales_fact,  customer_dim, product_dim
        WHERE customer_dim.state = '{state}' 
        and customer_dim.customerkey = sales_fact.customerkey
        and product_dim.productkey = sales_fact.productkey
            and category_name = "Furniture"
        group by customer_dim.city
        order by sales DESC

        """)
        

        cursor.execute(sql)
        rows = cursor.fetchall()

        x = []
        y = []
        
        for row in rows:
            x.append(row[0])
            y.append(row[1])
    
        cursor.close()
        conn.close()
        if len(x) > 10:
            x = x[:9]
            y = y[0:9]
        #print(y)
        plt.bar(x, y, color = 'brown')  

        title = ("Sales per city")

        plt.title(title)
        plt.xlabel('City')
        plt.ylabel('Sales')
        plt.legend()

        plt.ylim(0)  
        
#-------------------------------------------------------------------------------------------------    
    def _initialize_graph2(self):
        """
        Remove all the plots from the graph.
        """
        children = []

        # Gather children which are the plots in the layout.
        for i in range(self.ui.layout3.count()):
            child = self.ui.layout3.itemAt(i).widget()
            if child:
                children.append(child)

        # Delete the plots.
        for child in children:
            child.deleteLater()
            
    def _update_graph2(self):
        """
        Plot the closing prices and the
        exponentially smoothed prices.
        """        
        self._initialize_graph2()
        state = self.ui.state_menu.currentData()[0]
        # Add the figure to the UI.
        self.ui.layout3.addWidget(FigureCanvas(plt.figure()))
        
        conn = make_connection(config_file = 'config_files/wh_superstore.ini')
        cursor = conn.cursor()

        sql = (f"""
        select calendar_dim.month_name , sum(sales) as Sales 
        from sales_fact, product_dim, calendar_dim, customer_dim
        WHERE customer_dim.state = '{state}' 
        and product_dim.productkey = sales_fact.productkey
        and calendar_dim.calendarkey = sales_fact.calendarkey
        and customer_dim.customerkey = sales_fact.customerkey
        and category_name = "Furniture"
        group by calendar_dim.month_name
        order by Sales DESC
        
        """)

        cursor.execute(sql)
        rows = cursor.fetchall()

        x = []
        y= []
        for row in rows:
            x.append(row[0][:3])
            y.append(row[1])

        cursor.close()
        conn.close()

        plt.bar(x, y)  

        title = ("Monthwise sales")

        plt.title(title)
        plt.xlabel('Months')
        plt.ylabel('Sales')
        plt.legend()

        plt.ylim(0)   
# ----------------------------------------------------------------------------------------------

    def _initialize_graph3(self):
        """
        Remove all the plots from the graph.
        """
        children = []

        # Gather children which are the plots in the layout.
        for i in range(self.ui.layout4.count()):
            child = self.ui.layout4.itemAt(i).widget()
            if child:
                children.append(child)

        # Delete the plots.
        for child in children:
            child.deleteLater()

    def _update_graph3(self):
        """
        Plot the closing prices and the
        exponentially smoothed prices.
        """        
        self._initialize_graph3()
        state = self.ui.state_menu.currentData()[0]
        # Add the figure to the UI.
        self.ui.layout4.addWidget(FigureCanvas(plt.figure()))
        
        conn = make_connection(config_file = 'config_files/wh_superstore.ini')
        cursor = conn.cursor()

        sql = (f"""
         select sales_fact.websitekey, Sum(sales) as Sales
        from (select sf.*
        from sales_fact sf JOIN product_dim pd ON sf.productkey = pd.productkey
        where category_name = "Furniture") as sales_fact JOIN customer_dim cd ON sales_fact.customerkey = cd.customerkey
        WHERE cd.state = '{state}'
        group by sales_fact.websitekey
        order by Sales DESC;

        """)

        cursor.execute(sql)
        rows = cursor.fetchall()
        
        x = []
        y= []
        for row in rows:
            x.append(row[0]) 
            y.append(row[1])
        

        for i in range(len(x)):
            if x[i] == 1:
                x[i] = "Amazon"
            elif x[i] == 2:
                x[i] = "Costco"            
            elif x[i] == 3:
                x[i] = "Ikea"            
            elif x[i] == 4:
                x[i] = "Target"           
            elif x[i] == 5:
                x[i] = "Walmart"
                
       
        cursor.close()
        conn.close()
        plt.plot(x,y, color = "darkgreen")

        title = (" Top Websites selling Furniture ")

        plt.title(title)
        plt.xlabel('Websites')
        plt.ylabel('Sales')
        plt.legend()
        plt.close()
#         plt.ylim(0) 