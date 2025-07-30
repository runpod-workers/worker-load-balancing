# Load balancing worker template

This repo contains all the files necessary to create a basic load balancing worker on Runpod. For end-to-end deployment instructions, refer to the [Runpod documentation](https://docs.runpod.io/load-balancing/build-a-worker).

## Deployment steps

1. Build the image:

```bash
docker build --platform linux/amd64 -t YOUR_DOCKER_USERNAME/loadbalancer-example:v1.0 . 
```

2. Push to Docker Hub
```bash
docker push YOUR_DOCKER_USERNAME/loadbalancer-example:v1.0
```

3. Use this container image path when deploying your endpoint to Runpod

```
YOUR_DOCKER_USERNAME/loadbalancer-example:v1.0
```

4. Make sure to expose HTTP ports 5000 and 5001 in your endpoint's container configuration, and add these environmnet variables:
    - `PORT = 5000`
    - `PORT_HEALTH = 5001`.

## Test requests

Use the curl commands below to test your endpoint:

```bash
curl -X POST "https://ENDPOINT_ID.api.runpod.ai/generate" \
    -H 'Authorization: Bearer RUNPOD_API_KEY' \
    -H "Content-Type: application/json" \
    -d '{"prompt": "Hello, world!"}'
```

```bash
curl -X GET "https://ENDPOINT_ID.api.runpod.ai/ping" \
    -H 'Authorization: Bearer RUNPOD_API_KEY' \
    -H "Content-Type: application/json"
```

```bash
curl -X GET "https://ENDPOINT_ID.api.runpod.ai/stats" \
    -H 'Authorization: Bearer RUNPOD_API_KEY' \
    -H "Content-Type: application/json"
```
