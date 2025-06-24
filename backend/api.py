import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from model import predict_intent, get_response
from typing import Optional

class AstraBankAPI:
    def __init__(self):
        self.app = FastAPI()
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # For production, restrict to your frontend URL
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        self.add_routes()

    def add_routes(self):
        @self.app.post("/chat")
        async def chat(msg: Message, id: Optional[str] = None):
            # Preprocess message to match model expectations
            user_message = msg.message.strip().lower()
            intent = predict_intent(user_message)
            response = get_response(intent)
            return {"response": response, "id": id}

class Message(BaseModel):
    message: str

astra_api = AstraBankAPI()
app = astra_api.app

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
