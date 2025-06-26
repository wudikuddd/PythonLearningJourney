"""
celery通过消息(任务)进行通信, 
celery通常使用一个叫Broker(中间人/消息中间件/消息队列/任务队列)来协助clients(任务的发出者/客户端)和worker(任务的处理者/工作进程)进行通信的.
clients发出消息到任务队列中, broker将任务队列中的信息派发给worker来处理。

client ---> 消息 --> Broker(消息队列) -----> 消息 ---> worker(celery运行起来的工作进程)

消息队列(Message Queue), 也叫消息队列中间件, 简称消息中间件, 它是一个独立运行的程序, 表示在消息的传输过程中临时保存消息的容器。
所谓的消息, 是指代在两台计算机或2个应用程序之间传送的数据。消息可以非常简单, 例如文本字符串或者数字, 也可以是更复杂的json数据或hash数据等。
所谓的队列, 是一种先进先出、后进呼后出的数据结构, python中的list数据类型就可以很方便地用来实现队列结构。
目前开发中, 使用较多的消息队列有RabbitMQ, Kafka, RocketMQ, MetaMQ, ZeroMQ, ActiveMQ等, 当然, 像redis、mysql、MongoDB, 也可以充当消息中间件, 但是相对而言, 没有上面那么专业和性能稳定。

并发任务10k以下的, 直接使用redis
并发任务10k以上, 1000k以下的, 直接使用RabbitMQ
并发任务1000k以上的, 直接使用RocketMQ

启动worker和beat:

celery -A app worker -l INFO -c 2 -B

"""
import time

from celery import Celery
from kombu import Queue, Exchange

app = Celery('app',
             broker='redis://localhost:6379/5',
             backend='redis://localhost:6379/6'
             )
app.conf.broker_connection_retry_on_startup = True
# 时区设置
app.conf.enable_utc = False
app.conf.timezone = "Asia/Shanghai"

# default Queue
app.conf.task_default_queue = 'default_app'
# default routing_key
app.conf.task_default_routing_key = 'task.default_app'

# task_routes
app.conf.task_routes = {
    'practice.celery_use.simple_use.send_slow_task': {
        'queue': 'default_app_slow',
        'routing_key': 'app_slow.task.send_slow_task'
    },
}

# task_queues
app.conf.task_queues = (
    # The non-AMQP backends like Redis or SQS don’t support exchanges,
    # so they require the exchange to have the same name as the queue.
    Queue(
        'default_app',
        exchange=Exchange('default_app', type='topic'),
        routing_key='app.task.#',
    ),
    Queue(
        'default_app_slow',
        exchange=Exchange('default_app_slow', type='topic'),
        routing_key='app_slow.task.#',
    ),
)

# 定时任务
app.conf.beat_schedule = {
    'test_beat': {
        'task': 'simple_use.test_beat',
        'schedule': 2,  # 每 2 秒运行
    },
}


@app.task()
def test_beat():
    print('start test_beat')
    time.sleep(5)
    return 'ok test_beat'


@app.task()
def send_email():
    print('start send email')
    time.sleep(5)
    return 'ok'


@app.task()
def send_sms():
    print('start send sms')
    time.sleep(3)
    return 'ok'



@app.task()
def send_slow_task():  # 测试耗时任务
    print('start send slow_task')
    time.sleep(50)
    return 'ok'


@app.task()
def test_raise():
    raise Exception('test_raise')
