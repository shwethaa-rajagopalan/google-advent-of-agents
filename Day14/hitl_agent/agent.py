import asyncio
from typing import Any
from google.adk.agents import Agent
from google.adk.events import Event
from google.adk.runners import Runner
from google.adk.tools import LongRunningFunctionTool
from google.adk.sessions import InMemorySessionService
from google.genai import types


# 1. Define a tool that requires human approval
def ask_for_approval(purpose: str, amount: float) -> dict[str, Any]:
    """Ask a human to approve this action before proceeding."""
    return {"status": "pending", "purpose": purpose, "amount": amount}


# 2. Define the tool that runs after approval
def process_refund(purpose: str, amount: float) -> dict[str, str]:
    """Process the approved refund."""
    return {"status": "success", "message": f"Refunded ${amount} for {purpose}."}


# 3. Create the agent with a LongRunningFunctionTool
agent = Agent(
    name="refund_agent",
    model="gemini-3.1-pro",
    instruction="""You handle refunds. Always call ask_for_approval first.
    If approved, call process_refund. If rejected, tell the user.""",
    tools=[LongRunningFunctionTool(func=ask_for_approval), process_refund],
)


async def main():
    # 4. Set up session and runner
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name="hitl-app", user_id="user1", session_id="s1"
    )
    runner = Runner(agent=agent, app_name="hitl-app", session_service=session_service)

    # 5. Run the agent — it will pause when it hits ask_for_approval
    user_msg = types.Content(
        role="user",
        parts=[types.Part(text="Refund $200 for a duplicate charge on txn_123")],
    )

    # Two-step detection:
    #  - Step A: find the function_call on the event with long_running_tool_ids
    #  - Step B: find the function_response matching that call ID
    long_running_call = None
    pending_response = None

    async for event in runner.run_async(
        session_id=session.id, user_id="user1", new_message=user_msg
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                # Step A: capture the long-running function *call*
                if (
                    not long_running_call
                    and part.function_call
                    and event.long_running_tool_ids
                    and part.function_call.id in event.long_running_tool_ids
                ):
                    long_running_call = part.function_call

                # Step B: capture the matching function *response*
                if (
                    long_running_call
                    and part.function_response
                    and part.function_response.id == long_running_call.id
                ):
                    pending_response = part.function_response

            # Print any agent text
            text = "".join(p.text or "" for p in event.content.parts)
            if text:
                print(f"Agent: {text}")

    if not pending_response:
        return

    # 6. Get human decision
    print(f"\n⏸  Pending: {pending_response.response}")
    choice = input("Approve? [Y/n]: ").strip().lower()

    # 7. Send decision back — agent resumes
    updated = pending_response.model_copy(deep=True)
    updated.response = {"status": "approved" if choice != "n" else "rejected"}

    async for event in runner.run_async(
        session_id=session.id,
        user_id="user1",
        new_message=types.Content(
            role="user", parts=[types.Part(function_response=updated)]
        ),
    ):
        if event.content and event.content.parts:
            text = "".join(p.text or "" for p in event.content.parts)
            if text:
                print(f"Agent: {text}")


if __name__ == "__main__":
    asyncio.run(main())