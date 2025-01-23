from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from . import mailer

scheduler = BackgroundScheduler()

def email_task(subject,body,recipient):
	mailer.mail(subject,body,recipient)

def start_scheduler():
	scheduler.start()

