# 실제 AI 활용 기록

## 현재 확인 주체와 KONNECT 직접 작업 보완 — 2026-11-07

학생은 “내가 계속 직접 열어서 확인하고 있는데”라고 사이트·PDF의 지속적인 직접 확인을 다시 명시하였음. 웹사이트의 크기·띄어쓰기·배치·강조와 모션 위치·불투명도, PDF의 종결어미·서체·내용/목차 구분을 직접 읽고 조작해 수정 판단을 내렸음. 과거의 ‘사용자 검토 미수신’이나 특정 AI 도구의 미검사를 학생의 미확인으로 확대하지 않도록 정정하였음. 자동 측정·로그 생성의 AI 보조 범위는 그대로 공개함.

KONNECT 실제 작업에 대한 학생 원문: “도움신청 기능 제작중 발생한 라이브러리 엡데이트 오류부분을 직접 읽어보아서 현재 작업 공간과 문제가 생기는 부분이 있는지 확인한 후 AI의 권장을 무시하고 업데이트 후 진행 후 현재까지 문제있는 수준은 없음”. 도움신청 개발 중 오류 내용을 직접 읽고 작업 공간의 영향 여부를 살핀 뒤 AI 권장안을 그대로 채택하지 않고 업데이트를 진행한 판단과, 현재까지 개발을 막는 수준의 문제는 없었다는 결과임. 구체적인 라이브러리명·버전·실행 명령·전체 테스트 통과 결과는 추가로 만들어 쓰지 않았음. 공개 중간 결과는 `../tasks/T03.md`에 정리하였음.

## 본인의 판단·직접 확인 근거 — 2026-11-07 I024

P68·P70 평가 의견에 따라 기존 대화와 11월 7일 답변의 학생 관찰·판단을 구분하였음. Codex가 원문을 발췌·정리하였음. 기기·브라우저와 수정 후 결과는 학생의 진술이며 Codex의 실기기 측정이 아님. 학생은 “현재 노트북과 아이폰으로 직접진행하였다”, “브라우저는 크롬과 사파리로 진행하였다”라고 답하였음. 정확한 실행 시각·브라우저 버전·기기별 세부 결과는 제공되지 않았으므로 추가하지 않았음. 아래의 과거 기술 검사·캡처는 Codex 수행이며 학생의 직접 실행과 구분함.

### U01 — 웹사이트 가독성 확인과 수정 판단

| 항목 | 실제 관찰·판단과 근거 |
| --- | --- |
| 대상·예상 | 웹사이트의 본문 크기·배치·강조가 일정하고 내용을 읽기 쉬워야 함. 기존 폴더·코드를 재사용해야 함. |
| 초안 관찰 원문 | “디자인으로 글자를 배치한것은 좋은데 본문의 글자 크기도 균일하지 않고 배치도 균일하지 못해 또한 강조하는 것과 강조하지 않는 것이 구분되어있지 않아” |
| 보류·수정 이유 원문 | “그리고 HTML 한 파일로 다모으라은 게 아니야 불필요하게 폴더를 여러가 만들지 말고 재사용하라는 거지 다시 제작” |
| 본인 후속 확인 원문 | “웹사이트에서는 띄어쓰기와 문자의 크기를 보기 쉽도록 변경하였고” |
| 판단·반영 | 글자 배치 방향은 유지하되 초안 그대로의 반영은 보류하였음. 크기·배치·강조의 불일치와 읽기의 어려움 때문에 재제작, 공통 본문 체계, 띄어쓰기 수정을 요구하였음. 기존 화면·공통 CSS·JS를 재사용하였음. |
| 반영 위치·보조 근거 | `site/layouts/landing/list.html`, `site/assets/css/portfolio.css`, `site/assets/js/portfolio.js`. 현재 화면 캡처와 글자 크기·정렬 측정은 `../evidence/T08/`의 Codex 후속 검증임. |
| 확인 범위 | 학생의 직접 화면 읽기·가독성 판단임. 모든 기기별 픽셀값·접근성·기능 검사를 학생이 측정했다는 의미는 아님. |

