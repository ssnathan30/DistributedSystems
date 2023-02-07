#!/usr/bin/env python3
import sqlite3

class marketplace_db:
    
    def __init__(self):
        self.con = sqlite3.connect("marketplace.db")
        self.create_tables()
    
    def get_connection(self):
        return self.con

    def close_connection(self):
        self.con.close()

    def create_tables(self):
        cur = self.con.cursor()
        cur.execute(    """
                        CREATE TABLE IF NOT EXISTS sellers_info (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name VARCHAR(100),
                            username VARCHAR(100) NOT NULL UNIQUE,
                            password VARCHAR(100) NOT NULL,
                            feedback_thumbs_up INT,
                            feedback_thumbs_down INT,
                            items_sold INT
                        );
                        """
                    )
        cur.execute(    """
                        CREATE TABLE IF NOT EXISTS buyers (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name VARCHAR(100),
                            username VARCHAR(100) NOT NULL UNIQUE,
                            password VARCHAR(100) NOT NULL,
                            items_purchased INT
                            );
                        """
                    )
        cur.execute(    """
                        CREATE TABLE IF NOT EXISTS items (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name VARCHAR(100) UNIQUE,
                            category VARCHAR(100) NOT NULL,
                            keywords VARCHAR(200) NOT NULL,
                            condition VARCHAR(100) NOT NULL,
                            sale_price INT,
                            quantity INT,
                            seller_name VARCHAR(100),
                            FOREIGN KEY (seller_name) REFERENCES sellers_info(username)
                            CONSTRAINT CHK_Condition CHECK (condition='new' OR condition='old') 
                            );
                        """
                    )
        self.con.commit()
    
    def display(self):
        pass
    


db = marketplace_db()