
import asyncio
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    # Configure the MCP server
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "mcp_server.server"],
    )

    # Connect to the MCP server
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:

            # Initialize the MCP connection
            await session.initialize()

            # Discover available MCP tools
            tools = await session.list_tools()

            print("Available MCP tools:")
            for tool in tools.tools:
                print(f"- {tool.name}")

            # --------------------------------
            # Tool 1: Check service health
            # --------------------------------
            health_result = await session.call_tool(
                "check_service_health",
                arguments={"service_name": "worker"},
            )

            print("\nHealth check result:")
            for content in health_result.content:
                if content.type == "text":
                    print(content.text)

            # --------------------------------
            # Tool 2: Get service logs
            # --------------------------------
            log_result = await session.call_tool(
                "get_service_logs",
                arguments={"service_name": "worker"},
            )

            print("\nWorker service logs:")
            for content in log_result.content:
                if content.type == "text":
                    print(content.text)


if __name__ == "__main__":
    asyncio.run(main())
