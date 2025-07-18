import time
import os
from gametools import write, get_input, get_choice, pause, clear

# Game State
inventory = []
game_state = {
    "time_energy": 7,
    "timeline_fragments": 0,
    "scent_log": [],
    "visited_scenes": [],
    "helped_rat_rebels": False,
    "temple_rewarded": False,
    "market_rewarded": False,
    "factory_rewarded": False,
    "whispering_wall_seen": False,
    "blueprint_seen": False
}

def log_event(text):
    game_state["scent_log"].append(text)

def use_time_energy():
    game_state["time_energy"] -= 1
    if game_state["time_energy"] <= 0:
        return paradox_pit
    return None

# Scenes
def scene_lab_disaster():
    clear()
    write("You're Remy, a curious lab rat. You chew on a glowing wire...")
    pause()
    write("BOOM! A time explosion sends you across eras.")
    log_event("Caused a time mess by nibbling shiny tech.")
    game_state["visited_scenes"].append("Lab")
    return scene_ancient_temple

def scene_ancient_temple():
    clear()
    write("Dust. Statues. Ancient Temple. Cat statues glare at you.")
    if "Temple" not in game_state["visited_scenes"]:
        game_state["visited_scenes"].append("Temple")

    if not game_state["temple_rewarded"]:
        choice = get_choice("What do you explore?", ["Cheese altar", "Maze puzzle", "Avoid everything"])
        if choice == "Cheese altar":
            inventory.append("glowing cheese")
            game_state["time_energy"] += 2
            game_state["temple_rewarded"] = True
            log_event("Ate sacred cheese. Worth it.")
        elif choice == "Maze puzzle":
            game_state["timeline_fragments"] += 1
            game_state["temple_rewarded"] = True
            log_event("Solved the maze and got a timeline shard.")
        else:
            write("You stay hidden in a crack. Nothing gained.")
    else:
        write("You've already explored this area.")

    if (
        "Market" in game_state["visited_scenes"]
        and game_state["temple_rewarded"]
        and not game_state["whispering_wall_seen"]
    ):
        write("\nAs you explore again, you notice a faint humming behind the wall...")
        pause()
        write("You press your ear against the stone.")
        write("A soft whisper echoes: 'Three shards will show the way... but only cheese may unlock the truth.'")
        log_event("Heard the Whispering Wall in the temple.")
        game_state["whispering_wall_seen"] = True

    return scene_time_hub

def scene_medieval_market():
    clear()
    write("The market bustles with noise. You sniff around for mischief.")
    if "Market" not in game_state["visited_scenes"]:
        game_state["visited_scenes"].append("Market")

    if not game_state["market_rewarded"]:
        choice = get_choice("Try your luck at:", ["Stealing cheese", "Trading disguise", "Scurry off"])
        if choice == "Stealing cheese":
            inventory.append("aged cheese")
            game_state["market_rewarded"] = True
            log_event("Snatched aged cheese from a stall.")
        elif choice == "Trading disguise":
            inventory.append("rat disguise")
            game_state["market_rewarded"] = True
            log_event("Got disguise gear from a shady mouse.")
        else:
            write("You avoid trouble and hide.")
    else:
        write("You've already taken what you can from here.")

    return scene_time_hub

def scene_factory():
    clear()
    write("Hissing pipes. Loud gears. A ratcatcher nearby.")
    if "Factory" not in game_state["visited_scenes"]:
        game_state["visited_scenes"].append("Factory")

    if not game_state["factory_rewarded"]:
        write("You navigate steam vents and find a gear-shaped shard.")
        game_state["timeline_fragments"] += 1
        game_state["factory_rewarded"] = True
        log_event("Found a gear shard in the factory.")
    else:
        write("The factory is quiet. You’ve been here before.")

    if (
        "Temple" in game_state["visited_scenes"]
        and game_state["factory_rewarded"]
        and not game_state["blueprint_seen"]
    ):
        write("\nBehind a rusted panel, you spot a faded piece of blueprint paper...")
        pause()
        write("It shows... a strange device powered by cheese? It's labeled: 'Temporal Snackifier Prototype - Rev B'")
        log_event("Found the cheese-powered machine blueprint in the factory.")
        game_state["blueprint_seen"] = True

    return scene_time_hub

def scene_nexus():
    clear()
    write("You enter the Timeless Nest. Floating gears and glowing fragments surround you.")
    game_state["visited_scenes"].append("Nexus")
    if game_state["timeline_fragments"] >= 3:
        return ending_success
    else:
        return paradox_pit

def paradox_pit():
    clear()
    write("You fall into the Paradox Pit...")
    write("I can be yellow or blue, soft or hard;")
    write("on a burger or mac, often starred.")
    answer = get_input("What am I? ").lower().strip()
    if "cheese" in answer:
        return scene_nexus
    else:
        return ending_failure

def ending_success():
    clear()
    write("You restored the timeline! You return to the lab.")
    write("Although you don’t remember the cat wearing a monocle when you left…'")

    if game_state["whispering_wall_seen"] and game_state["blueprint_seen"]:
        write("\nAs you glance at the lab table, something glows beneath the clutter...")
        pause()
        write("It's a small metallic cube with a cheese-shaped button.")
        write("A note beside it reads: 'Temporal Snackifier Rev B — Do NOT press unless you're feeling... cheesy.'")
        write("You press it. The lights flicker. A faint hum. And then—")
        write("A steaming grilled cheese sandwich appears on a pedestal.")
        write("You munch happily, having not just saved time—but lunch, too.")
        log_event("Unlocked the secret cheese-powered device ending.")

    write("\nTHE END — Timeline Restored")
    return None

def ending_failure():
    clear()
    write("The paradox wins. You fade from existence.")
    return None

# Time Travel Hub
def scene_time_hub():
    clear()
    write("You float in a bubble outside time. Where do you want to go?")
    options = []

    if "Temple" in game_state["visited_scenes"]:
        options.append("Revisit the Ancient Temple")
    if "Market" in game_state["visited_scenes"]:
        options.append("Revisit the Medieval Market")
    if "Factory" in game_state["visited_scenes"]:
        options.append("Revisit the Industrial Factory")
    if "Nexus" not in game_state["visited_scenes"]:
        options.append("Continue to the Timeless Nest")

    choice = get_choice("Choose your destination:", options)

    result = use_time_energy()
    if result:
        return result

    if "Temple" in choice:
        return scene_ancient_temple
    elif "Market" in choice:
        return scene_medieval_market
    elif "Factory" in choice:
        return scene_factory
    elif "Nexus" in choice:
        return scene_nexus

# Game Loop
def main():
    current_scene = scene_lab_disaster
    while current_scene:
        current_scene = current_scene()

if __name__ == "__main__":
    main()
