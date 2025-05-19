import base64
from io import BytesIO
from typing import List, Literal, Dict

import pyautogui
from PIL import ImageGrab  # For consistent screenshotting with MacComputer

from ..computer import Computer


class WindowsComputer(Computer):
    """
    A Computer implementation for interacting with a Windows desktop environment.
    """

    def __init__(self):
        # pyautogui.FAILSAFE = False # Useful for debugging, disable for production
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def get_environment(self) -> Literal["windows", "mac", "linux", "browser"]:
        return "windows"

    def get_dimensions(self) -> tuple[int, int]:
        """Gets the primary screen's width and height."""
        width, height = pyautogui.size()
        return width, height

    def screenshot(self) -> str:
        """
        Captures a screenshot of the primary screen using Pillow's ImageGrab,
        returns it as a base64 encoded string.
        """
        try:
            img = ImageGrab.grab()
            if img is None:
                raise ValueError("ImageGrab.grab() returned None, screenshot failed.")

            buffered = BytesIO()
            img.save(buffered, format="PNG")
            img_bytes = buffered.getvalue()
            img_str = base64.b64encode(img_bytes).decode("utf-8")

            if not img_str:
                raise ValueError("Base64 string is empty after encoding screenshot.")
            return img_str
        except Exception as e:
            print(f"Error taking screenshot on Windows: {e}")
            # Fallback to prevent breaking the agent
            return "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="

    def click(self, x: int, y: int, button: str = "left") -> None:
        """Clicks at the specified coordinates."""
        pyautogui.click(x, y, button=button)

    def double_click(self, x: int, y: int) -> None:
        """Double clicks at the specified coordinates."""
        pyautogui.doubleClick(x, y)

    def scroll(self, x: int, y: int, scroll_x: int, scroll_y: int) -> None:
        """Scrolls the window currently under the mouse cursor."""
        pyautogui.moveTo(x, y)
        if scroll_y != 0:
            # Positive scroll_y scrolls up, negative scrolls down.
            pyautogui.scroll(scroll_y)
        if scroll_x != 0:
            # Positive scroll_x scrolls right, negative scrolls left.
            if hasattr(pyautogui, "hscroll"):
                pyautogui.hscroll(scroll_x)
            else:
                print(
                    "Horizontal scroll (hscroll) not directly available in this pyautogui version."
                )

    def type(self, text: str) -> None:
        """Types the given text."""
        pyautogui.typewrite(text)

    def wait(self, ms: int = 1000) -> None:
        """Waits for a specified number of milliseconds."""
        pyautogui.sleep(ms / 1000)

    def move(self, x: int, y: int) -> None:
        """Moves the mouse cursor to the specified coordinates."""
        pyautogui.moveTo(x, y)

    def keypress(self, keys: List[str]) -> None:
        """Presses and releases a sequence of keys."""
        # For modifier keys held down (e.g., Ctrl+C), pyautogui.hotkey('ctrl', 'c')
        # or managing keyDown/keyUp separately would be needed.
        # This implementation presses each key in the list sequentially.
        for key in keys:
            pyautogui.press(key)

    def drag(self, path: List[Dict[str, int]]) -> None:
        """Performs a drag operation along the specified path."""
        if not path:
            return

        start_x, start_y = path[0]["x"], path[0]["y"]
        pyautogui.moveTo(start_x, start_y)
        pyautogui.mouseDown()

        for point in path[1:]:
            pyautogui.moveTo(point["x"], point["y"], duration=0.1)

        pyautogui.mouseUp()

    def get_current_url(self) -> str:
        """
        For Windows desktop, attempts to return the title of the active window.
        """
        try:
            active_window = pyautogui.getActiveWindow()
            if (
                active_window
                and hasattr(active_window, "title")
                and active_window.title
            ):
                return active_window.title
            return "Active Window (Title N/A or empty)"
        except Exception as e:
            # pyautogui.getActiveWindow() can fail or return None.
            print(f"Could not get active window title on Windows: {e}")
            return "Active Window (Error retrieving title)"


if __name__ == "__main__":
    print("Testing WindowsComputer (requires a Windows environment with a GUI).")
    try:
        computer = WindowsComputer()
        with computer:
            print(f"Environment: {computer.get_environment()}")
            dims = computer.get_dimensions()
            print(f"Screen Dimensions: {dims}")
            # Example: Test screenshot
            # print("Taking screenshot in 3s...")
            # computer.wait(3000)
            # b64_img = computer.screenshot()
            # if b64_img and not b64_img.startswith("iVBOR"): # Check if not fallback
            #     print(f"Screenshot taken (first 50 chars): {b64_img[:50]}...")
            # else:
            #     print("Screenshot fallback or error.")
    except ImportError:
        print(
            "PyAutoGUI or Pillow not installed. Please install them to test WindowsComputer."
        )
    except Exception as e:
        print(f"An error occurred during WindowsComputer test: {e}")
