# 실제 기능 검증

환경: Windows, Firefox 159.0. 로컬 운영 경로 `http://127.0.0.1:1313/website_proj/`는 공개 하위 경로를 재현한다. 실제 iPhone 검사는 수행하지 않았다.

브라우저 검사 KST: 2026-10-29T15:55:03.425824+09:00. 정적 검사 KST: 2026-10-29T15:54:52.958466+09:00.

| 번호·기준 | 대상·조건 | 동작·예상 | 실제 결과 | 근거 |
| --- | --- | --- | --- | --- |
| V01 P01~P10 | 공개 사이트, main push | 자동 빌드·Pages·HTTPS·수정 후 재배포 | 최초 push 성공. 개인화와 최종 SHA는 T07·release에서 확인 | T07, evidence/T07/ |
| V02 P11~P20 | 두 언어 홈·깊은 앵커 | 자산·운영 경로 유효, PC 경로 없음 | 두 언어 각각 25개 참조 오류 0. 데모 CV·옛 논문 출력 없음 | static-final.json, I006 |
| V03 P21~P30 | #about·#current | 메뉴·직접 URL·새로고침·뒤로 가기·언어 전환 | 목적지·복귀·같은 섹션 언어 전환·모바일 선택 후 닫기 성공 | firefox/results.json |
| V04 P31~P40 | 두 언어 1440·768·390px·200% | 넘침 없이 읽고 조작, 폭 복구 | 실제 innerWidth 일치·깨진 이미지 0·가로 넘침 없음. 확대 DPR 1→2·폭 1440→720 | 각 폭·200% 화면, I007 |
| V05 P41~P50 | Tab·Enter·Escape·움직임 | 초점·실행·닫기·본문 접근·동작 축소 | Skip link·Enter 본문 이동·Escape 초점 복귀·움직임 전환 성공 | keyboard-focus.png, Firefox JSON |
| V06 P34·P41~P50 | JS 비활성 390px | 기본 HTML로 메뉴·본문 이용 | 네 메뉴 표시·네이티브 #current 이동·JS 향상 클래스 없음 | progressive/results.json |
| V07 P50 | 시스템 reduced-motion | 자동 움직임 축소 | 감소 조건 true·설정 off·실행 중 SVG 애니메이션 0 | progressive/results.json |

Firefox 조작 20건과 별도 점진적 향상 2건이 통과했다. 결과 경로는 `docs/evidence/T08/` 기준이다. 로컬과 공개 검사를 구분한다. HugoBlox 모듈의 `.Site.Data` 폐기 예정 경고는 현재 빌드를 막지 않지만 향후 호환성 점검 항목이다.

기능 변경·개선 전후는 I005 본문 템플릿 선택, I006 출력 정리, I008 헤더 가독성의 발견·수정·재검증에서 확인한다.

콘텐츠 한계: P72의 구체적 다음 행동은 사용자 요청으로 미기재다. P73의 도구별 구현 사례와 P78의 실제 산출물은 미제공이다. 이를 성과로 채우지 않았다.
