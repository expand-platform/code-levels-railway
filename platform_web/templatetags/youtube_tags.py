import re
from urllib.parse import parse_qs, urlparse

from django import template

register = template.Library()

_YOUTUBE_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")
_IFRAME_SRC_RE = re.compile(r"src=[\"']([^\"']+)[\"']", re.IGNORECASE)


def _extract_video_id(raw_url: str) -> str:
    if not raw_url:
        return ""

    url = str(raw_url).strip().replace("&amp;", "&")

    iframe_src_match = _IFRAME_SRC_RE.search(url)
    if iframe_src_match:
        url = iframe_src_match.group(1).strip()

    if url.startswith("//"):
        url = f"https:{url}"
    elif url.startswith("www."):
        url = f"https://{url}"
    elif not re.match(r"^https?://", url, flags=re.IGNORECASE):
        url = f"https://{url}"

    url = re.sub(r"^http://", "https://", url, flags=re.IGNORECASE)

    try:
        parsed = urlparse(url)
    except Exception:
        return ""

    host = parsed.netloc.lower().replace("www.", "")

    if host == "youtu.be":
        candidate = parsed.path.strip("/").split("/")[0]
        return candidate if _YOUTUBE_ID_RE.match(candidate) else ""

    if host in {"youtube.com", "m.youtube.com", "music.youtube.com", "youtube-nocookie.com"}:
        query_id = parse_qs(parsed.query).get("v", [""])[0]
        if _YOUTUBE_ID_RE.match(query_id):
            return query_id

        parts = [p for p in parsed.path.split("/") if p]
        for marker in ("embed", "shorts", "live", "v", "e"):
            if marker in parts:
                idx = parts.index(marker)
                if idx + 1 < len(parts) and _YOUTUBE_ID_RE.match(parts[idx + 1]):
                    return parts[idx + 1]

    fallback = re.search(r"([A-Za-z0-9_-]{11})(?:[^A-Za-z0-9_-]|$)", url)
    return fallback.group(1) if fallback else ""


@register.filter
def youtube_embed_url(raw_url):
    video_id = _extract_video_id(raw_url)
    if not video_id:
        return ""
    return f"https://www.youtube.com/embed/{video_id}"
