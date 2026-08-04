"""`studio platforms` -- messaging platform catalog and configs."""
from __future__ import annotations

import click

from .. import ui
from ..crud import build_crud_group, handle_errors

_CONFIG_COLUMNS = ["id", "platform_slug", "platform_name", "label", "status", "created_at"]


@click.group()
def platforms() -> None:
    """Messaging platform catalog and connected configs."""


@platforms.group()
def catalog() -> None:
    """Browse the platform catalog (Discord, Slack, WhatsApp, ...)."""


@catalog.command("list")
@click.pass_context
@handle_errors
def catalog_list(ctx: click.Context) -> None:
    """List all available platforms."""
    cli_ctx = ctx.obj
    with ui.spinner("Fetching catalog..."):
        data = cli_ctx.platforms.list_catalog()
    ui.render(data, output_format=cli_ctx.output_format, columns=["id", "slug", "name", "type", "is_connected"])


@catalog.command("get")
@click.argument("platform_id", type=int)
@click.pass_context
@handle_errors
def catalog_get(ctx: click.Context, platform_id: int) -> None:
    """Get a single platform catalog entry."""
    cli_ctx = ctx.obj
    with ui.spinner("Fetching platform..."):
        data = cli_ctx.platforms.get_catalog_entry(platform_id)
    ui.render(data, output_format=cli_ctx.output_format)


configs = build_crud_group(
    "configs",
    service_getter=lambda ctx: ctx.obj.platforms.configs,
    columns=_CONFIG_COLUMNS,
    id_type=int,
)
platforms.add_command(configs)


@platforms.command("connect")
@click.option("--platform", "platform_id", type=int, required=True, help="Platform id from the catalog.")
@click.option("--credentials", required=True, help="JSON credentials payload, or @path/to/file.json.")
@click.pass_context
@handle_errors
def connect(ctx: click.Context, platform_id: int, credentials: str) -> None:
    """Connect a messaging platform with credentials."""
    cli_ctx = ctx.obj
    creds = ui.parse_json_option(credentials) or {}
    with ui.spinner("Connecting..."):
        result = cli_ctx.platforms.connect(platform_id, creds)
    ui.print_success("Platform connected.")
    ui.render(result, output_format=cli_ctx.output_format)


@platforms.command("disconnect")
@click.option("--platform", "platform_id", type=int, required=True, help="Platform id from the catalog.")
@click.option("--yes", "-y", is_flag=True)
@click.pass_context
@handle_errors
def disconnect(ctx: click.Context, platform_id: int, yes: bool) -> None:
    """Disconnect a messaging platform."""
    cli_ctx = ctx.obj
    if not yes and not ui.confirm(f"Disconnect platform {platform_id}?"):
        ui.print_info("Cancelled.")
        return
    with ui.spinner("Disconnecting..."):
        cli_ctx.platforms.disconnect(platform_id)
    ui.print_success("Platform disconnected.")
