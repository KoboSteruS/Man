# -*- coding: utf-8 -*-
"""
Flask-приложение лендинга «Московское Агентство Недвижимости».
Раздача страницы, статики и API для заявок (отправка в Telegram-бота).
"""
import time
from collections import defaultdict

from flask import Flask, render_template, request, jsonify

from security import (
    validate_name,
    validate_phone,
    validate_email,
    validate_message,
)
from telegram_bot import send_lead, start_bot_thread

app = Flask(__name__)

# Запуск бота в фоне при старте приложения
start_bot_thread()

# Лимит заявок: макс. 5 с одного IP в минуту (защита от спама)
RATE_LIMIT_COUNT = 5
RATE_LIMIT_WINDOW = 60
_rate_store = defaultdict(list)


def _rate_limit_exceeded(ip: str) -> bool:
    now = time.time()
    times = _rate_store[ip]
    times[:] = [t for t in times if now - t < RATE_LIMIT_WINDOW]
    if len(times) >= RATE_LIMIT_COUNT:
        return True
    times.append(now)
    return False


@app.route("/")
def index():
    """Главная страница лендинга."""
    return render_template("index.html")


@app.route("/api/send-lead", methods=["POST"])
def api_send_lead():
    """
    Принимает заявку с формы и отправляет в Telegram.
    Валидация и санитизация: без HTML, без ссылок, лимит по IP.
    """
    ip = request.remote_addr or "unknown"
    if _rate_limit_exceeded(ip):
        return jsonify({"ok": False, "error": "Слишком много заявок. Попробуйте позже."}), 429

    data = request.get_json(silent=True) or request.form
    if not data:
        return jsonify({"ok": False, "error": "Нет данных"}), 400

    name_raw = (data.get("name") or "").strip()
    phone_raw = (data.get("phone") or "").strip()
    email_raw = (data.get("email") or "").strip()
    message_raw = (data.get("message") or "").strip()

    ok, name = validate_name(name_raw)
    if not ok:
        return jsonify({"ok": False, "error": name}), 400

    ok, phone = validate_phone(phone_raw)
    if not ok:
        return jsonify({"ok": False, "error": phone}), 400

    ok, email = validate_email(email_raw)
    if not ok:
        return jsonify({"ok": False, "error": email}), 400

    ok, message = validate_message(message_raw)
    if not ok:
        return jsonify({"ok": False, "error": message}), 400

    if send_lead(name=name, phone=phone, email=email, message=message):
        return jsonify({"ok": True})
    return jsonify({"ok": False, "error": "Не удалось отправить заявку. Напишите боту в Telegram команду /start."}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
