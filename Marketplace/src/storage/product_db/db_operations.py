from concurrent import futures
import os
import pathlib
import sqlite3
import product_pb2
import sys
from pysyncobj import *

# path to parent and src directory
parent_dir = pathlib.Path(__file__).parent.resolve()
src_dir = pathlib.Path(__file__).parent.parent.resolve()

sys.path.append(parent_dir)

class db_operations(SyncObj):
    def __init__(self,self_node,peer_nodes):
        self.self_node = self_node
        print(self_node)
        print(peer_nodes)
        try:
            super(db_operations, self).__init__(selfNode=self_node,otherNodes=peer_nodes)
        except Exception as e:
            print(e)
        print("Init Done")

    @replicated_sync
    def Get(self, request):
        # Connect to the database
        print("Executing Get Method")
        conn = sqlite3.connect(f'{parent_dir}/db/product.db')
        #conn = sqlite3.connect(f'product_{self.self_node}.db')
        cursor = conn.cursor()
        try:
            print(request)
            cursor.execute(request.query)
            # Fetch the results and build the response
            rows = cursor.fetchall()
            
            response = product_pb2.GetResponse()
            for row in rows:
                values = []
                for i in range(len(row)):
                    column_value = product_pb2.ColValue(column_name=cursor.description[i][0], column_value=str(row[i]))
                    values.append(column_value)
                response.rows.append(product_pb2.Rows(values=values))
            error = product_pb2.Issue(error_code=1,error_message="Success")
            response.error.CopyFrom(error)
            return response
        except Exception as e:
            # Return an error response if there was an issue with the get
            error = str(e)
            response = product_pb2.InsertResponse()
            error = product_pb2.Issue(error_code=-1,error_message=error)
            response.error.CopyFrom(error)
            return response
        finally:
            # Close the connection to the database
            cursor.close()
            conn.close()

    @replicated_sync
    def Insert(self, request):
        # Connect to the database
        conn = sqlite3.connect(f'{parent_dir}/db/product.db')
        cursor = conn.cursor()
        try:
            # Execute the insert statement
            cursor.execute(request.query)
            insert_id = cursor.lastrowid
            conn.commit()
        except Exception as e:
            # Return an error response if there was an issue with the insert
            error = str(e)
            response = product_pb2.InsertResponse()
            error = product_pb2.Issue(error_code=-1,error_message=error)
            response.error.CopyFrom(error)
            return response
        finally:
            cursor.close()
            conn.close()
        
        # Return the insert id
        response = product_pb2.InsertResponse(insert_id=insert_id)
        error = product_pb2.Issue(error_code=1,error_message="Success")
        response.error.CopyFrom(error)
        return response
    
    @replicated_sync
    def Update(self, request):
        # Connect to the database
        conn = sqlite3.connect(f'{parent_dir}/db/product.db')
        cursor = conn.cursor()
        try:
            # Execute the update statement
            cursor.execute(request.query)
            # Return the number of affected rows
            affected_rows = cursor.rowcount
            conn.commit()
        except Exception as e:
            # Return an error response if there was an issue with the update
            error = str(e)
            response = product_pb2.UpdateResponse()
            error = product_pb2.Issue(error_code=-1,error_message=error)
            response.error.CopyFrom(error)
            return response
        finally:
            cursor.close()
            conn.close()

        response = product_pb2.UpdateResponse(affected_rows=affected_rows)
        error = product_pb2.Issue(error_code=1,error_message="Success")
        response.error.CopyFrom(error)
        return response

    @replicated_sync
    def Delete(self, request):
        # Connect to the database
        conn = sqlite3.connect(f'{parent_dir}/db/product.db')
        cursor = conn.cursor()
        # Execute the delete statement
        try:
            cursor.execute(request.query)
            # Return the number of affected rows
            affected_rows = cursor.rowcount
            conn.commit()
        except Exception as e:
            # Return an error response if there was an issue with the update
            error = str(e)
            response = product_pb2.DeleteResponse()
            error = product_pb2.Issue(error_code=-1,error_message=error)
            response.error.CopyFrom(error)
            return response
        finally:
            cursor.close()
            conn.close()

        response = product_pb2.DeleteResponse(affected_rows=affected_rows)
        error = product_pb2.Issue(error_code=1,error_message="Success")
        response.error.CopyFrom(error)
        return response