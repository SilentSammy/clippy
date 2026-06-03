import pyperclip

_last = pyperclip.paste()


def clipboard_available():
    current = pyperclip.paste()
    return current if (current != _last and current.strip()) else None


def clipboard_read():
    global _last
    while True:
        current = pyperclip.paste()
        if current != _last and current.strip():
            _last = current
            return current


def clipboard_write(text):
    global _last
    _last = text
    pyperclip.copy(text)
