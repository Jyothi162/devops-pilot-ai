
import asyncio
import json
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def discover_mcp_tools() -> list[dict]:
    """
    Discover tools exposed by our MCP server.
    """

    server_params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "mcp_server.server"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            response = await session.list_tools()

            return [
                {
                    "name": tool.name,
                    "description": tool.description or "",
                    "input_schema": tool.inputSchema,
                }
                for tool in response.tools
            ]


async def execute_mcp_tool(
    tool_name: str,
    arguments: dict,
) -> dict:
    """
    Execute an explicitly allowed MCP tool.
    """

    allowed_tools = {
    "check_service_health",
    "get_service_logs",
    "get_service_metrics",
}

    if tool_name not in allowed_tools:
        raise ValueError(
            f"MCP tool is not allowed: {tool_name}"
        )

    server_params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "mcp_server.server"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            result = await session.call_tool(
                tool_name,
                arguments=arguments,
            )

            if result.isError:
                raise RuntimeError(
                    f"MCP tool failed: {tool_name}"
                )

            if result.structuredContent is not None:
                return result.structuredContent

            for content in result.content:
                if content.type == "text":
                    return json.loads(content.text)

    raise RuntimeError(
        f"MCP tool returned no data: {tool_name}"
    )


def list_available_tools() -> list[dict]:
    return asyncio.run(discover_mcp_tools())


def run_mcp_tool(
    tool_name: str,
    arguments: dict,
) -> dict:
    return asyncio.run(
        execute_mcp_tool(tool_name, arguments)
    )
