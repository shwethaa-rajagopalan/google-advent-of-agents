from google.adk.agents import Agent, ParallelAgent, SequentialAgent

# We specify our target model once since child agents can inherit it.
from google.adk.agents import LlmAgent
LlmAgent.set_default_model('gemini-2.5-flash')

from google.adk.tools import google_search

# ==============================================================================
# NOTES: OUTPUT KEYS AND STATE
# ==============================================================================
# In ADK, Agents process information and return a text response. By default,
# this response is simply passed up the chain or back to the user.
#
# However, we choose to explicitly specify an `output_key` (e.g., output_key='healthcare_research')
# to tell the ADK runner to automatically save the agent's final text response
# into the current session's STATE dictionary under that specific key.
#
# This enables powerful data routing between nested agents:
# 1. Agent A runs and saves its output to output_key='x'
# 2. Agent B has {x} in its instruction prompt.
# 3. Before Agent B runs, ADK automatically interpolates the value of 'x'
#    from the state into Agent B's instructions!
#
# Let's see this in action below:
# ==============================================================================

healthcare_researcher = Agent(
    name='healthcare_researcher',
    description='Specializes in AI trends in healthcare',
    instruction='Use the Google Search tool to research how AI is impacting healthcare. Provide a simple, concise bulleted list of 2-3 key trends. Cite examples if possible.',
    output_key='healthcare_research',
    tools=[google_search],
)

finance_researcher = Agent(
    name='finance_researcher',
    description='Specializes in AI trends in finance',
    instruction='Use the Google Search tool to research how AI is impacting finance and banking. Provide a simple, concise bulleted list of 2-3 key trends. Cite examples if possible.',
    output_key='finance_research',
    tools=[google_search],
)

education_researcher = Agent(
    name='education_researcher',
    description='Specializes in AI trends in education',
    instruction='Use the Google Search tool to research how AI is impacting education. Provide a simple, concise bulleted list of 2-3 key trends. Cite examples if possible.',
    output_key='education_research',
    tools=[google_search],
)

# ==============================================================================
# NOTES: PARALLEL AGENT FANOUT
# ==============================================================================
# A ParallelAgent runs all of its sub_agents concurrently rather than in sequence.
# Since our researchers are making network calls to LLMs, running them in
# parallel saves a massive amount of time. All three researchers will fetch
# their trends simultaneously and populate their respective output_keys in the
# shared session state dictionary.
# ==============================================================================
research_squad = ParallelAgent(
    name='research_squad',
    description='A squad of researchers that run concurrently.',
    sub_agents=[healthcare_researcher, finance_researcher, education_researcher],
)

# ==============================================================================
# NOTES: STATE INTERPOLATION (SYNTHESIS)
# ==============================================================================
# Look closely at the instruction string below. Notice the curly braces placeholders:
# {healthcare_research}, {finance_research}, {education_research}
#
# These placeholders perfectly match the output_keys from our researchers above.
# Because the SequentialAgent guarantees the `research_squad` finishes BEFORE
# this `synthesizer` runs, the ADK will automatically gather those saved
# responses from the state dictionary and inject them into this prompt before
# calling the LLM.
# ==============================================================================
synthesizer = Agent(
    name='synthesizer',
    description='Takes compiled research and writes a final report.',
    instruction="""
    You are the Lead Editor. Read the aggregated research trends provided by the squad and synthesize them into a single, cohesive brief report titled "The AI Impact Matrix". Compare and contrast the trends where applicable:
    
    # Healthcare Research
    {healthcare_research}
    
    # Finance Research
    {finance_research}
    
    # Education Research
    {education_research}
    """,
)

# ==============================================================================
# NOTES: SEQUENTIAL EXECUTION
# ==============================================================================
# SequentialAgent executes agents in list order, passing the output of the previous to the next.
# Here, it guarantees that the parallel fanout runs to completion (populating the state)
# before the synthesizer ever starts, ensuring the synthesizer has the data it needs.
# ==============================================================================
root_agent = SequentialAgent(
    name='root_agent',
    description='The main pipeline that orchestrates the fanout and synthesis.',
    sub_agents=[research_squad, synthesizer],
)

from google.adk.apps import App

app = App(
    name="fanout",
    root_agent=root_agent
)

if __name__ == '__main__':
    # Provided for local testing if running directly with `uv run python` instead of `adk run`
    import asyncio
    from google.adk.runners import InMemoryRunner

    async def run_demo():
        runner = InMemoryRunner(app=app)
        # Using a dummy prompt because the agents are already hardcoded with specific instructions.
        print("Starting Parallel Fanout Demo...")
        await runner.run_debug("Please execute the AI trend research task.")

    asyncio.run(run_demo())
