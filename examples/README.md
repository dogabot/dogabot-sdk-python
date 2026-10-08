# dogabot-sdk examples (Python)

Set a live API key, then run from this directory (or any cwd):

```bash
export DOGABOT_API_KEY=dbk_live_...
pip install -e ..   # from sdk/python, once
python get_me.py
python get_ticker.py
python list_markets.py
# paper place only — refuses unless you opt in:
CONFIRM_PLACE=1 python place_paper_order.py
```

Docs: https://docs.dogabot.com/sdk/
