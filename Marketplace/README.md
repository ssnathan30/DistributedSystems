## Programming Assignment Four

### Overview
An online marketplace is an e-commerce site that brings sellers and buyers together in one place. It allows sellers to 
put  items  for  sale  and  interested  buyers  to  purchase  those  items.

### Architecture
Components:
- Buyer
    - Buyer-Client-Interface
    - Buyer-Server-Interface
- Seller
    - Seller-Client-Interface
    - Seller-Server-Interface
- Storage
    - Customer-Database-Server
        - Atomic Broadcast Protocol
    - Product-Database-Server
        - Raft
    - Financial-Database-Server

#### Storage
- Customer and Product Server process requests through gRPC
    - The replication is handled by custom broadcast protocol for the customer database.
    - The replication is handled Psync raft implementation for the product database.
- Financial Server process requests through SOAP

##### Customer and Product Server
- The package contains the .proto files and gen_grpc script that can be used to generate the client and server stubs.
- Sqllite3 is used as the database for storing all the information
- To the start the server locally
```python
    python3 product_db_server.py
    python3 customer_db_server
```
- Each package contains the docker file to build images.

##### Financial Server
- The soap server exposed the endpoint "process_transaction".
- To start the soap server locally
```
    python3 soap_server.py
```

#### Seller and Buyer
- This component contains the client and server interface.
- Client
    - The client can be started by executing the  "<seller/buyer>_client_execution.py"
    - Client Interface takes care of validating the input, If all the required inputs are not provided, It will throw a validation error.
    - Using the logging module, The response time for each API is logged to "<seller/buyer>_response_time.log" inside the logs folder.
- Server
    - The server can be started locally using
    ```
        "python3 -m seller-server"
        "python3 -m swagger-server"
    ```
    - All the connection details are passed as env variables.
    - All the endpoint implementation can be found as part of the controllers
    - Endoint details and the inputs can be found as part of the swagger UI. http://<hostname:port>/api/v1/ui
    - In order to calculate the server throughout, The server processing time is logged to "<seller/buyer>_server_throughput.log" inside the logs folder.
#### Semantics for Keyword search
- For this functionality, I am using the existing python package “fuzzywuzzy” which calculates the matching score given a word and a list of words.
- It uses Levenshtein Distance to calculate the differences between sequences.
- Based on the item category, items are filtered.
- Then each item's keyword gets a score based on the input using the fuzzywuzzy library.
- Then the item along with its score is added to the heap.
- Currently, We are showing the top result based on the score. 
- This can be extended to show top 10 items based on keywords.

#### Current state
The source code is divided according to the components mentioned above.<br>

- Replication Factor
    - Seller server : 4
    - Buyer server : 4
    - Customer database : 5
    - Product database  : 5
    - Financial database : 1

- Functionalities
    - Buyer component supports the following functionalities
        - Acount Creation
        - Login
        - Logout
        - Search items for sale
        - Add item to cart
        - Remove item from cart
        - Clear cart
        - Display cart
        - Get Seller Rating
        - Make purchase
        - Provide seller rating
        - Get purchase history
    - Seller component supports the following functionalites
        - Account Creation
        - Login
        - Logout
        - Get Seller Rating
        - Add Item for Sale
        - Update Item Sale Price
        - Remove Item from Sale
        - Display All Items Posted by Seller
- Execution and Evaluation Script
    - Both seller and buyer modules contains the script to test different scenarios.
    - Execution scripts invokes all the apis based on the inputs and invokes one particular API for 1000 times.
    - Evaluation script creates 'n' instances using process pool executor and invokes the method in execution script.
    - Combining both the scripts, we can run 'n' instances and each instance invoking one api 1000 times for performance evaluation.
    - Usage
        - Start all the services using docker compose file
        ```
            docker compose up
        ```
        - Seller Server is mapped to port 4444
        - Buyer Server is mapped to port 5555
        - Make sure the configuration file inside the client package is modified to use the correct host and port name.
        - Run the evaluation script from corresponding module.
        ```
            - python3 <seller/buyer>_evaluation_script.py <NO_OF_CLIENT_WORKERS>
            - e.g. python3 seller_evaluation_script.py 10 ## For 10 instances of buyer or seller 
        ```
- Logs
    - Response time is logged for every api to log file inside logs folder.
    - Throughput time is logged for every api to log file inside the container.
    - How to copy the logs from container ?
    ```
        Buyer log :
        docker cp <container-id>:/usr/src/app/swagger_server/logs/buyer_server_throughput.log . 
        Seller log :
        docker cp <container-id>:/usr/src/app/seller_server/logs/seller_server_throughput.log .
    ```
- Assumptions
    - Server takes care of validating the authenticity of the request
    - Any operation can be performed by ther user only after login.
    - Purchase History is part of the product database
    - Financial Server returns [True/False] based on randomness (90% True and 10% False)

#### Hosting in GCP
- Enable kubernetes engine API for the project
- Create a standard cluster
- build all the server and database images and store it in the container registry
- Deploy service and deployment scripts to the cluster using kubectl
- Find the nodeport and IP

##### Build and deploy image to container registry
```
gcloud builds submit --tag <Container Registry>
gcloud builds submit --tag gcr.io/distributedsystems-swsr1249/buyer_server
```

##### Authenticat and configure kubectl to your cluster
```
gcloud container clusters get-credentials <cluster-name> --zone <zone> --project <project-id>
gcloud container clusters get-credentials cluster-2 --zone us-central1-a --project distributedsystems-swsr1249
```

##### Deploy the deployment folder
```
kubectl apply -f deployment
```

##### To find the nodeport
```
kubectl get service <service-name> --output yaml
kubectl get service seller-server --output yaml
```

##### To get external Ips
```
kubectl get nodes --output wide 
```

##### Expose nodeport
```
gcloud compute firewall-rules create test-node-port --allow tcp:30761
```
