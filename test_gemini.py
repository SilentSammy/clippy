import sys
import time
from chrome import get_driver
from gemini import is_chat_ready, send_message, is_response_complete, get_latest_response

sys.stdout.reconfigure(encoding='utf-8')

driver = get_driver()

print("Waiting for Gemini tab...")
while not is_chat_ready(driver):
    time.sleep(0.5)
print("Gemini is ready.")

for msg in ["What is the capital of France? One sentence.", "What is the capital of Japan? One sentence."]:
    print(f"\nSending: {msg}")
    count_before = send_message(driver, msg)
    while not is_response_complete(driver, count_before):
        time.sleep(0.2)
    print(f"Response: {get_latest_response(driver)}")