### U02 — 스크롤 모션 위치와 불투명도 확인

| 항목 | 실제 관찰·판단과 근거 |
| --- | --- |
| 예상 원문 | “웹사이트 접속했을 때 글들이 애니메이션으로 하나씯 들어오고 스크롤 할 때 다음화면이 이전화면을 가리면서 물처럼 흘러 들어는 방식” |
| 초기 실제 결과 | “동일한데 변한게 없어” / “똑같아” |
| 효과 켠 뒤 결과·판단 원문 | “화면 효과 켜니까 잘 보이네 다만 불투명도와 애니메이션의 자연스러움을 추가해서 물처럼 흐르는 것으로 만들어줘” |
| 대상 위치 수정 원문 | “원래 의도한 대로 스크롤 진행에 따라서 모션의 변화가 이루어져야 했으나 모션이 이루어지는 장소가 달라서 그 장소르 지칭하는 방식으로 명령을 진행하여수정함” |
| 수정 후 확인 원문 | “기존의 장소외에서 애니메이션이 진행되는 문제는 행결되었으나 의도한 바와 다르게 애니메이션이 작동되어 불투명도를 명시하여 그부분을 해결하엿다” |
| 채택·수정·이유 | 효과를 켰을 때 기본 동작이 보이는 것은 확인하였음. 대상 위치가 다른 문제는 위치를 지목해 수정하였고, 남은 표현 차이는 불투명도를 명시해 보완하였음. 원하는 화면 덮기 방식은 유지하되 위치·불투명도는 실제 화면을 본 뒤 재지시하였음. |
| 반영 위치·보조 근거 | 공통 화면·CSS·JS에 반영하였음. Claude가 패널 불투명도·곡선·잔여 이동을 작성하고 Codex가 검토·검사하였음. 아래 사례 F·G·H 및 `../issues/I013.md`, `../issues/I014.md`와 구분해 확인함. |
| 확인 범위 | 학생은 노트북·아이폰, Chrome·Safari로 직접 확인하고 위치·불투명도 문제가 해결되었다고 답하였음. 글별 등장 간격·모든 전환·모든 기기 조합의 성공을 측정한 것은 아님. |

### U03 — 제출 PDF의 문장·서체 구분 확인

| 항목 | 실제 관찰·판단과 근거 |
| --- | --- |
| 예상 | 읽기 쉬운 문장과 내용·목차를 구별할 수 있는 글자 크기·글꼴이어야 함. |
| 실제 읽기 결과 원문 | “본문 크기를 실제로 보았을 때 제대로 읽기 어려울 정도로 띄어쓰기와 단어선정 및 종결어미에 오류가 존재하여 존재하는 스킬로 적용하고 필요한 부분은 수정을 진행하였음” |
| PDF 구분 확인 원문 | “PDF에서는 종결어미와 문자의 크기 및 글꼴을 변경하여 문장 속 내용간의 분리와 목차마다의 분리를 식별할 수 있도록하엿다” |
| 본인 판단·이유 | 가독성을 해치는 표현을 그대로 채택하지 않고 스킬 적용과 필요한 수정을 선택하였음. 종결어미·크기·글꼴을 조정해 내용과 목차의 구분을 개선하였음. 원래의 과제 채점 요건 우선 지시는 유지하였음. |
| AI 제안·반영 위치 | Claude·ARS의 문장 개선 제안과 Codex의 대조·수정은 아래 기록과 보고서 사례 3에 공개하였음. 본문은 `../report-sections.json`, 서체·크기·배치는 `../../scripts/render_records.py`에 반영하였음. |
| 확인 범위 | 학생의 본문 읽기와 내용·목차 구분 판단임. 전체 PDF의 링크·문자·페이지를 프로그램으로 검사한 Codex의 검수와 구분함. 학생은 이후 수정 과정에서도 사이트와 PDF를 계속 직접 열어 확인하였음을 다시 명시하였음. |

