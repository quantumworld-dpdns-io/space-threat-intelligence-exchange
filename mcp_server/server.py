from __future__ import annotations

import json
import logging
from typing import Any

from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types

from stie.storage.qdrant_client import get_qdrant
from stie.config.settings import settings

logger = logging.getLogger("stie.mcp")

server = Server("stie-threat-intel")


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="search_threats",
            description="Search threat reports by text query",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "limit": {"type": "integer", "description": "Max results", "default": 10},
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="get_threat_report",
            description="Get a threat report by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "report_id": {"type": "string", "description": "Report ID"},
                },
                "required": ["report_id"],
            },
        ),
        types.Tool(
            name="get_threat_summary",
            description="Get summary statistics of threats",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        types.Tool(
            name="enrich_threat",
            description="Enrich a threat report using AI analysis",
            inputSchema={
                "type": "object",
                "properties": {
                    "report_id": {"type": "string", "description": "Report ID to enrich"},
                },
                "required": ["report_id"],
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict[str, Any] | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    if not arguments:
        arguments = {}

    if name == "search_threats":
        query = arguments.get("query", "")
        limit = min(arguments.get("limit", 10), 50)

        qdrant = await get_qdrant()
        results = await qdrant.search(
            collection_name=settings.qdrant_collection,
            query_vector=[0.0] * settings.ai_embedding_dimension,
            limit=limit,
        )
        return [types.TextContent(type="text", text=json.dumps([
            {"id": r.id, "score": r.score} for r in results
        ], indent=2))]

    elif name == "get_threat_summary":
        return [types.TextContent(type="text", text=json.dumps({
            "status": "operational",
            "version": settings.app_version,
            "vector_db": settings.qdrant_url,
            "llm_provider": settings.ai_llm_provider,
        }, indent=2))]

    elif name == "get_threat_report":
        return [types.TextContent(
            type="text",
            text=json.dumps({"error": "Not yet implemented"}, indent=2),
        )]

    elif name == "enrich_threat":
        return [types.TextContent(
            type="text",
            text=json.dumps({"error": "Not yet implemented"}, indent=2),
        )]

    raise ValueError(f"Unknown tool: {name}")


async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="stie-threat-intel",
                server_version=settings.app_version,
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
