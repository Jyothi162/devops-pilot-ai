
from agents.graph import graph


def main():
    print("\n===== DEVOPS PILOT AI =====")

    initial_state = {
        "user_request": "Why is my worker service failing?",
        "service_name": "worker",
        "investigation_plan": "",
        "infrastructure_result": {},
        "log_result": {},
        "diagnosis": "",
        "remediation": "",
        "approved": False,
        "final_response": "",
    }

    print("\nStarting multi-agent investigation...")

    result = graph.invoke(initial_state)

    print("\n===== SUPERVISOR PLAN =====")
    print(result["investigation_plan"])

    print("\n===== INFRASTRUCTURE HEALTH =====")
    print(result["infrastructure_result"])

    print("\n===== APPLICATION LOGS =====")
    print(result["log_result"])

    print("\n===== DIAGNOSIS =====")
    print(result["diagnosis"])

    print("\n===== REMEDIATION RECOMMENDATIONS =====")
    print(result["remediation"])

    print("\n===== INVESTIGATION COMPLETED =====")


if __name__ == "__main__":
    main()
