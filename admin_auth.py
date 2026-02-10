# -*- coding: utf-8 -*-
"""
Проверка JWT для доступа в админку.
Вход по URL: https://домен/<jwt_токен>/admin
Секрет берётся из JWT_SECRET в .env или из переменной окружения.
"""
import os
from typing import Optional

import jwt

# Подгрузка .env из корня проекта (рядом с app.py), чтобы JWT_SECRET работал без export/set
def _load_dotenv() -> None:
    root = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(root, ".env")
    if not os.path.isfile(env_path):
        return
    with open(env_path, "r", encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("export "):
                line = line[7:].strip()
            if "=" in line:
                key, _, value = line.partition("=")
                key = key.strip()
                value = value.strip().strip("'\"").strip()
                if key and key not in os.environ:
                    os.environ[key] = value


_load_dotenv()

# Секрет из переменной окружения или .env
JWT_SECRET = os.environ.get("JWT_SECRET", "change-me-in-production")
JWT_ALGORITHM = "HS256"


def verify_admin_token(token: str) -> bool:
    """
    Проверяет, что переданная строка — валидный JWT с правом админа.
    Токен без срока действия (бессрочный до смены секрета).
    """
    if not token or not token.strip():
        return False
    try:
        payload = jwt.decode(
            token.strip(),
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM],
            options={"verify_exp": False},
        )
        return bool(payload.get("admin"))
    except jwt.InvalidTokenError:
        return False


def create_admin_token() -> str:
    """Генерирует бессрочный токен для админа (для первоначальной настройки)."""
    return jwt.encode(
        {"admin": True},
        JWT_SECRET,
        algorithm=JWT_ALGORITHM,
    )
