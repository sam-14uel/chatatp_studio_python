"""`studio kb` -- standalone knowledge bases and agent-linked KB endpoints."""
from __future__ import annotations

import click

from .. import ui
from ..crud import build_crud_group, handle_errors

kb = build_crud_group(
    "kb",
    service_getter=lambda ctx: ctx.obj.kb,
    columns=["id", "name", "description", "status", "created_at"],
    id_type=str,
)


# -- standalone KB documents -------------------------------------------------
@kb.group("documents")
def documents() -> None:
    """Documents within a standalone knowledge base."""


@documents.command("list")
@click.argument("kb_id")
@click.pass_context
@handle_errors
def documents_list(ctx: click.Context, kb_id: str) -> None:
    """List documents in a knowledge base."""
    cli_ctx = ctx.obj
    with ui.spinner("Fetching documents..."):
        data = cli_ctx.kb.list_documents(kb_id)
    ui.render(data, output_format=cli_ctx.output_format, columns=["id", "name", "file_type", "status", "chunk_count"])


@documents.command("upload")
@click.argument("kb_id")
@click.option("--file", "file_path", required=True, type=click.Path(exists=True), help="Local file to upload.")
@click.pass_context
@handle_errors
def documents_upload(ctx: click.Context, kb_id: str, file_path: str) -> None:
    """Upload a document to a knowledge base."""
    cli_ctx = ctx.obj
    with ui.spinner("Uploading document..."):
        result = cli_ctx.kb.upload_document(kb_id, file_path)
    ui.print_success("Document uploaded.")
    ui.render(result, output_format=cli_ctx.output_format)


@documents.command("get")
@click.argument("kb_id")
@click.argument("doc_id")
@click.pass_context
@handle_errors
def documents_get(ctx: click.Context, kb_id: str, doc_id: str) -> None:
    """Get a knowledge base document."""
    cli_ctx = ctx.obj
    with ui.spinner("Fetching document..."):
        data = cli_ctx.kb.get_document(kb_id, doc_id)
    ui.render(data, output_format=cli_ctx.output_format)


@documents.command("delete")
@click.argument("kb_id")
@click.argument("doc_id")
@click.option("--yes", "-y", is_flag=True)
@click.pass_context
@handle_errors
def documents_delete(ctx: click.Context, kb_id: str, doc_id: str, yes: bool) -> None:
    """Delete a knowledge base document."""
    cli_ctx = ctx.obj
    if not yes and not ui.confirm(f"Delete document {doc_id}?"):
        ui.print_info("Cancelled.")
        return
    with ui.spinner("Deleting document..."):
        cli_ctx.kb.delete_document(kb_id, doc_id)
    ui.print_success("Document deleted.")


@documents.command("chunks")
@click.argument("kb_id")
@click.argument("doc_id")
@click.pass_context
@handle_errors
def documents_chunks(ctx: click.Context, kb_id: str, doc_id: str) -> None:
    """List the indexed chunks for a document."""
    cli_ctx = ctx.obj
    with ui.spinner("Fetching chunks..."):
        data = cli_ctx.kb.document_chunks(kb_id, doc_id)
    ui.render(data, output_format=cli_ctx.output_format)


# -- standalone KB domains ---------------------------------------------------
@kb.group("domains")
def domains() -> None:
    """Crawlable web domains within a standalone knowledge base."""


@domains.command("list")
@click.argument("kb_id")
@click.pass_context
@handle_errors
def domains_list(ctx: click.Context, kb_id: str) -> None:
    """List domains attached to a knowledge base."""
    cli_ctx = ctx.obj
    with ui.spinner("Fetching domains..."):
        data = cli_ctx.kb.list_domains(kb_id)
    ui.render(data, output_format=cli_ctx.output_format, columns=["id", "domain", "status", "pages_crawled"])


@domains.command("add")
@click.argument("kb_id")
@click.option("--url", "domain", required=True, help="Domain URL to crawl, e.g. https://example.com")
@click.pass_context
@handle_errors
def domains_add(ctx: click.Context, kb_id: str, domain: str) -> None:
    """Add a domain to a knowledge base."""
    cli_ctx = ctx.obj
    with ui.spinner("Adding domain..."):
        result = cli_ctx.kb.add_domain(kb_id, domain)
    ui.print_success("Domain added.")
    ui.render(result, output_format=cli_ctx.output_format)


