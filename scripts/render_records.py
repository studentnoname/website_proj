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
        'body': ParagraphStyle('body', fontName='Korean', fontSize=10, leading=16, textColor=INK, spaceAfter=6, wordWrap='CJK'),
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
    capture = ROOT / 'submission/screens/results.json'
    tokens['SCREEN_TIME'] = json.loads(capture.read_text(encoding='utf-8'))['checked_at'] if capture.is_file() else '미캡처'
    for section in sections:
        blocks.append(Paragraph(section['title'], sheet['heading']))
        if section.get('table'):
            cell_style = ParagraphStyle('table-cell', parent=sheet['body'], fontSize=9, leading=14, spaceAfter=0)
            cells = [section['table']['headers'], *section['table']['rows']]
            rows = [[Paragraph(markup(str(cell)), cell_style) for cell in row] for row in cells]
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
        for paragraph in section['paragraphs']:
            for key, value in tokens.items():
                paragraph = paragraph.replace('{' + key + '}', value)
            blocks.append(Paragraph(markup(paragraph), sheet['body']))
        for relative, caption in section.get('image', []):
            for key, value in tokens.items():
                caption = caption.replace('{' + key + '}', value)
            path = ROOT / relative
            if not path.is_file():
                raise FileNotFoundError(path)
            picture = Image(str(path))
            width = min(170*mm, picture.imageWidth * 0.35)
            height = picture.imageHeight * width / picture.imageWidth
            if height > 155*mm:
                width *= 155*mm / height
                height = 155*mm
            picture.drawWidth, picture.drawHeight = width, height
            blocks.append(KeepTogether([Spacer(1, 4*mm), picture, Spacer(1, 2*mm),
                                       Paragraph(markup(caption), sheet['small'])]))
    folder = ROOT / 'submission'
    folder.mkdir(exist_ok=True)
    output = folder / f"{identity['student_id']}_{identity['name']}_과제1.pdf"
    doc = SimpleDocTemplate(str(output), pagesize=A4, rightMargin=20*mm, leftMargin=20*mm,
                            topMargin=20*mm, bottomMargin=20*mm,
                            title='개인 소개 웹사이트 구축 결과 보고서', author=identity['name'])
    doc.build(blocks, onFirstPage=page_number, onLaterPages=page_number)
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
