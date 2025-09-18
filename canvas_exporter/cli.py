from email.policy import default
from pathlib import Path
from typing import Annotated
import click
import yaml
from slack_sdk.errors import SlackApiError
from canvas_exporter.slack import SlackClient
from pydantic import BaseModel, field_validator, Field

from canvas_exporter.slack_types import CanvasId, ChannelId


@click.group()
def cli():
    pass


@click.command()
@click.option("--token", envvar=["SLACK_TOKEN", "SLACK_BOT_TOKEN"])
@click.option("--output", default=None)
@click.argument("canvas_id")
def export(canvas_id: str, token: str, output: str | None):
    if not token:
        raise click.UsageError("SLACK_TOKEN environment variable is required")
    slack = SlackClient(token)
    html_content = slack.get_canvas_html(canvas_id)
    file_path = Path(output) if output else Path("output", f"{canvas_id}.html")
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(html_content, encoding="utf-8")
    print(f"Exported to {file_path}")


@click.command("join")
@click.option("--token", envvar=["SLACK_TOKEN", "SLACK_BOT_TOKEN"])
@click.argument("channel_id")
def join_channel(channel_id: str, token: str):
    if not token:
        raise click.UsageError("SLACK_TOKEN environment variable is required")
    slack = SlackClient(token)
    try:
        response = slack.join_channel(channel_id)
        print(f"Joined channel {channel_id} (#{response['channel']['name']})")
    except SlackApiError as e:
        print(f"Error joining channel: {e.response['error']}")


class CanvasesConfig(BaseModel):
    channels: dict[ChannelId, list[CanvasId]]  # channel_id -> list of canvas_ids


@click.command("from-file")
@click.option("--token", envvar=["SLACK_TOKEN", "SLACK_BOT_TOKEN"])
@click.option(
    "--output",
    type=click.Path(),
    default=Path("..", "canvases"),
    help="directory to save the canvases in",
)
@click.argument("config_file", type=click.Path(exists=True))
def from_file(config_file: str, token: str, output: Path):
    if not token:
        raise click.UsageError("SLACK_TOKEN environment variable is required")
    with open(config_file, "r") as file:
        data = yaml.safe_load(file)
        config = CanvasesConfig(**data)
    slack = SlackClient(token)
    for channel_id in config.channels:
        try:
            response = slack.join_channel(channel_id)
            print(f"✅ Joined channel {channel_id} (#{response['channel']['name']})")
        except SlackApiError as e:
            print(f"Error joining channel {channel_id}: {e.response['error']}")


cli.add_command(export)
cli.add_command(join_channel)
cli.add_command(from_file)
