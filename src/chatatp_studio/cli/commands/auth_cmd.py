"""`studio auth` -- signup, login, logout, whoami, oauth, password reset."""
from __future__ import annotations

import click

from .. import ui
from ..crud import handle_errors


@click.group()
def auth() -> None:
    """Authentication and account commands."""


@auth.command()
@click.option("--email", prompt=True)
@click.option("--name", prompt=True)
@click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True)
@click.pass_context
@handle_errors
def signup(ctx: click.Context, email: str, name: str, password: str) -> None:
    """Create a new ChatATP Studio account."""
    cli_ctx = ctx.obj
    with ui.spinner("Creating account..."):
        result = cli_ctx.auth.signup(email, password, name)
    _store_token_bundle(cli_ctx, result)
    ui.print_success(f"Account created and signed in as {email}.")


@auth.command()
@click.option("--email", prompt=True)
@click.option("--password", prompt=True, hide_input=True)
@click.pass_context
@handle_errors
def login(ctx: click.Context, email: str, password: str) -> None:
    """Sign in and store the session token in the local config."""
    cli_ctx = ctx.obj
    with ui.spinner("Signing in..."):
        result = cli_ctx.auth.signin(email, password)
    _store_token_bundle(cli_ctx, result)
    ui.print_success(f"Signed in as {email}.")


@auth.command()
@click.pass_context
@handle_errors
def logout(ctx: click.Context) -> None:
    """Sign out and clear local credentials."""
    cli_ctx = ctx.obj
    if cli_ctx.config.is_authenticated():
        try:
            with ui.spinner("Signing out..."):
                cli_ctx.auth.signout()
        except Exception:
            pass  # best-effort; still clear local credentials
    cli_ctx.config.clear_credentials()
    cli_ctx.config.save()
    ui.print_success("Signed out.")


@auth.command()
@click.pass_context
@handle_errors
def whoami(ctx: click.Context) -> None:
    """Show the currently authenticated user."""
    cli_ctx = ctx.obj
    with ui.spinner("Fetching current user..."):
        me = cli_ctx.auth.me()
    ui.render(me, output_format=cli_ctx.output_format)


@auth.command("update-profile")
@click.option("--name", default=None)
@click.option("--avatar-url", default=None)
@click.pass_context
@handle_errors
def update_profile(ctx: click.Context, name: str, avatar_url: str) -> None:
    """Update the current user's profile."""
    cli_ctx = ctx.obj
    fields = {k: v for k, v in {"name": name, "avatar_url": avatar_url}.items() if v is not None}
    if not fields:
        ui.print_warning("Nothing to update. Pass --name and/or --avatar-url.")
        return
    with ui.spinner("Updating profile..."):
        result = cli_ctx.auth.update_profile(**fields)
    ui.print_success("Profile updated.")
    ui.render(result, output_format=cli_ctx.output_format)


@auth.command()
@click.option("--role", prompt=True)
@click.pass_context
@handle_errors
def onboarding(ctx: click.Context, role: str) -> None:
    """Submit onboarding details for the current user."""
    cli_ctx = ctx.obj
    with ui.spinner("Submitting onboarding..."):
        result = cli_ctx.auth.onboarding(role=role)
    ui.print_success("Onboarding submitted.")
    ui.render(result, output_format=cli_ctx.output_format)


@auth.command("forgot-password")
@click.option("--email", prompt=True)
@click.pass_context
@handle_errors
def forgot_password(ctx: click.Context, email: str) -> None:
    """Request a password reset email."""
    cli_ctx = ctx.obj
    with ui.spinner("Requesting reset..."):
        cli_ctx.auth.forgot_password(email)
    ui.print_success("If that account exists, a reset email has been sent.")


@auth.command("reset-password")
@click.option("--token", prompt=True)
@click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True)
@click.pass_context
@handle_errors
def reset_password(ctx: click.Context, token: str, password: str) -> None:
    """Reset a password using a reset token."""
    cli_ctx = ctx.obj
    with ui.spinner("Resetting password..."):
        cli_ctx.auth.reset_password(token, password)
    ui.print_success("Password reset. You can now log in.")


@auth.command("oauth-providers")
@click.pass_context
@handle_errors
def oauth_providers(ctx: click.Context) -> None:
    """List available OAuth login providers."""
    cli_ctx = ctx.obj
    with ui.spinner("Fetching providers..."):
        result = cli_ctx.auth.oauth_providers()
    ui.render(result, output_format=cli_ctx.output_format)


@auth.command("oauth-start")
@click.argument("provider")
@click.pass_context
@handle_errors
def oauth_start(ctx: click.Context, provider: str) -> None:
    """Start an OAuth login flow for PROVIDER and print the URL to open."""
    cli_ctx = ctx.obj
    with ui.spinner("Starting OAuth flow..."):
        result = cli_ctx.auth.oauth_start(provider)
    url = result.get("authorization_url") if isinstance(result, dict) else None
    if url:
        ui.print_info(f"Open this URL in your browser to continue: {url}")
    ui.render(result, output_format=cli_ctx.output_format)


def _store_token_bundle(cli_ctx, result: dict) -> None:
    """Persist the access/refresh/token bundle returned by signup/signin."""
    cfg = cli_ctx.config
    cfg.access = result.get("access")
    cfg.refresh = result.get("refresh")
    cfg.token = result.get("token")
    user = result.get("user") or {}
    cfg.user_email = user.get("email")
    cfg.user_id = user.get("id")
    cfg.save()
