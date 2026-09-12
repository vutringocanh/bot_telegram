import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

base_url = os.getenv("ROUTER_BASE_URL")
api_key = os.getenv("ROUTER_API_KEY")
model = os.getenv("ROUTER_MODELS", "kr/glm-5").split(",")[0].strip()

print("Base URL:", base_url)
print("Model:", model)

client = OpenAI(
    base_url=base_url,
    api_key=api_key,
)

response = client.chat.completions.create(
    model=model,
    messages=[
        {
            "role": "user",
            "content": "Trả lời đúng một câu: Python đã kết nối thành công với 9Router."
        }
    ],
)

print()
print("AI:", response.choices[0].message.content)