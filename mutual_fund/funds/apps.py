from django.apps import AppConfig

class FundsConfig(AppConfig):
    name = 'funds'

    def ready(self):
        from apscheduler.schedulers.background import BackgroundScheduler
        from .tasks import update_mutual_fund_schemes
        scheduler = BackgroundScheduler()
        scheduler.add_job(update_mutual_fund_schemes, 'interval', hours=1, id='update_mutual_fund_schemes', replace_existing=True)
        scheduler.start()
