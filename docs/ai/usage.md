# 실제 AI 활용 기록

## 2026-11-05 실제 처리 방식과 중간 기록 설명

사용자는 다음 학습 행동으로 ‘도움 요청 API의 정상·입력 오류·권한 오류 테스트를 작성하고 결과 정리’를 선택했다. Claude Code(claude-opus-5-5)에 “This is a FUTURE learning action, not tests he has already completed”라고 구분하고 #future의 목표·다음 행동만 추가하도록 요청했다. 기존 tool-rail 배치를 재사용하고 기존 CSS에 학습 분야와의 간격 한 줄만 추가했다. Codex는 선택하지 않은 SQL 안·미제공 날짜·완료 실적이 들어가지 않았는지 검토한다.

사용자 원문: “지금 어떻게 한다고 추상적으로 나와있지 어떤 방식으로 어떤것을 어떻게 한다고 안나와있어서 이것을 조금더 자세하게 설명할 수 있도록 하고 빈칸을 채우려고해”. Codex는 비공개 도움 서비스·DTO·통합 테스트와 기존 검증 문서를 읽어 정상 등록→답변→해결, 400/401/403 조건, PostgreSQL 트랜잭션을 대조했다. 새 KONNECT 테스트는 실행하지 않았다.

실제 Claude Code CLI(claude-opus-5-5) 요청은 “Replace vague labels with a short bold title then br and a concise explanation in each existing p”와 “Do not edit #future yet: a real next learning action is awaiting his answer”이다. Claude는 기존 HTML에서 네 단계 설명·상태·중간 기록 링크를 작성하고 미검사임을 밝혔다. Codex는 영어의 처리 순서 오해를 줄이고 중간 기록 소개를 간결하게 정리했으며 링크를 설명과 같은 열에 묶었다. 원본 코드·민감값을 전달하거나 공개하지 않았다. 반영 파일은 기존 site/layouts/landing/list.html과 docs/tasks/T03.md다.

## 2026-11-05 채점 위험 보완

후속 실제 관찰: 사용자가 Desktop konnect를 지정한 뒤 Codex가 백엔드의 도움 요청·답변 Controller/Service/DTO, 통합 테스트, 기존 로컬 검증 문서를 읽었다. Claude Code(claude-opus-5-5)에 “Change ONLY the single existing paragraph under .lesson-note”와 “Those sources confirm work on help request/answer APIs, input and access-permission checks, and existing local DB/HTTP test records”로 한 문단의 두 언어 요약을 요청했다. 비공개 코드·운영 로그·개인정보·상세 보안 조사 내용은 전달하거나 공개하지 않았다. 이번 KONNECT 실행 검증·배포가 아니라 읽기 검토이며, 사이트에서는 작업 범주와 로컬 검증 방식을 설명한다.

사용자의 후속 답변으로 목적과 검증 이유가 확정되어 Claude Code에 기존 KONNECT 소개·마지막 작업 단계·작업 방식 문단만 보완하도록 요청했다. 실제 입력: “Confirmed purpose: international students need help; other users who have relevant experience share their experiences to help resolve those needs.” / “this is a web application connected to a live server, so he tests locally before deploying to check the integration.” 새 기능·성과·특정 도구 선택 이유를 만들지 않도록 제한했고 Codex가 원문과 대조한다. KONNECT 코드 직접 관찰은 경로 확인 전 미수행이다.

사용자의 “우선순위대로 해결”에 따라 Codex가 404 경로 보정과 보고서 증거 연결을 맡았다. 프론트 P77 문구는 Claude Code 2.1.287(claude-opus-5-5)로 기존 lesson 문단만 작성하도록 요청했다. 실제 입력 발췌는 “Clarify the existing first paragraph of .lesson-body by explicitly connecting those known facts”와 “Do NOT change the vague platform purpose (P75): the user's specific problem/feature answer is still pending”이다. Claude는 직접 검증의 목적을 설명하는 두 언어 문장을 작성하고 미검사임을 밝혔다. Codex는 중복과 어색한 영어를 줄이고 확인된 사실 범위를 검토했다. 반영 파일은 site/layouts/landing/list.html이다. 새 활동·성과·기능·다음 학습 행동을 만들지 않았다. 실제 빌드·홈과 404 정적 검사 및 배포 후 브라우저 검사로 확인한다.

## 사례 G — 글 순차 등장과 화면 전체 전환

