import os

import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# This is a load balancing worker: a plain HTTP server that Runpod routes
# requests to directly, without a queue. You can use any framework you like
# (FastAPI, Flask, ...) and expose any routes your application needs.
#
# Load your model(s) once, at import time, so they are ready in memory before
# the server starts accepting traffic. For example:
#
#     model = load_my_model()

app = FastAPI()


# Define the shape of your request and response bodies. Replace these with
# whatever your endpoint actually accepts and returns.
class GenerationRequest(BaseModel):
    prompt: str
    max_tokens: int = 100
    temperature: float = 0.7


class GenerationResponse(BaseModel):
    generated_text: str


request_count = 0


# Required: Runpod calls /ping to monitor worker health.
@app.get("/ping")
async def health_check():
    # Only the status code matters:
    #   200 - Healthy
    #   204 - Initializing (e.g. your model is still loading)
    #   anything else - Unhealthy
    return JSONResponse(status_code=200, content={"status": "healthy"})


# Your custom endpoint. Add as many routes as you need; replace the mock below
# with your real inference logic.
@app.post("/generate", response_model=GenerationResponse)
async def generate(request: GenerationRequest):
    global request_count
    request_count += 1
    # Mock implementation; run your model here and return its output.
    generated_text = f"Response to: {request.prompt} (request #{request_count})"
    return {"generated_text": generated_text}


@app.get("/stats")
async def stats():
    return {"total_requests": request_count}


@app.get("/")
async def root():
    datacenter_id = os.getenv("RUNPOD_DC_ID")
    return {"message": f"Hello, {datacenter_id if datacenter_id else 'world'}!".strip()}


if __name__ == "__main__":
    # When you deploy your endpoint, expose this port as the HTTP port and set
    # it (plus PORT_HEALTH) as environment variables in the Runpod console.
    port = int(os.getenv("PORT", "5000"))

    # Start the server, listening on all interfaces.
    uvicorn.run(app, host="0.0.0.0", port=port)
