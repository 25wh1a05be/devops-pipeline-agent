import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

# Load environment variables from .env
load_dotenv(override=True)

# Initialize Hindsight Client
client = Hindsight(
    base_url=os.getenv("HINDSIGHT_API_URL"),
    api_key=os.getenv("HINDSIGHT_API_TOKEN")
)
bank_id = os.getenv("HINDSIGHT_BANK_ID")

def learn_new_incident(incident_summary):
    """Saves a new incident and its fix back into Hindsight memory."""
    print(f"\n🧠 Saving new resolution to Hindsight bank '{bank_id}'...")
    try:
        client.retain(
            bank_id=bank_id,
            content=incident_summary
        )
        print("✅ Success! The agent will now remember this resolution for future errors.")
    except Exception as e:
        print(f"❌ Failed to save memory: {e}")

def diagnose_and_suggest_fix(new_log_error):
    """Queries Hindsight for historical incidents matching the error log."""
    print(f"\n🚨 New Pipeline Error Detected:\n{new_log_error}\n")
    
    # 1. Recall related incidents from Hindsight
    results = client.recall(
        bank_id=bank_id,
        query=new_log_error
    )
    
    past_contexts = []
    for memory in results.results:
        text_content = getattr(memory, 'text', getattr(memory, 'document', str(memory)))
        past_contexts.append(text_content)
    
    # 2. Display matched historical memories
    print("🤖 Agent Diagnosis & Resolution Strategy:")
    print("=" * 60)
    print("Matched Historical Incidents:")
    if past_contexts:
        for idx, ctx in enumerate(past_contexts[:3], 1):
            print(f"  {idx}. {ctx}")
    else:
        print("  (No relevant historical memories found)")
        
    # 3. Rule-based remediation suggestions
    print("\nRecommended Immediate Fix:")
    if "OOMKilled" in new_log_error or "137" in new_log_error:
        print(" -> Update memory limits in your `deployment.yaml` or container definition (e.g., from 512Mi to 1Gi).")
    elif "ENOSPC" in new_log_error or "watchers" in new_log_error:
        print(" -> Increase `fs.inotify.max_user_watches` on the runner node.")
    elif "Postgres" in new_log_error or "connection pool" in new_log_error:
        print(" -> Increase `max_connections` in your database configuration.")
    else:
        print(" -> Check log stack trace against historical incidents listed above.")
    print("=" * 60)

if __name__ == "__main__":
    print("🤖 DevOps Memory Agent Ready!")
    print("Commands:")
    print("  • Paste an error log to diagnose")
    print("  • Type 'learn' to store a new incident fix into Hindsight")
    print("  • Type 'exit' to quit\n")
    
    while True:
        try:
            user_input = input("\nPaste Error Log or Command > ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ['exit', 'quit']:
                print("\nShutting down DevOps Agent. Goodbye!")
                break
                
            elif user_input.lower() == 'learn':
                print("\n--- Teach New Incident Resolution ---")
                incident_details = input("Enter Incident & Fix Summary: ").strip()
                if incident_details:
                    learn_new_incident(incident_details)
                else:
                    print("⚠️ Cannot save empty resolution.")
            else:
                diagnose_and_suggest_fix(user_input)
                
        except KeyboardInterrupt:
            print("\nExiting agent...")
            break

    # Cleanly close the Hindsight client session
    client.close()