from crewai import Crew,Agent,Task,LLM
from crewai_tools import SerperDevTool
import os
from dotenv import load_dotenv
load_dotenv()
os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")
gemini_api_key = os.getenv("GEMINI_API_KEY")

llm = LLM(
    api_key=gemini_api_key,
    model="gemini/gemini-1.5-flash"
)

tool = SerperDevTool()

class BlogAutomation:
    def __init__(self):
        self.research_agent = Agent(
            role = "Senior Researcher",
            goal = "Research and gather information on the topic {topic}",
            backstory=(
                "Driven by curiosity and a thirst for knowledge, "
                "You are a Senior Researcher with a passion for uncovering the truth. "
                "Your mission is to explore the depths of information, "
                "delve into the unknown, and bring back valuable insights. "
                "and give a summary of the information you found on the topic {topic} "
            ),
            llm = llm,
            tools = [tool],
            verbose = True,
            allow_delegation=False
        )
        self.writing_agent = Agent(
            role = "Senior Writer",
            goal ="Write a blog post based on the research provided by the senior researcher",
            backstory=("As a Senior Writer, you have a knack for weaving words into compelling narratives. "
                "Your mission is to take the research findings and craft them into an engaging blog post. "
                "You have a talent for storytelling and a deep understanding of your audience's needs. "
                "and write a blog post based on the research provided."),
                llm = llm,
                verbose = True,
                allow_delegation=False
        )
    def create_task(self,topic):
        research_task = Task(
            description = "Research and gather information on the topic {topic}",
            expected_output="Summary of the information found on the topic {topic}",
            agent = self.research_agent,
            tools = [tool],
        )
        writing_task = Task(
            description = "Write a blog post based on the research provided by the senior researcher",
            expected_output = "A well structured blog post on the topic {topic} in markdown format",
            agent = self.writing_agent,
            output_file="blog_post.md"
        )
        return research_task, writing_task
    def kickoff(self,topic):
        research_task, writing_task = self.create_task(topic)
        crew = Crew(
           agents =[self.research_agent,self.writing_agent],
           tasks = [research_task, writing_task],
           verbose = True
       )
        result = crew.kickoff(inputs={'topic':topic})
        return result
        

