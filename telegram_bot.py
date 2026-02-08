# -*- coding: utf-8 -*-
"""
Telegram-бот для приёма заявок с лендинга.
Сохраняет chat_id при первом /start, отправляет заявки в этот чат.
Токен захардкожен по запросу.
"""
import json
import os
import threading
import time
from pathlib import Path

import requests

# Токен бота (временно захардкожен)
BOT_TOKEN = "8586225255:AAEJu5nGGr6vA1u3LQUWP2PMrTLcrLMGcSI"
API_URL = "https://api.telegram.org/bot{token}"
CHAT_ID_FILE = Path(__file__).resolve().parent / ".telegram_chat_id"


def _api(method: str, **params) -> dict | None:
    """Вызов метода Telegram Bot API."""
    url = API_URL.format(token=BOT_TOKEN) + "/" + method
    try:
        r = requests.post(url, json=params, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception:
        return None


def get_chat_id() -> int | None:
    """Читает сохранённый chat_id из файла."""
    try:
        if CHAT_ID_FILE.exists():
            data = json.loads(CHAT_ID_FILE.read_text(encoding="utf-8"))
            return data.get("chat_id")
    except Exception:
        pass
    return None


def save_chat_id(chat_id: int) -> None:
    """Сохраняет chat_id в файл."""
    try:
        CHAT_ID_FILE.write_text(json.dumps({"chat_id": chat_id}, ensure_ascii=False), encoding="utf-8")
    except Exception:
        pass


def send_lead(name: str, phone: str, email: str = "", message: str = "") -> bool:
    """
    Отправляет заявку в Telegram. Использует сохранённый chat_id.
    Возвращает True при успехе.
    """
    chat_id = get_chat_id()
    if not chat_id:
        return False

    lines = [
        "🆕 <b>Новая заявка с сайта</b>",
        "",
        f"<b>Имя:</b> {_escape(name)}",
        f"<b>Телефон:</b> {_escape(phone)}",
    ]
    if email:
        lines.append(f"<b>Email:</b> {_escape(email)}")
    if message:
        lines.append(f"<b>Сообщение:</b> {_escape(message)}")

    text = "\n".join(lines)
    out = _api("sendMessage", chat_id=chat_id, text=text, parse_mode="HTML")
    return out is not None and out.get("ok") is True


def _escape(s: str) -> str:
    """Экранирует HTML для Telegram."""
    return (
        str(s)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def _run_polling() -> None:
    """Фоновый цикл: получает обновления, при /start сохраняет chat_id и отвечает."""
    offset = 0
    while True:
        try:
            out = _api("getUpdates", offset=offset, timeout=30)
            if not out or not out.get("ok"):
                time.sleep(2)
                continue
            for upd in out.get("result", []):
                offset = upd["update_id"] + 1
                msg = upd.get("message") or upd.get("edited_message")
                if not msg:
                    continue
                chat_id = msg.get("chat", {}).get("id")
                text = (msg.get("text") or "").strip()
                if not chat_id:
                    continue
                save_chat_id(chat_id)
                if text == "/start":
                    _api("sendMessage", chat_id=chat_id, text="Чат подключён. Сюда будут приходить заявки с сайта.")
        except Exception:
            time.sleep(5)


def start_bot_thread() -> None:
    """Запускает бота в фоновом потоке (поллинг обновлений для сохранения chat_id)."""
    t = threading.Thread(target=_run_polling, daemon=True)
    t.start()
