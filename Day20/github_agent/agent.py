import os, pathlib
from google.adk.agents import Agent, LoopAgent, SequentialAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.skills import load_skill_from_dir
from google.adk.tools import exit_loop
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from google.adk.tools.skill_toolset import SkillToolset
from mcp import StdioServerParameters

SKILLS_DIR = pathlib.Path(__file__).parent / "skills"

github_mcp = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="npx", args=["-y", "@modelcontextprotocol/server-github"],
            env={"GITHUB_PERSONAL_ACCESS_TOKEN": os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN", "")},
        ),
    ),
    tool_filter=["get_file_contents", "search_code", "list_commits"],
)

readme_skill = SkillToolset(
    skills=[load_skill_from_dir(SKILLS_DIR / "readme-conventions")]
)

async def init_loop_state(callback_context: CallbackContext) -> None:
    if "criticism" not in callback_context.state:
        callback_context.state["criticism"] = "No previous feedback. This is the first draft."

codebase_analyzer = Agent(
    model="gemini-3-flash-preview", name="codebase_analyzer",
    instruction="Analyze the GitHub repo. Read the file tree and key source files. Output a structured summary.",
    tools=[github_mcp], output_key="codebase_analysis",
)
readme_writer = Agent(
    model="gemini-3-flash-preview", name="readme_writer",
    before_agent_callback=init_loop_state,
    instruction="Write or improve the README using {codebase_analysis}. Address all points in {criticism}.",
    tools=[readme_skill], output_key="current_readme",
)
readme_critic = Agent(
    model="gemini-3-flash-preview", name="readme_critic",
    instruction="Review {current_readme} against the checklist. Call exit_loop if all sections pass.",
    tools=[exit_loop], output_key="criticism",
)

root_agent = SequentialAgent(
    name="readme_harness",
    sub_agents=[
        codebase_analyzer,
        LoopAgent(name="refinement_loop", sub_agents=[readme_writer, readme_critic], max_iterations=3),
    ],
)