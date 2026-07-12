from django.utils.html import strip_tags


class ExcerptService:
    @staticmethod
    def generate_excerpt(content, max_length: int = 200, word_count: int = 30) -> str:
        """Generate a short excerpt from HTML content."""
        if not content:
            return ""

        clean_content = strip_tags(content).strip()
        words = clean_content.split()
        excerpt_words = words[:word_count]
        excerpt = " ".join(excerpt_words)

        if len(excerpt) > max_length:
            excerpt = excerpt[:max_length].rsplit(" ", 1)[0] + "..."
        elif len(words) > word_count:
            excerpt += "..."

        return excerpt