## 서체 위계와 전체 문서의 문맥 검토 — 2026-11-06 KST

사용자 요청 원문 발췌: ‘글자 크기와 폰트의 변화로 제목과 소제목을 나누어주고 문단을 나누어서 가독성을 올린다’. Codex가 PDF의 서체·크기·문단·표 배치를 수정하고 공개 텍스트와 TASK PDF를 대조하였음. 실제 오류 I023의 T03·T09 원문/PDF 불일치를 먼저 기록한 뒤 최신 원문으로 생성하였음.

추가 문맥 검토는 실제 Claude Code 2.1.287 / claude-opus-5-5의 읽기 검토로 수행하였음. 실제 전달문 발췌: “AI disclosure, verbatim actual requests, student-vs-agent judgment, actual failed/successful evidence, read-only vs executed KONNECT records, future plans, licenses and technical verification limits MUST remain accurate.” 과제 채점표와 현재 보고서·TASK 기록을 읽도록 하였고, 추적 파일 편집·PDF 변경·새 실행 검증은 금지하였음.

Claude의 의견 11개를 Codex가 대조하였음. 변경과 근거의 인접 배치, Git 설명 통합, 내부 약어 검사 문장 삭제, 날짜별 측정값 구분, 콘텐츠 공백으로 오해되는 표현과 띄어쓰기를 반영하였음. AI 사례 제목은 이미 소제목으로 출력하고 있어 중복 제목은 넣지 않았으며, 과거 브라우저 버전은 실제 기록을 유지하고 검사 시점을 명시하였음. 초기 계획 사례는 이 문서와 WORK_PLAN.md에 보존하고 제출 보고서의 대표 사례는 구현·전환 효과·문장 개선 3건으로 정리하였음. Claude 검토를 사용자의 직접 코드 검토나 새 KONNECT 실행으로 표시하지 않았음.

## 표·문단 배치와 완료형 어미 조정 — 2026-11-06 KST

사용자 원문: ‘표와 문단 띄어쓰기를 활용하여 가독성 증대 그리고 문서의 글씨를 ~하였음으로 변경하고 AI 가 쓴 것 같은 형식을 피하기’. 실제 Claude Code 2.1.287 / claude-opus-5-5에 기존 원문과 academic-paper의 writing_quality_check.md를 읽고 어미만 수정하도록 요청하였음. 실제 전달문은 “Completed work: concise report endings such as 구성하였음, 확인하였음, 수정하였음” 및 “Never make future plans or read-only evidence into completed testing”이었음. 이번에는 전체 스킬을 다시 호출하지 않고 앞서 적용한 정확성·간결성 지침으로 문장을 다듬었음.

Claude는 본문 87개와 검증표 7개 수정안을 반환하였음. Codex가 항목별 인용문·URL·변수·수치·경로·필드명과 목차·표 머리글·그림의 보존을 대조하였음. 남은 완료형 표현 4개를 추가로 정리하였고, AI 사용 공개와 실제 검증의 주체·한계는 유지하였음. 문체 개선을 AI 사용 은폐나 판별 회피로 적용하지 않았음.

Codex는 기존 PDF 렌더러에서 제출 정보·기준 대조·변경 전후·집계·문제 조치를 표로 배치하고 과정·판단을 문단으로 구성하였음. 본문 10pt, 줄간격 16.5pt, 문단 뒤 7pt와 표 안 여백을 적용하였으며, 사례별 요청·응답·판단·검증이 가능한 한 같은 페이지에 오도록 조정하였음. 11쪽 PDF를 렌더해 전체 페이지·링크·필수 항목을 확인하였음. 사이트와 KONNECT 코드는 변경하지 않았음.

## Academic Research Skills를 이용한 보고서 문장 개선 — 2026-11-06 KST

