
from datetime import datetime, timezone

from mcp.server.fastmcp import FastMCP

# Create our MCP server
mcp = FastMCP("DevOps Pilot MCP Server")


@mcp.tool()
def check_service_health(service_name: str) -> dict:
    """
    Check the health of a simulated application service.
    """

    services = {
        "api": "healthy",
        "database": "healthy",
        "worker": "unhealthy",
    }

    status = services.get(service_name.lower())

    if status is None:
        return {
            "service": service_name,
            "status": "unknown",
            "message": "Service not found",
        }

    return {
        "service": service_name,
        "status": status,
        "checked_at": datetime.now(timezone.utc).isoformat(),
    }


@mcp.tool()
def get_service_logs(service_name: str) -> dict:
    """
    Retrieve simulated application logs for a service.
    """

    logs = {
        "api": [
            "INFO: API server started",
            "INFO: GET /health - 200 OK",
        ],
        "database": [
            "INFO: Database connection established",
            "INFO: Database is accepting connections",
        ],
        "worker": [
            "INFO: Worker service started",
            "ERROR: Database connection timeout",
            "ERROR: Worker failed to process job",
        ],
    }

    service = service_name.lower()

    if service not in logs:
        return {
            "service": service_name,
            "logs": [],
            "message": "Service not found",
        }

    return {
        "service": service,
        "logs": logs[service],
    }


@mcp.tool()
def get_service_metrics(service_name: str) -> dict:
    """
    Return simulated CPU and memory metrics
    for a service.
    """

    metrics = {
        "api": {
            "cpu_percent": 25,
            "memory_percent": 40,
        },
        "database": {
            "cpu_percent": 35,
            "memory_percent": 55,
        },
        "worker": {
            "cpu_percent": 92,
            "memory_percent": 87,
        },
    }

    service = service_name.lower()

    if service not in metrics:
        return {
            "service": service,
            "status": "unknown",
            "message": "Service not found",
        }

    return {
        "service": service,
        "metrics": metrics[service],
        "source": "simulated",
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")
