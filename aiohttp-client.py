import aiohttp
import asyncio
import json
import msgpack

dates = ['01.12.2015', '2 november 2015', '2.11.15', '1.7.2013']

def packit(data):
    return msgpack.packb(json.dumps(data))

@asyncio.coroutine
def go(session):
    for date in dates:
        data = packit(dict(test_date=date))
        resp = yield from session.post('http://127.0.0.1:9999', data=data)
        answer = yield from resp.read()
        print('INFO: [{}] - {}'.format(date, json.loads(msgpack.unpackb(answer).decode('utf8'))['result']))
        yield from resp.release()

loop = asyncio.get_event_loop()
session = aiohttp.ClientSession(loop=loop)
loop.run_until_complete(go(session))
session.close()
loop.stop()
loop.run_forever()
loop.close()
