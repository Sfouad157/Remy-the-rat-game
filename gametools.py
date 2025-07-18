import time
import os

def write(text):
    """Print text with a pause for dramatic effect."""
    print(text)
    time.sleep(1)

def get_input(prompt):
    """Ask the user for input."""
    return input(f"{prompt} ")

def get_choice(prompt, options):
    """Display a list of choices and return the selected option."""
    print(f"\n{prompt}")
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    while True:
        choice = input("Enter the number of your choice: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return options[int(choice) - 1]
        else:
            print("Invalid choice. Try again.")

def pause():
    """Pause until user hits Enter."""
    input("\nPress Enter to continue...")

def clear():
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")