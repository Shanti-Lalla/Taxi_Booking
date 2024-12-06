# This code creates a database and tables for a taxi booking system

# Import the sqlite3 library to work with SQLite databases
import sqlite3

def create_database():
    # Create a connection to the database (or create it if it doesn't exist)
    conn = sqlite3.connect('taxi_booking.db')
    
    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()
    
    # Create the ADMIN table with columns for admin information
    # The triple quotes ''' allow us to write SQL across multiple lines
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ADMIN (
            adminID INTEGER PRIMARY KEY AUTOINCREMENT, 
            fname TEXT NOT NULL,                      
            lname TEXT NOT NULL,                       
            phone TEXT NOT NULL UNIQUE,                
            email TEXT NOT NULL UNIQUE,                
            password TEXT NOT NULL                    
        )
    ''')
    
    # Create the CUSTOMER table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS CUSTOMER (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            phone_number TEXT NOT NULL UNIQUE,
            email_address TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            payment_method TEXT NOT NULL,
            credit_card_number TEXT NOT NULL
        )
    ''')
    
    # Create the DRIVER table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS DRIVER (
            driver_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            phone_number TEXT NOT NULL UNIQUE,
            email_address TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    
    # Create the BOOKING_DETAILS table that references CUSTOMER and DRIVER tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS BOOKING_DETAILS (
            booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
            pickup_address TEXT NOT NULL,
            dropoff_address TEXT NOT NULL,
            pickup_date TEXT NOT NULL,
            pickup_time TEXT NOT NULL,
            dropoff_time TEXT NOT NULL,
            customer_id INTEGER,
            driver_id INTEGER,
            FOREIGN KEY (customer_id) REFERENCES CUSTOMER (customer_id),
            FOREIGN KEY (driver_id) REFERENCES DRIVER (driver_id)
        )
    ''')
    
    # Save (commit) the changes and close the connection
    conn.commit()
    conn.close()

# Call the function to create the database and tables
create_database()





import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QStackedWidget, QMessageBox, QComboBox
from PyQt6.QtCore import Qt
import sqlite3
import hashlib

class LoginWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Create widgets
        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.login_button = QPushButton("Login")
        self.signup_button = QPushButton("Sign Up")
        
        # Add widgets to layout
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.signup_button)
        
        # Connect signals
        self.login_button.clicked.connect(self.handle_login)
        self.signup_button.clicked.connect(self.show_signup_dialog)
        
        self.setLayout(layout)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        # Hash the password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        # Check credentials in database
        conn = sqlite3.connect('taxi_booking.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT user_type FROM users 
            WHERE username = ? AND password = ?
        ''', (username, hashed_password))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            user_type = result[0]
            self.parent().show_main_window(user_type)
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password")

    def show_signup_dialog(self):
        self.signup_dialog = SignupDialog(self)
        self.signup_dialog.show()

class SignupDialog(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sign Up")
        self.setGeometry(200, 200, 400, 300)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Create widgets
        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_password_label = QLabel("Confirm Password:")
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.name_label = QLabel("Full Name:")
        self.name_input = QLineEdit()
        self.email_label = QLabel("Email:")
        self.email_input = QLineEdit()
        self.phone_label = QLabel("Phone:")
        self.phone_input = QLineEdit()
        self.user_type_label = QLabel("Account Type:")
        self.user_type_combo = QComboBox()
        self.user_type_combo.addItems(['user', 'driver'])
        self.signup_button = QPushButton("Create Account")
        
        # Add widgets to layout
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.confirm_password_label)
        layout.addWidget(self.confirm_password_input)
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)
        layout.addWidget(self.phone_label)
        layout.addWidget(self.phone_input)
        layout.addWidget(self.user_type_label)
        layout.addWidget(self.user_type_combo)
        layout.addWidget(self.signup_button)
        
        # Connect signals
        self.signup_button.clicked.connect(self.handle_signup)
        
        self.setLayout(layout)

    def handle_signup(self):
        username = self.username_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()
        name = self.name_input.text()
        email = self.email_input.text()
        phone = self.phone_input.text()
        user_type = self.user_type_combo.currentText()
        
        # Validate inputs
        if not all([username, password, confirm_password, name, email, phone]):
            QMessageBox.warning(self, "Error", "All fields are required!")
            return
        
        if password != confirm_password:
            QMessageBox.warning(self, "Error", "Passwords do not match!")
            return
        
        # Hash the password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        # Try to create the account
        conn = sqlite3.connect('taxi_booking.db')
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO users (username, password, user_type, name, email, phone)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (username, hashed_password, user_type, name, email, phone))
            
            conn.commit()
            QMessageBox.information(self, "Success", "Account created successfully!")
            self.close()
            
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Error", "Username already exists!")
        finally:
            conn.close()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Taxi Booking System")
        self.setGeometry(100, 100, 800, 600)
        
        # Create stacked widget to manage different pages
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Create and add login page
        self.login_page = LoginWindow(self)
        self.stacked_widget.addWidget(self.login_page)
        
        # Initialize database
        self.init_database()

    def init_database(self):
        conn = sqlite3.connect('taxi_booking.db')
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                user_type TEXT NOT NULL,
                name TEXT,
                email TEXT,
                phone TEXT
            )
        ''')
        
        # Create bookings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                driver_id INTEGER,
                pickup_location TEXT,
                dropoff_location TEXT,
                booking_time DATETIME,
                status TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (driver_id) REFERENCES users (id)
            )
        ''')
        
        # Insert default admin user if not exists
        admin_password = hashlib.sha256("admin123".encode()).hexdigest()
        cursor.execute('''
            INSERT OR IGNORE INTO users (username, password, user_type, name)
            VALUES (?, ?, ?, ?)
        ''', ('admin', admin_password, 'admin', 'System Administrator'))
        
        conn.commit()
        conn.close()

    def show_main_window(self, user_type):
        # Here we'll implement the logic to show different windows based on user type
        if user_type == 'admin':
            # Show admin window
            pass
        elif user_type == 'driver':
            # Show driver window
            pass
        elif user_type == 'user':
            # Show user window
            pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
