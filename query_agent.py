import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv(override=True)

client = Hindsight(
    base_url=os.getenv("HINDSIGHT_API_URL"),
    api_key=os.getenv("HINDSIGHT_API_TOKEN")
)
bank_id = os.getenv("HINDSIGHT_BANK_ID")

def analyze_issue(query_text):
    print(f"\n🔍 Querying Hindsight memory bank for: '{query_text}'")
    
    results = client.recall(
        bank_id=bank_id,
        query=query_text
    )
    
    print("\n💡 Relevant Past Incidents & Solutions Found:")
    for memory in results.results:
        # Access text attribute or fallback to string representation
        text_content = getattr(memory, 'text', getattr(memory, 'document', str(memory)))
        print(f"- {text_content}")

if __name__ == "__main__":
    analyze_issue("Docker build memory limit error OOM")
    client.close()