"""Entry point for the `studio` executable."""
from __future__ import annotations

try:
    import click

    from . import __version__
    from .api_client import APIClient
    from .config import Config
    from .context import CLIContext
    from .commands import auth_cmd, config_cmd, agents_cmd, assistant_cmd, http_api_cmd, kb_cmd, llm_cmd, mcp_cmd, platforms_cmd, teams_cmd, users_cmd
except ImportError:
    print("Error: CLI dependencies missing. Please install via: pip install 'chatatp-studio[cli]'")
    raise SystemExit(1)


@click.group()
@click.version_option(version=__version__, prog_name="studio")
@click.option("--json", "as_json", is_flag=True, help="Output raw JSON instead of tables.")
@click.option("--api-url", default=None, help="Override the configured Studio API base URL for this invocation.")
@click.pass_context
def cli(ctx: click.Context, as_json: bool, api_url: str) -> None:
    """studio -- official ChatATP Studio command-line interface.

    Run `studio auth login` to authenticate, then explore resources with
    `studio <resource> --help`, e.g. `studio agents --help`.
    """
    config = Config.load()
    if api_url:
        config.api_url = api_url
    if as_json:
        config.output_format = "json"
    client = APIClient(config)
    ctx.obj = CLIContext(config=config, client=client, output_format=config.output_format)


cli.add_command(auth_cmd.auth)
cli.add_command(config_cmd.config)
cli.add_command(users_cmd.users)
cli.add_command(teams_cmd.teams)
cli.add_command(agents_cmd.agents)
cli.add_command(assistant_cmd.assistant)
cli.add_command(mcp_cmd.mcp)
cli.add_command(http_api_cmd.http_api)
cli.add_command(llm_cmd.llm)
cli.add_command(kb_cmd.kb)
cli.add_command(platforms_cmd.platforms)


def main() -> None:
    cli()


if __name__ == "__main__":
    main()
