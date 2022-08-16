from asyncore import poll
import sys
import uuid
sys.path.append('./app')

import pytest
import dataclasses
import redis
import json
from app import settings
from app.app import create_app 
from app.app import execute_alert_job
from app.entities import Alert


@pytest.fixture
def redis_conn():
    conn = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
    yield conn
    conn.flushall()

@pytest.fixture
async def client(aiohttp_client):
    web_app = await create_app()
    return await aiohttp_client(web_app) 

async def test_registry(client, redis_conn):
    resp = await client.post('/api/v1/register', json = {
        'n_msgs': 5,
        'monitor_rate': 1,
        'fail_rate': 0.25,
        'num_senders': 5,
        'poll_rate': 2,
    })
    assert resp.status == 200
    payload = await resp.json()
    alert_entity_id = payload['id']
    assert alert_entity_id
    # Verify we saved something
    saved_redis = redis_conn.get(alert_entity_id)
    assert saved_redis

    # Verify we saved the right stuff
    saved_redis_json = json.loads(saved_redis)
    for i in range(int(saved_redis_json['n_msgs'])):
        entry = redis_conn.lpop(saved_redis_json['queue_id'])
        # Save the index starting at 0
        assert int(entry) == i
    assert not redis_conn.lpop(saved_redis_json['queue_id'])

    # Verify we saved numPassed and numFailed
    assert json.loads(redis_conn.get(f'{alert_entity_id}.num_passed')) == 0
    assert json.loads(redis_conn.get(f'{alert_entity_id}.num_failed')) == 0

@pytest.mark.parametrize('fail_rate', [0, 1])
async def test_job_execution_increments(redis_conn, fail_rate):
    queue_id = str(uuid.uuid4())
    alert_entity_id = str(uuid.uuid4())
    n_msgs = 10

    redis_conn.set(alert_entity_id, json.dumps(
        dataclasses.asdict(Alert(
            queue_id = queue_id,
            n_msgs = n_msgs,
            fail_rate = fail_rate,
            num_senders=1,
            poll_rate=1,
        ))
    ))
    redis_conn.set(f'{alert_entity_id}.num_passed', 0)
    redis_conn.set(f'{alert_entity_id}.num_failed', 0)

    for i in range(n_msgs):
        redis_conn.rpush(queue_id, i)
    # Act
    await execute_alert_job(alert_entity_id)

    # Assert
    num_passed = json.loads(redis_conn.get(f'{alert_entity_id}.num_passed'))
    num_failed = json.loads(redis_conn.get(f'{alert_entity_id}.num_failed'))
    if fail_rate == 1:
        assert num_passed == 0
        assert num_failed == n_msgs
    else:
        assert num_passed == n_msgs
        assert num_failed == 0
    
    assert not redis_conn.lpop(queue_id)

async def test_simple_get(client, redis_conn):
    key = str(uuid.uuid4())
    queue_id = str(uuid.uuid4())
    msgs_in_queue = 19

    n_msgs = 100
    num_senders = 5
    num_passed = 10
    num_failed = 3
    poll_rate = 1
    redis_conn.set(key, json.dumps(dataclasses.asdict(Alert(
            queue_id = queue_id,
            n_msgs = n_msgs,
            fail_rate = 0.25,
            num_senders=num_senders,
            poll_rate=poll_rate,
        ))))
    redis_conn.set(f'{key}.num_passed', num_passed)
    redis_conn.set(f'{key}.num_failed', num_failed)
    for i in range(msgs_in_queue):
        redis_conn.rpush(queue_id, i)

    # Act
    response = await client.get(f'/api/v1/alerts?id={key}')
    # Assert
    assert response.status == 200
    response_json = await response.json()
    assert response_json['num_passed'] == num_passed
    assert response_json['num_failed'] == num_failed
    assert response_json['num_senders'] == num_senders
    assert response_json['poll_rate'] == poll_rate
    assert response_json['remaining_msgs'] == msgs_in_queue