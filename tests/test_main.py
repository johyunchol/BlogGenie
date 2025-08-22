"""main.py에 대한 테스트 코드입니다."""

from src import main

def test_main_exists():
    """main 함수가 존재하는지 테스트합니다."""
    assert callable(main.main)
