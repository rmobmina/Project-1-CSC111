"""CSC111 Project 1: Text Adventure Game

Instructions (READ THIS FIRST!)
===============================

This Python module contains the code for Project 1. Please consult
the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2024 CSC111 Teaching Team

###############################################################################
Side note: We used Python-TA to check our code.

    -   We were unable to get rid of print() and input() since they were a
    necessary part of the game experience we wanted to convey.
    -   We did not write doctests for any of the functions in this .py file
    because they were already done in game_data.py.
    -   The error regarding the game_data import we just decided to ignore.

Thank you for your understanding!
###############################################################################
"""

from game_data import GameController, World, Location, Player


###############################################################################
# functions that print vital background information and
# instructions at the start of the game
###############################################################################


def show_plot_menu() -> str:
    """Prints the plot of the game."""
    return """
    The Plot
    ==========
    You've got an important exam coming up this evening,
    and you've been studying for weeks. Last night was a
    particularly late night on campus. You had difficulty
    focusing, so rather than staying in one place, you studied in
    various places throughout campus as the night progressed.
    Unfortunately, when you woke up this morning, you were
    missing some important exam-related items. You cannot find
    your T-card, and you're nervous they won't let you into
    tonight's exam without it. Also, you seem to have misplaced
    your lucky exam pen -- even if they let you in, you can't
    possibly write with another pen! Finally, your instructor
    for the course lets you bring a cheat sheet - a handwritten
    page of information in the exam. Last night, you painstakingly
    crammed as much material onto a single page as humanly
    possible, but that's missing, too! All of this stuff must be
    around campus somewhere! Can you find all of it before
    your exam starts tonight?
    """


def show_objectives_menu() -> str:
    """Prints the objectives of the game."""
    return """
    Objectives
    ==========
    Your objectives in this game are as follows:
    1. Collect all essential items. These items are...
       - T-card
       - Cheat Sheet
       - Lucky Pen
    2. Return all essential items to your dorm room.
    3. Reach the exam centre after all essential items are returned.
    4. Do this all within 50 moves or less to win!

    Good luck on your adventure!
    """


###############################################################################
# helper functions that allow do_action to work properly in an organized manner
###############################################################################


def handle_go(player: Player, direction: str) -> None:
    """
    Handles player movement.
    Calls the player's move method with the specified direction.
    """
    player.move(direction)


def handle_look(location: Location) -> None:
    """
    Handles the look action.
    Calls the location's look_around method to describe the area.
    If an NPC is present, hints the player they can interact with them.
    Calls a function to reveal items available in the current location.
    """
    location.look_around()
    if location.has_npc:
        print("You found someone you recognize. Maybe speak to them?")
    reveal_items_in_location(location)


def handle_inventory(player: Player) -> None:
    """
    Displays the player's inventory.
    Calls the player's print_inventory method to list the
    items in the inventory.
    """
    player.print_inventory()


def handle_score(player: Player) -> None:
    """
    Displays the player's score.
    Uses print to show the current score by
    accessing the player's get_player_score method.
    """
    print(f'Current Score: {player.get_player_score()}')


def handle_quit(player: Player) -> None:
    """
    Handles the quit action.
    Sets the player's quit attribute to True, indicating
    the player wants to exit the game.
    """
    player.quit = True


def handle_speak(player: Player, location: Location) -> None:
    """
    Handles the speak action with an NPC if present.

        - If the location has been looked at and contains an NPC,
        initiates dialogue and updates the player's score.
        - If the location hasn't been looked at, advises the player to do so.
        - If no NPC is present, informs the player accordingly.
    """
    if location.looked and location.has_npc:
        location.talk_to_npc(player)
        player.add_score(location.get_npc_score())
    elif not location.looked:
        print("You might notice more if you look around first.")
    else:
        print("There's no one here to talk to.")


def handle_collect(location: Location, game_controller:
                   GameController, item_name: str) -> None:
    """
    Handles item collection. Attempts to collect the
    specified item. If successful, notifies the player.
    """
    item_collected = game_controller.collect_item(item_name, location)
    if item_collected:
        print("Better take this back to your dorm room.")


def handle_drop(player: Player, location: Location,
                game_controller: GameController, item_name: str) -> None:
    """
    Handles item dropping. Drops the specified item in the current location,
    or all items if no specific item is named.
    """
    if item_name == '':
        for curr_item in player.get_inventory():
            game_controller.drop_item(curr_item, location)
    else:
        game_controller.drop_item_name(item_name, location)


###############################################################################
# do_action interprets a player's choice as a string,
# maps it to a specific action and executes it
###############################################################################


def do_action(player: Player, location: Location,
              game_controller: GameController, choice: str) -> None:
    """Performs an action based on the player's choice."""

    # mapping the player's choice to the corresponding helper function
    # splits the choice string into a list to handle commands with arguments

    choice_lst = choice.lower().split(' ')

    # baseline requirement
    if choice_lst[0] == 'go':
        handle_go(player, choice_lst[1])

    # baseline requirement
    elif choice == 'look':
        handle_look(location)

    # baseline requirement
    elif choice == 'inventory':
        handle_inventory(player)

    # baseline requirement
    elif choice == 'score':
        handle_score(player)

    # baseline requirement
    elif choice == 'quit':
        handle_quit(player)

    # enhancement
    elif choice == 'speak':
        handle_speak(player, location)

    # enhancement
    elif choice_lst[0] == 'collect':
        item_name = ' '.join(choice_lst[1:])
        handle_collect(location, game_controller, item_name)

    # enhancement
    elif choice_lst[0] == 'drop':
        item_name = ' '.join(choice_lst[1:])
        handle_drop(player, location, game_controller, item_name)


