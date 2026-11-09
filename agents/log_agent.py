
from typing import Literal

from pydantic import BaseModel, Field
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

from agents.state import DevOpsState
from mcp_client.tool_executor import (
    list_available_tools,
    run_mcp_tool,
)


class LogToolDecision(BaseModel):
    tool_name: Literal["get_service_logs"] = Field(
        description="MCP tool selected for retrieving service logs"
    )
    reason: str = Field(
        description="Why this tool was selected"
    )


llm = ChatOllama(
    model="llama3.2",
    temperature=0,
)

tool_selector = llm.with_structured_output(
    LogToolDecision,
    method="json_schema",
)


def log_agent(state: DevOpsState) -> dict:
    """
    Log Analysis Agent:
    Discovers MCP tools, selects a permitted tool
    using Llama 3.2, and retrieves service logs.
    """

    service_name = state["service_name"]
    user_request = state["user_request"]

    # Discover available MCP tools
    available_tools = list_available_tools()

    # Restrict tools to the Log Analysis Agent
    permitted_tools = [
        tool for tool in available_tools
        if tool["name"] == "get_service_logs"
    ]

    if not permitted_tools:
        raise RuntimeError(
            "No permitted log analysis MCP tools available"
        )

    # Ask Llama 3.2 to select the tool
    decision = tool_selector.invoke([
        SystemMessage(
            content=(
                "You are a DevOps Log Analysis Agent. "
                "Select the appropriate MCP tool for "
                "retrieving application logs. "
                "Choose only from the permitted tools. "
                "Do not invent tools."
            )
        ),
        HumanMessage(
            content=(
                f"User request: {user_request}\n"
                f"Service: {service_name}\n"
                f"Permitted tools: {permitted_tools}"
            )
        ),
    ])

    # Validate tool permissions
    allowed_names = {
        tool["name"] for tool in permitted_tools
    }

    if decision.tool_name not in allowed_names:
        raise ValueError(
            f"Tool not permitted: {decision.tool_name}"
        )

    # Execute the selected MCP tool
    result = run_mcp_tool(
        tool_name=decision.tool_name,
        arguments={"service_name": service_name},
    )

    return {
        "log_result": result
    }
