from PyQt5 import uic
from PyQt5.QtGui import QWindow
from category import category
from DATA225utils import make_connection


class AppWindow(QWindow):
    """
    The main application window.
    """
    
    def __init__(self):
        """
        Load the UI and initialize its components.
        """
        super().__init__()
        
        self.ui = uic.loadUi('AppWindow.ui')
        self.ui.show();
        #self.ui.centerOnScreen()
 
        self.categoryName = ""
        
        self.ui.furniture_button.clicked.connect(self.show_furniture_dialog)
        self.ui.technology_button.clicked.connect(self.show_technology_dialog)
        self.ui.office_button.clicked.connect(self.show_office_dialog)
        self.ui.everything_button.clicked.connect(self.show_all_dialog)
        self.remove_temp_data()
        
    
    def show_furniture_dialog(self):
        """
        Show the furnitur dialog.
        """
        self.categoryName = "Furniture"
        self.furniture_dialog = category(self)
        self.furniture_dialog.show_dialog()
        
        
    def show_technology_dialog(self):
        """
        Show the student dialog.
        """
        self.categoryName = "Technology"
        self.technology_dialog = category(self)
        self.technology_dialog.show_dialog()
        
        
  
    def show_office_dialog(self):      
        """
        Show the student dialog.
        """
        self.categoryName = "Office Supplies"
        self.office_dialog = category(self)
        self.office_dialog.show_dialog()
        
    
    def show_all_dialog(self):
        """
        Show the student dialog.
        """
        self.categoryName = "All"
        self.all_dialog = category(self)
        self.all_dialog.show_dialog()
        
    def get_category(self):
        return self.categoryName
    
    
    def show_dialog(self):
        """
        Show this dialog.
        """
        self.ui.show()
        
        
    def remove_temp_data(self):
        
        conn = make_connection(config_file = 'config_files/db_superstore.ini')
        
        try:
            # Create a cursor object
            cursor = conn.cursor()
            
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
           
        except sqlite3.Error as e:
            # Handle the exception
            print('An error occurred:', e)

        finally:
            # Close the connection
            cursor.close()
            conn.close()
    
#     def centerOnScreen(self):
#         # Get the size of the screen
#         screen = QtWidgets.QDesktopWidget().screenGeometry()
        
#         # Get the size of the window
#         size = self.geometry()
        
#         # Calculate the center position of the window
#         x = (screen.width() - size.width()) / 2
#         y = (screen.height() - size.height()) / 2
        
#         # Set the window position
#         self.move(x, y)







   