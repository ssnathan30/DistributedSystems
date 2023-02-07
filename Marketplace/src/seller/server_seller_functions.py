import sqlite3
import json

class server_seller:
    def __init__(self,dbconn) -> None:
        self.dbconn = dbconn
        self.cursor = dbconn.cursor()
        self.active = False

    def create_account(self,username,password):
        try:
            self.cursor.execute(
                """
                    INSERT INTO sellers_info 
                        (username, password) 
                    VALUES 
                        ("{0}","{1}")
                """.format(username, password))
            self.dbconn.commit()
            content = {"result": "Account created"}
        except sqlite3.Error as err:
            content = {"result": "Database Error: invalid action {0}".format(str(err))}
        return 0, content

    def login(self,username,password):
        if not self.active:
            try:
                res = self.cursor.execute(
                    """
                        SELECT * FROM sellers_info 
                        WHERE username="{0}" AND
                        password="{1}"
                    """.format(username, password))
                if res.fetchone() is None:
                    content = {"result": "Login Failed !! Check your credentials or Sign up"} 
                else:
                    content = {"result": "Login Sucess !!"}
                    self.active = True
                    self.username = username
            except sqlite3.Error as err:
                content = {"result": "Database Error: invalid action {0}".format(str(err))}
            return 0, content
        else:
            return 0, {"result": "User session active"}

    def logout(self):
        if self.active:
            self.active = False
            self.username = ""
            return -1, {"result": "Sucessfully Logged Out !!"}
        else:
            return 0, {"result": "Invalid Operation. Please login!!"}

    def add_item(self,items):
        if self.active:
            try:
                for item in items:
                    res = self.cursor.execute(
                        """
                            INSERT INTO items 
                                (name, category, keywords, condition, sale_price, quantity, seller_name) 
                            VALUES 
                                ("{0}","{1}","{2}","{3}",{4},{5}, "{6}")                       
                        """.format(item["name"],item["category"],item["keywords"],item["condition"],int(item["sale_price"]),int(item["quantity"]), self.username))
                    self.dbconn.commit()
                content = {"result": "Successfully Added items"}
            except sqlite3.Error as err:
                content = {"result": "Database Error: invalid action {0}".format(str(err))}
            return 0, content
        else:
            return 0, {"result": "Invalid Operation. Please login!!"}

    def get_seller_rating(self):
        if self.active:
            try:
                res = self.cursor.execute(
                    """
                        SELECT feedback_thumbs_up, feedback_thumbs_down FROM sellers_info 
                        WHERE username="{0}"                        
                    """.format(self.username))
                if not res.fetchone():
                    content = {"result": "No Ratings Available"} 
                else:
                    content = {"result": res.fetchone()}
            except sqlite3.Error as err:
                content = {"result": "Database Error: invalid action {0}".format(str(err))}
            return 0, content
        else:
            return 0, {"result": "Invalid Operation. Please login!!"}

    def update_item(self,items):
        if self.active:
            try:
                for item in items:
                    name = item["name"]
                    price = item["price"]
                    res = self.cursor.execute(
                        ''' UPDATE items
                            SET sale_price = ?
                            WHERE name = ? AND
                            seller_name = ?
                        '''
                        , (price,name,self.username))
                    self.dbconn.commit()
                content = {"result": "Updated Items"} 
            except sqlite3.Error as err:
                content = {"result": "Database Error: invalid action {0}".format(str(err))}
            return 0, content
        else:
            return 0, {"result": "Invalid Operation. Please login!!"}

    def remove_item(self,items):
        if self.active:
            content = None
            try:
                for item in items:
                    name = item["name"]
                    quantity = item["quantity"]

                    res = self.cursor.execute(
                        ''' SELECT quantity 
                            FROM items
                            WHERE name = ? AND
                            seller_name = ? 
                        '''
                        , (name,self.username))
                    
                    existing_amount = res.fetchone()[0]

                    if int(existing_amount) <= int(quantity):
                        res = self.cursor.execute(
                                ''' DELETE 
                                    FROM items
                                    WHERE name = ? AND
                                    seller_name = ? 
                                '''
                                , (name,self.username))
                    else:
                        to_update = int(existing_amount)- int(quantity)
                        res = self.cursor.execute(
                                ''' UPDATE items 
                                    SET quantity = ?
                                    WHERE name = ? AND
                                    seller_name = ? 
                                '''
                                , (to_update, name, self.username))
                    self.dbconn.commit()
                content = {"result": "Removed/Updated Items"}
            except sqlite3.Error as err:
                content = {"result": "Database Error: invalid action {0}".format(str(err))}
            return 0, content
        else:
            return 0, {"result": "Invalid Operation. Please login!!"}

    def display_items(self):
        if self.active:
            try:
                res = self.cursor.execute(
                    """
                        SELECT * FROM items 
                        WHERE seller_name="{0}"
                    """.format(self.username))
                result = res.fetchall()
                content = {"Items" : result}
            except sqlite3.Error as err:
                content = {"result": "Database Error: invalid action {0}".format(str(err))}
            return 0, content
        else:
            return 0, {"result": "Invalid Operation. Please login!!"}
        

    def process(self,action,values=None):
        if action == 1: # Create Account
            if len(values) != 2:
                return "Invalid inputs for account creation"
            opcode, result = self.create_account(values[0],values[1])
            return opcode, json.dumps(result)
        elif action == 2: # Login
            if len(values) != 2:
                return "Invalid inputs for login"
            opcode, result = self.login(values[0],values[1])
            return opcode, json.dumps(result)
        elif action == 3: # Logout
            opcode, result = self.logout()
            return opcode, json.dumps(result)
        elif action == 4: # Seller rating
            opcode, result = self.get_seller_rating()
            return opcode, json.dumps(result)
        elif action == 5:
            opcode, result = self.add_item(values["item"])
            return opcode, json.dumps(result)
        elif action == 6:
            opcode, result = self.update_item(values)
            return opcode, json.dumps(result)
        elif action == 7:
            opcode, result = self.remove_item(values)
            return opcode, json.dumps(result)
        elif action == 8:
            opcode, result = self.display_items()
            return opcode, json.dumps(result)
        else:
            return "No OP"