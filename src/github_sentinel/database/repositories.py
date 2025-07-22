"""
Data access layer using Repository pattern.
"""

from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_

from .connection import UserModel, RepositoryModel, SubscriptionModel, ReportModel
from ..core.models import User, Repository, Subscription, Report, SubscriptionStatus
from ..core.exceptions import DatabaseError


class BaseRepository:
    """Base repository with common operations."""
    
    def __init__(self, session: Session, model_class):
        self.session = session
        self.model_class = model_class


class UserRepository(BaseRepository):
    """Repository for user operations."""
    
    def __init__(self, session: Session):
        super().__init__(session, UserModel)
    
    def create(self, user: User) -> User:
        """Create a new user."""
        try:
            db_user = UserModel(
                username=user.username,
                email=user.email,
                github_token=user.github_token,
                notification_preferences=user.notification_preferences
            )
            self.session.add(db_user)
            self.session.flush()
            
            user.id = db_user.id
            user.created_at = db_user.created_at
            user.updated_at = db_user.updated_at
            
            return user
        except Exception as e:
            raise DatabaseError(f"Failed to create user: {str(e)}")
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        try:
            db_user = self.session.query(UserModel).filter(UserModel.id == user_id).first()
            if db_user:
                return self._to_model(db_user)
            return None
        except Exception as e:
            raise DatabaseError(f"Failed to get user: {str(e)}")
    
    def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        try:
            db_user = self.session.query(UserModel).filter(UserModel.username == username).first()
            if db_user:
                return self._to_model(db_user)
            return None
        except Exception as e:
            raise DatabaseError(f"Failed to get user by username: {str(e)}")
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        try:
            db_user = self.session.query(UserModel).filter(UserModel.email == email).first()
            if db_user:
                return self._to_model(db_user)
            return None
        except Exception as e:
            raise DatabaseError(f"Failed to get user by email: {str(e)}")
    
    def update(self, user: User) -> User:
        """Update user."""
        try:
            db_user = self.session.query(UserModel).filter(UserModel.id == user.id).first()
            if not db_user:
                raise DatabaseError(f"User {user.id} not found")
            
            db_user.username = user.username
            db_user.email = user.email
            db_user.github_token = user.github_token
            db_user.notification_preferences = user.notification_preferences
            db_user.updated_at = datetime.now()
            
            self.session.flush()
            
            return self._to_model(db_user)
        except Exception as e:
            raise DatabaseError(f"Failed to update user: {str(e)}")
    
    def _to_model(self, db_user: UserModel) -> User:
        """Convert database model to domain model."""
        return User(
            id=db_user.id,
            username=db_user.username,
            email=db_user.email,
            github_token=db_user.github_token,
            notification_preferences=db_user.notification_preferences or {},
            created_at=db_user.created_at,
            updated_at=db_user.updated_at
        )


class RepositoryRepository(BaseRepository):
    """Repository for repository operations."""
    
    def __init__(self, session: Session):
        super().__init__(session, RepositoryModel)
    
    def create(self, repository: Repository) -> Repository:
        """Create a new repository."""
        try:
            db_repo = RepositoryModel(
                full_name=repository.full_name,
                owner=repository.owner,
                name=repository.name,
                description=repository.description,
                url=str(repository.url),
                default_branch=repository.default_branch,
                stars_count=repository.stars_count,
                forks_count=repository.forks_count,
                open_issues_count=repository.open_issues_count,
                language=repository.language,
                last_updated=repository.last_updated
            )
            self.session.add(db_repo)
            self.session.flush()
            
            repository.id = db_repo.id
            repository.created_at = db_repo.created_at
            
            return repository
        except Exception as e:
            raise DatabaseError(f"Failed to create repository: {str(e)}")
    
    def get_by_id(self, repo_id: int) -> Optional[Repository]:
        """Get repository by ID."""
        try:
            db_repo = self.session.query(RepositoryModel).filter(RepositoryModel.id == repo_id).first()
            if db_repo:
                return self._to_model(db_repo)
            return None
        except Exception as e:
            raise DatabaseError(f"Failed to get repository: {str(e)}")
    
    def get_by_full_name(self, full_name: str) -> Optional[Repository]:
        """Get repository by full name."""
        try:
            db_repo = self.session.query(RepositoryModel).filter(
                RepositoryModel.full_name == full_name
            ).first()
            if db_repo:
                return self._to_model(db_repo)
            return None
        except Exception as e:
            raise DatabaseError(f"Failed to get repository by full name: {str(e)}")
    
    def update(self, repository: Repository) -> Repository:
        """Update repository."""
        try:
            db_repo = self.session.query(RepositoryModel).filter(
                RepositoryModel.id == repository.id
            ).first()
            if not db_repo:
                raise DatabaseError(f"Repository {repository.id} not found")
            
            db_repo.description = repository.description
            db_repo.stars_count = repository.stars_count
            db_repo.forks_count = repository.forks_count
            db_repo.open_issues_count = repository.open_issues_count
            db_repo.language = repository.language
            db_repo.last_updated = repository.last_updated
            
            self.session.flush()
            
            return self._to_model(db_repo)
        except Exception as e:
            raise DatabaseError(f"Failed to update repository: {str(e)}")
    
    def _to_model(self, db_repo: RepositoryModel) -> Repository:
        """Convert database model to domain model."""
        return Repository(
            id=db_repo.id,
            full_name=db_repo.full_name,
            owner=db_repo.owner,
            name=db_repo.name,
            description=db_repo.description,
            url=db_repo.url,
            default_branch=db_repo.default_branch,
            stars_count=db_repo.stars_count,
            forks_count=db_repo.forks_count,
            open_issues_count=db_repo.open_issues_count,
            language=db_repo.language,
            last_updated=db_repo.last_updated,
            created_at=db_repo.created_at
        )


