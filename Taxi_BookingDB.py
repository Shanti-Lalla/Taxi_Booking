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





