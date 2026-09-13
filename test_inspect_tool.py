import asyncio
import json

from tool_registry import execute_tool


async def main():

    print("=" * 80)
    print("             DAI INSPECT_UI TOOL TEST")
    print("=" * 80)

    print()
    print("📝 Đang mở Notepad...")

    import subprocess
    subprocess.Popen(["notepad.exe"])

    await asyncio.sleep(2)

    print()
    print("🔎 Gọi inspect_ui tool...")

    result = await execute_tool(
        name="inspect_ui",
        arguments={},
        workspace_dir=".",
    )

    print()
    print("=" * 80)
    print("                    RESULT")
    print("=" * 80)

    print()

    print(
        json.dumps(
            result,
            indent=2,
            ensure_ascii=False,
        )
    )

    print()
    print("=" * 80)

    if result.get("window", {}).get("title"):
        print("✅ inspect_ui TOOL PASS")
    else:
        print("❌ inspect_ui TOOL FAILED")

    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())