"""
Scheduler service for managing periodic tasks.
"""

import schedule
import time
import threading
from typing import Callable, Dict, Any
from datetime import datetime

from ..core.config import Config
from ..core.exceptions import SchedulerError
from ..utils.logger import get_logger

logger = get_logger(__name__)


class SchedulerService:
    """Service for managing scheduled tasks."""
    
    def __init__(self, config: Config):
        """Initialize scheduler service."""
        self.config = config
        self.running = False
        self.scheduler_thread = None
        self.jobs = {}
    
    def start(self):
        """Start the scheduler."""
        if self.running:
            logger.warning("Scheduler is already running")
            return
        
        if not self.config.scheduler.enabled:
            logger.info("Scheduler is disabled in configuration")
            return
        
        self.running = True
        self.scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.scheduler_thread.start()
        logger.info("Scheduler started")
    
    def stop(self):
        """Stop the scheduler."""
        if not self.running:
            return
        
        self.running = False
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5)
        
        schedule.clear()
        self.jobs.clear()
        logger.info("Scheduler stopped")
    
    def schedule_daily_job(self, job_func: Callable, time_str: str = "09:00", job_id: str = None) -> str:
        """Schedule a daily job."""
        job_id = job_id or f"daily_{int(time.time())}"
        
        try:
            job = schedule.every().day.at(time_str).do(job_func)
            self.jobs[job_id] = job
            logger.info(f"Scheduled daily job {job_id} at {time_str}")
            return job_id
        except Exception as e:
            raise SchedulerError(f"Failed to schedule daily job: {str(e)}")
    
    def schedule_weekly_job(self, job_func: Callable, day: str = "monday", time_str: str = "09:00", job_id: str = None) -> str:
        """Schedule a weekly job."""
        job_id = job_id or f"weekly_{int(time.time())}"
        
        try:
            job = getattr(schedule.every(), day.lower()).at(time_str).do(job_func)
            self.jobs[job_id] = job
            logger.info(f"Scheduled weekly job {job_id} on {day} at {time_str}")
            return job_id
        except Exception as e:
            raise SchedulerError(f"Failed to schedule weekly job: {str(e)}")
    
    def schedule_monthly_job(self, job_func: Callable, day: int = 1, time_str: str = "09:00", job_id: str = None) -> str:
        """Schedule a monthly job."""
        job_id = job_id or f"monthly_{int(time.time())}"
        
        try:
            # Note: This is a simplified monthly scheduler
            # For production, you'd want a more sophisticated approach
            def monthly_wrapper():
                if datetime.now().day == day:
                    job_func()
            
            job = schedule.every().day.at(time_str).do(monthly_wrapper)
            self.jobs[job_id] = job
            logger.info(f"Scheduled monthly job {job_id} on day {day} at {time_str}")
            return job_id
        except Exception as e:
            raise SchedulerError(f"Failed to schedule monthly job: {str(e)}")
    
    def cancel_job(self, job_id: str) -> bool:
        """Cancel a scheduled job."""
        if job_id not in self.jobs:
            logger.warning(f"Job {job_id} not found")
            return False
        
        try:
            schedule.cancel_job(self.jobs[job_id])
            del self.jobs[job_id]
            logger.info(f"Cancelled job {job_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to cancel job {job_id}: {str(e)}")
            return False
    
    def get_jobs(self) -> Dict[str, Any]:
        """Get information about scheduled jobs."""
        return {
            job_id: {
                "next_run": str(job.next_run) if job.next_run else None,
                "job": str(job)
            }
            for job_id, job in self.jobs.items()
        }
    
    def _run_scheduler(self):
        """Run the scheduler loop."""
        logger.info("Scheduler loop started")
        
        while self.running:
            try:
                schedule.run_pending()
                time.sleep(1)
            except Exception as e:
                logger.error(f"Scheduler error: {str(e)}")
                time.sleep(5)  # Wait a bit before retrying
        
        logger.info("Scheduler loop ended") 