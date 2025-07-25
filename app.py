import streamlit as st
import pickle
import PyPDF2
import re
import datetime
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd

# ✅ Stopwords
stop_words = set(ENGLISH_STOP_WORDS)

# 📊 Global Analytics State
if 'resume_data' not in st.session_state:
    st.session_state.resume_data = []

# 🩹 Clean Resume Text
def cleanResume(txt):
    cleanText = re.sub(r'http\S+\s', ' ', txt)
    cleanText = re.sub(r'RT|cc', ' ', cleanText)
    cleanText = re.sub(r'#\S+\s', ' ', cleanText)
    cleanText = re.sub(r'@\S+', ' ', cleanText)
    cleanText = re.sub(r'[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', cleanText)
    cleanText = re.sub(r'[^\x00-\x7f]', ' ', cleanText)
    cleanText = re.sub(r'\s+', ' ', cleanText)
    cleanText = cleanText.lower()
    words = cleanText.split()
    words = [word for word in words if word not in stop_words and len(word) > 2]
    return ' '.join(words)

# 📄 Extract text from files
def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    return ' '.join(page.extract_text() for page in pdf_reader.pages)

def extract_text_from_docx(file):
    from docx import Document
    doc = Document(file)
    return '\n'.join([p.text for p in doc.paragraphs])

def extract_text_from_txt(file):
    try:
        return file.read().decode('utf-8')
    except UnicodeDecodeError:
        return file.read().decode('latin-1')

# 📁 File upload handler
def handle_file_upload(uploaded_file):
    ext = uploaded_file.name.split('.')[-1].lower()
    if ext == 'pdf':
        return extract_text_from_pdf(uploaded_file)
    elif ext == 'docx':
        return extract_text_from_docx(uploaded_file)
    elif ext == 'txt':
        return extract_text_from_txt(uploaded_file)
    else:
        raise ValueError("❌ Unsupported file type. Please upload PDF, DOCX, or TXT.")

# 🔮 Predict category
def predict_category(resume_text):
    cleaned_text = cleanResume(resume_text)
    vectorized_text = tfidf.transform([cleaned_text])
    prediction = svc_model.predict(vectorized_text.toarray())
    return le.inverse_transform(prediction)[0], cleaned_text

# 🧐 Resume suggestions (AI-like rules)
def generate_resume_tips(text):
    tips = []
    if len(text.split()) < 150:
        tips.append("📄 Your resume seems short. Try to add more relevant experience or skills.")
    if "objective" not in text.lower():
        tips.append("🎯 Consider adding an 'Objective' or 'Career Summary' section.")
    if "project" not in text.lower():
        tips.append("💼 Include academic or personal projects to showcase your practical experience.")
    if "intern" not in text.lower():
        tips.append("📌 If you've done any internships, make sure to mention them.")
    if "lead" not in text.lower() and "manage" not in text.lower():
        tips.append("💼 Use leadership/action words like 'led', 'managed', or 'coordinated'.")
    if len(tips) == 0:
        tips.append("✅ Your resume looks well structured. Great job!")
    return tips

# 📈 Resume Scoring System
def score_resume(text):
    score = 50
    if len(text.split()) > 200:
        score += 20
    if any(x in text.lower() for x in ["objective", "summary"]):
        score += 10
    if "project" in text.lower():
        score += 10
    if "intern" in text.lower():
        score += 10
    return min(score, 100)

# 🧐 Load model and encoder
tfidf = pickle.load(open('tfidf.pkl', 'rb'))
svc_model = pickle.load(open('clf.pkl', 'rb'))
le = pickle.load(open('encoder.pkl', 'rb'))

