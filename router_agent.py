import logging
import time
from typing import AsyncGenerator, Callable, Optional

from openai import OpenAI

from agent_base import AgentEvent, AgentSession, AgentType, BaseAgentRunner
from config import Config

logger = logging.getLogger(__name__)


class RouterAgentRunner(BaseAgentRunner):
    """Agent runner sử dụng 9Router qua OpenAI-compatible API."""

    @property
    def agent_type(self) -> str:
        return AgentType.ROUTER

    @property
    def display_name(self) -> str:
        return "🌐 9Router"

    @property
    def emoji(self) -> str:
        return "🌐"

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
                f"🌐 9Router → {model}"
            )

        yield AgentEvent(
            event_type="init",
            agent_type=self.agent_type,
            content=f"9Router / {model}",
        )

        try:
            client = self._get_client()

            # Khởi tạo history nếu chưa có
            if not session.history:
                session.history = [
                    {
                        "role": "system",
                        "content": (
                            "Bạn là AI coding agent chạy trên Windows. "
                            "Hãy trả lời ngắn gọn, chính xác và tập trung "
                            "vào việc hoàn thành yêu cầu của người dùng."
                        ),
                    }
                ]

            session.history.append(
                {
                    "role": "user",
                    "content": prompt,
                }
            )

            response = client.chat.completions.create(
                model=model,
                messages=session.history,
            )

            content = ""

            if response.choices:
                content = (
                    response.choices[0].message.content
                    or ""
                )

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
                },
            )

        except Exception as exc:
            logger.exception("9Router execution failed")

            duration = time.time() - start_time

            yield AgentEvent(
                event_type="error",
                agent_type=self.agent_type,
                content=f"9Router lỗi: {exc}",
                duration_seconds=duration,
            )