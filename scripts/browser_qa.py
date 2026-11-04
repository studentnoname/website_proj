"""Exercise the portfolio in a dedicated, headless Firefox profile."""
from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.local/python'))
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base-url', default='http://127.0.0.1:1313/website_proj/')
    parser.add_argument('--output', type=Path, default=ROOT / 'docs/evidence/T08/firefox')
    parser.add_argument('--firefox', default='C:/Program Files/Mozilla Firefox/firefox.exe')
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    profile = ROOT / '.local/firefox-qa-profile'
    profile.mkdir(parents=True, exist_ok=True)
    options = Options()
    options.binary_location = args.firefox
    options.add_argument('-headless')
    options.add_argument('-profile')
    options.add_argument(str(profile))
    options.set_preference('layout.css.devPixelsPerPx', '1.0')
    driver = webdriver.Firefox(options=options, service=Service(
        str(ROOT / '.local/tools/geckodriver/geckodriver.exe'),
        service_args=['--allow-system-access'],
        log_output=str(ROOT / '.local/geckodriver-qa.log')))
    results = []
    wait = WebDriverWait(driver, 15)
    base = args.base_url.rstrip('/') + '/'

    def record(name, passed, **evidence):
        results.append({'name': name, 'passed': bool(passed), **evidence})

    def load(url):
        driver.get(url)
        wait.until(lambda browser: browser.execute_script('return document.readyState') == 'complete')
        wait.until(lambda browser: browser.find_elements(By.CSS_SELECTOR, 'main#main'))
        driver.execute_async_script('const done=arguments[arguments.length-1]; document.fonts.ready.then(()=>done());')
        wait.until(lambda browser: browser.execute_script(
            "return document.getAnimations().every(a=>a.playState !== 'running')"))

    def viewport(width):
        # Windows Firefox's chrome window has a 500px minimum. Resize the dedicated
        # test browser element, as a responsive viewport, and verify content width.
        driver.set_window_size(max(width, 500), 1000)
        driver.set_context('chrome')
        driver.execute_script('''const b=gBrowser.selectedBrowser;
          b.style.setProperty('width',arguments[0]+'px','important');
          b.style.setProperty('max-width',arguments[0]+'px','important');
          b.style.setProperty('min-width','0px','important');
          b.style.setProperty('flex','0 0 '+arguments[0]+'px','important');
          ZoomManager.setZoomForBrowser(b,1);''', width)
        driver.set_context('content')
        wait.until(lambda browser: browser.execute_script('return innerWidth') == width)

    def screen(name):
        file = args.output / (name + '.png')
        driver.save_screenshot(str(file))
        return file.relative_to(ROOT).as_posix() if file.is_relative_to(ROOT) else str(file)

    def anchor_position(section):
        return driver.execute_script('''const section=document.getElementById(arguments[0]);
          const heading=section.querySelector('h2') || section.querySelector('h1');
          const h=heading.getBoundingClientRect();
          const header=document.querySelector('.site-header').getBoundingClientRect();
          return {headingTop:h.top,headingBottom:h.bottom,headerBottom:header.bottom,
            viewportHeight:innerHeight,visible:h.top>=header.bottom-1 && h.bottom<=innerHeight};''', section)

    try:
        type_at_width = {}
        for language, suffix in [('ko', ''), ('en', 'en/')]:
            for width in (1440, 900, 768, 390):
                viewport(width)
                load(base + suffix)
                metrics = driver.execute_script('''return {
                  width: innerWidth, contentWidth: document.documentElement.scrollWidth,
                  lang: document.documentElement.lang,
                  h1: document.querySelector('h1')?.textContent.trim(),
                  badImages: [...document.images].filter(i => !i.complete || !i.naturalWidth).length,
                  fontsReady: document.fonts.status,
                  loadedFonts: [...document.fonts].filter(f=>f.status==='loaded').map(f=>({family:f.family,weight:f.weight})),
                  clippedText: [...document.querySelectorAll('[data-copy],h1,h2,h3')].filter(e=>{
                    const range=document.createRange();range.selectNodeContents(e);
                    return [...range.getClientRects()].some(r=>r.left < -1 || r.right > innerWidth + 1);
                  }).map(e=>e.textContent.trim().slice(0,80))
                }''')
                record(f'{language}-{width}-layout', metrics['width'] == width and
                       metrics['contentWidth'] <= width + 1 and metrics['badImages'] == 0 and not metrics['clippedText'] and
                       metrics['lang'].lower().startswith(language),
                       url=driver.current_url, metrics=metrics, screenshot=screen(f'{language}-{width}'))
                if width in (1440, 390):
                    # Inspect the complete composition as well as individual folds.
                    driver.get_full_page_screenshot_as_file(str(
                        ROOT / '.local' / f'composition-{language}-{width}.png'))
                typography = driver.execute_script('''return {
                  copy: [...document.querySelectorAll('[data-copy]')].map(e=>{
                    const s=getComputedStyle(e); return {size:parseFloat(s.fontSize),leading:parseFloat(s.lineHeight)};
                  }),
                  headings: [...document.querySelectorAll('[data-pf-section] h2')].map(e=>parseFloat(getComputedStyle(e).fontSize)),
                  headingEdges: [...document.querySelectorAll('[data-pf-section] h2')].map(e=>e.getBoundingClientRect().left),
                  collisions: [...document.querySelectorAll('[data-pf-section]')].filter(section=>{
                    const h=section.querySelector('h2'),p=section.querySelector('[data-copy]');
                    if(!h||!p)return false;
                    const a=h.getBoundingClientRect(),b=p.getBoundingClientRect();
                    return Math.min(a.right,b.right)-Math.max(a.left,b.left)>1 &&
                           Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top)>1;
                  }).map(e=>e.id)
                }''')
                body_size = typography['copy'][0]['size'] if typography['copy'] else 0
                body_leading = typography['copy'][0]['leading'] if typography['copy'] else 0
                readable_body = body_size in (16, 18) and (width != 1440 or body_size == 18) and (width != 390 or body_size == 16)
                uniform_copy = len(typography['copy']) >= 12 and all(
                    abs(row['size'] - body_size) < .1 and abs(row['leading'] - body_leading) < .1
                    for row in typography['copy']) and body_size*1.6 <= body_leading <= body_size*1.9
                headings = typography['headings']
                uniform_headings = len(headings) == 3 and max(headings)-min(headings) < .1 and min(headings) >= body_size*1.5 and max(headings) <= 64
                signature = [body_size, body_leading, *headings]
                if language == 'ko':
                    type_at_width[width] = signature
                matching_language = width in type_at_width and len(signature) == len(type_at_width[width]) and all(
                    abs(a-b) < .1 for a,b in zip(signature,type_at_width[width]))
                record(f'{language}-{width}-type-hierarchy', readable_body and uniform_copy and uniform_headings and matching_language,
                       body_size=body_size, evidence=typography)
                edges = typography['headingEdges']
                aligned = len(edges) == 3 and max(edges)-min(edges) < 1 and not typography['collisions']
                record(f'{language}-{width}-section-alignment', aligned,
                       headings=edges, heading_copy_collisions=typography['collisions'])

        viewport(390)
        load(base)
        toggle = driver.find_element(By.CSS_SELECTOR, '[data-pf-nav-toggle]')
        toggle.click()
        record('mobile-menu-opens', toggle.get_attribute('aria-expanded') == 'true')
        toggle.send_keys(Keys.ESCAPE)
        record('mobile-escape-restores-focus', toggle.get_attribute('aria-expanded') == 'false' and
               driver.execute_script('return document.activeElement === arguments[0]', toggle))
        toggle.click()
        link = driver.find_element(By.CSS_SELECTOR, '[data-pf-nav-link][href="#current"]')
        link.click()
        record('mobile-menu-selects-section', driver.current_url.endswith('#current') and
               toggle.get_attribute('aria-expanded') == 'false', screenshot=screen('ko-mobile-current'))
        driver.find_element(By.CSS_SELECTOR, '[data-pf-lang]').click()
        wait.until(lambda browser: '/en/' in browser.current_url)
        record('language-keeps-anchor', driver.current_url.endswith('/en/#current') and
               driver.execute_script('return document.documentElement.lang').lower().startswith('en'))

        viewport(1440)
        viewport(390)
        viewport(1440)
        nav = driver.find_element(By.CSS_SELECTOR, '[data-pf-nav-link][href="#about"]')
        record('resize-restores-desktop-navigation', nav.is_displayed())

        load(base + '#about')
        driver.refresh()
        wait.until(lambda browser: browser.find_element(By.ID, 'about').is_displayed())
        record('deep-anchor-refresh', driver.current_url.endswith('#about'))
        driver.find_element(By.CSS_SELECTOR, '[data-pf-nav-link][href="#current"]').click()
        driver.back()
        wait.until(lambda browser: browser.current_url.endswith('#about'))
        record('anchor-back-navigation', driver.current_url.endswith('#about'))

        load(base)
        body = driver.find_element(By.TAG_NAME, 'body')
        body.send_keys(Keys.TAB)
        focus = driver.execute_script('''const e=document.activeElement;const s=getComputedStyle(e);
          return {tag:e.tagName,href:e.getAttribute('href'),outline:s.outlineStyle,
          outlineWidth:s.outlineWidth,boxShadow:s.boxShadow};''')
        record('keyboard-focus-visible', focus['tag'] in ('A', 'BUTTON') and
               (focus['outline'] != 'none' or focus['boxShadow'] != 'none'), evidence=focus,
               screenshot=screen('keyboard-focus'))
        driver.switch_to.active_element.send_keys(Keys.ENTER)
        record('keyboard-activates-skip-link', driver.current_url.endswith('#main') and
               driver.execute_script('return document.activeElement.id') == 'main')

        load(base)
        before = driver.execute_script('return {width:innerWidth,dpr:devicePixelRatio}')
        driver.set_context('chrome')
        driver.execute_script('ZoomManager.setZoomForBrowser(gBrowser.selectedBrowser,2);')
        driver.set_context('content')
        after = driver.execute_script('return {width:innerWidth,dpr:devicePixelRatio,scroll:document.documentElement.scrollWidth}')
        zoom = round(after['dpr'] / before['dpr'], 2)
        record('browser-200-percent-zoom', zoom == 2 and after['scroll'] <= after['width'] + 1,
               before=before, after=after, ratio=zoom, screenshot=screen('ko-200-percent'))
        driver.set_context('chrome')
        driver.execute_script('ZoomManager.setZoomForBrowser(gBrowser.selectedBrowser,1);')
        driver.set_context('content')

        for section in ('about', 'future', 'current'):
            load(base + '#' + section)
            position = anchor_position(section)
            record(f'anchor-{section}-visible', position['visible'], position=position,
                   screenshot=screen('ko-desktop-' + section))

        viewport(390)
        for section in ('about', 'future', 'current'):
            load(base + '#' + section)
            position = anchor_position(section)
            record(f'mobile-anchor-{section}-visible', position['visible'], position=position,
                   screenshot=screen('ko-mobile-' + section))

        motion = driver.find_elements(By.CSS_SELECTOR, '[data-pf-motion-toggle]')
        if motion and motion[0].is_displayed():
            previous = motion[0].get_attribute('aria-pressed')
            motion[0].click()
            record('motion-control', motion[0].get_attribute('aria-pressed') != previous,
                   previous=previous, current=motion[0].get_attribute('aria-pressed'))
        else:
            record('motion-control', True, note='No visible automatic-motion control; inspect CSS reduced-motion rule separately.')
    except Exception as error:
        record('unexpected-test-error', False, error=f'{type(error).__name__}: {error}',
               url=driver.current_url)
    finally:
        report = {'checked_at': datetime.now(timezone(timedelta(hours=9))).isoformat(),
                  'browser': driver.capabilities['browserName'],
                  'browser_version': driver.capabilities['browserVersion'], 'base_url': base,
                  'passed': bool(results) and all(row['passed'] for row in results), 'results': results}
        (args.output / 'results.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        driver.quit()
    print(json.dumps({'passed': report['passed'], 'checks': len(results),
                      'failures': [r for r in results if not r['passed']]}, ensure_ascii=False, indent=2))
    raise SystemExit(0 if report['passed'] else 1)


if __name__ == '__main__':
    main()
