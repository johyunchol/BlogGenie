import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext

class BlogGenieGUI:
    def __init__(self, master):
        self.master = master
        master.title("Blog Genie - 자동 블로그 포스팅 프로그램")

        # Configure grid for better resizing
        self.master.columnconfigure(1, weight=1)

        self.create_widgets()

    def create_widgets(self):
        row_idx = 0

        # Keyword Input
        self.keyword_label = ttk.Label(self.master, text="키워드 (필수):")
        self.keyword_label.grid(row=row_idx, column=0, sticky="w", padx=5, pady=5)
        self.keyword_entry = ttk.Entry(self.master, width=50)
        self.keyword_entry.grid(row=row_idx, column=1, sticky="ew", padx=5, pady=5)
        row_idx += 1

        # Target Audience
        self.target_audience_label = ttk.Label(self.master, text="대상 독자 (선택):")
        self.target_audience_label.grid(row=row_idx, column=0, sticky="w", padx=5, pady=5)
        self.target_audience_options = ["초보 개발자", "전문가", "일반 대중", "마케터", "기타 (직접 입력)"]
        self.target_audience_combobox = ttk.Combobox(self.master, values=self.target_audience_options, width=47)
        self.target_audience_combobox.grid(row=row_idx, column=1, sticky="ew", padx=5, pady=5)
        self.target_audience_combobox.set("일반 대중") # Default value
        row_idx += 1

        # Tone of Voice
        self.tone_of_voice_label = ttk.Label(self.master, text="어조 (선택):")
        self.tone_of_voice_label.grid(row=row_idx, column=0, sticky="w", padx=5, pady=5)
        self.tone_of_voice_options = ["전문적", "친근함", "유머러스", "객관적", "설득적"]
        self.tone_of_voice_combobox = ttk.Combobox(self.master, values=self.tone_of_voice_options, width=47)
        self.tone_of_voice_combobox.grid(row=row_idx, column=1, sticky="ew", padx=5, pady=5)
        self.tone_of_voice_combobox.set("전문적") # Default value
        row_idx += 1

        # Desired Length
        self.desired_length_label = ttk.Label(self.master, text="희망 길이 (선택):")
        self.desired_length_label.grid(row=row_idx, column=0, sticky="w", padx=5, pady=5)
        self.desired_length_options = ["짧게 (500-800 단어)", "보통 (800-1500 단어)", "길게 (1500+ 단어)"]
        self.desired_length_combobox = ttk.Combobox(self.master, values=self.desired_length_options, width=47)
        self.desired_length_combobox.grid(row=row_idx, column=1, sticky="ew", padx=5, pady=5)
        self.desired_length_combobox.set("보통 (800-1500 단어)") # Default value
        row_idx += 1

        # Number of Subheadings
        self.num_subheadings_label = ttk.Label(self.master, text="소제목 개수 (선택):")
        self.num_subheadings_label.grid(row=row_idx, column=0, sticky="w", padx=5, pady=5)
        self.num_subheadings_spinbox = ttk.Spinbox(self.master, from_=3, to=7, width=47)
        self.num_subheadings_spinbox.grid(row=row_idx, column=1, sticky="ew", padx=5, pady=5)
        self.num_subheadings_spinbox.set(5) # Default value
        row_idx += 1

        # SEO Optimization Level
        self.seo_level_label = ttk.Label(self.master, text="SEO 최적화 수준 (선택):")
        self.seo_level_label.grid(row=row_idx, column=0, sticky="w", padx=5, pady=5)
        self.seo_level_options = ["기본", "강화", "최대"]
        self.seo_level_combobox = ttk.Combobox(self.master, values=self.seo_level_options, width=47)
        self.seo_level_combobox.grid(row=row_idx, column=1, sticky="ew", padx=5, pady=5)
        self.seo_level_combobox.set("강화") # Default value
        row_idx += 1

        # Image Suggestion Preference
        self.image_pref_label = ttk.Label(self.master, text="이미지 제안 선호도 (선택):")
        self.image_pref_label.grid(row=row_idx, column=0, sticky="w", padx=5, pady=5)
        self.image_pref_options = ["Unsplash", "Pexels", "검색어만 추천"]
        self.image_pref_combobox = ttk.Combobox(self.master, values=self.image_pref_options, width=47)
        self.image_pref_combobox.grid(row=row_idx, column=1, sticky="ew", padx=5, pady=5)
        self.image_pref_combobox.set("검색어만 추천") # Default value
        row_idx += 1

        # Publishing Platform
        self.publishing_platform_label = ttk.Label(self.master, text="발행 플랫폼 (선택):")
        self.publishing_platform_label.grid(row=row_idx, column=0, sticky="w", padx=5, pady=5)
        self.publishing_platform_options = ["Markdown File Only", "Tistory", "WordPress"]
        self.publishing_platform_combobox = ttk.Combobox(self.master, values=self.publishing_platform_options, width=47)
        self.publishing_platform_combobox.grid(row=row_idx, column=1, sticky="ew", padx=5, pady=5)
        self.publishing_platform_combobox.set("Markdown File Only") # Default value
        row_idx += 1

        # Custom Instructions
        self.custom_instructions_label = ttk.Label(self.master, text="사용자 정의 지시사항 (선택):")
        self.custom_instructions_label.grid(row=row_idx, column=0, sticky="nw", padx=5, pady=5)
        self.custom_instructions_text = scrolledtext.ScrolledText(self.master, width=40, height=5, wrap=tk.WORD)
        self.custom_instructions_text.grid(row=row_idx, column=1, sticky="ew", padx=5, pady=5)
        row_idx += 1

        # Generate Button
        self.generate_button = ttk.Button(self.master, text="블로그 게시물 생성", command=self.generate_blog_post)
        self.generate_button.grid(row=row_idx, column=0, columnspan=2, pady=10)
        row_idx += 1 # Increment row_idx for the new output area

        # Output Display Area
        self.output_label = ttk.Label(self.master, text="결과:")
        self.output_label.grid(row=row_idx, column=0, sticky="nw", padx=5, pady=5)
        self.output_text = scrolledtext.ScrolledText(self.master, width=60, height=10, wrap=tk.WORD)
        self.output_text.grid(row=row_idx, column=1, sticky="ew", padx=5, pady=5)
        row_idx += 1

    def update_output(self, message):
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END) # Scroll to the end

    def generate_blog_post(self):
        self.update_output("블로그 게시물 생성을 시작합니다...")
        self.generate_button.config(state=tk.DISABLED) # Disable button during processing

        user_input = {
            "keyword": self.keyword_entry.get(),
            "target_audience": self.target_audience_combobox.get(),
            "tone_of_voice": self.tone_of_voice_combobox.get(),
            "desired_length": self.desired_length_combobox.get(),
            "num_subheadings": int(self.num_subheadings_spinbox.get()),
            "seo_optimization_level": self.seo_level_combobox.get(),
            "image_suggestion_preference": self.image_pref_combobox.get(),
            "publishing_platform": self.publishing_platform_combobox.get(),
            "custom_instructions": self.custom_instructions_text.get("1.0", tk.END).strip()
        }
        self.update_output("수집된 사용자 입력:")
        for key, value in user_input.items():
            self.update_output(f"  {key}: {value}")

        from src.core.pipeline import run_blog_post_pipeline
        
        # content_filepath is no longer needed as web search is integrated
        
        try:
            self.update_output("파이프라인 실행 중...")
            result = run_blog_post_pipeline(user_input=user_input)
            self.update_output(f"파이프라인 결과: {result}")
            self.update_output("블로그 게시물 생성이 완료되었습니다!")
        except Exception as e:
            self.update_output(f"오류 발생: {e}")
        finally:
            self.generate_button.config(state=tk.NORMAL) # Re-enable button

def run_gui():
    root = tk.Tk()
    app = BlogGenieGUI(root)
    root.mainloop()

if __name__ == "__main__":
    run_gui()
