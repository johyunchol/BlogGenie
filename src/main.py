import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.pipeline import run_blog_post_pipeline

def main() -> None:
    """프로그램의 메인 로직을 실행합니다."""
    print("Welcome to Blog-Genie!")
    
    keyword = "파이썬"
    content_file = "search_results.txt"
    
    run_blog_post_pipeline(keyword=keyword, content_filepath=content_file)

if __name__ == "__main__":
    main()