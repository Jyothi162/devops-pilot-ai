
from typing import Literal

from pydantic import BaseModel, Field
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

from agents.state import DevOpsState


# Define the allowed routing decisions
class SupervisorDecision(BaseModel):
    next_agent: Literal["infrastructure", "logs"] = Field(
        description="The specialist agent to call first"
    )
    investigation_plan: str = Field(
        description="A short investigation plan"
    )


llm = ChatOllama(
    model="llama3.2",
    temperature=0,
)

# Request structured output from Ollama
router_llm = llm.with_structured_output(
    SupervisorDecision,
    method="json_schema",
)


def supervisor_agent(state: DevOpsState) -> dict:
    """
    Supervisor Agent:
    Analyzes the user's request and chooses
    the first specialist agent.
    """

    user_request = state["user_request"]
    service_name = state["service_name"]

    system_prompt = """
    You are the Supervisor Agent of DevOps Pilot AI.

    Available specialists:

    1. infrastructure:
       Checks service health through an MCP tool.

    2. logs:
       Retrieves application logs through an MCP tool.

    Choose the most appropriate specialist to call first.

    Routing rules:
    - For service health, failures, or outages,
      choose infrastructure.
    - For requests primarily about logs or errors
      in logs, choose logs.
    - For unclear requests, choose infrastructure.

    Create a short investigation plan using only
    the capabilities available above.

    Do not claim any tools have been executed.
    Do not execute remediation.
    """

    decision = router_llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(
            content=(
                f"Service: {service_name}\n"
                f"User request: {user_request}"
            )
        ),
    ])

    return {
        "next_agent": decision.next_agent,
        "investigation_plan": decision.investigation_plan,
    }
