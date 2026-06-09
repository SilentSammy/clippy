class ChatBackend:
    """Abstract base for a web-based LLM chat backend driven via Selenium."""

    def __init__(self, driver):
        self.driver = driver

    def is_chat_ready(self):
        """Return True if the chat UI is loaded and ready for input."""
        pass

    def get_latest_response(self):
        """Return the text of the latest assistant response, or None."""
        pass

    def clear_input(self):
        """Clear all text and images from the input box."""
        pass

    def paste_image(self, pil_image):
        """Paste a PIL Image into the input without sending."""
        pass

    def send_message(self, text):
        """Insert text and send the message. Return a pre-send marker (e.g. response count)."""
        pass

    def is_response_complete(self, count_before=None):
        """Return True if the latest response has finished streaming."""
        pass
