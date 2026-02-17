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
        "site_title": "Московское Агентство Недвижимости — Петрозаводск, Карелия, Москва",
        "site_description": "Агентство недвижимости в Петрозаводске, Карелии и Москве. Продажа, покупка, аренда, ипотека. На рынке с 1997 года.",
        "phone": "+7 921 727 5869",
        "email": "ptz.man@yandex.ru",
        "address": "г. Петрозаводск, ул. Ровио, д. 38",
        "schedule": "Пн-Пт: 10:00 – 18:00",
        "hero_badge": "На рынке с 1997 года",
        "hero_title": "Найдём дом вашей",
        "hero_title_highlight": "мечты",
        "hero_lead": "Профессиональное агентство недвижимости в Петрозаводске, Карелии и Москве",
        "hero_cta": "Найти недвижимость",
        "hero_image": "hero_bg.png",
        "about1_image": "about1.png",
        "about2_image": "about2.png",
        "about3_image": "about3.png",
        "about1_caption": "",
        "about2_caption": "",
        "about3_caption": "",
        "gallery1_image": "gallery1.jpg",
        "gallery2_image": "gallery2.jpg",
        "gallery3_image": "gallery3.jpg",
        "gallery4_image": "gallery4.jpg",
        "gallery5_image": "gallery5.jpg",
        "gallery6_image": "gallery6.jpg",
        "gallery1_caption": "Дачные и земельные участки",
        "gallery2_caption": "Квартира под ключ — ремонт",
        "gallery3_caption": "Современный объект",
        "gallery4_caption": "Квартира под ключ — ремонт",
        "gallery5_caption": "Недвижимость за рубежом",
        "gallery6_caption": "Квартиры и дома",
        "gallery1_text": "",
        "gallery2_text": "",
        "gallery3_text": "",
        "gallery4_text": "",
        "gallery5_text": "",
        "gallery6_text": "",
        "stat_deals": "1000+",
        "stat_deals_label": "Успешных сделок",
        "stat_clean": "100%",
        "stat_clean_label": "Юридическая чистота",
        "stat_years": "27",
        "stat_years_label": "Лет на рынке",
        "about_badge": "О Компании",
        "about_title": "Мы знаем, что тепло и уют в Вашем доме – это главное",
        "about_lead": "27 лет помогаем людям находить дом мечты в Петрозаводске, Карелии и Москве",
        "about_p1": "ООО «Московское агентство недвижимости» в Петрозаводске создавалось для того, чтобы люди могли комфортно, с чувством безопасности и защищенности решать свои вопросы, связанные с недвижимостью.",
        "about_p2": "Высокие стандарты качества оказания риэлторских услуг – наша ежедневная насущная забота. Надежная команда профессионалов риэлторского дела накопила опыт трудных побед и ответственных решений.",
        "about_quote": "ПРОФЕССИОНАЛИЗМ И ПОРЯДОЧНОСТЬ – ОСНОВНЫЕ ПРИНЦИПЫ НАШЕЙ РАБОТЫ И СОТРУДНИЧЕСТВА!",
        "leader_name": "Топина Людмила Николаевна",
        "leader_position": "Руководитель агентства",
        "leader_info": "Является действительным членом Союза «Национальная палата недвижимости»",
        "leader_image": "certificate/Ludmila.jpg",
        "leader_cert1_image": "certificate/cert1.jpg",
        "leader_cert2_image": "certificate/cert2.jpg",
        "leader_cert3_image": "certificate/cert3.jpg",
        "leader_cert4_image": "certificate/cert4.jpg",
        "leader_cert5_image": "certificate/cert5.jpg",
        "leader_cert_main_image": "certificate/cert_big.png",
        "services_badge": "Наши Услуги",
        "services_title": "Все сделки с недвижимостью под ключ",
        "services_lead": "Осуществляем полный спектр риэлторских услуг с гарантией юридической чистоты",
        "gallery_badge": "Наша Недвижимость",
        "gallery_title": "Галерея лучших предложений",
        "gallery_lead": "Актуальные объекты недвижимости в Петрозаводске, Карелии, Москве и за рубежом",
        "cta_title": "Не нашли подходящий вариант?",
        "cta_text": "Оставьте заявку, и мы подберём идеальную недвижимость за 24 часа",
        "cta_btn": "Оставить заявку",
        "advantages_badge": "Наши преимущества",
        "advantages_title": "Почему выбирают нас",
        "advantages_lead": "Одно из ведущих агентств на рынке недвижимости Петрозаводска, Карелии и Москвы",
        "contact_badge": "Оставьте Заявку",
        "contact_title": "Получите бесплатную консультацию",
        "contact_lead": "Мы свяжемся с вами в ближайшее время и ответим на все вопросы",
        "congress_title": "Всероссийский Жилищный конгресс",
        "congress_lead": "Масштабное, креативное, легендарное мероприятие на рынке недвижимости России. Выступления топовых спикеров, мощный нетворкинг, обширная деловая и культурная программа",
        "congress_btn": "Регистрация",
        "congress_date": "13–17 апреля 2026",
        "congress_place": "Экспофорум, Санкт-Петербург",
        "congress_url": "https://russiacongress.ru",
        "footer_about": "Работаем на рынке недвижимости с 1997 года. Профессионализм и порядочность – основные принципы нашей работы.",
        "footer_copy": "© 2026 ООО «Московское Агентство Недвижимости». Все права защищены.",
        "news_badge": "Новости",
        "news_title": "Актуальные новости и события",
        "news_lead": "Полезная информация о рынке недвижимости и жизни агентства",
        "news_btn_all": "Все новости",
        "news1_title": "Изменения в ипотечных программах в 2026 году",
        "news1_date": "5 февраля 2026",
        "news1_sort_date": "2026-02-05",
        "news1_excerpt": "Кратко о новых условиях ипотеки и льготных программах.",
        "news1_text": "В 2026 году вступают в силу обновлённые условия по ипотечным программам. Специальные ставки для семей с детьми, программы для новостроек и вторичного рынка. Расскажем, как подобрать выгодный вариант и оформить сделку с нашей помощью.",
        "news2_title": "Как подготовить квартиру к продаже",
        "news2_date": "28 января 2026",
        "news2_sort_date": "2026-01-28",
        "news2_excerpt": "Простые шаги, которые помогут быстрее продать объект.",
        "news2_text": "Подготовка квартиры к продаже влияет на срок реализации и итоговую цену. Рекомендуем провести уборку, мелкий косметический ремонт, правильно расставить мебель и освещение. Наши специалисты бесплатно выезжают на осмотр и дают персональные рекомендации.",
        "news3_title": "Открытие нового офиса в Москве",
        "news3_date": "15 января 2026",
        "news3_sort_date": "2026-01-15",
        "news3_excerpt": "Расширяем присутствие: теперь мы и в столице.",
        "news3_text": "Московское Агентство Недвижимости открыло офис в Москве. Клиенты из Карелии и других регионов могут получать консультации по столичной недвижимости, а москвичи — по объектам в Петрозаводске и Карелии. Ждём вас в наших офисах.",
        "remont_projects_title": "Проекты ремонта",
        "project_remont_1_type": "photo",
        "project_remont_1_image": "",
        "project_remont_1_before_image": "",
        "project_remont_1_after_image": "",
        "project_remont_1_caption": "",
        "project_remont_2_type": "before_after",
        "project_remont_2_image": "",
        "project_remont_2_before_image": "",
        "project_remont_2_after_image": "",
        "project_remont_2_caption": "",
        "project_remont_3_type": "photo",
        "project_remont_3_image": "",
        "project_remont_3_before_image": "",
        "project_remont_3_after_image": "",
        "project_remont_3_caption": "",
        "project_remont_4_type": "photo",
        "project_remont_4_image": "",
        "project_remont_4_before_image": "",
        "project_remont_4_after_image": "",
        "project_remont_4_caption": "",
        "project_remont_5_type": "photo",
        "project_remont_5_image": "",
        "project_remont_5_before_image": "",
        "project_remont_5_after_image": "",
        "project_remont_5_caption": "",
        "project_remont_6_type": "photo",
        "project_remont_6_image": "",
        "project_remont_6_before_image": "",
        "project_remont_6_after_image": "",
        "project_remont_6_caption": "",
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
