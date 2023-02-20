## Build and deploy image to container registry
gcloud builds submit --tag gcr.io/distributedsystems-swsr1249/buyer_server

## Auth kubectl to the cluster
gcloud container clusters get-credentials cluster-2 --zone us-central1-a --project distributedsystems-swsr1249

## Deploy the entire folder
kubectl apply -f deployment

## To find the nodeport
kubectl get service seller-server --output yaml

## To get external Ips
kubectl get nodes --output wide 

## Expose nodeport
gcloud compute firewall-rules create test-node-port \
    --allow tcp:30761