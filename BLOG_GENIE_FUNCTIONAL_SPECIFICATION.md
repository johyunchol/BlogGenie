### **'Blog-Genie' 상세 기능 명세서**

**시스템 아키텍처 개요**

프로그램은 단일 파이프라인으로 실행되는 CLI(Command Line Interface) 애플리케이션을 가정합니다. 사용자가 키워드를 입력하면, 아래에 명세된 함수들이 순차적으로 호출되어 최종 결과물인 마크다운(.md) 파일을 생성합니다.

---

#### **1. 메인 파이프라인 (`run_blog_post_pipeline`)**

*   **설명:** 전체 블로그 포스팅 생성 과정을 총괄하고 조율하는 메인 함수입니다. 각 모듈(함수)을 순서대로 호출합니다.
*   **입력 (Input):**
    *   `user_input` (dict): 사용자가 GUI를 통해 입력한 모든 설정 및 키워드를 포함하는 딕셔너리.
        ```json
        {
          "keyword": "str",  // 필수: 블로그 포스트의 핵심 키워드
          "target_audience": "str",  // 선택: 블로그 게시물을 읽을 주 독자층
          "tone_of_voice": "str",  // 선택: 블로그 게시물의 전반적인 분위기나 어조
          "desired_length": "str",  // 선택: 생성될 블로그 게시물의 대략적인 길이
          "num_subheadings": "int",  // 선택: 본문에 포함될 소제목의 개수
          "seo_optimization_level": "str",  // 선택: SEO 최적화의 강도
          "image_suggestion_preference": "str",  // 선택: 이미지 추천 방식에 대한 선호도
          "publishing_platform": "str",  // 선택: 생성된 블로그 게시물을 자동으로 발행할 플랫폼
          "custom_instructions": "str"  // 선택: AI가 블로그 게시물을 생성할 때 참고할 추가적인 지시사항
        }
        ```
*   **처리 과정 (Process):**
    1.  `search_web_for_keyword(user_input['keyword'])`를 호출하여 관련 정보를 수집하고 `context_data`를 받습니다.
    2.  `generate_blog_content(user_input, context_data)`를 호출하여 `blog_post_object`를 생성합니다.
    3.  `save_as_markdown(blog_post_object, user_input['publishing_platform'])`를 호출하여 최종 결과물을 파일로 저장하고, 저장된 `file_path`를 받습니다. (향후 `publishing_platform`에 따라 발행 로직 추가)
    4.  `file_path`를 사용자에게 출력합니다.
*   **출력 (Output):**
    *   `file_path` (str): 생성된 마크다운 파일의 절대 경로. (예: `/Users/johndoe/blog_posts/20230822_파이썬_웹_프레임워크_비교.md`)
*   **예외 처리 (Exception Handling):**
    *   처리 과정 중 어느 단계에서든 실패(Exception)가 발생하면, 에러 메시지를 로그로 남기고 "프로세스 중단: [에러 원인]" 메시지를 출력 후 프로그램을 종료합니다.

---

#### **2. 웹 정보 수집 (`search_web_for_keyword`)**

*   **설명:** 주어진 키워드로 웹을 검색하고, 신뢰도 높은 소스에서 텍스트 정보를 추출하여 후속 처리를 위한 단일 컨텍스트 데이터로 만듭니다.
*   **입력 (Input):**
    *   `keyword` (str): 메인 파이프라인에서 전달받은 키워드.
*   **처리 과정 (Process):**
    1.  `google_web_search` 도구를 사용하여 키워드로 검색을 수행합니다. 검색어는 `"키워드란?"`, `"키워드 사용법"`, `"키워드 추천"` 등 다각도로 조합하여 실행합니다.
    2.  검색 결과 상위 5개의 신뢰도 높은 URL(뉴스, 공식 문서, 대형 블로그 등)을 추출합니다.
    3.  추출된 각 URL에 대해 `web_fetch` 도구를 사용하여 해당 페이지의 전체 텍스트 콘텐츠를 가져옵니다.
    4.  가져온 모든 텍스트 콘텐츠를 하나의 큰 문자열(context)로 결합합니다. 각 출처 사이의 구분자로 `--- [Source: URL] ---` 같은 형식을 삽입합니다.
*   **출력 (Output):**
    *   `context_data` (str): 여러 웹 페이지의 텍스트가 하나로 합쳐진 문자열.
*   **예외 처리 (Exception Handling):**
    *   `google_web_search` 호출 실패 또는 검색 결과가 없을 경우: "웹 검색 결과가 없습니다." 오류를 발생시킵니다.
    *   `web_fetch` 호출 실패 (HTTP 404, 500 등): 해당 URL은 건너뛰고 다음 URL 처리를 계속 진행합니다. 5개 URL 모두 실패 시 "정보를 수집할 수 있는 유효한 웹 페이지가 없습니다." 오류를 발생시킵니다.

---

#### **3. 블로그 콘텐츠 생성 (`generate_blog_content`)**

