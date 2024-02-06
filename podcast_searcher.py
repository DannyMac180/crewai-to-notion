import os
from crewai import Agent, Task, Crew, Process
from langchain_community.llms import Ollama
from notion_client import Client
from langchain_community.utilities.google_search import GoogleSearchAPIWrapper
from langchain.tools import DuckDuckGoSearchRun

# Initialize the Notion client with your integration token
notion = Client(auth="") # Replace with your Notion integration token
database_id = ""  # Replace with your database ID
note_title = "Podcast Search Results"

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

# Define your agent with a role and a backstory
podcast_finder = Agent(
  role='Podcast Curator',
  goal='Identify engaging and insightful podcasts across various genres for our listeners. These should not be the most popular podcasts that everyone already knows, but rather hidden gems that are worth discovering.',
  backstory="""As a Podcast Curator, you have a passion for audio storytelling and a keen ear for quality content. 
  You have experience in sifting through numerous podcast episodes to find those that truly stand out in terms of 
  content, production quality, and listener engagement. Your mission is to discover new and underappreciated podcasts 
  as well as to keep up with the popular ones that set the trends. You understand the diverse interests of listeners 
  and are adept at finding podcasts that cater to niche topics as well as those with broad appeal.""",
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

evaluator = Agent(
  role='Podcast Evaluator',
  goal='Assess the quality and relevance of podcasts found by the Podcast Curator.',
  backstory="""As a Podcast Evaluator, you have a critical ear and an eye for detail. You are skilled at analyzing listener feedback, 
  assessing audio quality, and determining the uniqueness of content. Your role is to ensure that only the best podcasts make it to our 
  recommended list.""",
  verbose=True,
  allow_delegation=True,
  llm=ollama_llm
)

summarizer = Agent(
  role='Content Summarizer',
  goal='Create concise summaries and highlights for each podcast.',
  backstory="""As a Content Summarizer, you have the ability to distill long audio content into engaging and informative summaries. 
  Your summaries help listeners quickly understand what a podcast episode is about and why it might be of interest to them.""",
  verbose=True,
  allow_delegation=True,
  llm=ollama_llm
)

# Define tasks for the agents
podcast_search_task = Task(
  description="Search for unique and engaging podcasts that are not widely known.",
  agent=podcast_finder
)

podcast_evaluate_task = Task(
  description="Evaluate the podcasts found for quality and relevance.",
  agent=evaluator
)

podcast_summarize_task = Task(
  description="Create concise summaries and highlights for the selected podcasts.",
  agent=summarizer
)

# Instantiate your crew with a sequential process
# Note: The order of agents and tasks should align with the workflow
crew = Crew(
  agents=[podcast_finder, evaluator, summarizer],
  tasks=[podcast_search_task, podcast_evaluate_task, podcast_summarize_task],
  verbose=2  # You can set it to 1 or 2 for different logging levels
)

# Get your crew to work!
result = crew.kickoff()

print("######################")
print("Crew Results:")
print(result)

# Add the result to the database
add_note_to_database(database_id, note_title, result)
