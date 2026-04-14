# Advent of Agents (Spring 2026)

This repository contains the code for various agents (Fanout, Sculptor, Critic, Hierarchical) built using the Google Agent Development Kit (ADK).

## Demo Videos

See the agents in action!
- **Hierarchical:** [https://youtu.be/68EznHkK_UQ](https://youtu.be/68EznHkK_UQ)
- **Fanout:** [https://youtu.be/4-lr3sh2ETM](https://youtu.be/4-lr3sh2ETM)
- **Critic:** [https://youtu.be/Kp0HrGst5-w](https://youtu.be/Kp0HrGst5-w)

## Prerequisites

- [Python 3.11+](https://www.python.org/downloads/)
- [uv](https://docs.astral.sh/uv/) (Python package and environment manager)

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd aoa-luissala
   ```

2. **Install dependencies using uv:**
   ```bash
   uv sync
   ```

## Environment Setup

You need a Google Gemini API key to run these agents.

1. Get an API key from [Google AI Studio](https://aistudio.google.com/).
2. Copy the sample environment file:
   ```bash
   cp sample.env .env
   ```
3. Edit the `.env` file and replace `"your_api_key_here"` with your actual API key.

*Note: The `.env` file is ignored by Git to keep your API keys secure.*

## Running the Agents

There are two main ways to execute the agents:

### 1. Locally via Direct Script Execution
You can run any specific agent directly to execute its built-in prompt via the `__main__` block. For example, to run the Hierarchical agent's predefined test:
```bash
uv run python agents/hierarchical/agent.py
```

### 2. Locally via Interactive ADK CLI
If you want to have an interactive chat session with the agent in your terminal, use the ADK CLI:
```bash
uv run adk run agents/hierarchical
```
This will start an interactive runner where you can converse and enter prompts directly in your terminal.

### 3. Via the ADK Web UI
If you prefer a visual interface, you can launch the built-in ADK web experience:
```bash
uv run adk web agents --port 21000
```
Then, open your browser and navigate to `http://localhost:21000/dev-ui/` to interact with all the deployed Apps.
