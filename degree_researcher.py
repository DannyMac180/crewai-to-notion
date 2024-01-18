import os
from crewai import Agent, Task, Crew, Process
from langchain_community.llms import Ollama
from notion_client import Client
from langchain_community.utilities.google_search import GoogleSearchAPIWrapper
from langchain.tools import DuckDuckGoSearchRun

# Initialize the Notion client with your integration token
notion = Client(auth="YOUR NOTION API KEY")
database_id = "6179c6f0db6d47f9be0c1eb97c088c15"  # Replace with your database ID
note_title = "CS Online Bachelor's Degrees"

# Function to add a note to the database
def add_note_to_database(database_id, title, content):
    new_page_data = {
        "parent": {"database_id": database_id},
        "properties": {
            "Title": {
                "title": [
                    {
                        "text": {
                            "content": title
                        }
                    }
                ]
            }
        },
        "children": [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": content
                            }
                        }
                    ]
                }
            }
        ]
    }
    # Use the Notion SDK to create a new page in the database
    notion.pages.create(**new_page_data)

# You can choose to use a local model through Ollama for example.
#
# from langchain.llms import Ollama
ollama_llm = Ollama(model="openhermes")

# Use DuckDuckGoSearchRun as a tool
search_tool = DuckDuckGoSearchRun()

# Define your agents with roles and goals
researcher = Agent(
  role='Senior Research Analyst',
  goal='Find prestigious and affordable unviversities that offer online Bachelor\'s degrees in Computer Science',
  backstory="""You are a guidance counselor at a high school in the US.
  You are helping a student find a prestigious and affordable university.
  The student is interested in pursuing a Bachelor's degree in Computer Science.
  The student is open to online programs, but they must be from a reputable university.""",
  verbose=True,
  allow_delegation=True,
  tools=[search_tool],
  llm=ollama_llm
  # You can pass an optional llm attribute specifying what mode you wanna use.
  # It can be a local model through Ollama / LM Studio or a remote
  # model like OpenAI, Mistral, Antrophic of others (https://python.langchain.com/docs/integrations/llms/)
  #
  # Examples:
  # llm=ollama_llm # was defined above in the file
  # llm=ChatOpenAI(model_name="gpt-3.5", temperature=0.7)
)
writer = Agent(
  role='University Admissions Officer',
  goal='Craft a compelling email to the student that lists the top 3 universities that offer online Bachelor\'s degrees in Computer Science',
  backstory="""You are an admissions officer at a prestigious university.
  You are responding to a student who is interested in pursuing a Bachelor's degree in Computer Science.
  The student is open to online programs, but they must be from a reputable university.""",
  verbose=True,
  allow_delegation=True,
  llm=ollama_llm
)

# Create tasks for your agents
task1 = Task(
  description="""Conduct a comprehensive analysis of the available online Bachelor's degrees in Computer Science.""",
  agent=researcher
)

task2 = Task(
  description="""Using the insights provided, develop an email that lists the top 3 universities that offer online Bachelor's degrees in Computer Science.""",
  agent=writer
)

# Instantiate your crew with a sequential process
crew = Crew(
  agents=[researcher, writer],
  tasks=[task1, task2],
  verbose=2, # You can set it to 1 or 2 to different logging levels
)

# Get your crew to work!
result = crew.kickoff()

print("######################")
print(result)

# Add the result to the database
add_note_to_database(database_id, note_title, result)
