"""Render task PDFs and the private Korean submission report."""
from __future__ import annotations

import argparse
from html import escape
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.local/python'))
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, CondPageBreak, Frame, Image, KeepTogether, PageTemplate, Paragraph, Spacer, Table, TableStyle

INK = colors.HexColor('#172b2b')
TEAL = colors.HexColor('#086b67')


def fonts():
    for normal, bold in [('C:/Windows/Fonts/malgun.ttf', 'C:/Windows/Fonts/malgunbd.ttf'),
                         ('/usr/share/fonts/truetype/nanum/NanumGothic.ttf', '/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf')]:
        if Path(normal).exists():
            pdfmetrics.registerFont(TTFont('Korean', normal))
            pdfmetrics.registerFont(TTFont('KoreanBold', bold if Path(bold).exists() else normal))
            display = Path('C:/Windows/Fonts/HANBatangB.ttf')
            pdfmetrics.registerFont(TTFont('KoreanDisplay', str(display) if display.exists() else bold))
            pdfmetrics.registerFontFamily('Korean', normal='Korean', bold='KoreanBold')
            return
    raise RuntimeError('A Korean TrueType font is required; configure fonts() for this host.')


def styles():
    return {
        'title': ParagraphStyle('title', fontName='KoreanDisplay', fontSize=24, leading=34, textColor=INK, spaceAfter=14),
        'heading': ParagraphStyle('heading', fontName='KoreanDisplay', fontSize=16, leading=24, textColor=TEAL, spaceBefore=16, spaceAfter=9, keepWithNext=True),
        'body': ParagraphStyle('body', fontName='Korean', fontSize=10.5, leading=17, textColor=INK, spaceAfter=7, wordWrap='CJK', allowWidows=0),
        'report': ParagraphStyle('report', fontName='Korean', fontSize=10.5, leading=17,
                                textColor=INK, spaceAfter=7, wordWrap='CJK', allowWidows=0),
        'case': ParagraphStyle('case', fontName='KoreanBold', fontSize=12, leading=18,
                               textColor=INK, spaceBefore=10, spaceAfter=6,
                               wordWrap='CJK', keepWithNext=True),
        'small': ParagraphStyle('small', fontName='Korean', fontSize=8, leading=13, textColor=INK, spaceAfter=5, wordWrap='CJK'),
    }


