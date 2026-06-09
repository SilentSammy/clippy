import sys
import time
from chrome import get_driver
from chatgpt import ChatGPTBackend

sys.stdout.reconfigure(encoding='utf-8')

driver = get_driver()
bot = ChatGPTBackend(driver)

print("Waiting for ChatGPT tab...")
while not bot.is_chat_ready():
    time.sleep(0.5)
print("ChatGPT is ready.")

for msg in ["What is the capital of Italy? One sentence.", "What is the capital of Spain? One sentence."]:
    print(f"\nSending: {msg}")
    count_before = bot.send_message(msg)
    while not bot.is_response_complete(count_before):
        time.sleep(0.2)
    print(f"Response: {bot.get_latest_response()}")
