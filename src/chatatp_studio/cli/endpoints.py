"""Central registry of Studio backend API paths.

Every path used by the CLI is declared here, in one place, so that the
implementation can be corrected or extended without hunting through
services and commands.

Paths marked "(documented)" are taken verbatim from the generated
ChatATP Studio API reference. Paths marked "(inferred)" were not
individually enumerated in the reference -- only the base path and the
response schema were documented -- and are inferred by following the
same REST conventions used by the fully-documented resources (teams,
users, platforms, knowledge bases): a collection endpoint at the base
path, and a detail endpoint at ``<base>/<id>/`` supporting
GET/PATCH/DELETE. If your backend uses different paths for these,
adjust them here; nothing else in the codebase needs to change.
"""
from __future__ import annotations

# ---------------------------------------------------------------------------
# Auth & users                                                 (documented)
# ---------------------------------------------------------------------------
AUTH_SIGNUP = "/dapi/auth/signup/"
AUTH_SIGNIN = "/dapi/auth/signin/"
AUTH_FORGOT_PASSWORD = "/dapi/auth/forgot-password/"
AUTH_RESET_PASSWORD = "/dapi/auth/reset-password/"
AUTH_SIGNOUT = "/dapi/auth/signout/"
AUTH_ME = "/dapi/auth/me/"
AUTH_PROFILE = "/dapi/auth/profile/"
AUTH_ONBOARDING = "/dapi/auth/onboarding/"
AUTH_TOKEN_REFRESH = "/dapi/auth/token/refresh/"
AUTH_OAUTH_PROVIDERS = "/dapi/auth/oauth/providers/"
AUTH_OAUTH_START = "/dapi/auth/oauth/{provider}/start/"
AUTH_OAUTH_CALLBACK = "/dapi/auth/oauth/{provider}/callback/"

USERS = "/dapi/users/"
USER_DETAIL = "/dapi/users/{id}/"
USER_INVITATIONS = "/dapi/users/invitations/"
USER_INVITATION_ACCEPT = "/dapi/users/invitations/{token}/accept/"
USER_INVITATION_DECLINE = "/dapi/users/invitations/{token}/decline/"

# ---------------------------------------------------------------------------
# Teams                                                        (documented)
# ---------------------------------------------------------------------------
TEAMS = "/dapi/teams/"
TEAM_DETAIL = "/dapi/teams/{id}/"
TEAM_MEMBERS = "/dapi/teams/{id}/members/"
TEAM_MEMBER_DETAIL = "/dapi/teams/{id}/members/{user_id}/"
TEAM_INVITATIONS = "/dapi/teams/{id}/invitations/"
TEAM_INVITATION_ACCEPT = "/dapi/teams/invitations/{token}/accept/"
TEAM_INVITATION_DECLINE = "/dapi/teams/invitations/{token}/decline/"

# ---------------------------------------------------------------------------
# Platforms                                                    (documented)
# ---------------------------------------------------------------------------
PLATFORM_CATALOG = "/dapi/platforms/catalog/"
PLATFORM_CATALOG_DETAIL = "/dapi/platforms/catalog/{id}/"
PLATFORM_CONFIGS = "/dapi/platforms/configs/"
PLATFORM_CONFIG_DETAIL = "/dapi/platforms/configs/{id}/"
PLATFORM_CONNECT = "/dapi/platforms/connect/"
PLATFORM_DISCONNECT = "/dapi/platforms/disconnect/"

# ---------------------------------------------------------------------------
# Knowledge bases                                              (documented)
# ---------------------------------------------------------------------------
KB_LIST = "/dapi/knowledge-bases/"
KB_DETAIL = "/dapi/knowledge-bases/{id}/"
KB_DOCUMENTS = "/dapi/knowledge-bases/{id}/documents/"
KB_DOCUMENT_DETAIL = "/dapi/knowledge-bases/{id}/documents/{doc_id}/"
KB_DOCUMENT_CHUNKS = "/dapi/knowledge-bases/{id}/documents/{doc_id}/chunks/"
KB_DOMAINS = "/dapi/knowledge-bases/{id}/domains/"
KB_DOMAIN_DETAIL = "/dapi/knowledge-bases/{id}/domains/{domain_id}/"
KB_DOMAIN_CRAWL = "/dapi/knowledge-bases/{id}/domains/{domain_id}/crawl/"
KB_STATS = "/dapi/knowledge-bases/{id}/stats/"
KB_SEARCH = "/dapi/knowledge-bases/{id}/search/"

AGENT_KB_STATS = "/dapi/agents/{agent_id}/kb/stats/"
AGENT_KB_DOCUMENTS = "/dapi/agents/{agent_id}/kb/documents/"
AGENT_KB_DOCUMENT_DETAIL = "/dapi/agents/{agent_id}/kb/documents/{doc_id}/"
AGENT_KB_DOCUMENT_CHUNKS = "/dapi/agents/{agent_id}/kb/documents/{doc_id}/chunks/"
AGENT_KB_DOMAINS = "/dapi/agents/{agent_id}/kb/domains/"
AGENT_KB_DOMAIN_DETAIL = "/dapi/agents/{agent_id}/kb/domains/{domain_id}/"
AGENT_KB_DOMAIN_CRAWL = "/dapi/agents/{agent_id}/kb/domains/{domain_id}/crawl/"
AGENT_KB_SEARCH = "/dapi/agents/{agent_id}/kb/search/"
AGENT_KB_TEST = "/dapi/agents/{agent_id}/kb/test/"

