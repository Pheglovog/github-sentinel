"""
GitHub Sentinel - AI Agent for monitoring GitHub repositories and generating reports.

This package provides functionality for:
- Repository subscription management
- Automated repository monitoring
- Report generation
- Notification systems
- Scheduled tasks
"""

__version__ = "0.1.0"
__author__ = "GitHub Sentinel Team"

from .core.config import Config
from .core.models import Repository, Subscription, Report

__all__ = [
    "Config",
    "Repository", 
    "Subscription",
    "Report",
] 