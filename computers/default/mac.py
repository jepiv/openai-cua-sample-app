import base64
from io import BytesIO
from typing import List, Literal, Dict

import pyautogui
from PIL import ImageGrab

from ..computer import Computer


class MacComputer(Computer):
    """
    A Computer implementation for interacting with a macOS desktop environment.
    """

    def __init__(self):
        # Note: macOS has stricter security for GUI automation.
        # Users might need to grant accessibility permissions to the terminal/Python.
        print(
            "Initializing MacComputer. "
            "Ensure necessary accessibility permissions are granted."
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def get_environment(self) -> Literal["windows", "mac", "linux", "browser"]:
        return "mac"

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
            print(f"Error taking screenshot on macOS: {e}")
            # Fallback to prevent breaking the agent
            return "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="

    def click(self, x: int, y: int, button: str = "left") -> None:
        pyautogui.click(x, y, button=button)

    def double_click(self, x: int, y: int) -> None:
        pyautogui.doubleClick(x, y)

    def scroll(self, x: int, y: int, scroll_x: int, scroll_y: int) -> None:
        pyautogui.moveTo(x, y)
        if scroll_y != 0:
            # On macOS, pyautogui.scroll behavior for scroll_y direction might differ.
            # Positive usually means scroll down, negative means scroll up.
            # This matches the typical expectation, so no inversion is applied here.
            # If testing shows opposite behavior on a specific macOS setup,
            # `pyautogui.scroll(-scroll_y)` might be needed.
            pyautogui.scroll(scroll_y)
        if scroll_x != 0:
            if hasattr(pyautogui, "hscroll"):
                pyautogui.hscroll(scroll_x)
            else:
                print(
                    "Horizontal scroll (hscroll) not directly available in this pyautogui version."
                )

    def type(self, text: str) -> None:
        pyautogui.typewrite(text)

    def wait(self, ms: int = 1000) -> None:
        pyautogui.sleep(ms / 1000)

    def move(self, x: int, y: int) -> None:
        pyautogui.moveTo(x, y)

    def keypress(self, keys: List[str]) -> None:
        for key in keys:
            pyautogui.press(key)

    def drag(self, path: List[Dict[str, int]]) -> None:
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
        For macOS desktop, attempts to return the title of the frontmost window.
        Note: PyAutoGUI's ability to get window titles on macOS can be limited
        and might require specific accessibility permissions.
        """
        try:
            # PyAutoGUI's getActiveWindow() might have limitations on macOS.
            active_window = pyautogui.getActiveWindow()
            if (
                active_window
                and hasattr(active_window, "title")
                and active_window.title
            ):
                return active_window.title
            return "Frontmost App (Title N/A or empty)"
        except Exception as e:
            print(f"Could not get active window title on macOS with PyAutoGUI: {e}")
            return "Frontmost App (Error retrieving title)"


if __name__ == "__main__":
    print(
        "Testing MacComputer (requires a macOS environment with a GUI "
        "and accessibility permissions for Python/terminal)."
    )
    try:
        computer = MacComputer()
        with computer:
            print(f"Environment: {computer.get_environment()}")
            dims = computer.get_dimensions()
            print(f"Screen Dimensions: {dims}")
    except ImportError:
        print("PyAutoGUI or Pillow not installed.")
    except Exception as e:
        print(f"An error occurred during MacComputer test: {e}")
