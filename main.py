import os
from fastapi import FastAPI
from pydantic import BaseModel
from ai.gemini import Gemini
from auth.dependencies import get_user_identifier
from auth.throttling import apply_rate_limit

#-------APP Initialization--------
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "APP is running"}

#--------AI Configuration----------
def load_system_prompt():
    try:
        with open("system_prompt.md", "r") as f:
            return f.read()
    except FileNotFoundError:
        return None

system_prompt = load_system_prompt()
gemini_api_key = "____API_KEY____"

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set.")
#create an instance of gemini client
ai_platform = Gemini(api_key=gemini_api_key, system_prompt=system_prompt)


#--------Pydantic Models---------
class ChatRequest(BaseModel):
    prompt: str   # we expect a json body like {"prompt": "....."}

class ChatResponse(BaseModel):
    response:str

#---------API Endpoints----------
@app.post("/chat", response_model = ChatResponse)
async def chat(request:ChatRequest, user_id:str = Depends(get_user_identifier)):
    apply_rate_limit(user_id)
    response_text = ai_platform.chat(request.prompt)
    return ChatResponse(response=response_text)