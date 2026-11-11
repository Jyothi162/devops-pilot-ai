
from agents.log_agent import log_agent


def main():
    state = {
        "user_request": "Investigate why the worker service is unhealthy.",
        "service_name": "worker",
        "investigation_plan": "",
        "next_agent": "",
        "infrastructure_result": {},
        "log_result": {},
        "diagnosis": "",
        "remediation": "",
        "approved": False,
        "final_response": "",
    }

    result = log_agent(state)

    print("\n===== LOG AGENT RESULT =====")
    print(result)


if __name__ == "__main__":
    main()
