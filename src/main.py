import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.pipeline import run_blog_post_pipeline
from src.gui import run_gui

def main() -> None:
    """프로그램의 메인 로직을 실행합니다."""

    if "--gui" in sys.argv:
        print("Starting Blog-Genie GUI...")
        run_gui()
    else:
        print("Running Blog-Genie in CLI mode...")
        # For CLI mode, create a dummy user_input for testing purposes
        user_input = {
            "keyword": "파이썬",
            "target_audience": "일반 대중",
            "tone_of_voice": "전문적",
            "desired_length": "보통 (800-1500 단어)",
            "num_subheadings": 5,
            "seo_optimization_level": "강화",
            "image_suggestion_preference": "검색어만 추천",
            "publishing_platform": "Markdown File Only",
            "custom_instructions": ""
        }
        # content_file is no longer needed as web search is integrated
        run_blog_post_pipeline(user_input=user_input)

if __name__ == "__main__":
    main()
