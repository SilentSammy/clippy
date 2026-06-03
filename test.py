import sys
import time

from chrome import get_driver
from chatgpt import send_message, is_chat_ready, get_latest_response

sys.stdout.reconfigure(encoding='utf-8')

driver = get_driver()

print("Waiting for ChatGPT to be ready...")
while not is_chat_ready(driver):
    time.sleep(0.5)
print("ChatGPT is ready.")

# user_input = input("You: ")
# send_message(driver, user_input)

while True:
    response = get_latest_response(driver)
    if response:
        print(response)
    time.sleep(0.3)
