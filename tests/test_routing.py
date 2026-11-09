
import pytest

from agents.graph import (
    route_supervisor,
    route_after_infrastructure,
    route_after_logs,
)


def test_supervisor_routes_to_infrastructure():
    state = {"next_agent": "infrastructure"}

    assert route_supervisor(state) == "infrastructure"


def test_supervisor_routes_to_logs():
    state = {"next_agent": "logs"}

    assert route_supervisor(state) == "logs"


def test_supervisor_rejects_invalid_agent():
    state = {"next_agent": "unknown"}

    with pytest.raises(ValueError):
        route_supervisor(state)


def test_infrastructure_routes_to_logs():
    state = {"log_result": {}}

    assert route_after_infrastructure(state) == "logs"


def test_infrastructure_routes_to_diagnosis():
    state = {"log_result": {"logs": ["ERROR: timeout"]}}

    assert route_after_infrastructure(state) == "diagnosis"


def test_logs_routes_to_infrastructure():
    state = {"infrastructure_result": {}}

    assert route_after_logs(state) == "infrastructure"


def test_logs_routes_to_diagnosis():
    state = {
        "infrastructure_result": {
            "service": "worker",
            "status": "unhealthy",
        }
    }

    assert route_after_logs(state) == "diagnosis"
