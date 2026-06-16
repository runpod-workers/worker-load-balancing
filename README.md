![Load Balancing Worker](public/worker-load-balancing_banner.png)

---

This repository is a starting point for building your own custom Runpod Serverless **load balancing** worker. Unlike a queue-based worker (which runs a `handler` function), a load balancing worker is a plain HTTP server that Runpod routes requests to directly — so you can use any framework (FastAPI, Flask, ...) and expose any routes your application needs.

---

[![Runpod](https://api.runpod.io/badge/runpod-workers/worker-load-balancing)](https://www.runpod.io/console/hub/runpod-workers/worker-load-balancing)

---

## Getting Started

1. **Use this template:** Create a new repository from this template (click **Use this template** on GitHub) or clone it directly.
2. **Customize:** Modify the server code and configuration to implement your task.
3. **Test:** Run the worker locally to ensure it functions correctly.
4. **Deploy:** Connect your repository to Runpod, or build and push the Docker image manually.

## Customizing Your Worker

- **`app.py`:** This is the core of your worker — a FastAPI HTTP server.
  - Load your model(s) once, at import time, so they're ready before the server accepts traffic.
  - The `/ping` endpoint is **required**: Runpod calls it to monitor worker health (return `200` when healthy, `204` while still initializing).
  - Replace the example `/generate` and `/stats` routes with whatever endpoints your application needs.
- **`requirements.txt`:** Add any Python libraries your worker needs here.
- **`Dockerfile`:** Defines the image for your worker. Add system dependencies (`apt-get install ...`), environment variables, or other setup steps as needed.
- **`.runpod/hub.json`:** Configuration for publishing to the [Runpod Hub](https://docs.runpod.io/hub/overview). `endpointType` is set to `"LB"` so the Hub deploys this as a load balancing endpoint. Update the title, description, category, and compute config for your worker.
- **`.runpod/tests.json`:** Sample inputs used to validate your worker when published to the Hub.

## Testing Locally

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python app.py
```

The server starts on the port set by `PORT` (default `5000`). In another terminal:

```bash
curl -X POST "http://localhost:5000/generate" \
    -H "Content-Type: application/json" \
    -d '{"prompt": "Hello, world!"}'

curl "http://localhost:5000/ping"
```

## Deploying to Runpod

There are two main ways to deploy your worker:

1. **GitHub integration (recommended):** Connect your repository to Runpod Serverless and select **Load Balancer** as the endpoint type. Runpod builds and deploys automatically when you push. See the [Build a load balancing worker guide](https://docs.runpod.io/serverless/load-balancing/build-a-worker).

2. **Manual Docker build & push:**

   ```bash
   # Build
   docker build --platform linux/amd64 -t YOUR_DOCKER_USERNAME/worker-load-balancing:v1.0 .

   # Push
   docker push YOUR_DOCKER_USERNAME/worker-load-balancing:v1.0
   ```

   Then create a Load Balancer endpoint in the Runpod console pointing at that image.

When configuring the endpoint, **expose HTTP port 5000** and add these environment variables:

- `PORT = 5000`
- `PORT_HEALTH = 5000`

## Test Requests

Once deployed, call your endpoint:

```bash
curl -X POST "https://ENDPOINT_ID.api.runpod.ai/generate" \
    -H 'Authorization: Bearer RUNPOD_API_KEY' \
    -H "Content-Type: application/json" \
    -d '{"prompt": "Hello, world!"}'
```

```bash
curl -X GET "https://ENDPOINT_ID.api.runpod.ai/ping" \
    -H 'Authorization: Bearer RUNPOD_API_KEY'
```

```bash
curl -X GET "https://ENDPOINT_ID.api.runpod.ai/stats" \
    -H 'Authorization: Bearer RUNPOD_API_KEY'
```

## Further Information

- [Load Balancing Endpoints](https://docs.runpod.io/serverless/load-balancing/overview)
- [Build a Load Balancing Worker](https://docs.runpod.io/serverless/load-balancing/build-a-worker)
- [Runpod Hub](https://docs.runpod.io/hub/overview)
- [Runpod Serverless Documentation](https://docs.runpod.io/serverless/overview)
- [Community Discord](https://discord.gg/cUpRmau42V)
