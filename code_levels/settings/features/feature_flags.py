from dataclasses import dataclass

DASHBOARD = "user_dashboard"
COURSES = "courses"


@dataclass(frozen=True)
class FeatureFlag:
    enabled: bool

    def is_enabled(self) -> bool:
        return self.enabled


USER_DASHBOARD = FeatureFlag(False)
COURSES_AVAILABLE = FeatureFlag(True)
