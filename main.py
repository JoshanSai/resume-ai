from fastapi import FastAPI
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

from agent import talkToAgent

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AgentChat(BaseModel):
    session_id: str
    query: str


@app.post("/talk-to-agent")
def agent(data: AgentChat):
    return talkToAgent(data.session_id, data.query)
