import time
from selenium.common.exceptions import NoSuchWindowException


def is_chat_ready(driver):
    try:
        # If we're already on chatgpt.com, just check for the input
        if "chatgpt.com" in driver.current_url:
            return bool(driver.find_elements("css selector", "#prompt-textarea"))
        # Otherwise scan handles to find the right tab — only switch once
        for handle in driver.window_handles:
            driver.switch_to.window(handle)
            if "chatgpt.com" in driver.current_url:
                return bool(driver.find_elements("css selector", "#prompt-textarea"))
        return False
    except NoSuchWindowException:
        return False


def get_latest_response(driver):
    messages = driver.find_elements("css selector", "[data-message-author-role='assistant'] .markdown")
    return messages[-1].text if messages else None


def send_message(driver, text):
    driver.execute_script("""
        const el = document.querySelector('#prompt-textarea');
        el.focus();
        document.execCommand('insertText', false, arguments[0]);
    """, text)
    driver.execute_script("""
        const btn = document.querySelector('[data-testid="send-button"]');
        btn.click();
    """)


def is_response_complete(driver):
    turns = driver.find_elements("css selector", "[data-turn='assistant']")
    if not turns:
        return False
    return bool(turns[-1].find_elements("css selector", "[data-testid='good-response-turn-action-button']"))


def wait_for_response(driver, poll_interval=0.2):
    while not is_response_complete(driver):
        time.sleep(poll_interval)
    return get_latest_response(driver)
