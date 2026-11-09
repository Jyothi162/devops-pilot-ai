
from typing import Any, TypedDict


class DevOpsState(TypedDict):
    user_request: str
    service_name: str

    investigation_plan: str
    next_agent: str

    infrastructure_result: dict[str, Any]
    log_result: dict[str, Any]

    diagnosis: str
    remediation: str

    approved: bool
    final_response: str
