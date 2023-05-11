# URL Shortener

In this repository I've implemented a URL shortener service using FastAPI and Redis. I've also dockerized the server and orchestrated it using Kubernetes. 

## How to use

First, create a persistent volume for Redis:

```bash
kubectl apply -f pvolume/redis/pvolume.yml
```

Then, create a persistent volume claim:

```bash
kubectl apply -f pvclaim/redis/pvclaim.yml
```

 Now you can create a deployment and a service for Redis:

```bash
kubectl apply -f deployment/redis/deployment.yaml
kubectl apply -f service/redis/service.yaml
```

Finally, you can create a deployment and a service for server:

```bash
kubectl apply -f deployment/api/deployment.yaml
kubectl apply -f service/api/service.yaml
```

To test the service, you should first create a pod for my simple curl docker image:

```bash
kubectl run curl -it --image amirparsa/simple-curl
```

In the opened prompt you can send an HTTP request to the server. Here is a sample request for `www.google.com`:

```bash
curl --location -s --request POST '10.101.247.133:8000/shortner' \                                                                                     ─╯
--header 'Content-Type: application/json' \
--data-raw '{
    "url": "www.google.com"
}'
```




