"""`studio http-api` -- HTTP API tools and connections."""
from __future__ import annotations

import click

from .. import ui
from ..crud import build_crud_group, handle_errors

_TOOL_COLUMNS = ["id", "slug", "name", "category", "method", "endpoint", "auth_type", "is_connected"]
_CONNECTION_COLUMNS = ["id", "tool_slug", "tool_name", "label", "enabled", "has_credentials", "last_error"]


@click.group("http-api")
def http_api() -> None:
    """HTTP API tools and connections."""


tools = build_crud_group(
    "tools",
    service_getter=lambda ctx: ctx.obj.http_api.tools,
    columns=_TOOL_COLUMNS,
    id_type=int,
)
connections = build_crud_group(
    "connections",
    service_getter=lambda ctx: ctx.obj.http_api.connections,
    columns=_CONNECTION_COLUMNS,
    id_type=int,
)

http_api.add_command(tools)
http_api.add_command(connections)


@connections.command("execute")
@click.argument("connection_id", type=int)
@click.option("--data", default=None, help="JSON body with variables/params/body, or @path/to/file.json.")
@click.pass_context
@handle_errors
def execute(ctx: click.Context, connection_id: int, data: str) -> None:
    """Execute an HTTP API tool connection."""
    cli_ctx = ctx.obj
    payload = ui.parse_json_option(data) or {}
    with ui.spinner("Executing..."):
        result = cli_ctx.http_api.execute(connection_id, payload)
    ui.render(result, output_format=cli_ctx.output_format)


@connections.command("oauth-initiate")
@click.argument("connection_id", type=int)
@click.pass_context
@handle_errors
def oauth_initiate(ctx: click.Context, connection_id: int) -> None:
    """Start the OAuth flow for an HTTP API connection and print the authorize URL."""
    cli_ctx = ctx.obj
    with ui.spinner("Starting OAuth flow..."):
        result = cli_ctx.http_api.oauth_initiate(connection_id)
    if isinstance(result, dict) and result.get("authorization_url"):
        ui.print_info(f"Open this URL to authorize: {result['authorization_url']}")
    ui.render(result, output_format=cli_ctx.output_format)