*   **설명:** 수집된 정보(context)와 사용자 요구사항을 바탕으로, AI를 활용하여 구조화된 블로그 게시물 전체를 생성합니다. 이 단계에서 본문은 소제목, 내용, 이미지 키워드를 포함하는 여러 단락으로 나뉩니다.
*   **입력 (Input):**
    *   `user_input` (dict): `run_blog_post_pipeline`으로부터 전달받은 사용자 입력 딕셔너리.
    *   `context_data` (str): `search_web_for_keyword`로부터 받은 텍스트 덩어리.
*   **처리 과정 (Process):**
    1.  **통합 생성 요청:** AI(LLM)에 `context_data`와 `user_input`을 제공하며, 아래의 모든 요소를 포함하는 JSON 객체를 생성하라는 단일 프롬프트를 전송합니다.
        *   `user_input`의 모든 요소를 고려하여 콘텐츠를 생성하도록 지시합니다. (키워드, 독자층, 어조, 길이, 소제목 개수, SEO 수준, 사용자 정의 지시사항 등)
        *   **본문(body):** `user_input['num_subheadings']`에 맞춰, 각 단락이 `subtitle`, `content`, `image_keyword` 세 가지 키를 갖는 객체의 배열로 생성되도록 요청합니다. `image_keyword`는 `content` 내용에 가장 적합한 이미지 검색어로 생성하도록 합니다.
        *   **SEO 요소:** 생성된 본문 전체를 바탕으로 `title`(최종 제목 1개), `suggested_titles`(추천 제목 배열), `meta_description`, `tags`를 생성하도록 요청합니다.
*   **출력 (Output):**
    *   `blog_post_object` (dict/object): 아래 구조를 가진 객체
        ```json
        {
          "title": "선택된 최종 제목",
          "suggested_titles": ["제목1", "제목2", ...],
          "meta_description": "생성된 메타 설명...",
          "tags": ["태그1", "태그2", ...],
          "body": [
            {
              "subtitle": "첫 번째 단락 소제목",
              "content": "첫 번째 단락의 내용입니다. 이 단락은 A와 B에 대해 설명합니다.",
              "image_keyword": "A와 B를 상징하는 이미지"
            },
            {
              "subtitle": "두 번째 단락 소제목",
              "content": "두 번째 단락의 내용입니다. 여기서는 C의 장점을 자세히 알아봅니다.",
              "image_keyword": "C의 장점을 보여주는 그래프"
            }
          ]
        }
        ```
*   **예외 처리 (Exception Handling):**
    *   AI(LLM) API 호출 실패 시: "콘텐츠 생성 AI 호출에 실패했습니다." 오류를 발생시킵니다.
    *   생성된 JSON의 형식이 올바르지 않을 경우: 재시도를 1회 수행하고, 그래도 실패 시 "유효한 형식의 콘텐츠 생성에 실패했습니다." 오류를 발생시킵니다.

---

#### **4. 마크다운 파일 저장 (`save_as_markdown`)**

*   **설명:** 생성된 구조화된 콘텐츠 객체를 하나의 마크다운 파일로 조합하고 저장합니다.
*   **입력 (Input):**
    *   `blog_post_object` (dict/object): `generate_blog_content`로부터 받은 콘텐츠 객체.
    *   `publishing_platform` (str): 사용자가 선택한 발행 플랫폼 (예: "Tistory", "WordPress", "Markdown File Only").
*   **처리 과정 (Process):**
    1.  `publishing_platform`이 "Markdown File Only"인 경우에만 파일명을 생성합니다. (형식: `YYYYMMDD_키워드.md`, 예: `20230822_파이썬_웹_프레임워크_비교.md`)
    2.  `publishing_platform`에 따라 마크다운 파일의 전체 내용을 문자열로 조합하거나, 해당 플랫폼의 API 형식에 맞춰 데이터를 준비합니다. "Markdown File Only"인 경우 아래 템플릿을 사용합니다.
        ```markdown
        # {blog_post_object.title}

        > **Meta Description:** {blog_post_object.meta_description}

        ---

        {for-loop over blog_post_object.body}
        ## {paragraph.subtitle}

        {paragraph.content}

        <!-- Recommended image query: "{paragraph.image_keyword}" -->

        ---
        {end for-loop}

        **Tags:** #{tag1}, #{tag2}, ...
        ```
    3.  `publishing_platform`이 "Markdown File Only"인 경우 `write_file` 도구를 사용하여 조합된 문자열을 1번에서 생성한 파일명으로 저장합니다. (향후 각 플랫폼 API를 통한 발행 로직 추가)
*   **출력 (Output):**
    *   `file_path` (str): 저장된 파일의 절대 경로.
*   **예외 처리 (Exception Handling):**
    *   파일 쓰기 권한이 없는 경우: "파일 저장 실패: 권한이 없습니다." 오류를 발생시킵니다.
    *   디스크 공간이 부족한 경우: "파일 저장 실패: 디스크 공간이 부족합니다." 오류를 발생시킵니다.
