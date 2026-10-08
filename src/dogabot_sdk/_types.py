from __future__ import annotations

from typing import Any, Mapping, MutableMapping, TypedDict

JsonValue = Any


class RequestOptions(TypedDict, total=False):
    query: Mapping[str, Any]
    headers: MutableMapping[str, str]
    idempotency_key: str
    timeout: float
