"""
Helper functions and utilities.
"""

import re
from datetime import datetime
from typing import Optional, Tuple
from urllib.parse import urlparse


def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Format datetime object to string."""
    return dt.strftime(format_str)


def parse_github_url(url: str) -> Optional[str]:
    """
    Parse GitHub URL and return owner/repo format.
    
    Examples:
        https://github.com/owner/repo -> owner/repo
        https://github.com/owner/repo.git -> owner/repo
        git@github.com:owner/repo.git -> owner/repo
    """
    # Handle different GitHub URL formats
    patterns = [
        r"github\.com[:/]([^/]+)/([^/.]+)(?:\.git)?/?$",  # HTTP/HTTPS and SSH
        r"^([^/]+)/([^/]+)$"  # Already in owner/repo format
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            owner, repo = match.groups()
            return f"{owner}/{repo}"
    
    return None


def validate_github_repo_name(repo_name: str) -> bool:
    """
    Validate GitHub repository name format (owner/repo).
    """
    pattern = r"^[a-zA-Z0-9._-]+/[a-zA-Z0-9._-]+$"
    return bool(re.match(pattern, repo_name))


def truncate_string(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate string to specified length."""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def safe_get(dictionary: dict, keys: list, default=None):
    """Safely get nested dictionary value."""
    for key in keys:
        if isinstance(dictionary, dict) and key in dictionary:
            dictionary = dictionary[key]
        else:
            return default
    return dictionary


def chunk_list(lst: list, chunk_size: int) -> list:
    """Split list into chunks of specified size."""
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)] 