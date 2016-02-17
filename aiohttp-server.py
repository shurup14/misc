#!/usr/bin/env python3

from aiohttp.web import Application, StreamResponse
import msgpack, json, re, asyncio

result = {}

def packit(data):
    return msgpack.packb(json.dumps(data))

@asyncio.coroutine
def index(request):
    req = yield from request.read()
    test_date = json.loads(msgpack.unpackb(req).decode('utf8'))['test_date']
    if re.match(r'^\d{1,2}\.\d{1,2}\.\d{4}$', test_date):
        result['result'] = 'ok'
    else:
        result['result'] = 'error'
    answer = packit(result)
    resp = StreamResponse()
    resp.content_length = len(answer)
    yield from resp.prepare(request)
    resp.write(answer)
    return resp


@asyncio.coroutine
def init(loop, handler=None):
    app = Application(loop=loop)
    app.router.add_route('POST', '/', index)
    handler = app.make_handler()
    srv = yield from loop.create_server(handler, '127.0.0.1', 9999)
    print("Server started at http://127.0.0.1:9999")
    return srv, handler


loop = asyncio.get_event_loop()
srv, handler = loop.run_until_complete(init(loop))
try:
    loop.run_forever()
except KeyboardInterrupt:
    loop.run_until_complete(handler.finish_connections())
