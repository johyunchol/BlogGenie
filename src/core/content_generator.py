import sys
import re
import os
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai
import json

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



def generate_blog_content(user_input: dict[str, any], context: str) -> dict[str, any]:
    """수집된 정보를 바탕으로 Gemini를 사용하여 구조화된 블로그 콘텐츠를 생성합니다."""
    print("Gemini를 사용하여 구조화된 블로그 콘텐츠 생성을 시작합니다...")
    
    try:
        configure_gemini()
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        raise ContentGenerationError(f"Gemini 모델 초기화 중 오류 발생: {e}")

    keyword = user_input.get('keyword', '')
    target_audience = user_input.get('target_audience', '전문가')
    tone_of_voice = user_input.get('tone_of_voice', '전문적')
    desired_length = user_input.get('desired_length', '길게 (1500+ 단어)')
    num_subheadings = user_input.get('num_subheadings', 5)
    seo_optimization_level = user_input.get('seo_optimization_level', '강화')
    custom_instructions = user_input.get('custom_instructions', '')

    prompt = f"""
당신은 SEO에 능숙한 전문 기술 블로거입니다.

아래 제공된 '키워드'와 '참고 자료'를 바탕으로, 독자들이 읽기 쉽고 유용한 블로그 게시물을 작성해주세요.
사용자 요청에 따라 다음 사항들을 특별히 고려하여 작성해주세요:

**사용자 요청 사항:**
-   **대상 독자:** {target_audience}
-   **어조:** {tone_of_voice}
-   **희망 길이:** {desired_length}
-   **소제목 개수:** 본문은 서론, 본론({num_subheadings}개 소제목), 결론의 구조를 갖춰야 합니다.
-   **SEO 최적화 수준:** {seo_optimization_level} (이 수준에 맞춰 제목, 메타 설명, 태그 및 본문 내 키워드 활용도를 조절해주세요.)
-   **추가 지시사항:** {custom_instructions if custom_instructions else "없음"}

**생성 규칙:**
1.  **title:** 키워드를 포함하여, 사람들의 흥미를 끌 만한 매력적인 제목이어야 합니다. Plain Text로 작성해주세요.
2.  **meta_description:** 검색 엔진에 표시될 내용으로, 게시물 전체 내용을 150자 내외로 요약하고 키워드를 포함해야 합니다.
3.  **body (구조화된 본문):**
    *   **배열(Array) 형태**여야 합니다.
    *   배열의 각 요소는 **소제목(subtitle), 내용(content), 추천 이미지 키워드(image_keyword)** 세 개의 키를 가진 JSON 객체여야 합니다.
    *   **subtitle:** 각 단락의 주제를 나타내는 소제목입니다. Markdown 형식이 아닌 Plain Text로 작성해주세요. 서론, 본론, 결론 이라는 단어가 굳이 들어가 필요는 없습니다.
    *   **content:** 소제목에 대한 상세 내용입니다. Markdown을 사용하여 가독성을 높여주세요. (예: `* 리스트`) '참고 자료'의 내용을 그대로 복사하지 말고, 자연스럽게 재구성하여 설명해야 합니다.
    *   **image_keyword:** 해당 단락의 내용을 시각적으로 보충할 수 있는 이미지가 효과적일 경우에만, **검색에 용이한 한글 키워드**를 추천해주세요. 예를 들어, 복잡한 개념을 설명하는 다이어그램, 코드 실행 결과를 보여주는 스크린샷, 특정 기술을 상징하는 이미지 등이 좋은 예시입니다. 이미지가 굳이 필요 없거나 글로만 설명하는 것이 더 나은 단락(예: 서론, 결론)의 경우, 반드시 **null** 값을 사용해주세요.
4.  **tags:** 쉼표로 구분된 5개 이상의 관련 태그를 문자열 형태로 추천해주세요.

**키워드:** {keyword}

**참고 자료:**
{context}

**출력 형식 (JSON):**
생성된 콘텐츠를 다음의 JSON 형식에 맞춰서 반환해주세요. 키(key)는 반드시 영어로 작성해야 합니다.
```json
{{
    "title": "생성된 제목",
    "meta_description": "생성된 메타 설명",
    "body": [
        {{
            "subtitle": "첫 번째 소제목",
            "content": "첫 번째 단락의 Markdown 형식 내용입니다.",
            "image_keyword": "첫 번째 단락 관련 이미지 검색어"
        }},
        {{
            "subtitle": "두 번째 소제목",
            "content": "두 번째 단락의 Markdown 형식 내용입니다.",
            "image_keyword": "두 번째 단락 관련 이미지 검색어"
        }}
    ],
    "tags": "쉼표로 구분된 태그1, 태그2, ..."
}}
```
"""
    
    MAX_RETRIES = 1
    MIN_BODY_LENGTH = 300 # Minimum characters for the total body content

    for attempt in range(MAX_RETRIES + 1):
        try:
            print(f"DEBUG: Attempt {attempt + 1} - Sending prompt to Gemini...")
            response = model.generate_content(prompt)
            response_text = response.text.strip()
            print(f"DEBUG: Raw Gemini Response: {response_text}")

            content_dict = None
            try:
                content_dict = json.loads(response_text)
                print("DEBUG: Successfully parsed response as direct JSON.")
            except json.JSONDecodeError:
                print("DEBUG: Response is not direct JSON. Trying regex extraction.")
                json_match = re.search(r'```json(.*?)```', response_text, re.DOTALL)
                if json_match:
                    json_string = json_match.group(1).strip()
                    try:
                        content_dict = json.loads(json_string)
                        print("DEBUG: Successfully parsed extracted JSON string.")
                    except json.JSONDecodeError as e:
                        raise ContentGenerationError(f"추출된 JSON 문자열 파싱 실패: {e}. 추출된 문자열: {json_string[:200]}...")
                else:
                    raise ContentGenerationError("Gemini 응답에서 유효한 JSON 형식을 찾을 수 없습니다.")
            
            if not content_dict:
                raise ContentGenerationError("Gemini 응답에서 유효한 JSON 콘텐츠를 생성하지 못했습니다.")
            
            if isinstance(content_dict.get('tags'), str):
                content_dict['tags'] = [tag.strip() for tag in content_dict['tags'].split(',')]
            
            # Validate body structure and content length
            body_content = content_dict.get('body', [])
            if not isinstance(body_content, list) or not all(isinstance(item, dict) for item in body_content):
                 raise ContentGenerationError("생성된 본문(body)이 유효한 배열 형식이 아닙니다.")

            total_body_length = sum(len(item.get('content', '')) for item in body_content)
            if total_body_length < MIN_BODY_LENGTH:
                print(f"경고: 생성된 본문 총 길이가 너무 짧습니다 ({total_body_length}자). 재시도합니다.")
                if attempt < MAX_RETRIES:
                    continue
                else:
                    raise ContentGenerationError(f"유의미한 콘텐츠 생성에 실패했습니다. (최소 {MIN_BODY_LENGTH}자 필요)")

            print("Gemini 블로그 콘텐츠 생성 완료.")
            return content_dict

        except Exception as e:
            print(f"콘텐츠 생성 중 오류 발생 (시도 {attempt + 1}/{MAX_RETRIES + 1}): {e}")
            if attempt < MAX_RETRIES:
                continue
            else:
                raise ContentGenerationError(f"Gemini 콘텐츠 생성 중 최종 오류 발생: {e}")


