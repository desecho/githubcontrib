"""Custom Types."""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, TypeAlias

from typing_extensions import NotRequired, TypedDict


class ContextVariables(TypedDict):
    """Context variables."""

    DEBUG: bool
    ADMIN_EMAIL: str
    GOOGLE_ANALYTICS_ID: str


class CommitType(TypedDict):
    """Commit type."""

    url: str
    date: datetime
    message: str


class TemplatesSettingsOptions(TypedDict):
    """Templates settings options."""

    context_processors: List[str]
    loaders: List[str | Tuple[str, List[str]]]
    builtins: List[str]


class TemplatesSettings(TypedDict):
    """Templates settings."""

    NAME: str
    BACKEND: str
    DIRS: NotRequired[List[str]]
    OPTIONS: NotRequired[TemplatesSettingsOptions]
    APP_DIRS: NotRequired[Optional[bool]]


UntypedObject: TypeAlias = Dict[str, Any]
