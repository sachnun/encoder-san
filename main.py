import os, sys
from typing import Union
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse, StreamingResponse

from utils.pdf import WebPDF


tags_metadata = [
    {
        "name": "web-convert",
        "description": "Convert web pages to PDF, EPUB, MOBI, and more.",
    },
]

description = """
A simple API for encoding files to various formats.
"""

app = FastAPI(
    title="Encoder-san API",
    description=description,
    version="0.1.0",
    openapi_tags=tags_metadata,
    redoc_url=None,
    docs_url="/docs",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# redirect to docs
@app.get("/", include_in_schema=False)
def redirect():
    return RedirectResponse(url="/docs")


# web to PDF
@app.get(
    "/web-convert/pdf",
    tags=["web-convert"],
    summary="Convert web pages to PDF",
    description="Convert web pages to PDF",
    responses={
        200: {
            "description": "PDF file",
            "content": {
                "application/pdf": {"schema": {"type": "string", "format": "binary"}}
            },
        }
    },
)
def web_to_pdf(
    url: str = Query(
        ...,
        description="URL of the web page to convert",
        example="https://google.com",
    ),
):
    # refactor url
    # remove http:// or https://
    # remove www.
    # remove trailing slash
    # get domain name
    filename = (
        url.replace("http://", "")
        .replace("https://", "")
        .replace("www.", "")
        .rstrip("/")
        .split("/")[0]
    )

    pdf = WebPDF()
    file = pdf.convert(url)

    return StreamingResponse(
        file,
        media_type="application/pdf",
        headers={
            # filename like url with ext .pdf
            "Content-Disposition": f"attachment; filename={filename}.pdf",
        },
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000)
