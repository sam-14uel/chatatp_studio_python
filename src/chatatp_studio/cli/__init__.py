"""
studio_cli
==========

Standalone reference implementation of the ChatATP Studio CLI (`studio`).

This package is intentionally self-contained (no dependency on the official
`chatatp-studio` SDK) so that it can be developed, tested, and versioned on
its own. The internal `APIClient` in `studio_cli.api_client` is the single
seam that talks to the network -- when this code is later merged into the
official `chatatp-studio` Python package, that client can be swapped for
the official SDK client with minimal changes to services/commands.
"""

__version__ = "0.1.1"