- 2026-11-04 KST, Claude Code 2.1.287, 실제 modelUsage: claude-opus-5-5. 사용자 요청은 이전 시도를 되돌리고 접속 시 글이 하나씩 들어오며 스크롤 시 다음 화면이 이전 화면을 덮도록 하라는 설명이었다. 실제 발췌는 `prompts/frontend.md`.
- Claude는 기존 HTML·CSS·JS 세 파일에 normal-flow 앵커와 sticky 패널, 전체 패널의 곡선 clip, 640ms·80ms 지연 등장, 키보드와 효과 제어를 작성했다. 빌드·실제 브라우저 검사는 하지 않았다고 명시했다. 철회한 자료를 참고하지 않았다.
- 판단: 단순 물결 장식은 제거하고 섹션의 배경·글 전체가 겹치는 방식을 채택했다. 짧은 섹션은 기존 높이를 유지하고 긴 섹션은 읽은 후 고정한다. Codex는 원래 배치를 유지하는 판단을 받아들이고 I011에서 짧은 패널을 모두 뷰포트 높이로 보던 검사와 첫 프레임 이전 startTime 검사를 고쳤다.
- 검증: 55개 Firefox 검사와 별도 2개 검사에서 실제 화면 hit-test·고정 좌표·앞 패널 이동·clip 경로·등장 시각·키보드·일반 흐름 복원·깊은 링크를 확인했다. `../verification.md`와 I011에 연결한다. Codex의 검토를 사용자의 직접 코드 검토라고 기록하지 않는다. 실제 Safari/iPhone은 미검사다.

## 사례 F — 사용자 요청에 따른 스크롤 물결

- 날짜: 2026-11-04 KST. 도구: Claude Code 2.1.287, 실제 modelUsage는 claude-opus-5-5. 프론트 선호에 따라 Claude가 기존 HTML·CSS·JS 세 파일을 수정하고 Codex가 검토·빌드·검증했다.
- 사용자 요청 원문: “웹사이트 스크롤 하면서 애니매이션을 추가 물이 흐르는 것처럼”. 실제 CLI 요청 발췌는 `prompts/frontend.md`에 보존했다. 이번 작업은 사용자가 철회한 자료를 참고하지 않았다.
- 응답 요약: 기존 색상으로 세 층의 물결을 두 섹션 경계에 배치하고, SVG 경로를 스크롤 위치와 짧은 관성으로 변형했다. 하단 효과 버튼·localStorage 선택·시스템 모션 축소와 비활성 탭 처리를 추가했다. Claude는 빌드·브라우저 검사를 하지 않았다고 명시했다.
- 채택·수정 판단: 본문을 숨기거나 흐리게 하지 않는 방식과 기본 스크롤 유지를 채택했다. Codex는 I010의 `data-on` 문자열 인용 문제를 발견하고 `data-enabled-label`로 고쳤다. 이는 사용자의 직접 코드 검토로 기록하지 않는다.
- 실제 반영: `site/layouts/landing/list.html`, `site/assets/css/portfolio.css`, `site/assets/js/portfolio.js`. 검사 코드는 기존 `scripts/browser_qa.py`, `scripts/progressive_qa.py`에서 확장했다. 화면·실제 동작·한계는 `../verification.md`와 I010에 연결한다.

## 사례 A — 구조 점검과 개발 계획

- 도구: Codex, 모델명 미표시.
- 날짜: 2026-10-28 KST.
- 사용자 실제 요청: “해당 파일구조를 읽고 어떻게 작업을 해야할지 계획을 수립”.
- 응답 요약: 웹사이트 구현 소스가 아닌 인계 묶음임을 확인하고, 상위 basicproj 저장소를 참조하는 문제와 준비 도구·TASK 완료 조건을 구분했다.
- 반영 위치: `WORK_PLAN.md`, 이후 `docs/tasks/T01.md`와 환경·빌드 도구.
- 검토: 과거 기록의 접근 불가·Claude 미설치를 현재 사실로 재사용하지 않고 로컬 도구·Git·원격 refs를 다시 점검했다.
- 직접 실행 근거: `docs/evidence/T01/`, T01의 실제 기본 빌드와 T07의 최초 main push 배포.
- 한계: 계획 수립 시점에는 사이트 구현·빌드·배포를 수행하지 않았다. 계획 파일만으로 완료를 주장하지 않는다.

## 사례 F — 기본 모션 설정에서 보이지 않는 효과 수정

