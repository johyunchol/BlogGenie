import sys
import tempfile
import os
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
)

# 백엔드 파이프라인 임포트
from src.core.pipeline import run_blog_post_pipeline

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Blog Genie")
        self.setMinimumSize(800, 600)

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Keyword input
        self.keyword_label = QLabel("Enter Keyword:")
        self.keyword_input = QLineEdit()
        layout.addWidget(self.keyword_label)
        layout.addWidget(self.keyword_input)

        # Content Input (QTextEdit)
        self.content_label = QLabel("Enter Content (or paste from search_results.txt):")
        self.content_input = QTextEdit()
        # Optionally load default content from search_results.txt if it exists
        try:
            with open("search_results.txt", 'r', encoding='utf-8') as f:
                self.content_input.setText(f.read())
        except FileNotFoundError:
            self.content_input.setText("Paste your reference content here...")
        layout.addWidget(self.content_label)
        layout.addWidget(self.content_input)

        # Generate button
        self.generate_button = QPushButton("Generate Post")
        self.generate_button.clicked.connect(self.generate_post)
        layout.addWidget(self.generate_button)

        # Result display
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        layout.addWidget(self.result_display)


    def generate_post(self):
        keyword = self.keyword_input.text()
        content_text = self.content_input.toPlainText()

        if not keyword:
            self.result_display.setMarkdown("**Please enter a keyword.**")
            return
        if not content_text:
            self.result_display.setMarkdown("**Please enter content.**")
            return
        
        self.result_display.setMarkdown(f"_Generating blog post for keyword: **{keyword}**..._")
        QApplication.processEvents() # UI 업데이트 강제

        # 임시 파일에 콘텐츠 저장
        temp_file = None
        try:
            with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as temp_file:
                temp_file.write(content_text)
            temp_filepath = temp_file.name

            # 백엔드 파이프라인 실행
            markdown_content = run_blog_post_pipeline(
                keyword=keyword, 
                content_filepath=temp_filepath, 
                save_to_file=False
            )
            
            # 최종 결과 표시
            self.result_display.setMarkdown(markdown_content)

        except Exception as e:
            error_message = f"# 오류 발생\n블로그 생성 중 오류가 발생했습니다.\n\n**Error:**\n```\n{e}\n```"
            self.result_display.setMarkdown(error_message)
        finally:
            # 임시 파일 삭제
            if temp_file and os.path.exists(temp_filepath):
                os.remove(temp_filepath)

def run_gui():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    run_gui()
