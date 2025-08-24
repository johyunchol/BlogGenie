# Project: Blog-Genie (자동 블로그 포스팅 프로그램)

## 1. 프로젝트 목표 (Project Goal)

사용자가 지정한 키워드에 대해 웹상의 정보를 수집 및 분석하여, SEO에 최적화된 완성형 블로그 게시물(마크다운 파일)을 자동으로 생성하는 CLI 애플리케이션 개발.

## 2. 현재까지 진행 상황 (Current Status)

- **기획 완료:**
  - `BLOG_GENIE_PRD.md`: 제품 요구사항 문서 작성 완료.
  - `BLOG_GENIE_FUNCTIONAL_SPECIFICATION.md`: 상세 기능 명세서 작성 완료.

- **개발 환경 구축:**
  - `PYTHON_CODING_CONVENTION.md`: Python 개발 가이드라인 정의.
  - `venv`를 이용한 가상 환경 설정 및 `requirements.txt`를 통한 의존성 관리 체계 구축.
  - `src`, `tests`를 포함하는 표준 프로젝트 구조 설정 완료.

- **핵심 기능 프로토타입 구현 완료:**
  - **1단계 (정보 수집):** `google_web_search` 도구를 사용하여 키워드 관련 정보를 수집하고 파일(`search_results.txt`)에 저장하는 기능 구현.
  - **2단계 (구조화된 콘텐츠 생성):** 수집된 정보를 바탕으로, 블로그 게시물을 '단락별 소제목, 내용, 이미지 추천 키워드'로 구조화하여 생성하는 기능으로 고도화.
  - **3.단계 (파일 저장):** 생성된 구조화된 콘텐츠를 최종 결과물인 `YYYYMMDD_키워드.md` 형식의 마크다운 파일로 저장하는 기능 구현.
  - **파이프라인:** 위 3단계의 과정을 순차적으로 실행하는 메인 파이프라인(`run_blog_post_pipeline`) 구현 완료.

## 3. 주요 기술 스택 (Tech Stack)

- **언어:** Python
- **핵심 도구:** `google_web_search`, `web_fetch`, `write_file`, `run_shell_command`
- **코드 품질:** `ruff`, `black`, `mypy`
- **테스트:** `pytest`

## 4. 향후 계획 (Next Steps)

- **AI 모델 연동:** 현재 샘플 데이터로 구현된 콘텐츠 생성 로직(`generate_blog_content`)을 실제 Gemini API와 연동하여 고품질 콘텐츠를 생성하도록 개선.
- **블로그 플랫폼 발행:** Tistory, WordPress 등 주요 블로그 플랫폼의 API와 연동하여 생성된 마크다운 파일을 자동으로 발행하는 기능 추가.
- **사용자 인터페이스 개선:** 키워드를 하드코딩하는 방식에서 벗어나, 사용자로부터 직접 키워드를 입력받는 CLI 인터페이스 개선.
