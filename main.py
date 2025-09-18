import click
import requests

HACK_CLUB_WORKSPACE = "T0266FRGM"


def canvas_html_url(canvas_id: str) -> str:
    return f"https://files.slack.com/files-pri/{HACK_CLUB_WORKSPACE}-{canvas_id}/canvas"


@click.command()
@click.argument("canvas_id")
def export(canvas_id: str):
    url = canvas_html_url(canvas_id)
    print(f"Canvas URL: {url}")
    response = requests.get(url)
    response.raise_for_status()
    file_name = f"{canvas_id}.html"


if __name__ == "__main__":
    export()
