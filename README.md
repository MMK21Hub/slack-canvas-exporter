# Slack Canvas Exporter

## Requirements

Python and `uv`

## Using the command-line tool

```bash
uv run main.py export --token <SLACK_TOKEN> [CANVAS_ID]
```

Slack tokens are accepted as a argument (`--token`), or as an environment variable (`SLACK_TOKEN` or `SLACK_BOT_TOKEN`).

### Joining a channel

The bot account has to be in the channel to export a canvas from it. You can join channels using the script like so:

```bash
uv run main.py join --token <SLACK_TOKEN> [CHANNEL_ID]
```

## Running the web service

```bash
uv run fastapi dev canvas_exporter/web.py
```

Then visit `http://127.0.0.1:8000/LINK`, replacing `LINK` with the link to the Slack canvas you want to view/export.
