import ctypes
from typing import Any, Dict, List, Optional

from pywinauto import Desktop


# Các loại control hữu ích cho Computer Agent
INTERESTING_CONTROL_TYPES = {
    "Button",
    "Edit",
    "ComboBox",
    "List",
    "ListItem",
    "Menu",
    "MenuBar",
    "MenuItem",
    "Tab",
    "TabItem",
    "CheckBox",
    "RadioButton",
    "Slider",
    "Text",
    "Image",
    "Document",
    "Tree",
    "TreeItem",
}


def get_foreground_hwnd() -> int:
    """
    Lấy HWND của cửa sổ Windows đang ở foreground.
    """

    hwnd = ctypes.windll.user32.GetForegroundWindow()

    return int(hwnd)


def get_window_from_hwnd(
    hwnd: int,
    backend: str = "uia",
):
    """
    Chuyển HWND thành PyWinAuto window.
    """

    desktop = Desktop(
        backend=backend
    )

    window = desktop.window(
        handle=hwnd
    )

    window.wait(
        "exists",
        timeout=10
    )

    return window


def rect_to_dict(rect) -> Dict[str, int]:

    return {
        "left": int(rect.left),
        "top": int(rect.top),
        "right": int(rect.right),
        "bottom": int(rect.bottom),
        "width": int(rect.width()),
        "height": int(rect.height()),
    }


def rect_center(rect) -> List[int]:

    center_x = (
        int(rect.left) + int(rect.right)
    ) // 2

    center_y = (
        int(rect.top) + int(rect.bottom)
    ) // 2

    return [
        center_x,
        center_y,
    ]


def get_control_info(
    control,
) -> Optional[Dict[str, Any]]:
    """
    Chuyển một PyWinAuto control
    thành dictionary sạch cho AI.
    """

    try:

        rect = control.rectangle()

        if rect.width() <= 0:
            return None

        if rect.height() <= 0:
            return None

        element_info = control.element_info

        control_type = (
            element_info.control_type
            or ""
        )

        name = (
            element_info.name
            or ""
        )

        automation_id = (
            element_info.automation_id
            or ""
        )

        class_name = (
            element_info.class_name
            or ""
        )

        # Chỉ giữ control hữu ích.
        if (
            control_type not in INTERESTING_CONTROL_TYPES
            and not name
            and not automation_id
        ):
            return None

        try:
            enabled = bool(
                control.is_enabled()
            )
        except Exception:
            enabled = None

        try:
            visible = bool(
                control.is_visible()
            )
        except Exception:
            visible = None

        return {
            "control_type": control_type,
            "name": name,
            "automation_id": automation_id,
            "class_name": class_name,
            "rect": rect_to_dict(rect),
            "center": rect_center(rect),
            "enabled": enabled,
            "visible": visible,
        }

    except Exception:
        return None


def inspect_window(
    window,
    max_controls: int = 200,
) -> Dict[str, Any]:
    """
    Inspect một PyWinAuto window.
    """

    try:

        rect = window.rectangle()

    except Exception:

        rect = None

    try:

        title = window.window_text()

    except Exception:

        title = ""

    try:

        control_type = (
            window.element_info.control_type
            or "Window"
        )

    except Exception:

        control_type = "Window"

    try:

        automation_id = (
            window.element_info.automation_id
            or ""
        )

    except Exception:

        automation_id = ""

    try:

        class_name = (
            window.element_info.class_name
            or ""
        )

    except Exception:

        class_name = ""

    try:

        process_id = int(
            window.process_id()
        )

    except Exception:

        process_id = None

    controls: List[Dict[str, Any]] = []

    try:

        descendants = window.descendants()

    except Exception:

        descendants = []

    for control in descendants:

        if len(controls) >= max_controls:
            break

        info = get_control_info(
            control
        )

        if info is not None:

            controls.append(
                info
            )

    result: Dict[str, Any] = {
        "window": {
            "title": title,
            "control_type": control_type,
            "automation_id": automation_id,
            "class_name": class_name,
            "process_id": process_id,
        },
        "controls": controls,
        "control_count": len(controls),
    }

    if rect is not None:

        result["window"]["rect"] = (
            rect_to_dict(rect)
        )

        result["window"]["center"] = (
            rect_center(rect)
        )

    return result


def inspect_active_window(
    max_controls: int = 200,
) -> Dict[str, Any]:
    """
    Inspect cửa sổ Windows đang foreground.
    """

    hwnd = get_foreground_hwnd()

    if not hwnd:
        raise RuntimeError(
            "Không lấy được foreground HWND."
        )

    window = get_window_from_hwnd(
        hwnd
    )

    result = inspect_window(
        window,
        max_controls=max_controls,
    )

    result["hwnd"] = hwnd

    return result


def find_controls(
    window,
    control_type: Optional[str] = None,
    name: Optional[str] = None,
    automation_id: Optional[str] = None,
) -> List[Any]:
    """
    Tìm controls theo UIA metadata.
    """

    controls = []

    try:
        descendants = window.descendants()
    except Exception:
        return controls

    for control in descendants:

        try:

            info = control.element_info

            current_type = (
                info.control_type
                or ""
            )

            current_name = (
                info.name
                or ""
            )

            current_id = (
                info.automation_id
                or ""
            )

            if (
                control_type is not None
                and current_type.lower()
                != control_type.lower()
            ):
                continue

            if (
                name is not None
                and current_name.lower()
                != name.lower()
            ):
                continue

            if (
                automation_id is not None
                and current_id.lower()
                != automation_id.lower()
            ):
                continue

            controls.append(
                control
            )

        except Exception:
            continue

    return controls


def inspect_active_window_text(
    max_controls: int = 200,
) -> str:
    """
    Phiên bản text gọn dành cho AI.
    """

    data = inspect_active_window(
        max_controls=max_controls
    )

    window = data["window"]

    lines = []

    lines.append(
        f"WINDOW: {window.get('title', '')}"
    )

    lines.append(
        f"TYPE: {window.get('control_type', '')}"
    )

    lines.append(
        f"HWND: {data.get('hwnd')}"
    )

    lines.append(
        f"PROCESS_ID: {window.get('process_id')}"
    )

    if "rect" in window:

        rect = window["rect"]

        lines.append(
            "RECT: "
            f"({rect['left']},{rect['top']})"
            f" -> "
            f"({rect['right']},{rect['bottom']})"
        )

    lines.append(
        ""
    )

    lines.append(
        "CONTROLS:"
    )

    for index, control in enumerate(
        data["controls"],
        start=1,
    ):

        control_type = (
            control["control_type"]
        )

        name = (
            control["name"]
        )

        automation_id = (
            control["automation_id"]
        )

        center = (
            control["center"]
        )

        rect = (
            control["rect"]
        )

        lines.append(
            f"{index}. "
            f"{control_type}"
            f" | name={name!r}"
            f" | id={automation_id!r}"
            f" | center={center}"
            f" | rect=("
            f"{rect['left']},"
            f"{rect['top']},"
            f"{rect['right']},"
            f"{rect['bottom']}"
            f")"
        )

    return "\n".join(lines)