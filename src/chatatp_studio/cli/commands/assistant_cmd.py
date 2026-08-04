"""`studio assistant` -- Copilot chat, config, sessions, events, analytics."""
from __future__ import annotations

import click

from .. import ui
from ..crud import handle_errors


@click.group()
def assistant() -> None:
    """AI Copilot: chat, sessions, and configuration."""


@assistant.command()
@click.option("--message", "-m", required=True, help="Message to send.")
@click.option("--session", "session_id", default=None, help="Existing session id to continue.")
@click.option("--stream", is_flag=True, help="Stream the reply via SSE instead of waiting for the full response.")
@click.pass_context
@handle_errors
def chat(ctx: click.Context, message: str, session_id: str, stream: bool) -> None:
    """Send a message to the Copilot assistant."""
    cli_ctx = ctx.obj
    if stream:
        _stream_chat(cli_ctx, message, session_id)
        return
    with ui.spinner("Thinking..."):
        result = cli_ctx.assistant.chat([{"role": "user", "content": message}], session_id=session_id)
    if isinstance(result, dict) and "reply" in result:
        ui.print_panel(f"Assistant ({result.get('model', '')})", str(result["reply"]))
        if result.get("tool_calls"):
            ui.render(result["tool_calls"], output_format=cli_ctx.output_format, title="Tool calls")
    else:
        ui.render(result, output_format=cli_ctx.output_format)


def _stream_chat(cli_ctx, message: str, session_id: str) -> None:
    """Stream `/dapi/assistant/chat/stream/` and print text deltas as they arrive."""
    import json as jsonlib

    from .. import endpoints

    payload = {"messages": [{"role": "user", "content": message}]}
    if session_id:
        payload["session_id"] = session_id

    client = cli_ctx.client
    url = client._url(endpoints.ASSISTANT_CHAT_STREAM)
    headers = client._headers({"Content-Type": "application/json", "Accept": "text/event-stream"})
    with client.session.post(url, headers=headers, json=payload, stream=True, timeout=client.timeout) as resp:
        if not resp.ok:
            client._handle_response(resp)
            return
        for raw_line in resp.iter_lines(decode_unicode=True):
            if not raw_line or not raw_line.startswith("data:"):
                continue
            data = raw_line[len("data:") :].strip()
            if not data or data == "[DONE]":
                continue
            try:
                event = jsonlib.loads(data)
            except jsonlib.JSONDecodeError:
                continue
            event_type = event.get("type")
            if event_type == "assistant_text.delta":
                ui.console.print(event.get("delta", ""), end="")
            elif event_type == "tool_call.started":
                ui.console.print()
                ui.print_info(f"Tool call started: {event.get('name')}")
            elif event_type == "error":
                ui.console.print()
                ui.print_error(str(event.get("message", event)))
        ui.console.print()


@assistant.group()
def config() -> None:
    """Copilot configuration (model, temperature, prompt, ...)."""


@config.command("get")
@click.pass_context
@handle_errors
def config_get(ctx: click.Context) -> None:
    """Show the current Copilot configuration."""
    cli_ctx = ctx.obj
    with ui.spinner("Fetching config..."):
        result = cli_ctx.assistant.get_config()
    ui.render(result, output_format=cli_ctx.output_format)


@config.command("update")
@click.option("--data", required=True, help="JSON payload, or @path/to/file.json.")
@click.pass_context
@handle_errors
def config_update(ctx: click.Context, data: str) -> None:
    """Update the Copilot configuration."""
    cli_ctx = ctx.obj
    payload = ui.parse_json_option(data) or {}
    with ui.spinner("Updating config..."):
        result = cli_ctx.assistant.update_config(**payload)
    ui.print_success("Configuration updated.")
    ui.render(result, output_format=cli_ctx.output_format)


@assistant.group()
def sessions() -> None:
    """Copilot chat sessions."""


@sessions.command("list")
@click.pass_context
@handle_errors
def sessions_list(ctx: click.Context) -> None:
    """List Copilot sessions."""
    cli_ctx = ctx.obj
    with ui.spinner("Fetching sessions..."):
        data = cli_ctx.assistant.list_sessions()
    ui.render(data, output_format=cli_ctx.output_format, columns=["id", "title", "state", "updated_at"])


@sessions.command("create")
@click.option("--title", default=None)
@click.pass_context
@handle_errors
def sessions_create(ctx: click.Context, title: str) -> None:
    """Create a new Copilot session."""
    cli_ctx = ctx.obj
    with ui.spinner("Creating session..."):
        result = cli_ctx.assistant.create_session(title)
    ui.print_success("Session created.")
    ui.render(result, output_format=cli_ctx.output_format)


@sessions.command("get")
@click.argument("session_id")
@click.pass_context
@handle_errors
def sessions_get(ctx: click.Context, session_id: str) -> None:
    """Get a Copilot session by id."""
    cli_ctx = ctx.obj
    with ui.spinner("Fetching session..."):
        result = cli_ctx.assistant.get_session(session_id)
    ui.render(result, output_format=cli_ctx.output_format)


