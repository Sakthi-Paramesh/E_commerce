from django import template

register = template.Library()


@register.filter(name='star_range')
def star_range(rating):
    """Returns a list of (index, filled) tuples for rendering 5 stars."""
    try:
        r = int(round(float(rating)))
    except (TypeError, ValueError):
        r = 0
    return [(i, i <= r) for i in range(1, 6)]


@register.filter(name='to_int')
def to_int(value):
    try:
        return int(round(float(value)))
    except (TypeError, ValueError):
        return 0


@register.simple_tag
def rating_stars(rating):
    try:
        r = int(round(float(rating)))
    except (TypeError, ValueError):
        r = 0
    filled = '<i class="bi bi-star-fill"></i>' * r
    empty = '<i class="bi bi-star"></i>' * (5 - r)
    return filled + empty
