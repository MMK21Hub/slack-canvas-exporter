HACK_CLUB_WORKSPACE = "T0266FRGM"


def canvas_html_url(canvas_id: str) -> str:
    return f"https://files.slack.com/files-pri/{HACK_CLUB_WORKSPACE}-{canvas_id}/canvas"


def main():
    print("Hello from slack-canvas-exporter!")


if __name__ == "__main__":
    main()
