# 📄 Resume Category Prediction App

An intelligent Streamlit-based web application that analyzes resumes (PDF/DOCX/TXT), predicts the job category using an ML model, scores the resume, and gives personalized improvement suggestions. It also includes a Career Booster Toolkit, feedback system, and a future-ready multi-language support option.

## 🚀 Features

- 📁 Upload resumes in **PDF, DOCX, or TXT**
- 🧠 Predicts job category using a trained **SVC model**
- 📈 Gives a **resume score out of 100**
- 💡 AI-powered **resume improvement suggestions**
- 📊 Real-time **analytics dashboard** (score and category trends)
- 📬 **Feedback form** with emoji rating
- 🧰 Career Booster Toolkit (resources, tips, resume builders)
- 🌐 Multi-language support (Coming Soon)
- 💻 Mobile-friendly and Streamlit Cloud deployable

---

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/resume-category-predictor.git
   cd resume-category-predictor
Install dependencies
pip install -r requirements.txt


Ensure the following files are present:

tfidf.pkl – TF-IDF Vectorizer

clf.pkl – Trained SVC Model

encoder.pkl – Label Encoder


📂 Folder Structure
resume-category-predictor/
│
├── app.py                  # Main Streamlit app
├── tfidf.pkl               # TF-IDF vectorizer
├── clf.pkl                 # Trained classifier
├── encoder.pkl             # Label encoder
├── requirements.txt        # Python dependencies
├── user_feedback.txt       # Saved user feedback
└── README.md               # Project documentation


📸 Screenshots
<img width="1888" height="1014" alt="image" src="https://github.com/user-attachments/assets/4d881ac8-62c8-4c9a-bdad-5372411c4392" />


🙌 Acknowledgements
Built using Streamlit, Scikit-learn, Matplotlib, and PyPDF2

Resume insights inspired by ATS and HR patterns

