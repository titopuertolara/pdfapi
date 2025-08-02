from jinja2 import Template
def select_template (employee_name,employee_country,employee_role,today_date_str,start_date_str,language):
    
    if language.lower()=='spanish':
        with open("lang_templates/spanish_template.txt", "r") as file:
            template_str = file.read()
    elif language.lower()=='english':
        with open("lang_templates/english_template.txt", "r") as file:
            template_str = file.read()
    else:
        with open("lang_templates/english_template.txt", "r") as file:
            template_str = file.read()
    
    template = Template(template_str)
    
    letter = template.render(
        employee_name=employee_name,
        employee_country=employee_country,
        employee_role=employee_role,
        start_date_str=start_date_str,
        today_date_str=today_date_str
    )
                        
    return letter