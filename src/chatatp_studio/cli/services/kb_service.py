"""Knowledge base service (standalone KBs and agent-linked KB endpoints)."""
from __future__ import annotations

from typing import Any, Dict, Optional

from .. import endpoints
from ..api_client import APIClient
from .base import BaseService


class KnowledgeBaseService(BaseService):
    def __init__(self, client: APIClient) -> None:
        super().__init__(client, endpoints.KB_LIST, endpoints.KB_DETAIL)

    # -- standalone KB documents ------------------------------------------------
    def list_documents(self, kb_id: Any) -> Any:
        return self.client.get(endpoints.KB_DOCUMENTS.format(id=kb_id))

    def upload_document(self, kb_id: Any, file_path: str) -> Any:
        return self.client.upload(endpoints.KB_DOCUMENTS.format(id=kb_id), file_path)

    def get_document(self, kb_id: Any, doc_id: Any) -> Any:
        return self.client.get(endpoints.KB_DOCUMENT_DETAIL.format(id=kb_id, doc_id=doc_id))

    def delete_document(self, kb_id: Any, doc_id: Any) -> Any:
        return self.client.delete(endpoints.KB_DOCUMENT_DETAIL.format(id=kb_id, doc_id=doc_id))

    def document_chunks(self, kb_id: Any, doc_id: Any) -> Any:
        return self.client.get(endpoints.KB_DOCUMENT_CHUNKS.format(id=kb_id, doc_id=doc_id))

    # -- standalone KB domains ---------------------------------------------------
    def list_domains(self, kb_id: Any) -> Any:
        return self.client.get(endpoints.KB_DOMAINS.format(id=kb_id))

    def add_domain(self, kb_id: Any, domain: str) -> Any:
        return self.client.post(endpoints.KB_DOMAINS.format(id=kb_id), {"domain": domain})

    def get_domain(self, kb_id: Any, domain_id: Any) -> Any:
        return self.client.get(endpoints.KB_DOMAIN_DETAIL.format(id=kb_id, domain_id=domain_id))

    def delete_domain(self, kb_id: Any, domain_id: Any) -> Any:
        return self.client.delete(endpoints.KB_DOMAIN_DETAIL.format(id=kb_id, domain_id=domain_id))

    def crawl_domain(self, kb_id: Any, domain_id: Any) -> Any:
        return self.client.post(endpoints.KB_DOMAIN_CRAWL.format(id=kb_id, domain_id=domain_id))

    # -- standalone KB search / stats -------------------------------------------
    def stats(self, kb_id: Any) -> Any:
        return self.client.get(endpoints.KB_STATS.format(id=kb_id))

    def search(self, kb_id: Any, query: str, top_k: int = 5) -> Any:
        return self.client.post(endpoints.KB_SEARCH.format(id=kb_id), {"query": query, "top_k": top_k})

    # -- agent-linked KB endpoints -----------------------------------------------
    def agent_stats(self, agent_id: Any) -> Any:
        return self.client.get(endpoints.AGENT_KB_STATS.format(agent_id=agent_id))

    def agent_list_documents(self, agent_id: Any) -> Any:
        return self.client.get(endpoints.AGENT_KB_DOCUMENTS.format(agent_id=agent_id))

    def agent_upload_document(self, agent_id: Any, file_path: str) -> Any:
        return self.client.upload(endpoints.AGENT_KB_DOCUMENTS.format(agent_id=agent_id), file_path)

    def agent_get_document(self, agent_id: Any, doc_id: Any) -> Any:
        return self.client.get(endpoints.AGENT_KB_DOCUMENT_DETAIL.format(agent_id=agent_id, doc_id=doc_id))

    def agent_delete_document(self, agent_id: Any, doc_id: Any) -> Any:
        return self.client.delete(endpoints.AGENT_KB_DOCUMENT_DETAIL.format(agent_id=agent_id, doc_id=doc_id))

    def agent_document_chunks(self, agent_id: Any, doc_id: Any) -> Any:
        return self.client.get(endpoints.AGENT_KB_DOCUMENT_CHUNKS.format(agent_id=agent_id, doc_id=doc_id))

    def agent_list_domains(self, agent_id: Any) -> Any:
        return self.client.get(endpoints.AGENT_KB_DOMAINS.format(agent_id=agent_id))

    def agent_add_domain(self, agent_id: Any, domain: str) -> Any:
        return self.client.post(endpoints.AGENT_KB_DOMAINS.format(agent_id=agent_id), {"domain": domain})

    def agent_delete_domain(self, agent_id: Any, domain_id: Any) -> Any:
        return self.client.delete(endpoints.AGENT_KB_DOMAIN_DETAIL.format(agent_id=agent_id, domain_id=domain_id))

    def agent_crawl_domain(self, agent_id: Any, domain_id: Any) -> Any:
        return self.client.post(endpoints.AGENT_KB_DOMAIN_CRAWL.format(agent_id=agent_id, domain_id=domain_id))

    def agent_search(self, agent_id: Any, query: str, top_k: int = 5) -> Any:
        return self.client.post(endpoints.AGENT_KB_SEARCH.format(agent_id=agent_id), {"query": query, "top_k": top_k})

    def agent_test(self, agent_id: Any, test_query: str) -> Any:
        return self.client.post(endpoints.AGENT_KB_TEST.format(agent_id=agent_id), {"test_query": test_query})

    # -- agent <-> KB attachments -------------------------------------------------
    def list_attachments(self, agent_id: Any) -> Any:
        return self.client.get(endpoints.AGENT_KB_ATTACHMENTS.format(agent_id=agent_id))

    def attach(self, agent_id: Any, knowledge_base_id: Any, **options: Any) -> Any:
        payload = {"knowledge_base_id": knowledge_base_id, **options}
        return self.client.post(endpoints.AGENT_KB_ATTACHMENTS.format(agent_id=agent_id), payload)

    def update_attachment(self, agent_id: Any, attachment_id: Any, **options: Any) -> Any:
        return self.client.put(
            endpoints.AGENT_KB_ATTACHMENT_DETAIL.format(agent_id=agent_id, attachment_id=attachment_id), options
        )

    def detach(self, agent_id: Any, attachment_id: Any) -> Any:
        return self.client.delete(
            endpoints.AGENT_KB_ATTACHMENT_DETAIL.format(agent_id=agent_id, attachment_id=attachment_id)
        )

    def available(self, agent_id: Any) -> Any:
        return self.client.get(endpoints.AGENT_KB_AVAILABLE.format(agent_id=agent_id))
