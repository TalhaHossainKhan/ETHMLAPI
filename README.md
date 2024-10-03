# Overview

This project converts the Ethereum fraud detection model into a FastAPI-based API, allowing seamless communication with the Chrome extension. The API provides real-time fraud risk assessment for Ethereum addresses.

# How It Works

I wrapped the existing fraud detection model in a FastAPI application. Here's a quick rundown:

1. The model is loaded when the API starts up.
2. Endpoints are set up to accept Ethereum addresses.
3. When a request comes in, the API processes the address through our model.
4. The result is returned as a JSON response.

This setup lets the Chrome extension quickly check addresses without needing to run the full model locally.
