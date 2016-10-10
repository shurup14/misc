from aiohttp import web
import aiohttp


def send_all(users, message):
    for user in users:
        user.send_str(message)

async def websocket_handler(request):

    ws = web.WebSocketResponse(autoclose=False)
    await ws.prepare(request)

    users = request.app['users']

    try:
        if ws not in users:
            ws.send_str('Provide your name:')
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                if ws not in users:
                    users[ws] = msg.data
                    send_all(users, '{} joined us'.format(msg.data))
                else:
                    send_all(users, '{}: {}'.format(users[ws], msg.data))
            elif msg.type == aiohttp.WSMsgType.ERROR:
                print('ws connection closed with exception %s' %
                      ws.exception())
    finally:
        if ws in users:
            await ws.close()
            if ws.closed:
                name = users[ws]
                del users[ws]
                send_all(users, '{} left us'.format(name))

    return ws


def make_app():
    app = web.Application()
    app.router.add_route('GET', '/', websocket_handler)
    app['users'] = {}
    return app

web.run_app(make_app(), port=9000)