사용자 요청 원문 발췌: ‘이 스킬을 적용해서 작성해줘 대신 과제 채점의 가중치가 가장 높아서 절대 그걸 어겨서는 안돼’. 실제 Claude Code 2.1.287의 claude-opus-5-5를 실행하고 academic-research-skills:academic-paper 스킬 호출을 확인했다. 사용한 원본은 Cheng-I Wu의 Academic Research Skills 3.24.2, 고정 커밋 6d9388674de1ad0437ad95db3d52f92b92204d84이다. 출처: https://github.com/Imbad0202/academic-research-skills/blob/6d9388674de1ad0437ad95db3d52f92b92204d84/academic-paper/SKILL.md . 이용 조건은 CC BY-NC 4.0이다.

실제 전달 요청 발췌: “THE COURSE RUBRIC OVERRIDES EVERY SKILL DEFAULT.” / “Prefer no more than 45 bounded operations.” 기존 보고서와 채점표, SKILL.md와 academic_writing_style·writing_quality_check·writing_judgment_framework를 읽도록 했다. 목차·표·그림·수치·링크·실제 요청 인용문, 향후 계획과 기존 기록 읽기의 범위를 보호했다. 학번·이름의 실제 값과 비공개 KONNECT 코드는 전달하지 않았다.

Claude는 개조식 항목 171개를 127개로 묶는 43개 수정안을 작성하고, 변경 전·후·재검증·반영 위치·한계의 역할을 표시했다. Codex는 모든 old 문자열의 정확한 일치·비중첩, 8개 목차·표·그림 불변, URL·변수·수치·요청 인용문·파일 경로와 기준 ID를 대조했다. 추가된 P77/P78 반복 표기·390px 설명·변경 1에서 6절의 기존 오류 0 결과로 가는 참조는 원문에 있는 사실의 재사용으로 확인했다. 파일명 뒤 마침표는 경로 자체의 변경과 구분했다. 새 성과·새 실행 결과로 바뀐 문장이 없는지도 수정안 전체를 읽어 검토했다.

반영 판단은 사용자가 지정한 과제 우선·내용 유지 범위에 따라 Codex가 수행했다. 논문용 IMRaD·초록·APA·새 문헌·추가 연구/윤리 절은 적용하지 않았다. ARS의 전체 연구 파이프라인·학술용 patch 승인/재생 체계·채점 인증을 실행했다는 뜻이 아니다. 실제 적용 범위는 지침의 명료성·정확성·근거 대조 원칙과 개별 항목 수정이다. 약어 검사 결과는 템플릿 변수·공식 도구·코드 표기까지 경고하므로 국문 과제의 오류 판정으로 사용하지 않는다.

반영 파일은 docs/report-sections.json이다. 이번 실제 사용은 보고서 7절 사례 4와 8절 출처에도 구분했다. 최종 main·Actions 정보를 갱신한 뒤 PDF의 전체 렌더·본문·그림·증빙 링크를 확인한다. 사이트의 HTML·CSS·JavaScript와 KONNECT 코드는 변경하지 않는다.

## P49 현재 메뉴의 비색상 표시 — 2026-11-06 KST

사용자 요청: ‘최종 제출 상태 말고 나머지는 보완’. Claude Code 2.1.287 / claude-opus-5-5에 기존 공통 CSS만 수정하도록 요청했다. 실제 요청 발췌: “Add a shared .nav a[aria-current] rule that uses both font-weight: 700 and a visible underline” / “Retain existing colors, backgrounds, hit target sizes, focus outline, hover behavior”.

Claude는 선택된 항목에 굵은 글씨와 2px 밑줄을 적용하고 미검사 상태로 반환했다. Codex가 diff를 검토하고 실제 1440·390px에서 aria-current, 굵기·밑줄, 나머지 항목과의 구별을 확인했다. 다른 콘텐츠·JS·폴더·이미지는 변경하지 않았다. 기존 브라우저 검사에 두 언어·네 폭의 about→current 선택 변경과 비색상 구분 검사를 추가해 같은 누락을 확인할 수 있도록 했다. 공개 결과와 최종 PDF의 버전은 I021·검증 기록에서 연결한다.

