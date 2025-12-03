# src/app/api.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.app.orchestrator import handle_user_message

app = FastAPI(title="Hyper Personalized CX Bot")

# Allow frontend (React dev server) to call the backend
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # Which origins can call this API
    allow_credentials=True,
    allow_methods=["*"],            # Allow POST, GET, OPTIONS, etc.
    allow_headers=["*"],            # Allow all headers
)


class ChatRequest(BaseModel):
    user_id: str
    message: str
    lat: float
    lon: float


class ChatResponse(BaseModel):
    answer: str


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    result = handle_user_message(req.user_id, req.message, req.lat, req.lon)
    return ChatResponse(answer=result["answer"])
