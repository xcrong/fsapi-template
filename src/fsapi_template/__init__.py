import uvicorn

from fastapi import FastAPI

from .config import uvicorn_config, logger

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


def main() -> int:
    logger.info("Start ... ")
    try:
        uvicorn.run(
            app=uvicorn_config.app,
            host=uvicorn_config.host,
            port=uvicorn_config.port,
            reload=uvicorn_config.reload,
            reload_includes=(
                uvicorn_config.reload_includes if uvicorn_config.reload else None
            ),
            log_level=uvicorn_config.log_level,
        )

        return 0
    except KeyboardInterrupt:
        logger.info("Done ...")
        return 1
