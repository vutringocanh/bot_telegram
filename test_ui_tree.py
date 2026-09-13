import time
import tkinter as tk

from pywinauto import Desktop


def create_test_window():
    root = tk.Tk()

    root.title("DAI UI Tree Test")
    root.geometry("800x500")
    root.resizable(False, False)

    tk.Label(
        root,
        text="DAI COMPUTER VISION TEST",
        font=("Arial", 24, "bold")
    ).pack(pady=40)

    entry = tk.Entry(
        root,
        width=35,
        font=("Arial", 14)
    )
    entry.insert(0, "DAI Computer Agent")
    entry.pack(pady=20)

    frame = tk.Frame(root)
    frame.pack(pady=30)

    for name in ["OPEN", "SAVE", "CANCEL"]:
        tk.Button(
            frame,
            text=name,
            width=12,
            height=2,
            font=("Arial", 14, "bold")
        ).pack(side="left", padx=15)

    root.update()

    return root


def main():

    print("=" * 70)
    print("           DAI WINDOWS UI TREE TEST")
    print("=" * 70)

    root = create_test_window()

    print()
    print("⏳ Chờ cửa sổ...")
    time.sleep(2)

    try:

        desktop = Desktop(backend="uia")

        window = desktop.window(
            title="DAI UI Tree Test"
        )

        window.wait(
            "exists",
            timeout=10
        )

        print()
        print("🪟 WINDOW FOUND")
        print()

        print("=" * 70)
        print("                 UI TREE")
        print("=" * 70)

        window.print_control_identifiers()

        print("=" * 70)

    except Exception as exc:

        print()
        print("❌ ERROR:")
        print(exc)

    finally:

        print()
        print("🛑 Đóng cửa sổ...")
        root.destroy()


if __name__ == "__main__":
    main()