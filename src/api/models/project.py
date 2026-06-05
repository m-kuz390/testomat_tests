from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ProjectAttributes(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        populate_by_name=True,
    )

    title: str | None = None
    description: str | None = None
    status: str | None = None
    lang: str | None = None
    framework: str | None = None
    timezone: str | None = None
    github: str | None = None
    url: str | None = None
    avatar: str | None = None
    branch: str | None = None
    company: str | None = None
    demo: bool | None = None
    sync: bool | None = None
    attachments: Any | None = None
    jira: Any | None = None
    subscription: Any | None = None
    features: Any | None = None
    environments: Any | None = None
    tests_count: int | None = Field(default=None, alias="tests-count")
    jira_count: int | None = Field(default=None, alias="jira-count")
    api_key: str | None = Field(default=None, alias="api-key")
    testomatio_url: str | None = Field(default=None, alias="testomatio-url")
    record_url: str | None = Field(default=None, alias="record-url")
    living_doc_url: str | None = Field(default=None, alias="living-doc-url")
    company_slug: str | None = Field(default=None, alias="company-slug")
    has_living_docs: bool | None = Field(default=None, alias="has-living-docs")
    created_at: datetime | None = Field(default=None, alias="created-at")


class Project(BaseModel):
    id: str | None = None
    type: str | None = None
    attributes: ProjectAttributes | None = None
    relationships: dict[str, Any] | None = None
