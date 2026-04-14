# Project Configuration & Preferences

## Workflow and Tooling

### Project Execution
- **Python environments**: This project uses `uv`. Execute Python scripts internally using `uv run python <script.py>`.
- **ADK Command Line**: Use the ADK CLI to run adk agents when appropriate, e.g. `uv run adk run <path_to_agent_file>.py`. See `uv run adk run --help`.
  - **Note**: `adk run` is interactive and requires user input to function.
- **Corporate Security (Airlock)**: The environment uses private package registries with "Airlock". Any Airlock-related messages are expected security warnings—bubble them up directly to the user rather than trying to fix them.

### Defaults
- **Formatting and Linting**: `uv run ruff check` and `uv run ruff format` unless explicitly stated otherwise.
