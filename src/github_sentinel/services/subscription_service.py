"""
Subscription management service.
"""

from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session

from ..core.models import (
    Subscription, Repository, User, SubscriptionStatus, NotificationChannel
)
from ..core.exceptions import SubscriptionError, ValidationError
from ..database.repositories import SubscriptionRepository, RepositoryRepository
from ..services.github_service import GitHubService
from ..utils.logger import get_logger
from ..utils.helpers import validate_github_repo_name


logger = get_logger(__name__)


class SubscriptionService:
    """Service for managing repository subscriptions."""
    
    def __init__(
        self, 
        db_session: Session,
        github_service: GitHubService,
        subscription_repo: SubscriptionRepository,
        repository_repo: RepositoryRepository
    ):
        """Initialize subscription service."""
        self.db_session = db_session
        self.github_service = github_service
        self.subscription_repo = subscription_repo
        self.repository_repo = repository_repo
    
    async def create_subscription(
        self,
        user_id: int,
        repo_full_name: str,
        notification_channels: List[NotificationChannel] = None,
        frequency: str = "daily",
        watch_events: List[str] = None
    ) -> Subscription:
        """Create a new repository subscription."""
        # Validate repository name format
        if not validate_github_repo_name(repo_full_name):
            raise ValidationError(f"Invalid repository name format: {repo_full_name}")
        
        # Check if subscription already exists
        existing = self.subscription_repo.get_by_user_and_repo(user_id, repo_full_name)
        if existing:
            if existing.status == SubscriptionStatus.ACTIVE:
                raise SubscriptionError("Subscription already exists and is active")
            else:
                # Reactivate existing subscription
                return await self.update_subscription_status(existing.id, SubscriptionStatus.ACTIVE)
        
        # Validate repository access
        try:
            can_access = await self.github_service.validate_repository_access(repo_full_name)
            if not can_access:
                raise SubscriptionError(f"Repository {repo_full_name} not found or not accessible")
        except Exception as e:
            raise SubscriptionError(f"Failed to validate repository: {str(e)}")
        
        # Get or create repository record
        repository = await self._get_or_create_repository(repo_full_name)
        
        # Create subscription
        subscription = Subscription(
            user_id=user_id,
            repository_id=repository.id,
            repository=repository,
            status=SubscriptionStatus.ACTIVE,
            notification_channels=notification_channels or [NotificationChannel.EMAIL],
            frequency=frequency,
            watch_events=watch_events or ["push", "pull_request", "issues", "releases"],
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        try:
            saved_subscription = self.subscription_repo.create(subscription)
            logger.info(f"Created subscription for user {user_id} to repository {repo_full_name}")
            return saved_subscription
        except Exception as e:
            raise SubscriptionError(f"Failed to create subscription: {str(e)}")
    
    async def get_user_subscriptions(
        self, 
        user_id: int,
        status: Optional[SubscriptionStatus] = None
    ) -> List[Subscription]:
        """Get all subscriptions for a user."""
        try:
            return self.subscription_repo.get_by_user(user_id, status)
        except Exception as e:
            raise SubscriptionError(f"Failed to retrieve subscriptions: {str(e)}")
    
    async def get_subscription(self, subscription_id: int) -> Optional[Subscription]:
        """Get subscription by ID."""
        try:
            return self.subscription_repo.get_by_id(subscription_id)
        except Exception as e:
            raise SubscriptionError(f"Failed to retrieve subscription: {str(e)}")
    
    async def update_subscription(
        self,
        subscription_id: int,
        notification_channels: Optional[List[NotificationChannel]] = None,
        frequency: Optional[str] = None,
        watch_events: Optional[List[str]] = None
    ) -> Subscription:
        """Update subscription settings."""
        subscription = await self.get_subscription(subscription_id)
        if not subscription:
            raise SubscriptionError(f"Subscription {subscription_id} not found")
        
        # Update fields if provided
        if notification_channels is not None:
            subscription.notification_channels = notification_channels
        if frequency is not None:
            subscription.frequency = frequency
        if watch_events is not None:
            subscription.watch_events = watch_events
        
        subscription.updated_at = datetime.now()
        
        try:
            updated_subscription = self.subscription_repo.update(subscription)
            logger.info(f"Updated subscription {subscription_id}")
            return updated_subscription
        except Exception as e:
            raise SubscriptionError(f"Failed to update subscription: {str(e)}")
    
    async def update_subscription_status(
        self,
        subscription_id: int,
        status: SubscriptionStatus
    ) -> Subscription:
        """Update subscription status."""
        subscription = await self.get_subscription(subscription_id)
        if not subscription:
            raise SubscriptionError(f"Subscription {subscription_id} not found")
        
        subscription.status = status
        subscription.updated_at = datetime.now()
        
        try:
            updated_subscription = self.subscription_repo.update(subscription)
            logger.info(f"Updated subscription {subscription_id} status to {status}")
            return updated_subscription
        except Exception as e:
            raise SubscriptionError(f"Failed to update subscription status: {str(e)}")
    
    async def delete_subscription(self, subscription_id: int) -> bool:
        """Delete a subscription."""
        subscription = await self.get_subscription(subscription_id)
        if not subscription:
            raise SubscriptionError(f"Subscription {subscription_id} not found")
        
        try:
            success = self.subscription_repo.delete(subscription_id)
            if success:
                logger.info(f"Deleted subscription {subscription_id}")
            return success
        except Exception as e:
            raise SubscriptionError(f"Failed to delete subscription: {str(e)}")
    
    async def get_active_subscriptions(self) -> List[Subscription]:
        """Get all active subscriptions for processing."""
        try:
            return self.subscription_repo.get_active_subscriptions()
        except Exception as e:
            raise SubscriptionError(f"Failed to retrieve active subscriptions: {str(e)}")
    
    async def get_subscriptions_by_frequency(self, frequency: str) -> List[Subscription]:
        """Get subscriptions by frequency for scheduled processing."""
        try:
            return self.subscription_repo.get_by_frequency(frequency)
        except Exception as e:
            raise SubscriptionError(f"Failed to retrieve subscriptions by frequency: {str(e)}")
    
    async def _get_or_create_repository(self, repo_full_name: str) -> Repository:
        """Get existing repository or create new one."""
        # Check if repository exists in database
        repository = self.repository_repo.get_by_full_name(repo_full_name)
        
        if repository:
            # Update repository info from GitHub
            try:
                github_repo = await self.github_service.get_repository_info(repo_full_name)
                repository.description = github_repo.description
                repository.stars_count = github_repo.stars_count
                repository.forks_count = github_repo.forks_count
                repository.open_issues_count = github_repo.open_issues_count
                repository.language = github_repo.language
                repository.last_updated = github_repo.last_updated
                
                repository = self.repository_repo.update(repository)
            except Exception as e:
                logger.warning(f"Failed to update repository info: {e}")
            
            return repository
        
        # Create new repository record
        try:
            github_repo = await self.github_service.get_repository_info(repo_full_name)
            github_repo.created_at = datetime.now()
            
            repository = self.repository_repo.create(github_repo)
            logger.info(f"Created repository record for {repo_full_name}")
            return repository
            
        except Exception as e:
            raise SubscriptionError(f"Failed to create repository record: {str(e)}") 