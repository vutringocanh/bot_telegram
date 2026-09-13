import time
import tkinter as tk

from pywinauto import Desktop


WINDOW_TITLE = "DAI UI Inspector Test"


def create_test_window():
    root = tk.Tk()

    root.title(WINDOW_TITLE)
    root.geometry("900x550")
    root.resizable(False, False)

    tk.Label(
        root,
        text="DAI UI INSPECTOR TEST",
        font=("Arial", 24, "bold")
    ).pack(pady=(35, 10))

    tk.Label(
        root,
        text="PyWinAuto / Windows UI Automation",
        font=("Arial", 13)
    ).pack(pady=(0, 30))

    form = tk.Frame(root)
    form.pack()

    tk.Label(
        form,
        text="Project:",
        font=("Arial", 14)
    ).grid(row=0, column=0, padx=10, pady=10)

    entry_project = tk.Entry(
        form,
        width=40,
        font=("Arial", 14)
    )

    entry_project.insert(
        0,
        r"C:\Users\Admin\Downloads\telegram"
    )

    entry_project.grid(
        row=0,
        column=1,
        padx=10,
        pady=10
    )

    tk.Label(
        form,
        text="Model:",
        font=("Arial", 14)
    ).grid(row=1, column=0, padx=10, pady=10)

    model_var = tk.StringVar(
        value="kr/glm-5"
    )

    model_menu = tk.OptionMenu(
        form,
        model_var,
        "kr/glm-5",
        "kr/MiniMax-M2.5",
        "kr/qwen3-coder-next"
    )

    model_menu.config(
        font=("Arial", 13),
        width=25
    )

    model_menu.grid(
        row=1,
        column=1,
        padx=10,
        pady=10
    )

    button_frame = tk.Frame(root)
    button_frame.pack(pady=45)

    for name in [
        "OPEN PROJECT",
        "RUN",
        "STOP"
    ]:
        tk.Button(
            button_frame,
            text=name,
            width=15,
            height=2,
            font=("Arial", 13, "bold")
        ).pack(
            side="left",
            padx=12
        )

    tk.Label(
        root,
        text="Status: Ready",
        font=("Arial", 13)
    ).pack(pady=10)

    root.update()

    return root


def inspect_window():

    print()
    print("=" * 80)
    print("                 DAI UI INSPECTOR")
    print("=" * 80)

    try:

        desktop = Desktop(
            backend="uia"
        )

        window = desktop.window(
            title=WINDOW_TITLE
        )

        window.wait(
            "exists",
            timeout=10
        )

        window_rect = window.rectangle()

        print()
        print("WINDOW")
        print("-" * 80)

        print(
            f"Title : {window.window_text()}"
        )

        print(
            f"Type  : {window.element_info.control_type}"
        )

        print(
            f"Rect  : "
            f"({window_rect.left}, {window_rect.top})"
            f" -> "
            f"({window_rect.right}, {window_rect.bottom})"
        )

        print()
        print("CONTROLS")
        print("-" * 80)

        controls = window.descendants()

        count = 0

        for control in controls:

            try:

                rect = control.rectangle()

                # Bỏ control không có kích thước
                if rect.width() <= 0 or rect.height() <= 0:
                    continue

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

                center_x = (
                    rect.left + rect.right
                ) // 2

                center_y = (
                    rect.top + rect.bottom
                ) // 2

                # Bỏ các container lớn để output dễ đọc
                interesting_types = {
                    "Button",
                    "Edit",
                    "ComboBox",
                    "List",
                    "ListItem",
                    "Menu",
                    "MenuItem",
                    "Tab",
                    "TabItem",
                    "CheckBox",
                    "RadioButton",
                    "Slider",
                    "Text",
                    "Image",
                }

                if (
                    control_type not in interesting_types
                    and not name
                    and not automation_id
                ):
                    continue

                count += 1

                print()
                print(
                    f"[{count}] {control_type}"
                )

                print(
                    f"    Name          : {name!r}"
                )

                print(
                    f"    AutomationId  : "
                    f"{automation_id!r}"
                )

                print(
                    f"    Rectangle     : "
                    f"({rect.left}, {rect.top})"
                    f" -> "
                    f"({rect.right}, {rect.bottom})"
                )

                print(
                    f"    Center        : "
                    f"({center_x}, {center_y})"
                )

            except Exception:
                continue

        print()
        print("-" * 80)
        print(
            f"TOTAL INTERESTING CONTROLS: {count}"
        )

        print("=" * 80)

    except Exception as exc:

        print()
        print("❌ INSPECTOR ERROR")
        print(exc)


def main():

    print("=" * 80)
    print("              DAI UI INSPECTOR TEST")
    print("=" * 80)

    print()
    print("🪟 Tạo cửa sổ test...")

    root = create_test_window()

    print(
        "⏳ Chờ Windows UI Automation ổn định..."
    )

    time.sleep(2)

    root.update()

    inspect_window()

    print()
    print("🛑 Đóng cửa sổ...")

    root.destroy()


if __name__ == "__main__":
    main()