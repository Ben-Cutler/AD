from aiohttp import web
from aiohttp.web import json_response, run_app
from redis import Redis
from app.entities import Alert
from .producer import Producer
from .consumer import Consumer
import asyncio
import time
import settings
import random
import dataclasses
import uuid
import json


async def create_app():
    app = web.Application() 
    setup_register_route(app)
    return app

def setup_register_route(app):
    app.router.add_route('POST', '/api/v1/register', register_alert)
    app.router.add_route('POST', '/api/v1/execute', execute_alert)
    app.router.add_route('GET', '/api/v1/alerts', get_alert)

async def register_alert(request: web.Request):
    redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
    request_json = await request.json()
    
    alert_key = str(uuid.uuid4())
    alert_queue_key = str(uuid.uuid4())
    
    num_msgs_to_send = request_json.get('n_msgs', 1000)
    redis.set(alert_key, json.dumps(
        dataclasses.asdict(Alert(
            queue_id = alert_queue_key,
            n_msgs = num_msgs_to_send,
            fail_rate = request_json['fail_rate'],
            num_senders=request_json['num_senders'],
            poll_rate=request_json['poll_rate']
        ))
    ))
    redis.set(f'{alert_key}.num_passed', 0)
    redis.set(f'{alert_key}.num_failed', 0)

    # Populate queue with "jobs" so we have a thread-safe way of processing SMSs
    for i in range(num_msgs_to_send):
        redis.rpush(alert_queue_key, i)
        
    return json_response({'id': alert_key})
    
async def execute_alert(request: web.Request):
    redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
    request_json = await request.json()
    redis_payload = json.loads(redis.get(request_json['id']))
    for _ in range(redis_payload['num_senders']):
        asyncio.create_task(execute_alert_job(request_json['id']))
    
async def execute_alert_job(alert_entity_id):
    redis_conn = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
    alert_instance = json.loads(redis_conn.get(alert_entity_id))
    notification_provider = Producer(alert_instance['n_msgs']).messages()
    notification_consumer = Consumer()
    while True:
        alert_id = redis_conn.lpop(alert_instance['queue_id'])
        if not alert_id:
            break 
        payload = next(notification_provider)
        time.sleep(abs(random.normalvariate(settings.MEAN_SEND_TIME, 0.25)))
        if random.random() > alert_instance['fail_rate']:
            notification_consumer.consume(payload)
            redis_conn.incrby(f'{alert_entity_id}.num_passed', 1)
        else:
            redis_conn.incrby(f'{alert_entity_id}.num_failed', 1)

async def get_alert(request: web.Request):
    redis_conn = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
    _id = request.query['id']
    alert_entity = json.loads(redis_conn.get(_id))
    passed = int(redis_conn.get(f'{_id}.num_passed'))
    failed = int(redis_conn.get(f'{_id}.num_failed'))
    queue_sz = redis_conn.llen(alert_entity['queue_id'])
    if not queue_sz:
        queue_sz = 0
    return json_response({
            'num_passed' : passed,
            'num_failed': failed,
            'num_senders': alert_entity['num_senders'],
            'poll_rate': alert_entity['poll_rate'],
            'remaining_msgs': queue_sz,
    })
    
if __name__ == '__main__':
    run_app(
        app = create_app(),
        host = settings.HOST,
        port = settings.PORT,
    )