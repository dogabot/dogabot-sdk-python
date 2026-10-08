"""Place a tiny paper market order (requires Idempotency-Key).

Safety: set CONFIRM_PLACE=1 to actually call the API. Default is dry-run print.
trading_mode stays paper — do not flip to live unless you intend to.
"""

from __future__ import annotations

import json
import os
import sys
import uuid

from dogabot_sdk import Client


def main() -> None:
    if not os.environ.get("DOGABOT_API_KEY"):
        print("Set DOGABOT_API_KEY=dbk_live_...", file=sys.stderr)
        sys.exit(1)

    body = {
        "exchange": os.environ.get("DOGABOT_EXCHANGE", "hyperliquid"),
        "symbol": os.environ.get("DOGABOT_SYMBOL", "BTC"),
        "side": "buy",
        "quantity": 0.001,
        "order_type": "market",
        "trading_mode": "paper",
        "broadcast_mode": "personal",
    }
    idem = os.environ.get("DOGABOT_IDEMPOTENCY_KEY") or f"example-paper-{uuid.uuid4()}"

    if os.environ.get("CONFIRM_PLACE") != "1":
        print("Dry-run only. Would POST placeorder with:")
        print(json.dumps({"body": body, "idempotency_key": idem}, indent=2))
        print("Re-run with CONFIRM_PLACE=1 to submit (still paper).")
        return

    with Client() as client:
        out = client.resources.post_terminal_placeorder(
            body=body,
            options={"idempotency_key": idem},
        )
        print(json.dumps(out, indent=2, default=str))


if __name__ == "__main__":
    main()
