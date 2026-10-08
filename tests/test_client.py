from __future__ import annotations

import httpx
import pytest
import respx

from dogabot_sdk import APIError, Client, OPERATION_IDS


@respx.mock
def test_get_me_success() -> None:
    route = respx.get("https://api.test/api/v1/me").mock(
        return_value=httpx.Response(200, json={"data": {"user_id": "u1"}})
    )
    with Client(api_key="dbk_live_test", base_url="https://api.test") as client:
        out = client.get_me()
    assert out == {"data": {"user_id": "u1"}}
    assert route.called
    assert route.calls[0].request.headers["Authorization"] == "Bearer dbk_live_test"
    assert route.calls[0].request.headers["User-Agent"].startswith("dogabot-sdk-python/")


def test_write_requires_idempotency() -> None:
    with Client(api_key="dbk_live_test", base_url="https://api.test") as client:
        with pytest.raises(ValueError, match="idempotency_key"):
            client.resources.post_terminal_placeorder(body={"symbol": "BTC"})


@respx.mock
def test_write_sends_idempotency() -> None:
    route = respx.post("https://api.test/api/v1/terminal/place-order").mock(
        return_value=httpx.Response(200, json={"data": {"ok": True}})
    )
    with Client(api_key="dbk_live_test", base_url="https://api.test") as client:
        client.resources.post_terminal_placeorder(
            body={"symbol": "BTC"},
            options={"idempotency_key": "k1"},
        )
    assert route.calls[0].request.headers["Idempotency-Key"] == "k1"


@respx.mock
def test_api_error() -> None:
    respx.get("https://api.test/api/v1/me").mock(
        return_value=httpx.Response(401, json={"error": "unauthorized"})
    )
    with Client(api_key="dbk_live_test", base_url="https://api.test", max_retries=0) as client:
        with pytest.raises(APIError) as ei:
            client.get_me()
    assert ei.value.status_code == 401
    assert str(ei.value) == "unauthorized"


def test_operation_ids_coverage() -> None:
    assert len(OPERATION_IDS) >= 100
    with Client(api_key="x", base_url="https://api.test") as client:
        for oid in OPERATION_IDS:
            import re

            snake = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", oid)
            snake = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", snake).lower().replace("__", "_")
            assert hasattr(client.resources, snake), snake
