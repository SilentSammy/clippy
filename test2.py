import sys
import time
from chrome import get_driver
from chatgpt import get_latest_response

sys.stdout.reconfigure(encoding='utf-8')

driver = get_driver()

print("Driver attached. Polling get_latest_response...")
while True:
    response = get_latest_response(driver)
    if response:
        print(response)
    time.sleep(0.3)
