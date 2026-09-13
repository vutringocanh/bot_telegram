import time
import tkinter as tk

from pywinauto import Desktop


def create_test_window():
    root = tk.Tk()

    root.title("DAI UI Click Test")
    root.geometry("800x500")
    root.resizable(False, False)

    tk.Label(
        root,
        text="DAI UI AUTOMATION CLICK TEST",
        font=("Arial", 24, "bold")
    ).pack(pady=40)

    status = tk.Label(
        root,
        text="Status: Waiting...",
        font=("Arial", 16)
    )
    status.pack(pady=20)

    frame = tk.Frame(root)
    frame.pack(pady=30)

    def clicked(name):
        status.config(
            text=f"Status: {name} CLICKED"
        )

    for name in ["OPEN", "SAVE", "CANCEL"]:
        tk.Button(
            frame,
            text=name,
            width=12,
            height=2,
            font=("Arial", 14, "bold"),
            command=lambda n=name: clicked(n)
        ).pack(
            side="left",
            padx=15
        )

    root.update()

    return root


def find_buttons():

    desktop = Desktop(backend="uia")

    window = desktop.window(
        title="DAI UI Click Test"
    )

    window.wait(
        "exists",
        timeout=10
    )

    print()
    print("=" * 70)
    print("              BUTTON DISCOVERY")
    print("=" * 70)

    # Lấy tất cả Button mà UI Automation nhìn thấy
    buttons = window.descendants(
        control_type="Button"
    )

    real_buttons = []

    for button in buttons:

        rect = button.rectangle()

        # Bỏ qua các nút Minimize / Maximize / Close
        # vì chúng nằm ở title bar.
        if rect.top > window.rectangle().top + 40:

            real_buttons.append(button)

    print()
    print(
        f"Found {len(real_buttons)} application buttons"
    )

    for i, button in enumerate(real_buttons):

        rect = button.rectangle()

        center_x = (
            rect.left + rect.right
        ) // 2

        center_y = (
            rect.top + rect.bottom
        ) // 2

        print()
        print(
            f"BUTTON {i}"
        )

        print(
            f"  Rectangle:"
            f" ({rect.left}, {rect.top})"
            f" -> ({rect.right}, {rect.bottom})"
        )

        print(
            f"  CENTER:"
            f" ({center_x}, {center_y})"
        )

    print()
    print("=" * 70)

    return real_buttons


def main():

    print("=" * 70)
    print("           DAI UI AUTOMATION CLICK TEST")
    print("=" * 70)

    root = create_test_window()

    print()
    print("⏳ Chờ cửa sổ ổn định...")
    time.sleep(2)

    root.update()

    buttons = find_buttons()

    if len(buttons) >= 3:

        print()
        print("🖱️ Click button đầu tiên...")

        buttons[0].click_input()

        time.sleep(2)

        print()
        print("✅ Click đã được gửi.")

    else:

        print()
        print("❌ Không tìm đủ 3 button.")

    print()
    print("⏳ Giữ cửa sổ thêm 3 giây để kiểm tra...")
    time.sleep(3)

    root.destroy()


if __name__ == "__main__":
    main()