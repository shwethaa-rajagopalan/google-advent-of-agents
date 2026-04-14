from google.adk.agents import Agent, LoopAgent
from google.adk.tools import FunctionTool, ToolContext

def approve_draft(tool_context: ToolContext) -> dict:
    tool_context.actions.escalate = True # Breaks the loop execution early
    return {"status": "success", "message": "Approved."}

writer = Agent(
    name='writer', model='gemini-3-flash-preview',
    instruction="Revise your draft based on feedback: {latest_feedback?}",
    output_key='latest_draft'
)

critic = Agent(
    name='critic', model='gemini-3-flash-preview',
    instruction=(
        "Evaluate draft: {latest_draft}. "
        "RUBRIC: 1. Must be sci-fi. 2. Must be under 100 words. "
        "If it FAILS, provide feedback. If it PASSES perfectly, call approve_draft."
    ),
    tools=[FunctionTool(approve_draft)],
    output_key='latest_feedback'
)

root_agent = LoopAgent(name="loop", sub_agents=[writer, critic], max_iterations=4)

from google.adk.apps import App
app = App(name="critic", root_agent=root_agent)