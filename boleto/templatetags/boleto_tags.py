import json
from django import template

register = template.Library()

@register.filter
def parse_json(value, key=None):
    if isinstance(value, list):
        value = json.dumps(value)
    try:
        json_value = json.loads(value)
        return json_value.get('retorno')
    except json.JSONDecodeError:
        return None