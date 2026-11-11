
from typing import Any, TypedDict


class DevOpsState(TypedDict):
    # Incident information
    user_request: str
    service_name: str

    # Supervisor routing
    investigation_plan: str
    next_agent: str

    # MCP evidence
    infrastructure_result: dict[str, Any]
    log_result: dict[str, Any]

    # AI analysis
    diagnosis: str
    remediation: str

    # Human approval and final output
    approved: bool
    final_response: str
