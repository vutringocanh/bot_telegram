import time
import tkinter as tk

from pywinauto import Desktop


def create_test_window():
    root = tk.Tk()

    root.title("DAI UI Automation Test")
    root.geometry("800x500")
    root.resizable(False, False)

    root.update_idletasks()

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width - 800) // 2
    y = (screen_height - 500) // 2

    root.geometry(f"800x500+{x}+{y}")

    # Title
    tk.Label(
        root,
        text="DAI COMPUTER VISION TEST",
        font=("Arial", 24, "bold")
    ).pack(pady=(35, 10))

    tk.Label(
        root,
        text="Windows UI Automation coordinate test",
        font=("Arial", 13)
    ).pack(pady=(0, 30))

    # Input
    frame = tk.Frame(root)
    frame.pack()

    tk.Label(
        frame,
        text="Agent name:",
        font=("Arial", 14)
    ).grid(row=0, column=0, padx=10)

    entry = tk.Entry(
        frame,
        width=35,
        font=("Arial", 14)
    )
    entry.insert(0, "DAI Computer Agent")
    entry.grid(row=0, column=1, padx=10)

    # Buttons
    button_frame = tk.Frame(root)
    button_frame.pack(pady=50)

    tk.Button(
        button_frame,
        text="OPEN",
        width=12,
        height=2,
        font=("Arial", 14, "bold")
    ).grid(row=0, column=0, padx=15)

    tk.Button(
        button_frame,
        text="SAVE",
        width=12,
        height=2,
        font=("Arial", 14, "bold")
    ).grid(row=0, column=1, padx=15)

    tk.Button(
        button_frame,
        text="CANCEL",
        width=12,
        height=2,
        font=("Arial", 14, "bold")
    ).grid(row=0, column=2, padx=15)

    tk.Label(
        root,
        text="Status: UI Automation test",
        font=("Arial", 12)
    ).pack()

    root.update()

    return root


def find_and_report_controls():

    print()
    print("=" * 70)
    print("       WINDOWS UI AUTOMATION RESULT")
    print("=" * 70)

    try:
        desktop = Desktop(backend="uia")

        # Tìm cửa sổ theo title
        window = desktop.window(
            title="DAI UI Automation Test"
        )

        window.wait(
            "exists",
            timeout=10
        )

        print()
        print("🪟 WINDOW FOUND")
        print(
            f"   Title: {window.window_text()}"
        )

        rect = window.rectangle()

        print(
            f"   Window rectangle: "
            f"left={rect.left}, "
            f"top={rect.top}, "
            f"right={rect.right}, "
            f"bottom={rect.bottom}"
        )

        print()

        # ----------------------------------------------------
        # Find buttons
        # ----------------------------------------------------

        for name in [
            "OPEN",
            "SAVE",
            "CANCEL"
        ]:

            print(f"🔎 Searching: {name}")

            try:

                button = window.child_window(
                    title=name,
                    control_type="Button"
                )

                button.wait(
                    "exists",
                    timeout=5
                )

                rect = button.rectangle()

                center_x = (
                    rect.left + rect.right
                ) // 2

                center_y = (
                    rect.top + rect.bottom
                ) // 2

                print(
                    f"   ✅ FOUND"
                )

                print(
                    f"   Text: {button.window_text()}"
                )

                print(
                    f"   Rectangle:"
                    f" ({rect.left}, {rect.top})"
                    f" → ({rect.right}, {rect.bottom})"
                )

                print(
                    f"   CENTER:"
                    f" ({center_x}, {center_y})"
                )

                print()

            except Exception as exc:

                print(
                    f"   ❌ NOT FOUND: {exc}"
                )

    except Exception as exc:

        print()
        print(
            f"❌ UI Automation error: {exc}"
        )

    print("=" * 70)


def main():

    print("=" * 70)
    print("       DAI WINDOWS UI AUTOMATION TEST")
    print("=" * 70)

    print()
    print("🪟 Đang tạo cửa sổ test...")

    root = create_test_window()

    print(
        "⏳ Chờ cửa sổ ổn định..."
    )

    time.sleep(2)

    root.update()

    find_and_report_controls()

    print()
    print("🛑 Đóng cửa sổ test...")

    root.destroy()


if __name__ == "__main__":
    main()