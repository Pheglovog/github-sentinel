"""
Database connection management.
"""

from contextlib import contextmanager
from typing import Generator
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import func

from ..core.config import Config
from ..core.exceptions import DatabaseError
from ..utils.logger import get_logger


logger = get_logger(__name__)

Base = declarative_base()


class DatabaseManager:
    """Database connection manager."""
    
    def __init__(self, config: Config):
        """Initialize database manager."""
        self.config = config
        self.engine = None
        self.SessionLocal = None
        self._initialize()
    
    def _initialize(self):
        """Initialize database engine and session factory."""
        try:
            self.engine = create_engine(
                self.config.get_database_url(),
                echo=self.config.database.echo
            )
            self.SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )
            logger.info("Database connection initialized")
        except Exception as e:
            raise DatabaseError(f"Failed to initialize database: {str(e)}")
    
    def create_tables(self):
        """Create database tables."""
        try:
            Base.metadata.create_all(bind=self.engine)
            logger.info("Database tables created")
        except Exception as e:
            raise DatabaseError(f"Failed to create tables: {str(e)}")
    
    def get_session(self) -> Session:
        """Get database session."""
        if not self.SessionLocal:
            raise DatabaseError("Database not initialized")
        return self.SessionLocal()


# Database Models (SQLAlchemy ORM)

class UserModel(Base):
    """User database model."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    github_token = Column(String(255), nullable=False)
    notification_preferences = Column(JSON, default={})
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    subscriptions = relationship("SubscriptionModel", back_populates="user")


class RepositoryModel(Base):
    """Repository database model."""
    __tablename__ = "repositories"
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), unique=True, index=True, nullable=False)
    owner = Column(String(100), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    url = Column(String(500), nullable=False)
    default_branch = Column(String(100), default="main")
    stars_count = Column(Integer, default=0)
    forks_count = Column(Integer, default=0)
    open_issues_count = Column(Integer, default=0)
    language = Column(String(50))
    last_updated = Column(DateTime)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    subscriptions = relationship("SubscriptionModel", back_populates="repository")


class SubscriptionModel(Base):
    """Subscription database model."""
    __tablename__ = "subscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    repository_id = Column(Integer, ForeignKey("repositories.id"), nullable=False)
    status = Column(String(20), default="active", nullable=False)
    notification_channels = Column(JSON, default=[])
    frequency = Column(String(20), default="daily", nullable=False)
    watch_events = Column(JSON, default=[])
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("UserModel", back_populates="subscriptions")
    repository = relationship("RepositoryModel", back_populates="subscriptions")
    reports = relationship("ReportModel", back_populates="subscription")


class ReportModel(Base):
    """Report database model."""
    __tablename__ = "reports"
    
    id = Column(Integer, primary_key=True, index=True)
    subscription_id = Column(Integer, ForeignKey("subscriptions.id"), nullable=False)
    title = Column(String(500), nullable=False)
    content = Column(JSON, nullable=False)
    format = Column(String(20), default="markdown", nullable=False)
    generated_at = Column(DateTime, default=func.now())
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)
    summary = Column(Text)
    
    # Relationships
    subscription = relationship("SubscriptionModel", back_populates="reports")


@contextmanager
def get_db_session(db_manager: DatabaseManager) -> Generator[Session, None, None]:
    """Context manager for database sessions."""
    session = db_manager.get_session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close() 