
from agents.supervisor import supervisor_agent


# Simulated user incident
state = {
    "user_request": "Why is my worker service failing?",
    "service_name": "worker",
}

# Run the Supervisor Agent
result = supervisor_agent(state)

print("\n===== SUPERVISOR AGENT =====")
print(result["investigation_plan"])