- 2026-11-04 KST, Claude Code 2.1.287, 실제 모델 claude-opus-5-5. 사용자 원문: “동일한데 변한게 없어”. Codex는 강제 모션 설정이 없는 Firefox에서 reduced=true·사이트 효과 off를 확인했다(I013). Windows 브라우저의 직접 UI 확인은 URL 정책 미지원으로 중단됐고 별도 자동화 프로필로 확인했다.
- 실제 CLI 입력 발췌: “Respect system reduced motion by default, but allow EXPLICIT site-level opt-in” / “Factor hero entrance into reusable function”. 기존 세 프론트 파일만 수정하도록 제한했다. 응답은 첫 화면·하단 제어 동기화, 사이트 내 명시적 켜기, 850ms·120ms 등장 재생을 구현하고 미검사임을 밝혔다.
- Codex가 diff·한국어 문구를 검토하고 Hugo 빌드·정적 검사·기존 Firefox 55개 검사·점진적 향상 11개 검사를 수행했다. 기본 모션 설정을 강제로 바꾸지 않는 검사와 두 언어의 실제 겹침을 추가했다. 기기 설정은 변경하지 않았다. 사용자의 디자인 만족이나 실제 iPhone 검증으로 기록하지 않는다.

## 사례 G — #intro 진입과 명시적 재생 링크

- 2026-11-04 KST, Claude Code 2.1.287, claude-opus-5-5. 사용자 원문 “똑같아”. Codex가 효과 on 상태의 루트·#intro 첫 진입을 비교해 애니메이션 7개·0개를 확인했다(I014). 사용자 주소는 아직 미확인이다.
- 실제 CLI 입력: “Treat initial #intro as first-screen entrance” / “Add explicit preview URL support ?motion=on”. 기존 JS만 수정하도록 제한했다. Claude는 수정 내용을 설명하고 미검사임을 밝혔다. Codex가 build와 정적 검사, 두 언어 진입·새로고침·선택 유지 검사를 수행했다. 실제 결과는 progressive/results.json에 보존한다. 새 framework·폴더·콘텐츠는 추가하지 않았다.

## 사례 H — 투명도와 유동적인 추종 움직임

- 사용자 실제 확인: “화면 효과 켜니까 잘 보이네 다만 불투명도와 애니메이션의 자연스러움을 추가해서 물처럼 흐르는 것으로 만들어줘”. 2026-11-04 KST, Claude Code 2.1.287, claude-opus-5-5.
- 실제 CLI 입력 발췌: “Incoming COMPLETE panel briefly translucent” / “Add restrained, finite liquid FOLLOW-THROUGH on actual incoming panel position + curve after native scroll.” 기존 CSS·JS만 편집하도록 제한했다. Claude는 0.88→1의 전체 패널 불투명도, 넓은 한 곡선, 짧게 따라오다 가라앉는 이동, 최대 320ms 후 정지, 900ms 첫 글 등장을 구현하고 미검사라고 밝혔다.
- Codex는 기존 겹침·메뉴·모션 제어 검사에 PC·모바일의 실제 불투명도와 아래/위 방향의 잔여 이동·정지를 추가했다. 사용자가 기본 효과의 작동을 확인한 것과 이번 부드러움에 대한 만족 여부는 구분한다. 본문·활동·다음 행동은 수정하지 않는다.

## 사례 B — HugoBlox 프론트 구현

- 도구: Claude Code 2.1.287, 실제 응답의 modelUsage: claude-opus-5-5.
- 날짜: 2026-10-29 KST.
- 실제 구현 요청 전문: `prompts/frontend.md`.
- 사용자 실제 지시: “작업시작”. 콘텐츠 후속 답변은 `../content-decisions.md`.
- 목적: HugoBlox 기반 한국어·영어 소개 화면, 메뉴·반응형·접근성 구현.
- 핵심 제약: 기존 테마 baseof와 head·라이선스 고지 유지, 사실 확인된 주장만 사용, 공개 산출물 링크와 다음 학습 행동을 만들지 않기.
- 응답 요약: 네 섹션·언어별 데이터·SVG·메뉴·움직임 제어를 실제 작성했다. 셸 없이 작성했으므로 빌드·브라우저 검증은 수행하지 않았다고 명시했다.
- 실제 반영: `site/data/portfolio/`, `site/content/{ko,en}/`, `site/layouts/_partials/portfolio/`, navbar·footer·assets hook, `site/assets/{css,js}/portfolio.*`.
- Codex 판단·수정: 초기 home override는 landing type에 적용되지 않아 I005로 수정했다. 제거할 수 없었던 데모 CV·사진은 I006에서 제거했고, 실제 화면의 반투명 헤더는 I008에서 개선했다. 사용자가 선택하지 않은 기본 콘텐츠 라이선스는 자동 적용하지 않았다.
- 직접 검증: 정적 HTML 두 언어 통과와 Firefox 159.0의 20개 배치·조작 검사. 전후는 `../evidence/T08/static-first.json`, `static-fixed.json`, `firefox/results.json`과 이슈 문서로 확인한다.
- 사용자 판단: 최종 화면·번역·AI가 만든 표현에 대한 사용자 검토는 아직 받지 않았다. Codex의 코드 검토를 사용자의 판단으로 대신 기록하지 않는다.

