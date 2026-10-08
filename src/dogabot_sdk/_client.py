from __future__ import annotations

import os
import time
from importlib.metadata import PackageNotFoundError, version
from typing import Any

import httpx

from dogabot_sdk._errors import APIError
from dogabot_sdk._types import JsonValue, RequestOptions
from dogabot_sdk.resources_generated import Resources

DEFAULT_BASE = "https://api.dogabot.com"


def _pkg_version() -> str:
    try:
        return version("dogabot-sdk")
    except PackageNotFoundError:
        return "0.1.0"


class Client:
    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str = DEFAULT_BASE,
        timeout: float = 30.0,
        max_retries: int = 2,
        http_client: httpx.Client | None = None,
        user_agent: str | None = None,
    ) -> None:
        key = api_key or os.environ.get("DOGABOT_API_KEY")
        if not key:
            raise ValueError("api_key is required (pass api_key= or set DOGABOT_API_KEY)")
        self.api_key = key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.user_agent = user_agent or f"dogabot-sdk-python/{_pkg_version()}"
        self._owns_client = http_client is None
        self._http = http_client or httpx.Client(timeout=timeout)
        self.resources = Resources(self)

    def close(self) -> None:
        if self._owns_client:
            self._http.close()

    def __enter__(self) -> Client:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    def get_me(self, *, options: RequestOptions | None = None) -> JsonValue:
        return self.resources.get_me(options=options)

    def request(
        self,
        *,
        method: str,
        path: str,
        body: JsonValue | None = None,
        write: bool = False,
        options: RequestOptions | None = None,
    ) -> JsonValue:
        opts = options or {}
        idem = opts.get("idempotency_key")
        if write and not idem:
            raise ValueError(f"idempotency_key is required for write operation {method} {path}")

        url = path if path.startswith("http") else f"{self.base_url}{path}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
            "User-Agent": self.user_agent,
        }
        extra = opts.get("headers")
        if extra:
            headers.update(extra)
        if idem:
            headers["Idempotency-Key"] = idem

        params = opts.get("query")
        timeout = opts.get("timeout", self.timeout)

        attempt = 0
        while True:
            resp = self._http.request(
                method,
                url,
                params=params,
                json=body if body is not None else None,
                headers=headers,
                timeout=timeout,
            )
            if resp.is_success:
                if not resp.content:
                    return None
                try:
                    return resp.json()
                except Exception:
                    return resp.text

            retryable = resp.status_code == 429 or resp.status_code >= 500
            if retryable and attempt < self.max_retries:
                attempt += 1
                retry_after = resp.headers.get("Retry-After")
                try:
                    wait = float(retry_after) if retry_after else min(2**attempt, 8)
                except ValueError:
                    wait = min(2**attempt, 8)
                time.sleep(wait)
                continue

            body_json: dict[str, Any] | None
            try:
                parsed = resp.json()
                body_json = parsed if isinstance(parsed, dict) else None
            except Exception:
                body_json = None
            msg = (
                body_json.get("error")
                if body_json and isinstance(body_json.get("error"), str)
                else f"HTTP {resp.status_code} {method} {path}"
            )
            raise APIError(msg, status_code=resp.status_code, body=body_json, headers=resp.headers)
