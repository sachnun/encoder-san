from typing import Union
from fastapi import FastAPI, Response
from pydantic import BaseModel
from subtitle import Subtitle

import aiohttp


class Item(BaseModel):
    id: str


app = FastAPI()


@app.get("/")
def read_root():
    return {
        "title": "Encoder service",
        "description": "This service is used to encode anything",
        "version": "0.0.1",
    }


@app.post("/caption")
async def caption(item: Item):
    async with aiohttp.ClientSession() as session:
        async with session.request(
            "COPY", "https://gdrive-index.dakunesu.workers.dev/?id=" + item.id
        ) as response:

            if response.status != 200:
                return Response(status_code=404)

            subs = Subtitle(await response.text())
            return Response(content=subs.generate(), media_type="text/vtt")


# if 500 error, check the log
@app.exception_handler(Exception)
async def exception_handler(request, exc):
    return Response(
        content={
            "error": "Internal server error",
            "message": str(exc),
        },
        status_code=500,
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
