# 🧠 AskFromPDF – Educational PDF Analyzer

**AskFromPDF** is a Python-based web application that analyzes educational PDFs (like IMO workbooks or quizzes) and extracts:
- ✅ Text-based questions
- 🖼 Images from each page
- 📊 Structured JSON outputs for AI and quiz generation

This tool is perfect for educators, ed-tech platforms, or developers who want to automate PDF content extraction for question banks or AI training datasets.

---

## 🚀 Features

- 📄 Extracts **text** from each PDF page
- 🖼 Detects and saves **images** from each page
- ✂️ Separates **question images** from **option images**
- 📦 Generates structured `final_output.json` with questions and image paths
- 🧪 Built-in **Streamlit UI** for ease of use

---

## 📂 Output JSON Format

Example:
```json
[
  {
    "page": 1,
    "question": "What is the next shape?",
    "image": "extracted/page1_question.png",
    "option_images": [
      "extracted/page1_option1.png",
      "extracted/page1_option2.png"
    ]
  }
]