def generate_markdown_content(blog_post_object: dict[str, any]) -> str:
    """구조화된 콘텐츠 객체를 최종 마크다운 문자열로 조합합니다."""
    print("마크다운 콘텐츠 생성을 시작합니다...")
    
    title = blog_post_object.get('title', '제목 없음')
    meta_description = blog_post_object.get('meta_description', '')
    body_sections = blog_post_object.get('body', [])
    tags = blog_post_object.get('tags', [])

    # Format tags for display
    tags_formatted = ", ".join([f"#{t}" for t in tags])
    
    # Build body from sections
    body_formatted = ""
    for section in body_sections:
        subtitle = section.get('subtitle', '')
        content = section.get('content', '')
        image_keyword = section.get('image_keyword')

        body_formatted += f"## {subtitle}\n\n"
        body_formatted += f"{content}\n\n"
        if image_keyword:
            body_formatted += f"<!-- Recommended image query: \"{image_keyword}\" -->\n\n"
        body_formatted += "---\n\n"


    # Combine all parts
    final_content = f"""# {title}

> **Meta Description:** {meta_description}

---

{body_formatted}

**Tags:** {tags_formatted}
"""
    print("마크다운 콘텐츠 생성 완료.")
    return final_content.strip()


def save_markdown_to_file(content: str, keyword: str, publishing_platform: str) -> str:
    """마크다운 콘텐츠를 파일로 저장합니다."""
    print(f"마크다운 파일 저장을 시작합니다. 발행 플랫폼: {publishing_platform}...")
    
    if publishing_platform == "Markdown File Only":
        today = datetime.now().strftime("%Y%m%d")
        # Sanitize keyword for filename
        sanitized_keyword = re.sub(r'[\\/*?:\"<>|]', "", keyword).replace(' ', '_')
        filename = f"{today}_{sanitized_keyword}.md"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"마크다운 파일 저장 완료: {filename}")
        return os.path.abspath(filename)
    else:
        # 향후 Tistory, WordPress 등 API 연동 로직 추가 예정
        print(f"경고: {publishing_platform} 플랫폼 발행은 아직 지원되지 않습니다. 마크다운 파일로 저장하지 않습니다.")
        return f"발행되지 않음 (플랫폼: {publishing_platform})"
