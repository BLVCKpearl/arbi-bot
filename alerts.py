import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, EMAIL_SMTP_SERVER, EMAIL_SMTP_USER, EMAIL_SMTP_PASS, EMAIL_TO

class Alerts:
    """
    Handles notifications via Telegram and email.
    """
    def __init__(self):
        pass

    def send_telegram_alert(self, message):
        """
        Send a Telegram alert using the Telegram Bot API.
        """
        if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
            print("[ALERT] Telegram bot token or chat ID not set.")
            return
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
        try:
            resp = requests.post(url, data=data, timeout=10)
            if resp.status_code == 200:
                print("[ALERT] Telegram notification sent.")
            else:
                print(f"[ALERT] Failed to send Telegram notification: {resp.text}")
        except Exception as e:
            print(f"[ALERT] Telegram notification error: {e}")

    def send_email_alert(self, subject, message):
        """
        Stub: Send an email alert.
        """
        pass 