"""`studio llm` -- LLM providers and provider configs."""
from __future__ import annotations

import click

from .. import ui
from ..crud import build_crud_group, handle_errors

_PROVIDER_COLUMNS = ["id", "slug", "name", "base_url", "available_models"]
_CONFIG_COLUMNS = ["id", "provider_slug", "provider_name", "label", "is_default", "api_key_masked"]


@click.group()
def llm() -> None:
    """LLM providers and API-key configurations."""


providers = build_crud_group(
    "providers",
    service_getter=lambda ctx: ctx.obj.llm.providers,
    columns=_PROVIDER_COLUMNS,
    id_type=int,
    supports_create=False,
    supports_update=False,
    supports_delete=False,
)
configs = build_crud_group(
    "configs",
    service_getter=lambda ctx: ctx.obj.llm.configs,
    columns=["id", "provider_slug", "provider_name", "label", "is_default", "api_key_masked"],
    id_type=int,
)

llm.add_command(providers)
llm.add_command(configs)


@providers.command("models")
@click.argument("provider_id", type=int)
@click.pass_context
@handle_errors
def models(ctx: click.Context, provider_id: int) -> None:
    """List available models for a provider."""
    cli_ctx = ctx.obj
    with ui.spinner("Fetching models..."):
        result = cli_ctx.llm.provider_models(provider_id)
    ui.render(result, output_format=cli_ctx.output_format)
