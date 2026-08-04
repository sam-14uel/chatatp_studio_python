"""Rich-powered terminal UI helpers shared by every command module."""
from __future__ import annotations

import json as jsonlib
from contextlib import contextmanager
from typing import Any, Dict, Iterable, List, Optional, Sequence

import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Confirm, Prompt
from rich.table import Table

console = Console()
err_console = Console(stderr=True)


def print_json(data: Any) -> None:
    console.print_json(jsonlib.dumps(data, default=str))


def print_success(message: str) -> None:
    console.print(f"[bold green]\u2713[/bold green] {message}")


def print_info(message: str) -> None:
    console.print(f"[bold cyan]i[/bold cyan] {message}")


def print_warning(message: str) -> None:
    console.print(f"[bold yellow]![/bold yellow] {message}")


def print_error(message: str) -> None:
    err_console.print(f"[bold red]\u2717[/bold red] {message}")


def print_panel(title: str, body: str) -> None:
    console.print(Panel.fit(body, title=title))


def mask_secret(value: Optional[str], keep: int = 4) -> str:
    if not value:
        return ""
    if len(value) <= keep:
        return "*" * len(value)
    return "*" * (len(value) - keep) + value[-keep:]


def print_table(
    rows: Sequence[Dict[str, Any]],
    columns: Optional[Sequence[str]] = None,
    title: Optional[str] = None,
) -> None:
    if not rows:
        print_info("No results.")
        return
    columns = list(columns) if columns else list(rows[0].keys())
    table = Table(title=title, show_lines=False, header_style="bold cyan")
    for col in columns:
        table.add_column(col)
    for row in rows:
        table.add_row(*[_stringify(row.get(col)) for col in columns])
    console.print(table)


def _stringify(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        text = jsonlib.dumps(value, default=str)
        return text if len(text) <= 60 else text[:57] + "..."
    return str(value)


def render(data: Any, output_format: str = "table", columns: Optional[Sequence[str]] = None, title: Optional[str] = None) -> None:
    """Render a list-or-object API response according to the desired format."""
    if output_format == "json":
        print_json(data)
        return
    # Paginated DRF response: {"results": [...], "count": N, ...}
    if isinstance(data, dict) and "results" in data and isinstance(data["results"], list):
        print_table(data["results"], columns=columns, title=title)
        meta = {k: v for k, v in data.items() if k != "results"}
        if meta:
            print_info(f"count={meta.get('count')} next={bool(meta.get('next'))} previous={bool(meta.get('previous'))}")
        return
    if isinstance(data, list):
        print_table(data, columns=columns, title=title)
        return
    if isinstance(data, dict):
        print_table([data], columns=columns, title=title)
        return
    console.print(data)


@contextmanager
def spinner(message: str):
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task(description=message, total=None)
        yield


def confirm(message: str, default: bool = False) -> bool:
    return Confirm.ask(message, default=default)


def prompt(message: str, default: Optional[str] = None, password: bool = False) -> str:
    return Prompt.ask(message, default=default, password=password)


def parse_json_option(value: Optional[str]) -> Optional[Dict[str, Any]]:
    """Parse a --data/--config JSON string, or read it from @file if prefixed with @."""
    if value is None:
        return None
    if value.startswith("@"):
        with open(value[1:], "r", encoding="utf-8") as fh:
            value = fh.read()
    try:
        return jsonlib.loads(value)
    except jsonlib.JSONDecodeError as exc:
        raise click.BadParameter(f"Invalid JSON: {exc}") from exc


def key_value_pairs_to_dict(pairs: Iterable[str]) -> Dict[str, Any]:
    """Convert ['key=value', 'nested.key=value'] into a flat dict.

    Values are parsed as JSON when possible (so `--set enabled=true` yields
    a boolean), falling back to plain strings.
    """
    result: Dict[str, Any] = {}
    for pair in pairs:
        if "=" not in pair:
            raise click.BadParameter(f"Expected key=value, got: {pair}")
        key, raw_value = pair.split("=", 1)
        try:
            value: Any = jsonlib.loads(raw_value)
        except jsonlib.JSONDecodeError:
            value = raw_value
        result[key] = value
    return result
