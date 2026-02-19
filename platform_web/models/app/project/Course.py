import uuid

from django.db import models
from platform_web.models.app.project.ProgrammingLanguage import ProgrammingLanguage


class Course(models.Model):
    # project-based learning
    WEB_DEVELOPMENT = "Web Development"
    DESKTOP_APPS = "Desktop Applications"
    TELEGRAM_BOTS = "Telegram Bots"
    MOBILE_APPS = "Mobile Applications"
    DATA_SCIENCE = "Data Science"
    SECURITY = "Security"

    # language-based
    HTML_CSS = "HTML & CSS"
    JS_BASICS = "JavaScript Basics"
    ADVANCED_JS = "Advanced JavaScript"

    # framework-specific
    REACT = "React for Beginners"
    VUE = "Vue.js Crash Course"
    DJANGO = "Django Essentials"
    FASTAPI = "APIs with FastAPI"

    # basics for specific technologies
    PYTHON_WEB = "Python for Web Development"
    SQL = "Database Design & SQL"
    TESTING = "Testing & Debugging"
    DEVOPS = "Deployment & DevOps"
    GIT = "Version Control with Git"
    UIUX = "UI/UX Design Principles"
    NODE = "Backend Development with Node.js"
    FULLSTACK = "Full Stack Web Development"

    COURSE_CHOICES = [
        # project-based learning
        (WEB_DEVELOPMENT, "Web Development"),
        (DESKTOP_APPS, "Desktop Applications"),
        (MOBILE_APPS, "Mobile Applications"),
        (TELEGRAM_BOTS, "Telegram Bots"),
        (DATA_SCIENCE, "Data Science"),
        (SECURITY, "Security"),
        
        # language-based
        (HTML_CSS, "HTML & CSS Fundamentals"),
        (JS_BASICS, "JavaScript Basics"),
        (ADVANCED_JS, "Advanced JavaScript"),
        
        # framework-specific
        (VUE, "Vue.js Crash Course"),
        (REACT, "React for Beginners"),
        (FASTAPI, "APIs with FastAPI"),
        (DJANGO, "Django Essentials"),
        
        # basics for specific technologies
        (PYTHON_WEB, "Python for Web Development"),
        (SQL, "Database Design & SQL"),
        (TESTING, "Testing & Debugging"),
        (DEVOPS, "Deployment & DevOps"),
        (GIT, "Version Control with Git"),
        (UIUX, "UI/UX Design Principles"),
        (NODE, "Backend Development with Node.js"),
        (FULLSTACK, "Full Stack Web Development"),
    ]

    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    languages = models.ManyToManyField(
        ProgrammingLanguage, related_name="courses", blank=True
    )
    order = models.PositiveIntegerField(default=0)
    
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    class Meta:
        db_table = "courses"
        ordering = ["order", "title"]

    def __str__(self):
        return self.title
