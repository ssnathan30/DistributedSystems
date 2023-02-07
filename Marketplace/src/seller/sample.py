import sqlite3
import sys
import os 
"""
con = sqlite3.connect("/Users/thedarkknight/Batman/Nathan/GradSchool/Spring-2023/DistributedSystems/Workspace/DistributedSystems/Marketplace/src/com.package.seller/marketplace.db")
cur = con.cursor()
print(cur.execute("PRAGMA table_info('sellers_info')").fetchall())
print(cur.execute("select * from items").fetchall())
cur.close()
"""
#print(sys.path)

file_dir = os.path.dirname(__file__)
print(file_dir)
sys.path.append(file_dir)


#path = os.getcwd()
print(os.path.abspath(os.path.join(file_dir, os.pardir)))