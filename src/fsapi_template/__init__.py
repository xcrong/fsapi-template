import uvicorn
from fastapi import FastAPI

from .config import logger, uvicorn_config

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/fib")
def fib(n: int):
    if n <= 0:
        return 0
    elif n == 1 or n == 2:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


def main() -> int:  # pragma: no cover
    logger.info("Start ... ")
    try:
        uvicorn.run(
            app=uvicorn_config.app,
            host=uvicorn_config.host,
            port=uvicorn_config.port,
            reload=uvicorn_config.reload,
            reload_includes=(
                uvicorn_config.reload_includes
                if uvicorn_config.reload
                else None
            ),
            log_level=uvicorn_config.log_level,
        )

        return 0
    except KeyboardInterrupt:
        logger.info("Done ...")
        return 1
