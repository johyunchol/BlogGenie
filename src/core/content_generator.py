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

def generate_blog_content(keyword: str, context: str) -> dict[str, any]:
    """수집된 정보를 바탕으로 블로그 콘텐츠를 생성합니다."""
    print("블로그 콘텐츠 생성을 시작합니다...")
    body = f"""# {keyword}에 대한 심층 분석\n\n## 서론\n{keyword}는 전 세계적으로 가장 인기 있는 프로그래밍 언어 중 하나입니다. 이 글에서는 {keyword}의 특징과 장점에 대해 알아봅니다.\n\n## 주요 특징\n{context[:500]}...\n\n## 결론\n결론적으로, {keyword}는 배우기 쉽고 강력한 언어입니다."""
    suggested_titles = [
        f"{keyword}, 왜 최고의 선택일까?",
        f"초보자를 위한 {keyword} 완벽 가이드",
        f"{keyword}의 모든 것: 특징, 장점, 그리고 활용 분야"
    ]
    tags = [keyword, "프로그래밍", "코딩", "IT", "개발자"]
    print("블로그 콘텐츠 생성 완료.")
    return {
        "title": suggested_titles[0],
        "suggested_titles": suggested_titles,
        "meta_description": f"{keyword}에 대한 모든 것을 알아보세요. 특징, 장점, 활용 분야 등을 상세히 다룹니다.",
        "tags": tags,
        "body": body
    }

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

def save_as_markdown(blog_post_object: dict[str, any], image_suggestions: dict[str, any], keyword: str) -> str:
    """모든 콘텐츠를 조합하여 최종 마크다운 파일을 저장합니다."""
    print("마크다운 파일 저장을 시작합니다...")
    today = datetime.now().strftime("%Y%m%d")
    filename = f"{today}_{keyword.replace(' ', '_')}.md"
    
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
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"마크다운 파일 저장 완료: {filename}")
    return filename