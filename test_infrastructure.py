
from agents.infrastructure_agent import infrastructure_agent


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

    result = infrastructure_agent(state)
    print(result)


if __name__ == "__main__":
    main()
