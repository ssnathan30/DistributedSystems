import sqlite3
import json
import pathlib

# path to parent and src directory
parent_dir = pathlib.Path(__file__).parent.resolve()
src_dir = pathlib.Path(__file__).parent.parent.resolve()

# Connect to the database
conn = sqlite3.connect('{0}/db/product.db'.format(parent_dir))
cursor = conn.cursor()

res = cursor.execute("select * from Purchase_History")
print(res.fetchall())

#res = cursor.execute("select * from Purchase_History")
#print(res.fetchall())

# Commit the changes
conn.commit()

# Close the connection
conn.close()