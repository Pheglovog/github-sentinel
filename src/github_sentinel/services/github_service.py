"""
GitHub API service for fetching repository data and activity.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import asyncio
import httpx
from github import Github, GithubException
from github.Repository import Repository as GithubRepo
from github.PaginatedList import PaginatedList

from ..core.models import (
    Repository, CommitInfo, PullRequestInfo, IssueInfo, 
    ReleaseInfo, RepositoryActivity
)
from ..core.config import Config
from ..core.exceptions import GitHubAPIError, ConfigError
from ..utils.logger import get_logger


logger = get_logger(__name__)


class GitHubService:
    """Service for interacting with GitHub API."""
    
    def __init__(self, config: Config):
        """Initialize GitHub service."""
        self.config = config
        
        if not config.github.token:
            raise ConfigError("GitHub token is required")
        
        self.client = Github(
            config.github.token,
            base_url=config.github.base_url,
            timeout=config.github.timeout
        )
    
    async def get_repository_info(self, full_name: str) -> Repository:
        """Get repository information."""
        try:
            repo = self.client.get_repo(full_name)
            return self._convert_repository(repo)
        except GithubException as e:
            raise GitHubAPIError(
                f"Failed to fetch repository {full_name}: {e.data}",
                status_code=e.status,
                response_text=str(e.data)
            )
    
    async def get_repository_activity(
        self, 
        full_name: str, 
        since: datetime, 
        until: Optional[datetime] = None
    ) -> RepositoryActivity:
        """Get repository activity for a specific time period."""
        if until is None:
            until = datetime.now()
        
        try:
            repo = self.client.get_repo(full_name)
            repository = self._convert_repository(repo)
            
            # Fetch different types of activities
            commits = await self._get_commits(repo, since, until)
            pull_requests = await self._get_pull_requests(repo, since, until)
            issues = await self._get_issues(repo, since, until)
            releases = await self._get_releases(repo, since, until)
            
            # Get repository stats changes
            stars_change, forks_change = await self._get_repository_changes(repo, since, until)
            
            return RepositoryActivity(
                repository=repository,
                period_start=since,
                period_end=until,
                commits=commits,
                pull_requests=pull_requests,
                issues=issues,
                releases=releases,
                stars_change=stars_change,
                forks_change=forks_change
            )
            
        except GithubException as e:
            raise GitHubAPIError(
                f"Failed to fetch activity for {full_name}: {e.data}",
                status_code=e.status,
                response_text=str(e.data),
                rate_limited=e.status == 403
            )
    
    async def validate_repository_access(self, full_name: str) -> bool:
        """Validate that we can access the repository."""
        try:
            repo = self.client.get_repo(full_name)
            repo.name  # Trigger API call
            return True
        except GithubException as e:
            if e.status == 404:
                return False
            raise GitHubAPIError(
                f"Failed to validate repository access: {e.data}",
                status_code=e.status
            )
    
    async def search_repositories(self, query: str, limit: int = 10) -> List[Repository]:
        """Search for repositories."""
        try:
            repositories = self.client.search_repositories(query)
            results = []
            
            for repo in repositories[:limit]:
                results.append(self._convert_repository(repo))
            
            return results
            
        except GithubException as e:
            raise GitHubAPIError(
                f"Repository search failed: {e.data}",
                status_code=e.status
            )
    
    def _convert_repository(self, repo: GithubRepo) -> Repository:
        """Convert GitHub repository to our model."""
        return Repository(
            full_name=repo.full_name,
            owner=repo.owner.login,
            name=repo.name,
            description=repo.description,
            url=repo.html_url,
            default_branch=repo.default_branch,
            stars_count=repo.stargazers_count,
            forks_count=repo.forks_count,
            open_issues_count=repo.open_issues_count,
            language=repo.language,
            last_updated=repo.updated_at,
            created_at=repo.created_at
        )
    
    async def _get_commits(
        self, 
        repo: GithubRepo, 
        since: datetime, 
        until: datetime
    ) -> List[CommitInfo]:
        """Get commits for the specified period."""
        commits = []
        try:
            for commit in repo.get_commits(since=since, until=until):
                commits.append(CommitInfo(
                    sha=commit.sha,
                    message=commit.commit.message,
                    author=commit.commit.author.name or commit.commit.author.email,
                    date=commit.commit.author.date,
                    url=commit.html_url
                ))
                
                # Limit to avoid rate limiting
                if len(commits) >= 50:
                    break
                    
        except GithubException as e:
            logger.warning(f"Failed to fetch commits: {e}")
        
        return commits
    
    async def _get_pull_requests(
        self, 
        repo: GithubRepo, 
        since: datetime, 
        until: datetime
    ) -> List[PullRequestInfo]:
        """Get pull requests for the specified period."""
        pull_requests = []
        try:
            # Get PRs updated in the period
            for pr in repo.get_pulls(state='all', sort='updated'):
                if pr.updated_at < since:
                    break  # PRs are sorted by update date, so we can break
                
                if pr.updated_at <= until:
                    pull_requests.append(PullRequestInfo(
                        number=pr.number,
                        title=pr.title,
                        author=pr.user.login,
                        state=pr.state,
                        created_at=pr.created_at,
                        updated_at=pr.updated_at,
                        url=pr.html_url
                    ))
                
                # Limit to avoid rate limiting
                if len(pull_requests) >= 25:
                    break
                    
        except GithubException as e:
            logger.warning(f"Failed to fetch pull requests: {e}")
        
        return pull_requests
    
    async def _get_issues(
        self, 
        repo: GithubRepo, 
        since: datetime, 
        until: datetime
    ) -> List[IssueInfo]:
        """Get issues for the specified period."""
        issues = []
        try:
            for issue in repo.get_issues(state='all', since=since):
                if issue.updated_at > until:
                    continue
                
                # Skip pull requests (GitHub API includes PRs in issues)
                if issue.pull_request:
                    continue
                    
                issues.append(IssueInfo(
                    number=issue.number,
                    title=issue.title,
                    author=issue.user.login,
                    state=issue.state,
                    created_at=issue.created_at,
                    updated_at=issue.updated_at,
                    labels=[label.name for label in issue.labels],
                    url=issue.html_url
                ))
                
                # Limit to avoid rate limiting
                if len(issues) >= 25:
                    break
                    
        except GithubException as e:
            logger.warning(f"Failed to fetch issues: {e}")
        
        return issues
    
    async def _get_releases(
        self, 
        repo: GithubRepo, 
        since: datetime, 
        until: datetime
    ) -> List[ReleaseInfo]:
        """Get releases for the specified period."""
        releases = []
        try:
            for release in repo.get_releases():
                if release.published_at and release.published_at >= since and release.published_at <= until:
                    releases.append(ReleaseInfo(
                        tag_name=release.tag_name,
                        name=release.title or release.tag_name,
                        author=release.author.login if release.author else "Unknown",
                        published_at=release.published_at,
                        prerelease=release.prerelease,
                        draft=release.draft,
                        url=release.html_url
                    ))
                    
        except GithubException as e:
            logger.warning(f"Failed to fetch releases: {e}")
        
        return releases
    
    async def _get_repository_changes(
        self, 
        repo: GithubRepo, 
        since: datetime, 
        until: datetime
    ) -> tuple[int, int]:
        """Calculate changes in stars and forks (simplified implementation)."""
        # Note: This is a simplified implementation
        # For accurate historical data, you'd need to store snapshots
        # or use GitHub's traffic API (which has limited history)
        try:
            current_stars = repo.stargazers_count
            current_forks = repo.forks_count
            
            # For demo purposes, we'll return 0 changes
            # In a real implementation, you'd compare with historical data
            return 0, 0
            
        except GithubException:
            return 0, 0 