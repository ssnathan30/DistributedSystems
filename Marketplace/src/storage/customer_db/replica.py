from collections import defaultdict
import socket
import threading
import json
import time
from util import *
from  request_message import *
from sequence_message import *
import uuid
from heapq import *
from concurrent import futures
import os
import pathlib
import grpc
import sqlite3
import customer_pb2
import customer_pb2_grpc
import sys
from replica import *

BUFFER_SIZE = 1024

# path to parent and src directory
parent_dir = pathlib.Path(__file__).parent.resolve()
src_dir = pathlib.Path(__file__).parent.parent.resolve()

sys.path.append(parent_dir)

class db_operations:

   def GetData(self,request):
        conn = sqlite3.connect(f'{parent_dir}/db/customer.db')
        cursor = conn.cursor()
        try:
            cursor.execute(request)
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

   def InsertData(self, request):
        # Connect to the database
        conn = sqlite3.connect(f'{parent_dir}/db/customer.db')
        cursor = conn.cursor()
        try:
            # Execute the insert statement
            cursor.execute(request)
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
    
   def UpdateData(self, request):
        # Connect to the database
        conn = sqlite3.connect(f'{parent_dir}/db/customer.db')
        cursor = conn.cursor()
        try:
            # Execute the update statement
            cursor.execute(request)
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

   def DeleteData(self, request):
        # Connect to the database
        conn = sqlite3.connect(f'{parent_dir}/db/customer.db')
        cursor = conn.cursor()
        # Execute the delete statement
        try:
            cursor.execute(request)
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

