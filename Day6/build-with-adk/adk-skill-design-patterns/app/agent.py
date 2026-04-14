"""5 Skill Design Patterns — ADK Demo Agent.

One agent, five skills, five design patterns. Each skill demonstrates
a different pattern for structuring SKILL.md content:

1. Tool Wrapper (api-expert) — wraps library best practices
2. Generator (report-generator) — produces structured output from templates
3. Reviewer (code-reviewer) — evaluates against a checklist
4. Inversion (project-planner) — interviews the user before acting
5. Pipeline (doc-pipeline) — chains multiple steps in sequence

All 5 skills are loaded into a single SkillToolset. The agent decides
which skill to activate based on the user's request, using progressive
disclosure: L1 (descriptions) → L2 (instructions) → L3 (references/assets).

Companion code for: https://lavinigam.com/posts/adk-skill-design-patterns/
"""

import pathlib

from google.adk import Agent
from google.adk.skills import load_skill_from_dir
from google.adk.tools.skill_toolset import SkillToolset

SKILLS_DIR = pathlib.Path(__file__).parent / "skills"

# --- Load all 5 skills from their directories ---
# Each skill follows the Agent Skills spec (agentskills.io):
#   SKILL.md (required) + references/ + assets/ (optional)
# The directory name MUST match the `name` field in SKILL.md frontmatter.

# Pattern 1: Tool Wrapper — wraps a library's conventions
api_expert = load_skill_from_dir(SKILLS_DIR / "api-expert")

# Pattern 2: Generator — produces structured output from templates
report_generator = load_skill_from_dir(SKILLS_DIR / "report-generator")

# Pattern 3: Reviewer — evaluates code against a checklist
code_reviewer = load_skill_from_dir(SKILLS_DIR / "code-reviewer")

# Pattern 4: Inversion — interviews the user, then synthesizes
project_planner = load_skill_from_dir(SKILLS_DIR / "project-planner")

# Pattern 5: Pipeline — multi-step sequential workflow
doc_pipeline = load_skill_from_dir(SKILLS_DIR / "doc-pipeline")

# --- Compose into a single SkillToolset ---
# SkillToolset auto-registers 3 tools:
#   list_skills      → L1: agent sees all skill names + descriptions
#   load_skill       → L2: agent loads full instructions when needed
#   load_skill_resource → L3: agent loads references/assets on demand
#
# The agent pays zero context cost for unused skills —
# only the ~100 token description is loaded at startup.

skill_toolset = SkillToolset(
    skills=[
        api_expert,       # Pattern 1: Tool Wrapper
        report_generator, # Pattern 2: Generator
        code_reviewer,    # Pattern 3: Reviewer
        project_planner,  # Pattern 4: Inversion
        doc_pipeline,     # Pattern 5: Pipeline
    ],
)

# --- Agent Definition ---
root_agent = Agent(
    model="gemini-2.5-flash",
    name="pattern_demo_agent",
    description="A developer assistant powered by 5 skill design patterns.",
    instruction=(
        "You are a developer assistant with access to specialized skills. "
        "For every user request:\n"
        "\n"
        "1. Review the available skills to find the best match.\n"
        "2. Load the matching skill's full instructions.\n"
        "3. Follow the skill's instructions step by step.\n"
        "4. Use load_skill_resource to access reference files and templates "
        "when the skill instructions tell you to.\n"
        "\n"
        "Available skill patterns:\n"
        "- api-expert: FastAPI best practices (ask about APIs)\n"
        "- report-generator: Structured reports (ask to write a report)\n"
        "- code-reviewer: Code review (submit code for review)\n"
        "- project-planner: Project planning (ask to plan a project)\n"
        "- doc-pipeline: API documentation (ask to document code)\n"
    ),
    tools=[skill_toolset],
)
