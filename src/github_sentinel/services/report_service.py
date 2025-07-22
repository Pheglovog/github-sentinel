"""
Report generation service for creating repository activity reports.
"""

from datetime import datetime
from typing import List, Dict, Any
from jinja2 import Template

from ..core.models import Report, RepositoryActivity, ReportFormat
from ..core.config import Config
from ..core.exceptions import ReportGenerationError
from ..utils.logger import get_logger

logger = get_logger(__name__)


class ReportService:
    """Service for generating activity reports."""
    
    def __init__(self, config: Config):
        """Initialize report service."""
        self.config = config
    
    async def generate_report(
        self,
        activities: List[RepositoryActivity],
        subscription_id: int,
        report_format: ReportFormat = ReportFormat.MARKDOWN,
        custom_template: str = None
    ) -> Report:
        """Generate a comprehensive activity report."""
        
        period_start = min(activity.period_start for activity in activities) if activities else datetime.now()
        period_end = max(activity.period_end for activity in activities) if activities else datetime.now()
        
        # Generate title
        repo_names = [activity.repository.full_name for activity in activities]
        title = self._generate_title(repo_names, period_start, period_end)
        
        # Generate content based on format
        if report_format == ReportFormat.MARKDOWN:
            content = await self._generate_markdown_report(activities)
        elif report_format == ReportFormat.HTML:
            content = await self._generate_html_report(activities)
        elif report_format == ReportFormat.JSON:
            content = await self._generate_json_report(activities)
        else:
            raise ReportGenerationError(f"Unsupported report format: {report_format}")
        
        # Generate summary
        summary = self._generate_summary(activities)
        
        report = Report(
            subscription_id=subscription_id,
            title=title,
            content=content,
            format=report_format,
            period_start=period_start,
            period_end=period_end,
            activities=activities,
            summary=summary
        )
        
        return report
    
    def _generate_title(self, repo_names: List[str], start: datetime, end: datetime) -> str:
        """Generate report title."""
        if len(repo_names) == 1:
            return f"Activity Report for {repo_names[0]} ({start.date()} - {end.date()})"
        elif len(repo_names) <= 3:
            repos = ", ".join(repo_names)
            return f"Activity Report for {repos} ({start.date()} - {end.date()})"
        else:
            return f"Activity Report for {len(repo_names)} repositories ({start.date()} - {end.date()})"
    
    async def _generate_markdown_report(self, activities: List[RepositoryActivity]) -> Dict[str, Any]:
        """Generate Markdown format report."""
        template = Template("""
# Repository Activity Report

## Summary
{{ summary }}

{% for activity in activities %}
## {{ activity.repository.full_name }}

**Repository Info:**
- ⭐ Stars: {{ activity.repository.stars_count }}
- 🍴 Forks: {{ activity.repository.forks_count }}
- 🐛 Open Issues: {{ activity.repository.open_issues_count }}
- 🛠️ Language: {{ activity.repository.language or "N/A" }}

### Activity Summary
- 📝 Commits: {{ activity.commits|length }}
- 🔀 Pull Requests: {{ activity.pull_requests|length }}
- 🐛 Issues: {{ activity.issues|length }}
- 🚀 Releases: {{ activity.releases|length }}

{% if activity.commits %}
### Recent Commits
{% for commit in activity.commits[:5] %}
- `{{ commit.sha[:8] }}` - {{ commit.message[:80] }}{% if commit.message|length > 80 %}...{% endif %} ({{ commit.author }})
{% endfor %}
{% if activity.commits|length > 5 %}
*... and {{ activity.commits|length - 5 }} more commits*
{% endif %}
{% endif %}

{% if activity.pull_requests %}
### Recent Pull Requests
{% for pr in activity.pull_requests[:5] %}
- #{{ pr.number }} - {{ pr.title }} ({{ pr.state }})
{% endfor %}
{% if activity.pull_requests|length > 5 %}
*... and {{ activity.pull_requests|length - 5 }} more PRs*
{% endif %}
{% endif %}

{% if activity.issues %}
### Recent Issues
{% for issue in activity.issues[:5] %}
- #{{ issue.number }} - {{ issue.title }} ({{ issue.state }})
{% endfor %}
{% if activity.issues|length > 5 %}
*... and {{ activity.issues|length - 5 }} more issues*
{% endif %}
{% endif %}

{% if activity.releases %}
### Recent Releases
{% for release in activity.releases %}
- 🏷️ {{ release.tag_name }} - {{ release.name }} ({{ release.published_at.strftime('%Y-%m-%d') }})
{% endfor %}
{% endif %}

---
{% endfor %}

*Report generated on {{ now.strftime('%Y-%m-%d %H:%M:%S') }}*
        """)
        
        # Generate summary
        total_commits = sum(len(activity.commits) for activity in activities)
        total_prs = sum(len(activity.pull_requests) for activity in activities)
        total_issues = sum(len(activity.issues) for activity in activities)
        total_releases = sum(len(activity.releases) for activity in activities)
        
        summary = f"📊 Total activity across {len(activities)} repositories: {total_commits} commits, {total_prs} PRs, {total_issues} issues, {total_releases} releases"
        
        markdown_content = template.render(
            activities=activities,
            summary=summary,
            now=datetime.now()
        )
        
        return {
            "markdown": markdown_content.strip(),
            "summary": summary
        }
    
    async def _generate_html_report(self, activities: List[RepositoryActivity]) -> Dict[str, Any]:
        """Generate HTML format report."""
        # TODO: Implement HTML report generation
        return {"html": "<h1>HTML Report</h1><p>Coming soon...</p>"}
    
    async def _generate_json_report(self, activities: List[RepositoryActivity]) -> Dict[str, Any]:
        """Generate JSON format report."""
        return {
            "activities": [
                {
                    "repository": activity.repository.dict(),
                    "period": {
                        "start": activity.period_start.isoformat(),
                        "end": activity.period_end.isoformat()
                    },
                    "commits": [commit.dict() for commit in activity.commits],
                    "pull_requests": [pr.dict() for pr in activity.pull_requests],
                    "issues": [issue.dict() for issue in activity.issues],
                    "releases": [release.dict() for release in activity.releases]
                }
                for activity in activities
            ]
        }
    
    def _generate_summary(self, activities: List[RepositoryActivity]) -> str:
        """Generate activity summary."""
        if not activities:
            return "No activity to report."
        
        total_commits = sum(len(activity.commits) for activity in activities)
        total_prs = sum(len(activity.pull_requests) for activity in activities)
        total_issues = sum(len(activity.issues) for activity in activities)
        total_releases = sum(len(activity.releases) for activity in activities)
        
        return f"Total activity: {total_commits} commits, {total_prs} pull requests, {total_issues} issues, {total_releases} releases across {len(activities)} repositories" 