from django import template

register = template.Library()

@register.filter
def is_currently_employed(occupation, company_name):
    return company_name.lower() in occupation.lower()