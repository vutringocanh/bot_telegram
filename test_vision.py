import base64
import io

from openai import OpenAI
from PIL import ImageGrab


# =========================
# 9Router
# =========================

BASE_URL = "http://127.0.0.1:20128/v1"
API_KEY = "sk-9router"
MODEL = "kr/glm-5"


# =========================
# Capture screenshot
# =========================

print("📸 Đang chụp màn hình...")

image = ImageGrab.grab(all_screens=True)

print(f"🖥️ Screenshot: {image.width}x{image.height}")


# =========================
# Resize để giảm payload
# =========================

MAX_SIZE = 1600

if max(image.width, image.height) > MAX_SIZE:
    ratio = MAX_SIZE / max(image.width, image.height)

    new_size = (
        int(image.width * ratio),
        int(image.height * ratio),
    )

    image = image.resize(new_size)

    print(f"📐 Resize: {image.width}x{image.height}")


# =========================
# Convert PNG → Base64
# =========================

buffer = io.BytesIO()

image.save(buffer, format="PNG")

image_base64 = base64.b64encode(
    buffer.getvalue()
).decode("utf-8")


print(f"📦 Image size: {len(image_base64) / 1024:.1f} KB")


# =========================
# OpenAI Client
# =========================

client = OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY,
)


# =========================
# Vision request
# =========================

print(f"🧠 Gửi screenshot cho {MODEL}...")


response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": (
                        "Hãy phân tích screenshot này. "
                        "Mô tả ngắn gọn những gì đang hiển thị "
                        "trên màn hình Windows. "
                        "Nếu có cửa sổ ứng dụng, hãy nói tên ứng dụng."
                    ),
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": (
                            "data:image/png;base64,"
                            + image_base64
                        )
                    },
                },
            ],
        }
    ],
)


# =========================
# Result
# =========================

print()
print("=" * 60)
print("👁️ VISION RESULT")
print("=" * 60)

print(response.choices[0].message.content)

print("=" * 60)
print("✅ Vision test hoàn tất")