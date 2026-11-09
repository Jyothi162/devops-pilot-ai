
from langgraph.graph import StateGraph, START, END

from agents.state import DevOpsState
from agents.supervisor import supervisor_agent
from agents.infrastructure_agent import infrastructure_agent
from agents.log_agent import log_agent
from agents.diagnosis_agent import diagnosis_agent
from agents.remediation_agent import remediation_agent


def route_supervisor(state: DevOpsState) -> str:
    """
    Read the Supervisor Agent's routing decision.
    """

    next_agent = state["next_agent"]

    if next_agent not in ("infrastructure", "logs"):
        raise ValueError(
            f"Invalid supervisor routing decision: {next_agent}"
        )

    return next_agent


def route_after_infrastructure(state: DevOpsState) -> str:
    """
    If logs have not been collected, collect them.
    Otherwise proceed to diagnosis.
    """

    if not state.get("log_result"):
        return "logs"

    return "diagnosis"


def route_after_logs(state: DevOpsState) -> str:
    """
    If infrastructure health has not been checked,
    check it. Otherwise proceed to diagnosis.
    """

    if not state.get("infrastructure_result"):
        return "infrastructure"

    return "diagnosis"


def build_graph():
    """
    Build the Supervisor-routed DevOps workflow.
    """

    workflow = StateGraph(DevOpsState)

    # Register agent components
    workflow.add_node("supervisor", supervisor_agent)
    workflow.add_node("infrastructure", infrastructure_agent)
    workflow.add_node("logs", log_agent)
    workflow.add_node("diagnosis", diagnosis_agent)
    workflow.add_node("remediation", remediation_agent)

    # Start with the Supervisor
    workflow.add_edge(START, "supervisor")

    # Supervisor chooses the first specialist
    workflow.add_conditional_edges(
        "supervisor",
        route_supervisor,
        {
            "infrastructure": "infrastructure",
            "logs": "logs",
        },
    )

    # Ensure both types of evidence are collected
    workflow.add_conditional_edges(
        "infrastructure",
        route_after_infrastructure,
        {
            "logs": "logs",
            "diagnosis": "diagnosis",
        },
    )

    workflow.add_conditional_edges(
        "logs",
        route_after_logs,
        {
            "infrastructure": "infrastructure",
            "diagnosis": "diagnosis",
        },
    )

    # Analyze evidence and recommend actions
    workflow.add_edge("diagnosis", "remediation")
    workflow.add_edge("remediation", END)

    return workflow.compile()


graph = build_graph()
