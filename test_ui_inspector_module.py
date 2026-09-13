import json
import subprocess
import time

from pywinauto import Desktop

from ui_inspector import inspect_window


def main():

    print("=" * 80)
    print("          DAI UI INSPECTOR - REAL NOTEPAD TEST")
    print("=" * 80)

    print()
    print("📝 Đang mở Notepad...")

    subprocess.Popen(
        ["notepad.exe"]
    )

    time.sleep(2)

    try:

        desktop = Desktop(
            backend="uia"
        )

        # Tìm Notepad
        windows = desktop.windows(
            control_type="Window"
        )

        notepad = None

        for window in windows:

            try:

                title = window.window_text()

                if (
                    "Notepad" in title
                    or "Untitled" in title
                    or "*Untitled" in title
                ):

                    notepad = window
                    break

            except Exception:
                continue

        if notepad is None:

            print()
            print("❌ Không tìm thấy Notepad.")

            return

        print()
        print("✅ NOTEPAD FOUND")

        print(
            f"Title: {notepad.window_text()}"
        )

        print()

        # Đưa Notepad lên foreground
        try:
            notepad.set_focus()
        except Exception:
            pass

        time.sleep(1)

        print(
            "🔎 Đang inspect Notepad..."
        )

        result = inspect_window(
            notepad
        )

        print()
        print("=" * 80)
        print("                 INSPECTION RESULT")
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

        print()
        print(
            "🎉 REAL NOTEPAD INSPECTION PASS"
        )

        print()
        print(
            "🛑 Đóng Notepad..."
        )

        try:
            notepad.close()
        except Exception:
            pass

    except Exception as exc:

        print()
        print("❌ TEST FAILED")

        print(
            f"{type(exc).__name__}: {exc}"
        )

        print("=" * 80)


if __name__ == "__main__":
    main()