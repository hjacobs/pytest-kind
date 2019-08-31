from aiohttp import web


async def hello(request):
    return web.Response(text="Hello, world")


async def health(request):
    return web.Response(text="OK")


app = web.Application()
app.add_routes([web.get("/", hello)])
app.add_routes([web.get("/health", health)])
web.run_app(app)
