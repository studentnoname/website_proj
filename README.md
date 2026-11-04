# Jung Jiwoong — 개인 포트폴리오

HugoBlox Academic CV의 빌드 환경에서 동작하는 한국어·영어 단일 페이지 포트폴리오다. 기존 `layouts`, `assets/css`, `assets/js` 폴더를 재사용하며, 화면·공통 스타일·동작을 나누어 관리한다.

- 사이트: https://studentnoname.github.io/website_proj/
- English: https://studentnoname.github.io/website_proj/en/
- 소스: https://github.com/studentnoname/website_proj
- 배포: https://github.com/studentnoname/website_proj/actions/workflows/hugo-pages.yml

## 설치와 실행

빌드 기준: Python 3.12, Node 24, Hugo 0.167.0 **Extended**, Go 1.27.1, Dart Sass 1.105.0. 원본 Download ZIP을 제공 준비 스크립트 3.1로 준비했다.

Windows 프로젝트 루트:

```powershell
python scripts/bootstrap_windows.py
.\scripts\build.ps1 -InstallDependencies
python scripts/serve.py
```

미리보기: http://127.0.0.1:1313/website_proj/

bootstrap은 공식 파일의 SHA-256을 확인하고 `.local/tools/`에만 설치한다. 전역 PATH와 상위 저장소 설정은 바꾸지 않는다. Python·Node는 먼저 설치한다. 의존성이 바뀌지 않았다면 이후 `-InstallDependencies`를 생략한다.

다른 환경은 기준 도구를 PATH에 준비한 뒤 CI와 같은 진입점을 사용한다.

```text
python .github/pages_build.py --dependencies
python .github/pages_build.py --build
python scripts/serve.py
```

산출물은 `public/`이다. 이전 출력을 정리하고 `/website_proj/` 경로를 보정한다. 일반 `hugo` 명령만 실행하면 운영 `pages.json`이 빠질 수 있다. 개인화 이후 준비 스크립트를 다시 실행해 사이트를 덮어쓰지 않는다.

## 수정할 위치

| 내용 | 파일 |
| --- | --- |
| 화면·두 언어 본문 | `site/layouts/landing/list.html` |
| 공통 글자 크기·정렬·강조 규칙 | `site/assets/css/portfolio.css` |
| 메뉴·언어 전환 동작 | `site/assets/js/portfolio.js` |
| 한국어·영어 메뉴 | `site/config/_default/menus.ko.yaml`, `menus.en.yaml` |
| 메인 이미지 | `site/static/media/resolve-hero.png` |
| 언어 설정 | `site/config/_default/languages.yaml` |
| 홈 메타 정보 | `site/content/ko/_index.md`, `site/content/en/_index.md` |
| 운영 설정 | `site/pages.json`, `site/config/_default/hugo.yaml`, `params.yaml` |

앵커는 `#intro`, `#about`, `#future`, `#current`다. 두 언어의 사실을 함께 수정한다. 사용자가 비워 두도록 한 다음 학습 행동, 미확인 도구별 기능, 없는 KONNECT 산출물을 임의로 채우지 않는다.

본문은 PC 18px·모바일 16px, 줄간격 1.75를 공통으로 사용한다. 제목·설명의 시작선은 공유하고, 아래 내용은 소개의 도구 목록, 학습 분야의 세 열, KONNECT의 전폭 작업 흐름으로 구성한다. 큰 타이포는 첫 화면에 사용하며, 도구 목록은 동등하게 표시한다.

이전 디자인은 `archive/portfolio-v1` 브랜치에 보존했다. 사용하지 않는 원본 예제·모듈 소스와 이전 화면 조각을 제거했다. Hugo 모듈 의존성과 Pages 빌드 설정은 유지한다. `docs/`의 이전 작업 기록은 당시 결과를 기록한 자료이며, 현재 화면의 편집 파일이 아니다.

## 검증

```text
python scripts/check_site.py
python -m pip install --target .local/python -r scripts/requirements-qa.txt
python scripts/browser_qa.py
python scripts/progressive_qa.py
```

브라우저 검사는 미리보기 서버, Windows Firefox, `.local/tools/geckodriver/geckodriver.exe`가 필요하다. 드라이버 공식 배포: https://github.com/mozilla/geckodriver/releases/tag/v0.37.1

사용자 기본 프로필 대신 `.local/` 검사 프로필을 사용한다. 390px는 실제 콘텐츠 뷰포트, 200%는 브라우저 확대·DPR로 확인한다. JavaScript 없는 이동과 reduced-motion도 별도 검사한다. [검증 기록](docs/verification.md), [TASK 기록](docs/tasks/)에 실제 결과와 한계를 적었다.

## 수정과 재배포

1. 작업 브랜치에서 실제 변경·관련 검사·기록을 커밋한다.
2. 빌드와 검사를 마치면 이력을 유지해 main에 통합하고 `git push origin main`한다.
3. 해당 SHA의 Actions build·deploy 성공을 확인한다.
4. 공개 한국어·영어 주소에서 실제 변경과 자산 URL을 확인한다.

Settings → Pages의 Source는 **GitHub Actions**다. 수동 실행만으로 main push 자동 배포를 대신하지 않는다. 버전·워크플로는 `.github/workflows/hugo-pages.yml`을 참조한다.

## 출처·기록·제출

[출처](docs/sources.md), [AI 활용](docs/ai/usage.md), [이력 집계](docs/commit-log.md), [커밋 정책](docs/handbook/COMMIT_POLICY.md)을 관리한다. `LICENSE.md`와 모듈 라이선스·공개 HugoBlox 제작 고지는 보존한다. 원본 README는 `docs/handbook/HUGOBLOX_README.md`에 보존했다.

원본: https://themes.gohugo.io/themes/blox-tailwind/ · https://github.com/HugoBlox/kit

최종 main push 성공 후 `python scripts/collect_release.py`로 SHA·Actions·커밋 포함·제외 근거를 로컬 `submission/release.json`에 내보낸다. TASK PDF는 `python scripts/render_records.py --tasks`로 생성한다. 제출 PDF는 `--release`와 로컬 `--identity` 파일을 지정해 생성한다. 제출 개인정보와 최종 파일은 공개 Git에 포함하지 않는다.
