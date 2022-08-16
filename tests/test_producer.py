import sys
sys.path.append('./app')

from app.producer import Producer


def test_producer():
    p = Producer(2).messages()
    first = next(p)
    second = next(p)
    for record in [first, second]:
        assert len(record['msg_txt']) == 100
        assert 0 <= record['phone_num'] < 10000000000
    