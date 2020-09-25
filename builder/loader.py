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
    'Metadata!B2:C',
    'Announcements!A2:C',
    'Members!A2:H',
    'Research!A2:F',
    'Tags!A2:F',
    'Links!A2:G',
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

def row_to_dict(row, keys, start_at=0):
    i = start_at
    result_dict = {}
    for key in keys:
        if len(row) > i:
            result_dict[key] = row[i]
        else:
            result_dict[key] = ''
        i += 1
    return result_dict

def conv_metadata(table):
    items = {}
    for row in table:
        items[row[0]] = row[1] if len(row) > 1 else ''
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
        member = row_to_dict(row, ['name', 'email', 'image', 'description', 'links', 'degree', 'year'], 1)
        group['members'].append(member)
    if group:
        groups.append(group)
    return groups

def conv_research(table):
    groups = []
    group = None
    for row in table:
        title = row[0]
        if group is None or group['title'] != title:
            if group:
                groups.append(group)
            group = {'title': title, 'rows': []}
        item = row_to_dict(row, ['title', 'authors', 'booktitle', 'links', 'tags'], 1)            
        if 'tags' in item:
            item['tags'] = [tag.strip() for tag in (item['tags'] or '').split(',') if tag]
        group['rows'].append(item)
    if group:
        groups.append(group)
    return groups

def conv_tags(table):
    tags = {}
    for row in table:
        tags[row[0]] = {
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
            group = {'title': title, 'rows': []}
        item = row_to_dict(row, ['title', 'full_title', 'url', 'query', 'call_month', 'event_month'], 1)
        group['rows'].append(item)
    if group:
        groups.append(group)
    return groups

def load_data():
    doc_id = get_doc_id()
    tables = load_ranges(doc_id, RANGES)
    return {
        'metadata': conv_metadata(tables[0]),
        'announcements': conv_announcements(tables[1]),
        'members': conv_members(tables[2]),
        'research': conv_research(tables[3]),
        'tags': conv_tags(tables[4]),
        'links': conv_links(tables[5]),
    }

