# -*- coding: utf-8 -*-
"""
Загрузка изображений в админке: Hero, О нас, Галерея.
Сохраняем в static/img/<dir>/ с фиксированными именами, обновляем content.
"""
import os
from pathlib import Path
from typing import Optional, Tuple

# Слот -> (подпапка в static/img, базовое имя файла)
UPLOAD_SLOTS = {
    "hero_bg": ("hero", "hero_bg"),
    "about1": ("about", "about1"),
    "about2": ("about", "about2"),
    "about3": ("about", "about3"),
    "gallery1": ("gallery", "gallery1"),
    "gallery2": ("gallery", "gallery2"),
    "gallery3": ("gallery", "gallery3"),
    "gallery4": ("gallery", "gallery4"),
    "gallery5": ("gallery", "gallery5"),
    "gallery6": ("gallery", "gallery6"),
}

# Ключ в content для имени файла (hero_bg -> hero_image, about1 -> about1_image, ...)
def get_content_key(slot: str) -> str:
    if slot == "hero_bg":
        return "hero_image"
    return f"{slot}_image"


ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}
MAX_SIZE_MB = 5


def save_uploaded_image(
    slot: str,
    file_storage,
    static_root: Path,
) -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Сохраняет загруженный файл в static/img/<dir>/<base>.<ext> и возвращает
    (ok, filename_for_content, error_message).
    """
    if slot not in UPLOAD_SLOTS:
        return False, None, "Неверный слот"
    if not file_storage or not file_storage.filename:
        return False, None, "Файл не выбран"

    subdir, base = UPLOAD_SLOTS[slot]
    ext = Path(file_storage.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        return False, None, "Разрешены только JPG и PNG"

    file_storage.stream.seek(0, os.SEEK_END)
    size = file_storage.stream.tell()
    file_storage.stream.seek(0)
    if size > MAX_SIZE_MB * 1024 * 1024:
        return False, None, f"Размер не более {MAX_SIZE_MB} МБ"

    # Нормализуем расширение для content: .jpeg -> .jpg
    if ext == ".jpeg":
        ext = ".jpg"
    filename = base + ext
    dest_dir = static_root / "img" / subdir
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_path = dest_dir / filename

    try:
        file_storage.save(str(dest_path))
    except OSError:
        return False, None, "Ошибка записи файла"

    return True, filename, None
