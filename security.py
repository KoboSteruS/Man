# -*- coding: utf-8 -*-
"""
Валидация и санитизация данных заявок.
Защита от спама, ссылок, HTML/JS-инъекций.
"""
import re
from typing import Tuple

# Лимиты длины
MAX_NAME_LEN = 100
MAX_PHONE_LEN = 30
MAX_EMAIL_LEN = 254
MAX_MESSAGE_LEN = 2000

# Регулярки
RE_HTML_TAG = re.compile(r"<[^>]+>", re.IGNORECASE)
RE_SCRIPT = re.compile(r"<script\b[^>]*>.*?</script>", re.IGNORECASE | re.DOTALL)
RE_URL = re.compile(
    r"https?://[^\s<>]+|www\.[^\s<>]+|\[?https?://[^\]]+\]?",
    re.IGNORECASE
)
RE_DANGEROUS = re.compile(r"[<>\"'`{}\\]|javascript:|data:|vbscript:", re.IGNORECASE)
# Телефон: только цифры, +, скобки, пробелы, дефис
RE_PHONE_ALLOWED = re.compile(r"^[\d+\s()\-]+$")
RE_EMAIL_BASIC = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
# Управляющие символы
RE_CONTROL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")


def _strip_html(text: str) -> str:
    """Удаляет HTML-теги и содержимое script."""
    if not text:
        return ""
    s = RE_SCRIPT.sub("", text)
    s = RE_HTML_TAG.sub("", s)
    return s


def _strip_links(text: str) -> str:
    """Заменяет ссылки на плейсхолдер."""
    if not text:
        return ""
    return RE_URL.sub("[ссылка удалена]", text)


def _strip_control(text: str) -> str:
    """Удаляет управляющие символы."""
    if not text:
        return ""
    return RE_CONTROL.sub("", text)


def sanitize_plain(text: str, max_length: int) -> str:
    """
    Санитизация произвольного текста: без HTML, без ссылок, без опасных символов.
    """
    if text is None:
        return ""
    s = str(text)
    if not s.strip():
        return ""
    s = _strip_html(s)
    s = _strip_links(s)
    s = RE_DANGEROUS.sub("", s)
    s = _strip_control(s)
    s = " ".join(s.split())
    return s[:max_length].strip()


def validate_name(value: str) -> Tuple[bool, str]:
    """
    Валидация имени. Возвращает (ok, cleaned) или (False, error_message).
    """
    s = (value or "").strip()
    if len(s) < 2:
        return False, "Имя слишком короткое"
    cleaned = sanitize_plain(s, MAX_NAME_LEN)
    if len(cleaned) < 2:
        return False, "Укажите корректное имя"
    return True, cleaned


def validate_phone(value: str) -> Tuple[bool, str]:
    """
    Валидация телефона. Только цифры, +, скобки, пробелы, дефис.
    """
    s = (value or "").strip()
    if not s:
        return False, "Укажите телефон"
    if len(s) > MAX_PHONE_LEN:
        return False, "Телефон слишком длинный"
    if not RE_PHONE_ALLOWED.match(s):
        return False, "Телефон может содержать только цифры, +, скобки и дефис"
    digits = re.sub(r"\D", "", s)
    if len(digits) < 10:
        return False, "Слишком мало цифр в номере"
    return True, s


def validate_email(value: str) -> Tuple[bool, str]:
    """Валидация email. Пустое значение допустимо (поле необязательное)."""
    s = (value or "").strip()
    if not s:
        return True, ""
    if len(s) > MAX_EMAIL_LEN:
        return False, "Email слишком длинный"
    if "<" in s or ">" in s or " " in s or "\n" in s:
        return False, "Некорректный email"
    if not RE_EMAIL_BASIC.match(s):
        return False, "Некорректный формат email"
    return True, s


def validate_message(value: str) -> Tuple[bool, str]:
    """Валидация сообщения. Пустое допустимо. Ссылки и HTML удаляются."""
    s = (value or "").strip()
    if not s:
        return True, ""
    cleaned = sanitize_plain(s, MAX_MESSAGE_LEN)
    return True, cleaned
