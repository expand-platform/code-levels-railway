from django.utils.translation import gettext_lazy as _


class ProjectType:
    TOPIC = "topic"
    PROJECT = "project"
    WORKOUT = "workout"


class ProjectConfig:
    MAX_SEARCH_LENGTH = 100
    PROJECTS_LAYOUT_QUERY = "view"
    PROJECTS_LAYOUT_DEFAULT = "default"
    PROJECTS_LAYOUT_ROADMAP = "roadmap"
    ROADMAP_LAYOUT_LIST = "list"
    LAYOUT_PROJECTS = "projects"
    LAYOUT_ROADMAP = "roadmap"
    LAYOUT_NONE = ""

    MODE_SETTINGS = {
        "projects": {
            "filter_by": "course",
            "project_type": ProjectType.PROJECT,
            "is_video_course": "false",
        },
        "topics": {
            "filter_by": "language",
            "project_type": ProjectType.TOPIC,
            "is_video_course": "false",
        },
        "courses": {
            "filter_by": "course",
            "project_type": ProjectType.PROJECT,
            "is_video_course": "true",
        },
    }

    ROADMAP_LAYOUTS = frozenset({PROJECTS_LAYOUT_ROADMAP, ROADMAP_LAYOUT_LIST})

    @classmethod
    def mode(cls, page_mode):
        return cls.MODE_SETTINGS.get(page_mode, cls.MODE_SETTINGS["projects"])

    @classmethod
    def search_query(cls, params) -> str:
        return params.get("search", "").strip()[: cls.MAX_SEARCH_LENGTH]

    @classmethod
    def requested_layout(cls, params) -> str:
        return params.get(cls.PROJECTS_LAYOUT_QUERY, "")

    @classmethod
    def roadmap_layout(cls, params) -> str:
        layout = params.get(cls.PROJECTS_LAYOUT_QUERY, cls.PROJECTS_LAYOUT_ROADMAP)
        if layout not in cls.ROADMAP_LAYOUTS:
            return cls.PROJECTS_LAYOUT_ROADMAP
        return layout

    @classmethod
    def view_query(cls, layout: str, *, default: str) -> str:
        if not layout or layout == default:
            return ""
        return f"?{cls.PROJECTS_LAYOUT_QUERY}={layout}"

    @classmethod
    def layout_toggle(cls, kind, current):
        if kind == cls.LAYOUT_PROJECTS:
            group_label = _("Projects layout")
            choices = (
                (cls.PROJECTS_LAYOUT_DEFAULT, _("List")),
                (cls.PROJECTS_LAYOUT_ROADMAP, _("Roadmap")),
            )
        elif kind == cls.LAYOUT_ROADMAP:
            group_label = _("Roadmap layout")
            choices = (
                (cls.PROJECTS_LAYOUT_ROADMAP, _("Roadmap")),
                (cls.ROADMAP_LAYOUT_LIST, _("List")),
            )
        else:
            return None
        return {
            "label": group_label,
            "options": [
                {
                    "value": value,
                    "label": label,
                    "checked": value == current,
                }
                for value, label in choices
            ],
        }
