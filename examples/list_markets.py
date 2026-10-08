"""List markets with optional filters (GET /api/v1/markets)."""

from __future__ import annotations

import json
import os
import sys

from dogabot_sdk import Client


def main() -> None:
    if not os.environ.get("DOGABOT_API_KEY"):
        print("Set DOGABOT_API_KEY=dbk_live_...", file=sys.stderr)
        sys.exit(1)
    with Client() as client:
        markets = client.resources.get_markets(
            options={"query": {"limit": 5, "is_tradable": "true"}},
        )
        print(json.dumps(markets, indent=2, default=str))


if __name__ == "__main__":
    main()
