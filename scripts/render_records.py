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
from reportlab.platypus import Flowable, Image, KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

INK = colors.HexColor('#172b2b')
TEAL = colors.HexColor('#086b67')


def fonts():
    for normal, bold in [('C:/Windows/Fonts/malgun.ttf', 'C:/Windows/Fonts/malgunbd.ttf'),
                         ('/usr/share/fonts/truetype/nanum/NanumGothic.ttf', '/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf')]:
        if Path(normal).exists():
            pdfmetrics.registerFont(TTFont('Korean', normal))
            pdfmetrics.registerFont(TTFont('KoreanBold', bold if Path(bold).exists() else normal))
            return
    raise RuntimeError('A Korean TrueType font is required; configure fonts() for this host.')


def styles():
    return {
        'title': ParagraphStyle('title', fontName='KoreanBold', fontSize=23, leading=33, textColor=INK, spaceAfter=12),
        'heading': ParagraphStyle('heading', fontName='KoreanBold', fontSize=14, leading=21, textColor=TEAL, spaceBefore=14, spaceAfter=8, keepWithNext=True),
        'body': ParagraphStyle('body', fontName='Korean', fontSize=10, leading=15.5, textColor=INK, spaceAfter=5, wordWrap='CJK', allowWidows=0),
        'outline': ParagraphStyle('outline', fontName='Korean', fontSize=10, leading=15.5,
                                  textColor=INK, leftIndent=12, firstLineIndent=0,
                                  bulletIndent=0, bulletFontName='Korean', bulletFontSize=10,
                                  spaceAfter=2, wordWrap='CJK', allowWidows=0),
        'case': ParagraphStyle('case', fontName='KoreanBold', fontSize=10, leading=15.5,
                               textColor=TEAL, spaceBefore=8, spaceAfter=5,
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


def markdown_blocks(text, sheet):
    blocks = []
    for line in text.splitlines():
        if not line.strip() or line.startswith('```'):
            continue
        if line.startswith('# '):
            blocks.append(Paragraph(markup(line[2:]), sheet['title']))
        elif line.startswith('## '):
            blocks.append(Paragraph(markup(line[3:]), sheet['heading']))
        else:
            blocks.append(Paragraph(markup(line), sheet['body']))
    return blocks


def page_number(canvas, document):
    canvas.setFont('Korean', 8)
    canvas.drawRightString(A4[0] - 20*mm, 12*mm, str(document.page))


class Workflow(Flowable):
    def __init__(self):
        super().__init__()
        self.width, self.height = 170*mm, 24*mm

    def draw(self):
        c = self.canv
        for index, label in enumerate(['요구사항 확인', '구현·선택', '실행·재검증']):
            x = index * 58*mm
            c.setFillColor(colors.HexColor('#eef5f3'))
            c.setStrokeColor(TEAL)
            c.roundRect(x, 3*mm, 49*mm, 15*mm, 3*mm, fill=1)
            c.setFont('KoreanBold', 10)
            c.setFillColor(INK)
            c.drawCentredString(x + 24.5*mm, 9*mm, label)
            if index < 2:
                c.line(x + 50*mm, 10.5*mm, x + 56*mm, 10.5*mm)
                c.line(x + 54*mm, 12*mm, x + 56*mm, 10.5*mm)
                c.line(x + 54*mm, 9*mm, x + 56*mm, 10.5*mm)


def task_pdfs():
    sheet = styles()
    for source in sorted((ROOT / 'docs/tasks').glob('T[0-9][0-9].md')):
        blocks = markdown_blocks(source.read_text(encoding='utf-8'), sheet)
        blocks.insert(1, Workflow())
        doc = SimpleDocTemplate(str(source.with_suffix('.pdf')), pagesize=A4, rightMargin=20*mm,
                                leftMargin=20*mm, topMargin=18*mm, bottomMargin=20*mm,
                                title=source.stem + ' 개발 기록', author='Jung Jiwoong')
        doc.build(blocks, onFirstPage=page_number, onLaterPages=page_number)
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

    for section in sections:
        section_start = len(blocks)
        blocks.append(Paragraph(section['title'], sheet['heading']))
        case_start, case_intro_remaining = None, 0
        for item in section['outline']:
            text = markup(fill(item))
            if item.startswith('사례 ') and section['title'].startswith('7 '):
                case_start, case_intro_remaining = len(blocks), 2
                blocks.append(Paragraph(text, sheet['case']))
                continue
            # Emphasize the field label, leaving the explanatory text at one weight.
            text = re.sub(r'^([^:<]{1,36}):', r'<b>\1:</b>', text, count=1)
            blocks.append(Paragraph(text, sheet['outline'], bulletText='•'))
            if case_intro_remaining:
                case_intro_remaining -= 1
                if not case_intro_remaining:
                    blocks[case_start:] = [KeepTogether(blocks[case_start:])]
        if section.get('table'):
            cell_style = ParagraphStyle('table-cell', parent=sheet['body'], spaceAfter=0)
            cells = [section['table']['headers'], *section['table']['rows']]
            rows = [[Paragraph(markup(fill(str(cell))), cell_style) for cell in row] for row in cells]
            table = Table(rows, colWidths=[20*mm, 38*mm, 48*mm, 64*mm], repeatRows=1, hAlign='LEFT')
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e2efeb')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f7faf9')]),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LINEBELOW', (0, 0), (-1, 0), 0.7, TEAL),
                ('LINEBELOW', (0, 1), (-1, -1), 0.25, colors.HexColor('#d5e1de')),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 7),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
            ]))
            blocks.extend([table, Spacer(1, 4*mm)])
        images = section.get('image', [])
        if images:
            desktop, desktop_captions = figure(*images[0], 118)
            mobile, mobile_captions = figure(*images[1], 38)
            pair = Table([[desktop, mobile]], colWidths=[123*mm, 47*mm])
            pair.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'),
                                     ('LEFTPADDING', (0, 0), (-1, -1), 0),
                                     ('RIGHTPADDING', (0, 0), (-1, -1), 0)]))
            gallery = [pair, Spacer(1, 2*mm), *desktop_captions, *mobile_captions]
            for relative, caption in images[2:]:
                picture, captions = figure(relative, caption, 150)
                gallery.extend([Spacer(1, 3*mm), picture, Spacer(1, 2*mm), *captions])
            blocks.append(KeepTogether(gallery))
        if section['title'].startswith('8 '):
            blocks[section_start:] = [KeepTogether(blocks[section_start:])]
    folder = ROOT / 'submission'
    folder.mkdir(exist_ok=True)
    output = folder / f"{identity['student_id']}_{identity['name']}_과제1.pdf"
    temporary = output.with_suffix('.building.pdf')
    doc = SimpleDocTemplate(str(temporary), pagesize=A4, rightMargin=20*mm, leftMargin=20*mm,
                            topMargin=20*mm, bottomMargin=20*mm,
                            title='개인 소개 웹사이트 구축 결과 보고서', author=identity['name'])
    try:
        doc.build(blocks, onFirstPage=page_number, onLaterPages=page_number)
        temporary.replace(output)
    finally:
        temporary.unlink(missing_ok=True)
    print('Private submission PDF created under submission/.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tasks', action='store_true')
    parser.add_argument('--release', type=Path)
    parser.add_argument('--identity', type=Path)
    args = parser.parse_args()
    fonts()
    if args.tasks:
        task_pdfs()
    if args.release:
        if not args.identity:
            parser.error('--identity is required with --release')
        submission(args.release, args.identity)


if __name__ == '__main__':
    main()
