import logging
import sqlite3
import pathlib

parent_dir = pathlib.Path(__file__).parent.resolve()

# path to src directory
src_dir = pathlib.Path(__file__).parent.parent.resolve()

class marketplace_db(object):

    def __init__(self,db_file_loc="/"):
        self.con = sqlite3.connect("{0}/marketplace.db".format(db_file_loc), isolation_level=None)
        self.con.execute('pragma journal_mode=wal;')
        
        logging.basicConfig(filename="{0}/logs/db_execution.log".format(src_dir),format='%(asctime)s %(message)s')
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
    
    def prepare_db(self):
        self.__create_tables()

    def __get_connection(self):
        return self.con
    
    def __get_cursor(self):
        return self.con.cursor()

    def __close_connection(self):
        self.con.close()
    
    def execute(self,query,get_result):
        try:
            res = self.con.execute(query)
            self.con.commit()
            if get_result:
                result = res.fetchall()
            return {"message": "Success","error_code" : 0, "value": result if get_result else ""}
        except Exception as e:
            self.logger.info(str(e))
            return {"message": "Database Error: invalid action {0}".format(str(e)), "error_code" : -1, "value" : ""}

    def __create_tables(self):
        cur = self.con.cursor()
        cur.execute("""
                        CREATE TABLE IF NOT EXISTS sellers_info (
                            id INTEGER PRIMARY KEY NOT NULL,
                            name VARCHAR(100),
                            username VARCHAR(100) NOT NULL UNIQUE,
                            password VARCHAR(100) NOT NULL,
                            feedback_thumbs_up INT,
                            feedback_thumbs_down INT,
                            items_sold INT
                        );
                        """
                    )
        cur.execute("""
                        CREATE TABLE IF NOT EXISTS buyers_info (
                            id INTEGER PRIMARY KEY NOT NULL,
                            name VARCHAR(100),
                            username VARCHAR(100) NOT NULL UNIQUE,
                            password VARCHAR(100) NOT NULL,
                            items_purchased INT
                            );
                        """
                    )
        cur.execute("""
                        CREATE TABLE IF NOT EXISTS items (
                            id INTEGER PRIMARY KEY NOT NULL,
                            name VARCHAR(100) NOT NULL UNIQUE,
                            category INT NOT NULL CHECK (category >= 0 AND category <= 9),
                            keywords VARCHAR(200) NOT NULL,
                            condition VARCHAR(100) NOT NULL,
                            sale_price NUMERIC NOT NULL,
                            quantity INT DEFAULT 1 NOT NULL,
                            seller_id INTEGER NOT NULL,
                            FOREIGN KEY (seller_id) REFERENCES sellers_info(id)
                            CONSTRAINT CHK_Condition CHECK (condition='new' OR condition='old') 
                            );
                        """
                    )
        cur.execute("""
                        CREATE TABLE IF NOT EXISTS cart (
                            buyer_id INTEGER,
                            item_id INTEGER,
                            quantity INT NOT NULL,
                            FOREIGN KEY (item_id) REFERENCES items(id),
                            FOREIGN KEY (buyer_id) REFERENCES buyers(id)
                        );
                    """)
        cur.execute("""
                        CREATE TABLE IF NOT EXISTS performance (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            func_name VARCHAR(100),
                            exec_time VARCHAR(100)
                        );
                    """)
        self.con.commit()

    def display_all_tables(self):
        all_tables = """
                    SELECT name FROM sqlite_master  
                    WHERE type='table';
                    """
        result = self.__get_cursor().execute(all_tables)
        return result.fetchall()


db = marketplace_db(parent_dir)
db.prepare_db()
print(db.display_all_tables())