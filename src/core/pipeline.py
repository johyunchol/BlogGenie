"""전체 콘텐츠 생성 파이프라인을 정의하는 모듈입니다."""

from src.core.content_generator import (
    read_web_content_from_file, 
    generate_blog_content,
    find_relevant_images,
    save_as_markdown
)

def run_blog_post_pipeline(keyword: str, content_filepath: str) -> None:
    """블로그 포스트 생성을 위한 전체 파이프라인을 실행합니다."""
    try:
        # 1. 파일에서 정보 읽기
        context_data = read_web_content_from_file(content_filepath)
        print(f'"{keyword}"에 대한 정보 파일을 성공적으로 읽었습니다.')

        # 2. 블로그 콘텐츠 생성
        blog_post_object = generate_blog_content(keyword, context_data)
        print("블로그 콘텐츠가 생성되었습니다.")

        # 3. 관련 이미지 검색어 추천
        image_suggestions = find_relevant_images(blog_post_object)
        print("이미지 검색어가 추천되었습니다.")

        # 4. 마크다운 파일 저장
        file_path = save_as_markdown(blog_post_object, image_suggestions, keyword)
        print(f"\n🎉 성공! 마크다운 파일이 다음 경로에 저장되었습니다: {file_path}")

    except Exception as e:
        print(f"오류 발생: 파이프라인 실행 중단 - {e}")