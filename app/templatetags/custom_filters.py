from django import template

register = template.Library()

@register.filter
def is_currently_employed(occupation, company_names):
    # Split the company names by comma and strip whitespace from each name
    try:
        company_names_list = [name.strip() for name in company_names.split(',')]
        # Check if any of the company names exists in the occupation
        for company_name in company_names_list:
            if company_name.lower() in occupation.lower():
                return "Employed"  # Return "Employed" if any company name is found in the occupation
        return "Not Employed"
    except:
        return "Not confirmed"