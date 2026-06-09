import sys
import time

from chrome import get_driver
from gemini import GeminiBackend
from chatgpt import ChatGPTBackend
from clipboard import clipboard_available, clipboard_read, clipboard_write, clipboard_image_available, mark_image_seen

enabled = True
one_shot = False

def cmd_on():
    global enabled
    enabled = True
    clipboard_write("Clippy enabled.")
    print("Clippy enabled.")

def cmd_off():
    global enabled
    enabled = False
    clipboard_write("Clippy disabled.")
    print("Clippy disabled.")

def cmd_once():
    global one_shot
    one_shot = True
    clipboard_write("Clippy ready for one message.")
    print("One-shot armed.")

def cmd_clear():
    backend.clear_input()
    clipboard_write("Input cleared.")
    print("Input cleared.")

def cmd_gemini():
    global backend, chat_ready
    backend = GeminiBackend(driver)
    chat_ready = None
    clipboard_write("Switched to Gemini.")
    print("Switched to Gemini.")

def cmd_chatgpt():
    global backend, chat_ready
    backend = ChatGPTBackend(driver)
    chat_ready = None
    clipboard_write("Switched to ChatGPT.")
    print("Switched to ChatGPT.")

def cmd_help():
    clipboard_write("!on: enable | !off: disable | !once: one message then disable | !clear: clear input | !gemini: use Gemini | !chatgpt: use ChatGPT | !help: show this")
    print("Help copied to clipboard.")

cmd_dict = {
    "!on": cmd_on,
    "!off": cmd_off,
    "!once": cmd_once,
    "!clear": cmd_clear,
    "!gemini": cmd_gemini,
    "!chatgpt": cmd_chatgpt,
    "!help": cmd_help,
}

sys.stdout.reconfigure(encoding='utf-8')

driver = get_driver()
backend = GeminiBackend(driver)
# backend = ChatGPTBackend(driver)

waiting_for_response = False
count_before = 0
chat_ready = None

print("Clippy is running.")

while True:
    time.sleep(0.5)

    ready = backend.is_chat_ready()
    if ready != chat_ready:
        chat_ready = ready
        if ready:
            print("Chat is ready.")
        else:
            print("Chat is not ready. Please open _.com.")

    if not chat_ready:
        continue

    if waiting_for_response:
        if backend.is_response_complete(count_before):
            clipboard_write(backend.get_latest_response())
            waiting_for_response = False
            print("Response copied to clipboard.")
        continue

    text = clipboard_available()
    img = clipboard_image_available()

    if img:
        mark_image_seen()
        if enabled or one_shot:
            backend.paste_image(img)
            clipboard_write("Image added to prompt. Copy text to send.")
            print("Image pasted into prompt.")
    elif text:
        clipboard_read()  # mark as seen
        if text.strip() in cmd_dict:
            cmd_dict[text.strip()]()
            continue
        if not enabled and not one_shot:
            continue
        if one_shot:
            one_shot = False
            enabled = False
        print(f"Sending: {text[:80]}...")
        clipboard_write("Waiting for response...")
        count_before = backend.send_message(text)
        waiting_for_response = True