@sessions.command("rename")
@click.argument("session_id")
@click.option("--title", required=True)
@click.pass_context
@handle_errors
def sessions_rename(ctx: click.Context, session_id: str, title: str) -> None:
    """Rename a Copilot session."""
    cli_ctx = ctx.obj
    with ui.spinner("Updating session..."):
        result = cli_ctx.assistant.update_session(session_id, title)
    ui.print_success("Session updated.")
    ui.render(result, output_format=cli_ctx.output_format)


@sessions.command("delete")
@click.argument("session_id")
@click.option("--yes", "-y", is_flag=True)
@click.pass_context
@handle_errors
def sessions_delete(ctx: click.Context, session_id: str, yes: bool) -> None:
    """Delete a Copilot session."""
    cli_ctx = ctx.obj
    if not yes and not ui.confirm(f"Delete session {session_id}?"):
        ui.print_info("Cancelled.")
        return
    with ui.spinner("Deleting session..."):
        cli_ctx.assistant.delete_session(session_id)
    ui.print_success("Session deleted.")


@sessions.command("state")
@click.argument("session_id")
@click.pass_context
@handle_errors
def sessions_state(ctx: click.Context, session_id: str) -> None:
    """Show a session's current state."""
    cli_ctx = ctx.obj
    with ui.spinner("Fetching state..."):
        result = cli_ctx.assistant.session_state(session_id)
    ui.render(result, output_format=cli_ctx.output_format)


@sessions.command("stop")
@click.argument("session_id")
@click.pass_context
@handle_errors
def sessions_stop(ctx: click.Context, session_id: str) -> None:
    """Stop an in-progress session."""
    cli_ctx = ctx.obj
    with ui.spinner("Stopping session..."):
        cli_ctx.assistant.stop_session(session_id)
    ui.print_success("Session stopped.")


@sessions.command("retry")
@click.argument("session_id")
@click.option("--from-event", "from_event_id", type=int, required=True)
@click.pass_context
@handle_errors
def sessions_retry(ctx: click.Context, session_id: str, from_event_id: int) -> None:
    """Retry a session from a given event id."""
    cli_ctx = ctx.obj
    with ui.spinner("Retrying..."):
        result = cli_ctx.assistant.retry_session(session_id, from_event_id)
    ui.render(result, output_format=cli_ctx.output_format)


@sessions.group("events")
def events() -> None:
    """Session event history."""


@events.command("list")
@click.argument("session_id")
@click.pass_context
@handle_errors
def events_list(ctx: click.Context, session_id: str) -> None:
    """List events for a session."""
    cli_ctx = ctx.obj
    with ui.spinner("Fetching events..."):
        data = cli_ctx.assistant.list_events(session_id)
    ui.render(data, output_format=cli_ctx.output_format, columns=["id", "sequence_number", "event_type", "created_at"])


@events.command("edit")
@click.argument("session_id")
@click.argument("event_id", type=int)
@click.option("--content", required=True)
@click.pass_context
@handle_errors
def events_edit(ctx: click.Context, session_id: str, event_id: int, content: str) -> None:
    """Edit the text content of a session event."""
    cli_ctx = ctx.obj
    with ui.spinner("Updating event..."):
        result = cli_ctx.assistant.edit_event(session_id, event_id, content)
    ui.print_success("Event updated.")
    ui.render(result, output_format=cli_ctx.output_format)


@events.command("regenerate")
@click.argument("session_id")
@click.argument("event_id", type=int)
@click.option("--prompt", default=None, help="Optional rewrite instruction.")
@click.pass_context
@handle_errors
def events_regenerate(ctx: click.Context, session_id: str, event_id: int, prompt: str) -> None:
    """Regenerate an assistant message."""
    cli_ctx = ctx.obj
    with ui.spinner("Regenerating..."):
        result = cli_ctx.assistant.regenerate_event(session_id, event_id, prompt)
    ui.render(result, output_format=cli_ctx.output_format)


@events.command("feedback")
@click.argument("session_id")
@click.argument("event_id", type=int)
@click.option("--value", type=click.Choice(["up", "down"]), required=True)
@click.option("--note", default=None)
@click.pass_context
@handle_errors
def events_feedback(ctx: click.Context, session_id: str, event_id: int, value: str, note: str) -> None:
    """Leave feedback on an assistant message."""
    cli_ctx = ctx.obj
    with ui.spinner("Sending feedback..."):
        cli_ctx.assistant.feedback(session_id, event_id, value, note)
    ui.print_success("Feedback recorded.")


@assistant.command()
@click.pass_context
@handle_errors
def analytics(ctx: click.Context) -> None:
    """Show Copilot usage analytics."""
    cli_ctx = ctx.obj
    with ui.spinner("Fetching analytics..."):
        result = cli_ctx.assistant.analytics()
    ui.render(result, output_format=cli_ctx.output_format)
