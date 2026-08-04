"""`studio users` -- user management and invitations."""
from __future__ import annotations

import click

from .. import ui
from ..crud import build_crud_group, handle_errors

_COLUMNS = ["id", "email", "full_name", "role", "is_staff", "created_at"]

users = build_crud_group(
    "users",
    service_getter=lambda ctx: ctx.obj.users,
    columns=_COLUMNS,
    id_type=int,
)


@users.group("invitations")
def invitations() -> None:
    """User invitations."""


@invitations.command("list")
@click.pass_context
@handle_errors
def list_invitations(ctx: click.Context) -> None:
    """List pending invitations for the current user."""
    cli_ctx = ctx.obj
    with ui.spinner("Fetching invitations..."):
        data = cli_ctx.users.list_invitations()
    ui.render(data, output_format=cli_ctx.output_format)


@invitations.command("accept")
@click.argument("token")
@click.pass_context
@handle_errors
def accept_invitation(ctx: click.Context, token: str) -> None:
    """Accept an invitation by token."""
    cli_ctx = ctx.obj
    with ui.spinner("Accepting invitation..."):
        result = cli_ctx.users.accept_invitation(token)
    ui.print_success("Invitation accepted.")
    ui.render(result, output_format=cli_ctx.output_format)


@invitations.command("decline")
@click.argument("token")
@click.pass_context
@handle_errors
def decline_invitation(ctx: click.Context, token: str) -> None:
    """Decline an invitation by token."""
    cli_ctx = ctx.obj
    with ui.spinner("Declining invitation..."):
        result = cli_ctx.users.decline_invitation(token)
    ui.print_success("Invitation declined.")
    ui.render(result, output_format=cli_ctx.output_format)
