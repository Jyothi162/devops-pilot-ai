import os

from typing import Literal

from pydantic import BaseModel, Field
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

from agents.state import DevOpsState
from mcp_client.tool_executor import (
    list_available_tools,
    run_mcp_tool,
)


class InfrastructureToolDecision(BaseModel):
    tool_name: Literal[
        "check_service_health",
        "get_service_metrics",
    ] = Field(
        description="Selected infrastructure MCP tool"
    )
    reason: str = Field(
        description="Reason for selecting the tool"
    )


llm = ChatOllama(
    model="llama3.2",
    temperature=0,
    base_url=os.getenv(
        "OLLAMA_BASE_URL",
        "http://localhost:11434"
    ),
)

tool_selector = llm.with_structured_output(
    InfrastructureToolDecision,
    method="json_schema",
)


def infrastructure_agent(state: DevOpsState) -> dict:
    """
    Select and execute an infrastructure MCP tool.
    """

    service_name = state["service_name"]
    user_request = state["user_request"]

    available_tools = list_available_tools()

    # Tools this specialist is authorized to use
    permitted_names = {
        "check_service_health",
        "get_service_metrics",
    }

    permitted_tools = [
        tool for tool in available_tools
        if tool["name"] in permitted_names
    ]

    if not permitted_tools:
        raise RuntimeError(
            "No infrastructure MCP tools available"
        )

    decision = tool_selector.invoke([
        SystemMessage(
            content=(
                "You are a DevOps Infrastructure Agent. "
                "Choose exactly one tool from the available "
                "permitted MCP tools. "
                "For service health or availability, choose "
                "check_service_health. "
                "For CPU, memory, or resource utilization, "
                "choose get_service_metrics. "
                "Do not invent tools or execute commands."
            )
        ),
        HumanMessage(
            content=(
                f"User request: {user_request}\n"
                f"Service: {service_name}\n"
                f"Available tools: {permitted_tools}"
            )
        ),
    ])

    # Validate the LLM decision
    available_names = {
        tool["name"] for tool in permitted_tools
    }

    if decision.tool_name not in available_names:
        raise ValueError(
            f"Tool not permitted: {decision.tool_name}"
        )

    # Execute the selected MCP tool
    result = run_mcp_tool(
        tool_name=decision.tool_name,
        arguments={"service_name": service_name},
    )

    return {
        "infrastructure_result": result
    }