class SubscriptionRepository(BaseRepository):
    """Repository for subscription operations."""
    
    def __init__(self, session: Session):
        super().__init__(session, SubscriptionModel)
    
    def create(self, subscription: Subscription) -> Subscription:
        """Create a new subscription."""
        try:
            db_sub = SubscriptionModel(
                user_id=subscription.user_id,
                repository_id=subscription.repository_id,
                status=subscription.status.value,
                notification_channels=[ch.value for ch in subscription.notification_channels],
                frequency=subscription.frequency,
                watch_events=subscription.watch_events
            )
            self.session.add(db_sub)
            self.session.flush()
            
            subscription.id = db_sub.id
            subscription.created_at = db_sub.created_at
            subscription.updated_at = db_sub.updated_at
            
            return subscription
        except Exception as e:
            raise DatabaseError(f"Failed to create subscription: {str(e)}")
    
    def get_by_id(self, subscription_id: int) -> Optional[Subscription]:
        """Get subscription by ID."""
        try:
            db_sub = self.session.query(SubscriptionModel).filter(
                SubscriptionModel.id == subscription_id
            ).first()
            if db_sub:
                return self._to_model(db_sub)
            return None
        except Exception as e:
            raise DatabaseError(f"Failed to get subscription: {str(e)}")
    
    def get_by_user(self, user_id: int, status: Optional[SubscriptionStatus] = None) -> List[Subscription]:
        """Get subscriptions by user."""
        try:
            query = self.session.query(SubscriptionModel).filter(SubscriptionModel.user_id == user_id)
            
            if status:
                query = query.filter(SubscriptionModel.status == status.value)
            
            db_subs = query.all()
            return [self._to_model(db_sub) for db_sub in db_subs]
        except Exception as e:
            raise DatabaseError(f"Failed to get user subscriptions: {str(e)}")
    
    def get_by_user_and_repo(self, user_id: int, repo_full_name: str) -> Optional[Subscription]:
        """Get subscription by user and repository."""
        try:
            db_sub = self.session.query(SubscriptionModel).join(RepositoryModel).filter(
                and_(
                    SubscriptionModel.user_id == user_id,
                    RepositoryModel.full_name == repo_full_name
                )
            ).first()
            if db_sub:
                return self._to_model(db_sub)
            return None
        except Exception as e:
            raise DatabaseError(f"Failed to get subscription by user and repo: {str(e)}")
    
    def get_active_subscriptions(self) -> List[Subscription]:
        """Get all active subscriptions."""
        try:
            db_subs = self.session.query(SubscriptionModel).filter(
                SubscriptionModel.status == SubscriptionStatus.ACTIVE.value
            ).all()
            return [self._to_model(db_sub) for db_sub in db_subs]
        except Exception as e:
            raise DatabaseError(f"Failed to get active subscriptions: {str(e)}")
    
    def get_by_frequency(self, frequency: str) -> List[Subscription]:
        """Get subscriptions by frequency."""
        try:
            db_subs = self.session.query(SubscriptionModel).filter(
                and_(
                    SubscriptionModel.frequency == frequency,
                    SubscriptionModel.status == SubscriptionStatus.ACTIVE.value
                )
            ).all()
            return [self._to_model(db_sub) for db_sub in db_subs]
        except Exception as e:
            raise DatabaseError(f"Failed to get subscriptions by frequency: {str(e)}")
    
    def update(self, subscription: Subscription) -> Subscription:
        """Update subscription."""
        try:
            db_sub = self.session.query(SubscriptionModel).filter(
                SubscriptionModel.id == subscription.id
            ).first()
            if not db_sub:
                raise DatabaseError(f"Subscription {subscription.id} not found")
            
            db_sub.status = subscription.status.value
            db_sub.notification_channels = [ch.value for ch in subscription.notification_channels]
            db_sub.frequency = subscription.frequency
            db_sub.watch_events = subscription.watch_events
            db_sub.updated_at = datetime.now()
            
            self.session.flush()
            
            return self._to_model(db_sub)
        except Exception as e:
            raise DatabaseError(f"Failed to update subscription: {str(e)}")
    
    def delete(self, subscription_id: int) -> bool:
        """Delete subscription."""
        try:
            db_sub = self.session.query(SubscriptionModel).filter(
                SubscriptionModel.id == subscription_id
            ).first()
            if not db_sub:
                return False
            
            self.session.delete(db_sub)
            self.session.flush()
            
            return True
        except Exception as e:
            raise DatabaseError(f"Failed to delete subscription: {str(e)}")
    
    def _to_model(self, db_sub: SubscriptionModel) -> Subscription:
        """Convert database model to domain model."""
        from ..core.models import NotificationChannel
        
        # Load repository if available
        repository = None
        if db_sub.repository:
            repository = Repository(
                id=db_sub.repository.id,
                full_name=db_sub.repository.full_name,
                owner=db_sub.repository.owner,
                name=db_sub.repository.name,
                description=db_sub.repository.description,
                url=db_sub.repository.url,
                default_branch=db_sub.repository.default_branch,
                stars_count=db_sub.repository.stars_count,
                forks_count=db_sub.repository.forks_count,
                open_issues_count=db_sub.repository.open_issues_count,
                language=db_sub.repository.language,
                last_updated=db_sub.repository.last_updated,
                created_at=db_sub.repository.created_at
            )
        
        return Subscription(
            id=db_sub.id,
            user_id=db_sub.user_id,
            repository_id=db_sub.repository_id,
            repository=repository,
            status=SubscriptionStatus(db_sub.status),
            notification_channels=[NotificationChannel(ch) for ch in (db_sub.notification_channels or [])],
            frequency=db_sub.frequency,
            watch_events=db_sub.watch_events or [],
            created_at=db_sub.created_at,
            updated_at=db_sub.updated_at
        )


