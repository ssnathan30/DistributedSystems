from concurrent import futures
import os
import pathlib
import grpc
import sqlite3
import customer_pb2
import customer_pb2_grpc
import sys

# path to parent and src directory
parent_dir = pathlib.Path(__file__).parent.resolve()
src_dir = pathlib.Path(__file__).parent.parent.resolve()

sys.path.append(parent_dir)

class CustomerDatabaseServerServicer(customer_pb2_grpc.CustomerDatabaseServerServicer):
    def GetData(self, request, context):
        # Connect to the database
        conn = sqlite3.connect(f'{parent_dir}/db/customer.db')
        cursor = conn.cursor()
        try:
            cursor.execute(request.query)
            # Fetch the results and build the response
            rows = cursor.fetchall()
            
            response = customer_pb2.GetDataResponse()
            for row in rows:
                values = []
                for i in range(len(row)):
                    column_value = customer_pb2.ColumnValue(column_name=cursor.description[i][0], column_value=str(row[i]))
                    values.append(column_value)
                response.rows.append(customer_pb2.Row(values=values))
            error = customer_pb2.Error(error_code=1,error_message="Success")
            response.error.CopyFrom(error)
            return response
        except Exception as e:
            # Return an error response if there was an issue with the get
            error = str(e)
            response = customer_pb2.InsertDataResponse()
            error = customer_pb2.Error(error_code=-1,error_message=error)
            response.error.CopyFrom(error)
            return response
        finally:
            # Close the connection to the database
            cursor.close()
            conn.close()

    def InsertData(self, request, context):
        # Connect to the database
        conn = sqlite3.connect(f'{parent_dir}/db/customer.db')
        cursor = conn.cursor()
        try:
            # Execute the insert statement
            cursor.execute(request.query)
            insert_id = cursor.lastrowid
            conn.commit()
        except Exception as e:
            # Return an error response if there was an issue with the insert
            error = str(e)
            response = customer_pb2.InsertDataResponse()
            error = customer_pb2.Error(error_code=-1,error_message=error)
            response.error.CopyFrom(error)
            return response
        finally:
            cursor.close()
            conn.close()
        
        # Return the insert id
        response = customer_pb2.InsertDataResponse(insert_id=insert_id)
        error = customer_pb2.Error(error_code=1,error_message="Success")
        response.error.CopyFrom(error)
        return response
    
    def UpdateData(self, request, context):
        # Connect to the database
        conn = sqlite3.connect(f'{parent_dir}/db/customer.db')
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
            response = customer_pb2.UpdateDataResponse()
            error = customer_pb2.Error(error_code=-1,error_message=error)
            response.error.CopyFrom(error)
            return response
        finally:
            cursor.close()
            conn.close()

        response = customer_pb2.UpdateDataResponse(affected_rows=affected_rows)
        error = customer_pb2.Error(error_code=1,error_message="Success")
        response.error.CopyFrom(error)
        return response

    def DeleteData(self, request, context):
        # Connect to the database
        conn = sqlite3.connect(f'{parent_dir}/db/customer.db')
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
            response = customer_pb2.DeleteDataResponse()
            error = customer_pb2.Error(error_code=-1,error_message=error)
            response.error.CopyFrom(error)
            return response
        finally:
            cursor.close()
            conn.close()

        response = customer_pb2.DeleteDataResponse(affected_rows=affected_rows)
        error = customer_pb2.Error(error_code=1,error_message="Success")
        response.error.CopyFrom(error)
        return response

def serve():
    customer_host = os.getenv("customer_host","localhost")
    customer_port = os.getenv("customer_port",50080)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1000))
    customer_pb2_grpc.add_CustomerDatabaseServerServicer_to_server(CustomerDatabaseServerServicer(), server)
    server.add_insecure_port(f'{customer_host}:{customer_port}')
    print(f'Listening on hostname: {customer_host}, port {customer_port}')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
