import base64
import json
import os
import time
import urllib.request
import urllib.error
import tkinter as tk
from tkinter import ttk

from PIL import ImageGrab


# ============================================================
# CONFIG
# ============================================================

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL = "ahmadwaqar/smolvlm2-500m-video:latest"

IMAGE_FILE = "vision_gui_test.png"


# ============================================================
# CREATE TEST GUI
# ============================================================

def create_test_window():
    root = tk.Tk()

    root.title("DAI Computer Vision Test")
    root.geometry("800x500")
    root.resizable(False, False)

    # Center window
    root.update_idletasks()

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width - 800) // 2
    y = (screen_height - 500) // 2

    root.geometry(f"800x500+{x}+{y}")

    # --------------------------------------------------------
    # Title
    # --------------------------------------------------------

    title = tk.Label(
        root,
        text="DAI COMPUTER VISION TEST",
        font=("Arial", 24, "bold")
    )
    title.pack(pady=(35, 10))

    subtitle = tk.Label(
        root,
        text="Can the AI locate buttons and interface elements?",
        font=("Arial", 13)
    )
    subtitle.pack(pady=(0, 30))

    # --------------------------------------------------------
    # Input
    # --------------------------------------------------------

    frame = tk.Frame(root)
    frame.pack(pady=10)

    label = tk.Label(
        frame,
        text="Agent name:",
        font=("Arial", 14)
    )
    label.grid(row=0, column=0, padx=10)

    entry = tk.Entry(
        frame,
        width=35,
        font=("Arial", 14)
    )
    entry.insert(0, "DAI Computer Agent")
    entry.grid(row=0, column=1, padx=10)

    # --------------------------------------------------------
    # Buttons
    # --------------------------------------------------------

    button_frame = tk.Frame(root)
    button_frame.pack(pady=50)

    open_button = tk.Button(
        button_frame,
        text="OPEN",
        width=12,
        height=2,
        font=("Arial", 14, "bold")
    )
    open_button.grid(row=0, column=0, padx=15)

    save_button = tk.Button(
        button_frame,
        text="SAVE",
        width=12,
        height=2,
        font=("Arial", 14, "bold")
    )
    save_button.grid(row=0, column=1, padx=15)

    cancel_button = tk.Button(
        button_frame,
        text="CANCEL",
        width=12,
        height=2,
        font=("Arial", 14, "bold")
    )
    cancel_button.grid(row=0, column=2, padx=15)

    # --------------------------------------------------------
    # Status
    # --------------------------------------------------------

    status = tk.Label(
        root,
        text="Status: Waiting for vision analysis...",
        font=("Arial", 12)
    )
    status.pack(pady=10)

    root.update()

    return root


# ============================================================
# SCREENSHOT
# ============================================================

def capture_screenshot():
    print("📸 Chụp GUI test...")

    screenshot = ImageGrab.grab(all_screens=True)

    print(
        f"🖥️ Screenshot: "
        f"{screenshot.width}x{screenshot.height}"
    )

    screenshot.save(
        IMAGE_FILE,
        format="PNG"
    )

    print(
        f"💾 Saved: {IMAGE_FILE}"
    )


# ============================================================
# VISION
# ============================================================

def ask_vision():

    with open(IMAGE_FILE, "rb") as f:
        image_base64 = base64.b64encode(
            f.read()
        ).decode("utf-8")

    prompt = """
You are analyzing a computer screenshot for a computer-control agent.

Carefully inspect the screenshot.

Identify these exact interface elements if visible:

1. The main application window.
2. The text input field.
3. The OPEN button.
4. The SAVE button.
5. The CANCEL button.

For each element provide:
- name
- approximate center position as pixel coordinates (x, y)
- approximate bounding box (left, top, right, bottom)

The screenshot resolution is 1920x1080.

Use this exact format:

ELEMENT: name
CENTER: x, y
BOX: left, top, right, bottom

Do not invent elements that are not visible.
Estimate coordinates from the full 1920x1080 screenshot.
""".strip()

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "images": [
            image_base64
        ],
        "stream": False,
        "options": {
            "temperature": 0
        }
    }

    request = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json"
        },
        method="POST"
    )

    print()
    print("👁️ Gửi screenshot cho SmolVLM2...")
    print()

    try:
        with urllib.request.urlopen(
            request,
            timeout=180
        ) as response:

            data = json.loads(
                response.read().decode("utf-8")
            )

            return data.get("response", "")

    except urllib.error.HTTPError as exc:

        print(
            f"❌ Ollama HTTP Error: {exc.code}"
        )

        try:
            print(
                exc.read().decode(
                    "utf-8",
                    errors="replace"
                )
            )
        except Exception:
            pass

        return None

    except Exception as exc:

        print(
            f"❌ Vision error: {exc}"
        )

        return None


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 65)
    print("       DAI COMPUTER VISION — COORDINATE TEST")
    print("=" * 65)
    print()

    # Create GUI
    root = create_test_window()

    print("🪟 Test window đã mở.")
    print("⏳ Chờ 2 giây để GUI ổn định...")

    root.update()
    time.sleep(2)

    # Capture
    capture_screenshot()

    # Vision
    result = ask_vision()

    print()

    print("=" * 65)
    print("                 VISION RESULT")
    print("=" * 65)

    if result:
        print(result)
    else:
        print("❌ Không nhận được kết quả.")

    print("=" * 65)

    print()
    print("🛑 Đóng cửa sổ test...")

    root.destroy()


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()