"""
Command line interface for GitHub Sentinel.
"""

import asyncio
import sys
from datetime import datetime, timedelta
from typing import Optional

import click
from tabulate import tabulate

from ..core.config import Config
from ..core.models import User, NotificationChannel
from ..core.exceptions import GitHubSentinelError
from ..database.connection import DatabaseManager
from ..database.repositories import UserRepository, SubscriptionRepository, RepositoryRepository
from ..services.github_service import GitHubService
from ..services.subscription_service import SubscriptionService
from ..utils.logger import setup_logging, get_logger
from ..utils.helpers import validate_github_repo_name, parse_github_url


logger = get_logger(__name__)


def setup_application(config_file: Optional[str] = None) -> tuple:
    """Setup application with configuration and services."""
    # Load configuration
    config = Config.load(config_file)
    
    # Setup logging
    setup_logging(config.logging)
    
    # Validate required settings
    missing = config.validate_required_settings()
    if missing:
        click.echo(f"Missing required settings: {', '.join(missing)}")
        click.echo("Please set the required environment variables or configuration.")
        sys.exit(1)
    
    # Initialize database
    db_manager = DatabaseManager(config)
    db_manager.create_tables()
    
    # Initialize services
    github_service = GitHubService(config)
    
    return config, db_manager, github_service


@click.group()
@click.option('--config', '-c', help='Configuration file path')
@click.pass_context
def main(ctx, config):
    """GitHub Sentinel - Monitor GitHub repositories and generate reports."""
    ctx.ensure_object(dict)
    ctx.obj['config_file'] = config


@main.command()
@click.option('--username', '-u', required=True, help='Username')
@click.option('--email', '-e', required=True, help='Email address')
@click.option('--github-token', '-t', required=True, help='GitHub personal access token')
@click.pass_context
def init(ctx, username, email, github_token):
    """Initialize GitHub Sentinel with user credentials."""
    try:
        config, db_manager, github_service = setup_application(ctx.obj['config_file'])
        
        with db_manager.get_session() as session:
            user_repo = UserRepository(session)
            
            # Check if user already exists
            existing_user = user_repo.get_by_username(username)
            if existing_user:
                click.echo(f"User '{username}' already exists.")
                return
            
            # Create new user
            user = User(
                username=username,
                email=email,
                github_token=github_token,
                notification_preferences={
                    NotificationChannel.EMAIL: True,
                    NotificationChannel.SLACK: False,
                    NotificationChannel.WEBHOOK: False,
                }
            )
            
            created_user = user_repo.create(user)
            click.echo(f"User '{username}' created successfully!")
            click.echo(f"User ID: {created_user.id}")
            
    except GitHubSentinelError as e:
        click.echo(f"Error: {e.message}")
        sys.exit(1)
    except Exception as e:
        click.echo(f"Unexpected error: {str(e)}")
        sys.exit(1)


@main.command()
@click.option('--user-id', '-u', type=int, required=True, help='User ID')
@click.option('--repo', '-r', required=True, help='Repository (owner/name format or GitHub URL)')
@click.option('--frequency', '-f', default='daily', help='Update frequency (daily, weekly, monthly)')
@click.option('--channels', '-ch', multiple=True, help='Notification channels (email, slack, webhook)')
@click.pass_context
def subscribe(ctx, user_id, repo, frequency, channels):
    """Subscribe to a repository."""
    try:
        config, db_manager, github_service = setup_application(ctx.obj['config_file'])
        
        # Parse repository name
        repo_name = parse_github_url(repo) or repo
        if not validate_github_repo_name(repo_name):
            click.echo(f"Invalid repository format: {repo}. Use 'owner/repo' format.")
            sys.exit(1)
        
        # Parse notification channels
        notification_channels = []
        if channels:
            for ch in channels:
                try:
                    notification_channels.append(NotificationChannel(ch.lower()))
                except ValueError:
                    click.echo(f"Invalid notification channel: {ch}")
                    sys.exit(1)
        else:
            notification_channels = [NotificationChannel.EMAIL]
        
        with db_manager.get_session() as session:
            subscription_repo = SubscriptionRepository(session)
            repository_repo = RepositoryRepository(session)
            
            subscription_service = SubscriptionService(
                session, github_service, subscription_repo, repository_repo
            )
            
            # Create subscription
            subscription = asyncio.run(subscription_service.create_subscription(
                user_id=user_id,
                repo_full_name=repo_name,
                notification_channels=notification_channels,
                frequency=frequency
            ))
            
            click.echo(f"Successfully subscribed to {repo_name}")
            click.echo(f"Subscription ID: {subscription.id}")
            click.echo(f"Frequency: {frequency}")
            click.echo(f"Channels: {', '.join([ch.value for ch in notification_channels])}")
            
    except GitHubSentinelError as e:
        click.echo(f"Error: {e.message}")
        sys.exit(1)
    except Exception as e:
        click.echo(f"Unexpected error: {str(e)}")
        sys.exit(1)


