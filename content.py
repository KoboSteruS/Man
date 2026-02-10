# -*- coding: utf-8 -*-
"""
Загрузка и сохранение контента лендинга (JSON).
Используется главной страницей и админкой.
"""
import json
import os
from pathlib import Path
from typing import Any, Dict

# Путь к файлу контента (рядом с app.py)
DATA_DIR = Path(__file__).resolve().parent / "data"
CONTENT_FILE = DATA_DIR / "site_content.json"


def _default_content() -> Dict[str, Any]:
    """Контент по умолчанию (текущие тексты с лендинга)."""
    return {
        "site_title": "Московское Агентство Недвижимости — Петрозаводск, Карелия",
        "site_description": "Агентство недвижимости в Петрозаводске и Республике Карелия. Продажа, покупка, аренда, ипотека. На рынке с 1997 года.",
        "phone": "+7 (900) 455-10-10",
        "email": "ptz.man@yandex.ru",
        "address": "г. Петрозаводск, ул. Ровио, д. 38",
        "schedule": "Пн-Пт: 10:00 – 18:00",
        "hero_badge": "На рынке с 1997 года",
        "hero_title": "Найдём дом вашей",
        "hero_title_highlight": "мечты",
        "hero_lead": "Профессиональное агентство недвижимости в Петрозаводске и Республике Карелия",
        "hero_cta": "Найти недвижимость",
        "stat_deals": "1000+",
        "stat_deals_label": "Успешных сделок",
        "stat_clean": "100%",
        "stat_clean_label": "Юридическая чистота",
        "stat_years": "27",
        "stat_years_label": "Лет на рынке",
        "about_badge": "О Компании",
        "about_title": "Мы знаем, что тепло и уют в Вашем доме – это главное",
        "about_lead": "27 лет помогаем людям находить дом мечты в Петрозаводске и Республике Карелия",
        "about_p1": "ООО «Московское агентство недвижимости» в Петрозаводске создавалось для того, чтобы люди могли комфортно, с чувством безопасности и защищенности решать свои вопросы, связанные с недвижимостью.",
        "about_p2": "Высокие стандарты качества оказания риэлторских услуг – наша ежедневная насущная забота. Надежная команда профессионалов риэлторского дела накопила опыт трудных побед и ответственных решений.",
        "about_quote": "ПРОФЕССИОНАЛИЗМ И ПОРЯДОЧНОСТЬ – ОСНОВНЫЕ ПРИНЦИПЫ НАШЕЙ РАБОТЫ И СОТРУДНИЧЕСТВА!",
        "services_badge": "Наши Услуги",
        "services_title": "Все сделки с недвижимостью под ключ",
        "services_lead": "Осуществляем полный спектр риэлторских услуг с гарантией юридической чистоты",
        "gallery_badge": "Наша Недвижимость",
        "gallery_title": "Галерея лучших предложений",
        "gallery_lead": "Актуальные объекты недвижимости в Карелии и за рубежом",
        "cta_title": "Не нашли подходящий вариант?",
        "cta_text": "Оставьте заявку, и мы подберём идеальную недвижимость за 24 часа",
        "cta_btn": "Оставить заявку",
        "advantages_badge": "Наши преимущества",
        "advantages_title": "Почему выбирают нас",
        "advantages_lead": "Одно из ведущих агентств на рынке недвижимости Петрозаводска и Республики Карелия",
        "contact_badge": "Оставьте Заявку",
        "contact_title": "Получите бесплатную консультацию",
        "contact_lead": "Мы свяжемся с вами в ближайшее время и ответим на все вопросы",
        "partner_title": "Официальный партнёр",
        "partner_text": "С 2012 года агентство является первым и единственным в Республике Карелия официальным партнёром и аккредитованным представителем «Дрийм Хоум» ЕООД (Болгария).",
        "footer_about": "Работаем на рынке недвижимости с 1997 года. Профессионализм и порядочность – основные принципы нашей работы.",
        "footer_copy": "© 2026 ООО «Московское Агентство Недвижимости». Все права защищены.",
    }


def load_content() -> Dict[str, Any]:
    """Загружает контент: из файла с подмешиванием дефолтов."""
    defaults = _default_content()
    if not CONTENT_FILE.exists():
        return defaults
    try:
        with open(CONTENT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            return {**defaults, **data}
        return defaults
    except (json.JSONDecodeError, OSError):
        return defaults


def get_default_keys() -> set:
    """Множество ключей, разрешённых для сохранения (защита от произвольных полей)."""
    return set(_default_content().keys())


def save_content(data: Dict[str, Any]) -> bool:
    """Сохраняет контент в JSON. Возвращает True при успехе."""
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        with open(CONTENT_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except OSError:
        return False
