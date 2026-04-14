from google.adk.tools import AgentTool
from google.adk.tools import google_search
from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.apps import App

# The Planner is used purely as a tool by the Manager
planner = LlmAgent(
    name='planner',
    model='gemini-3-flash-preview',
    instruction='Break the user prompt into exactly three distinct research themes.'
)

# Define sub-agents for execution
researcher = LlmAgent(
    name='researcher', 
    model='gemini-3-flash-preview', 
    tools=[google_search], 
    instruction='Research the assigned topic step-by-step.'
)
synthesizer = LlmAgent(
    name='synthesizer', 
    model='gemini-3-flash-preview', 
    instruction='Synthesize the findings into a cohesive report.'
)

# A logical pipeline of sub-agents to handle execution
execution_pipeline = SequentialAgent(
    name='execution_pipeline',
    sub_agents=[researcher, synthesizer]
)

# The Manager orchestrates the whole flow autonomously
manager = LlmAgent(
    name='manager',
    model='gemini-3-flash-preview',
    tools=[AgentTool(planner)],
    sub_agents=[execution_pipeline],
    instruction='''
    1. Use the planner tool to create a detailed research plan based on the user's prompt.
    2. Activate your execution_pipeline sub-agent and pass the completed plan to it so it can execute it.
    '''
)

root_agent = manager
app = App(name="hierarchical", root_agent=root_agent)