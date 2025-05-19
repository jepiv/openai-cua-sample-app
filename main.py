import argparse

from agent.agent import Agent
from computers import LocalPlaywrightBrowser, MacComputer, WindowsComputer


def main(user_input=None, target_env="browser"):
    """
    Main function to run the CUA agent with a specified computer environment.
    """
    computer_instance = None

    if target_env == "windows":
        try:
            computer_instance = WindowsComputer()
            print("Using WindowsComputer.")
        except ImportError:
            print(
                "PyAutoGUI or Pillow not installed. WindowsComputer cannot be used. "
                "Falling back to LocalPlaywrightBrowser."
            )
            computer_instance = LocalPlaywrightBrowser()
            print("Using LocalPlaywrightBrowser as fallback.")
        except Exception as e:
            print(
                f"Error initializing WindowsComputer: {e}. "
                "Falling back to LocalPlaywrightBrowser."
            )
            computer_instance = LocalPlaywrightBrowser()
            print("Using LocalPlaywrightBrowser as fallback.")
    elif target_env == "mac":
        try:
            computer_instance = MacComputer()
            print("Using MacComputer.")
        except ImportError:
            print(
                "PyAutoGUI or Pillow not installed. MacComputer cannot be used. "
                "Falling back to LocalPlaywrightBrowser."
            )
            computer_instance = LocalPlaywrightBrowser()
            print("Using LocalPlaywrightBrowser as fallback.")
        except Exception as e:
            print(
                f"Error initializing MacComputer: {e}. "
                "Falling back to LocalPlaywrightBrowser."
            )
            computer_instance = LocalPlaywrightBrowser()
            print("Using LocalPlaywrightBrowser as fallback.")
    elif target_env == "browser":
        computer_instance = LocalPlaywrightBrowser()
        print("Using LocalPlaywrightBrowser.")
    else:
        print(
            f"Unknown target environment: {target_env}. "
            "Defaulting to LocalPlaywrightBrowser."
        )
        computer_instance = LocalPlaywrightBrowser()

    if computer_instance is None:
        print("Failed to initialize any computer instance. Exiting.")
        return

    with computer_instance as computer:
        agent = Agent(computer=computer)
        items = []
        if user_input:  # For non-interactive mode with initial input
            items.append({"role": "user", "content": user_input})
            # Assuming run_full_turn handles further interaction or is a one-shot
            agent.run_full_turn(items, debug=True, show_images=True)
        else:  # Interactive loop
            while True:
                try:
                    cli_input = input("> ")
                    if cli_input.lower() == "exit":
                        print("Exiting...")
                        break
                    items.append({"role": "user", "content": cli_input})
                    output_items = agent.run_full_turn(
                        items, debug=True, show_images=True
                    )
                    items += output_items
                except KeyboardInterrupt:
                    print("\nExiting...")
                    break
                except Exception as e:
                    print(f"An error occurred in the main loop: {e}")
                    break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run the CUA agent with a specified computer environment."
    )
    parser.add_argument(
        "--env",
        type=str,
        default="browser",
        choices=["browser", "windows", "mac"],
        help=(
            "Specify the target environment: 'browser', 'windows', or 'mac'. "
            "Default is 'browser'."
        ),
    )
    args = parser.parse_args()

    main(target_env=args.env)
