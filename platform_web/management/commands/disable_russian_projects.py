import re

from django.core.management.base import BaseCommand

from platform_web.models.project.Project import Project


class Command(BaseCommand):
    help = "Disable active projects whose titles match a Russian/Cyrillic regex pattern"

    def add_arguments(self, parser):
        parser.add_argument(
            "--pattern",
            default=r"[\u0400-\u04FF]",
            help=(
                "Regex used for title matching. Defaults to any Cyrillic character: "
                "[\\u0400-\\u04FF]"
            ),
        )
        parser.add_argument(
            "--apply",
            action="store_true",
            help="Apply changes. Without this flag, command runs in dry-run mode.",
        )
        parser.add_argument(
            "--limit",
            type=int,
            default=20,
            help="How many matched titles to print as preview (default: 20).",
        )

    def handle(self, *args, **options):
        pattern = options["pattern"]
        apply_changes = options["apply"]
        limit = options["limit"]

        try:
            re.compile(pattern)
        except re.error as exc:
            self.stderr.write(self.style.ERROR(f"Invalid regex pattern: {exc}"))
            return

        queryset = Project.objects.filter(is_active=True, title__regex=pattern)
        matched_count = queryset.count()

        self.stdout.write(f"Regex pattern: {pattern}")
        self.stdout.write(f"Matched active projects: {matched_count}")

        preview_titles = list(queryset.values_list("title", flat=True)[:limit])
        if preview_titles:
            self.stdout.write("Matched title preview:")
            for title in preview_titles:
                self.stdout.write(f" - {title}")

        if not apply_changes:
            self.stdout.write(
                self.style.WARNING(
                    "Dry-run mode. Re-run with --apply to disable matched projects."
                )
            )
            return

        updated_count = queryset.update(is_active=False)
        self.stdout.write(
            self.style.SUCCESS(f"Disabled projects: {updated_count}")
        )