@domains.command("get")
@click.argument("kb_id")
@click.argument("domain_id")
@click.pass_context
@handle_errors
def domains_get(ctx: click.Context, kb_id: str, domain_id: str) -> None:
    """Get a knowledge base domain."""
    cli_ctx = ctx.obj
    with ui.spinner("Fetching domain..."):
        data = cli_ctx.kb.get_domain(kb_id, domain_id)
    ui.render(data, output_format=cli_ctx.output_format)


@domains.command("delete")
@click.argument("kb_id")
@click.argument("domain_id")
@click.option("--yes", "-y", is_flag=True)
@click.pass_context
@handle_errors
def domains_delete(ctx: click.Context, kb_id: str, domain_id: str, yes: bool) -> None:
    """Delete a knowledge base domain."""
    cli_ctx = ctx.obj
    if not yes and not ui.confirm(f"Delete domain {domain_id}?"):
        ui.print_info("Cancelled.")
        return
    with ui.spinner("Deleting domain..."):
        cli_ctx.kb.delete_domain(kb_id, domain_id)
    ui.print_success("Domain deleted.")


@domains.command("crawl")
@click.argument("kb_id")
@click.argument("domain_id")
@click.pass_context
@handle_errors
def domains_crawl(ctx: click.Context, kb_id: str, domain_id: str) -> None:
    """Trigger a crawl for a knowledge base domain."""
    cli_ctx = ctx.obj
    with ui.spinner("Starting crawl..."):
        result = cli_ctx.kb.crawl_domain(kb_id, domain_id)
    ui.print_success("Crawl started.")
    ui.render(result, output_format=cli_ctx.output_format)


# -- standalone KB search / stats -------------------------------------------
@kb.command("stats")
@click.argument("kb_id")
@click.pass_context
@handle_errors
def stats(ctx: click.Context, kb_id: str) -> None:
    """Show indexing stats for a knowledge base."""
    cli_ctx = ctx.obj
    with ui.spinner("Fetching stats..."):
        data = cli_ctx.kb.stats(kb_id)
    ui.render(data, output_format=cli_ctx.output_format)


@kb.command("search")
@click.argument("kb_id")
@click.option("--query", "-q", required=True)
@click.option("--top-k", type=int, default=5, show_default=True)
@click.pass_context
@handle_errors
def search(ctx: click.Context, kb_id: str, query: str, top_k: int) -> None:
    """Search a knowledge base."""
    cli_ctx = ctx.obj
    with ui.spinner("Searching..."):
        data = cli_ctx.kb.search(kb_id, query, top_k)
    ui.render(data, output_format=cli_ctx.output_format)


# -- agent-linked KB endpoints ------------------------------------------------
@click.group("agent")
def agent_kb() -> None:
    """Knowledge-base endpoints scoped to a specific agent."""


kb.add_command(agent_kb)


@agent_kb.command("stats")
@click.argument("agent_id", type=int)
@click.pass_context
@handle_errors
def agent_stats(ctx: click.Context, agent_id: int) -> None:
    """Show KB stats for an agent."""
    cli_ctx = ctx.obj
    with ui.spinner("Fetching stats..."):
        data = cli_ctx.kb.agent_stats(agent_id)
    ui.render(data, output_format=cli_ctx.output_format)


@agent_kb.group("documents")
def agent_documents() -> None:
    """Documents directly attached to an agent's built-in knowledge base."""


@agent_documents.command("list")
@click.argument("agent_id", type=int)
@click.pass_context
@handle_errors
def agent_documents_list(ctx: click.Context, agent_id: int) -> None:
    """List an agent's KB documents."""
    cli_ctx = ctx.obj
    with ui.spinner("Fetching documents..."):
        data = cli_ctx.kb.agent_list_documents(agent_id)
    ui.render(data, output_format=cli_ctx.output_format)


@agent_documents.command("upload")
@click.argument("agent_id", type=int)
@click.option("--file", "file_path", required=True, type=click.Path(exists=True))
@click.pass_context
@handle_errors
def agent_documents_upload(ctx: click.Context, agent_id: int, file_path: str) -> None:
    """Upload a document to an agent's KB."""
    cli_ctx = ctx.obj
    with ui.spinner("Uploading document..."):
        result = cli_ctx.kb.agent_upload_document(agent_id, file_path)
    ui.print_success("Document uploaded.")
    ui.render(result, output_format=cli_ctx.output_format)


