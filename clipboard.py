import hashlib
import io
import pyperclip
from PIL import ImageGrab

_last = pyperclip.paste()
_last_image_hash = None


def _image_hash(img):
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return hashlib.md5(buf.getvalue()).hexdigest()


def clipboard_available():
    current = pyperclip.paste()
    return current if (current != _last and current.strip()) else None


def clipboard_image_available():
    global _last_image_hash
    img = ImageGrab.grabclipboard()
    if img is None:
        return None
    h = _image_hash(img)
    if h == _last_image_hash:
        return None
    _last_image_hash = h
    return img


def mark_image_seen():
    global _last_image_hash
    img = ImageGrab.grabclipboard()
    if img:
        _last_image_hash = _image_hash(img)


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
