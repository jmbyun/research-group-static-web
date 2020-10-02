import json
import markdown
import urllib.parse
from datetime import datetime
from jinja2 import Environment, PackageLoader, Markup, select_autoescape

def init_env():
    global env
    env = Environment(
        loader=PackageLoader('builder', 'templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    md = markdown.Markdown(extensions=['meta'])
    env.filters['markdown'] = lambda text: Markup(md.convert(text))
    env.filters['jsonify'] = lambda text: json.dumps(text)

def render_index(data):
    template = env.get_template('landing.html')
    max_size = 7
    landing_research = data['research'][0]['rows'][:]
    if len(landing_research) > max_size:
        landing_research = landing_research[:max_size]
    return template.render(data=data, landing_research=landing_research)

def render_members(data):
    template = env.get_template('members.html')
    return template.render(data=data)

def render_research(data):
    template = env.get_template('research.html')
    return template.render(data=data)

def render_links(data):
    template = env.get_template('links.html')
    today = datetime.today()
    for group in data['links']:
        for link in group['rows']:
            if link['query']:
                months = 'jan;feb;mar;apr;may;jun;jul;aug;sep;oct;nov;dec'.split(';')
                try:
                    event_month_num = months.index(link['event_month'][:3].lower()) + 1
                    link['show_this_year'] = today.month <= event_month_num
                    link['show_next_year'] = today.month >= event_month_num - 5
                except ValueError:
                    link['show_this_year'] = True
                    link['show_next_year'] = True
                link['this_year_url'] = 'http://www.google.com/search?q=%s&btnI' % urllib.parse.quote(link['query'].replace(r'{{year}}', str(today.year)))
                link['next_year_url'] = 'http://www.google.com/search?q=%s&btnI' % urllib.parse.quote(link['query'].replace(r'{{year}}', str(today.year + 1)))
                link['this_year_label'] = link['query'].replace(r'{{year}}', str(today.year))
                link['next_year_label'] = link['query'].replace(r'{{year}}', str(today.year + 1))                
                
    return template.render(data=data)

def render_contact(data):
    template = env.get_template('contact.html')
    return template.render(data=data)

def render_page(data, page):
    template = env.get_template('page.html')
    return template.render(data=data, title=page['title'], content=page['content'])

def render_redirect(data, redirect):
    template = env.get_template('redirect.html')
    return template.render(data=data, url=redirect['url'])

def render_personal_website(data, website):
    template = env.get_template('personal_website.html')
    return template.render(data=data, website=website['website'], contents=website['contents'])

init_env()
