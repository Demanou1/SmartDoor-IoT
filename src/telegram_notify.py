# telegram_notify.py
# Smart Door System — Telegram Nachricht + Foto senden
# Autor: Ydriss Armel Demanou | Westfälische Hochschule Gelsenkirchen 2026

import requests

class TelegramNotifier:
    """
    Sendet Textnachrichten und Fotos ueber die Telegram Bot API.
    Kommunikation erfolgt ueber HTTPS an api.telegram.org.
    """

    def __init__(self, token: str, chat_id: str):
        self.base    = f"https://api.telegram.org/bot{token}"
        self.chat_id = chat_id

    def send_text(self, text: str):
        """Textnachricht senden."""
        r = requests.post(
            f"{self.base}/sendMessage",
            data={"chat_id": self.chat_id, "text": text},
            timeout=10
        )
        r.raise_for_status()

    def send_photo(self, photo_path: str, caption: str = ""):
        """Foto mit optionaler Bildunterschrift senden."""
        with open(photo_path, "rb") as f:
            files = {"photo": f}
            data  = {"chat_id": self.chat_id, "caption": caption}
            r = requests.post(
                f"{self.base}/sendPhoto",
                data=data,
                files=files,
                timeout=20
            )
            r.raise_for_status()
