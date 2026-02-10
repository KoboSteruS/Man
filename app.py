# -*- coding: utf-8 -*-
"""
Flask-приложение лендинга «Московское Агентство Недвижимости».
Раздача страницы, статики, API заявок, админка по JWT.
"""
import os
import time
from collections import defaultdict

# Подгружаем .env до импорта admin_auth (utf-8-sig убирает BOM на Windows)
_app_root = os.path.dirname(os.path.abspath(__file__))
_env_path = os.path.join(_app_root, ".env")
if os.path.isfile(_env_path):
    with open(_env_path, "r", encoding="utf-8-sig") as _f:
        for _line in _f:
            _line = _line.strip()
            if not _line or _line.startswith("#"):
                continue
            if _line.startswith("export "):
                _line = _line[7:].strip()
            if "=" in _line:
                _k, _, _v = _line.partition("=")
                _k, _v = _k.strip(), _v.strip().strip("'\"").strip()
                if _k and _k not in os.environ:
                    os.environ[_k] = _v

from flask import Flask, render_template, request, jsonify

from admin_auth import verify_admin_token, JWT_SECRET
from content import get_default_keys, load_content, save_content
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

# При старте: показываем, откуда взят секрет для админ-токена (без самого секрета)
if JWT_SECRET == "change-me-in-production":
    print("[Admin JWT] Используется дефолтный секрет. Задай JWT_SECRET в .env для своей ссылки.")
else:
    print("[Admin JWT] Секрет загружен из .env. Токен генерируй командой: python make_admin_token.py")

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
    content = load_content()
    return render_template("index.html", content=content)


@app.route("/<token>/admin", methods=["GET"])
def admin_page(token: str):
    """Админка: доступ только при валидном JWT в пути (домен/<jwt>/admin)."""
    if not verify_admin_token(token):
        return jsonify({"error": "Неверный или просроченный токен"}), 403
    content = load_content()
    return render_template("admin.html", content=content, admin_token=token)


@app.route("/<token>/admin/save", methods=["POST"])
def admin_save(token: str):
    """Сохранение контента из админки."""
    if not verify_admin_token(token):
        return jsonify({"ok": False, "error": "Неверный или просроченный токен"}), 403
    data = request.get_json(silent=True)
    if not data or not isinstance(data, dict):
        return jsonify({"ok": False, "error": "Нет данных"}), 400
    allowed_keys = get_default_keys()
    cleaned = {k: str(v).strip() if v is not None else "" for k, v in data.items() if k in allowed_keys}
    if save_content(cleaned):
        return jsonify({"ok": True})
    return jsonify({"ok": False, "error": "Не удалось сохранить"}), 500


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
