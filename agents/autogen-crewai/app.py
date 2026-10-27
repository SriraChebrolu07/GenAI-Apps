from crewai import Agent, Task, Crew, Process
from langchain.tools import DuckDuckGoSearchRun
from langchain_google_genai import ChatGoogleGenerativeAI
import os

# Initialize tools
search_tool = DuckDuckGoSearchRun()
llm = ChatGoogleGenerativeAI(model="gemini-pro",
                             verbose=True,
                             temperature=0.5,
                             google_api_key=os.getenv("GOOGLE_API_KEY"))

#Create Agents
coach = Agent(
    role='Senior Career Coach',
    goal="Discover and examine key tech and AI career skills for 2024",
    backstory="You're an expert in spotting new trends and essential skills in AI and technology.",
    verbose=True,
    allow_delegation=False,
    tools=[search_tool],
    llm=llm
)

influencer = Agent(
    role='LinkedIn post creator',
    goal="Write catchy, emoji-filled LinkedIn posts within 200 words",
    backstory="You're a specialised writer on LinkedIn, focusing on AI and technology.",
    verbose=True,
    allow_delegation=True,
    llm=llm
)

critic = Agent(
    role='Expert Writing Critic',
    goal="Give constructive feedback on post drafts",
    backstory="You're skilled in offering straightforward, effective advice to tech writers. Ensure posts are concise, under 200 words, with emojis and hashtags.",
    verbose=True,
    allow_delegation=True,
    llm=llm
)

#Create Tasks with expected_output
task_search = Task(
    description="Compile a report listing at least 5 new AI and tech skills, presented in bullet points",
    expected_output="A bullet-pointed report of new AI and tech skills",
    agent=coach
)

task_post = Task(
    description="Create a LinkedIn post with a brief headline and a maximum of 200 words, focusing on upcoming AI and tech skills",
    expected_output="A concise LinkedIn post about AI and tech skills",
    agent=influencer
)

task_critique = Task(
    description="Refine the post for brevity, ensuring an engaging headline (no more than 30 characters) and keeping within a 200-word limit",
    expected_output="A refined, engaging LinkedIn post under 200 words",
    agent=critic
)

# Create Crew
crew = Crew(
    agents=[coach, influencer, critic],
    tasks=[task_search, task_post, task_critique],
    verbose=2,
    process=Process.sequential
)

# Execute the tasks
result = crew.kickoff()

print("#############")
print(result)
