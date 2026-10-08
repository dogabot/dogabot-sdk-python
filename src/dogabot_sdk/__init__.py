"""Official dogabot REST API SDK for Python."""

from dogabot_sdk._client import Client
from dogabot_sdk._errors import APIError
from dogabot_sdk.resources_generated import OPERATION_IDS, Resources

__all__ = ["Client", "APIError", "Resources", "OPERATION_IDS"]
