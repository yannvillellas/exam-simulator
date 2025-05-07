# Exam Simulator

This is a simple exam simulator application that loads questions from a markdown file and presents them in a user-friendly GUI interface. The application supports randomizing questions, filtering out AI-generated questions, and provides immediate feedback on answers.

## Features

- Load exam questions from a markdown file
- Randomize question order
- Filter out AI-generated questions
- Interactive GUI with immediate feedback
- Track score throughout the exam
- Dark mode interface

## Requirements

- Python 3.x
- Tkinter (usually included with Python, but may need to be installed separately on some Linux distributions)

For Linux users who don't have Tkinter installed:

```bash
# Debian/Ubuntu
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter

# Arch Linux
sudo pacman -S tk
```

## Installation

```bash
git clone https://github.com/yourusername/exam-simulator.git
cd exam-simulator
```

## Usage

Run the simulator with a specified exam file:

```bash
python exam.py -p path/to/your/exam_file.md
```

or

```bash
python exam.py --path path/to/your/exam_file.md
```

> **Warning:** If you run the program without specifying an exam file, it will automatically search for and use the first .md file it finds in the current directory (excluding README.md). If no .md files are found in the current directory, it will look in the 'exams' folder. This automatic selection can lead to unexpected behavior if multiple .md files are present.

## Markdown File Format

The exam simulator expects a specific format for the markdown file containing questions:

### Basic Structure

```markdown
## Section Title (optional)

1. Question text here?

   1. Correct Answer (always the first option)
   2. Wrong Option
   3. Wrong Option
   4. Wrong Option

2. [AI-Generated] Another question here?

   1. Correct Answer (always the first option)
   2. Wrong Option
   3. Wrong Option
   4. Wrong Option
```

### Format Rules

1. Each question starts with a number followed by a period (e.g., `1.`, `2.`)
2. Options should be indented and numbered (e.g., `1.`, `2.`)
3. **The first option is always the correct answer** (the order will be randomized when displayed)
4. If a question is AI-generated, add `[AI-Generated]` in the question text
5. Questions can be organized under section headings (`##`, `###`)
6. Questions must be separated by a blank line

### Example

```markdown
## Mathematics

1. What is 2 + 2?

   1. 4 (this is the correct answer)
   2. 3
   3. 5
   4. 6

2. [AI-Generated] What is the square root of 16?

   1. 4 (this is the correct answer)
   2. 2
   3. 6
   4. 8
```

## User Interface

- **Randomize Questions**: Toggle to randomize the order of questions
- **Show only non-AI questions**: Toggle to filter out AI-generated questions
- **Restart Quiz**: Restart the quiz with current settings
- **Click anywhere**: After selecting an answer, click anywhere to proceed to the next question

## Directory Structure

You can organize your exam files however you prefer. Here's a suggested structure:

```bash
exam-simulator/
├── exam.py
├── README.md
└── exams/
    └── your_exam_file.md
```

But you can place your exam files anywhere and reference them with the full path:

```bash
python exam.py -p /path/to/any/location/your_exam_file.md
```

## License

[MIT License](LICENSE)
