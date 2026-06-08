import re
import time
from selenium.common.exceptions import NoSuchWindowException

_INPUT_SEL = ".ql-editor.textarea[contenteditable='true']"
_SEND_BTN_SEL = "button[jslog^='173899']"
_ACTION_BTN_SEL = "button[aria-label]:not([aria-label=''])"


def is_chat_ready(driver):
    try:
        if "gemini.google.com" in driver.current_url:
            return bool(driver.find_elements("css selector", _INPUT_SEL))
        for handle in driver.window_handles:
            driver.switch_to.window(handle)
            if "gemini.google.com" in driver.current_url:
                return bool(driver.find_elements("css selector", _INPUT_SEL))
        return False
    except NoSuchWindowException:
        return False


def get_latest_response(driver):
    responses = driver.find_elements("css selector", "model-response")
    if not responses:
        return None
    text = responses[-1].text
    # Strip "Gemini said\n" / "Gemini dijo\n" / any localised variant
    text = re.sub(r'^Gemini \S+\n', '', text)
    return text


def send_message(driver, text):
    driver.execute_script("""
        const el = document.querySelector(arguments[1]);
        el.focus();
        document.execCommand('insertText', false, arguments[0]);
    """, text, _INPUT_SEL)
    count_before = len(driver.find_elements("css selector", "model-response"))
    driver.execute_script("""
        document.querySelector(arguments[0]).click();
    """, _SEND_BTN_SEL)
    return count_before


def is_response_complete(driver, count_before=None):
    responses = driver.find_elements("css selector", "model-response")
    if not responses:
        return False
    if count_before is not None and len(responses) <= count_before:
        return False
    return bool(responses[-1].find_elements("css selector", _ACTION_BTN_SEL))
