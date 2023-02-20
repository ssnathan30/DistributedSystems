import sqlite3
import json
import pathlib

# path to parent and src directory
parent_dir = pathlib.Path(__file__).parent.resolve()
src_dir = pathlib.Path(__file__).parent.parent.resolve()

# Connect to the database
conn = sqlite3.connect('{0}/db/customer.db'.format(parent_dir))
cursor = conn.cursor()

# Create tables
# Table Seller
cursor.execute('''
CREATE TABLE Seller (
    id INT PRIMARY KEY,
    seller_name VARCHAR(32),
    feedback_thumbs_up INT DEFAULT 0,
    feedback_thumbs_down INT DEFAULT 0,
    number_of_items_sold INT
);''')

# Table Seller_Login
cursor.execute('''
CREATE TABLE Seller_Login (
    seller_id INT,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    is_active BOOLEAN DEFAULT 0,
    FOREIGN KEY (seller_id) REFERENCES Seller(id)
);''')

# Table Buyer
cursor.execute('''
CREATE TABLE Buyer (
    id INT PRIMARY KEY,
    buyer_name VARCHAR(32),
    number_of_items_purchased INT
);
''')

# Table Buyer_Login
cursor.execute('''
CREATE TABLE Buyer_Login (
    buyer_id INT,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    is_active BOOLEAN DEFAULT 0,
    FOREIGN KEY (buyer_id) REFERENCES Buyer(id)
);''')


cursor.execute("INSERT INTO Seller VALUES (1, 'seller1', 3, 2, 10)")
cursor.execute("INSERT INTO Seller VALUES (2, 'seller2', 3, 2, 10)")
cursor.execute("INSERT INTO Seller VALUES (3, 'seller3', 3, 2, 10)")

# Commit the changes
conn.commit()

# Retrieve data
cursor.execute("SELECT * FROM Buyer_Login")
items = cursor.fetchall()
column_names = [description[0] for description in cursor.description]
# Create a list of dictionaries with the column names as keys
results = [dict(zip(column_names, row)) for row in items]
# Print the results as JSON
print(json.dumps(results, indent=4))

# Close the connection
conn.close()
