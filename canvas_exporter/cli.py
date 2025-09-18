from email.policy import default
import json
from pathlib import Path
from typing import Annotated
import click
from click import echo, secho
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
    echo(f"Exported to {file_path}")


@click.command("join")
@click.option("--token", envvar=["SLACK_TOKEN", "SLACK_BOT_TOKEN"])
@click.argument("channel_id")
def join_channel(channel_id: str, token: str):
    if not token:
        raise click.UsageError("SLACK_TOKEN environment variable is required")
    slack = SlackClient(token)
    try:
        response = slack.join_channel(channel_id)
        echo(f"Joined channel {channel_id} (#{response['channel']['name']})")
    except SlackApiError as e:
        echo(f"Error joining channel: {e.response['error']}")


class CanvasesConfig(BaseModel):
    channels: dict[ChannelId, dict[CanvasId, str]]  # channel_id -> list of canvas_ids


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
        if not isinstance(data, dict):
            raise click.ClickException(
                f"Invalid config file format: expected a dict, got {type(data)}"
            )
        config = CanvasesConfig(**data)
    slack = SlackClient(token)
    channel_names: dict[str, str] = {}
    echo(f"Ensuring the bot is in all {len(config.channels)} listed channels...")
    for channel_id in config.channels:
        try:
            response = slack.join_channel(channel_id)
            channel_names[channel_id] = response["channel"]["name"]
            if "warning" in response and response["warning"] == "already_in_channel":
                echo(
                    f"✅ Already in channel {channel_id} (#{response['channel']['name']})"
                )
            else:
                echo(f"🆕 Joined channel {channel_id} (#{response['channel']['name']})")
        except SlackApiError as e:
            echo(f"💥 Error joining channel {channel_id}: {e.response['error']}")
    echo("Downloading canvases...")
    for channel_id, canvases in config.channels.items():
        channel_name = channel_names.get(channel_id, channel_id)
        channel_dir = output / channel_name
        channel_dir.mkdir(parents=True, exist_ok=True)
        for canvas_id, canvas_name in canvases.items():
            canvas_info = slack.client.files_info(file=canvas_id)
            if not canvas_info["ok"]:
                secho(
                    f"💥 Error fetching canvas {canvas_id}: {canvas_info['error']}",
                    fg="red",
                )
                continue
            canvas_info_json = json.dumps(canvas_info["file"], indent=2)
            with open(channel_dir / f"{canvas_name}.json", "w") as json_file:
                json_file.write(canvas_info_json)


cli.add_command(export)
cli.add_command(join_channel)
cli.add_command(from_file)
