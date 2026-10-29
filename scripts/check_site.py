"""Check emitted HTML against the Pages path, language and content requirements."""
from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / 'public'
ORIGIN = 'https://studentnoname.github.io'
PREFIX = '/website_proj/'
SECTIONS = {'intro', 'about', 'future', 'current'}


class Document(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.references = []
        self.errors = []
        self.lang = ''
        self.h1_count = 0
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == 'html':
            self.lang = values.get('lang', '')
        if tag == 'h1':
            self.h1_count += 1
        if values.get('id'):
            if values['id'] in self.ids:
                self.errors.append('Duplicate id: ' + values['id'])
            self.ids.add(values['id'])
        if tag == 'img' and 'alt' not in values:
            self.errors.append('Image without alt: ' + values.get('src', ''))
        for attr in ('href', 'src', 'poster'):
            if attr in values:
                self.references.append((tag, attr, values[attr]))
        if values.get('srcset'):
            self.references.extend((tag, 'srcset', entry.strip().split()[0])
                                   for entry in values['srcset'].split(',') if entry.strip())


def inspect():
    failures = []
    checks = []
    parsed = {}
    for rel, expected in [('index.html', 'ko'), ('en/index.html', 'en')]:
        file = PUBLIC / rel
        if not file.is_file():
            failures.append(f'Missing homepage: {rel}')
            continue
        text = file.read_text(encoding='utf-8')
        document = Document(text)
        parsed[file.resolve()] = document
        errors = list(document.errors)
        if document.lang.split('-')[0].lower() != expected:
            errors.append(f'Expected {expected} language, got {document.lang}')
        if document.h1_count != 1:
            errors.append(f'Expected one h1, got {document.h1_count}')
        if SECTIONS - document.ids:
            errors.append('Missing sections: ' + ', '.join(sorted(SECTIONS - document.ids)))
        for phrase in ('Your Name', 'Download CV', 'DeepMind', 'Alice Smith', 'Lorem ipsum'):
            if phrase in text:
                errors.append('Demo content: ' + phrase)
        if 'Jung Jiwoong' not in text or 'KONNECT' not in text:
            errors.append('Missing personal introduction or KONNECT activity')
        for value in ('localhost', '127.0.0.1', 'file://', 'C:\\Users\\'):
            if value in text:
                errors.append('Development address leaked: ' + value)
        base_url = ORIGIN + PREFIX + ('' if rel == 'index.html' else 'en/')
        for tag, attr, reference in document.references:
            if reference.startswith(('mailto:', 'tel:', 'data:')):
                continue
            if not reference or reference == '#':
                errors.append(f'Empty {tag} {attr}')
                continue
            if reference.startswith(('javascript:', 'http:')):
                errors.append('Unsafe or mixed-content reference: ' + reference)
                continue
            resolved = urlsplit(urljoin(base_url, reference))
            if resolved.netloc != urlsplit(ORIGIN).netloc:
                continue
            if not resolved.path.startswith(PREFIX):
                errors.append('Escapes deployment prefix: ' + reference)
                continue
            target = PUBLIC / unquote(resolved.path[len(PREFIX):])
            if target.is_dir():
                target = target / 'index.html'
            if not target.is_file():
                errors.append('Missing internal target: ' + reference)
                continue
            if resolved.fragment and target.suffix == '.html':
                other = parsed.get(target.resolve())
                if other is None:
                    other = Document(target.read_text(encoding='utf-8'))
                    parsed[target.resolve()] = other
                if unquote(resolved.fragment) not in other.ids:
                    errors.append('Missing anchor: ' + reference)
        checks.append({'page': rel, 'language': document.lang, 'references': len(document.references),
                       'sections': sorted(SECTIONS & document.ids), 'errors': errors})
        failures.extend(f'{rel}: {error}' for error in errors)
    return {'checked_at': datetime.now(timezone(timedelta(hours=9))).isoformat(),
            'base_url': ORIGIN + PREFIX, 'passed': not failures,
            'checks': checks, 'failures': failures}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = inspect()
    text = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding='utf-8')
    print(text)
    raise SystemExit(0 if result['passed'] else 1)


if __name__ == '__main__':
    main()