class replica:
   def __init__(self,replica_id,peers,udp_port,total_replicas,host) -> None:
      """
         replica_id  : The instance id
         peers       : List of peers to broadcast request
         udp_port    : Port for the gRPC server to send request 
         total_replicas : Total number of replicas
         host        : Replica's hostname
      """
      self.replica_id = replica_id
      self.local_seq_no = 0
      self.global_seq_no = 0
      self.total_replicas = total_replicas

      print(f"Total replicas : {self.total_replicas}")
      
      # Next global number that the replica should handle
      self.next_gsn = self.replica_id

      # Buffer requests - Maintain heap
      self.buffer = []

      # Heap that maintains the global_seq_number and request
      self.ready_to_process = []

      # For handling negative ack
      self.backup_buffer = dict()
      
      # Metadata
      self.last_delivered_local_seq_no = -1
      self.last_delivered_global_seq_no = 0
      self.last_received_global_seq_no = -1

      # Processed requests
      self.processed_gids = set()
      # Map request_id -> request
      self.processed_requests = {}

      # Peers to broadcast incoming messages
      self.peers = peers.values()
      self.peer_replica_map = peers
      
      self.peer_request_port = udp_port
      self.host = host if host else "localhost"

      # DB operations
      self.db_ops = db_operations()

      # Create a socket object and bind it to the specified host and port
      self.peer_req_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      self.peer_req_socket.bind((self.host, self.peer_request_port))
   
   def handle_peer_requests(self):
    """
    Handles incoming messages from peers.
    """
    while True:
         message, address = self.peer_req_socket.recvfrom(BUFFER_SIZE)
         print(f"Received message from {address}: {message.decode()}")

         str_payload = message.decode()
         json_payload = json.loads(str_payload)

         # Handle request based on type
         if json_payload["type"] == "request_message":
            self.handle_request_message(json_payload["message"])
         elif json_payload["type"] == "neg_ack_req":
            self.handle_negative_ack_request(json_payload["message"])
         elif json_payload["type"] == "neg_ack_res":
            self.handle_negative_ack_response(json_payload["message"],int(json_payload["gid"]))
         else:
            self.handle_sequence_message(json_payload["message"])
   
   def handle_negative_ack_request(self,request):
      json_payload = json.loads(request)
      g_seq_no = json_payload["global_seq_number"]
      send_to = json_payload["requested_by"]

      print(f"Handling {send_to}'s Negative_ACK_request for GID : {g_seq_no} ")

      while g_seq_no not in self.backup_buffer:
         print(f"Buffer : {self.backup_buffer}")
         print(f"Request not in backup buffer. Sleeping for 5 secs")
         time.sleep(5)
      
      request = self.backup_buffer[g_seq_no]

      payload = dict()
      payload["message"] = json.dumps(request.__dict__)
      payload["type"] = "neg_ack_res"
      payload["gid"] = g_seq_no
      payload = dict_to_bytes(payload)

      # send request
      self.peer_req_socket.sendto(payload, self.peer_replica_map[send_to])
   
   def handle_negative_ack_response(self,request,gid):
      json_payload = json.loads(request)
      request = request_message(**json_payload)

      print(f"Received Negative ACK response for {gid}")
      
      # Update the global sequence number
      if self.global_seq_no < gid:
         self.global_seq_no = gid
      
      to_remove = None

      for r_id, r in self.buffer:
         if request.request_id == r_id:
            to_remove = (r_id, r)

      if to_remove:
         self.buffer.remove(to_remove)

      gids = [x[0] for x in self.ready_to_process]
      print(f"Available Gids : {gids}")

      # Push to the ready buffer
      try:
         if gid not in gids:
            heappush(self.ready_to_process,(gid, request))
      except Exception as e:
         print(e)

   def send_neg_ack(self,i):
      replica_id = None
      if i % self.total_replicas == 0:
         replica_id = self.total_replicas
      else:
         replica_id = i % self.total_replicas
      
      payload = dict()
      payload["message"] = json.dumps({"global_seq_number" : i, "requested_by" : self.replica_id})
      payload["type"] = "neg_ack_req"
      payload = dict_to_bytes(payload)

      print(f"Sending Negative Ack for {i} to {replica_id}")

      # Send message to the peer
      print(self.peer_replica_map[replica_id])
      self.peer_req_socket.sendto(payload, self.peer_replica_map[replica_id])
   
   def send_negative_ack(self,peer_last_gsn):
      if peer_last_gsn > self.last_received_global_seq_no:
         print("Handling Negative Ack")
         for i in range(self.last_received_global_seq_no + 1, peer_last_gsn + 1):
            self.send_neg_ack(i)
   
   def handle_request_message(self,request):
      str_payload = request
      json_payload = json.loads(str_payload)

      request = request_message(**json_payload)
      heappush(self.buffer,(request.request_id,request))

      # Handle negative ack if necessary
      # peer_last_gsn = int(request.metadata["last_received_gsn"])
      # self.send_negative_ack(peer_last_gsn)
         
      print(f"Task buffer : {self.buffer}")

   def handle_sequence_message(self,request):
      json_payload = json.loads(request)
      json_payload = json_to_dic(json_payload)

      seq_request = sequence_message(**json_payload)
      
      # Update the global sequence number
      self.global_seq_no = seq_request.global_seq_no
      self.last_received_global_seq_no = seq_request.global_seq_no
      
      for request_id, request in self.buffer:
          if request_id == seq_request.request_id:
             heappush(self.ready_to_process,(seq_request.global_seq_no, request))
             break
      
      # Handle negative ack if necessary
      # peer_last_gsn = int(seq_request.metadata["last_received_gsn"])
      # self.send_negative_ack(peer_last_gsn)

   def prereq_check_to_process_seq_msg(self):
      ## This checks if all the global seq < k has sequence and request message
      g_ids = [ item[0] for item in self.ready_to_process]
      g_ids.extend(self.processed_gids)

      print(g_ids)
      print(self.global_seq_no)

      for i in range(1,self.global_seq_no):
         if i not in g_ids:
            return False, i
         
      ## This checks if all the local seq has a sequence and request message
      for i in range(1,self.local_seq_no):
         if i not in g_ids:
            return False, i
      
      return True, None

   def process_sequence_messages(self):
      """
      The method that is responsible for generating sequence messages
      1) 
         It has received all Sequence messages with global sequence
         numbers less than k as well as all corresponding Request messages to which those global sequence numbers are
         assigned,
      2) 
         All request messages sent by the member with member id sid and local seq number less than seq# have been assigned a global sequence number
      """
      while True:
         if self.buffer:
            print(f"Processing Global sequence number : {self.global_seq_no}" )
            if self.next_gsn == self.global_seq_no + 1:
               while True:
                  status, gid = self.prereq_check_to_process_seq_msg()
                  if status:
                     break
                  # send negative ack
                  self.send_neg_ack(gid)
                  print("Precheck failed")
                  time.sleep(5)
               
               self.global_seq_no = self.global_seq_no + 1
               
               request_id, request = heappop(self.buffer)
               print(f"Processing request : {request_id}")

               # Add the request to ready buffer
               heappush(self.ready_to_process,(self.global_seq_no,request))

               # Prepare sequence message
               seq_message = sequence_message(
                                                request_id=request_id,
                                                global_seq_no=self.global_seq_no,
                                                metadata={
                                                   "last_delivered_lsn" : self.last_delivered_local_seq_no,
                                                   "last_delivered_gsn" : self.last_delivered_global_seq_no,
                                                   "last_received_gsn"  : self.last_received_global_seq_no 
                                                }
                                             )
               # Convert the object to json strings
               payload = dict()
               payload["message"] = json.dumps(seq_message.__dict__)
               payload["type"] = "sequence_message"
               payload = dict_to_bytes(payload)

               # Broadcast the sequence messsage
               self.send_broadcast_message(payload)

               # Update the next global number to process
               self.next_gsn = self.next_gsn + self.total_replicas

               # Update last received global seq no
               self.last_received_global_seq_no = self.global_seq_no
            else:
               print([ gid for gid, request in self.ready_to_process])
               time.sleep(5)
         else:
               time.sleep(5)

   def connect_peers(self):
      """
      Connect peers
      """
      # Listen for incoming connections and add them to the clients list
      while True:
         client, address = self.peer_req_socket.recvfrom(BUFFER_SIZE)
         if address not in self.sock_clients:
               self.sock_clients.append(address)
               print(f"Client connected from {address}")
   
   def process_requests(self):
      while True:
         while self.ready_to_process:
            gid,request = self.ready_to_process[0]
            if self.last_delivered_global_seq_no == self.ready_to_process[0][0] - 1:
               gid, request = heappop(self.ready_to_process)

               if request.type == "get":
                  response = self.db_ops.GetData(request.request)
               elif request.type == "insert":
                  response = self.db_ops.InsertData(request.request)
               elif request.type == "update":
                  response = self.db_ops.UpdateData(request.request)
               else:
                  response = self.db_ops.DeleteData(request.request)
               
               print(f"Processed Request : {request.request} with GID : {gid}")
               
               # Add processed requests
               self.processed_gids.add(gid)
               self.processed_requests[request.request_id] = response
               self.backup_buffer[gid] = request

               print(f"Global seq ID : {self.global_seq_no}")
               print(f"Next Global seq ID : {self.next_gsn}")
               self.last_delivered_global_seq_no = gid

               # Remove the requests from the buffer
               if (request.request_id,request) in self.buffer:
                  self.buffer.remove((request.request_id,request))
            elif self.last_delivered_global_seq_no >= self.ready_to_process[0][0]:
               gid, request = heappop(self.ready_to_process)
            else:
               print(f"Last delivered GID from {self.replica_id} is {self.last_delivered_global_seq_no}")
               print(f"Ready to process GID : {self.ready_to_process[0][0]}")
               
               # Negative Ack
               # Request for sequence and requests for the missing requests
               for i in range(self.last_delivered_global_seq_no + 1,self.ready_to_process[0][0]):
                  replica_id = None

                  if i % self.total_replicas == 0:
                     replica_id = self.total_replicas
                  else:
                     replica_id = i % self.total_replicas
                  
                  payload = dict()
                  payload["message"] = json.dumps({"global_seq_number" : i, "requested_by" : self.replica_id})
                  payload["type"] = "neg_ack_req"
                  payload = dict_to_bytes(payload)

                  print(f"Sending Negative Ack for {i} to {replica_id}")

                  # Send message to the peer
                  self.peer_req_socket.sendto(payload, self.peer_replica_map[replica_id])
               time.sleep(10)
   
   def send_broadcast_request_message(self,r_message,r_type):
      # Create a unique request id
      request_id = time.time()

      # Increase the local seq number
      self.local_seq_no += 1

      # Create payload to broadcast
      req_payload = request_message  ( 
                                    request_id=request_id, 
                                    sender_id=self.replica_id,
                                    local_seq_no=self.local_seq_no,
                                    request=r_message,
                                    type=r_type,
                                    metadata={
                                       "last_delivered_lsn" : self.last_delivered_local_seq_no,
                                       "last_delivered_gsn" : self.last_delivered_global_seq_no,
                                       "last_received_gsn"  : self.last_received_global_seq_no 
                                    }
                                 )
      
      # Convert the object to json strings
      payload = dict()
      payload["message"] = json.dumps(req_payload.__dict__)
      payload["type"] = "request_message"
      payload = dict_to_bytes(payload)

      heappush(self.buffer,(req_payload.request_id,req_payload))

      # Broadcast message
      print(self.peers)
      for peer in self.peers:
         self.peer_req_socket.sendto(payload, peer)
      
      # while the request is processed, sleep
      while request_id not in self.processed_requests:
         time.sleep(5)
      
      return request_id
   
   def send_broadcast_sequence_message(self,sequence_message):
      payload = dict()
      payload["message"] = json.dumps(sequence_message)
      payload["type"] = "sequence_message"
      payload = dict_to_bytes(payload)

      # Broadcast message
      for peer in self.peers:
         self.peer_req_socket.sendto(payload, peer)
   
   def send_broadcast_message(self,request):
      """
      Sends a broadcast message to all connected clients.
      """
      json_request = json.loads(request)
      if json_request["type"] == "request_message":
         return self.send_broadcast_request_message(json_request["message"],json_request["req_type"])
      else:
         return self.send_broadcast_sequence_message(json_request["message"])
      
      # print(f"Task buffer : {self.buffer}")
   
   def start(self):
      # Start the thread for handling incoming messages
      threading.Thread(target=self.handle_peer_requests, daemon=False).start()
      threading.Thread(target=self.process_requests, daemon=False).start()
      threading.Thread(target=self.process_sequence_messages, daemon=False).start()