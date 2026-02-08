# -*- coding: utf-8 -*-
"""
Flask-приложение лендинга «Московское Агентство Недвижимости».
Раздача страницы, статики и API для заявок (отправка в Telegram-бота).
"""
from flask import Flask, render_template, request, jsonify

from telegram_bot import send_lead, start_bot_thread

app = Flask(__name__)

# Запуск бота в фоне при старте приложения
start_bot_thread()


@app.route("/")
def index():
    """Главная страница лендинга."""
    return render_template("index.html")


@app.route("/api/send-lead", methods=["POST"])
def api_send_lead():
    """
    Принимает заявку с формы и отправляет в Telegram.
    Тело: JSON { "name", "phone", "email?", "message?" } или form-data.
    """
    data = request.get_json(silent=True) or request.form
    if not data:
        return jsonify({"ok": False, "error": "Нет данных"}), 400

    name = (data.get("name") or "").strip()
    phone = (data.get("phone") or "").strip()
    email = (data.get("email") or "").strip()
    message = (data.get("message") or "").strip()

    if not name or not phone:
        return jsonify({"ok": False, "error": "Укажите имя и телефон"}), 400

    if send_lead(name=name, phone=phone, email=email, message=message):
        return jsonify({"ok": True})
    return jsonify({"ok": False, "error": "Не удалось отправить заявку. Напишите боту в Telegram команду /start."}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
