import asyncio
from typing import Any

from computer_tools import ComputerTools


# ============================================================
# TOOL DEFINITIONS
# ============================================================

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "screenshot",
            "description": (
                "Chụp toàn bộ màn hình Windows hiện tại. "
                "Dùng để quan sát trạng thái desktop sau mỗi thao tác."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "screen_size",
            "description": "Lấy kích thước màn hình Windows.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "mouse_position",
            "description": "Lấy vị trí chuột hiện tại.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "move_mouse",
            "description": "Di chuyển chuột tới tọa độ màn hình.",
            "parameters": {
                "type": "object",
                "properties": {
                    "x": {
                        "type": "integer",
                        "description": "Tọa độ X.",
                    },
                    "y": {
                        "type": "integer",
                        "description": "Tọa độ Y.",
                    },
                    "duration": {
                        "type": "number",
                        "description": "Thời gian di chuyển bằng giây.",
                    },
                },
                "required": ["x", "y"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "click",
            "description": "Click chuột tại tọa độ màn hình.",
            "parameters": {
                "type": "object",
                "properties": {
                    "x": {
                        "type": "integer",
                        "description": "Tọa độ X.",
                    },
                    "y": {
                        "type": "integer",
                        "description": "Tọa độ Y.",
                    },
                    "button": {
                        "type": "string",
                        "enum": ["left", "right"],
                    },
                    "clicks": {
                        "type": "integer",
                        "description": "Số lần click.",
                    },
                },
                "required": ["x", "y"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "double_click",
            "description": "Double click tại tọa độ màn hình.",
            "parameters": {
                "type": "object",
                "properties": {
                    "x": {
                        "type": "integer",
                    },
                    "y": {
                        "type": "integer",
                    },
                },
                "required": ["x", "y"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "right_click",
            "description": "Right click tại tọa độ màn hình.",
            "parameters": {
                "type": "object",
                "properties": {
                    "x": {
                        "type": "integer",
                    },
                    "y": {
                        "type": "integer",
                    },
                },
                "required": ["x", "y"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "drag",
            "description": "Kéo chuột từ một tọa độ tới tọa độ khác.",
            "parameters": {
                "type": "object",
                "properties": {
                    "x1": {"type": "integer"},
                    "y1": {"type": "integer"},
                    "x2": {"type": "integer"},
                    "y2": {"type": "integer"},
                    "duration": {"type": "number"},
                },
                "required": ["x1", "y1", "x2", "y2"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "scroll",
            "description": "Cuộn chuột.",
            "parameters": {
                "type": "object",
                "properties": {
                    "amount": {
                        "type": "integer",
                        "description": (
                            "Số dương cuộn lên, số âm cuộn xuống."
                        ),
                    },
                },
                "required": ["amount"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "type_text",
            "description": (
                "Gõ văn bản vào cửa sổ đang active."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                    },
                },
                "required": ["text"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "press",
            "description": "Nhấn một phím trên bàn phím.",
            "parameters": {
                "type": "object",
                "properties": {
                    "key": {
                        "type": "string",
                        "description": (
                            "Ví dụ: enter, esc, tab, backspace, "
                            "up, down, left, right."
                        ),
                    },
                },
                "required": ["key"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "hotkey",
            "description": "Nhấn tổ hợp phím.",
            "parameters": {
                "type": "object",
                "properties": {
                    "keys": {
                        "type": "array",
                        "items": {
                            "type": "string",
                        },
                    },
                },
                "required": ["keys"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "wait",
            "description": "Chờ một khoảng thời gian để ứng dụng ổn định.",
            "parameters": {
                "type": "object",
                "properties": {
                    "seconds": {
                        "type": "number",
                    },
                },
                "required": ["seconds"],
            },
        },
    },
]


# ============================================================
# TOOL EXECUTION
# ============================================================

async def execute_tool(
    name: str,
    arguments: dict[str, Any],
    workspace_dir: str,
) -> Any:

    if name == "screenshot":
        return ComputerTools.screenshot()

    if name == "screen_size":
        return ComputerTools.screen_size()

    if name == "mouse_position":
        return ComputerTools.mouse_position()

    if name == "move_mouse":
        return ComputerTools.move_mouse(
            x=arguments["x"],
            y=arguments["y"],
            duration=arguments.get("duration", 0.2),
        )

    if name == "click":
        return ComputerTools.click(
            x=arguments["x"],
            y=arguments["y"],
            button=arguments.get("button", "left"),
            clicks=arguments.get("clicks", 1),
        )

    if name == "double_click":
        return ComputerTools.double_click(
            arguments["x"],
            arguments["y"],
        )

    if name == "right_click":
        return ComputerTools.right_click(
            arguments["x"],
            arguments["y"],
        )

    if name == "drag":
        return ComputerTools.drag(
            x1=arguments["x1"],
            y1=arguments["y1"],
            x2=arguments["x2"],
            y2=arguments["y2"],
            duration=arguments.get("duration", 0.5),
        )

    if name == "scroll":
        return ComputerTools.scroll(
            arguments["amount"]
        )

    if name == "type_text":
        return ComputerTools.type_text(
            arguments["text"]
        )

    if name == "press":
        return ComputerTools.press(
            arguments["key"]
        )

    if name == "hotkey":
        return ComputerTools.hotkey(
            *arguments["keys"]
        )

    if name == "wait":
        return await ComputerTools.wait(
            arguments.get("seconds", 1)
        )

    return {
        "success": False,
        "error": f"Unknown tool: {name}",
    }