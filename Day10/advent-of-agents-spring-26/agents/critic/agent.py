from google.adk.agents import Agent, LoopAgent, SequentialAgent
from google.adk.tools import FunctionTool, ToolContext

# ==============================================================================
# NOTES: ESCALATING OUT OF LOOPS
# ==============================================================================
# ADK's `LoopAgent` wraps a sub-agent and runs it repeatedly up to `max_iterations`.
# To break out of this loop successfully before hitting the max, an agent can 
# use a Tool like this one. 
# Setting `tool_context.actions.escalate = True` tells the ADK runner to immediately
# halt the current execution context (the loop) and escalate control back to the 
# parent agent or caller.
# ==============================================================================

def approve_draft(tool_context: ToolContext) -> dict:
    """
    Call this tool when the draft completely meets the rubric and is approved.
    DO NOT CALL THIS IF THE DRAFT FAILS ANY RUBRIC CRITERIA.
    """
    tool_context.actions.escalate = True
    return {"status": "success", "message": "Draft approved. Escalating out of loop to finish."}

approve_tool = FunctionTool(approve_draft)

# ==============================================================================
# NOTES: STATE AND TEMPLATING IN LOOPS
# ==============================================================================
# By specifying `output_key='latest_feedback'` on the critic, we save its 
# feedback into the session state. We then inject that feedback back into the 
# writer's instruction. The ADK optional syntax `{var?}` ensures 
# the writer doesn't fail on its first run when feedback isn't available yet.
# ==============================================================================

writer = Agent(
    name='writer',
    model='gemini-2.5-flash',
    description='You are a creative sci-fi writer.',
    instruction=(
        "You are a sci-fi writer. Your job is to write a short story based on the user's prompt. "
        "IMPORTANT: If the critic provides feedback, revise your story strictly following their feedback. "
        "Do not explain yourself, just provide the revised story.\n\n"
        "Latest Feedback: {latest_feedback?}"
    ),
    output_key='latest_draft'
)

critic = Agent(
    name='critic',
    model='gemini-3.1-pro-preview',
    description='You are a strict editor and critic.',
    instruction=(
        "You evaluate the writer's draft against the following RUBRIC:\n"
        "1. The story must be a sci-fi story.\n"
        "2. The story must exactly contain the words: 'nebula', 'glitch', and 'chronometer'.\n"
        "3. The story must be very short, under 100 words.\n\n"
        "If the draft FAILS any criteria, output actionable feedback on what needs to be fixed. "
        "DO NOT approve the draft. "
        "If the draft PASSES all criteria perfectly, you MUST call the `approve_draft` tool to signal "
        "that the draft is approved and the loop can end.\n\n"
        "Current Draft to Evaluate:\n"
        "{latest_draft}"
    ),
    tools=[approve_tool],
    output_key='latest_feedback'
)

root_agent = LoopAgent(
    name="writer_critic_loop",
    sub_agents=[writer, critic],
    max_iterations=4
)

from google.adk.apps import App

app = App(
    name="critic",
    root_agent=root_agent
)

if __name__ == '__main__':
    # Provided for local testing if running directly with `uv run python` instead of `adk run`
    import asyncio
    from google.adk.runners import InMemoryRunner

    async def run_demo():
        runner = InMemoryRunner(app=app)
        print("Starting Critic Demo (Writer-Critic Loop)...")
        await runner.run_debug("Write me a story.")

    asyncio.run(run_demo())
