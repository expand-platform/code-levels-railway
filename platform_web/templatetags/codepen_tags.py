from django import template

register = template.Library()

@register.filter
def codepen_parts(url):
    """
    Extracts the username and hash from a CodePen URL of the form:
    https://codepen.io/{username}/pen/{hash}
    Returns a tuple (username, hash)
    """
    if not url or '/pen/' not in url or 'codepen.io/' not in url:
        return ('', '')
    try:
        parts = url.split('codepen.io/')[1].split('/pen/')
        username = parts[0].strip('/').split('/')[0]
        hash = parts[1].split('/')[0]
        return (username, hash)
    except Exception:
        return ('', '')

@register.filter
def codepen_username(url):
    return codepen_parts(url)[0]

@register.filter
def codepen_hash(url):
    return codepen_parts(url)[1]
