"""Export final main SHA, deployment result and inspectable commit-count evidence."""
from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import subprocess
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
REPO = 'studentnoname/website_proj'
BASELINE = '42f92735f3729f9aa0d63d637fa45f6d2dd25629'


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True, encoding='utf-8').strip()


def github(path):
    request = urllib.request.Request('https://api.github.com/' + path,
                                     headers={'User-Agent': 'portfolio-release', 'Accept': 'application/vnd.github+json'})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def collect():
    sha = git('rev-parse', 'main')
    if git('rev-parse', 'HEAD') != sha:
        raise RuntimeError('Switch to the submitted main commit before collecting the final release.')
    if git('status', '--porcelain'):
        raise RuntimeError('Commit or explicitly exclude pending project changes before final collection.')
    if git('ls-remote', 'origin', 'refs/heads/main').split()[0] != sha:
        raise RuntimeError('Local and remote main do not match.')
    commits = git('rev-list', '--reverse', 'main').splitlines()
    evidence = []
    for commit in commits:
        names = git('diff-tree', '--root', '--no-commit-id', '--name-only', '-r', commit).splitlines()
        parents = git('rev-list', '--parents', '-n', '1', commit).split()[1:]
        subject = git('show', '-s', '--format=%s', commit)
        reason = ''
        if commit == BASELINE:
            reason = 'Official ZIP and generated baseline registration; not original project work.'
        elif len(parents) > 1:
            reason = 'Merge commit; source commits are counted separately.'
        elif not names:
            reason = 'Empty change.'
        elif all(Path(name).suffix.lower() == '.pdf' for name in names):
            reason = 'Generated PDF artifacts only; source document work is counted separately.'
        evidence.append({'sha': commit, 'subject': subject, 'paths': names, 'included': not reason,
                         'exclusion_reason': reason, 'url': f'https://github.com/{REPO}/commit/{commit}'})
    runs = github(f'repos/{REPO}/actions/workflows/hugo-pages.yml/runs?head_sha={sha}&event=push&per_page=5')['workflow_runs']
    if not runs:
        raise RuntimeError('No push-triggered Pages workflow for the final SHA.')
    run = runs[0]
    if run['status'] != 'completed' or run['conclusion'] != 'success':
        raise RuntimeError('Final deployment is not successful yet: ' + run['html_url'])
    site = f'https://studentnoname.github.io/website_proj/'
    for suffix in ['', 'en/']:
        with urllib.request.urlopen(site + suffix, timeout=30) as response:
            text = response.read().decode('utf-8')
            if response.status != 200 or 'KONNECT' not in text or 'id=intro' not in text:
                raise RuntimeError('Public portfolio content is missing: ' + suffix)
    excluded = sum(not entry['included'] for entry in evidence)
    return {'collected_at': datetime.now(timezone(timedelta(hours=9))).isoformat(),
            'sha': sha, 'commit_url': f'https://github.com/{REPO}/commit/{sha}',
            'site_url': site, 'repository_url': f'https://github.com/{REPO}',
            'actions_url': run['html_url'], 'actions_status': run['conclusion'],
            'baseline_sha': BASELINE, 'baseline_included': False,
            'candidate_count': len(evidence), 'excluded_count': excluded,
            'valid_count': len(evidence) - excluded, 'commits': evidence}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'submission/release.json')
    args = parser.parse_args()
    release = collect()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(release, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({key: release[key] for key in ['sha', 'actions_url', 'candidate_count', 'excluded_count', 'valid_count']}, indent=2))


if __name__ == '__main__':
    main()
