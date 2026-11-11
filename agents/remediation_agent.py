
from langchain_core.messages import HumanMessage, SystemMessage

from agents.llm_config import get_llm
from agents.state import DevOpsState


# Use the shared LLM configuration
llm = get_llm()


def remediation_agent(state: DevOpsState) -> dict:
    """
    Remediation Agent:
    Recommends safe corrective actions based
    on the Diagnosis Agent's findings.
    """

    diagnosis = state["diagnosis"]
    service_name = state["service_name"]

    system_prompt = """
    You are a DevOps Remediation Agent.

    Your responsibility is to recommend safe
    corrective actions for application and
    infrastructure incidents.

    Based only on the supplied diagnosis:

    1. Summarize the suspected problem.
    2. Recommend safe troubleshooting steps.
    3. Explain why each step is useful.
    4. Identify actions requiring human approval.
    5. Recommend how to verify recovery.

    Rules:
    - Do not execute any commands.
    - Do not claim that remediation has happened.
    - Do not invent diagnostic evidence.
    - Do not recommend destructive operations.
    - Require human approval before changes
      to services or infrastructure.
    """

    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(
            content=(
                f"Service: {service_name}\n\n"
                f"Diagnosis:\n{diagnosis}"
            )
        ),
    ])

    return {
        "remediation": str(response.content)
    }
