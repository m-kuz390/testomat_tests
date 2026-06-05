from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class TestAttributes(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        populate_by_name=True,
    )

    title: str | None = None
    description: str | None = None
    state: str | None = None
    priority: str | None = None
    emoji: str | None = None
    file: str | None = None
    sync: bool | None = None
    labels: list[str] | None = None
    tags: list[str] | None = None
    issues: list[str] | None = None
    milestones: list[Any] | None = None
    attachments: list[Any] | None = None
    params: Any | None = None
    position: int | None = None
    comments_count: int | None = Field(default=None, alias="comments-count")
    forks_count: int | None = Field(default=None, alias="forks-count")
    jira_issues: list[str] | None = Field(default=None, alias="jira-issues")
    is_branched: bool | None = Field(default=None, alias="is-branched")
    is_detail: bool | None = Field(default=None, alias="is-detail")
    is_linked: bool | None = Field(default=None, alias="is-linked")
    is_shared: bool | None = Field(default=None, alias="is-shared")
    has_examples: bool | None = Field(default=None, alias="has-examples")
    suite_id: str | None = Field(default=None, alias="suite-id")
    template_id: str | None = Field(default=None, alias="template-id")
    import_id: str | None = Field(default=None, alias="import-id")
    assigned_to: str | None = Field(default=None, alias="assigned-to")
    created_by: int | None = Field(default=None, alias="created-by")
    public_title: str | None = Field(default=None, alias="public-title")
    to_url: str | None = Field(default=None, alias="to-url")
    created_at: datetime | None = Field(default=None, alias="created-at")
    updated_at: datetime | None = Field(default=None, alias="updated-at")
    run_at: datetime | None = Field(default=None, alias="run-at")


class Test(BaseModel):
    id: str | None = None
    type: str | None = None
    attributes: TestAttributes | None = None
    relationships: dict[str, Any] | None = None
