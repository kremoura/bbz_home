from django import template

register = template.Library()

@register.filter
def formatar_cpf_cnpj(cpf_cnpj):
    if len(cpf_cnpj) == 11:  # CPF
        return "{}.{}.{}-{}".format(cpf_cnpj[:3], cpf_cnpj[3:6], cpf_cnpj[6:9], cpf_cnpj[9:])
    elif len(cpf_cnpj) == 14:  # CNPJ
        return "{}.{}.{}/{}-{}".format(cpf_cnpj[:2], cpf_cnpj[2:5], cpf_cnpj[5:8], cpf_cnpj[8:12], cpf_cnpj[12:])
    else:
        return "Formato inválido"