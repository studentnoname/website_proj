# 실제 AI 활용 기록

## 사례 A — 구조 점검과 개발 계획

- 도구: Codex, 모델명 미표시.
- 날짜: 2026-10-28 KST.
- 사용자 실제 요청: “해당 파일구조를 읽고 어떻게 작업을 해야할지 계획을 수립”.
- 응답 요약: 웹사이트 구현 소스가 아닌 인계 묶음임을 확인하고, 상위 basicproj 저장소를 참조하는 문제와 준비 도구·TASK 완료 조건을 구분했다.
- 반영 위치: `WORK_PLAN.md`, 이후 `docs/tasks/T01.md`와 환경·빌드 도구.
- 검토: 과거 기록의 접근 불가·Claude 미설치를 현재 사실로 재사용하지 않고 로컬 도구·Git·원격 refs를 다시 점검했다.
- 직접 실행 근거: `docs/evidence/T01/`, T01의 실제 기본 빌드와 T07의 최초 main push 배포.
- 한계: 계획 수립 시점에는 사이트 구현·빌드·배포를 수행하지 않았다. 계획 파일만으로 완료를 주장하지 않는다.

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