# 🌐 Main App
def main():
    st.set_page_config(page_title="Resume Category Prediction", page_icon="📄", layout="wide")
    st.title("📄 Resume Category Prediction App")

    # Sidebar Navigation
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/194/194931.png", width=100)
        st.markdown("### Hello! Welcome to the Resume App 👋")

        st.markdown("---")
        menu_option = st.radio("📂 Choose a section:", [
            "Resume Analysis",
            "Analytics Dashboard",
            "Career Booster Toolkit",
            "Multi-language Support (Coming Soon)"
        ])

        st.markdown("---")
        st.markdown("📌 Project by: [Subrav bhande](https://github.com/subravbhande)")
        st.markdown("📁 [GitHub Repo](https://github.com/subravbhande/resume-predictor-app)")
        st.markdown("<center>Made with ❤️ for you</center>", unsafe_allow_html=True)

        # Feedback last
        with st.expander("📬 Give Feedback"):
            if "feedback_submitted" not in st.session_state:
                st.session_state.feedback_submitted = False

            if not st.session_state.feedback_submitted:
                st.markdown("### How would you rate the app?")
                rating = st.radio("Your Rating:", ["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"], index=None, horizontal=True)

                liked_features = st.multiselect(
                    "What did you like the most?",
                    ["Resume Prediction", "UI Design", "Resume Tips", "Resume Builder Links", "Ease of Use"]
                )

                feedback_text = st.text_area("Any suggestions or feedback?")

                if st.button("Send Feedback"):
                    if rating is None:
                        st.warning("⚠️ Please provide a rating.")
                    elif not liked_features:
                        st.warning("⚠️ Please select what you liked.")
                    else:
                        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        with open("user_feedback.txt", "a", encoding="utf-8") as f:
                            f.write(f"Time: {now}\n")
                            f.write(f"Rating: {rating}\n")
                            f.write(f"Liked: {', '.join(liked_features)}\n")
                            f.write(f"Feedback: {feedback_text}\n")
                            f.write("-" * 60 + "\n")
                        st.session_state.feedback_submitted = True
                        st.rerun()
            else:
                st.success("🎉 Thank you! Your feedback has been submitted.")

    # Section: Resume Analysis
    if menu_option == "Resume Analysis":
        st.subheader("📁 Upload your resume below")
        uploaded_file = st.file_uploader("Drag and drop your file here", type=["pdf", "docx", "txt"])

        if uploaded_file is not None:
            try:
                resume_text = handle_file_upload(uploaded_file)
                category, cleaned_text = predict_category(resume_text)
                tips = generate_resume_tips(resume_text)
                score = score_resume(resume_text)

                st.success("✅ Resume processed successfully!")

                if st.checkbox("🔍 Show extracted resume text"):
                    st.text_area("Extracted Resume Text", resume_text, height=300)

                st.subheader("🌟 Predicted Category")
                st.write(f"**🧠 {category}**")

                st.subheader("📈 Resume Score")
                st.progress(score)
                st.info(f"Your resume score is **{score}/100**")

                st.subheader("💡 AI Resume Suggestions")
                for tip in tips:
                    st.markdown(f"- {tip}")

                st.session_state.resume_data.append({
                    'category': category,
                    'score': score,
                    'length': len(cleaned_text.split())
                })

            except Exception as e:
                st.error(f"❌ Error: {e}")

    elif menu_option == "Analytics Dashboard":
        st.subheader("📊 Resume Analytics Dashboard")
        data = st.session_state.resume_data
        if data:
            df = pd.DataFrame(data)

            col1, col2 = st.columns(2)

            with col1:
                st.metric("📄 Total Resumes Uploaded", len(df))
                st.metric("🧮 Average Resume Score", f"{df['score'].mean():.2f}/100")

            with col2:
                fig, ax = plt.subplots()
                category_counts = df['category'].value_counts()
                ax.bar(category_counts.index, category_counts.values, color='skyblue')
                ax.set_title("Top Predicted Categories")
                ax.set_ylabel("Count")
                st.pyplot(fig)

            st.bar_chart(df['length'], use_container_width=True)
        else:
            st.info("Upload at least one resume to see analytics.")

    elif menu_option == "Career Booster Toolkit":
        st.subheader("🚀 Career Booster Toolkit")
        st.markdown("Comprehensive resources to boost your career growth, learning, and visibility.")

        with st.expander("🎓 Skill Development Platforms"):
            st.markdown("- [Coursera](https://coursera.org)")
            st.markdown("- [edX](https://edx.org)")
            st.markdown("- [Udemy](https://udemy.com)")
            st.markdown("- [freeCodeCamp](https://www.freecodecamp.org/)")
            st.markdown("- [Kaggle Learn](https://www.kaggle.com/learn)")

        with st.expander("💼 Resume & Portfolio Builders"):
            st.markdown("- [Canva Resume Builder](https://www.canva.com/resumes/)")
            st.markdown("- [Novoresume](https://novoresume.com/)")
            st.markdown("- [Zety](https://zety.com/resume-builder)")
            st.markdown("- [GitHub Portfolio Guide](https://github.com/emmabostian/developer-portfolios)")
            st.markdown("- [Notion Portfolio Template](https://www.notion.so)")

        with st.expander("🧠 Mock Interviews & Practice"):
            st.markdown("- [InterviewBit](https://www.interviewbit.com/)")
            st.markdown("- [Pramp](https://www.pramp.com/)")
            st.markdown("- [Exercism](https://exercism.io/)")
            st.markdown("- [GeeksforGeeks Practice](https://practice.geeksforgeeks.org/)")

        with st.expander("🗂️ Contribute to Open Source"):
            st.markdown("- [First Contributions](https://firstcontributions.github.io/)")
            st.markdown("- [Up-for-Grabs](https://up-for-grabs.net/)")
            st.markdown("- [CodeTriage](https://www.codetriage.com/)")
            st.markdown("- [EddieHub](https://github.com/EddieHubCommunity)")

        with st.expander("🌐 Build Your Network"):
            st.markdown("- [LinkedIn](https://linkedin.com)")
            st.markdown("- [AngelList](https://angel.co/)")
            st.markdown("- [Twitter - Dev Community](https://twitter.com/search?q=developer)")
            st.markdown("- [Polywork](https://www.polywork.com/)")

        with st.expander("📈 Trending Tech & Career Insights"):
            st.markdown("- [Stack Overflow Survey](https://insights.stackoverflow.com/survey)")
            st.markdown("- [GitHub Octoverse](https://octoverse.github.com/)")
            st.markdown("- [TechRadar](https://www.techradar.com/)")
            st.markdown("- [Google Trends](https://trends.google.com/)")

        with st.expander("🤖 AI-Powered Career Advice Tools"):
            st.markdown("- [ChatGPT](https://chat.openai.com)")
            st.markdown("- [Jasper.ai](https://www.jasper.ai/)")
            st.markdown("- [Kickresume](https://www.kickresume.com/)")
            st.markdown("- [Resume Worded](https://www.resumeworded.com/)")

        with st.expander("📆 Productivity & Planning Tools"):
            st.markdown("- [Notion](https://www.notion.so)")
            st.markdown("- [Trello](https://trello.com/)")
            st.markdown("- [Pomofocus](https://pomofocus.io/)")
            st.markdown("- [Todoist](https://todoist.com/)")

        st.markdown("---")
        st.info("💡 Tip: Bookmark this toolkit or export it to Notion/Google Keep to use daily.")

    elif menu_option == "Multi-language Support (Coming Soon)":
        st.subheader("🌐 Multi-language Support")
        st.markdown("This feature is coming soon! You'll be able to select and analyze resumes in different languages.")
        st.selectbox("Choose your preferred language:", ["English", "Hindi", "Tamil", "Telugu", "Marathi"], index=0, disabled=True)

if __name__ == '__main__':
    main()
