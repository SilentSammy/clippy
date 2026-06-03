import sys
import time

from chrome import get_driver
# from chatgpt import send_message, is_response_complete, get_latest_response, is_chat_ready
from gemini import send_message, is_response_complete, get_latest_response, is_chat_ready
from clipboard import clipboard_available, clipboard_read, clipboard_write

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

def cmd_help():
    clipboard_write("!on: enable | !off: disable | !once: send one message then disable | !help: show this")
    print("Help copied to clipboard.")

cmd_dict = {
    "!on": cmd_on,
    "!off": cmd_off,
    "!once": cmd_once,
    "!help": cmd_help,
}

sys.stdout.reconfigure(encoding='utf-8')

driver = get_driver()

waiting_for_response = False
count_before = 0
chat_ready = None

print("Clippy is running.")

while True:
    time.sleep(0.5)

    ready = is_chat_ready(driver)
    if ready != chat_ready:
        chat_ready = ready
        if ready:
            print("Chat is ready.")
        else:
            print("Chat is not ready. Please open _.com.")

    if not chat_ready:
        continue

    if waiting_for_response:
        if is_response_complete(driver, count_before):
            clipboard_write(get_latest_response(driver))
            waiting_for_response = False
            print("Response copied to clipboard.")
        continue

    text = clipboard_available()
    if text:
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
        count_before = send_message(driver, text)
        waiting_for_response = True
