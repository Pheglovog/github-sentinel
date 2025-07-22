"""
Custom exceptions for GitHub Sentinel.
"""


class GitHubSentinelError(Exception):
    """Base exception for GitHub Sentinel."""
    
    def __init__(self, message: str, error_code: str = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class ConfigError(GitHubSentinelError):
    """Configuration related errors."""
    pass


class APIError(GitHubSentinelError):
    """API related errors."""
    
    def __init__(self, message: str, status_code: int = None, response_text: str = None):
        self.status_code = status_code
        self.response_text = response_text
        super().__init__(message)


class GitHubAPIError(APIError):
    """GitHub API specific errors."""
    
    def __init__(self, message: str, status_code: int = None, response_text: str = None, rate_limited: bool = False):
        self.rate_limited = rate_limited
        super().__init__(message, status_code, response_text)


class DatabaseError(GitHubSentinelError):
    """Database related errors."""
    pass


class SubscriptionError(GitHubSentinelError):
    """Subscription management errors."""
    pass


class NotificationError(GitHubSentinelError):
    """Notification system errors."""
    
    def __init__(self, message: str, channel: str = None):
        self.channel = channel
        super().__init__(message)


class ReportGenerationError(GitHubSentinelError):
    """Report generation errors."""
    pass


class SchedulerError(GitHubSentinelError):
    """Scheduler related errors."""
    pass


class ValidationError(GitHubSentinelError):
    """Data validation errors."""
    pass 