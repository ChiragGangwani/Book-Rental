from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .task import rental_period_expire

scheduler=AsyncIOScheduler()

# Assigning jobs to scheduler
scheduler.add_job(rental_period_expire,'cron',hour=5)