@main.command()
@click.option('--user-id', '-u', type=int, required=True, help='User ID')
@click.pass_context
def list_subscriptions(ctx, user_id):
    """List all subscriptions for a user."""
    try:
        config, db_manager, github_service = setup_application(ctx.obj['config_file'])
        
        with db_manager.get_session() as session:
            subscription_repo = SubscriptionRepository(session)
            subscription_service = SubscriptionService(
                session, github_service, subscription_repo, RepositoryRepository(session)
            )
            
            subscriptions = asyncio.run(subscription_service.get_user_subscriptions(user_id))
            
            if not subscriptions:
                click.echo(f"No subscriptions found for user {user_id}")
                return
            
            # Format data for table display
            table_data = []
            for sub in subscriptions:
                repo_name = sub.repository.full_name if sub.repository else "Unknown"
                channels = ', '.join([ch.value for ch in sub.notification_channels])
                table_data.append([
                    sub.id,
                    repo_name,
                    sub.status.value,
                    sub.frequency,
                    channels,
                    sub.created_at.strftime("%Y-%m-%d")
                ])
            
            headers = ["ID", "Repository", "Status", "Frequency", "Channels", "Created"]
            click.echo(tabulate(table_data, headers=headers, tablefmt="grid"))
            
    except GitHubSentinelError as e:
        click.echo(f"Error: {e.message}")
        sys.exit(1)
    except Exception as e:
        click.echo(f"Unexpected error: {str(e)}")
        sys.exit(1)


@main.command()
@click.option('--subscription-id', '-s', type=int, required=True, help='Subscription ID')
@click.pass_context
def unsubscribe(ctx, subscription_id):
    """Unsubscribe from a repository."""
    try:
        config, db_manager, github_service = setup_application(ctx.obj['config_file'])
        
        with db_manager.get_session() as session:
            subscription_repo = SubscriptionRepository(session)
            subscription_service = SubscriptionService(
                session, github_service, subscription_repo, RepositoryRepository(session)
            )
            
            success = asyncio.run(subscription_service.delete_subscription(subscription_id))
            
            if success:
                click.echo(f"Successfully unsubscribed from subscription {subscription_id}")
            else:
                click.echo(f"Subscription {subscription_id} not found")
                
    except GitHubSentinelError as e:
        click.echo(f"Error: {e.message}")
        sys.exit(1)
    except Exception as e:
        click.echo(f"Unexpected error: {str(e)}")
        sys.exit(1)


@main.command()
@click.option('--repo', '-r', required=True, help='Repository name (owner/repo)')
@click.option('--days', '-d', default=7, help='Number of days to analyze')
@click.pass_context
def analyze(ctx, repo, days):
    """Analyze repository activity for the specified period."""
    try:
        config, db_manager, github_service = setup_application(ctx.obj['config_file'])
        
        # Parse repository name
        repo_name = parse_github_url(repo) or repo
        if not validate_github_repo_name(repo_name):
            click.echo(f"Invalid repository format: {repo}. Use 'owner/repo' format.")
            sys.exit(1)
        
        # Calculate date range with timezone info
        from datetime import timezone
        end_date = datetime.now(timezone.utc)
        start_date = end_date - timedelta(days=days)
        
        click.echo(f"Analyzing {repo_name} activity from {start_date.date()} to {end_date.date()}...")
        
        # Get repository activity
        activity = asyncio.run(github_service.get_repository_activity(
            repo_name, start_date, end_date
        ))
        
        # Display results
        click.echo(f"\n=== Repository: {activity.repository.full_name} ===")
        click.echo(f"Description: {activity.repository.description or 'N/A'}")
        click.echo(f"Language: {activity.repository.language or 'N/A'}")
        click.echo(f"Stars: {activity.repository.stars_count}")
        click.echo(f"Forks: {activity.repository.forks_count}")
        click.echo(f"Open Issues: {activity.repository.open_issues_count}")
        
        click.echo(f"\n=== Activity Summary ({days} days) ===")
        click.echo(f"Commits: {len(activity.commits)}")
        click.echo(f"Pull Requests: {len(activity.pull_requests)}")
        click.echo(f"Issues: {len(activity.issues)}")
        click.echo(f"Releases: {len(activity.releases)}")
        
        # Show recent commits
        if activity.commits:
            click.echo(f"\n=== Recent Commits ===")
            for commit in activity.commits[:5]:  # Show first 5
                click.echo(f"• {commit.sha[:8]} - {commit.message[:60]}... ({commit.author})")
        
        # Show recent PRs
        if activity.pull_requests:
            click.echo(f"\n=== Recent Pull Requests ===")
            for pr in activity.pull_requests[:5]:  # Show first 5
                click.echo(f"• #{pr.number} - {pr.title[:60]}... ({pr.state})")
        
        # Show recent issues
        if activity.issues:
            click.echo(f"\n=== Recent Issues ===")
            for issue in activity.issues[:5]:  # Show first 5
                click.echo(f"• #{issue.number} - {issue.title[:60]}... ({issue.state})")
        
        # Show releases
        if activity.releases:
            click.echo(f"\n=== Recent Releases ===")
            for release in activity.releases:
                click.echo(f"• {release.tag_name} - {release.name} ({release.published_at.date()})")
        
    except GitHubSentinelError as e:
        click.echo(f"Error: {e.message}")
        sys.exit(1)
    except Exception as e:
        click.echo(f"Unexpected error: {str(e)}")
        sys.exit(1)


