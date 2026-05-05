from typing import Any

from platform_web.services.model.SeoService import SeoService
from platform_web.services.model.SlugService import SlugService


class SeoSlugMixin:
    title: Any
    slug: Any
    seo_title: Any
    seo_description: Any
    pk: Any

    def save(self, *args, **kwargs):
        if not self.pk:
            self._fill_seo()

        if not self.slug and self.title:
            self.slug = SlugService.generate_unique_slug(
                self.title,
                self.__class__,
                exclude_pk=self.pk,
                fallback_prefix=self.__class__.__name__.lower(),
            )
        super().save(*args, **kwargs)

    def _fill_seo(self):
        if not self.seo_title:
            self.seo_title = SeoService.generate_initial_seo_title(self.title)
        if not self.seo_description:
            self.seo_description = SeoService.generate_initial_seo_description(
                self.title
            )
