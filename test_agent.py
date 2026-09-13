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
        prompt="Mở Notepad trên Windows. Sau khi Notepad mở, hãy dùng inspect_ui để tìm vùng soạn thảo văn bản (Text Editor), sau đó click vào giữa vùng soạn thảo và nhập chính xác câu: 'Xin chào! Đây là DAI Computer Agent 👋'. Cuối cùng dùng inspect_ui để kiểm tra lại cửa sổ và xác nhận thao tác đã hoàn thành. Không được đoán tọa độ nếu inspect_ui có thể cung cấp tọa độ phù hợp.",
        workspace_dir=r"C:\Users\Admin\Downloads\telegram",
        on_status_update=lambda x: print("[STATUS]", x),
    ):

        print(
            f"[{event.event_type}] "
            f"{event.tool_name or ''} "
            f"{event.content[:500]}"
        )


asyncio.run(main())