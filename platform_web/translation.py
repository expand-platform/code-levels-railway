from modeltranslation.translator import translator, TranslationOptions
from platform_web.models.base.website_config import WebsiteConfig


class WebsiteConfigTranslationOptions(TranslationOptions):
    fields = ("tagline",)


translator.register(WebsiteConfig, WebsiteConfigTranslationOptions)
