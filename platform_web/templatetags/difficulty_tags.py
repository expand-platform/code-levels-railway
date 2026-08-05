from django import template

register = template.Library()

DIFFICULTY_LEVELS = {
    "easy": "easy",
    "you can do this": "easy",
    "moderate": "medium",
    "some effort required": "medium",
    "hard": "hard",
    "challenging": "hard",
    "extreme": "insane",
    "hardcore": "insane",
    "for experts only": "insane",
}


@register.filter
def difficulty_level(difficulty):
    if difficulty is None:
        return "unknown"

    name = getattr(difficulty, "name", difficulty)
    if not name:
        return "unknown"

    return DIFFICULTY_LEVELS.get(str(name).strip().lower(), "unknown")
