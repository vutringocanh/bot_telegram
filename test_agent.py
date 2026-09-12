import asyncio

from agent_manager import agent_mgr


async def main():

    user_id = 999999

    agent_mgr.set_active_agent_type(
        user_id,
        "router",
    )

    async for event in agent_mgr.execute_prompt(
        user_id=user_id,
        prompt="Mở Notepad trên Windows và gõ Hello DAI",
        workspace_dir=r"C:\Users\Admin\Downloads\telegram",
        on_status_update=lambda x: print("[STATUS]", x),
    ):

        print(
            f"[{event.event_type}] "
            f"{event.tool_name or ''} "
            f"{event.content[:500]}"
        )


asyncio.run(main())