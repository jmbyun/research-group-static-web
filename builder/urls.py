from .renderer import *

class Page:
    def __init__(self, path, renderer):
        self.path = path
        self.renderer = renderer

def get_pages():
    return [
        Page('index.html', render_index),
        Page('members.html', render_members),
        Page('research.html', render_research),
        Page('links.html', render_links),
        Page('contact.html', render_contact),
    ]