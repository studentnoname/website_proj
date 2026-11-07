# 출처와 이용 조건

## 보고서 문장 개선 스킬

- Cheng-I Wu, Academic Research Skills 3.24.2 / academic-paper. CC BY-NC 4.0. 고정 원본: https://github.com/Imbad0202/academic-research-skills/blob/6d9388674de1ad0437ad95db3d52f92b92204d84/academic-paper/SKILL.md .
- 2026-11-06 실제 Claude Code에 적용했다. 과제 채점 기준을 우선해 문장의 명료성·정확성·근거 대조와 관련 항목 묶기에 사용했다. 논문용 기본 서식이나 전체 연구 파이프라인은 적용하지 않았다. 실제 요청·반영·검증 범위는 ai/usage.md와 현재 보고서 7절 사례 3에 구분한다.

## 테마와 빌드

- Hugo Themes 선택 페이지: https://themes.gohugo.io/themes/blox-tailwind/
- 실제 원본 저장소: https://github.com/HugoBlox/kit
- Download ZIP: https://codeload.github.com/HugoBlox/kit/zip/refs/heads/main
- 다운로드·식별: 2026-10-29 KST. SHA-256과 원본 도구 다운로드는 `evidence/T01/downloads.json` 참조.
- 기반 예제: `templates/academic-cv`, 준비된 실제 사이트는 `site/`.
- 원본 이용 조건: 루트 `LICENSE.md`와 모듈 내부 라이선스를 보존했다. 공개 화면에는 HugoBlox 제작 고지를 유지한다.
- 제공 준비 스크립트: 과제 제공 `prepare_github_pages.py` 3.1. inputs 원본은 로컬 인계 폴더에 보존하고 실행 사본의 npm 도구 설치 격리만 수정했다. 수정 근거는 I002.

## 공개 정보와 시각 자료

- 이름·관심·활동 과정: 사용자 제공 인계 내용과 2026-10-29의 추가 답변. 확인 결정은 `content-decisions.md` 참조.
- 직접 확인·작업 결과: 2026-11-07 답변으로 사이트·PDF의 지속적인 직접 확인, 노트북·아이폰/Chrome·Safari의 관찰·수정·재확인과 KONNECT 라이브러리 업데이트 판단·이후 개발 결과를 보완하였음. 실제 원문은 `ai/usage.md`, 공개 작업 기록은 `tasks/T03.md`에 보존하였음.
- 기존 발표 사진: 맥락과 공개 범위가 확인되지 않아 사이트에 사용하지 않는다.
- 제공 hub 링크: 본인 KONNECT 활동과 관계가 확인되지 않아 활동 결과 근거에 사용하지 않는다.
- 원본 데모 인물·경력·논문·다운로드 자료: 개인 콘텐츠로 게시하지 않는다.
- 신규 SVG 도형·스타일·번역: Claude를 이용한 구현 결과는 실제 반영 경로와 검증을 `ai/`에 기록한다. 외부 사진을 본인 활동 자료처럼 사용하지 않는다.
- 2026-11-04 초기 물결 장식 시도는 사용자의 설명에 따라 제거했다. 현재는 Claude가 기존 HTML·CSS·JavaScript에 작성한 순차 등장과 화면 겹침이며, SVG clipPath는 다음 패널 자체의 위쪽을 곡선으로 표시한다. 외부 이미지·애니메이션 라이브러리를 추가하지 않는다. KONNECT의 실제 산출물이나 측정값을 표현하지 않는다. Codex가 실제 화면·입력·모션 축소를 검사했다.

## 재제작 메인 이미지

- 파일: `site/static/media/resolve-hero.png` (1122 × 1402 PNG).
- 2026-10-29, 내장 imagegen 도구의 신규 생성 모드로 제작한 장식용 추상 조형이다. 본인 활동이나 KONNECT 결과를 촬영한 이미지가 아니다.
- 프롬프트: “Create a premium 3D abstract sculpture image for a personal developer portfolio hero, portrait 4:5 composition, high resolution. One large continuous sculptural looping ribbon that twists into an open knot, symbolizing persistence and finding a way through. Beautifully art-directed photorealistic CGI: polished liquid chrome edges, softly frosted translucent glass body, pale electric chartreuse light glowing through a few curved inner surfaces, detailed specular reflections. Asymmetric dynamic ascending loop, sophisticated gallery/product photography with a subtle tangible pedestal shadow. Center the sculpture with generous breathing room, occupying about 80% of canvas, and keep the complete silhouette inside frame. Background and ground are an almost-black charcoal green #101311, seamless dark studio with no obvious horizon, cinematic softbox lighting, bright silver highlights and restrained lime #dcff75 accents. The subject should feel physically rich, expensive and dimensional, not a generic AI brain, not wires, not a network diagram, not a flat thin-line illustration. No text, letters, numbers, logo, watermark, user interface, or border. This is a finished website raster artwork, not a website mockup.”

## 기술 참고

- GitHub Pages API 설정: https://docs.github.com/en/rest/pages/pages
- Hugo 공식 빌드 도구: https://github.com/gohugoio/hugo/releases/tag/v0.167.0
- Go 공식 배포: https://go.dev/dl/
- Sass 공식 배포: https://github.com/sass/dart-sass/releases/tag/1.105.0
- Firefox 검사 드라이버: https://github.com/mozilla/geckodriver/releases/tag/v0.37.1

페이지 내용과 동작의 최종 근거는 해당 커밋의 실제 빌드·공개 화면·검사 결과다. 원본 도구의 검증 카탈로그를 현재 사이트의 통과 결과로 대체하지 않는다.
