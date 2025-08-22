# Blog-Genie Python 개발 가이드라인

이 문서는 Blog-Genie 프로젝트의 Python 코드 품질을 일관성 있게 유지하고, 가독성과 유지보수성을 높이기 위한 개발 규칙 및 스타일 가이드를 정의합니다. 모든 기여자는 이 가이드라인을 따르는 것을 원칙으로 합니다.

---

### 1. 코딩 스타일 (Coding Style)

**PEP 8**을 기본 스타일 가이드로 채택합니다. 모든 코드는 PEP 8을 준수해야 합니다.

- **주요 내용:**
  - 들여쓰기: 4개의 스페이스(Space) 사용. 탭(Tab) 사용 금지.
  - 라인 길이: 한 줄에 최대 79자(Docstring, 주석은 72자)를 권장하나, 최대 88자까지 허용. 이는 코드 포맷터인 `Black`의 기본 설정과 일치합니다.
  - 네이밍 컨벤션:
    - `함수`, `변수`, `메서드`: `snake_case` (예: `run_pipeline`)
    - `클래스`: `PascalCase` (예: `BlogGenerator`)
    - `상수`: `ALL_CAPS_SNAKE_CASE` (예: `MAX_RETRIES`)
    - `모듈`: 짧은 `snake_case` (예: `utils.py`)

- **자동 포맷팅:**
  - 코드 포맷터로 **`Black`**을 사용합니다. Commit 전 `Black`을 실행하여 코드를 자동으로 포맷팅해야 합니다.
  - **`isort`** 또는 **`Ruff`**의 import 정렬 기능을 사용하여 import 순서를 자동으로 정렬합니다. (표준 라이브러리 -> 서드파티 라이브러리 -> 로컬 라이브러리 순)

---

### 2. 타입 힌팅 (Type Hinting)

**PEP 484**에 따라 모든 함수 시그니처(파라미터 및 반환 값)에 타입 힌트를 명시하는 것을 원칙으로 합니다.

- **목적:**
  - 코드의 가독성 및 명확성 증대.
  - 정적 분석 도구(`Mypy`)를 통한 잠재적 타입 오류 발견.
  - 개발 도구(IDE)의 코드 자동 완성 및 분석 기능 강화.

- **예시:**
  ```python
  def search_web(keyword: str, retries: int = 3) -> list[str]:
      # ... function body ...
      return ["url1", "url2"]
  ```

---

### 3. Docstrings

**PEP 257**을 따르며, 모든 모듈, 함수, 클래스, 메서드에는 Docstring을 작성해야 합니다. Docstring 스타일은 **Google Python Style**을 따릅니다.

- **목적:**
  - 코드의 목적, 사용법, 인자, 반환 값 등을 명확히 설명.
  - 문서 자동 생성 도구(Sphinx 등)와의 연동.

- **예시:**
  ```python
  def generate_blog_content(context: str, keyword: str) -> dict[str, any]:
      """주어진 컨텍스트와 키워드로 블로그 콘텐츠를 생성합니다.

      Args:
          context: 웹에서 수집된 원본 텍스트 데이터.
          keyword: 콘텐츠의 핵심 주제가 될 키워드.

      Returns:
          제목, 본문, 태그 등을 포함하는 딕셔너리 객체.
          
      Raises:
          AIContentError: AI 모델이 유의미한 콘텐츠 생성에 실패한 경우.
      """
      # ... function body ...
  ```

---

### 4. 프로젝트 구조 (Project Structure)

프로젝트는 다음과 같은 기본 구조를 따릅니다.

```
/blog_poster
├── .venv/                  # 가상 환경
├── src/                    # 소스 코드
│   ├── __init__.py
│   ├── core/               # 핵심 로직 (웹 크롤링, AI 연동 등)
│   │   └── __init__.py
│   ├── utils/              # 보조 유틸리티 (파일 I/O, 설정 로더 등)
│   │   └── __init__.py
│   └── main.py             # 프로그램 메인 진입점
├── tests/                  # 테스트 코드
│   ├── core/
│   │   └── test_crawling.py
│   └── test_main.py
├── .env                    # 환경 변수 (API 키 등)
├── .gitignore
├── requirements.txt        # 의존성 목록
└── README.md
```

---

### 5. 의존성 관리 (Dependency Management)

- **가상 환경:** `venv`를 사용하여 프로젝트별로 격리된 개발 환경을 구성합니다.
  - 생성: `python -m venv .venv`
  - 활성화: `source .venv/bin/activate` (macOS/Linux)
- **패키지 관리:** `pip`와 `requirements.txt`를 사용합니다.
  - 패키지 설치: `pip install -r requirements.txt`
  - 의존성 파일 갱신: `pip freeze > requirements.txt`

---

### 6. 테스팅 (Testing)

- **테스트 프레임워크:** **`pytest`**를 사용합니다.
- **규칙:**
  - `tests` 디렉토리 안에 `src`와 동일한 구조로 테스트 파일을 작성합니다.
  - 테스트 파일명은 `test_*.py` 또는 `*_test.py` 형식으로 작성합니다.
  - 각 기능 및 함수에 대한 단위 테스트(Unit Test)를 작성하는 것을 원칙으로 합니다.

---

### 7. 코드 품질 도구 (Code Quality Tools)

- **Linter:** **`Ruff`** 또는 `Flake8`을 사용하여 코드 스타일 및 잠재적 오류를 검사합니다. `Ruff`는 속도가 매우 빠르고 다양한 기능을 지원하므로 강력히 권장합니다.
- **Formatter:** **`Black`**을 사용하여 일관된 코드 스타일을 유지합니다.
- **Static Type Checker:** **`Mypy`**를 사용하여 타입 힌트의 정합성을 검사합니다.

- **실행 명령어 예시:**
  ```bash
  # Linter (Ruff)
  ruff check .

  # Formatter (Black)
  black .

  # Type Checker (Mypy)
  mypy src/
  ```

---

### 8. Git 커밋 메시지 규칙 (Git Commit Message Convention)

**Conventional Commits** 명세에 따라 커밋 메시지를 작성합니다.

- **형식:** `<type>(<scope>): <subject>`
- **주요 `type`:**
  - `feat`: 새로운 기능 추가
  - `fix`: 버그 수정
  - `docs`: 문서 변경
  - `style`: 코드 스타일 변경 (포맷팅, 세미콜론 등)
  - `refactor`: 기능 변경 없는 코드 리팩토링
  - `test`: 테스트 코드 추가/수정
  - `chore`: 빌드, 패키지 매니저 등 기타 변경사항
- **예시:**
  ```
  feat(core): AI를 이용한 콘텐츠 생성 기능 추가
  fix(crawling): 특정 사이트에서 HTML 파싱이 실패하는 문제 수정
  docs(readme): 프로젝트 실행 방법 업데이트
  ```
