from crewai.flow.flow import Flow,start,listen
from pydantic import BaseModel
from blog_automation import BlogAutomation
from blog_translate import BlogTranslation
import time

class MainBlogState(BaseModel):
    topic: str = ""
    language: str = ""
    blog_content: str = ""
    translated_blog_content: str = ""

class MainBlogFlow(Flow[MainBlogState]):
    @start()
    def initialise_state(self):
        self.state.topic = "AI in Healthcare"
        self.state.language = "French"
    @listen(initialise_state)
    def create_blog(self):
        blog_automation = BlogAutomation()
        blog_content = blog_automation.kickoff(self.state.topic)
        self.state.blog_content = blog_content.raw
    @listen(create_blog)
    def translate_blog(self):
        blog_translation = BlogTranslation()
        translated_blog_content = blog_translation.kickoff(self.state.language,self.state.blog_content)
        self.state.blog_content = translated_blog_content.raw
flow = MainBlogFlow()
if __name__ == "__main__":
    result = flow.kickoff()
