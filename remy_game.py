from gametools import write, get_input, get_choice, pause, clear

inventory = []
game_state = {
    "timeline_fragments": 0,
    "scent_log": [],
    "temple_rewarded": False,
    "market_rewarded": False,
    "factory_rewarded": False,
    "whispering_wall_seen": False,
    "blueprint_seen": False,
    "rebel_helped": False,
    "temple_secret_done": False,
    "factory_sabotaged": False,
    "energy": 7,
}

def log_event(text):
    game_state["scent_log"].append(text)
    write(f"\n New log entry: {text}", delay=0.02, pause_after=1.5)

def print_energy_meter():
    write(f"\n Energy Remaining: {game_state['energy']}/7", delay=0.01, pause_after=1.5)

def scene_transition(scene_function):
    game_state["energy"] -= 1
    print_energy_meter()
    if game_state["energy"] <= 0:
        return scene_riddle_ending
    return scene_function

def scene_lab_disaster():
    clear()
    write("You're Remy, a curious lab rat. You chew on a glowing wire...")
    pause()
    write("BOOM! A time explosion sends you across eras.")
    log_event("Caused a time mess by nibbling shiny tech.")
    return scene_time_hub

def scene_time_hub():
    clear()
    write("You land in the Chrono-Hub — a swirling portal nexus connecting all timelines.")
    print_energy_meter()
    pause()
    while True:
        choice = get_choice("Where would you like to go?", [
            "Ancient Temple",
            "Medieval Market",
            "Industrial Factory",
            "Meet the Rebel Rats",
            "Enter the Nexus"
        ])
        if choice == "Ancient Temple":
            return scene_transition(scene_ancient_temple)
        elif choice == "Medieval Market":
            return scene_transition(scene_medieval_market)
        elif choice == "Industrial Factory":
            return scene_transition(scene_factory)
        elif choice == "Meet the Rebel Rats":
            return scene_transition(scene_rebel_rats)
        elif choice == "Enter the Nexus":
            return scene_transition(scene_nexus)

def scene_ancient_temple():
    clear()
    write("You arrive in an ancient temple filled with cat statues and glowing glyphs.")

    cheese_taken = "glowing cheese" in inventory
    maze_done = game_state["timeline_fragments"] >= 1
    secret_done = game_state.get("temple_secret_done", False)

    while True:
        options = []
        if not cheese_taken:
            options.append("Cheese altar")
        if not maze_done:
            options.append("Maze puzzle")
        if "rat disguise" in inventory and not secret_done:
            options.append("Crawl into secret tunnel")
        options.append("Leave the temple")

        choice = get_choice("What do you want to explore?", options)

        if choice == "Cheese altar":
            inventory.append("glowing cheese")
            game_state["energy"] += 1
            log_event("Ate sacred cheese. Energy +1!")
            cheese_taken = True

        elif choice == "Maze puzzle":
            game_state["timeline_fragments"] += 1
            log_event("You take several lefts and then a few rights and after being lost longer than you would like to admit... you solve the maze and get a time shard!")
            maze_done = True

        elif choice == "Crawl into secret tunnel":
            log_event("Found a hidden chamber of cheese relics.")
            write("You find ancient relics and a mural of a rat holding a golden cheese.")
            game_state["temple_secret_done"] = True

        elif choice == "Leave the temple":
            break

    if not game_state["temple_rewarded"]:
        game_state["temple_rewarded"] = cheese_taken or maze_done

    if not game_state["whispering_wall_seen"]:
        write("\nYou hear a faint whisper behind the wall...")
        pause()
        write("A voice says: 'Three shards will show the way... only cheese may unlock the truth.'")
        log_event("Heard the Whispering Wall.")
        game_state["whispering_wall_seen"] = True

    return scene_time_hub

def scene_medieval_market():
    clear()
    write("You pop out into a medieval market. Humans yell, carts crash, cheese everywhere.")

    cheese_stolen = "aged cheese" in inventory
    disguise_traded = "rat disguise" in inventory

    while True:
        options = []
        if not cheese_stolen:
            options.append("Steal cheese")
        if not disguise_traded:
            options.append("Trade disguise")
        options.append("Leave the market")

        choice = get_choice("What do you want to do?", options)

        if choice == "Steal cheese":
            inventory.append("aged cheese")
            game_state["market_rewarded"] = True
            game_state["energy"] += 1
            log_event("Energy +1 from aged cheese.")
            cheese_stolen = True

        elif choice == "Trade disguise":
            inventory.append("rat disguise")
            game_state["market_rewarded"] = True
            log_event("Traded for a rat disguise. Maybe it helps blend in somewhere... mysterious.")
            disguise_traded = True

        elif choice == "Leave the market":
            break

    return scene_time_hub