## 사례 C — 사용자 피드백에 따른 재제작

- 사용자 요청: 결과와 복잡한 파일 구성에 대한 불만 이후 “다시 제작해”. 이전 결과는 `archive/portfolio-v1`에 보존했다.
- 실제 도구: Claude Code CLI로 `site/layouts/landing/list.html`을 새로 작성하고 Codex가 검토·수정했다. 한국어·영어 HTML, CSS, 메뉴 동작을 이 파일 하나에 모았다. 별도 imagegen 도구로 생성한 메인 이미지의 프롬프트와 경로는 `../sources.md`에 기록했다.
- 변경: 어두운 메인 화면, 라임 색상, 큰 타이포, 입체 이미지, 밝은 소개·학습 영역, KONNECT 활동 영역으로 다시 구성했다. 사용하지 않는 원본 예제·모듈 소스와 이전 화면 조각을 제거했다. Hugo 빌드·모듈 의존성·라이선스는 유지한다.
- 검토 수정: 공개 이름은 Jung Jiwoong으로 유지하고 제출용 개인정보를 제외했다. 프론트 기능의 틀 구성이라는 사실을 보존하고, 계획 설명을 사용자 답변 범위로 정리했다. 화면에서 발견한 CSS 구분자 경로 치환을 수정했다.
- 검증: 새 화면을 Firefox에서 PC·태블릿·모바일 크기로 캡처하여 직접 확인했다. 두 언어 빌드와 정적 참조, 메뉴·앵커·언어 전환·키보드·확대 검사를 수행한다. 기존 사례 B의 경로와 화면은 이전 디자인의 이력이다.

## 사례 D — 본문 체계와 기존 폴더 재사용

- 사용자 확인: 한 HTML로 합치는 것이 목적이 아니라 기존 폴더와 코드를 재사용하라는 뜻이었다. 본문 크기·배치의 일관성과 강조 단계도 다시 요청했다.
- Claude Code CLI가 기존 경로의 화면·공통 CSS·JS 세 파일을 작성하고 Codex가 검토했다. 새 기능별 폴더는 만들지 않았다. 메뉴는 기존 언어별 설정을 읽도록 연결했다.
- 공통 기준: 본문 18px/모바일 16px, 줄간격 1.75. 섹션 제목 48px/36px, 하위 제목 22px/20px, 보조 정보 13px. 세 본문 섹션은 같은 열 구조·간격·시작선을 사용한다. 도구명은 동등하게 표시하고, 라임 강조는 첫 화면 문구·주요 버튼·백엔드 역할에 제한했다.
- Codex 수정: 버튼의 늘어나는 높이, 제목과 본문의 세로 시작선, 모바일 도구 줄바꿈을 조정했다. 설명에 있던 완벽주의 조절은 이미 달성한 성과로 표현하지 않았다.
- 검증은 기존 브라우저 검사에 실제 글자 크기·줄간격·제목 크기와 가로·세로 정렬 측정을 추가했다. 결과와 캡처는 기존 `../evidence/T08/` 경로를 재사용한다.

## 사례 E — 읽는 흐름과 전폭 구성

- 사용자 후속 요청 “해봐”에 따라 Claude Code CLI로 기존 HTML·CSS·JS를 수정하고 Codex가 실제 전체 화면을 검토했다. 관심과 역할을 먼저 설명하는 메인, 도구 목록이 있는 짧은 소개, 세 열 학습 분야, 전폭 KONNECT 작업 흐름으로 구성했다. 가상의 결과 화면은 만들지 않았다.
- Codex는 중간 폭에서 도구 이름이 잘릴 가능성을 줄이도록 도구 목록의 전환 폭을 조정하고, 학습 분야는 태블릿까지 세 열을 유지했다. 공통 본문·제목 크기와 헤더 정렬은 유지했다. 화면 전체와 주요 영역의 한국어·영어·모바일 캡처를 검토했다.
- 기존 검사에 900px 중간 폭, 텍스트 실제 범위의 잘림 확인, 전체 페이지 캡처를 추가했다. 로컬 Firefox 38개 검사와 JS 비활성·모션 축소 2개 검사가 통과했다. AI 결과가 사용자의 미제공 결과물이나 달성한 학습 계획으로 표현되지 않도록 확인했다.
