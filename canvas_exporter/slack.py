import requests
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from canvas_exporter.constants import HACK_CLUB_WORKSPACE


def canvas_html_url(canvas_id: str) -> str:
    return f"https://files.slack.com/files-pri/{HACK_CLUB_WORKSPACE}-{canvas_id}/canvas"


class SlackClient:
    def __init__(self, token: str):
        self.token = token
        self.client = WebClient(token=token)
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json; charset=utf-8",
        }

    def join_channel(self, channel_id: str):
        return self.client.conversations_join(channel=channel_id)

    def get_canvas_html(self, canvas_id: str) -> str:
        url = canvas_html_url(canvas_id)
        print(f"Canvas URL: {url}")
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.text
