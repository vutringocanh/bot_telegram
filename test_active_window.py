import time
import ctypes

from pywinauto import Desktop


def get_foreground_window():

    user32 = ctypes.windll.user32

    hwnd = user32.GetForegroundWindow()

    return hwnd


def inspect_active_window():

    print()
    print("=" * 80)
    print("              DAI ACTIVE WINDOW INSPECTOR")
    print("=" * 80)

    try:

        # Windows API lấy HWND cửa sổ foreground
        hwnd = get_foreground_window()

        print()
        print(
            f"HWND        : {hwnd}"
        )

        if not hwnd:

            print("❌ Không lấy được foreground window.")

            return

        desktop = Desktop(
            backend="uia"
        )

        # Chuyển HWND thành UIA window
        window = desktop.window(
            handle=hwnd
        )

        window.wait(
            "exists",
            timeout=10
        )

        print()
        print("🪟 ACTIVE WINDOW")
        print("-" * 80)

        title = window.window_text()

        print(
            f"Title       : {title!r}"
        )

        print(
            f"ControlType : "
            f"{window.element_info.control_type}"
        )

        try:

            process_id = window.process_id()

            print(
                f"Process ID  : {process_id}"
            )

        except Exception:

            print(
                "Process ID  : N/A"
            )

        try:

            rect = window.rectangle()

            print(
                f"Rectangle   : "
                f"({rect.left}, {rect.top})"
                f" -> "
                f"({rect.right}, {rect.bottom})"
            )

        except Exception:

            print(
                "Rectangle   : N/A"
            )

        print()
        print("CONTROLS")
        print("-" * 80)

        controls = window.descendants()

        count = 0

        interesting_types = {
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

        for control in controls:

            try:

                control_type = (
                    control.element_info.control_type
                    or ""
                )

                name = (
                    control.element_info.name
                    or ""
                )

                automation_id = (
                    control.element_info.automation_id
                    or ""
                )

                class_name = (
                    control.element_info.class_name
                    or ""
                )

                rect = control.rectangle()

                if rect.width() <= 0:
                    continue

                if rect.height() <= 0:
                    continue

                if (
                    control_type not in interesting_types
                    and not name
                    and not automation_id
                ):
                    continue

                count += 1

                center_x = (
                    rect.left + rect.right
                ) // 2

                center_y = (
                    rect.top + rect.bottom
                ) // 2

                print()
                print(
                    f"[{count}] {control_type}"
                )

                print(
                    f"    Name         : "
                    f"{name!r}"
                )

                print(
                    f"    AutomationId : "
                    f"{automation_id!r}"
                )

                print(
                    f"    ClassName    : "
                    f"{class_name!r}"
                )

                print(
                    f"    Rect         : "
                    f"({rect.left}, {rect.top})"
                    f" -> "
                    f"({rect.right}, {rect.bottom})"
                )

                print(
                    f"    Center       : "
                    f"({center_x}, {center_y})"
                )

            except Exception:

                continue

        print()
        print("-" * 80)

        print(
            f"TOTAL CONTROLS: {count}"
        )

        print("=" * 80)

    except Exception as exc:

        print()
        print("❌ INSPECTOR ERROR")

        print(
            f"{type(exc).__name__}: {exc}"
        )

        print("=" * 80)


def main():

    print("=" * 80)
    print("          DAI ACTIVE WINDOW UI TEST")
    print("=" * 80)

    print()
    print(
        "🖱️ Hãy click vào cửa sổ muốn inspect."
    )

    print(
        "⏳ Bạn có 5 giây..."
    )

    print()

    for i in range(5, 0, -1):

        print(
            f"   {i}..."
        )

        time.sleep(1)

    inspect_active_window()


if __name__ == "__main__":
    main()