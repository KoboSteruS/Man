#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для генерации JWT-токена доступа в админку.
Запуск: положите JWT_SECRET в файл .env в корне проекта или задайте в окружении, затем:
  python make_admin_token.py
"""
import os
import sys

_script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _script_dir)

# Явно грузим .env из папки скрипта до импорта admin_auth (иначе на части машин секрет не подхватывается)
_env_path = os.path.join(_script_dir, ".env")
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
                if _k:
                    os.environ[_k] = _v

from admin_auth import JWT_SECRET, create_admin_token


def main() -> None:
    if JWT_SECRET == "change-me-in-production":
        print("JWT_SECRET не задан — используем секрет для разработки (change-me-in-production).")
        print("В production задайте в .env: JWT_SECRET=ваша-длинная-случайная-строка")
        print()
    token = create_admin_token()
    print("Токен для входа в админку (подставьте в URL вместо <токен>):")
    print()
    print(token)
    print()
    print("Ссылка для входа: https://ваш-домен-или-ip/" + token + "/admin")


if __name__ == "__main__":
    main()
