# Московское Агентство Недвижимости — лендинг

Flask-лендинг по макету из папки `Design/`. Реализован на HTML, CSS и JavaScript без фреймворков; статика и шаблон отдаются через Flask.

## Структура проекта

```
MoskowLending/
├── app.py                 # Точка входа Flask
├── requirements.txt
├── README.md
├── Design/                # Исходный макет (React/Vite)
├── templates/
│   └── index.html         # Единственная страница лендинга
└── static/
    ├── css/
    │   └── style.css      # Стили (токены, секции, компоненты)
    └── js/
        └── main.js       # Хедер при скролле, карусель галереи, лайки, форма, тост
```

## Установка и запуск

1. Создать виртуальное окружение (рекомендуется):

   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # Windows
   # source .venv/bin/activate  # Linux/macOS
   ```

2. Установить зависимости:

   ```bash
   pip install -r requirements.txt
   ```

3. Запустить приложение:

   ```bash
   python app.py
   ```

4. Открыть в браузере: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

## Секции лендинга

- **Header** — фиксированный, при скролле фон и стиль ссылок меняются
- **Hero** — полноэкранный блок с фоном, заголовком, CTA и блоками статистики
- **О компании** — текст, коллаж фото, карточки преимуществ, цитата
- **Услуги** — сетка услуг и карусель банков-партнёров (CSS-анимация)
- **Галерея недвижимости** — карусель из 6 карточек (по 3 в кадре), лайки сохраняются в `localStorage`
- **Преимущества** — сетка карточек и блок с цитатой
- **Контакты** — карточки контактов, форма заявки, партнёрский блок, карта
- **Footer** — градиентный фон, ссылки, контакты, копирайт

## Переменные окружения

Не требуются. Для продакшена можно задать:

- `FLASK_ENV=production`
- При необходимости использовать прокси (Nginx/Apache) для раздачи статики.

## Технические детали

- Стили: один файл `style.css` с CSS-переменными (токены из макета), без Tailwind
- Иконки: inline SVG в разметке
- Логотип: текст «МАН» (в макете использовалась ссылка на Figma-asset)
- Картинки: Unsplash по URL из макета; карта — iframe Google Maps
- Форма: отправка без бэкенда, показ тоста «Спасибо! Мы свяжемся с вами»

## Git-коммиты (рекомендуемые)

```
feat(flask): add Flask app and landing page structure
feat(templates): add index.html with all sections from Design
feat(css): add style.css with tokens, layout and components
feat(js): add main.js for header, gallery carousel, likes, form toast
docs: add README with setup and run instructions
```
