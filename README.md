# crewai-to-notion
A Python script that saves your CrewAI agents crew output to a Notion Database

*Note this script uses the Open-Hermes-2.5 model from Nous Reasearch but you can use other models with CrewAI

# Intro
[CrewAI]([url](https://github.com/joaomdmoura/crewAI)https://github.com/joaomdmoura/crewAI) is a great new agents framework where you can create a "crew" of AI agents to perform a task.

I really love to use CrewAI, but I wanted away to easily save the output somewhere other than the dev console. So I created this simple script where you can automatically save the output of a CrewAI process to a Notion DB using the Notion Python SDK.

# Steps to use the script

1. pip install notion-client

2. Save Notion values
   * API Key
   * Database ID
   * Note Title (something that describes your agent process)

3. Switch the "Properties" field for the add_note_to_database function to the property name of the first column in your Notion DB (I just called mine "Title")

4. Run the file and your run will get saved to the specified Notion DB

