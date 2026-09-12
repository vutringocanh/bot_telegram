import json
import logging
import time
from typing import AsyncGenerator, Callable, Optional

from openai import OpenAI

from agent_base import (
    AgentEvent,
    AgentSession,
    AgentType,
    BaseAgentRunner,
)
from config import Config
from tool_registry import TOOLS, execute_tool


logger = logging.getLogger(__name__)


MAX_TOOL_ROUNDS = 20


class RouterAgentRunner(BaseAgentRunner):
    """
    DAI Computer Agent.

    9Router = backend/model provider.
    RouterAgentRunner = agent brain/orchestrator.
    """

    @property
    def agent_type(self) -> str:
        return AgentType.ROUTER

    @property
    def display_name(self) -> str:
        return "🧠 DAI Computer Agent"

    @property
    def emoji(self) -> str:
        return "🧠"

    def _get_client(self) -> OpenAI:
        return OpenAI(
            base_url=Config.ROUTER_BASE_URL,
            api_key=Config.ROUTER_API_KEY,
        )

    def get_available_models(self) -> list[tuple[str, str]]:
        return [
            (model, model)
            for model in Config.ROUTER_MODELS
        ]

    def get_available_efforts(self) -> list[tuple[str, str]]:
        return [
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
        ]

    def _system_prompt(self) -> str:
        return """
Bạn là DAI Computer Agent, một AI agent có quyền điều khiển máy tính Windows.

Bạn không chỉ trả lời người dùng bằng văn bản.

Bạn có thể:
- nhìn trạng thái máy tính thông qua screenshot
- điều khiển chuột
- click
- double click
- right click
- kéo chuột
- scroll
- gõ bàn phím
- nhấn phím
- dùng hotkey
- chờ ứng dụng phản hồi

NGUYÊN TẮC:

1. Khi người dùng yêu cầu thực hiện một hành động trên máy tính,
   hãy THỰC HIỆN hành động đó bằng tool thay vì chỉ hướng dẫn.

2. Nếu chưa biết trạng thái màn hình,
   hãy dùng screenshot trước.

3. Sau một hành động quan trọng,
   hãy screenshot lại để kiểm tra kết quả.

4. Không tự bịa tọa độ.
   Khi cần tọa độ GUI, phải quan sát screenshot.

5. Nếu một thao tác không thành công,
   hãy quan sát lại và thử phương án khác.

6. Có thể thực hiện nhiều tool liên tiếp để hoàn thành một nhiệm vụ.

7. Không dừng giữa chừng chỉ vì một tool thành công.
   Hãy kiểm tra xem mục tiêu cuối cùng đã hoàn thành chưa.

8. Khi hoàn thành, trả lời ngắn gọn cho người dùng.

Bạn đang chạy trên Windows.
Workspace hiện tại sẽ được cung cấp trong context của agent.
"""

    async def execute_prompt(
        self,
        session: AgentSession,
        prompt: str,
        workspace_dir: str,
        on_status_update: Optional[Callable[[str], None]] = None,
    ) -> AsyncGenerator[AgentEvent, None]:

        start_time = time.time()
        model = session.model or Config.DEFAULT_ROUTER_MODEL

        if on_status_update:
            on_status_update(
                f"🧠 DAI Computer Agent → {model}"
            )

        yield AgentEvent(
            event_type="init",
            agent_type=self.agent_type,
            content=f"DAI Computer Agent / {model}",
        )

        try:
            client = self._get_client()

            if not session.history:
                session.history = [
                    {
                        "role": "system",
                        "content": self._system_prompt(),
                    }
                ]

            session.history.append(
                {
                    "role": "user",
                    "content": (
                        f"Workspace hiện tại: {workspace_dir}\n\n"
                        f"Yêu cầu người dùng:\n{prompt}"
                    ),
                }
            )

            for round_number in range(1, MAX_TOOL_ROUNDS + 1):

                if on_status_update:
                    on_status_update(
                        f"🧠 Đang suy nghĩ... bước {round_number}"
                    )

                response = client.chat.completions.create(
                    model=model,
                    messages=session.history,
                    tools=TOOLS,
                    tool_choice="auto",
                )

                if not response.choices:
                    break

                message = response.choices[0].message

                # -------------------------------------------------
                # MODEL TRẢ VỀ TEXT → HOÀN THÀNH
                # -------------------------------------------------

                if not message.tool_calls:

                    content = message.content or ""

                    session.history.append(
                        {
                            "role": "assistant",
                            "content": content,
                        }
                    )

                    duration = time.time() - start_time

                    yield AgentEvent(
                        event_type="result",
                        agent_type=self.agent_type,
                        content=content,
                        duration_seconds=duration,
                        raw_data={
                            "model": model,
                            "tool_rounds": round_number,
                        },
                    )

                    return

                # -------------------------------------------------
                # MODEL YÊU CẦU TOOL
                # -------------------------------------------------

                assistant_tool_message = {
                    "role": "assistant",
                    "content": message.content or "",
                    "tool_calls": [],
                }

                for tool_call in message.tool_calls:

                    assistant_tool_message["tool_calls"].append(
                        {
                            "id": tool_call.id,
                            "type": "function",
                            "function": {
                                "name": tool_call.function.name,
                                "arguments": tool_call.function.arguments,
                            },
                        }
                    )

                session.history.append(
                    assistant_tool_message
                )

                # -------------------------------------------------
                # EXECUTE TOOLS
                # -------------------------------------------------

                for tool_call in message.tool_calls:

                    tool_name = tool_call.function.name

                    try:
                        arguments = json.loads(
                            tool_call.function.arguments or "{}"
                        )
                    except json.JSONDecodeError:
                        arguments = {}

                    if on_status_update:
                        on_status_update(
                            f"🛠️ {tool_name}"
                        )

                    yield AgentEvent(
                        event_type="tool_start",
                        agent_type=self.agent_type,
                        content=f"Đang chạy {tool_name}",
                        tool_name=tool_name,
                        tool_args=arguments,
                    )

                    tool_start = time.time()

                    try:
                        result = await execute_tool(
                            name=tool_name,
                            arguments=arguments,
                            workspace_dir=workspace_dir,
                        )

                    except Exception as tool_exc:

                        logger.exception(
                            "Tool execution failed: %s",
                            tool_name,
                        )

                        result = {
                            "success": False,
                            "error": str(tool_exc),
                        }

                    tool_duration = time.time() - tool_start

                    # -------------------------------------------------
                    # IMAGE RESULT
                    # -------------------------------------------------

                    if (
                        isinstance(result, dict)
                        and result.get("success")
                        and result.get("image") is not None
                    ):
                        image = result["image"]

                        # Hiện tại gửi metadata cho model.
                        # Vision loop sẽ được nâng cấp ở Phase 3.
                        tool_result = {
                            "success": True,
                            "type": "screenshot",
                            "message": (
                                "Đã chụp screenshot thành công. "
                                "Ảnh hiện chưa được truyền trực tiếp "
                                "vào model trong Phase 2."
                            ),
                        }

                    else:
                        tool_result = result

                    # -------------------------------------------------
                    # TOOL RESULT → MODEL
                    # -------------------------------------------------

                    try:
                        serialized_result = json.dumps(
                            tool_result,
                            ensure_ascii=False,
                            default=str,
                        )
                    except Exception:
                        serialized_result = str(tool_result)

                    session.history.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": serialized_result,
                        }
                    )

                    yield AgentEvent(
                        event_type="tool_done",
                        agent_type=self.agent_type,
                        content=serialized_result[:4000],
                        tool_name=tool_name,
                        tool_args=arguments,
                        duration_seconds=tool_duration,
                    )

            # ---------------------------------------------------------
            # MAX ROUNDS
            # ---------------------------------------------------------

            duration = time.time() - start_time

            yield AgentEvent(
                event_type="result",
                agent_type=self.agent_type,
                content=(
                    "⚠️ Agent đã đạt giới hạn số bước "
                    f"({MAX_TOOL_ROUNDS})."
                ),
                duration_seconds=duration,
                raw_data={
                    "model": model,
                    "tool_rounds": MAX_TOOL_ROUNDS,
                },
            )

        except Exception as exc:

            logger.exception(
                "DAI Computer Agent execution failed"
            )

            duration = time.time() - start_time

            yield AgentEvent(
                event_type="error",
                agent_type=self.agent_type,
                content=f"DAI Agent lỗi: {exc}",
                duration_seconds=duration,
            )