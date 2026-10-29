"""Install checksum-verified, project-local Windows build tools."""
from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path, PurePosixPath
import sys
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[1]
TOOLS = (
    ('hugo', 'https://github.com/gohugoio/hugo/releases/download/v0.167.0/hugo_extended_0.167.0_windows-amd64.zip',
     'b04cdf0ae9098fe093ea90e1bd778d21649d71f55914d267aa60aa80b59074e0', '.local/tools/hugo', '.local/tools/hugo/hugo.exe'),
    ('go', 'https://go.dev/dl/go1.27.1.windows-amd64.zip',
     'a3911b5e0e1b1053f25ed0675f4c1c6aad1e2bfcf253df2b9be4caabd2edd95d', '.local/tools', '.local/tools/go/bin/go.exe'),
    ('sass', 'https://github.com/sass/dart-sass/releases/download/1.105.0/dart-sass-1.105.0-windows-x64.zip',
     '720463a7c0554641e17239e6b359f24fa5c5bc10776c25236e29c45416ddff07', '.local/tools', '.local/tools/dart-sass/sass.bat'),
)


def install(name: str, url: str, digest: str, destination: str, executable: str) -> None:
    archive = ROOT / '.local/downloads' / f'{name}.zip'
    archive.parent.mkdir(parents=True, exist_ok=True)
    if not archive.is_file():
        temporary = archive.with_suffix('.part')
        request = urllib.request.Request(url, headers={'User-Agent': 'portfolio-local-tools'})
        with urllib.request.urlopen(request, timeout=90) as response, temporary.open('wb') as output:
            while chunk := response.read(1024 * 1024):
                output.write(chunk)
        temporary.replace(archive)
    if hashlib.sha256(archive.read_bytes()).hexdigest() != digest:
        raise RuntimeError(f'Checksum mismatch: {archive}. Remove that archive and retry.')
    if not (ROOT / executable).is_file():
        with zipfile.ZipFile(archive) as source:
            for item in source.infolist():
                parts = PurePosixPath(item.filename.replace('\\', '/')).parts
                if item.filename.startswith('/') or any(p == '..' or ':' in p for p in parts):
                    raise RuntimeError('Unsafe archive path')
            source.extractall(ROOT / destination)
    print(f'{name}: checksum verified; ready in {destination}')


def main() -> None:
    if os.name != 'nt':
        raise SystemExit('This helper installs Windows amd64 tools. See README for other systems.')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    for tool in TOOLS:
        install(*tool)


if __name__ == '__main__':
    main()
