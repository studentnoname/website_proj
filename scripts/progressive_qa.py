"""Verify readable navigation without JavaScript and system reduced motion."""
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
    parser.add_argument('--output', type=Path, default=ROOT / 'docs/evidence/T08/progressive')
    args = parser.parse_args()
    output = args.output
    output.mkdir(parents=True, exist_ok=True)
    results = []
    version = None
    for mode in ['no-javascript', 'reduced-motion', 'system-default']:
        options = Options()
        options.binary_location = 'C:/Program Files/Mozilla Firefox/firefox.exe'
        profile = ROOT / '.local' / ('firefox-' + mode + '-profile')
        profile.mkdir(exist_ok=True)
        for argument in ['-headless', '-profile', str(profile)]:
            options.add_argument(argument)
        options.set_preference('javascript.enabled', mode != 'no-javascript')
        if mode != 'system-default':
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
            base = args.base_url.rstrip('/') + '/'
            driver.get(base)
            wait = WebDriverWait(driver, 15)
            if mode != 'no-javascript':
                driver.execute_script("localStorage.removeItem('pf-panel-motion')")
                driver.refresh()
            if mode == 'no-javascript':
                links = driver.find_elements(By.CSS_SELECTOR, '[data-pf-nav-link]')
                passed = len(links) == 4 and all(link.is_displayed() for link in links)
                motion_buttons = driver.find_elements(By.CSS_SELECTOR, '[data-pf-motion-toggle]')
                passed = passed and all(not button.is_displayed() for button in motion_buttons)
                enhanced = driver.execute_script("return document.documentElement.classList.contains('js')")
                links[-1].click()
                passed = passed and not enhanced and driver.current_url.endswith('#current')
                results.append({'mode': mode, 'passed': passed, 'menu_links': len(links),
                                'js_enhanced': enhanced, 'url_after_native_click': driver.current_url})
            elif mode == 'reduced-motion':
                state = driver.execute_script('''return {
                  reduced: matchMedia('(prefers-reduced-motion:reduce)').matches,
                  setting: document.documentElement.dataset.pfMotion,
                  panelsNormal: [...document.querySelectorAll('[data-pf-panel]')].every(e=>getComputedStyle(e).position!=='sticky' && getComputedStyle(e).clipPath==='none'),
                  revealsReadable: [...document.querySelectorAll('[data-pf-reveal]')].every(e=>parseFloat(getComputedStyle(e).opacity)>.99),
                  running: [...document.querySelectorAll('body *')].filter(e=>{
                    const s=getComputedStyle(e);return s.animationName!=='none' && s.animationPlayState==='running'
                  }).length};''')
                results.append({'mode': mode, 'passed': state['reduced'] and state['running'] == 0 and
                                state['panelsNormal'] and state['revealsReadable'] and state['setting'] == 'off',
                                'state': state})
            else:
                state = driver.execute_script('''return {
                  reduced:matchMedia('(prefers-reduced-motion:reduce)').matches,
                  setting:document.documentElement.dataset.pfMotion,
                  stored:localStorage.getItem('pf-panel-motion')};''')
                results.append({'mode': mode, 'passed': state['setting'] == ('off' if state['reduced'] else 'on'), 'state':state})
            driver.save_screenshot(str(output / (mode + '.png')))
            if mode == 'reduced-motion':
                for language, suffix in [('ko',''),('en','en/')]:
                    driver.get(base + suffix)
                    driver.execute_script("localStorage.removeItem('pf-panel-motion')")
                    driver.refresh()
                    control = driver.find_element(By.CSS_SELECTOR, '#intro [data-pf-motion-toggle]')
                    rect = control.rect
                    visible = control.is_displayed() and rect['y'] < driver.execute_script('return innerHeight')
                    control.click()
                    wait.until(lambda b: b.execute_script("return document.documentElement.dataset.pfMotion==='on'"))
                    enabled = driver.execute_script('''return {
                      ready:document.querySelectorAll('[data-pf-ready]').length,
                      sticky:getComputedStyle(document.querySelector('[data-pf-panel]')).position,
                      synced:[...document.querySelectorAll('[data-pf-motion-toggle]')].every(e=>e.getAttribute('aria-pressed')==='true'),
                      entrance:document.getAnimations().some(a=>a.effect.target.closest('#intro')),
                      system:matchMedia('(prefers-reduced-motion:reduce)').matches};''')
                    results.append({'mode':language+'-reduced-explicit-enable',
                                    'passed':visible and enabled['ready']==4 and enabled['sticky']=='sticky' and enabled['synced'] and enabled['entrance'] and enabled['system'], 'state':enabled})
                    wait.until(lambda b:b.execute_script("return document.getAnimations().every(a=>a.playState!=='running')"))
                    driver.save_screenshot(str(output / (language+'-explicit-on.png')))
                    driver.execute_script("const t=document.getElementById('about');scrollTo(0,t.offsetTop-innerHeight*.5)")
                    driver.execute_async_script('const done=arguments[0];requestAnimationFrame(()=>requestAnimationFrame(done))')
                    wait.until(lambda b:b.execute_script("return document.getAnimations().every(a=>a.playState!=='running')"))
                    cover = driver.execute_script('''const a=document.querySelector('#intro [data-pf-panel]').getBoundingClientRect(),
                      b=document.querySelector('#about [data-pf-panel]').getBoundingClientRect();
                      return {oldBottom:a.bottom,newTop:b.top,clipped:getComputedStyle(document.querySelector('#about [data-pf-panel]')).clipPath!=='none',
                        oldOwner:document.elementFromPoint(innerWidth*.6,b.top-25)?.closest('[data-pf-panel-track]')?.id,
                        newOwner:document.elementFromPoint(innerWidth*.6,b.top+100)?.closest('[data-pf-panel-track]')?.id};''')
                    results.append({'mode':language+'-reduced-real-cover','passed':cover['oldOwner']=='intro' and cover['newOwner']=='about' and cover['clipped'],'state':cover})
                    driver.save_screenshot(str(output / (language+'-explicit-cover.png')))
                    driver.refresh()
                    persisted = driver.execute_script("return document.documentElement.dataset.pfMotion==='on' && localStorage.getItem('pf-panel-motion')==='on'")
                    results.append({'mode':language+'-explicit-choice-persists','passed':persisted})
                    footer = driver.find_element(By.CSS_SELECTOR, '.site-footer [data-pf-motion-toggle]')
                    footer.send_keys(Keys.ENTER)
                    off = driver.execute_script("return document.documentElement.dataset.pfMotion==='off' && [...document.querySelectorAll('[data-pf-panel]')].every(e=>getComputedStyle(e).position!=='sticky' && getComputedStyle(e).clipPath==='none') && document.getAnimations().every(a=>a.playState!=='running')")
                    results.append({'mode':language+'-keyboard-disable','passed':off})
                driver.execute_script("localStorage.removeItem('pf-panel-motion')")
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