AGENT_KB_ATTACHMENTS = "/dapi/agents/{agent_id}/knowledge-bases/"
AGENT_KB_ATTACHMENT_DETAIL = "/dapi/agents/{agent_id}/knowledge-bases/{attachment_id}/"
AGENT_KB_AVAILABLE = "/dapi/agents/{agent_id}/knowledge-bases/available/"

# ---------------------------------------------------------------------------
# Assistant / Copilot                                          (documented)
# ---------------------------------------------------------------------------
ASSISTANT_CHAT = "/dapi/assistant/chat/"
ASSISTANT_CHAT_STREAM = "/dapi/assistant/chat/stream/"
ASSISTANT_CONFIG = "/dapi/assistant/config/"
ASSISTANT_SESSIONS = "/dapi/assistant/sessions/"
ASSISTANT_SESSION_CREATE = "/dapi/assistant/sessions/create/"
ASSISTANT_SESSION_DETAIL = "/dapi/assistant/sessions/{id}/"
ASSISTANT_SESSION_STATE = "/dapi/assistant/sessions/{id}/state/"
ASSISTANT_SESSION_STOP = "/dapi/assistant/sessions/{id}/stop/"
ASSISTANT_SESSION_RETRY = "/dapi/assistant/sessions/{id}/retry/"
ASSISTANT_SESSION_EVENTS = "/dapi/assistant/sessions/{id}/events/"
ASSISTANT_SESSION_EVENT_DETAIL = "/dapi/assistant/sessions/{id}/events/{event_id}/"
ASSISTANT_SESSION_EVENT_REGENERATE = "/dapi/assistant/sessions/{id}/events/{event_id}/regenerate/"
ASSISTANT_SESSION_EVENT_FEEDBACK = "/dapi/assistant/sessions/{id}/events/{event_id}/feedback/"
ASSISTANT_ANALYTICS = "/dapi/assistant/analytics/"

# ---------------------------------------------------------------------------
# Agents                                                        (inferred)
# Base path /dapi/agents/ is documented; the list/detail CRUD paths follow
# the same convention as every other documented resource collection.
# ---------------------------------------------------------------------------
AGENTS = "/dapi/agents/"
AGENT_DETAIL = "/dapi/agents/{id}/"
AGENT_PREVIEW = "/dapi/agents/{id}/preview/"

# ---------------------------------------------------------------------------
# MCP                                                           (inferred)
# Base path /dapi/mcp/ is documented, together with the MCPServer and
# MCPConnection serializers; collection/detail paths follow REST convention.
# ---------------------------------------------------------------------------
MCP_SERVERS = "/dapi/mcp/servers/"
MCP_SERVER_DETAIL = "/dapi/mcp/servers/{id}/"
MCP_CONNECTIONS = "/dapi/mcp/connections/"
MCP_CONNECTION_DETAIL = "/dapi/mcp/connections/{id}/"
MCP_OAUTH_INITIATE = "/dapi/mcp/connections/{id}/oauth/initiate/"

# ---------------------------------------------------------------------------
# HTTP API tools                                                (inferred)
# Base path /dapi/http-api/ is documented, together with the HttpApiTool and
# HttpApiConnection serializers, and a prose description of an execute
# endpoint and an OAuth initiate endpoint. Paths follow REST convention.
# ---------------------------------------------------------------------------
HTTP_API_TOOLS = "/dapi/http-api/tools/"
HTTP_API_TOOL_DETAIL = "/dapi/http-api/tools/{id}/"
HTTP_API_CONNECTIONS = "/dapi/http-api/connections/"
HTTP_API_CONNECTION_DETAIL = "/dapi/http-api/connections/{id}/"
HTTP_API_CONNECTION_EXECUTE = "/dapi/http-api/connections/{id}/execute/"
HTTP_API_OAUTH_INITIATE = "/dapi/http-api/connections/{id}/oauth/initiate/"

# ---------------------------------------------------------------------------
# LLM providers                                                 (inferred)
# Base path /dapi/llm/ is documented, together with the Provider and
# ProviderConfig serializers, and a "provider models" endpoint. Paths
# follow REST convention.
# ---------------------------------------------------------------------------
LLM_PROVIDERS = "/dapi/llm/providers/"
LLM_PROVIDER_DETAIL = "/dapi/llm/providers/{id}/"
LLM_PROVIDER_MODELS = "/dapi/llm/providers/{id}/models/"
LLM_PROVIDER_CONFIGS = "/dapi/llm/configs/"
LLM_PROVIDER_CONFIG_DETAIL = "/dapi/llm/configs/{id}/"
