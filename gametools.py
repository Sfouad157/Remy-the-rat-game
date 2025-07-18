import os
import sys
import time

def write(text, delay=0.02, pause_after=1.5):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()
    time.sleep(pause_after)

def get_input(prompt):
    return input(f"{prompt} ")

def get_choice(prompt, options):
    write(prompt)
    for i, option in enumerate(options, 1):
        write(f"{i}. {option}", delay=0.01, pause_after=0.3)
    while True:
        choice = input("Enter the number of your choice: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return options[int(choice) - 1]
        else:
            print("Invalid choice. Try again.")

def pause():
    input("\nPress Enter to continue...")

def clear():
    os.system("cls" if os.name == "nt" else "clear")