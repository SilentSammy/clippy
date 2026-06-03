import time
from selenium.common.exceptions import NoSuchWindowException


def is_chat_ready(driver):
    try:
        if "gemini.google.com" in driver.current_url:
            return bool(driver.find_elements("css selector", "[aria-label='Enter a prompt for Gemini']"))
        for handle in driver.window_handles:
            driver.switch_to.window(handle)
            if "gemini.google.com" in driver.current_url:
                return bool(driver.find_elements("css selector", "[aria-label='Enter a prompt for Gemini']"))
        return False
    except NoSuchWindowException:
        return False


def get_latest_response(driver):
    responses = driver.find_elements("css selector", "model-response")
    if not responses:
        return None
    text = responses[-1].text
    # Strip "Gemini said\n" prefix if present
    prefix = "Gemini said\n"
    if text.startswith(prefix):
        text = text[len(prefix):]
    return text


def send_message(driver, text):
    driver.execute_script("""
        const el = document.querySelector('[aria-label="Enter a prompt for Gemini"]');
        el.focus();
        document.execCommand('insertText', false, arguments[0]);
    """, text)
    count_before = len(driver.find_elements("css selector", "model-response"))
    driver.execute_script("""
        const btn = Array.from(document.querySelectorAll('button'))
            .find(b => b.getAttribute('aria-label') === 'Send message');
        btn.click();
    """)
    return count_before


def is_response_complete(driver, count_before=None):
    responses = driver.find_elements("css selector", "model-response")
    if not responses:
        return False
    if count_before is not None and len(responses) <= count_before:
        return False
    last = responses[-1]
    return bool(last.find_elements("css selector", "button[aria-label='Good response']"))