###############################################################################
# these functions collectively enhance the player's interaction within
# a game environment by allowing them to choose and execute actions, learn
# about specific commands, and discover items within their current location.
###############################################################################


def choose_action(chosen_action: str) -> None:
    """Allows the player to choose an action from the available actions."""
    # check if the chosen action is to display the menu
    if chosen_action == 'menu':
        print("[menu]")
        # display all available actions in the current location
        for action in loc.get_available_actions():
            print(action)
        # prompt the player to enter their choice of action
        chosen_action = input("\nEnter action: ")

    # check if the chosen action is to display help for a specific command
    if chosen_action.split(' ')[0] == 'help':
        # display information about the specified command
        command_info(chosen_action.split(' ')[1])
        return

    # check if the chosen action is available in the current location
    if chosen_action.lower().split(' ')[0] in loc.get_available_actions():
        # perform the chosen action
        do_action(p, loc, g, chosen_action)
    else:
        # notify the player that the chosen action is not available
        print("This action is not available in this location.")


def command_info(command: str) -> None:
    """Prints information about a specific command."""
    # here's a dictionary containing information about each command
    info = {
        "go": "go [direction] -> direction can be north, south, east, or west "
              "(be mindful of your moves left)",
        "look": "look -> display long location description and reveals any "
                "npcs and items in this location.",
        "speak": "speak -> interact with NPCs for clues about the items "
                 "(hint: use \'look\' first)",
        "collect": "collect [item_name] -> collects an item "
                   "(hint: use \'look\' first and speak to npcs)",
        "inventory": "inventory -> display all items in your inventory.",
        "score": "score -> display your current score.",
        "drop": "drop [item_name] -> drops an item from your inventory that "
                "can be picked up in the same location (hint: to drop all "
                "items, type \'drop\')"
    }

    # check if the specified command is in the info dictionary
    if command in info:
        # print the information about the specified command
        print(info[command])
    else:
        # print an error message if the command does not exist
        print("Error: this command does not exist!")


def reveal_items_in_location(loca: Location) -> None:
    """Reveals all the items found in a location."""

    # call the look_for_items method to find items in the location
    items_found = loca.look_for_items()

    # if no items are found, return from the function
    if items_found is None:
        return

    # if items are found in the location
    if len(items_found) > 0:
        # print a message based on the number of items found
        if len(items_found) == 1:
            print('There is an item here. Try collecting it.')
        elif len(items_found) > 1:
            print('There are some items here. Try collecting them.')

        # print the names of all items found in the location
        print("Here are all the item(s) that you found: ")
        for i in range(0, len(items_found)):
            print(f'{i + 1}. {items_found[i].name}')

        # provide instructions on how to collect the items
        print("Type \'collect [item_name]\' to collect the item.")


###############################################################################
# the main block initializes the game environment and player,
# then enters a loop to continually prompt for and process player
# actions, update game state, and check for game over or win
# conditions, managing the flow of the game.
###############################################################################


if __name__ == "__main__":
    # import python_ta for code analysis and checking.
    import python_ta

    # run python_ta
    python_ta.check_all(config={'allowed-import-modules':
                                ["python_ta", "game_data"]})

    # start by showing the plot menu
    print(show_plot_menu())

    # then show the objectives menu
    print(show_objectives_menu())

    # prompt the player to enter their name to start the adventure
    player_name = input("Please enter your name to start the adventure: ")

    # define the menu of available actions for the player
    menu = ["go", "look", "speak", "collect",
            "inventory", "score", "drop", "quit"]

    # initialize the game world, player, and game controller objects
    with open('../../../Desktop/CSC111 - Project 1/CSC111-Project-1/map.txt') as map_file, \
            open('../../../Desktop/CSC111 - Project 1/CSC111-Project-1/locations.txt') as location_file, \
            open('../../../Desktop/CSC111 - Project 1/CSC111-Project-1/items.txt') as item_file, \
            open('../../../Desktop/CSC111 - Project 1/CSC111-Project-1/npc.txt') as npc_file:
        w = World(map_file, location_file, item_file, npc_file,
                  menu, restricted_locations=[2, 8])
        p = Player(0, 0, w.map, 50, player_name)
        g = GameController(w, p)

    # the main game loop: continue playing until the player quits/game over
    while not p.quit:
        # get the location of the player on the map
        loc = w.get_location(p.position[0], p.position[1])

        # update the accessibility of locations based on player's movements
        loc.update_access(p)

        # print player information and location description
        p.print_player_info()
        if not loc:
            continue
        else:
            loc.get_description()

        # prompt the player to choose an action
        print("What to do? (type in \'menu\' for a list of available commands "
              + "and \'help [command]\' to find how to use a command")
        c = input("\nEnter action: ")
        print()
        choose_action(c)
        print()

        # if player chose to speak, interact with NPCs
        if 'speak' in c:
            loc.talk_to_npc(p)

        # check if the game over (player quits or reaches win/lose condition)
        if p.check_game_over():
            break

        # check for win condition (all objectives completed within move limit)
        if g.check_for_win():
            print("Congratulations! You've returned all items "
                  "and reached the exam centre. \n"
                  + "You aced your test and went back feeling "
                    "accomplished. You win!")
            print(f"Game Over. You're final score is {p.get_player_score()}")
            break
