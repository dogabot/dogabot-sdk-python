"""Fetch a ticker with query params (GET /api/v1/ticker)."""

from __future__ import annotations

import json
import os
import sys

from dogabot_sdk import Client


def main() -> None:
    if not os.environ.get("DOGABOT_API_KEY"):
        print("Set DOGABOT_API_KEY=dbk_live_...", file=sys.stderr)
        sys.exit(1)
    exchange = os.environ.get("DOGABOT_EXCHANGE", "hyperliquid")
    symbol = os.environ.get("DOGABOT_SYMBOL", "BTC")
    with Client() as client:
        ticker = client.resources.get_ticker(
            options={"query": {"exchange": exchange, "symbol": symbol}},
        )
        print(json.dumps(ticker, indent=2, default=str))


if __name__ == "__main__":
    main()
