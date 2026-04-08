from html.parser import HTMLParser

from django import template

register = template.Library()


class _LiTextExtractor(HTMLParser):
    """Extracts plain text content from <li> elements."""

    def __init__(self):
        super().__init__()
        self._in_li = False
        self._current: list[str] = []
        self.items: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag == "li":
            self._in_li = True
            self._current = []

    def handle_endtag(self, tag):
        if tag == "li" and self._in_li:
            text = "".join(self._current).strip()
            if text:
                self.items.append(text)
            self._in_li = False

    def handle_data(self, data):
        if self._in_li:
            self._current.append(data)


@register.filter
def li_items(html_value):
    """Returns a list of plain-text strings extracted from <li> tags in an HTML string."""
    if not html_value:
        return []
    parser = _LiTextExtractor()
    parser.feed(str(html_value))
    return parser.items
