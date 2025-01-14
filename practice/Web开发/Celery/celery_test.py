import time

from celery import Celery


app = Celery('celery_test', broker='redis://localhost:6379/0')
app.conf.broker_connection_retry_on_startup = True
# 时区设置
app.conf.enable_utc = False
app.conf.timezone = "Asia/Shanghai"


@app.task
def send_email():
    print('start send email')
    time.sleep(5)
    return 'ok'


@app.task
def send_sms():
    print('start send sms')
    time.sleep(5)
    return 'ok'
