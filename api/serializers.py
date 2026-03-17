from rest_framework import serializers
from platform_web.models.app.project.Project import Project
from platform_web.models.app.project.ProgrammingLanguage import ProgrammingLanguage
from platform_web.models.app.project.Lesson import Lesson
from platform_web.models.app.project.Framework import Framework
from platform_web.models.app.project.Difficulty import Difficulty
from platform_web.models.app.project.Course import Course
from platform_web.models.app.user.Certificate import Certificate
from platform_web.models.base.website_config import WebsiteConfig
from platform_web.models.base.social_media_link import SocialMediaLink

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class ProgrammingLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgrammingLanguage
        fields = '__all__'

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'

class FrameworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Framework
        fields = '__all__'

class DifficultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Difficulty
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = '__all__'

class WebsiteConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebsiteConfig
        fields = '__all__'

class SocialMediaLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaLink
        fields = '__all__'