def markup(text):
    text = escape(text.strip())
    text = re.sub(r'`([^`]+)`', r'<b>\1</b>', text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', text)
    # URLs are kept as visible, clickable addresses.
    text = re.sub(r'https?://[^\s<>]+', lambda m: '<link href="' + m[0] + '">' + m[0] + '</link>', text)
    return text


def content_table(headers, data, widths, sheet, formatter=markup, key_column=False):
    cell = ParagraphStyle('table-cell', parent=sheet['report'], spaceAfter=0)
    head = ParagraphStyle('table-heading', parent=cell, fontName='KoreanBold')
    rows = [[Paragraph(formatter(str(c)), head) for c in headers]]
    rows += [[Paragraph(formatter(str(c)), head if key_column and i == 0 else cell)
              for i, c in enumerate(row)] for row in data]
    table = Table(rows, colWidths=[w*mm for w in widths], repeatRows=1, hAlign='LEFT')
    table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#edf2f0')),
        ('LINEBELOW', (0, 0), (-1, 0), 0.7, TEAL),
        ('LINEBELOW', (0, 1), (-1, -1), 0.3, colors.HexColor('#d9e0dc')),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
        ('RIGHTPADDING', (0, 0), (-1, -1), 7),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    return table


def table_heading(text, style):
    # Keep room for the title, repeated header and first row, while letting long
    # tables start partway down a page rather than moving the entire table.
    style = ParagraphStyle('table-title', parent=style, keepWithNext=False)
    return [CondPageBreak(48*mm), Paragraph(markup(text), style)]


def markdown_blocks(text, sheet):
    blocks, lines = [], text.splitlines()
    index = 0
    while index < len(lines):
        line = lines[index].strip()
        index += 1
        if not line:
            continue
        if line.startswith('```'):
            code = []
            while index < len(lines) and not lines[index].startswith('```'):
                code.append(lines[index])
                index += 1
            index += 1
            if line == '```mermaid':
                # The current source contains one linear six-step data flow.
                labels = list(dict.fromkeys(re.findall(r'\w+\[([^\]]+)\]', '\n'.join(code))))
                blocks.append(Paragraph(markup(' → '.join(labels)), sheet['body']))
            else:
                for code_line in code:
                    blocks.append(Paragraph(escape(code_line), sheet['body']))
        elif line.startswith('|'):
            rows = [[c.strip() for c in line.strip('|').split('|')]]
            while index < len(lines) and lines[index].strip().startswith('|'):
                row = [c.strip() for c in lines[index].strip().strip('|').split('|')]
                if not all(re.fullmatch(r':?-+:?', c) for c in row):
                    rows.append(row)
                index += 1
            widths = {2:[40,130], 3:[36,67,67], 4:[24,32,59,55]}.get(len(rows[0]))
            blocks.extend([content_table(rows[0],rows[1:],widths,sheet),Spacer(1,4*mm)])
        elif line.startswith('### '):
            blocks.append(Paragraph(markup(line[4:]), sheet['case']))
        elif line.startswith('## '):
            next_line=next((s.strip() for s in lines[index:] if s.strip()),'')
            if next_line.startswith('|'):
                blocks.extend(table_heading(line[3:],sheet['heading']))
            else:
                blocks.append(Paragraph(markup(line[3:]), sheet['heading']))
        elif line.startswith('# '):
            blocks.append(Paragraph(markup(line[2:]), sheet['title']))
        else:
            is_list = bool(re.match(r'(?:- |\d+\. )',line))
            while index < len(lines) and lines[index].strip() and not lines[index].startswith(('#','|','```','- ')) and not re.match(r'\d+\. ',lines[index]) and not is_list:
                line += ' ' + lines[index].strip()
                index += 1
            blocks.append(Paragraph(markup(line),sheet['body']))
    return blocks


def page_number(canvas, document):
    canvas.setFont('Korean', 8)
    canvas.drawRightString(A4[0] - 20*mm, 12*mm, str(document.page))


def task_pdfs(selected=None):
    sheet = styles()
    for source in sorted((ROOT / 'docs/tasks').glob('T[0-9][0-9].md')):
        if selected and source.stem not in selected:
            continue
        blocks = markdown_blocks(source.read_text(encoding='utf-8'), sheet)
        doc = BaseDocTemplate(str(source.with_suffix('.pdf')), pagesize=A4, rightMargin=20*mm,
                                leftMargin=20*mm, topMargin=20*mm, bottomMargin=20*mm,
                                title=source.stem + ' 개발 기록', author='Jung Jiwoong')
        frame = Frame(20*mm,20*mm,A4[0]-40*mm,A4[1]-40*mm,
                      leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)
        doc.addPageTemplates([PageTemplate(id='task',frames=[frame],onPage=page_number)])
        doc.build(blocks)
        print(source.with_suffix('.pdf').relative_to(ROOT).as_posix())


def submission(release_path, identity_path):
    release = json.loads(release_path.read_text(encoding='utf-8'))
    identity = json.loads(identity_path.read_text(encoding='utf-8'))
    sheet = styles()
    blocks = [Paragraph('개인 소개 웹사이트 구축 결과 보고서', sheet['title']),
              Paragraph('2026학년도 초급프로젝트 · 과제 1', sheet['small'])]
    sections = json.loads((ROOT / 'docs/report-sections.json').read_text(encoding='utf-8'))
    tokens = {'STUDENT_ID': identity['student_id'], 'STUDENT_NAME': identity['name'],
              'FINAL_SHA': release['sha'], 'COMMIT_URL': release['commit_url'],
              'ACTIONS_URL': release['actions_url'], 'ACTIONS_STATUS': release['actions_status'],
              'CANDIDATES': str(release['candidate_count']), 'EXCLUDED': str(release['excluded_count']),
              'VALID_COUNT': str(release['valid_count']), 'WRITTEN_AT': release['collected_at']}
    tokens['SOURCE_BASE'] = 'https://github.com/studentnoname/website_proj/blob/' + release['sha'] + '/'
    excluded_commits = [entry for entry in release['commits'] if not entry['included']]
    reasons = {
        'Official ZIP and generated baseline registration; not original project work.': '공식 원본 ZIP과 준비 결과의 단순 등록',
        'Generated PDF artifacts only; source document work is counted separately.': 'TASK PDF만 자동 생성한 커밋; 원문 작성 이력과 중복하여 세지 않음',
        'Merge commit; source commits are counted separately.': '병합 커밋; 원래 작업 커밋을 별도로 집계',
        'Empty change.': '실제 변경 없음',
    }
    tokens['EXCLUDED_DETAILS'] = '; '.join(
        entry['sha'] + ': ' + reasons.get(entry['exclusion_reason'], entry['exclusion_reason'])
        for entry in excluded_commits) if excluded_commits else '없음(0개)'
    capture = json.loads((ROOT / 'docs/evidence/T08/firefox/results.json').read_text(encoding='utf-8'))
    progressive = json.loads((ROOT / 'docs/evidence/T08/progressive/results.json').read_text(encoding='utf-8'))
    if not capture['passed'] or not progressive['passed']:
        raise ValueError('Passing, repository-tracked browser evidence is required for the submission report.')
    tokens['SCREEN_TIME'] = capture['checked_at']
    tokens['BROWSER_CHECKS'] = str(len(capture['results']))
    tokens['PROGRESSIVE_CHECKS'] = str(len(progressive['results']))

    def fill(text):
        for key, value in tokens.items():
            text = text.replace('{' + key + '}', value)
        return text

    def figure(relative, caption, width_mm):
        captured_at = capture.get('screenshots', {}).get(relative, {}).get('captured_at', tokens['SCREEN_TIME'])
        caption = fill(caption.replace('{SCREEN_TIME}', captured_at))
        path = ROOT / relative
        if not path.is_file():
            raise FileNotFoundError(path)
        picture = Image(str(path))
        source_width, source_height = picture.imageWidth, picture.imageHeight
        picture.drawWidth = width_mm * mm
        picture.drawHeight = source_height * picture.drawWidth / source_width
        caption_blocks = [Paragraph(markup(caption), sheet['small']),
                          Paragraph('저장소 상대 경로(클릭): <link href="' +
                                    escape(tokens['SOURCE_BASE'] + relative, quote=True) + '">' +
                                    escape(relative) + '</link>', sheet['small'])]
        return picture, caption_blocks

    def paragraph(text):
        text = markup(fill(text))
        text = re.sub(r'^([^:<]{1,36}):', r'<b>\1:</b>', text, count=1)
        return Paragraph(text, sheet['report'])

    def report_table(headers, data, widths, key_column=False):
        return content_table(headers,data,widths,sheet,lambda c:markup(fill(c)),key_column)

    def field_rows(items):
        return [list(item.split(':', 1)) for item in items]

    for section in sections:
        section_start = len(blocks)
        blocks.append(Paragraph(section['title'], sheet['heading']))
        number = int(section['title'].split()[0])
        items = list(section['outline'])
        subheadings = {section['outline'][int(i)]: title for i,title in section.get('subheadings',{}).items()}
        if number==1:
            blocks.extend([report_table(['항목','제출 정보'],field_rows(items[:9]),[35,135],True),Spacer(1,5*mm)])
            items=items[9:]
        if number==4:
            labels=('집계 구간:','시작 기준 포함 여부:','유효 개수:','실제 제외 목록')
            summary=[s for s in items if s.startswith(labels)]
            blocks.extend([report_table(['항목','집계 내용'],field_rows(summary),[37,133],True),Spacer(1,5*mm)])
            items=[s for s in items if s not in summary]
        case_start = None
        index=0
        while index<len(items):
            item=items[index]
            if item in subheadings:
                if item.startswith(('P71','E1 ')):
                    blocks.extend(table_heading(subheadings[item],sheet['case']))
                else:
                    blocks.append(Paragraph(markup(subheadings[item]),sheet['case']))
            if number==2 and item.startswith('P71'):
                last=next(i for i in range(index,len(items)) if items[i].startswith('P80'))
                blocks.extend([report_table(['기준','사이트에 반영한 내용'],field_rows(items[index:last+1]),[34,136],True),Spacer(1,5*mm)])
                index=last+1
                continue
            if number==3 and re.match(r'변경 [12] ',item) and '변경 전:' in item:
                title,before=item.split('변경 전:',1)
                blocks.append(KeepTogether([
                    Paragraph(markup(fill(title.strip())),sheet['case']),
                    report_table(['구분','변경 내용'],[['변경 전',before],items[index+1].split(':',1)],[26,144],True),
                    Spacer(1,4*mm)]))
                index+=2
                continue
            if number==5 and item.startswith('E1 '):
                evidence=items[index:index+4]
                blocks.extend([report_table(['근거','저장소 경로와 링크'],field_rows(evidence),[40,130],True),Spacer(1,4*mm)])
                index+=4
                continue
            if number==6 and item.startswith('관찰:'):
                blocks.extend([report_table(['단계','본문 출력 문제의 확인과 조치'],field_rows(items[index:index+4]),[28,142],True),Spacer(1,5*mm)])
                index+=4
                continue
            text = markup(fill(item))
            if item.startswith('사례 ') and section['title'].startswith('7 '):
                if case_start is not None:
                    blocks[case_start:] = [KeepTogether(blocks[case_start:])]
                case_start = len(blocks)
                blocks.append(Paragraph(text, sheet['case']))
                index+=1
                continue
            blocks.extend(paragraph(part) for part in item.split('\n\n'))
            index+=1
        if case_start is not None:
            blocks[case_start:] = [KeepTogether(blocks[case_start:])]
            blocks[section_start:section_start+2] = [KeepTogether(blocks[section_start:section_start+2])]
        if section.get('table'):
            blocks.extend(table_heading('영역별 검증 결과',sheet['case']))
            blocks.extend([report_table(section['table']['headers'],section['table']['rows'],[20,36,51,63]),Spacer(1,5*mm)])
        images = section.get('image', [])
        if images:
            desktop, desktop_captions = figure(*images[0], 118)
            mobile, mobile_captions = figure(*images[1], 38)
            pair = Table([[desktop, mobile]], colWidths=[123*mm, 47*mm])
            pair.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'),
                                     ('LEFTPADDING', (0, 0), (-1, -1), 0),
                                     ('RIGHTPADDING', (0, 0), (-1, -1), 0)]))
            blocks.append(KeepTogether([pair, Spacer(1, 2*mm), *desktop_captions, *mobile_captions]))
            for relative, caption in images[2:]:
                picture, captions = figure(relative, caption, 150)
                blocks.append(KeepTogether([Spacer(1, 3*mm), picture, Spacer(1, 2*mm), *captions]))
        if section['title'].startswith('8 '):
            blocks[section_start:] = [KeepTogether(blocks[section_start:])]
    folder = ROOT / 'submission'
    folder.mkdir(exist_ok=True)
    output = folder / f"{identity['student_id']}_{identity['name']}_과제1.pdf"
    temporary = output.with_suffix('.building.pdf')
    doc = BaseDocTemplate(str(temporary), pagesize=A4, rightMargin=20*mm, leftMargin=20*mm,
                            topMargin=20*mm, bottomMargin=20*mm,
                            title='개인 소개 웹사이트 구축 결과 보고서', author=identity['name'])
    frame=Frame(20*mm,20*mm,A4[0]-40*mm,A4[1]-40*mm,
                leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id='report',frames=[frame],onPage=page_number)])
    try:
        doc.build(blocks)
        temporary.replace(output)
    finally:
        temporary.unlink(missing_ok=True)
    print('Private submission PDF created under submission/.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tasks', action='store_true')
    parser.add_argument('--task', action='append', choices=[f'T{i:02}' for i in range(1,10)],
                        help='Regenerate only this TASK PDF; repeat for multiple records.')
    parser.add_argument('--release', type=Path)
    parser.add_argument('--identity', type=Path)
    args = parser.parse_args()
    fonts()
    if args.tasks or args.task:
        task_pdfs(args.task)
    if args.release:
        if not args.identity:
            parser.error('--identity is required with --release')
        submission(args.release, args.identity)


if __name__ == '__main__':
    main()
