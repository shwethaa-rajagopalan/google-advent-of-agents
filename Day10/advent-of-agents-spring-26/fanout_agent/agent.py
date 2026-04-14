from google.adk.agents import Agent, ParallelAgent, SequentialAgent
from google.adk.tools import google_search

# 1. Define independent research agents with explicit output_keys and grounding tools
healthcare_researcher = Agent(name='healthcare_researcher', model='gemini-3-flash-preview', output_key='healthcare_research', tools=[google_search], instruction='Use the Google Search tool to...')
finance_researcher = Agent(name='finance_researcher', model='gemini-3-flash-preview', output_key='finance_research', tools=[google_search], instruction='Use the Google Search tool to...')

# 2. Fanout: Run them all concurrently
research_squad = ParallelAgent(
    name='research_squad',
    sub_agents=[healthcare_researcher, finance_researcher],
)

# 3. State Interpolation: Use `{output_key}` placeholders in the synthesizer prompt
synthesizer = Agent(
    name='synthesizer',
    model='gemini-3-flash-preview',
    instruction="Synthesize the following trends: \n\n{healthcare_research}\n\n{finance_research}",
)

# 4. Sequential block ensures fanout completes and populates state before synthesis
root_agent = SequentialAgent(
    name='root_agent',
    sub_agents=[research_squad, synthesizer],
)

from google.adk.apps import App
app = App(name="fanout", root_agent=root_agent)