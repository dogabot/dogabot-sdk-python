from __future__ import annotations

from typing import Any, Mapping

import httpx


class APIError(Exception):
    def __init__(
        self,
        message: str,
        *,
        status_code: int,
        body: Mapping[str, Any] | None,
        headers: httpx.Headers,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.body = body
        self.headers = headers
