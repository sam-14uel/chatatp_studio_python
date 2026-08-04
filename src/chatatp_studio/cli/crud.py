"""Generic CRUD command factory shared by every resource command group.

`build_crud_group` produces a `click.Group` with `list`, `get`, `create`,
`update`, and `delete` subcommands wired to a `BaseService`-shaped object
(anything with .list/.get/.create/.update/.delete). Resource-specific
command modules use this for the boilerplate CRUD surface and then add
bespoke subcommands (connect, preview, execute, search, ...) alongside it.
"""
from __future__ import annotations

from typing import Any, Callable, Optional, Sequence

import click

from . import ui
from .exceptions import APIError, AuthenticationError, StudioError


def handle_errors(fn: Callable) -> Callable:
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return fn(*args, **kwargs)
        except AuthenticationError as exc:
            ui.print_error(str(exc))
            raise SystemExit(1)
        except APIError as exc:
            ui.print_error(str(exc))
            raise SystemExit(1)
        except StudioError as exc:
            ui.print_error(str(exc))
            raise SystemExit(1)

    wrapper.__name__ = fn.__name__
    wrapper.__doc__ = fn.__doc__
    return wrapper


def build_crud_group(
    name: str,
    service_getter: Callable[[click.Context], Any],
    *,
    columns: Optional[Sequence[str]] = None,
    id_type: type = str,
    id_arg_name: str = "resource_id",
    create_help: str = "Create a new resource from a JSON payload (or @file.json).",
    supports_create: bool = True,
    supports_update: bool = True,
    supports_delete: bool = True,
) -> click.Group:
    @click.group(name=name, help=f"Manage {name}.")
    def group() -> None:
        pass

    @group.command("list")
    @click.option("--page", type=int, default=None, help="Page number, if the API paginates results.")
    @click.option("--page-size", type=int, default=None, help="Page size, if supported by the API.")
    @click.option("--filter", "filters", multiple=True, help="Extra query filter as key=value. Repeatable.")
    @click.pass_context
    @handle_errors
    def list_cmd(ctx: click.Context, page: Optional[int], page_size: Optional[int], filters: Sequence[str]) -> None:
        f"""List {name}."""
        params = ui.key_value_pairs_to_dict(filters)
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size
        service = service_getter(ctx)
        with ui.spinner(f"Fetching {name}..."):
            data = service.list(**params)
        ui.render(data, output_format=ctx.obj.output_format, columns=columns, title=name)

    @group.command("get")
    @click.argument(id_arg_name, type=id_type)
    @click.pass_context
    @handle_errors
    def get_cmd(ctx: click.Context, **kwargs: Any) -> None:
        f"""Retrieve a single resource from {name} by id."""
        resource_id = kwargs[id_arg_name]
        service = service_getter(ctx)
        with ui.spinner("Fetching..."):
            data = service.get(resource_id)
        ui.render(data, output_format=ctx.obj.output_format, columns=columns)

    if supports_create:

        @group.command("create")
        @click.option("--data", "data", required=True, help="JSON payload, or @path/to/file.json.")
        @click.pass_context
        @handle_errors
        def create_cmd(ctx: click.Context, data: str) -> None:
            f"""Create a new resource in {name}."""
            payload = ui.parse_json_option(data) or {}
            service = service_getter(ctx)
            with ui.spinner("Creating..."):
                result = service.create(payload)
            ui.print_success("Created.")
            ui.render(result, output_format=ctx.obj.output_format, columns=columns)

    if supports_update:

        @group.command("update")
        @click.argument(id_arg_name, type=id_type)
        @click.option("--data", "data", required=True, help="JSON payload (partial), or @path/to/file.json.")
        @click.option("--full", is_flag=True, help="Send a full PUT replace instead of a partial PATCH.")
        @click.pass_context
        @handle_errors
        def update_cmd(ctx: click.Context, data: str, full: bool, **kwargs: Any) -> None:
            f"""Update an existing resource in {name}."""
            resource_id = kwargs[id_arg_name]
            payload = ui.parse_json_option(data) or {}
            service = service_getter(ctx)
            with ui.spinner("Updating..."):
                result = service.update(resource_id, payload, partial=not full)
            ui.print_success("Updated.")
            ui.render(result, output_format=ctx.obj.output_format, columns=columns)

    if supports_delete:

        @group.command("delete")
        @click.argument(id_arg_name, type=id_type)
        @click.option("--yes", "-y", is_flag=True, help="Skip the confirmation prompt.")
        @click.pass_context
        @handle_errors
        def delete_cmd(ctx: click.Context, yes: bool, **kwargs: Any) -> None:
            f"""Delete a resource from {name}."""
            resource_id = kwargs[id_arg_name]
            if not yes and not ui.confirm(f"Delete {name} {resource_id}?"):
                ui.print_info("Cancelled.")
                return
            service = service_getter(ctx)
            with ui.spinner("Deleting..."):
                service.delete(resource_id)
            ui.print_success("Deleted.")

    return group
