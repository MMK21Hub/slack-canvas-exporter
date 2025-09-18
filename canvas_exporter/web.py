import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse, Response
from pydantic import HttpUrl, ValidationError
from dotenv import load_dotenv

from canvas_exporter.slack import SlackClient

load_dotenv()
slack_token = os.environ.get("SLACK_TOKEN") or os.environ.get("SLACK_BOT_TOKEN")
if not slack_token:
    raise ValueError("SLACK_TOKEN environment variable is required")

app = FastAPI()
slack = SlackClient(token=slack_token)


@app.get("/")
def root():
    return JSONResponse(
        {
            "link": "https://github.com/MMK21Hub/slack-canvas-exporter",
            "hello": "Hello from Slack Canvas Exporter :)",
        }
    )


def canvas_id_from_url(canvas_identifier: str) -> str:
    # Canvas URLs look like: https://hackclub.slack.com/docs/T0266FRGM/F099JTRJXRA
    try:
        canvas_url = HttpUrl(canvas_identifier)
        path = canvas_url.path or ""
        path_parts = path.strip("/").split("/")
        if path_parts[0] != "docs":
            raise ValueError("Unexpected canvas URL format")
        return path_parts[2]
    except ValidationError:
        # If it's not a URL, assume it's a canvas ID
        if canvas_identifier.startswith("F"):
            return canvas_identifier
        raise ValueError("Invalid canvas ID or URL")


@app.get("/{canvas_identifier:path}")
def get_canvas(canvas_identifier: str):
    canvas_id = canvas_id_from_url(canvas_identifier)
    html_content = slack.get_canvas_html(canvas_id)
    return Response(content=html_content, media_type="text/html")
