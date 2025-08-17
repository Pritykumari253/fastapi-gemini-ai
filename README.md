**FASTAPI GEMINI AI**

A simple FastAPI project to demonstrate how to build an API server for an AI application using Gemini.

**To run the application, we use the following command:**

uvicorn src.main:app --reload

The API will be available at http://127.0.0.1:8000.

**Making Requests**
You can send a request to the chat API without an authentication token. These requests are subject to a global rate limit.

**Unauthenticated Request**
You can send a request to the chat API without an authentication token. These requests are subject to a global rate limit.

**Authenticated Request**
For a higher rate limit, we can authenticate by providing a JWT token. I made sure to replace GENERATED_TOKEN with a valid token.

**Configuration**
You can configure the system prompt by editing the src/prompts/system_prompt.md file.

**Rate Limiting**
The API implements rate limiting to prevent abuse. You can modify these limits by changing the constants in src/auth/throttling.py:

GLOBAL_RATE_LIMIT = 3
GLOBAL_TIME_WINDOW_SECONDS = 60

**Generating a Test Token**
The /chat endpoint is protected and requires a JWT token for authentication. For testing purposes, we can generate a valid token using jwt.io
