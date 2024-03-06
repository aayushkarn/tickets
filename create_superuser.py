import sqlite3
from main.Authentication.utils import hashPassword
from datetime import datetime

# Connect to the SQLite database
connection = sqlite3.connect("instance/db.sqlite3")

# Create a cursor object
cursor = connection.cursor()

# Insert data into the database
password = hashPassword('admin')
now = datetime.now()

cursor.execute("INSERT INTO users (name, username, email, password, is_superuser, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)", ('Admin', 'admin', 'admin@a.com', password, True, now, now))
# Commit the changes and close the connection
connection.commit()
connection.close()