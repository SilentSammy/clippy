import base64
import io
import re
import time
import uuid
from selenium.common.exceptions import NoSuchWindowException

from backend import ChatBackend

_INPUT_SEL = ".ql-editor.textarea[contenteditable='true']"
_SEND_BTN_SEL = "button[jslog^='173899']"
_ACTION_BTN_SEL = "button[aria-label]:not([aria-label=''])"
_URL_FRAGMENT = "gemini.google.com"


class GeminiBackend(ChatBackend):
    """Drives the Gemini web UI (gemini.google.com) via Selenium."""

    def is_chat_ready(self):
        try:
            if _URL_FRAGMENT in self.driver.current_url:
                return bool(self.driver.find_elements("css selector", _INPUT_SEL))
            for handle in self.driver.window_handles:
                self.driver.switch_to.window(handle)
                if _URL_FRAGMENT in self.driver.current_url:
                    return bool(self.driver.find_elements("css selector", _INPUT_SEL))
            return False
        except NoSuchWindowException:
            return False

    def get_latest_response(self):
        responses = self.driver.find_elements("css selector", "model-response")
        if not responses:
            return None
        text = responses[-1].text
        # Strip "Gemini said\n" / "Gemini dijo\n" / any localised variant
        text = re.sub(r'^Gemini \S+\n', '', text)
        return text

    def _wait_for_send_btn(self, timeout=6):
        for _ in range(int(timeout / 0.2)):
            btns = self.driver.find_elements("css selector", _SEND_BTN_SEL)
            if btns and btns[0].is_enabled() and not btns[0].get_attribute("disabled"):
                return True
            time.sleep(0.2)
        return False

    def clear_input(self):
        self.driver.execute_script("""
            const el = document.querySelector(arguments[0]);
            el.innerHTML = '<p><br></p>';
            el.dispatchEvent(new Event('input', { bubbles: true }));
        """, _INPUT_SEL)

    def paste_image(self, pil_image):
        buf = io.BytesIO()
        pil_image.save(buf, format="PNG")
        b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
        self.driver.execute_script("""
            const b64 = arguments[0];
            const inputSel = arguments[1];
            const byteChars = atob(b64);
            const byteNums = new Uint8Array(byteChars.length);
            for (let i = 0; i < byteChars.length; i++) byteNums[i] = byteChars.charCodeAt(i);
            const blob = new Blob([byteNums], { type: 'image/png' });
            const file = new File([blob], arguments[2], { type: 'image/png' });
            const dt = new DataTransfer();
            dt.items.add(file);
            const el = document.querySelector(inputSel);
            el.focus();
            el.dispatchEvent(new ClipboardEvent('paste', {
                clipboardData: dt,
                bubbles: true,
                cancelable: true
            }));
        """, b64, _INPUT_SEL, f"screenshot-{uuid.uuid4().hex[:8]}.png")
        self._wait_for_send_btn()

    def send_message(self, text):
        self.driver.execute_script("""
            const el = document.querySelector(arguments[1]);
            el.focus();
            document.execCommand('insertText', false, arguments[0]);
        """, text, _INPUT_SEL)
        count_before = len(self.driver.find_elements("css selector", "model-response"))
        self._wait_for_send_btn()
        self.driver.execute_script("document.querySelector(arguments[0]).click();", _SEND_BTN_SEL)
        return count_before

    def is_response_complete(self, count_before=None):
        responses = self.driver.find_elements("css selector", "model-response")
        if not responses:
            return False
        if count_before is not None and len(responses) <= count_before:
            return False
        return bool(responses[-1].find_elements("css selector", _ACTION_BTN_SEL))
