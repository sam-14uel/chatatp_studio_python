"""`studio config` -- inspect and edit the local CLI configuration."""
from __future__ import annotations

import click

from .. import ui
from ..crud import handle_errors

_SENSITIVE = {"access", "refresh", "token"}


@click.group()
def config() -> None:
    """Manage local CLI configuration (~/.studio/config.json)."""


@config.command("show")
@click.pass_context
@handle_errors
def show(ctx: click.Context) -> None:
    """Print the current configuration (secrets are masked)."""
    cfg = ctx.obj.config
    data = cfg.as_dict()
    for key in _SENSITIVE:
        if data.get(key):
            data[key] = ui.mask_secret(data[key])
    ui.render(data, output_format=ctx.obj.output_format)


@config.command("get")
@click.argument("key")
@click.pass_context
@handle_errors
def get(ctx: click.Context, key: str) -> None:
    """Print a single configuration value."""
    cfg = ctx.obj.config
    value = cfg.get(key)
    if key in _SENSITIVE and value:
        value = ui.mask_secret(value)
    click.echo(value)


@config.command("set")
@click.argument("key")
@click.argument("value")
@click.pass_context
@handle_errors
def set_(ctx: click.Context, key: str, value: str) -> None:
    """Set a configuration value, e.g. `studio config set api_url https://...`."""
    cfg = ctx.obj.config
    cfg.set(key, value)
    cfg.save()
    ui.print_success(f"{key} updated.")


@config.command("path")
def path() -> None:
    """Print the path to the local config file."""
    from ..config import CONFIG_PATH

    click.echo(str(CONFIG_PATH))