## P79 연결·P78 결과 구분 보완 — 2026-11-06 KST

사용자 요청: ‘우선순위대로 진행’. 앞선 검토의 P79 배운 점→다음 개선 연결과 P78 중간 결과 명료화를 순서대로 반영한다. Claude Code 2.1.287 / claude-opus-5-5에 기존 HTML의 두 문단만 수정하도록 요청했다. 실제 요청 발췌: “This is a copy-only revision in the existing Hugo portfolio” / “This connects the lesson to the user-selected FUTURE action; do not imply the planned tests are completed.”

Claude는 한국어·영어의 개선 계획과 중간 기록 설명만 바꾸었으며 검사를 실행하지 않았다고 밝혔다. Codex는 diff와 두 언어 빌드 결과를 확인하고 docs/tasks/T03.md 및 보고서 원문을 맞췄다. 기존 도움 기능 변경 기록의 회귀·빌드·타입 검사 성공은 읽기 확인으로만 요약했다. 새 KONNECT 실행 결과·공개 코드·정책 상세를 추가하지 않았다. 화면 검증과 최종 공개/PDF 확인은 I020의 결과로 연결한다.

## 2026-11-05 공개 내용의 정보 최소화

사용자 요청은 “어플을 들어가서 공격할 수 있는 경로를 적었거나 중요한 정보를 적었는 지확인하고 수정”이다. Codex는 현재 공개 파일과 도달 가능한 과거 텍스트/PDF를 패턴 검색하고 활동 문서를 읽었다. 실제 운영 인증정보·접속 주소·공격 절차는 확인하지 못했으며 과거 테마의 DB 접속 문자열은 예제 계정·암호였다. 이는 콘텐츠 검토이고 앱 자체의 보안 시험이 아니다.

Claude Code에 기존 HTML의 세 작업 문단만 수정하도록 요청했다. 실제 입력 발췌: “Keep the concrete educational workflow and grading criteria” / “reduce unnecessary policy detail”. 세부 정책의 수치·접근 판정·응답 대응·저장 내부 처리는 제외하고 사용 도구와 일반적인 입력 확인·저장/조회·결과 비교 방법을 남긴다. Codex가 원문과 사실 범위·공개 수준을 대조하고 문서·화면 증거·보고서도 함께 정리한다. 원본 KONNECT 코드·서비스는 변경하지 않는다.

## 2026-11-05 실제 처리 방식과 중간 기록 설명

사용자는 다음 학습 행동으로 ‘도움 요청 API의 정상·입력 오류·권한 오류 테스트를 작성하고 결과 정리’를 선택했다. Claude Code(claude-opus-5-5)에 “This is a FUTURE learning action, not tests he has already completed”라고 구분하고 #future의 목표·다음 행동만 추가하도록 요청했다. 기존 tool-rail 배치를 재사용하고 기존 CSS에 학습 분야와의 간격 한 줄만 추가했다. Codex는 선택하지 않은 SQL 안·미제공 날짜·완료 실적이 들어가지 않았는지 검토한다.

사용자 원문: “지금 어떻게 한다고 추상적으로 나와있지 어떤 방식으로 어떤것을 어떻게 한다고 안나와있어서 이것을 조금더 자세하게 설명할 수 있도록 하고 빈칸을 채우려고해”. Codex는 비공개 백엔드·통합 테스트와 기존 검증 문서를 읽어 정상 처리·입력·접근 검사와 저장 흐름을 대조했다. 세부 정책과 응답 대응은 공개 요약에서 제외한다. 새 KONNECT 테스트는 실행하지 않았다.

