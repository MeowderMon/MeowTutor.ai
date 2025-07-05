# 🐾 MeowTutor.ai — AI PDF Tutor + Quiz Generator

**MeowTutor.ai** is an AI-powered Streamlit app that lets you:

- Upload **any PDF** — readable, scanned, or handwritten
- **Chat with an AI tutor** based on its content
- **Generate quizzes** with multiple difficulty levels and questions
- Works even if the PDF has **no selectable text** (uses OCR fallback)


## 🔥 Features

- 🧬 **Neural Read Mode** — Ask questions to an AI Tutor
- 🎯 **Quiz Attack Mode** — Generate customizable MCQs
- 🧠 **OCR Support** — Reads scanned/handwritten/image-based PDFs
- ✏️ **Custom Funky UI** — Cyberpunk CSS design
- 🪄 **Smart Fallbacks** — Uses PyPDF2 → PyMuPDF → OCR fallback


## 📦 Python Dependencies

Install Python packages with:

```bash
pip install -r requirements.txt
```

## 📦 System Requirements

Install these manually before running the app:

### Windows:

- [Poppler](https://github.com/oschwartz10612/poppler-windows/releases)  
  ➤ Add `C:\poppler-xx\Library\bin` to **System PATH**

- [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki)  
  ➤ Add `C:\Program Files\Tesseract-OCR` to **System PATH**



## 🚀 Getting Started

1. **Clone this repo:**

```bash
git clone https://github.com/yourusername/meowtutor-ai.git
cd meowtutor-ai
```

2. **(Recommended) Create a virtual environment:**

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Run the app:**

```bash
streamlit run app.py
```

5. **Open in your browser:**
Usually at [http://localhost:8501](http://localhost:8501)


## ⚡️ Troubleshooting

- **OCR not working?**
Make sure Tesseract & Poppler are installed and added in Environment Variable.
- **`venv/` or `.pyc` files showing in git?**
Make sure your `.gitignore` includes:


## 🤝 Contributing

Pull requests are welcome!
Open an issue for feature requests or bugs.

## 📄 License

MIT License

## 🙏 Credits

- [Streamlit](https://streamlit.io/)
- [PyPDF2](https://pypdf2.readthedocs.io/)
- [PyMuPDF](https://pymupdf.readthedocs.io/)
- [pdf2image](https://github.com/Belval/pdf2image)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [Poppler](https://poppler.freedesktop.org/)

**Made with ❤️ by [The MeowdarMons]**
