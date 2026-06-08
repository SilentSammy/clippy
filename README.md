# Clippy

Monitors your clipboard and forwards its contents to Gemini. The response is copied back to your clipboard for easy pasting. Screenshots are also supported — paste multiple images before sending.

## Requirements

- Python 3
- Google Chrome
- `pip install -r requirements.txt`

## Usage

1. Run `main.py`
2. Clippy will launch Chrome automatically if it isn't already open
3. Navigate to [gemini.google.com](https://gemini.google.com) and log in
4. Copy any text — Clippy will send it to Gemini and copy the response back to your clipboard
5. Optionally take screenshots first (Win+Shift+S) — images are added to the prompt and sent with the next text you copy

## Clipboard Commands

| Command  | Description |
|----------|-------------|
| `!on`    | Enable Clippy |
| `!off`   | Disable Clippy |
| `!once`  | Send one message (including any queued images) then disable |
| `!clear` | Clear any images queued in the input box |
| `!help`  | Copy a brief command reference to the clipboard |

Commands are detected by copying them to the clipboard. Clippy will confirm the action by writing the result back to the clipboard.
