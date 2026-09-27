import os
from dotenv import load_dotenv
from groq import Groq
from hindsight_client import Hindsight

load_dotenv()

# Initialize Clients with variable names from your .env file
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

hindsight_client = Hindsight(
    base_url=os.getenv("HINDSIGHT_API_URL"),
    api_key=os.getenv("HINDSIGHT_API_KEY"),
)
BANK_ID = os.getenv("HINDSIGHT_BANK_ID")


def save_meeting_memory(participant: str, company: str, notes: str) -> dict:
    """Store meeting notes into Hindsight memory bank."""
    content = f"Meeting with {participant} from {company}. Details: {notes}"
    try:
        hindsight_client.retain(bank_id=BANK_ID, content=content)
        return {"status": "success", "message": f"Saved memory for {participant} ({company})"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def generate_meeting_brief(participant: str, company: str, agenda: str) -> dict:
    """Recall past context from Hindsight and synthesize a brief with Groq."""
    search_query = f"Past meetings, commitments, concerns, or context regarding {participant} from {company}"
    
    try:
        recall_response = hindsight_client.recall(bank_id=BANK_ID, query=search_query)
        memories = [
            getattr(m, "text", str(m)) 
            for m in getattr(recall_response, "results", [])
        ]
        context_str = "\n".join(memories) if memories else "No previous meeting memory found."
    except Exception as e:
        context_str = f"Error retrieving memories: {str(e)}"

    prompt = f"""You are an executive meeting assistant. Prepare a high-signal, concise meeting brief.

### Upcoming Meeting Details:
- Participant: {participant}
- Company: {company}
- Agenda: {agenda}

### Recalled Historical Context:
{context_str}

### Instructions:
Provide:
1. Executive Summary of Past Relationship & Key Points
2. Critical Risks / Open Commitments to Address
3. Recommended Discussion Points & Next Steps
"""

    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="openai/gpt-oss-120b",
        )
        brief = chat_completion.choices[0].message.content
        return {"status": "success", "brief": brief, "memories_used": context_str}
    except Exception as e:
        return {"status": "error", "message": str(e)}