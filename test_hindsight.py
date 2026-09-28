import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

client = Hindsight(
    base_url=os.getenv("HINDSIGHT_API_URL"),
    api_key=os.getenv("HINDSIGHT_API_KEY"),
)

bank_id = os.getenv("HINDSIGHT_BANK_ID")

print("Testing Hindsight...")
print("Bank:", bank_id)

try:
    client.retain(
        bank_id=bank_id,
        content=(
            "Meeting with Rahul Sharma from Acme Technologies. "
            "Rahul wants to reduce AWS cloud costs. "
            "His main concern is migration downtime. "
            "He requested a proposal by next Friday."
        ),
    )
    print("✅ Meeting memory saved!")

    result = client.recall(
        bank_id=bank_id,
        query="What does Rahul Sharma from Acme Technologies care about, and what was discussed previously?"
    )

    print("\n=== RECALLED MEMORY ===")
    for memory in getattr(result, "results", []):
        print(getattr(memory, "text", memory))

except Exception as e:
    print("❌ Error during Hindsight test:", e)
