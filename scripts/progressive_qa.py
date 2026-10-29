"""Verify readable navigation without JavaScript and system reduced motion."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.local/python'))
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service


def main():
    output = ROOT / 'docs/evidence/T08/progressive'
    output.mkdir(parents=True, exist_ok=True)
    results = []
    version = None
    for mode in ['no-javascript', 'reduced-motion']:
        options = Options()
        options.binary_location = 'C:/Program Files/Mozilla Firefox/firefox.exe'
        profile = ROOT / '.local' / ('firefox-' + mode + '-profile')
        profile.mkdir(exist_ok=True)
        for argument in ['-headless', '-profile', str(profile)]:
            options.add_argument(argument)
        options.set_preference('javascript.enabled', mode != 'no-javascript')
        options.set_preference('ui.prefersReducedMotion', 1)
        driver = webdriver.Firefox(options=options, service=Service(
            str(ROOT / '.local/tools/geckodriver/geckodriver.exe'),
            service_args=['--allow-system-access'],
            log_output=str(ROOT / '.local' / ('geckodriver-' + mode + '.log'))))
        try:
            version = driver.capabilities['browserVersion']
            driver.set_window_size(500, 1000)
            driver.set_context('chrome')
            driver.execute_script('''const b=gBrowser.selectedBrowser;
              b.style.setProperty('max-width','390px','important');
              b.style.setProperty('width','390px','important');
              b.style.setProperty('min-width','0px','important');
              b.style.setProperty('flex','0 0 390px','important');
              ZoomManager.setZoomForBrowser(b,1);''')
            driver.set_context('content')
            driver.get('http://127.0.0.1:1313/website_proj/')
            if mode == 'no-javascript':
                links = driver.find_elements(By.CSS_SELECTOR, '[data-pf-nav-link]')
                passed = len(links) == 4 and all(link.is_displayed() for link in links)
                enhanced = driver.execute_script("return document.documentElement.classList.contains('pf-js')")
                links[-1].click()
                passed = passed and not enhanced and driver.current_url.endswith('#current')
                results.append({'mode': mode, 'passed': passed, 'menu_links': len(links),
                                'js_enhanced': enhanced, 'url_after_native_click': driver.current_url})
            else:
                state = driver.execute_script('''return {
                  reduced: matchMedia('(prefers-reduced-motion:reduce)').matches,
                  setting: document.documentElement.dataset.pfMotion,
                  running: [...document.querySelectorAll('svg *')].filter(e=>{
                    const s=getComputedStyle(e);return s.animationName!=='none' && s.animationPlayState==='running'
                  }).length};''')
                results.append({'mode': mode, 'passed': state['reduced'] and state['running'] == 0,
                                'state': state})
            driver.save_screenshot(str(output / (mode + '.png')))
        finally:
            driver.quit()
    report = {'checked_at': datetime.now(timezone(timedelta(hours=9))).isoformat(),
              'browser': 'Firefox', 'version': version, 'passed': all(r['passed'] for r in results),
              'results': results}
    (output / 'results.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if report['passed'] else 1)


if __name__ == '__main__':
    main()
