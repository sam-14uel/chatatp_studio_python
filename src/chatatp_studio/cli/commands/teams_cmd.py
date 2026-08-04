"""`studio teams` -- teams, members, and invitations."""
from __future__ import annotations

import click

from .. import ui
from ..crud import build_crud_group, handle_errors

_COLUMNS = ["id", "name", "slug", "member_count", "my_role", "created_at"]

teams = build_crud_group(
    "teams",
    service_getter=lambda ctx: ctx.obj.teams,
    columns=_COLUMNS,
    id_type=int,
)


@teams.group("members")
def members() -> None:
    """Team member management."""


@members.command("list")
@click.argument("team_id", type=int)
@click.pass_context
@handle_errors
def list_members(ctx: click.Context, team_id: int) -> None:
    """List members of TEAM_ID."""
    cli_ctx = ctx.obj
    with ui.spinner("Fetching members..."):
        data = cli_ctx.teams.list_members(team_id)
    ui.render(data, output_format=cli_ctx.output_format)


@members.command("add")
@click.argument("team_id", type=int)
@click.option("--user", "user_id", type=int, required=True, help="User id to add.")
@click.option("--role", default="member", show_default=True)
@click.pass_context
@handle_errors
def add_member(ctx: click.Context, team_id: int, user_id: int, role: str) -> None:
    """Add a user to TEAM_ID."""
    cli_ctx = ctx.obj
    with ui.spinner("Adding member..."):
        result = cli_ctx.teams.add_member(team_id, user_id, role)
    ui.print_success("Member added.")
    ui.render(result, output_format=cli_ctx.output_format)


@members.command("remove")
@click.argument("team_id", type=int)
@click.argument("user_id", type=int)
@click.option("--yes", "-y", is_flag=True)
@click.pass_context
@handle_errors
def remove_member(ctx: click.Context, team_id: int, user_id: int, yes: bool) -> None:
    """Remove USER_ID from TEAM_ID."""
    cli_ctx = ctx.obj
    if not yes and not ui.confirm(f"Remove user {user_id} from team {team_id}?"):
        ui.print_info("Cancelled.")
        return
    with ui.spinner("Removing member..."):
        cli_ctx.teams.remove_member(team_id, user_id)
    ui.print_success("Member removed.")


@teams.group("invitations")
def invitations() -> None:
    """Team invitation management."""


@invitations.command("list")
@click.argument("team_id", type=int)
@click.pass_context
@handle_errors
def list_invitations(ctx: click.Context, team_id: int) -> None:
    """List invitations for TEAM_ID."""
    cli_ctx = ctx.obj
    with ui.spinner("Fetching invitations..."):
        data = cli_ctx.teams.list_invitations(team_id)
    ui.render(data, output_format=cli_ctx.output_format)


@invitations.command("create")
@click.argument("team_id", type=int)
@click.option("--email", required=True)
@click.option("--role", default="member", show_default=True)
@click.pass_context
@handle_errors
def create_invitation(ctx: click.Context, team_id: int, email: str, role: str) -> None:
    """Invite EMAIL to TEAM_ID."""
    cli_ctx = ctx.obj
    with ui.spinner("Sending invitation..."):
        result = cli_ctx.teams.create_invitation(team_id, email, role)
    ui.print_success("Invitation sent.")
    ui.render(result, output_format=cli_ctx.output_format)


@invitations.command("accept")
@click.argument("token")
@click.pass_context
@handle_errors
def accept_invitation(ctx: click.Context, token: str) -> None:
    """Accept a team invitation by token."""
    cli_ctx = ctx.obj
    with ui.spinner("Accepting invitation..."):
        result = cli_ctx.teams.accept_invitation(token)
    ui.print_success("Invitation accepted.")
    ui.render(result, output_format=cli_ctx.output_format)


@invitations.command("decline")
@click.argument("token")
@click.pass_context
@handle_errors
def decline_invitation(ctx: click.Context, token: str) -> None:
    """Decline a team invitation by token."""
    cli_ctx = ctx.obj
    with ui.spinner("Declining invitation..."):
        result = cli_ctx.teams.decline_invitation(token)
    ui.print_success("Invitation declined.")
    ui.render(result, output_format=cli_ctx.output_format)
