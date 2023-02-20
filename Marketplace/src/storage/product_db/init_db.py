import sqlite3
import json
import pathlib

# path to parent and src directory
parent_dir = pathlib.Path(__file__).parent.resolve()
src_dir = pathlib.Path(__file__).parent.parent.resolve()

# Connect to the database
conn = sqlite3.connect('{0}/db/product.db'.format(parent_dir))
conn.execute('pragma journal_mode=wal;')
cursor = conn.cursor()

# Create tables
# Table Item
cursor.execute('''
CREATE TABLE Item (
    id INT PRIMARY KEY,
    item_name VARCHAR(32),
    item_category INT,
    keywords VARCHAR(50),
    condition VARCHAR(3),
    sale_price DECIMAL,
    seller_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    CONSTRAINT CHK_Condition CHECK (condition='new' OR condition='old')
);''')

# Table Cart
cursor.execute('''
CREATE TABLE IF NOT EXISTS cart (
    buyer_id INTEGER,
    item_id INTEGER,
    quantity INT NOT NULL,
    FOREIGN KEY (item_id) REFERENCES Item(id)
);''')
               
cursor.execute('''
CREATE TABLE IF NOT EXISTS Purchase_History (
    t_id VARCHAR(100),
    buyer_id INTEGER,
    item_id INTEGER,
    quantity INT NOT NULL,
    feedback_thumbsup INT DEFAULT 0,
    feedback_thumbsdown INT DEFAULT 0,
    FOREIGN KEY (item_id) REFERENCES Item(id)
    PRIMARY KEY (t_id,item_id)
);''')
               
cursor.execute("INSERT INTO Item VALUES (5, 'Apple',    '1', 'Red,Fruit,Health,Food',       'new', 3, 1, 100)")
cursor.execute("INSERT INTO Item VALUES (6, 'Grapes',   '1', 'Violet,Fruit,Health,Food',    'new', 3, 1, 100)")
cursor.execute("INSERT INTO Item VALUES (7, 'Cucumber', '1', 'Green,Vegetable,Health,Food', 'new', 3, 1, 100)")
cursor.execute("INSERT INTO Item VALUES (8, 'Mango',    '1', 'Yellow,Fruit,Health,Food',    'new', 3, 1, 100)")

# Commit the changes
conn.commit()

# Close the connection
conn.close()
