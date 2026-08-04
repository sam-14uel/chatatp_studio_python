"""`studio mcp` -- MCP servers and connections."""
from __future__ import annotations

import click

from .. import ui
from ..crud import build_crud_group, handle_errors

_SERVER_COLUMNS = ["id", "slug", "name", "category", "transport_type", "auth_type", "is_connected"]
_CONNECTION_COLUMNS = ["id", "server_slug", "server_name", "label", "enabled", "has_credentials", "last_error"]


@click.group()
def mcp() -> None:
    """MCP servers and connections."""


servers = build_crud_group(
    "servers",
    service_getter=lambda ctx: ctx.obj.mcp.servers,
    columns=_SERVER_COLUMNS,
    id_type=int,
)
connections = build_crud_group(
    "connections",
    service_getter=lambda ctx: ctx.obj.mcp.connections,
    columns=_CONNECTION_COLUMNS,
    id_type=int,
)

mcp.add_command(servers)
mcp.add_command(connections)


@connections.command("oauth-initiate")
@click.argument("connection_id", type=int)
@click.pass_context
@handle_errors
def oauth_initiate(ctx: click.Context, connection_id: int) -> None:
    """Start the OAuth flow for an MCP connection and print the authorize URL."""
    cli_ctx = ctx.obj
    with ui.spinner("Starting OAuth flow..."):
        result = cli_ctx.mcp.oauth_initiate(connection_id)
    if isinstance(result, dict) and result.get("authorization_url"):
        ui.print_info(f"Open this URL to authorize: {result['authorization_url']}")
    ui.render(result, output_format=cli_ctx.output_format)
