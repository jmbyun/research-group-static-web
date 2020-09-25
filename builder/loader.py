import certifi
import dateutil.parser
import re
import json
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from . import config

SHEETS_URL_BASE = 'https://sheets.googleapis.com/v4/spreadsheets'
RANGES = [
    'Metadata!A1:B',
    'Announcements!A2:C',
    'Members!A2:H',
    'Research!A2:F',
    'Tags!A2:F',
    'Links!A2:G',
    'Redirections!A2:B',
]

def get_doc_id():
    data_url = config.DATA_URL
    tokens = data_url.split('/')
    doc_id = ''
    # Use a heuristic method for finding document ID from the URL.
    for token in tokens:
        if re.match(r'[a-zA-Z0-9]+', token) is not None:
            if len(token) > len(doc_id):
                doc_id = token
    return doc_id

def load_ranges(doc_id, ranges):
    params = '&'.join(['ranges=%s' % urllib.parse.quote(r) for r in ranges])
    url = '%s/%s/values:batchGet?%s&key=%s' % (SHEETS_URL_BASE, doc_id, params, config.API_KEY)

    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, cafile=certifi.where()) as response:
        data = response.read()
    data_dict = json.loads(data)
    return [r['values'] for r in data_dict['valueRanges']]

def conv_metadata(table):
    items = {}
    for row in table:
        items[row[0]] = row[1]
    return items

def conv_announcements(table):
    items = []
    for row in table:
        if row[2]:
            expire_at = dateutil.parser.parse(row[2]) 
            now = datetime.now(timezone.utc)
            if expire_at <= now:
                # This is already expired.
                continue
        items.append({
            'title': row[0],
            'content': row[1]
        })
    return items

def conv_members(table):
    groups = []
    group = None
    for row in table:
        title = row[0]
        if group is None or group['title'] != title:
            if group:
                groups.append(group)
            group = {'title': title, 'members': []}
        group['members'].append({
            'name': row[1],
            'email': row[2],
            'image': row[3],
            'description': row[4],
            'links': row[5],
            'degree': row[6],
            'year': row[7],
        })
    return groups

def conv_research(table):
    groups = []
    group = None
    for row in table:
        title = row[0]
        if group is None or group['title'] != title:
            if group:
                groups.append(group)
            group = {'title': title, 'items': []}
        group['items'].append({
            'title': row[1],
            'authors': row[2],
            'booktitle': row[3],
            'links': row[4],
            'tags': [tag.strip() for tag in (row[5] or '').split(',') if tag]
        })
    return groups

def conv_tags(table):
    tags = {}
    for row in table:
        items[row[0]] = {
            'title': row[1],
            'tag': row[2],
            'color': row[3],
        }
    return tags

def conv_links(table):
    groups = []
    group = None
    for row in table:
        title = row[0]
        if group is None or group['title'] != title:
            if group:
                groups.append(group)
            group = {'title': title, 'items': []}
        group['items'].append({
            'title': row[1],
            'full_title': row[2],
            'url': row[3],
            'query': row[4],
            'call_month': row[5],
            'event_month': row[6],
        })
    return groups

def load_data():
    doc_id = get_doc_id()
    tables = load_ranges(doc_id, RANGES)
    return {
        'metadata': conv_metadata(tables[0]),
        'announcements': conv_announcements(tables[1]),
        'members': conv_members(tables[2]),
        'research': conv_research(tables[3]),
        'tags': conv_tags(tables[4),
        'links': conv_links(tables[5]),
    }

