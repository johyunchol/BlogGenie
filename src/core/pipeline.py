from src.core.content_generator import (
    generate_blog_content,
    generate_markdown_content,
    save_markdown_to_file
)

def run_blog_post_pipeline(user_input: dict[str, any], save_to_file: bool = True) -> str:
    """블로그 포스트 생성을 위한 전체 파이프라인을 실행하고 마크다운 콘텐츠를 반환합니다."""
    try:
        keyword = user_input.get('keyword', '')
        publishing_platform = user_input.get('publishing_platform', 'Markdown File Only')

        # 1. 키워드를 직접 컨텍스트로 사용 (웹 검색 단계 제거)
        context_data = keyword # Use keyword directly as context

        # 2. 구조화된 블로그 콘텐츠 생성
        blog_post_object = generate_blog_content(user_input, context_data)
        print("구조화된 블로그 콘텐츠가 생성되었습니다.")

        # 3. 마크다운 콘텐츠 생성
        markdown_content = generate_markdown_content(blog_post_object)
        print("마크다운 콘텐츠가 생성되었습니다.")

        # 4. (선택) 마크다운 파일 저장
        if save_to_file:
            file_path = save_markdown_to_file(markdown_content, keyword, publishing_platform)
            print(f"\n🎉 성공! 마크다운 파일이 다음 경로에 저장되었습니다: {file_path}")
        
        return markdown_content

    except Exception as e:
        print(f"오류 발생: 파이프라인 실행 중단 - {e}")
        return f"# 오류 발생\n\n파이프라인 실행 중 다음과 같은 오류가 발생했습니다:\n\n```\n{e}\n```"