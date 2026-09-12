import asyncio
import pyautogui
import pyperclip
from system_utils import SystemUtils


class ComputerTools:
    """
    Bộ công cụ điều khiển Windows cho DAI Computer Agent.

    AI không gọi pyautogui trực tiếp.
    Mọi thao tác GUI đều đi qua lớp này.
    """

    @staticmethod
    def screenshot():
        """
        Chụp toàn bộ desktop.
        """
        ok, result = SystemUtils.capture_screenshot()

        if not ok:
            return {
                "success": False,
                "error": str(result),
            }

        return {
            "success": True,
            "image": result,
        }

    @staticmethod
    def screen_size():
        """
        Trả về kích thước màn hình chính.
        """
        width, height = pyautogui.size()

        return {
            "success": True,
            "width": width,
            "height": height,
        }

    @staticmethod
    def mouse_position():
        """
        Lấy vị trí chuột hiện tại.
        """
        x, y = pyautogui.position()

        return {
            "success": True,
            "x": x,
            "y": y,
        }

    @staticmethod
    def move_mouse(x: int, y: int, duration: float = 0.2):
        """
        Di chuyển chuột tới tọa độ.
        """
        pyautogui.moveTo(
            int(x),
            int(y),
            duration=max(0, float(duration)),
        )

        return {
            "success": True,
            "x": int(x),
            "y": int(y),
        }

    @staticmethod
    def click(
        x: int | None = None,
        y: int | None = None,
        button: str = "left",
        clicks: int = 1,
    ):
        """
        Click chuột.
        """

        if x is not None and y is not None:
            pyautogui.moveTo(int(x), int(y), duration=0.15)

        pyautogui.click(
            button=button,
            clicks=int(clicks),
            interval=0.08,
        )

        return {
            "success": True,
            "action": "click",
            "button": button,
            "clicks": int(clicks),
        }

    @staticmethod
    def double_click(x: int, y: int):
        """
        Double click.
        """
        pyautogui.doubleClick(
            int(x),
            int(y),
            interval=0.1,
        )

        return {
            "success": True,
            "action": "double_click",
            "x": int(x),
            "y": int(y),
        }

    @staticmethod
    def right_click(x: int, y: int):
        """
        Right click.
        """
        pyautogui.rightClick(int(x), int(y))

        return {
            "success": True,
            "action": "right_click",
            "x": int(x),
            "y": int(y),
        }

    @staticmethod
    def drag(
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        duration: float = 0.5,
        button: str = "left",
    ):
        """
        Kéo chuột.
        """
        pyautogui.moveTo(int(x1), int(y1), duration=0.15)

        pyautogui.dragTo(
            int(x2),
            int(y2),
            duration=max(0.1, float(duration)),
            button=button,
        )

        return {
            "success": True,
            "action": "drag",
        }

    @staticmethod
    def scroll(amount: int):
        """
        Cuộn chuột.
        """
        pyautogui.scroll(int(amount))

        return {
            "success": True,
            "action": "scroll",
            "amount": int(amount),
        }

    @staticmethod
    def type_text(text: str, interval: float = 0.01):
        """
        Gõ văn bản Unicode vào cửa sổ đang active
        thông qua Clipboard + Ctrl+V.
        """
        text = str(text)

        old_clipboard = None

        try:
            try:
                old_clipboard = pyperclip.paste()
            except Exception:
                pass

            pyperclip.copy(text)

            pyautogui.hotkey("ctrl", "v")

            # Chờ rất ngắn để Windows/app nhận dữ liệu.
            if interval > 0:
                import time
                time.sleep(min(float(interval), 0.2))

            return {
                "success": True,
                "action": "type_unicode",
                "length": len(text),
            }

        except Exception as exc:
            return {
                "success": False,
                "action": "type_unicode",
                "error": str(exc),
            }

        finally:
            # Khôi phục clipboard nếu có thể.
            if old_clipboard is not None:
                try:
                    pyperclip.copy(old_clipboard)
                except Exception:
                    pass

    @staticmethod
    def press(key: str):
        """
        Nhấn một phím.
        """
        pyautogui.press(str(key))

        return {
            "success": True,
            "action": "press",
            "key": str(key),
        }

    @staticmethod
    def hotkey(*keys: str):
        """
        Nhấn tổ hợp phím.
        """
        pyautogui.hotkey(*[str(k) for k in keys])

        return {
            "success": True,
            "action": "hotkey",
            "keys": list(keys),
        }

    @staticmethod
    async def wait(seconds: float = 1.0):
        """
        Chờ để GUI ổn định.
        """
        seconds = max(0, min(float(seconds), 30))

        await asyncio.sleep(seconds)

        return {
            "success": True,
            "action": "wait",
            "seconds": seconds,
        }

    @staticmethod
    async def run_command(
        command: str,
        cwd: str,
        timeout: int = 60,
    ):
        """
        Chạy PowerShell thông qua SecurityGuard hiện tại.
        """
        return_code, output = await SystemUtils.run_shell_command(
            command=command,
            cwd=cwd,
            timeout=timeout,
        )

        return {
            "success": return_code == 0,
            "return_code": return_code,
            "output": output,
        }