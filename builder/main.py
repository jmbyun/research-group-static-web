import json
import os
import shutil
from . import config, loader, urls

def init_build_path():
    if not os.path.exists(config.BUILD_PATH):
        os.makedirs(config.BUILD_PATH)

def render_pages():
    data = loader.load_data()

    for page in urls.get_pages(data):
        page_abs_path = os.path.join(config.BUILD_PATH, page.path)
        page_dir_abs_path = os.path.dirname(page_abs_path)
        if not os.path.exists(page_dir_abs_path):
            os.makedirs(page_dir_abs_path)
        with open(page_abs_path, 'w') as f:
            f.write(page.renderer(data))

    data_export_path = os.path.join(config.BUILD_PATH, 'data.json')
    with open(data_export_path, 'w') as f:
        json.dump(data, f)

def copy_assets():
    source_path = os.path.join(config.BASE_PATH, 'assets')
    target_path = os.path.join(config.BUILD_PATH, 'assets')
    if os.path.exists(target_path):
        shutil.rmtree(target_path)
    shutil.copytree(source_path, target_path)

def build():
    init_build_path()
    render_pages()
    copy_assets()
