from datetime import datetime, date
from apscheduler.schedulers.background import BackgroundScheduler
from helpers.business import update_payment_scheduler


def start():
  scheduler = BackgroundScheduler({'apscheduler.timezone': 'Asia/Kolkata'})
  # scheduler.add_job(update_payment_scheduler, 'interval', seconds=10)
  # scheduler.add_job(update_payment_scheduler, 'date', run_date=date(datetime.now().year, datetime.now().month, 1))
  scheduler.add_job(update_payment_scheduler, 'date', run_date=datetime(datetime.now().year, datetime.now().month, 1, 1, 45, 5))
  scheduler.start()