@agent_documents.command("get")
@click.argument("agent_id", type=int)
@click.argument("doc_id")
@click.pass_context
@handle_errors
def agent_documents_get(ctx: click.Context, agent_id: int, doc_id: str) -> None:
    """Get an agent's KB document."""
    cli_ctx = ctx.obj
    with ui.spinner("Fetching document..."):
        data = cli_ctx.kb.agent_get_document(agent_id, doc_id)
    ui.render(data, output_format=cli_ctx.output_format)


@agent_documents.command("delete")
@click.argument("agent_id", type=int)
@click.argument("doc_id")
@click.option("--yes", "-y", is_flag=True)
@click.pass_context
@handle_errors
def agent_documents_delete(ctx: click.Context, agent_id: int, doc_id: str, yes: bool) -> None:
    """Delete an agent's KB document."""
    cli_ctx = ctx.obj
    if not yes and not ui.confirm(f"Delete document {doc_id}?"):
        ui.print_info("Cancelled.")
        return
    with ui.spinner("Deleting document..."):
        cli_ctx.kb.agent_delete_document(agent_id, doc_id)
    ui.print_success("Document deleted.")


@agent_documents.command("chunks")
@click.argument("agent_id", type=int)
@click.argument("doc_id")
@click.pass_context
@handle_errors
def agent_documents_chunks(ctx: click.Context, agent_id: int, doc_id: str) -> None:
    """List chunks for an agent's KB document."""
    cli_ctx = ctx.obj
    with ui.spinner("Fetching chunks..."):
        data = cli_ctx.kb.agent_document_chunks(agent_id, doc_id)
    ui.render(data, output_format=cli_ctx.output_format)


@agent_kb.group("domains")
def agent_domains() -> None:
    """Domains directly attached to an agent's built-in knowledge base."""


@agent_domains.command("list")
@click.argument("agent_id", type=int)
@click.pass_context
@handle_errors
def agent_domains_list(ctx: click.Context, agent_id: int) -> None:
    """List an agent's KB domains."""
    cli_ctx = ctx.obj
    with ui.spinner("Fetching domains..."):
        data = cli_ctx.kb.agent_list_domains(agent_id)
    ui.render(data, output_format=cli_ctx.output_format)


@agent_domains.command("add")
@click.argument("agent_id", type=int)
@click.option("--url", "domain", required=True)
@click.pass_context
@handle_errors
def agent_domains_add(ctx: click.Context, agent_id: int, domain: str) -> None:
    """Add a domain to an agent's KB."""
    cli_ctx = ctx.obj
    with ui.spinner("Adding domain..."):
        result = cli_ctx.kb.agent_add_domain(agent_id, domain)
    ui.print_success("Domain added.")
    ui.render(result, output_format=cli_ctx.output_format)


@agent_domains.command("delete")
@click.argument("agent_id", type=int)
@click.argument("domain_id")
@click.option("--yes", "-y", is_flag=True)
@click.pass_context
@handle_errors
def agent_domains_delete(ctx: click.Context, agent_id: int, domain_id: str, yes: bool) -> None:
    """Delete a domain from an agent's KB."""
    cli_ctx = ctx.obj
    if not yes and not ui.confirm(f"Delete domain {domain_id}?"):
        ui.print_info("Cancelled.")
        return
    with ui.spinner("Deleting domain..."):
        cli_ctx.kb.agent_delete_domain(agent_id, domain_id)
    ui.print_success("Domain deleted.")


@agent_domains.command("crawl")
@click.argument("agent_id", type=int)
@click.argument("domain_id")
@click.pass_context
@handle_errors
def agent_domains_crawl(ctx: click.Context, agent_id: int, domain_id: str) -> None:
    """Trigger a crawl for an agent's KB domain."""
    cli_ctx = ctx.obj
    with ui.spinner("Starting crawl..."):
        result = cli_ctx.kb.agent_crawl_domain(agent_id, domain_id)
    ui.print_success("Crawl started.")
    ui.render(result, output_format=cli_ctx.output_format)


