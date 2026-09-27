import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from hindsight_sdk import HindsightClient
from groq import Groq

# Initialize Clients
hindsight_client = HindsightClient(
    api_key=os.getenv("HINDSIGHT_API_KEY"),
    base_url=os.getenv("HINDSIGHT_API_URL")
)
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
BANK_ID = os.getenv("HINDSIGHT_BANK_ID", "Name: OpsMemory Incidents")

app = FastAPI(title="MemoryMeet AI")

# Frontend HTML
HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>MemoryMeet AI</title>
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0b0f19; color: #f1f5f9; margin: 0; padding: 30px 16px; }
    .wrapper { max-width: 1000px; margin: 0 auto; }
    h1 { text-align: center; color: #38bdf8; margin-bottom: 24px; font-weight: 700; }
    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 20px; margin-bottom: 24px; }
    .card { background: #161e2e; padding: 22px; border-radius: 10px; border: 1px solid #283548; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3); }
    h2 { margin-top: 0; font-size: 1.15rem; color: #38bdf8; }
    label { display: block; margin-top: 12px; font-size: 0.85rem; color: #94a3b8; font-weight: 500; }
    input, textarea { width: 100%; box-sizing: border-box; background: #0b0f19; border: 1px solid #334155; color: #f8fafc; padding: 10px 12px; border-radius: 6px; margin-top: 5px; font-size: 0.9rem; }
    input:focus, textarea:focus { outline: none; border-color: #38bdf8; }
    button { margin-top: 18px; width: 100%; padding: 11px; background: #2563eb; color: #ffffff; border: none; border-radius: 6px; cursor: pointer; font-weight: 600; font-size: 0.95rem; }
    button:hover { background: #1d4ed8; }
    #brief-output { line-height: 1.6; font-size: 0.95rem; color: #e2e8f0; }
    #brief-output table { width: 100%; border-collapse: collapse; margin: 16px 0; }
    #brief-output th, #brief-output td { border: 1px solid #334155; padding: 8px 12px; text-align: left; }
    #brief-output th { background: #1e293b; color: #38bdf8; }
    #brief-output code { background: #0f172a; padding: 2px 6px; border-radius: 4px; color: #f472b6; }
    #brief-output ul, #brief-output ol { padding-left: 20px; }
    .status-msg { color: #94a3b8; font-style: italic; }
  </style>
</head>
<body>
  <div class="wrapper">
    <h1>MemoryMeet AI</h1>
    <div class="grid">
      <div class="card">
        <h2>1. Log Past Meeting</h2>
        <label>Participant</label>
        <input id="save-part" placeholder="e.g. Rahul Sharma" />
        <label>Company</label>
        <input id="save-comp" placeholder="e.g. Acme Tech" />
        <label>Notes / Commitments</label>
        <textarea id="save-notes" rows="4" placeholder="Discussed reducing AWS costs..."></textarea>
        <button id="btn-save" onclick="saveMemory()">Save to Hindsight</button>
      </div>

      <div class="card">
        <h2>2. Prep Upcoming Meeting</h2>
        <label>Participant</label>
        <input id="prep-part" placeholder="e.g. Rahul Sharma" />
        <label>Company</label>
        <input id="prep-comp" placeholder="e.g. Acme Tech" />
        <label>New Agenda</label>
        <textarea id="prep-agenda" rows="4" placeholder="Review AWS migration proposal..."></textarea>
        <button id="btn-gen" onclick="generateBrief()">Generate Executive Brief</button>
      </div>
    </div>

    <div class="card">
      <h2>Generated Meeting Brief</h2>
      <div id="brief-output" class="status-msg">Fill in section 2 and click "Generate Executive Brief" to generate.</div>
    </div>
  </div>

  <script>
    async function saveMemory() {
      const btn = document.getElementById('btn-save');
      const participant = document.getElementById('save-part').value;
      const company = document.getElementById('save-comp').value;
      const notes = document.getElementById('save-notes').value;

      if (!participant || !company || !notes) {
        alert('Please fill out all fields.');
        return;
      }

      btn.disabled = true;
      btn.innerText = 'Saving...';
      try {
        const res = await fetch('/api/save-meeting', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({ participant, company, notes })
        });
        const data = await res.json();
        alert(data.message || 'Saved successfully');
        document.getElementById('save-notes').value = '';
      } catch (err) {
        alert('Error: ' + err);
      } finally {
        btn.disabled = false;
        btn.innerText = 'Save to Hindsight';
      }
    }

    async function generateBrief() {
      const btn = document.getElementById('btn-gen');
      const out = document.getElementById('brief-output');
      const participant = document.getElementById('prep-part').value;
      const company = document.getElementById('prep-comp').value;
      const agenda = document.getElementById('prep-agenda').value;

      if (!participant || !company) {
        alert('Please provide participant and company.');
        return;
      }

      btn.disabled = true;
      btn.innerText = 'Analyzing...';
      out.className = 'status-msg';
      out.textContent = 'Recalling past interactions from Hindsight and synthesizing brief...';

      try {
        const res = await fetch('/api/get-brief', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({ participant, company, agenda })
        });
        const data = await res.json();
        out.className = '';
        if (data.brief) {
          out.innerHTML = marked.parse(data.brief);
        } else {
          out.textContent = data.message || 'Unable to generate brief.';
        }
      } catch (err) {
        out.textContent = 'Error: ' + err;
      } finally {
        btn.disabled = false;
        btn.innerText = 'Generate Executive Brief';
      }
    }
  </script>
</body>
</html>
"""

# Models
class MeetingSaveRequest(BaseModel):
    participant: str
    company: str
    notes: str

class MeetingBriefRequest(BaseModel):
    participant: str
    company: str
    agenda: str

# Endpoints handling root and /api prefixes
@app.get("/", response_class=HTMLResponse)
@app.get("/api", response_class=HTMLResponse)
@app.get("/api/", response_class=HTMLResponse)
def read_root():
    return HTMLResponse(content=HTML_CONTENT)

@app.post("/save-meeting")
@app.post("/api/save-meeting")
def save_meeting(data: MeetingSaveRequest):
    try:
        content = f"Meeting with {data.participant} from {data.company}: {data.notes}"
        hindsight_client.retain(
            bank_id=BANK_ID,
            content=content,
            context=f"Participant: {data.participant}, Company: {data.company}"
        )
        return {"status": "success", "message": f"Successfully retained memory for {data.participant} ({data.company})"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/get-brief")
@app.post("/api/get-brief")
def get_brief(data: MeetingBriefRequest):
    try:
        query = f"Meeting history, past decisions, open items, and commitments with {data.participant} at {data.company}"
        recall_res = hindsight_client.recall(bank_id=BANK_ID, query=query)
        
        memories = ""
        if hasattr(recall_res, 'memories') and recall_res.memories:
            memories = "\n".join([f"- {m.content}" for m in recall_res.memories])
        elif isinstance(recall_res, list):
            memories = "\n".join([f"- {str(item)}" for item in recall_res])
        else:
            memories = str(recall_res)

        prompt = f"""
You are an executive meeting preparation assistant. Prepare an actionable executive brief for an upcoming meeting.

Participant: {data.participant}
Company: {data.company}
Upcoming Agenda: {data.agenda}

Past Context & Memory (from Hindsight):
{memories}

Please format the brief with:
1. Executive Summary of past relationship & key points
2. Critical Risks / Open Commitments to watch out for
3. Recommended Discussion Points & Next Steps
"""
        completion = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="openai/gpt-oss-120b"
        )
        brief_text = completion.choices[0].message.content
        return {"status": "success", "brief": brief_text}
    except Exception as e:
        return {"status": "error", "message": str(e)}