def scene_factory():
    clear()
    write("You're now in a steamy, dangerous industrial factory.")

    shard_found = game_state["timeline_fragments"] >= 2
    blueprint_seen = game_state["blueprint_seen"]
    sabotage_done = game_state["factory_sabotaged"]

    while True:
        options = []
        if not shard_found:
            options.append("Search the steam vents")
        if not blueprint_seen:
            options.append("Check behind the control panel")
        if game_state["rebel_helped"] and not sabotage_done:
            options.append("Help rebels sabotage machine")
        options.append("Leave the factory")

        choice = get_choice("What do you want to do?", options)

        if choice == "Search the steam vents":
            game_state["timeline_fragments"] += 1
            game_state["factory_rewarded"] = True
            log_event("Recovered a gear-shaped shard from the factory.")
            shard_found = True

        elif choice == "Check behind the control panel":
            write("You find a blueprint labeled: 'Temporal Snackifier – Rev B. Powered by cheese.'")
            game_state["blueprint_seen"] = True
            log_event("Found blueprint for cheese-powered device.")
            blueprint_seen = True

        elif choice == "Help rebels sabotage machine":
            write("You quietly insert a jammed cog. Steam bursts and sparks fly.")
            log_event("Assisted rebel rats with sabotage.")
            game_state["factory_sabotaged"] = True

        elif choice == "Leave the factory":
            break

    return scene_time_hub

def scene_rebel_rats():
    clear()
    if not game_state["rebel_helped"]:
        if game_state.get("temple_secret_done"):
            write("In a quiet vent shaft, you find a group of rebel rats holding a cheese-powered lantern.")
            write("Their leader, Whiskers, says: 'Remy, we’ve heard of your journey. Help us unite the timelines.'")
            log_event("Met the Rebel Rats and gained their trust.")
            game_state["rebel_helped"] = True
        else:
            write("You stumble into a quiet vent shaft filled with whispering rats.")
            write("The leader eyes you cautiously. 'Unless you've seen the ancient secrets, we cannot trust you.'")
            write("Maybe you missed something in a place you’ve already been...")
            pause()
            return scene_time_hub
    else:
        write("You return to the rebel rats. Whiskers nods. 'We’re rooting for you, Remy.'")
    pause()
    return scene_time_hub

def scene_nexus():
    clear()
    write("You've reached the Timeless Nest. Gears spin, portals flicker.")
    pause()

    if game_state["timeline_fragments"] >= 2:
        return ending_success
    else:
        return scene_riddle_ending

def ending_success():
    clear()
    write("You restored the timeline! You return to the lab.")
    write("However you don't remember the cat wearing that monocle much less talking originally...")

    if game_state["whispering_wall_seen"] and game_state["blueprint_seen"]:
        pause()
        write("You see a glowing cube on the lab bench.")
        write("It says: 'Temporal Snackifier Rev B. Push if hungry.'")
        write("You press it... and a grilled cheese sandwich appears.")
        log_event("Unlocked the secret cheese-powered ending.")
        write("You munch happily. Timeline saved. Hunger defeated.")

    if game_state["rebel_helped"] and game_state["factory_sabotaged"]:
        write("Whiskers the rebel rat salutes you from the shadows.")
        log_event("Rebel Rats helped restore peace across timelines.")

    write("\nTHE END — Timeline Restored")
    write("\n(But perhaps your choices could lead to other endings...)")
    return None

def scene_riddle_ending():
    clear()
    write("You collapse into a bubble of paradox cheese space.")
    write("A glowing voice speaks:")
    write("\n'I can be yellow or blue, soft or hard; on a burger or mac, often starred.\nWhat am I?'")
    answer = get_input("Your answer: ").strip().lower()
    if "cheese" in answer:
        write("\nThe paradox accepts your cheesy wisdom.")
        write("Time repairs itself around your answer. A grilled cheese floats by.")
        log_event("Solved riddle and earned the secret cheese ending.")
    else:
        return ending_failure
    write("\nTHE END — Cheese Fate Decided")
    return None

def ending_failure():
    clear()
    write("You failed to recover enough timeline fragments.")
    write("The paradox swallows all. Even the cheese.")
    return None

def main():
    current_scene = scene_lab_disaster
    while current_scene:
        current_scene = current_scene()

if __name__ == "__main__":
    main()