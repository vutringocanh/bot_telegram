import base64
import json
import os
import urllib.request
import urllib.error

from PIL import ImageGrab


# ============================================================
# CONFIG
# ============================================================

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

MODEL = "ahmadwaqar/smolvlm2-500m-video:latest"

IMAGE_FILE = "screen_test.png"


# ============================================================
# SCREENSHOT
# ============================================================

def capture_screenshot():
    print("📸 Đang chụp màn hình...")

    try:
        screenshot = ImageGrab.grab(all_screens=True)

        width, height = screenshot.size

        print(f"🖥️ Screenshot: {width}x{height}")

        screenshot.save(
            IMAGE_FILE,
            format="PNG"
        )

        print(f"💾 Đã lưu: {IMAGE_FILE}")

        return True

    except Exception as exc:
        print(f"❌ Không thể chụp màn hình: {exc}")
        return False


# ============================================================
# LOAD IMAGE
# ============================================================

def load_image():
    if not os.path.exists(IMAGE_FILE):
        print(f"⚠️ Không tìm thấy {IMAGE_FILE}")
        print("📸 Tự động chụp screenshot mới...")
        
        if not capture_screenshot():
            return None

    try:
        with open(IMAGE_FILE, "rb") as f:
            image_data = f.read()

        print(f"📦 Image size: {len(image_data) / 1024:.1f} KB")

        image_base64 = base64.b64encode(image_data).decode("utf-8")

        return image_base64

    except Exception as exc:
        print(f"❌ Không thể đọc ảnh: {exc}")
        return None


# ============================================================
# SEND TO OLLAMA
# ============================================================

def ask_vision(image_base64):
    prompt = """
Analyze this computer screenshot carefully.

Identify every visible application window.

For each visible window:
- Give its title or application name.
- Describe its main visible content.

Also identify visible:
- buttons
- text fields
- menus
- terminal windows
- browser windows
- important UI elements

Pay attention to the foreground window and the background windows.

Only describe things that are actually visible in the screenshot.
Do not guess.

Answer in simple English.
Be concise but informative.
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

    data = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(
        OLLAMA_URL,
        data=data,
        headers={
            "Content-Type": "application/json"
        },
        method="POST"
    )

    print()
    print("👁️ Đang gửi screenshot cho SmolVLM2...")
    print(f"🧠 Model: {MODEL}")
    print()

    try:
        with urllib.request.urlopen(
            request,
            timeout=180
        ) as response:

            response_data = response.read()

            result = json.loads(
                response_data.decode("utf-8")
            )

            return result.get(
                "response",
                ""
            )

    except urllib.error.HTTPError as exc:

        print(
            f"❌ Ollama HTTP Error: "
            f"{exc.code}"
        )

        try:
            error_body = exc.read().decode(
                "utf-8",
                errors="replace"
            )

            print(error_body)

        except Exception:
            pass

        return None

    except urllib.error.URLError as exc:

        print("❌ Không kết nối được Ollama.")
        print(f"   {exc}")

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

    print("=" * 60)
    print("       DAI LOCAL VISION TEST")
    print("=" * 60)
    print()

    # --------------------------------------------------------
    # 1. Check Ollama
    # --------------------------------------------------------

    print("🔌 Ollama:")
    print(f"   {OLLAMA_URL}")

    print()

    # --------------------------------------------------------
    # 2. Load / capture screenshot
    # --------------------------------------------------------

    image_base64 = load_image()

    if not image_base64:
        print()
        print("❌ Không có ảnh để phân tích.")
        return

    # --------------------------------------------------------
    # 3. Vision
    # --------------------------------------------------------

    result = ask_vision(
        image_base64
    )

    print()

    if result is None:
        print("=" * 60)
        print("❌ VISION FAILED")
        print("=" * 60)
        return

    # --------------------------------------------------------
    # 4. Output
    # --------------------------------------------------------

    print("=" * 60)
    print("              SMOLVLM2 RESULT")
    print("=" * 60)

    print(result)

    print("=" * 60)
    print()

    print("✅ Vision request hoàn thành.")


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()