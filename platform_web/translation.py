from modeltranslation.translator import translator, TranslationOptions
from platform_web.models.app.project.Difficulty import Difficulty
from platform_web.models.base.website_config import WebsiteConfig
from platform_web.models.app.project.Course import Course


class WebsiteConfigTranslationOptions(TranslationOptions):
    fields = ("tagline",)


class CourseTranslationOptions(TranslationOptions):
    fields = ("title",)

class DifficultyTranslationOptions(TranslationOptions):
    fields = ("name",)


translator.register(WebsiteConfig, WebsiteConfigTranslationOptions)
translator.register(Course, CourseTranslationOptions)
translator.register(Difficulty, DifficultyTranslationOptions)
