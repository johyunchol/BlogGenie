import sys
import re
from datetime import datetime

class WebContentError(Exception):
    """웹 콘텐츠 수집 관련 오류"""
    pass

class ContentGenerationError(Exception):
    """AI 콘텐츠 생성 관련 오류"""
    pass

def read_web_content_from_file(filepath: str) -> str:
    """파일에서 웹 콘텐츠를 읽어옵니다."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        raise WebContentError(f"콘텐츠 파일({filepath})을 찾을 수 없습니다.")

import sys
import re
import os
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai
import json

# .env 파일에서 환경 변수 로드
load_dotenv()

class WebContentError(Exception):
    """웹 콘텐츠 수집 관련 오류"""
    pass

class ContentGenerationError(Exception):
    """AI 콘텐츠 생성 관련 오류"""
    pass

def configure_gemini():
    """Gemini API를 설정합니다."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ContentGenerationError("GEMINI_API_KEY가 .env 파일에 설정되지 않았습니다.")
    genai.configure(api_key=api_key)

def read_web_content_from_file(filepath: str) -> str:
    """파일에서 웹 콘텐츠를 읽어옵니다."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        raise WebContentError(f"콘텐츠 파일({filepath})을 찾을 수 없습니다.")

def generate_blog_content(keyword: str, context: str) -> dict[str, any]:
    """수집된 정보를 바탕으로 Gemini를 사용하여 블로그 콘텐츠를 생성합니다."""
    print("Gemini를 사용하여 블로그 콘텐츠 생성을 시작합니다...")
    
    try:
        configure_gemini()
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        raise ContentGenerationError(f"Gemini 모델 초기화 중 오류 발생: {e}")

    prompt = f"""당신은 SEO에 능숙한 전문 기술 블로거입니다.

아래 제공된 '키워드'와 '참고 자료'를 바탕으로, 독자들이 읽기 쉽고 유용한 블로그 게시물을 작성해주세요.

**생성 규칙:**
1.  **제목 (title):** 키워드를 포함하여, 사람들의 흥미를 끌 만한 매력적인 제목이어야 합니다. 결과물에 불필요한 특수문자 (#, *, " 등)가 포함되지 않게 해야 합니다. 마크다운 형식이 아닌 Plain Text로 작성해야 해야 합니다.
2.  **메타 설명 (meta_description):** 검색 엔진에 표시될 내용으로, 게시물 전체 내용을 150자 내외로 요약하고 키워드를 포함해야 합니다.
3.  **본문 (body):
    *   서론, 본론, 결론의 구조를 갖춰야 합니다.
    *   Markdown을 사용하여 가독성을 높여주세요. (예: `## 소제목`, `* 리스트`)
    *   '참고 자료'의 내용을 그대로 복사하지 말고, 자연스럽게 재구성하여 설명해야 합니다.
4.  **추천 태그 (tags):** 쉼표로 구분된 5개 이상의 관련 태그를 문자열 형태로 추천해주세요. (예: "파이썬, 프로그래밍, 웹개발, AI")

**키워드:** {keyword}

**참고 자료:**
{context}

**출력 형식 (JSON):**
생성된 콘텐츠를 다음의 JSON 형식에 맞춰서 반환해주세요. 키(key)는 반드시 영어로 작성해야 합니다.
```json
{{
    "title": "생성된 제목",
    "meta_description": "생성된 메타 설명",
    "body": "생성된 Markdown 형식의 본문",
    "tags": "쉼표로 구분된 태그1, 태그2, ..."
}}
```
"""

    try:
        response = model.generate_content(prompt)
        # 응답에서 JSON 부분만 추출
        json_response_text = re.search(r'```json\n(.*?)\n```', response.text, re.DOTALL)
        if not json_response_text:
            raise ContentGenerationError("Gemini 응답에서 유효한 JSON 형식을 찾을 수 없습니다.")
        
        content_dict = json.loads(json_response_text.group(1))
        
        # 태그를 리스트로 변환
        if isinstance(content_dict.get('tags'), str):
            content_dict['tags'] = [tag.strip() for tag in content_dict['tags'].split(',')]
        
        print("Gemini 블로그 콘텐츠 생성 완료.")
        return content_dict

    except Exception as e:
        raise ContentGenerationError(f"Gemini 콘텐츠 생성 중 오류 발생: {e}")


def find_relevant_images(blog_post_object: dict[str, any]) -> dict[str, any]:
    """생성된 블로그 콘텐츠를 기반으로 관련 이미지 검색어를 찾습니다."""
    print("관련 이미지 검색어 추천을 시작합니다...")
    body = blog_post_object['body']
    subheadings = re.findall(r"^##\s(.+)", body, re.MULTILINE)
    
    queries = {
        "hero_image_query": f"{blog_post_object['title']} abstract",
        "section_image_queries": {sh: f"{sh} concept" for sh in subheadings}
    }
    print("이미지 검색어 추천 완료.")
    return queries

def generate_markdown_content(blog_post_object: dict[str, any], image_suggestions: dict[str, any]) -> str:
    """모든 콘텐츠를 조합하여 최종 마크다운 문자열을 생성합니다."""
    print("마크다운 콘텐츠 생성을 시작합니다...")
    
    # Format tags for display
    tags_formatted = ", ".join([f"#{t}" for t in blog_post_object['tags']])
    
    # Format image suggestions
    image_queries_formatted = f"- **대표 이미지:** {image_suggestions['hero_image_query']}"
    for section, query in image_suggestions['section_image_queries'].items():
        image_queries_formatted += f"\n- **{section} 섹션:** {query}"

    content = f"""# {blog_post_object['title']}

> **Meta Description:** {blog_post_object['meta_description']}

---
### 이미지 검색어 추천
{image_queries_formatted}
---

{blog_post_object['body']}

---
**Tags:** {tags_formatted}
"""
    print("마크다운 콘텐츠 생성 완료.")
    return content

def save_markdown_to_file(content: str, keyword: str) -> str:
    """마크다운 콘텐츠를 파일로 저장합니다."""
    print("마크다운 파일 저장을 시작합니다...")
    today = datetime.now().strftime("%Y%m%d")
    filename = f"{today}_{keyword.replace(' ', '_')}.md"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"마크다운 파일 저장 완료: {filename}")
    return filename
