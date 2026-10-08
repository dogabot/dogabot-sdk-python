# dogabot-sdk (Python)

Official REST client for the [dogabot public API](https://docs.dogabot.com/).

```bash
pip install dogabot-sdk
# or: uv add dogabot-sdk
# from source: pip install "dogabot-sdk @ git+https://github.com/dogabot/dogabot-sdk-python.git"
```

```python
from dogabot_sdk import Client

with Client(api_key="dbk_live_...") as client:  # or DOGABOT_API_KEY
    me = client.get_me()
    print(me)
```

Writes require an idempotency key:

```python
client.resources.post_terminal_placeorder(
    body={"exchange": "hyperliquid", "symbol": "BTC", "side": "buy", "quantity": 0.001,
          "order_type": "market", "trading_mode": "paper", "broadcast_mode": "personal"},
    options={"idempotency_key": "place-paper-btc-1"},
)
```

**Backend use only** for API keys — do not embed `dbk_live_…` in browser bundles.

Runnable samples: [`examples/`](./examples/).

Docs: https://docs.dogabot.com/sdk/ · MCP: https://docs.dogabot.com/mcp/