실제 Claude Code CLI(claude-opus-5-5) 요청은 “Replace vague labels with a short bold title then br and a concise explanation in each existing p”와 “Do not edit #future yet: a real next learning action is awaiting his answer”이다. Claude는 기존 HTML에서 네 단계 설명·상태·중간 기록 링크를 작성하고 미검사임을 밝혔다. Codex는 영어의 처리 순서 오해를 줄이고 중간 기록 소개를 간결하게 정리했으며 링크를 설명과 같은 열에 묶었다. 원본 코드·민감값을 전달하거나 공개하지 않았다. 반영 파일은 기존 site/layouts/landing/list.html과 docs/tasks/T03.md다.

## 2026-11-05 채점 위험 보완

후속 실제 관찰: 사용자가 Desktop konnect를 지정한 뒤 Codex가 백엔드의 도움 요청·답변 Controller/Service/DTO, 통합 테스트, 기존 로컬 검증 문서를 읽었다. Claude Code(claude-opus-5-5)에 “Change ONLY the single existing paragraph under .lesson-note”와 “Those sources confirm work on help request/answer APIs, input and access-permission checks, and existing local DB/HTTP test records”로 한 문단의 두 언어 요약을 요청했다. 비공개 코드·운영 로그·개인정보·상세 보안 조사 내용은 전달하거나 공개하지 않았다. 이번 KONNECT 실행 검증·배포가 아니라 읽기 검토이며, 사이트에서는 작업 범주와 로컬 검증 방식을 설명한다.

사용자의 후속 답변으로 목적과 검증 이유가 확정되어 Claude Code에 기존 KONNECT 소개·마지막 작업 단계·작업 방식 문단만 보완하도록 요청했다. 실제 입력: “Confirmed purpose: international students need help; other users who have relevant experience share their experiences to help resolve those needs.” / “this is a web application connected to a live server, so he tests locally before deploying to check the integration.” 새 기능·성과·특정 도구 선택 이유를 만들지 않도록 제한했고 Codex가 원문과 대조한다. KONNECT 코드 직접 관찰은 경로 확인 전 미수행이다.

사용자의 “우선순위대로 해결”에 따라 Codex가 404 경로 보정과 보고서 증거 연결을 맡았다. 프론트 P77 문구는 Claude Code 2.1.287(claude-opus-5-5)로 기존 lesson 문단만 작성하도록 요청했다. 실제 입력 발췌는 “Clarify the existing first paragraph of .lesson-body by explicitly connecting those known facts”와 “Do NOT change the vague platform purpose (P75): the user's specific problem/feature answer is still pending”이다. Claude는 직접 검증의 목적을 설명하는 두 언어 문장을 작성하고 미검사임을 밝혔다. Codex는 중복과 어색한 영어를 줄이고 확인된 사실 범위를 검토했다. 반영 파일은 site/layouts/landing/list.html이다. 새 활동·성과·기능·다음 학습 행동을 만들지 않았다. 실제 빌드·홈과 404 정적 검사 및 배포 후 브라우저 검사로 확인한다.

## 사례 G — 글 순차 등장과 화면 전체 전환

