def get_playbook(playbook_name):
    with open('../utils/renewal.jinja', 'r') as file:
        template_content = file.read()
    return template_content