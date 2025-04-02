import os
import sys
import streamlit as st

# Force Python to use pysqlite3 instead of the system sqlite3
__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
from crewai.flow.flow import Flow, start, listen
from pydantic import BaseModel
from blog_automation import BlogAutomation
from blog_translate import BlogTranslation


st.set_page_config(page_title="AI Blog Generator", page_icon="📝", layout="wide")


class MainBlogState(BaseModel):
    topic: str = ""
    language: str = ""
    blog_content: str = ""
    translated_blog_content: str = ""


class MainBlogFlow(Flow[MainBlogState]):
    def __init__(self, topic: str, language: str):
        super().__init__()
        self.topic = topic  
        self.language = language

    @start()
    def initialise_state(self):
        self.state.topic = self.topic  
        self.state.language = self.language

    @listen(initialise_state)
    def create_blog(self):
        blog_automation = BlogAutomation()
        blog_content = blog_automation.kickoff(self.state.topic)
        self.state.blog_content = blog_content.raw

    @listen(create_blog)
    def translate_blog(self):
        blog_translation = BlogTranslation()
        translated_blog_content = blog_translation.kickoff(self.state.language, self.state.blog_content)
        self.state.translated_blog_content = translated_blog_content.raw


def main():
    st.markdown("<h1 style='text-align: center; color: #444444;'>📝 AI-Powered Blog Generator & Translator</h1>", unsafe_allow_html=True)

  
    with st.sidebar:
        st.markdown("### ✨ **Customize Your Blog**")
        topic = st.text_input("📌 Enter Blog Topic", "AI in Healthcare")
        language = st.text_input("🌎 Enter Target Language", "French")
        generate_btn = st.button("🚀 Generate & Translate Blog")

    
    if "blog_content" not in st.session_state:
        st.session_state.blog_content = ""
    if "translated_blog_content" not in st.session_state:
        st.session_state.translated_blog_content = ""
    if "language" not in st.session_state:
        st.session_state.language = ""

    if generate_btn:
        with st.spinner("⏳ Generating and Translating Blog... Please wait."):
            flow = MainBlogFlow(topic, language)
            result = flow.kickoff()

            
            st.session_state.blog_content = flow.state.blog_content
            st.session_state.translated_blog_content = flow.state.translated_blog_content
            st.session_state.language = language  

            st.success("✅ Blog Successfully Generated & Translated!")

    
    if st.session_state.blog_content:
        st.markdown("<hr style='border:1px solid #ccc;'>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📄 **Generated Blog (English)**")
            st.text_area("", st.session_state.blog_content, height=350, key="english")

        with col2:
            st.subheader(f"🌍 **Translated Blog ({st.session_state.language})**")
            st.text_area("", st.session_state.translated_blog_content, height=350, key="translated")

        
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            st.download_button(
                "⬇️ Download English Blog",
                st.session_state.blog_content,
                file_name="blog_en.md",
                mime="text/markdown"
            )

        with col2:
            st.download_button(
                f"⬇️ Download {st.session_state.language} Blog",
                st.session_state.translated_blog_content,
                file_name=f"blog_{st.session_state.language}.md",
                mime="text/markdown"
            )

if __name__ == "__main__":
    main()
