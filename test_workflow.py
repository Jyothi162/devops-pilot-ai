
from agents.graph import graph

initial_state = {
    "user_request": (
        "Investigate why the worker service is unhealthy, "
        "check its logs, and recommend safe remediation steps."
    ),
    "service_name": "worker",
}

print("\nStarting DevOps Pilot AI investigation...\n")

try:
    result = graph.invoke(initial_state)

    print("\n===== INVESTIGATION PLAN =====")
    print(result.get("investigation_plan"))

    print("\n===== SUPERVISOR ROUTING =====")
    print(result.get("next_agent"))

    print("\n===== INFRASTRUCTURE RESULT =====")
    print(result.get("infrastructure_result"))

    print("\n===== LOG RESULT =====")
    print(result.get("log_result"))

    print("\n===== DIAGNOSIS =====")
    print(result.get("diagnosis"))

    print("\n===== REMEDIATION =====")
    print(result.get("remediation"))

    print("\nInvestigation completed successfully!")

except Exception as error:
    print(f"\nInvestigation failed: {error}")
    raise
