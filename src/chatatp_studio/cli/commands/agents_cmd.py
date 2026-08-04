"""`studio agents` -- agent CRUD and preview chat."""
from __future__ import annotations

import click

from .. import ui
from ..crud import build_crud_group, handle_errors

_COLUMNS = ["id", "name", "status", "description", "team_id", "updated_at"]

agents = build_crud_group(
    "agents",
    service_getter=lambda ctx: ctx.obj.agents,
    columns=_COLUMNS,
    id_type=int,
)


@agents.command("preview")
@click.argument("agent_id", type=int)
@click.option("--message", "-m", required=True, help="Message to send to the agent.")
@click.pass_context
@handle_errors
def preview(ctx: click.Context, agent_id: int, message: str) -> None:
    """Send a one-off preview message to an agent and print the reply."""
    cli_ctx = ctx.obj
    with ui.spinner("Waiting for agent reply..."):
        result = cli_ctx.agents.preview(agent_id, message)
    if isinstance(result, dict) and "reply" in result:
        reply = result["reply"]
        content = reply.get("content") if isinstance(reply, dict) else reply
        ui.print_panel("Agent reply", str(content))
        if result.get("tool_calls"):
            ui.render(result["tool_calls"], output_format=cli_ctx.output_format, title="Tool calls")
    else:
        ui.render(result, output_format=cli_ctx.output_format)
