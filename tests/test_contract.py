"""Contract: SDK operation lists match sdk/operations.json / OpenAPI."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OPS = json.loads((ROOT / "operations.json").read_text())["operations"]
OPENAPI = json.loads((ROOT / "openapi.json").read_text())


def test_openapi_matches_api_docs() -> None:
    # sdk/openapi.json is a copy of the docs build; drift means `make sdk-sync` was skipped.
    docs = ROOT.parent / "js" / "api-docs" / "dist" / "openapi.json"
    if not docs.exists():  # published SDK repo has no js/api-docs
        return
    assert json.loads(docs.read_text()) == OPENAPI, "run `make sdk-sync`"


def test_operations_match_openapi() -> None:
    oids = set()
    for path, methods in OPENAPI["paths"].items():
        for method, op in methods.items():
            if isinstance(op, dict) and op.get("operationId"):
                oids.add(op["operationId"])
    catalog = {op["operationId"] for op in OPS}
    assert catalog == oids


def test_js_operation_ids_exported() -> None:
    text = (ROOT / "js" / "src" / "resources.generated.ts").read_text()
    for op in OPS:
        assert f'"{op["operationId"]}"' in text or f"'{op['operationId']}'" in text
        assert f"async {op['operationId']}(" in text


def test_python_methods_exist() -> None:
    text = (ROOT / "python" / "src" / "dogabot_sdk" / "resources_generated.py").read_text()
    assert "OPERATION_IDS" in text
    for op in OPS:
        assert f'"{op["operationId"]}"' in text


def test_go_methods_exist() -> None:
    text = (ROOT / "go" / "resources_generated.go").read_text()
    for op in OPS:
        assert f'"{op["operationId"]}"' in text
        method = op["operationId"][0].upper() + op["operationId"][1:]
        assert f"func (c *Client) {method}(" in text


def test_dotnet_methods_exist() -> None:
    text = (ROOT / "dotnet" / "src" / "Dogabot.Sdk" / "Resources.Generated.cs").read_text()
    for op in OPS:
        assert f'"{op["operationId"]}"' in text
        method = op["operationId"][0].upper() + op["operationId"][1:] + "Async"
        assert f"public Task<JsonElement> {method}(" in text
