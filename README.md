# ChatATP Studio SDK

Python SDK for building and interacting with agents created in ChatATP Studio.

- Async-first API
- Conversation lifecycle management
- Streaming support
- Fully typed

![PyPI](https://img.shields.io/pypi/v/chatatp-studio)
![Python](https://img.shields.io/pypi/pyversions/chatatp-studio)

# chatatp-studio

Official Python SDK for the [ChatATP Studio](https://studio.chat-atp.com) Developer API.

## Requirements

- Python 3.10+

## Installation

```bash
pip install chatatp-studio
```

## Quick start

```python
import asyncio
from chatatp_studio import ChatATPClient

async def main():
    client = ChatATPClient(api_key="chatatp_sk_...")

    # Send a message — conversation lifecycle handled automatically
    result = await client.chat(
        agent_id=7,
        external_user_id="user_12345",
        message="Do you ship to Lagos?",
    )

    print(result.agent_message.content)
    # → "Yes, shipping is available."

    await client.aclose()

asyncio.run(main())
```

## Context manager

```python
async with ChatATPClient(api_key="chatatp_sk_...") as client:
    result = await client.chat(
        agent_id=7,
        external_user_id="user_12345",
        message="Hello!",
    )
```

## Streaming

```python
async for event in await client.chat_stream(
    agent_id=7,
    external_user_id="user_12345",
    message="Give me a summary of your return policy.",
):
    if event.type == "agent.response.completed":
        print(event.data)
```

## Resources

```python
# Agents
page  = await client.agents.list()
agent = await client.agents.retrieve(7)

# Conversations
conv = await client.conversations.create(7, "user_12345")
page = await client.conversations.list(agent_id=7)
await client.conversations.delete(conv.id)

# Messages
history = await client.messages.list(conv.id)
reply   = await client.messages.send(conv.id, "Hello")

# Usage
usage = await client.usage.retrieve()
```

## Error handling

```python
from chatatp_studio import NotFoundError, RateLimitError

try:
    await client.agents.retrieve(999)
except NotFoundError:
    print("Not found")
except RateLimitError:
    print("Rate limited")
```

## License

MIT
