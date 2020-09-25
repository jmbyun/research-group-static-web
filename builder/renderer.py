from jinja2 import Environment, PackageLoader, select_autoescape

def init_env():
    global env
    env = Environment(
    loader=PackageLoader('builder', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

def render_index(data):
    template = env.get_template('base.html')
    return template.render(data=data)

init_env()
