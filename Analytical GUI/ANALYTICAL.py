from PyQt5 import uic
from PyQt5.QtGui import QWindow
from DATA225utils import make_connection
#from TechnologyDialog import TechnologyDialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvas 

from furniture import furniture
from technology import technology
from officesupply import officesupply
class ANALYTICAL(QWindow):
    """
    The main application window.
    """
    
    def __init__(self):
        """
        Load the UI and initialize its components.
        """
        super().__init__()
        
        self.ui = uic.loadUi('analytical.ui')
        self.ui.show();
        self.unitsold = 0
        self.sales = 0
        self.fsales = 0
        self.tsales = 0
        self.osales = 0
        self.funits = 0
        self.tunits = 0
        self.ounits = 0
        self.unitsolds = 0
        self.sales1 = 0
        self._update()
        
        self.ui.sales.setText(f"{self.sales1:.2f} M")
        self.ui.fsales.setValue(self.fsales)
        self.ui.tsales.setValue(self.tsales)
        self.ui.osales.setValue(self.osales)
        self.ui.unitssold.setText(f"{self.unitsolds:.2f} K")
        self.ui.funits.setValue(self.funits)
        self.ui.tunits.setValue(self.tunits)
        self.ui.ounits.setValue(self.ounits)
        self._update_graph()
        self._update_graph2()
        
        # Next Button dialog.
        self._furniture_dialog = furniture()
        self.ui.furniturebutton.clicked.connect(self._show__furniture_dialog)
        
        self._technology_dialog = technology()
        self.ui.technologybutton.clicked.connect(self._show__technology_dialog)
        
        self._officesupply_dialog = officesupply()
        self.ui.officesupplybutton.clicked.connect(self._show__officesupply_dialog)
    
    def _show__furniture_dialog(self):
        """
        Show the furniture dialog.
        """
        self._furniture_dialog.show_dialog()
        
    def _show__technology_dialog(self):
        
        """
         Show the technology dialog.
        """
        self._technology_dialog.show_dialog()
             
    def _show__officesupply_dialog(self):
        
        """
         Show the officesupply dialog.
        """
        self._officesupply_dialog.show_dialog()
             

            
            
    def _update(self):
        
        conn = make_connection(config_file = 'config_files/wh_superstore.ini')
        cursor = conn.cursor()

        sql = ("""
        SELECT year, COUNT(order_id) AS order_count, SUM(sales) as sale, SUM(units_sold) as units_sold
        FROM sales_fact sf JOIN calendar_dim cd ON cd.calendarkey = sf.calendarkey
        GROUP BY year
        ORDER BY year;
        """)

        cursor.execute(sql)
        rows = cursor.fetchall()

        self.sales = (rows[0][2])
        self.unitsold = (rows[0][3])
        
        self.sales1 = float(self.sales / 1000000)
        self.unitsolds = float(self.unitsold / 1000)
        

        sql = ("""
        SELECT category_name, COUNT(order_id) AS order_count, SUM(sales) as sale, SUM(units_sold) as units_sold
         FROM sales_fact sf JOIN product_dim pd ON pd.productkey = sf.productkey
         GROUP BY category_name
         ORDER BY category_name;
        """)

        cursor.execute(sql)
        rows = cursor.fetchall()

        by_category_sales = []
        by_category_unitssold = []
        for row in rows:
            by_category_sales.append(row[2])
            by_category_unitssold.append(row[3])
        
        self.fsales = (by_category_sales[0] / self.sales ) * 100
        self.tsales = (by_category_sales[2] / self.sales ) * 100
        self.osales = (by_category_sales[1] / self.sales ) * 100
    
        self.funits = (by_category_unitssold[0] / self.unitsold) * 100
        self.tunits = (by_category_unitssold[2] / self.unitsold) * 100
        self.ounits = (by_category_unitssold[1] / self.unitsold) * 100
        
        #print(self.sales, self.unitsold, self.fsales, self.tsales, self.osales, self.funits, self.tunits, self.ounits)
        
        cursor.close()
        conn.close()
    def _initialize_graph(self):
        """
        Remove all the plots from the graph.
        """
        children = []
        
        # Gather children which are the plots in the layout.
        for i in range(self.ui.graph_layout_3.count()):
            child = self.ui.graph_layout_3.itemAt(i).widget()
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
        self.ui.graph_layout_3.addWidget(FigureCanvas(plt.figure()))
        
        conn = make_connection(config_file = 'config_files/wh_superstore.ini')
        cursor = conn.cursor()

        sql = ("""
        SELECT month_name 
        FROM calendar_dim 
        GROUP BY month_name;
        """)

        cursor.execute(sql)
        rows = cursor.fetchall()

        x = []
        for row in rows:
            x.append(row[0][:3])

        sql = ("""
        SELECT month_name, SUM(sales) as sale
        FROM sales_fact sf JOIN calendar_dim cd ON cd.calendarkey = sf.calendarkey
        GROUP BY month_name
        ORDER BY month_name;
            """
            )

        cursor.execute(sql)
        rows = cursor.fetchall()

        y = []
        for row in rows:
            y.append(row[1])

        cursor.close()
        conn.close()

        plt.plot(x, y)  

        title = ("Sales Per Month")

        plt.title(title)
        plt.xlabel('Month')
        plt.ylabel('Sales')
        plt.legend()

        plt.ylim(0) 

        #plt.show()
    def _initialize_graph2(self):
        """
        Remove all the plots from the graph.
        """
        children = []
        
        # Gather children which are the plots in the layout.
        for i in range(self.ui.graph_layout_2.count()):
            child = self.ui.graph_layout_2.itemAt(i).widget()
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
        
        # Add the figure to the UI.
        self.ui.graph_layout_2.addWidget(FigureCanvas(plt.figure()))
        
        conn = make_connection(config_file = 'config_files/wh_superstore.ini')
        cursor = conn.cursor()

        sql = ("""
        SELECT month_name 
        FROM calendar_dim 
        GROUP BY month_name;
        """)

        cursor.execute(sql)
        rows = cursor.fetchall()

        x = []
        for row in rows:
            x.append(row[0][:3])

        sql = ("""
        SELECT month_name, SUM(sales) as sale
        FROM sales_fact sf JOIN product_dim pd ON pd.productkey = sf.productkey JOIN calendar_dim cd ON cd.calendarkey = sf.calendarkey
        WHERE category_name = 'Furniture'
        GROUP BY month_name
        ORDER BY month_name;
            """
            )

        cursor.execute(sql)
        rows = cursor.fetchall()

        y1 = []
        for row in rows:
            y1.append(row[1])

        sql = ("""
        SELECT month_name, SUM(sales) as sale
        FROM sales_fact sf JOIN product_dim pd ON pd.productkey = sf.productkey JOIN calendar_dim cd ON cd.calendarkey = sf.calendarkey
        WHERE category_name = 'Technology'
        GROUP BY month_name
        ORDER BY month_name;
            """
            )

        cursor.execute(sql)
        rows = cursor.fetchall()

        y2 = []
        for row in rows:
            y2.append(row[1])


        sql = ("""
        SELECT month_name, SUM(sales) as sale
        FROM sales_fact sf JOIN product_dim pd ON pd.productkey = sf.productkey JOIN calendar_dim cd ON cd.calendarkey = sf.calendarkey
        WHERE category_name = 'Office Supplies'
        GROUP BY month_name
        ORDER BY month_name;
            """
            )

        cursor.execute(sql)
        rows = cursor.fetchall()

        y3 = []
        for row in rows:
            y3.append(row[1])


        cursor.close()
        conn.close()

        plt.plot(x, y1, label = 'Furniture')
        plt.plot(x, y2, label = 'Technology')
        plt.plot(x, y3, label = 'Office Supplies')

        title = ("Sales Per Month By product category")

        plt.title(title)
        plt.xlabel('Month')
        plt.ylabel('Sales')
        plt.legend()

        plt.ylim(0) 
        plt.close()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = ANALYTICAL()
    sys.exit(app.exec_())