from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class AgentRequest(BaseModel):
    message: str

@app.post("/agent")
async def interact(request: AgentRequest):
    return {"response": f"Agent received: {request.message}"}
