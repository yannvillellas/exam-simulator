#!/usr/bin/env python3
"""
Exam Simulator
This script simulates a quiz application using Tkinter.
It loads questions from a markdown file, displays them in a GUI,
and allows the user to select answers.
The application supports randomizing the order of questions,
and provides feedback on the user's answers.
"""
import os
import re
import random
import tkinter as tk
import argparse
from tkinter import ttk, messagebox

FOREGROUND_COLOR = "#CCCCCC"
BACKGROUND_COLOR = "#181818"
SUCCESS_COLOR = "#00C853"
ERROR_COLOR = "#D50000"

class ExamSimulator:
    """Simulates a quiz application using a Tkinter GUI."""

    def __init__(self, root, exam_file=None):
        self.root = root
        self.exam_file = exam_file

        if exam_file:
            if os.path.dirname(os.path.abspath(exam_file)) == os.path.abspath(os.getcwd()):
                self.root.title(f"Exam Simulator - {os.path.basename(exam_file)}")
            else:
                self.root.title(f"Exam Simulator - {os.path.basename(exam_file)} ({exam_file})")
        else:
            self.root.title("Exam Simulator")

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        width = max(int(screen_width * 0.8), 800)
        height = max(int(screen_height * 0.8), 600)

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.minsize(800, 600)

        self.root.resizable(False, False)
        self.result_shown = False

        self.window_width = width
        self.window_height = height

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.set_dark_mode()

        self.questions = []
        self.question_order = []
        self.current_question_index = 0
        self.selected_answer = tk.StringVar()
        self.score = 0
        self.randomized = False

        self.setup_ui()
        self.load_questions()
        self.show_question()

    def set_dark_mode(self):
        """Configure the user interface with dark mode theme colors."""
        self.root.configure(bg=BACKGROUND_COLOR)

        style = ttk.Style()
        style.theme_use('default')

        style.configure("TFrame", background=BACKGROUND_COLOR)
        style.configure("TLabel", background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR,
                       anchor="w", justify="left")

        style.configure("TRadiobutton", background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR,
                       anchor="w", justify="left")
        style.map("TRadiobutton",
                 background=[('active', BACKGROUND_COLOR)],
                 foreground=[('active', FOREGROUND_COLOR)])

        style.configure("TButton", background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)
        style.configure("TCheckbutton", background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)
        style.map("TCheckbutton",
                 background=[('active', BACKGROUND_COLOR)],
                 foreground=[('active', FOREGROUND_COLOR)])

    def setup_ui(self):
        """Set up the main user interface components and layout."""
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

        self.question_text = ttk.Label(
            self.main_frame,
            wraplength=self.window_width - 80,
            padding=(10, 10, 10, 10),
            font=("Arial", 12),
            anchor="w",
            justify="left"
        )
        self.question_text.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        self.answer_frame = ttk.Frame(self.main_frame)
        self.answer_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.answer_frame.grid_columnconfigure(0, weight=1)

        self.controls_frame = ttk.Frame(self.main_frame)
        self.controls_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=5)

        self.randomize_var = tk.BooleanVar(value=False)
        self.randomize_check = ttk.Checkbutton(
            self.controls_frame,
            text="Randomize Questions",
            variable=self.randomize_var,
            command=self.toggle_randomize
        )
        self.randomize_check.pack(side=tk.LEFT, padx=5)

        self.non_ai_var = tk.BooleanVar(value=False)
        self.non_ai_check = ttk.Checkbutton(
            self.controls_frame,
            text="Show only non-AI questions",
            variable=self.non_ai_var,
            command=self.toggle_non_ai_only
        )
        self.non_ai_check.pack(side=tk.LEFT, padx=5)

        self.restart_btn = ttk.Button(
            self.controls_frame,
            text="Restart Quiz",
            command=self.restart_quiz
        )
        self.restart_btn.pack(side=tk.RIGHT, padx=5)

        self.status_label = ttk.Label(self.main_frame, text="")
        self.status_label.grid(row=3, column=0, sticky="ew", padx=10, pady=5)

    def load_questions(self):
        """Load and parse questions from the markdown exam file."""
        if not self.exam_file:
            messagebox.showerror("Error", "No exam file specified")
            return

        if not os.path.exists(self.exam_file):
            messagebox.showerror("Error", f"Exam file not found at {self.exam_file}")
            return

        with open(self.exam_file, 'r', encoding='utf-8') as file:
            content = file.read()

        pattern = r"(\d+\.\s+.*?)(?=\n\d+\.\s+|\n##|\n### |\Z)"
        question_blocks = re.findall(pattern, content, re.DOTALL)

        self.questions = []
        for block in question_blocks:
            lines = block.strip().split("\n")
            if not lines or len(lines) < 2:
                continue
            is_ai = '[AI-Generated]' in lines[0]
            question_match = re.match(r"\d+\.\s+(.*)", lines[0])
            if not question_match:
                continue
            question_text = question_match.group(1).strip()
            options = []

            option_lines = []
            for line in lines[1:]:
                if re.match(r"^\s*\d+\.\s+", line):
                    option_text = re.sub(r"^\s*\d+\.\s+", "", line)
                    if option_text.strip():
                        option_lines.append(option_text.strip())

            if option_lines:
                options = option_lines
                correct_answer = 0
                self.questions.append({
                    "question": question_text,
                    "options": options,
                    "correct_answer": correct_answer,
                    "is_ai": is_ai
                })

        if not self.questions:
            messagebox.showerror("Error",
                f"No valid questions found in {self.exam_file}. Please check the file format.")
            return

        self.initialize_question_order()
        self.update_status()
        print(f"Loaded {len(self.questions)} questions from the exam file.")

    def toggle_randomize(self):
        """Toggle between randomized and sequential question order."""
        self.randomized = self.randomize_var.get()
        self.initialize_question_order()
        self.restart_quiz()

    def toggle_non_ai_only(self):
        """Toggle the filter to show only non-AI generated questions."""
        self.initialize_question_order()
        self.restart_quiz()

    def restart_quiz(self):
        """Reset the quiz to the beginning with current settings."""
        self.current_question_index = 0
        self.score = 0
        self.show_question()

    def initialize_question_order(self):
        """Set up the question sequence based on current randomization and filtering settings."""
        filtered = [i for i, q in enumerate(self.questions)
                    if not (self.non_ai_var.get() and q.get("is_ai"))]
        if self.randomized:
            self.question_order = filtered
            random.shuffle(self.question_order)
        else:
            self.question_order = filtered

    def get_current_question(self):
        """Get the current question data based on ordering and index."""
        if not self.questions or not self.question_order:
            return None

        actual_index = self.question_order[self.current_question_index]
        return self.questions[actual_index]

    def update_status(self):
        """Update the status bar with current score and question progress."""
        if self.non_ai_var.get():
            total = sum(1 for q in self.questions if not q.get("is_ai"))
            self.status_label.config(
                text=f"Score: {self.score}/{total} | "
                     f"Question {self.current_question_index + 1} of {total} "
                     f"(Non-AI only)"
            )
        else:
            self.status_label.config(
                text=f"Score: {self.score}/{len(self.questions)} | "
                     f"Question {self.current_question_index + 1} of {len(self.questions)} "
                     f"{'(Randomized)' if self.randomized else ''}"
            )

    def show_question(self):
        """Display the current question and its answer options in the UI."""
        for widget in self.answer_frame.winfo_children():
            widget.destroy()
        self.root.unbind("<Button-1>")
        self.answer_widgets = []
        self.result_shown = False
        if not self.questions:
            return
        question_data = self.get_current_question()
        self.question_text.config(
            text=f"Q{self.current_question_index + 1}: {question_data['question']}"
        )
        options_frame = ttk.Frame(self.answer_frame)
        options_frame.pack(fill=tk.BOTH, expand=True, anchor="w")
        options_frame.columnconfigure(0, weight=1)
        self.selected_answer.set("")
        options = list(enumerate(question_data["options"]))
        random.shuffle(options)
        self.shuffled_option_indices = [i for i, _ in options]
        for display_idx, (_orig_idx, option) in enumerate(options):
            frame = tk.Frame(options_frame, bg=BACKGROUND_COLOR)
            frame.grid(row=display_idx, column=0, sticky="ew", pady=5)
            radio = tk.Radiobutton(
                frame,
                text=option,
                variable=self.selected_answer,
                value=str(display_idx),
                command=self.on_radio_selected,
                wraplength=self.window_width - 80,
                anchor="w",
                justify="left",
                bg=BACKGROUND_COLOR,
                fg=FOREGROUND_COLOR,
                selectcolor=FOREGROUND_COLOR,
                font=("Arial", 12),
                highlightthickness=0,
                bd=0,
                activebackground=BACKGROUND_COLOR,
                activeforeground=FOREGROUND_COLOR
            )
            radio.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=10)
            icon_label = tk.Label(frame, text="", bg=BACKGROUND_COLOR, font=("Arial", 32), width=2)
            icon_label.pack(side=tk.LEFT, padx=0, ipadx=0, ipady=0)
            self.answer_widgets.append((radio, icon_label))
        self.update_status()

    def on_radio_selected(self):
        """Handle the selection of an answer option."""
        if self.result_shown:
            return
        answer = self.selected_answer.get()
        if answer:
            self.show_result(int(answer))

    def show_result(self, display_index):
        """Show the result of the selected answer and provide feedback."""
        question_data = self.get_current_question()
        correct_answer = question_data["correct_answer"]
        selected_option_index = self.shuffled_option_indices[display_index]
        is_correct = selected_option_index == correct_answer
        for radio, _ in self.answer_widgets:
            radio.config(state=tk.DISABLED)
        for i, (radio, icon_label) in enumerate(self.answer_widgets):
            orig_idx = self.shuffled_option_indices[i]
            if orig_idx == correct_answer:
                icon_label.config(text="✓", fg=SUCCESS_COLOR)
            elif i == display_index:
                icon_label.config(text="×", fg=ERROR_COLOR)
            else:
                icon_label.config(text="")
        if is_correct:
            self.score += 1
        self.update_status()
        self.result_shown = True
        self.root.bind("<Button-1>", lambda e: self.advance_to_next())

    def advance_to_next(self, _event=None):
        """Advance to the next question or show the final score."""
        self.root.unbind("<Button-1>")
        if self.current_question_index < len(self.question_order) - 1:
            self.current_question_index += 1
            self.show_question()
        else:
            if self.non_ai_var.get():
                total = sum(1 for q in self.questions if not q.get("is_ai"))
            else:
                total = len(self.questions)
            self.status_label.config(text=f"End | Final score: {self.score}/{total}")
            for radio, _ in getattr(self, 'answer_widgets', []):
                radio.config(state=tk.DISABLED)

    def on_window_resize(self, event):
        """Adjust UI elements when the window is resized."""
        self.window_width = event.width
        self.window_height = event.height
        self.question_text.config(wraplength=self.window_width - 20)
        for radio, _ in getattr(self, 'answer_widgets', []):
            radio.config(wraplength=self.window_width - 40)

def main():
    """Main entry point for the Exam Simulator application."""
    parser = argparse.ArgumentParser(description="Exam Simulator")
    parser.add_argument("-p", "--path", type=str, help="Path to the exam file")
    args = parser.parse_args()

    exam_file = args.path

    if not exam_file:
        current_dir_files = [f for f in os.listdir()
                            if f.endswith('.md') and f.lower() != 'readme.md']
        if current_dir_files:
            exam_file = current_dir_files[0]
            print(f"No path specified. Using file: {exam_file}")
        else:
            if os.path.exists('exams') and os.path.isdir('exams'):
                exam_dir_files = [os.path.join('exams', f) for f in os.listdir('exams')
                                 if f.endswith('.md') and f.lower() != 'readme.md']
                if exam_dir_files:
                    exam_file = exam_dir_files[0]
                    print(f"No path specified. Using file: {exam_file}")

    root = tk.Tk()
    ExamSimulator(root, exam_file=exam_file)
    root.mainloop()

if __name__ == "__main__":
    main()
