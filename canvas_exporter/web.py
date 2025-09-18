from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import HttpUrl

app = FastAPI()


@app.get("/")
def root():
    return JSONResponse(
        {
            "link": "https://github.com/MMK21Hub/slack-canvas-exporter",
            "hello": "Hello from Slack Canvas Exporter :)",
        }
    )


@app.get("/{canvas_url}")
def get_canvas(canvas_url: HttpUrl):
    return {"canvas_url": canvas_url}
