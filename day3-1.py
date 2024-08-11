import logging
from asgi_correlation_id import correlation_id_filter, CorrelationIdMiddleware
from fastapi import FastAPI

logger = logging.getLogger(__name__)

def configure_logging():
    cid_filter = correlation_id_filter(uuid_length=32)
    console_handler = logging.StreamHandler()
    console_handler.addFilter(cid_filter())
    logging.basicConfig(
        handlers=[console_handler],
        level=logging.DEBUG,
        format='%(levelname)s: \t  %(asctime)s %(name)s:%(lineno)d [%(correlation_id)s] %(message)s'
    )


app = FastAPI(on_startup=[configure_logging])
app.add_middleware(CorrelationIdMiddleware)


@app.get("/")
async def read_root(request: Request):
    correlation_id = request.headers.get("X-Correlation-ID")
    return {"message": "Hello World", "correlation_id": correlation_id}

