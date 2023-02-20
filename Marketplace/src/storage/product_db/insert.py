import sqlite3
import json
import pathlib

# path to parent and src directory
parent_dir = pathlib.Path(__file__).parent.resolve()
src_dir = pathlib.Path(__file__).parent.parent.resolve()

# Connect to the database
conn = sqlite3.connect('{0}/db/product.db'.format(parent_dir))
cursor = conn.cursor()

cursor.execute("INSERT INTO Item VALUES (5, 'Apple', '1', 'Red,Fruit,Health,Food', 'new', 3, 1, 10)")
cursor.execute("INSERT INTO Item VALUES (6, 'Grapes', '1', 'Violet,Fruit,Health,Food', 'new', 3, 1, 10)")
cursor.execute("INSERT INTO Item VALUES (7, 'Cucumber', '1', 'Green,Vegetable,Health,Food', 'new', 3, 1, 10)")
cursor.execute("INSERT INTO Item VALUES (8, 'Mango', '1', 'Yellow,Fruit,Health,Food', 'new', 3, 1, 10)")
cursor.execute("INSERT INTO Item VALUES (9, 'Mango', '1', 'Yellow,Fruit,Health,Food', 'new', 3, 1, 10)")

# Commit the changes
conn.commit()

# Close the connection
conn.close()