from crewai import Crew,Agent,Task,LLM
from dotenv import load_dotenv
load_dotenv()
import os
gemini_api_key = os.getenv("GEMINI_API_KEY")
os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")
llm = LLM(
    api_key = gemini_api_key,
    model = "gemini/gemini-1.5-flash"
)


class BlogTranslation:
    def __init__(self):
        self.translator_agent = Agent(
            role = "Senior Traslator",
            goal = "Translate the blog post on the content {content} from English to {language}",
            backstory = (
                "As a Senior Translator, you have a deep understanding of languages and cultures. "
                "Your mission is to accurately translate the blog post on the content {content} from English to {language}, "
                "ensuring that the essence and meaning are preserved. "
                "You have a keen eye for detail and a passion for bridging language barriers."
                "and translate the blog post from English to {language}"
            ),
            llm = llm,
            vebose = True,
            allow_delegation = False
        )
        self.write_agent = Agent(
            role = "Senior Writer",
            goal = "Write a blog post on the content provided by senior translator in  marlkdown format",
            backstory = (
                "As a Senior Writer, you have a knack for weaving words into compelling narratives. "
                "Your mission is to take the translated content and craft it into an engaging blog post. "
                "You have a talent for storytelling and a deep understanding of your audience's needs. "
                "and write a blog post on the content provided by senior translator in  marlkdown format"
            ),
            llm = llm,
            verbose = True,
            allow_code_execution=False

        )
    def create_task(self,language):
        translation_task = Task(
            description = "Translate the blog post on the content {content} from English to {language}",
            expected_output = "Translated blog post on the content {content} in {language}",
            agent = self.translator_agent
        )
        writing_task = Task(
            description = "Write a blog post on the content provided by senior translator in  marlkdown format",
            expected_output = "A well structured blog post in {language} in markdown format",
            agent = self.write_agent,
            output_file = "translated_blog_post.md"
        )
        return translation_task, writing_task
    def kickoff(self,language,content):
        translate_task, writing_task = self.create_task(language)
        crew = Crew(
            agents = [self.translator_agent,self.write_agent],
            tasks = [translate_task,writing_task],
            verbose = True
        )
        result = crew.kickoff(inputs = {"content": content,'language':language})
        return result