class ReportRepository(BaseRepository):
    """Repository for report operations."""
    
    def __init__(self, session: Session):
        super().__init__(session, ReportModel)
    
    def create(self, report: Report) -> Report:
        """Create a new report."""
        try:
            db_report = ReportModel(
                subscription_id=report.subscription_id,
                title=report.title,
                content=report.content,
                format=report.format.value,
                period_start=report.period_start,
                period_end=report.period_end,
                summary=report.summary
            )
            self.session.add(db_report)
            self.session.flush()
            
            report.id = db_report.id
            report.generated_at = db_report.generated_at
            
            return report
        except Exception as e:
            raise DatabaseError(f"Failed to create report: {str(e)}")
    
    def get_by_id(self, report_id: int) -> Optional[Report]:
        """Get report by ID."""
        try:
            db_report = self.session.query(ReportModel).filter(ReportModel.id == report_id).first()
            if db_report:
                return self._to_model(db_report)
            return None
        except Exception as e:
            raise DatabaseError(f"Failed to get report: {str(e)}")
    
    def get_by_subscription(self, subscription_id: int, limit: int = 10) -> List[Report]:
        """Get reports by subscription."""
        try:
            db_reports = self.session.query(ReportModel).filter(
                ReportModel.subscription_id == subscription_id
            ).order_by(ReportModel.generated_at.desc()).limit(limit).all()
            
            return [self._to_model(db_report) for db_report in db_reports]
        except Exception as e:
            raise DatabaseError(f"Failed to get subscription reports: {str(e)}")
    
    def _to_model(self, db_report: ReportModel) -> Report:
        """Convert database model to domain model."""
        from ..core.models import ReportFormat
        
        return Report(
            id=db_report.id,
            subscription_id=db_report.subscription_id,
            title=db_report.title,
            content=db_report.content,
            format=ReportFormat(db_report.format),
            generated_at=db_report.generated_at,
            period_start=db_report.period_start,
            period_end=db_report.period_end,
            summary=db_report.summary
        ) 