import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv(override=True)

api_token = os.getenv("HINDSIGHT_API_TOKEN")
api_url = os.getenv("HINDSIGHT_API_URL")
bank_id = os.getenv("HINDSIGHT_BANK_ID")

client = Hindsight(
    base_url=api_url,
    api_key=api_token
)

# Step A: Ensure bank is created on Hindsight
print(f"Ensuring bank '{bank_id}' exists...")
try:
    client.create_bank(bank_id=bank_id)
    print("Bank ready!")
except Exception as e:
    print(f"Bank creation response: {e}")

# Step B: Retain memories
past_incidents = [
    "INCIDENT #101: Docker build for auth-service failed with Exit Code 137 (OOMKilled). Resolution: Increased memory limit in deployment.yaml from 512Mi to 1Gi.",
    "INCIDENT #102: Staging deployment timed out during database migration step. Root Cause: Postgres connection pool reached maximum limit of 20 connections. Resolution: Increased max_connections to 50 in staging config.",
    "INCIDENT #103: CI pipeline failed on 'npm run build' step with error 'ENOSPC: System limit for number of file watchers reached'. Resolution: Increased fs.inotify.max_user_watches on CI runner."
]

print("\nStoring DevOps incident memories into Hindsight...")

for incident in past_incidents:
    client.retain(
        bank_id=bank_id,
        content=incident
    )

print("✅ Memory seeding complete!")
client.close()