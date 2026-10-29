"""Serve the production output under its actual GitHub Pages project path."""
from __future__ import annotations

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
PREFIX = '/website_proj'


class ProjectHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        path = urlsplit(self.path).path
        if path == '/':
            self.send_response(302)
            self.send_header('Location', PREFIX + '/')
            self.end_headers()
            return
        if path == PREFIX:
            self.send_response(301)
            self.send_header('Location', PREFIX + '/')
            self.end_headers()
            return
        if not path.startswith(PREFIX + '/'):
            self.send_error(404, 'Outside the project deployment path')
            return
        self.path = self.path[len(PREFIX):]
        super().do_GET()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=1313)
    args = parser.parse_args()
    public = ROOT / 'public'
    if not (public / 'index.html').is_file():
        raise SystemExit('Build the site first: python .github/pages_build.py --build')
    handler = partial(ProjectHandler, directory=str(public))
    server = ThreadingHTTPServer(('127.0.0.1', args.port), handler)
    print(f'Local: http://127.0.0.1:{args.port}{PREFIX}/', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
