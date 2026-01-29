import uuid

from django.db import models
from django.utils.text import slugify


class ProgrammingLanguage(models.Model):
    HTML_CSS = "HTML/CSS"
    JAVASCRIPT = "JavaScript"
    PYTHON = "Python"
    PHP = "PHP"
    JAVA = "Java"
    CPP = "C++"
    CSHARP = "C#"
    RUBY = "Ruby"
    GO = "Go"
    SWIFT = "Swift"
    KOTLIN = "Kotlin"
    RUST = "Rust"
    SCALA = "Scala"
    DART = "Dart"
    OBJECTIVE_C = "Objective-C"
    PERL = "Perl"
    HASKELL = "Haskell"
    ELIXIR = "Elixir"
    CLOJURE = "Clojure"
    SHELL = "Shell"

    LANGUAGE_CHOICES = [
        (HTML_CSS, "HTML/CSS"),
        (JAVASCRIPT, "JavaScript"),
        (PYTHON, "Python"),
        (PHP, "PHP"),
        (JAVA, "Java"),
        (CPP, "C++"),
        (CSHARP, "C#"),
        (RUBY, "Ruby"),
        (GO, "Go"),
        (SWIFT, "Swift"),
        (KOTLIN, "Kotlin"),
        (RUST, "Rust"),
        (SCALA, "Scala"),
        (DART, "Dart"),
        (OBJECTIVE_C, "Objective-C"),
        (PERL, "Perl"),
        (HASKELL, "Haskell"),
        (ELIXIR, "Elixir"),
        (CLOJURE, "Clojure"),
        (SHELL, "Shell"),
    ]

    name = models.CharField(max_length=50, choices=LANGUAGE_CHOICES, unique=True)
    slug = models.SlugField(max_length=60, unique=True, blank=True)
    order = models.PositiveIntegerField(
        default=0, help_text="Order for displaying programming languages (lower comes first)"
    )
    
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    
    class Meta:
        db_table = "programming_languages"
        ordering = ["order", "name"]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
