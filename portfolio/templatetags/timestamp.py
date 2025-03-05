from django import template

register = template.Library()


@register.filter("timestamp")
def convert_timestamp_to_time(timestamp):
    """
    Converts a timestamp to a datetime.
    """
    from datetime import datetime

    if timestamp == "":
        return datetime.now()
    return datetime.fromtimestamp(int(timestamp))
