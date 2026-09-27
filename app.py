import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import agent

app = FastAPI(title="MemoryMeet AI")

# Resolve absolute path to the static directory
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


class MeetingSaveRequest(BaseModel):
    participant: str
    company: str
    notes: str


class MeetingBriefRequest(BaseModel):
    participant: str
    company: str
    agenda: str


@app.get("/")
def read_root():
    index_path = STATIC_DIR / "index.html"
    return FileResponse(str(index_path))


@app.post("/api/save-meeting")
def save_meeting(data: MeetingSaveRequest):
    return agent.save_meeting_memory(data.participant, data.company, data.notes)


@app.post("/api/get-brief")
def get_brief(data: MeetingBriefRequest):
    return agent.generate_meeting_brief(data.participant, data.company, data.agenda)