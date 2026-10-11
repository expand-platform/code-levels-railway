import os
import uuid

from django.utils.text import slugify


class ImageUploadService:
    @staticmethod
    def unique_path(filename: str, folder: str, fallback: str) -> str:
        base, ext = os.path.splitext(os.path.basename(filename))
        stem = slugify(base)[:60] or fallback
        tail = uuid.uuid4().hex[:8]
        return f"{folder}/{stem}-{tail}{ext.lower()}"
