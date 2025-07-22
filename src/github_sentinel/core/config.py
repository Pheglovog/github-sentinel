"""
Configuration management for GitHub Sentinel.
"""

import os
from typing import Optional, List
from pydantic import Field
from pydantic_settings import BaseSettings
from pathlib import Path


class DatabaseConfig(BaseSettings):
    """Database configuration."""
    url: str = Field(default="sqlite:///github_sentinel.db", env="DATABASE_URL")
    echo: bool = Field(default=False, env="DATABASE_ECHO")
    
    class Config:
        env_prefix = "DB_"


class GitHubConfig(BaseSettings):
    """GitHub API configuration."""
    token: Optional[str] = Field(default=None, env="GITHUB_TOKEN")
    base_url: str = Field(default="https://api.github.com", env="GITHUB_BASE_URL")
    timeout: int = Field(default=30, env="GITHUB_TIMEOUT")
    max_retries: int = Field(default=3, env="GITHUB_MAX_RETRIES")
    
    class Config:
        env_prefix = "GITHUB_"


class NotificationConfig(BaseSettings):
    """Notification configuration."""
    # Email settings
    smtp_host: Optional[str] = Field(default=None, env="SMTP_HOST")
    smtp_port: int = Field(default=587, env="SMTP_PORT")
    smtp_username: Optional[str] = Field(default=None, env="SMTP_USERNAME")
    smtp_password: Optional[str] = Field(default=None, env="SMTP_PASSWORD")
    smtp_use_tls: bool = Field(default=True, env="SMTP_USE_TLS")
    
    # Slack settings
    slack_webhook_url: Optional[str] = Field(default=None, env="SLACK_WEBHOOK_URL")
    slack_token: Optional[str] = Field(default=None, env="SLACK_TOKEN")
    
    # Discord settings
    discord_webhook_url: Optional[str] = Field(default=None, env="DISCORD_WEBHOOK_URL")
    
    class Config:
        env_prefix = "NOTIFICATION_"


class SchedulerConfig(BaseSettings):
    """Scheduler configuration."""
    enabled: bool = Field(default=True, env="SCHEDULER_ENABLED")
    default_timezone: str = Field(default="UTC", env="SCHEDULER_TIMEZONE")
    max_workers: int = Field(default=4, env="SCHEDULER_MAX_WORKERS")
    
    class Config:
        env_prefix = "SCHEDULER_"


class LoggingConfig(BaseSettings):
    """Logging configuration."""
    level: str = Field(default="INFO", env="LOG_LEVEL")
    format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        env="LOG_FORMAT"
    )
    file_path: Optional[str] = Field(default=None, env="LOG_FILE")
    max_file_size: int = Field(default=10485760, env="LOG_MAX_FILE_SIZE")  # 10MB
    backup_count: int = Field(default=5, env="LOG_BACKUP_COUNT")
    
    class Config:
        env_prefix = "LOG_"


class Config(BaseSettings):
    """Main configuration class."""
    # Environment
    environment: str = Field(default="development", env="ENVIRONMENT")
    debug: bool = Field(default=False, env="DEBUG")
    
    # Application settings
    app_name: str = Field(default="GitHub Sentinel", env="APP_NAME")
    version: str = Field(default="0.1.0", env="APP_VERSION")
    
    # Component configurations
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    github: GitHubConfig = Field(default_factory=GitHubConfig)
    notifications: NotificationConfig = Field(default_factory=NotificationConfig)
    scheduler: SchedulerConfig = Field(default_factory=SchedulerConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    
    # Report settings
    reports_dir: str = Field(default="reports", env="REPORTS_DIR")
    default_report_format: str = Field(default="markdown", env="DEFAULT_REPORT_FORMAT")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
    
    @classmethod
    def load(cls, config_file: Optional[str] = None) -> "Config":
        """Load configuration from file and environment."""
        if config_file and Path(config_file).exists():
            return cls(_env_file=config_file)
        return cls()
    
    def validate_required_settings(self) -> List[str]:
        """Validate required settings and return list of missing ones."""
        missing = []
        
        if not self.github.token:
            missing.append("GITHUB_TOKEN")
        
        return missing
    
    @property 
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment.lower() == "production"
    
    def get_database_url(self) -> str:
        """Get properly formatted database URL."""
        return self.database.url 