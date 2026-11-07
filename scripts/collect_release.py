"""Export final main SHA, deployment result and inspectable commit-count evidence."""
from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import json
import re
from pathlib import Path
import subprocess
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
REPO = 'studentnoname/website_proj'
BASELINE = '1954a8b29c7c3a5435ec30238c9f9be2090e3b97'


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True, encoding='utf-8').strip()


def github(path):
    request = urllib.request.Request('https://api.github.com/' + path,
                                     headers={'User-Agent': 'portfolio-release', 'Accept': 'application/vnd.github+json'})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def history(ref):
    commits = git('rev-list', '--reverse', ref).splitlines()
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
        elif all(name.startswith('docs/evidence/') or Path(name).suffix.lower() == '.pdf' for name in names):
            reason = 'Evidence artifacts only; conservatively excluded from the substantive-change count.'
        categories = []
        if any(Path(name).suffix.lower() in {'.py', '.ps1', '.html', '.css', '.js'} for name in names):
            categories.append('구현·검사 도구 변경')
        if any(Path(name).suffix.lower() in {'.yaml', '.yml', '.toml', '.json', '.mod'} and not name.startswith('docs/evidence/') for name in names):
            categories.append('설정·의존성·보고서 데이터 변경')
        if any(Path(name).suffix.lower() == '.md' for name in names):
            categories.append('콘텐츠·판단·오류·작업 원문 변경')
        inclusion = ' / '.join(categories) or '실제 추적 파일 변경'
        evidence.append({'sha': commit, 'subject': subject, 'paths': names, 'included': not reason,
                         'exclusion_reason': reason, 'inclusion_reason': '' if reason else inclusion,
                         'url': f'https://github.com/{REPO}/commit/{commit}'})
    return evidence


def write_commit_log(ref):
    sha = git('rev-parse', ref + '^{commit}')
    entries = history(sha)
    excluded = sum(not entry['included'] for entry in entries)
    lines = ['# 커밋 집계 근거', '', f'검토 기준 SHA: `{sha}`', '',
             f'집계 시작 SHA: `{BASELINE}`. 원본 ZIP·준비 결과의 단순 등록이므로 제외하였음.', '',
             f'공개 검토 구간: 전체 후보 {len(entries)}개 - 제외 {excluded}개 = 포함 {len(entries)-excluded}개.', '',
             '아래에는 기준 SHA까지의 모든 커밋과 실제 변경 파일·포함/제외 사유·diff 링크를 제시하였음. 포함 사유의 분류는 파일 목록에서 생성하였으며, 개별 변경의 내용은 커밋 링크에서 확인할 수 있음. 원문이 함께 바뀐 TASK PDF는 원문 변경과 한 번만 세고, 증거 파일만 보관한 커밋은 보수적으로 제외하였음.', '',
             '최종 제출 SHA는 보고서 1절에 기재함. 이 공개 기준 이후 최종 SHA까지의 추가 커밋·변경 파일·포함/제외 사유는 보고서 4절에 별도로 출력함. 자기 SHA를 문서에 넣기 위한 amend·이력 재작성 없이 최종 구간 전체를 대조할 수 있음.', '',
             '개인정보 보호를 위한 이전 작성자·커미터 교체는 파일 트리·메시지·시각·개수·부모 관계를 보존하였으며, 같은 커밋을 중복하여 세지 않았음. 작성자 개인정보와 비공개 KONNECT 코드는 이 목록에 포함하지 않았음.', '',
             '| 번호 | 전체 SHA·diff | 실제 변경 내용 | 변경 파일 | 포함/제외 근거 |',
             '| --- | --- | --- | --- | --- |']
    for n, entry in enumerate(entries, 1):
        subject = entry['subject'].replace('|', '\\|')
        paths = (f"원본 ZIP·준비 결과 {len(entry['paths'])}개 파일(전체 목록은 diff)" if entry['sha'] == BASELINE else
                 '<br>'.join('`' + name.replace('|', '\\|') + '`' for name in entry['paths']))
        exclusion_labels = {
            'Official ZIP and generated baseline registration; not original project work.': '공식 원본 ZIP과 준비 결과의 단순 등록',
            'Generated PDF artifacts only; source document work is counted separately.': 'PDF만 자동 생성한 변경으로 원문 작성 이력과 중복하여 세지 않음',
            'Evidence artifacts only; conservatively excluded from the substantive-change count.': '검증 증거만 보관한 변경은 보수적으로 제외',
            'Merge commit; source commits are counted separately.': '병합 커밋은 원래 작업 커밋과 중복하여 세지 않음',
            'Empty change.': '실제 변경 없음',
        }
        verdict = ('포함: ' + entry['inclusion_reason']) if entry['included'] else (
            '제외: ' + exclusion_labels.get(entry['exclusion_reason'], entry['exclusion_reason']))
        lines.append(f"| {n} | [{entry['sha']}]({entry['url']}) | {subject} | {paths} | {verdict} |")
    (ROOT / 'docs/commit-log.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(json.dumps({'audit_sha': sha, 'candidate_count': len(entries), 'excluded_count': excluded,
                      'included_count': len(entries)-excluded}))


def collect():
    sha = git('rev-parse', 'main')
    if git('rev-parse', 'HEAD') != sha:
        raise RuntimeError('Switch to the submitted main commit before collecting the final release.')
    if git('status', '--porcelain'):
        raise RuntimeError('Commit or explicitly exclude pending project changes before final collection.')
    if git('ls-remote', 'origin', 'refs/heads/main').split()[0] != sha:
        raise RuntimeError('Local and remote main do not match.')
    evidence = history(sha)
    snapshot = re.search(r'검토 기준 SHA: `([0-9a-f]{40})`', (ROOT / 'docs/commit-log.md').read_text(encoding='utf-8'))
    audit_sha = snapshot.group(1) if snapshot else None
    if audit_sha:
        git('merge-base', '--is-ancestor', audit_sha, sha)
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
            'public_commit_audit_sha': audit_sha,
            'baseline_sha': BASELINE, 'baseline_included': False,
            'candidate_count': len(evidence), 'excluded_count': excluded,
            'valid_count': len(evidence) - excluded, 'commits': evidence}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'submission/release.json')
    parser.add_argument('--commit-log-ref', help='Write the existing public commit log through this immutable commit.')
    args = parser.parse_args()
    if args.commit_log_ref:
        write_commit_log(args.commit_log_ref)
        return
    release = collect()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(release, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({key: release[key] for key in ['sha', 'actions_url', 'candidate_count', 'excluded_count', 'valid_count']}, indent=2))


if __name__ == '__main__':
    main()
