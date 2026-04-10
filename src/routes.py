from fastapi import APIRouter
from pydantic import BaseModel
from src.agent import Agent
from src.memory import memory

router = APIRouter()
agent = Agent()

class ChatRequest(BaseModel):
    session_id: str
    customer_id: str
    message: str

@router.post("/chat")
def chat(req: ChatRequest):
    history = memory.get(req.session_id)
    reply = agent.run(req.customer_id, req.message, history)
    memory.add(req.session_id, req.message, reply)
    return {"reply": reply}
