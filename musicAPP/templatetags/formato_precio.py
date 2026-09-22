from django import template

register = template.Library()


@register.filter
def formato_precio(valor):
    # Presenta cantidades enteras con puntos como separadores de miles.
    if valor is None:
        return ''
    return f'{int(valor):,}'.replace(',', '.')