@main.command()
@click.option('--frequency', '-f', default='daily', help='Process subscriptions with this frequency')
@click.pass_context  
def process(ctx, frequency):
    """Process subscriptions and generate reports."""
    try:
        config, db_manager, github_service = setup_application(ctx.obj['config_file'])
        
        with db_manager.get_session() as session:
            subscription_repo = SubscriptionRepository(session)
            subscription_service = SubscriptionService(
                session, github_service, subscription_repo, RepositoryRepository(session)
            )
            
            subscriptions = asyncio.run(subscription_service.get_subscriptions_by_frequency(frequency))
            
            if not subscriptions:
                click.echo(f"No {frequency} subscriptions found to process.")
                return
            
            click.echo(f"Processing {len(subscriptions)} {frequency} subscriptions...")
            
            for subscription in subscriptions:
                try:
                    click.echo(f"Processing subscription {subscription.id} for {subscription.repository.full_name}...")
                    
                    # Calculate date range based on frequency
                    end_date = datetime.now()
                    if frequency == 'daily':
                        start_date = end_date - timedelta(days=1)
                    elif frequency == 'weekly':
                        start_date = end_date - timedelta(weeks=1)
                    elif frequency == 'monthly':
                        start_date = end_date - timedelta(days=30)
                    else:
                        start_date = end_date - timedelta(days=1)
                    
                    # Get repository activity
                    activity = asyncio.run(github_service.get_repository_activity(
                        subscription.repository.full_name, start_date, end_date
                    ))
                    
                    # Simple summary
                    summary = f"Activity for {subscription.repository.full_name}: "
                    summary += f"{len(activity.commits)} commits, "
                    summary += f"{len(activity.pull_requests)} PRs, "
                    summary += f"{len(activity.issues)} issues, "
                    summary += f"{len(activity.releases)} releases"
                    
                    click.echo(f"  {summary}")
                    
                    # Here you would typically generate a report and send notifications
                    # For now, just print the summary
                    
                except Exception as e:
                    click.echo(f"  Error processing subscription {subscription.id}: {str(e)}")
                    continue
            
            click.echo("Processing completed.")
            
    except GitHubSentinelError as e:
        click.echo(f"Error: {e.message}")
        sys.exit(1)
    except Exception as e:
        click.echo(f"Unexpected error: {str(e)}")
        sys.exit(1)


@main.command()
@click.pass_context
def status(ctx):
    """Show GitHub Sentinel status and configuration."""
    try:
        config, db_manager, github_service = setup_application(ctx.obj['config_file'])
        
        click.echo("=== GitHub Sentinel Status ===")
        click.echo(f"Version: {config.version}")
        click.echo(f"Environment: {config.environment}")
        click.echo(f"Debug Mode: {config.debug}")
        
        click.echo(f"\n=== Database ===")
        click.echo(f"URL: {config.database.url}")
        
        click.echo(f"\n=== GitHub API ===")
        click.echo(f"Base URL: {config.github.base_url}")
        click.echo(f"Token: {'***' + config.github.token[-4:] if config.github.token else 'Not set'}")
        
        # Test GitHub connection
        try:
            repo_info = asyncio.run(github_service.get_repository_info("octocat/Hello-World"))
            click.echo("✓ GitHub API connection successful")
        except Exception as e:
            click.echo(f"✗ GitHub API connection failed: {str(e)}")
        
        # Database stats
        with db_manager.get_session() as session:
            user_repo = UserRepository(session)
            subscription_repo = SubscriptionRepository(session)
            
            try:
                users_count = len(session.query(session.query(UserRepository.model_class).statement.subquery()).all())
                active_subs = len(subscription_repo.get_active_subscriptions())
                
                click.echo(f"\n=== Statistics ===")
                click.echo(f"Total Users: {users_count}")
                click.echo(f"Active Subscriptions: {active_subs}")
                
            except Exception as e:
                click.echo(f"Could not retrieve statistics: {str(e)}")
        
    except GitHubSentinelError as e:
        click.echo(f"Error: {e.message}")
        sys.exit(1)
    except Exception as e:
        click.echo(f"Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main() 