@agent_kb.command("search")
@click.argument("agent_id", type=int)
@click.option("--query", "-q", required=True)
@click.option("--top-k", type=int, default=5, show_default=True)
@click.pass_context
@handle_errors
def agent_search(ctx: click.Context, agent_id: int, query: str, top_k: int) -> None:
    """Search an agent's knowledge base."""
    cli_ctx = ctx.obj
    with ui.spinner("Searching..."):
        data = cli_ctx.kb.agent_search(agent_id, query, top_k)
    ui.render(data, output_format=cli_ctx.output_format)


@agent_kb.command("test")
@click.argument("agent_id", type=int)
@click.option("--query", "-q", required=True)
@click.pass_context
@handle_errors
def agent_test(ctx: click.Context, agent_id: int, query: str) -> None:
    """Run a KB retrieval test query for an agent."""
    cli_ctx = ctx.obj
    with ui.spinner("Testing..."):
        data = cli_ctx.kb.agent_test(agent_id, query)
    ui.render(data, output_format=cli_ctx.output_format)


# -- agent <-> KB attachments -------------------------------------------------
@agent_kb.group("attachments")
def attachments() -> None:
    """Attach or detach standalone knowledge bases from an agent."""


@attachments.command("list")
@click.argument("agent_id", type=int)
@click.pass_context
@handle_errors
def attachments_list(ctx: click.Context, agent_id: int) -> None:
    """List knowledge bases attached to an agent."""
    cli_ctx = ctx.obj
    with ui.spinner("Fetching attachments..."):
        data = cli_ctx.kb.list_attachments(agent_id)
    ui.render(data, output_format=cli_ctx.output_format)


@attachments.command("available")
@click.argument("agent_id", type=int)
@click.pass_context
@handle_errors
def attachments_available(ctx: click.Context, agent_id: int) -> None:
    """List knowledge bases available to attach to an agent."""
    cli_ctx = ctx.obj
    with ui.spinner("Fetching available knowledge bases..."):
        data = cli_ctx.kb.available(agent_id)
    ui.render(data, output_format=cli_ctx.output_format)


@attachments.command("attach")
@click.argument("agent_id", type=int)
@click.option("--kb-id", required=True, help="Knowledge base id to attach.")
@click.option("--enabled/--disabled", default=True)
@click.option("--auto-context/--no-auto-context", default=True)
@click.option("--max-context-chunks", type=int, default=3, show_default=True)
@click.option("--context-threshold", type=float, default=0.3, show_default=True)
@click.pass_context
@handle_errors
def attachments_attach(
    ctx: click.Context,
    agent_id: int,
    kb_id: str,
    enabled: bool,
    auto_context: bool,
    max_context_chunks: int,
    context_threshold: float,
) -> None:
    """Attach a standalone knowledge base to an agent."""
    cli_ctx = ctx.obj
    with ui.spinner("Attaching..."):
        result = cli_ctx.kb.attach(
            agent_id,
            kb_id,
            enabled=enabled,
            auto_context=auto_context,
            max_context_chunks=max_context_chunks,
            context_threshold=context_threshold,
        )
    ui.print_success("Knowledge base attached.")
    ui.render(result, output_format=cli_ctx.output_format)


@attachments.command("update")
@click.argument("agent_id", type=int)
@click.argument("attachment_id")
@click.option("--data", required=True, help="JSON payload, or @path/to/file.json.")
@click.pass_context
@handle_errors
def attachments_update(ctx: click.Context, agent_id: int, attachment_id: str, data: str) -> None:
    """Update an agent's knowledge-base attachment settings."""
    cli_ctx = ctx.obj
    payload = ui.parse_json_option(data) or {}
    with ui.spinner("Updating attachment..."):
        result = cli_ctx.kb.update_attachment(agent_id, attachment_id, **payload)
    ui.print_success("Attachment updated.")
    ui.render(result, output_format=cli_ctx.output_format)


@attachments.command("detach")
@click.argument("agent_id", type=int)
@click.argument("attachment_id")
@click.option("--yes", "-y", is_flag=True)
@click.pass_context
@handle_errors
def attachments_detach(ctx: click.Context, agent_id: int, attachment_id: str, yes: bool) -> None:
    """Detach a knowledge base from an agent."""
    cli_ctx = ctx.obj
    if not yes and not ui.confirm(f"Detach knowledge base attachment {attachment_id}?"):
        ui.print_info("Cancelled.")
        return
    with ui.spinner("Detaching..."):
        cli_ctx.kb.detach(agent_id, attachment_id)
    ui.print_success("Knowledge base detached.")
