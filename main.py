import sys
import time
import pyperclip

from chrome import get_driver
from chatgpt import send_message, is_response_complete, get_latest_response, is_chat_ready

sys.stdout.reconfigure(encoding='utf-8')

driver = get_driver()

last_clipboard = pyperclip.paste()
waiting_for_response = False
chat_ready = None

print("Clippy is running. Copy any text to send it to ChatGPT.")

while True:
    time.sleep(0.5)

    ready = is_chat_ready(driver)
    if ready != chat_ready:
        chat_ready = ready
        if ready:
            print("ChatGPT is ready.")
        else:
            print("ChatGPT is not ready. Please open chatgpt.com.")

    if not chat_ready:
        continue

    if waiting_for_response:
        if is_response_complete(driver):
            response = get_latest_response(driver)
            pyperclip.copy(response)
            last_clipboard = response
            waiting_for_response = False
            print("Response copied to clipboard.")
        continue

    current_clipboard = pyperclip.paste()

    if current_clipboard == last_clipboard or not current_clipboard.strip():
        continue

    last_clipboard = current_clipboard
    print(f"Sending: {current_clipboard[:80]}...")
    send_message(driver, current_clipboard)
    waiting_for_response = True
