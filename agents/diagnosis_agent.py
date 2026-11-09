
import json

from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

from agents.state import DevOpsState


llm = ChatOllama(
    model="llama3.2",
    temperature=0,
)


def diagnosis_agent(state: DevOpsState) -> dict:
    """
    Diagnosis Agent:
    Analyzes infrastructure health and log evidence.
    """

    service_name = state["service_name"]

    infrastructure = state["infrastructure_result"]
    logs = state["log_result"]

    system_prompt = """
    You are a DevOps Diagnosis Agent.

    Your responsibility is to identify likely causes
    of application or infrastructure failures.

    Analyze only the supplied health-check results
    and application logs.

    Instructions:
    1. Summarize the observed service status.
    2. Identify the most relevant errors.
    3. Explain the most likely root cause.
    4. Distinguish observations from hypotheses.
    5. State what additional evidence is needed
       to confirm the root cause.

    Do not invent monitoring results or tool outputs.
    Do not claim to have executed commands.
    Do not perform remediation.
    """

    evidence = {
        "service_name": service_name,
        "infrastructure": infrastructure,
        "logs": logs,
    }

    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(
            content=json.dumps(evidence, indent=2)
        ),
    ])

    return {
        "diagnosis": str(response.content)
    }
