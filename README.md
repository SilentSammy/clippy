# Clippy

Monitors your clipboard and forwards its contents to ChatGPT. The response is copied back to your clipboard for easy pasting.

## Requirements

- Python 3
- Google Chrome
- `pip install -r requirements.txt`

## Usage

1. Run `main.py`
2. Clippy will launch Chrome automatically if it isn't already open
3. Navigate to [chatgpt.com](https://chatgpt.com) and log in
4. Copy any text — Clippy will send it to ChatGPT and copy the response back to your clipboard

## Clipboard Commands

| Command | Description |
|---------|-------------|
| `!on`   | Enable Clippy |
| `!off`  | Disable Clippy |
| `!once` | Send the next copied text to ChatGPT, then disable |
| `!help` | Copy a brief command reference to the clipboard |


Commands are detected by copying them to the clipboard. Clippy will confirm the action by writing the result back to the clipboard.
