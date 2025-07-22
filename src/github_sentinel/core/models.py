"""
Core data models for GitHub Sentinel.
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, HttpUrl


class NotificationChannel(str, Enum):
    """Notification channel types."""
    EMAIL = "email"
    SLACK = "slack"
    WEBHOOK = "webhook"
    DISCORD = "discord"


class ReportFormat(str, Enum):
    """Report format types."""
    JSON = "json"
    MARKDOWN = "markdown" 
    HTML = "html"
    PDF = "pdf"


class SubscriptionStatus(str, Enum):
    """Subscription status types."""
    ACTIVE = "active"
    PAUSED = "paused"
    INACTIVE = "inactive"


class User(BaseModel):
    """User model."""
    id: Optional[int] = None
    username: str
    email: str
    github_token: str
    notification_preferences: Dict[NotificationChannel, bool] = Field(default_factory=dict)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class Repository(BaseModel):
    """GitHub repository model."""
    id: Optional[int] = None
    full_name: str  # owner/repo format
    owner: str
    name: str
    description: Optional[str] = None
    url: HttpUrl
    default_branch: str = "main"
    stars_count: int = 0
    forks_count: int = 0
    open_issues_count: int = 0
    language: Optional[str] = None
    last_updated: Optional[datetime] = None
    created_at: Optional[datetime] = None


class Subscription(BaseModel):
    """Repository subscription model."""
    id: Optional[int] = None
    user_id: int
    repository_id: int
    repository: Optional[Repository] = None
    status: SubscriptionStatus = SubscriptionStatus.ACTIVE
    notification_channels: List[NotificationChannel] = Field(default_factory=list)
    frequency: str = "daily"  # daily, weekly, monthly
    watch_events: List[str] = Field(default_factory=lambda: [
        "push", "pull_request", "issues", "releases"
    ])
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class CommitInfo(BaseModel):
    """Commit information."""
    sha: str
    message: str
    author: str
    date: datetime
    url: HttpUrl


class PullRequestInfo(BaseModel):
    """Pull request information."""
    number: int
    title: str
    author: str
    state: str
    created_at: datetime
    updated_at: datetime
    url: HttpUrl


class IssueInfo(BaseModel):
    """Issue information."""
    number: int
    title: str
    author: str
    state: str
    created_at: datetime
    updated_at: datetime
    labels: List[str] = Field(default_factory=list)
    url: HttpUrl


class ReleaseInfo(BaseModel):
    """Release information."""
    tag_name: str
    name: str
    author: str
    published_at: datetime
    prerelease: bool = False
    draft: bool = False
    url: HttpUrl


class RepositoryActivity(BaseModel):
    """Repository activity summary."""
    repository: Repository
    period_start: datetime
    period_end: datetime
    commits: List[CommitInfo] = Field(default_factory=list)
    pull_requests: List[PullRequestInfo] = Field(default_factory=list) 
    issues: List[IssueInfo] = Field(default_factory=list)
    releases: List[ReleaseInfo] = Field(default_factory=list)
    stars_change: int = 0
    forks_change: int = 0


class Report(BaseModel):
    """Report model."""
    id: Optional[int] = None
    subscription_id: int
    title: str
    content: Dict[str, Any]  # JSON content
    format: ReportFormat = ReportFormat.MARKDOWN
    generated_at: datetime = Field(default_factory=datetime.now)
    period_start: datetime
    period_end: datetime
    activities: List[RepositoryActivity] = Field(default_factory=list)
    summary: Optional[str] = None 