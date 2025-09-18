# Slack Canvas Exporter

## Requirements

Python and `uv`

## Usage

```bash
uv run main.py export --token <SLACK_TOKEN> [CANVAS_ID]
```

Slack tokens are accepted as a argument (`--token`), or as an environment variable (`SLACK_TOKEN` or `SLACK_BOT_TOKEN`).

### Joining a channel

The bot account has to be in the channel to export a canvas from it. You can join channels using the script like so:

```bash
uv run main.py join --token <SLACK_TOKEN> [CHANNEL_ID]
```
