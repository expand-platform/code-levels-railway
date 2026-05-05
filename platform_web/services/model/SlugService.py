from django.utils.text import slugify
from platform_web.data.transliteration import transliterate_ru_to_latin

import uuid


class SlugService:
    @staticmethod
    def generate_unique_slug(title: str, model_class, exclude_pk=None, fallback_prefix: str = "item") -> str:
        transliterated = transliterate_ru_to_latin(str(title))
        base_slug = slugify(transliterated) or slugify(str(title))

        if not base_slug:
            base_slug = f"{fallback_prefix}-{str(uuid.uuid4())[:8]}"

        slug = base_slug
        counter = 1
        qs = model_class.objects.filter(slug=slug)
        if exclude_pk is not None:
            qs = qs.exclude(pk=exclude_pk)

        while qs.exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
            qs = model_class.objects.filter(slug=slug)
            if exclude_pk is not None:
                qs = qs.exclude(pk=exclude_pk)

        return slug