- 2026-11-04 KST, Claude Code 2.1.287, 실제 modelUsage: claude-opus-5-5. 사용자 요청은 이전 시도를 되돌리고 접속 시 글이 하나씩 들어오며 스크롤 시 다음 화면이 이전 화면을 덮도록 하라는 설명이었다. 실제 발췌는 `prompts/frontend.md`.
- Claude는 기존 HTML·CSS·JS 세 파일에 normal-flow 앵커와 sticky 패널, 전체 패널의 곡선 clip, 640ms·80ms 지연 등장, 키보드와 효과 제어를 작성했다. 빌드·실제 브라우저 검사는 하지 않았다고 명시했다. 철회한 자료를 참고하지 않았다.
- 판단: 단순 물결 장식은 제거하고 섹션의 배경·글 전체가 겹치는 방식을 채택했다. 짧은 섹션은 기존 높이를 유지하고 긴 섹션은 읽은 후 고정한다. Codex는 원래 배치를 유지하는 판단을 받아들이고 I011에서 짧은 패널을 모두 뷰포트 높이로 보던 검사와 첫 프레임 이전 startTime 검사를 고쳤다.
- 검증: 55개 Firefox 검사와 별도 2개 검사에서 실제 화면 hit-test·고정 좌표·앞 패널 이동·clip 경로·등장 시각·키보드·일반 흐름 복원·깊은 링크를 확인했다. `../verification.md`와 I011에 연결한다. Codex의 검토를 사용자의 직접 코드 검토라고 기록하지 않는다. 해당 자동 측정 환경은 Windows Firefox였음.

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
- Codex가 diff·한국어 문구를 검토하고 Hugo 빌드·정적 검사·기존 Firefox 55개 검사·점진적 향상 11개 검사를 수행했다. 기본 모션 설정을 강제로 바꾸지 않는 검사와 두 언어의 실제 겹침을 추가했다. 기기 설정은 변경하지 않았다. 확인 범위는 Windows Firefox의 브라우저 뷰포트이며 해당 자동 측정 환경은 Windows Firefox였음.

## 사례 G — #intro 진입과 명시적 재생 링크

- 2026-11-04 KST, Claude Code 2.1.287, claude-opus-5-5. 사용자 원문 “똑같아”. Codex가 효과 on 상태의 루트·#intro 첫 진입을 비교해 애니메이션 7개·0개를 확인했다(I014). 사용자 주소는 아직 미확인이다.
- 실제 CLI 입력: “Treat initial #intro as first-screen entrance” / “Add explicit preview URL support ?motion=on”. 기존 JS만 수정하도록 제한했다. Claude는 수정 내용을 설명하고 미검사임을 밝혔다. Codex가 build와 정적 검사, 두 언어 진입·새로고침·선택 유지 검사를 수행했다. 실제 결과는 progressive/results.json에 보존한다. 새 framework·폴더·콘텐츠는 추가하지 않았다.

## 사례 H — 투명도와 유동적인 추종 움직임

- 사용자 실제 확인: “화면 효과 켜니까 잘 보이네 다만 불투명도와 애니메이션의 자연스러움을 추가해서 물처럼 흐르는 것으로 만들어줘”. 2026-11-04 KST, Claude Code 2.1.287, claude-opus-5-5.
- 실제 CLI 입력 발췌: “Incoming COMPLETE panel briefly translucent” / “Add restrained, finite liquid FOLLOW-THROUGH on actual incoming panel position + curve after native scroll.” 기존 CSS·JS만 편집하도록 제한했다. Claude는 0.88→1의 전체 패널 불투명도, 넓은 한 곡선, 짧게 따라오다 가라앉는 이동, 최대 320ms 후 정지, 900ms 첫 글 등장을 구현하고 미검사라고 밝혔다.
- Codex는 기존 겹침·메뉴·모션 제어 검사에 PC·모바일의 실제 불투명도와 아래/위 방향의 잔여 이동·정지를 추가했다. 학생은 후속 답변에서 위치·불투명도 수정 후 문제가 해결된 것을 직접 확인하였다고 밝혔음. 원문은 상단 U02에 보존하였음. 본문·활동·다음 행동은 수정하지 않는다.

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
- 본인 확인: 학생이 초안과 수정본을 직접 열어 읽고 가독성·배치·효과에 대한 판단과 재확인 결과를 전달하였음. 현재 기록은 상단 U01~U03이며, 초기 작성 시점의 답변 대기 상태를 현재의 미검토로 기술하지 않음.

## 사례 C — 사용자 피드백에 따른 재제작

- 사용자 요청: 파일 구성 단순화와 화면 재구성을 위한 “다시 제작해”. 이전 결과는 `archive/portfolio-v1`에 보존하였음.
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
