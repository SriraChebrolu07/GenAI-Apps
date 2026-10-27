from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import DuckDuckGoSearchRun
from crewai import Agent, Task, Crew, Process
import os

# Initialize tools
search_tool = DuckDuckGoSearchRun()
llm = ChatGoogleGenerativeAI(model="gemini-pro",
                             verbose=True,
                             temperature=0.5,
                             google_api_key=os.getenv("GOOGLE_API_KEY"))

# Create Agents
influencer = Agent(
    role='LinkedIn post creator',
    goal="Write attractive, emoji-filled LinkedIn posts within 200 words",
    backstory="You're a specialized writer on LinkedIn, focusing on python, AI and technology.",
    verbose=True,
    allow_delegation=False,  # We're not delegating this task
    llm=llm
)

# Create Task for creating a LinkedIn post
task_post = Task(
    description="Create a LinkedIn post with a brief headline and a maximum of 200 words, focusing on upcoming AI and tech skills",
    expected_output="A concise LinkedIn post about AI and tech skills",
    agent=influencer
)

# Create a Crew with only the LinkedIn post task
crew = Crew(
    agents=[influencer],
    tasks=[task_post],
    verbose=2,
    process=Process.sequential
)

# Execute the task to create the LinkedIn post
result = crew.kickoff()

print("#############")
print(result)
