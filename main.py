from email.policy import default
from pathlib import Path
import click
import requests

HACK_CLUB_WORKSPACE = "T0266FRGM"


def canvas_html_url(canvas_id: str) -> str:
    return f"https://files.slack.com/files-pri/{HACK_CLUB_WORKSPACE}-{canvas_id}/canvas"


@click.command()
@click.option("--token", envvar=["SLACK_TOKEN", "SLACK_BOT_TOKEN"])
@click.option("--output", default=None)
@click.argument("canvas_id")
def export(canvas_id: str, token: str, output: str | None):
    if not token:
        raise click.UsageError("SLACK_TOKEN environment variable is required")

    url = canvas_html_url(canvas_id)
    print(f"Canvas URL: {url}")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    file_path = Path(output) if output else Path("output", f"{canvas_id}.html")
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(response.text)
    print(f"Exported to {file_path}")


if __name__ == "__main__":
    export()
