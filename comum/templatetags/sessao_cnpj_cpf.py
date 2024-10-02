# comum/templatetags/sessao_cnpj_cpf.py

from django import template
from django.template.loader import get_template

register = template.Library()

@register.simple_tag
def verifica_sessao_cnpj_cpf(request):
    if request.session.get('cnpj_cpf'):
        return True
    else:
        return False