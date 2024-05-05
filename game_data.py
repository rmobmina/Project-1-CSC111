"""CSC111 Project 1: Text Adventure Game Classes

Instructions (READ THIS FIRST!)
===============================

This Python module contains the main classes for Project 1, to be imported
and used by the `adventure` module.
Please consult the project handout for instructions and details.

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
    -   For the most part, we stuck with the default 80-character line limit
    set by the default model but our doctests AND RIs needed the full 120 to
    work, and therefore the errors could not be removed.
    -   Due to the above, we ended up with over 1000 lines in this module.
    -   We also were unable to reduce the number of arguments/instance
    attributes because they were a big factor as to how we were able to
    include so many enhancements in the first place.

Thank you for your understanding!
###############################################################################
"""
from typing import Optional, TextIO, Dict
from dataclasses import dataclass


###############################################################################
# item class

# represents an item in the game world with attributes like
# name, position, code, and essential status.
# provides methods for dropping items, verifying codes, and
# checking if an item was dropped.
###############################################################################


@dataclass
class Item:
    """
    An item in our text adventure game world.

    Instance Attributes:
        - name: The name of the item.
        - start_position: The original position of the item.
        - target_position: The position where the item must be dropped off at.
        - target_points: The points awarded when the item is delivered
          to its target position.
        - _code: The secret code required to collect the item.
        - is_essential: Indicates whether the item is essential
          for completing the game.
        - _dropped: Tracks whether the item has been dropped by the player.

    Representation Invariants:
        - self.name != ''
        - 1 <= self.start_position <= 13
        - 1 <= self.target_position <= 13
        - self.target_points >= 0
        - self._code != ''
    """
    name: str
    start_position: int
    target_position: int
    target_points: int
    _code: str
    is_essential: bool
    _dropped: bool = False

    def drop(self) -> None:
        """Drop the item from the player's inventory.

        >>> item = Item('T-card', 3, 1, 5, '1244', True, False)
        >>> item.drop()
        >>> item._dropped
        True
        """
        # mark the item as dropped
        self._dropped = True

    def was_dropped(self) -> bool:
        """
        Return whether the item was already dropped.

            - True if item has been dropped.
            - False if item has not been dropped.

        >>> item = Item('Cheat Sheet', 8, 1, 5, '3124', False, False)
        >>> item.was_dropped()
        False
        >>> item.drop()
        >>> item.was_dropped()
        True
        """
        # check if the item has been dropped
        return self._dropped

    def verify_code(self, attempted_code: str) -> bool:
        """
        Verify if the code inputed by the player matches the item's secret code.

            - True if the attempted_code matches the item's secret code.
            - False if the attempted_code does not match the item's secret code.

        Preconditions:
            - attempted_code != ''

        >>> item = Item('Lucky Pen', 13, 1, 5, '1568', True, False)
        >>> item.verify_code('1234')
        False
        >>> item.verify_code('1568')
        True
        """
        # check if the provided code matches the item's code
        return self._code == attempted_code


###############################################################################
# player class

# represents the player in the game world with attributes such as
# position, inventory, score, and moves left.
# manages player actions like movement, inventory management,
# adding/removing items, and scoring.
###############################################################################


class Player:
    """
    A Player in the text advanture game.

    Instance Attributes:
        - position: The x and y-coordinate of the player's current
          location on the world map.
        - world_map: The actual world map to use as reference to
          where the player is located.
        - _inventory: The player's inventory consiting of
          all items they collected.
        - _capacity: The maximum number of items the player
          can hold in their inventory.
        - quit: A flag indicating whether the player has quit the game.
        - _score: the player's total points earned so far.
        - max_num_moves: The maximum number of moves that is
          given at the begining of the game.
        - _num_moves_left: The remaining number of unused moves
          by player while playing the game.
        - name: The name of the player.

    Representation Invariants:
        - 0 <= self.x < len(self.world_map[0])
        - 0 <= self.y < len(self.world_map)
        - self._capacity > 0
        - self._score >= 0
        - self._num_moves_left >= 0
        - self.max_num_moves > 0
    """
    position: tuple[int, int]
    world_map: list[list[int]]
    _inventory: list[Item]
    _capacity: int
    quit: bool
    score: int
    max_num_moves: int
    _num_moves_left: int
    name: str

    def __init__(self, x: int, y: int, world_map: list[list[int]],
                 max_moves: int, name: str) -> None:
        """Initializes a new Player in the game."""
        self.position = x, y
        self.world_map = world_map
        self._inventory = []
        self._capacity = 2
        self.quit = False
        self.score = 0
        self.max_num_moves = max_moves
        self._num_moves_left = self.max_num_moves
        self.name = name

    def print_player_info(self) -> None:
        """
        Prints the player's current location and moves they have left.

        >>> import io
        >>> from contextlib import redirect_stdout
        >>> player = Player(0, 0, [[0]], 20, 'Test')
        >>> player._num_moves_left = 10
        >>> buffer = io.StringIO()
        >>> with redirect_stdout(buffer):
        ...     player.print_player_info()
        >>> print(buffer.getvalue().strip())
        Player position: (0, 0)           Moves Left: (10/20)
        """
        # print the player's coordinates
        # then print remaining moves into an f-string for display
        print(f"Player position: {self.position}           "
              + f"Moves Left: ({self._num_moves_left}/{self.max_num_moves})")

    def get_player_score(self) -> int:
        """
        Returns the player's score.

        >>> player = Player(0, 0, [[0]], 10, 'Akram')
        >>> player.score = 5
        >>> player.get_player_score()
        5
        """
        # returns the value stored in the score attribute
        return self.score

    def add_score(self, amount: int) -> None:
        """
        Adds to the player's score.

        Preconditions:
            - amount > 0

        >>> player = Player(0, 0, [[0]], 10, 'Akram')
        >>> player.add_score(5)
        >>> player.score
        5
        """
        # increment the player's score by the given amount
        self.score += amount

    def calculate_final_player_score(self) -> None:
        """
        Calculates the player's final score after beating the game.

            The final score is calculated through the following:

            (score earned by npcs/locations/items) + (remaining moves)

        >>> player = Player(0, 0, [[0]], 10, 'Akram')
        >>> player.score = 20
        >>> player._num_moves_left = 5
        >>> player.calculate_final_player_score()
        >>> player.score
        25
        """
        # calculate the player's final score at the end of the game
        # by adding remaining moves to the current score.
        self.score += self.max_num_moves - self._num_moves_left

    def get_inventory(self) -> list[Item]:
        """
        Returns the player's inventory.

        >>> player = Player(0, 0, [[0]], 10, 'Reena')
        >>> item1 = Item('T-card', 3, 1, 5, '1244', True, False)
        >>> player.add_item(item1)
        >>> player.get_inventory()[0].name
        'T-card'
        """
        # returns the list stored in the _inventory attribute
        return self._inventory

    def print_inventory(self) -> None:
        """
        Prints the contents of the player's inventory.

        >>> import io
        >>> from contextlib import redirect_stdout
        >>> player = Player(0, 0, [[0]], 20, 'Test')
        >>> item = Item('Key', 1, 1, 50, '1234', True)
        >>> player.add_item(item)
        >>> buffer = io.StringIO()
        >>> with redirect_stdout(buffer):
        ...     player.print_inventory()
        >>> print(buffer.getvalue().strip())
        Item 0: Key (worth 50 points)
        """
        # if the inventory is empty, notify the player
        if not self._inventory:
            print('You have no items in here. '
                  'Try looking around and pick up what you find.')
            return
        # if there are items, list them with their point values
        for i in range(0, len(self._inventory)):
            print(f'Item {i}: {self._inventory[i].name} '
                  f'(worth {self._inventory[i].target_points} points)')

    def inventory_full(self) -> bool:
        """
        Checks if the player's inventory is full.

            - True if the number of items in the inventory
              matches the capacity.
            - False if number of items in the inventory
              does not match the capacity.

        Maximum capacity is set at 2.

        >>> player = Player(0, 0, [[0]], 10, 'Test')
        >>> player.add_item(Item('T-card', 3, 1, 5, '1244', True))
        >>> player.add_item(Item('Cheat Sheet', 8, 1, 5, '1244', True))
        >>> player.inventory_full()
        True
        >>> player.remove_item(player._inventory[0])
        >>> player.inventory_full()
        False
        """
        # check if inventory is size 2
        return len(self._inventory) == self._capacity

    def add_item(self, item: Item) -> None:
        """
        Adds an item to the player's inventory.

        >>> player = Player(0, 0, [[0]], 10, 'Reena')
        >>> tcard = Item('T-card', 3, 1, 5, '1244', True)
        >>> player.add_item(tcard)
        >>> player._inventory[0].name
        'T-card'
        """
        # adds the item to the inventory list
        self._inventory.append(item)

    def remove_item(self, item: Item) -> None:
        """
        Removes an item from the player's inventory.

        Preconditions:
            - item in self._inventory

        >>> player = Player(0, 0, [[0]], 10, 'Akram')
        >>> pen = Item('Lucky Pen', 13, 1, 5, '1568', True)
        >>> player.add_item(pen)
        >>> player.remove_item(pen)
        >>> player._inventory
        []
        """
        # removes the item from the inventory list
        self._inventory.remove(item)

    def find_item_by_name(self, item_name: str) -> Optional[Item]:
        """
        Returns the item with the given name from the player's inventory.

            - None if item does not exist.
            - Item name as a string if it exists.

        Preconditions:
            - item_name != ''

        >>> player = Player(0, 0, [[0]], 10, 'Reena')
        >>> pen = Item('Lucky Pen', 13, 1, 5, '1568', True)
        >>> player.add_item(pen)
        >>> player.find_item_by_name('Lucky Pen').name
        'Lucky Pen'
        >>> print(player.find_item_by_name('T-card'))
        None
        """
        # search for an item by name in the player's inventory
        for item in self._inventory:
            if item.name.lower().strip() == item_name.strip().lower():
                # return it if found
                return item
        # return None if no item is found
        return None

    def is_location_valid(self, x: int, y: int) -> bool:
        """
        Returns whether the location at the given (x, y) coordinate
        is valid within the world map bounds.

            - True if within bounds and location is valid.
            - False if outside bounds and location invalid.

        >>> player = Player(0, 0, [[0, -1], [1, 1]], 10, 'Reena')
        >>> player.is_location_valid(1, 0)
        False
        >>> player.is_location_valid(0, 1)
        True
        >>> player.is_location_valid(2, 0)
        False
        """
        # check if x and y are within the bounds of the world_map dimensions
        if not (0 <= x < len(self.world_map[0])
                and 0 <= y < len(self.world_map)):
            return False
        else:
            # if inside bounds, check if the location is accessible
            return self.world_map[y][x] != -1

    def move(self, direction: str) -> None:
        """
        Move the player in the given direction if possible.

        >>> player = Player(0, 0, [[0, 0], [0, 0]], 10, 'Akram')
        >>> player.move('east')
        >>> player.position
        (1, 0)
        >>> player.move('south')
        >>> player.position
        (1, 1)
        >>> player.move('west')
        >>> player.position
        (0, 1)
        >>> player.move('north')
        >>> player.position
        (0, 0)
        >>> player.move('up')
        Invalid Command: please choose (north, south, east, west)
        """
        # initialize new position variables based on current position
        new_y_pos = self.position[1]
        new_x_pos = self.position[0]

        # convert the direction to lowercase, adjust the position accordingly
        direction = direction.lower()

        # move up in the map (decrease y coordinate)
        if direction == "north":
            new_y_pos -= 1
        # move down in the map (increase y coordinate)
        elif direction == "south":
            new_y_pos += 1
        # move right in the map (increase x coordinate)
        elif direction == "east":
            new_x_pos += 1
        # move left in the map (decrease x coordinate)
        elif direction == "west":
            new_x_pos -= 1
        else:
            # if direction is invalid, print an error message and exit
            print('Invalid Command: please choose (north, south, east, west)')
            return

        # decrement the number of moves left after deciding to move
        self._num_moves_left -= 1

        # check if the new position is valid before moving the player
        if not self.is_location_valid(new_x_pos, new_y_pos):
            # if the new position is invalid, print a warning message
            print('Whoops! No exit here. Better turn back.')
        else:
            # if the new position is valid, update the player's position
            self.position = new_x_pos, new_y_pos

    def check_game_over(self) -> bool:
        """
        Checks if the game should end due to running out of moves.

        >>> player = Player(0, 0, [[0]], 5, 'Reena')
        >>> player._num_moves_left = 1
        >>> player.check_game_over()
        False
        >>> player._num_moves_left = 0
        >>> player.check_game_over()
        Oh no... You ran out of moves! You could not make it to your test and failed. Game over!
        True
        """
        # check if the player has no moves left
        if self._num_moves_left <= 0:
            print('Oh no... You ran out of moves! '
                  'You could not make it to your test and failed. Game over!')
            # return True to indicate the game is over
            return True
        # return False if player still has moves left, game can continue
        return False


###############################################################################
# location class

# represents a location in the game world with attributes like
# map dimensions, score, and available actions/items.
# manages player interaction with locations, including looking
# around, talking to NPCs, and updating access.
###############################################################################


class Location:
    """
    A location in our text adventure game world.

    Instance Attributes:
        - map_dim: The width and length of the world map
          that contains this location.
        - map_id: The id of this location in the world map.
        - score: The number of points awarded for visiting this location.
        - _description_short: A brief description of the location
          after visiting the first time.
        - _description_long: A detailed description of the
          location when first visiting.
        - player_visited: Whether the player already visited
          this location before.
        - _available_items: List of items available in this location.
        - _available_actions: List of all the available commands
          when at this location.
        - _npc_dialogue: The dialogue spoken by the non-player
          character (NPC) at this location.
        - has_npc: A flag indicating whether this location has an NPC.
        - looked: A flag indicating whether the player has
          looked around this location.
        - has_npc_spoken: A flag indicating whether the player
          has spoken to the non-player character (NPC) at this location.

    Representation Invariants:
        - self.map_dim[0] > 0 and self.map_dim[1] > 0
        - 0 <= position[0] < self.map_dim[0]
          and 0 <= position[1] < self.map_dim[1]
        - self._description_short != '' and self._description_short != ''
        - all({item is not None for item in self._available_items})
        - self.score >= 0
    """
    map_dim: tuple[int, int]
    map_id: int
    score: int
    _description_short: str
    _description_long: str
    player_visited: bool
    _available_items: list[Optional[Item]]
    _available_actions: list[str]
    _npc_dialogue: str
    has_npc: bool = False
    looked: bool = False
    has_npc_spoken: bool = False

    def __init__(self, map_dim: tuple[int, int], map_id: int, score: int,
                 description_short: str, description_long: str,
                 actions: list[str], npc_dialogue: str = "") -> None:
        """Initialize a new location in the game."""
        self.map_dim = map_dim
        self.map_id = map_id
        self.score = score
        self._description_short = description_short
        self._description_long = description_long
        self.player_visited = False
        self._available_items = []
        self._available_actions = []
        self.set_npc_dialogue(npc_dialogue)
        self.update_available_actions(actions)
        self.looked = False
        self.has_npc_spoken = False

    def set_npc_dialogue(self, dialogue: str) -> None:
        """
        Set the dialogue spoken by the NPC at this location.

        >>> loc = Location((10, 10), 1, 5, "short", "long", ["look"])
        >>> loc.set_npc_dialogue("Hello, adventurer!")
        >>> loc._npc_dialogue
        'Hello, adventurer!'
        """
        # assign dialogue to NPC
        self._npc_dialogue = dialogue
        # indicate an NPC is present if dialogue is not empty
        if self._npc_dialogue != "":
            self.has_npc = True

    def talk_to_npc(self, player: Player) -> None:
        """
        Print the NPC dialogue.

        >>> loc = Location((10, 10), 1, 5, "short", "long", ["look"])
        >>> loc.set_npc_dialogue("5 Greetings, {name}!")
        >>> player1 = Player(0, 0, [[0]], 10, 'Akram')
        >>> loc.talk_to_npc(player1)
        Greetings, Akram!
        """
        # check if there is an NPC and they haven't spoken yet
        if self.has_npc and not self.has_npc_spoken:
            # print the NPC's dialogue,
            # using the player's name in the f-string string
            print(self._npc_dialogue[2:].format(name=player.name))
            # mark that the NPC has now spoken to prevent repeating the dialogue
            self.has_npc_spoken = True

    def get_npc_score(self) -> int:
        """
        Return the number of points earned for talking to the NPC.

        >>> loc = Location((10, 10), 1, 5, "short", "long", ["look"])
        >>> loc.set_npc_dialogue("5 Hello, adventurer!")
        >>> loc.get_npc_score()
        5
        """
        # return points earned from NPC interaction
        if self.has_npc:
            return int(self._npc_dialogue.strip()[0])
        return 0

    def look_for_items(self) -> list[Item]:
        """
        Return a list of items found in this location.

        >>> loc = Location((10, 10), 1, 5, "short", "long", ["look"])
        >>> loc.look_for_items()
        There seem to be no items in this location
        []
        >>> item = Item('Lucky Pen', 13, 1, 5, '1568', True)
        >>> loc.add_item(item)
        >>> item in loc.look_for_items()
        True
        """
        # if there are no items at this location
        # print a message saying there is nothing
        if len(self._available_items) == 0:
            print('There seem to be no items in this location')
            return []
        # if there are items at this lcoation
        # mention what those item(s) are
        else:
            return self._available_items

    def look_around(self) -> None:
        """
        Allow the player to look around the location.

        >>> loc = Location((10, 10), 1, 5, "short", "This is a test", ["look"])
        >>> loc.look_around()
        --------------------------------------------------
        This is a test
        --------------------------------------------------
        <BLANKLINE>
        """
        # provide a detailed description of the location,
        # enabling item and NPC discovery
        # baseline requirement
        self.looked = True
        print("--------------------------------------------------")
        print(self._description_long)
        print("--------------------------------------------------\n")

    def get_description(self) -> None:
        """
        Print the appropriate description when the player is in this location.

            - A detailed description will be printed on the first visit.
            - A brief description will be printed on subsequent visits.

        >>> loc = Location((10, 10), 1, 5, "short", "long", ["look"])
        >>> loc.get_description()
        --------------------------------------------------
        LOCATION 1
        long
        --------------------------------------------------
        <BLANKLINE>
        >>> loc.get_description()
        --------------------------------------------------
        LOCATION 1
        short
        --------------------------------------------------
        <BLANKLINE>
        """
        print("--------------------------------------------------")
        # Add this line to print "LOCATION #", baseline requirement
        print(f"LOCATION {self.map_id}")
        if self.player_visited:
            print(self._description_short)
        else:
            print(self._description_long)
            self.player_visited = True
        print("--------------------------------------------------\n")

    def update_available_actions(self, actions: list[str]) -> None:
        """
        Update the available actions in this location.
        This is based on NPCs, items, etc.

        >>> loc = Location((10, 10), 1, 5, "short", "long", [])
        >>> loc.get_available_actions()
        []
        >>> loc.update_available_actions(['look', 'talk'])
        >>> loc.get_available_actions()
        ['look', 'talk']
        """
        self._available_actions = actions

    def get_available_actions(self) -> list[str]:
        """
        Return the available actions in this location.

            - The actions depend on the items available in the location.
              and the x,y position of this location on the world map.

        >>> loc = Location((10, 10), 1, 5, "short", "long", ["look", "talk"])
        >>> loc.get_available_actions()
        ['look', 'talk']
        """
        return self._available_actions

    def update_access(self, player: Player) -> None:
        """
        Update the player's access to this location.

            - Checks if the player visited this location and
              rewards them with some points.
            - These points add to their total score and cannot
              be regained after visiting the first time.

        >>> player1 = Player(0, 0, [[0]], 10, 'Reena')
        >>> loc = Location((10, 10), 1, 5, "short", "long", ["look"])
        >>> loc.update_access(player1)
        >>> player1.get_player_score()
        5
        >>> loc.player_visited = False
        >>> loc.update_access(player1)
        >>> loc.player_visited = True
        >>> loc.update_access(player1)
        >>> player1.get_player_score()
        10
        """
        # grant points for first-time location visitation
        if not self.player_visited:
            player.add_score(self.score)

    def add_item(self, item: Item) -> None:
        """
        Add an item to the available items.

        >>> loc = Location((10, 10), 1, 5, "short", "long", ["look"])
        >>> item1 = Item('Lucky Pen', 13, 1, 5, '1568', True)
        >>> loc.add_item(item1)
        >>> item1 in loc._available_items
        True

        """
        self._available_items.append(item)

    def remove_item(self, item: Item) -> None:
        """
        Remove an item from the available items.

        >>> loc = Location((10, 10), 1, 5, "short", "long", ["look"])
        >>> item1 = Item('T-card', 3, 1, 5, '1244', True)
        >>> loc.add_item(item1)
        >>> loc.remove_item(item1)
        >>> loc.look_for_items()
        There seem to be no items in this location
        []
        """
        self._available_items.remove(item)

    def find_item_by_name(self, item_name: str) -> Optional[Item]:
        """
        Find an item by its name.

        >>> loc = Location((10, 10), 1, 5, "short", "long", ["look"])
        >>> item1 = Item('Cheat Sheet', 8, 1, 5, '1244', True)
        >>> loc.add_item(item1)
        >>> loc.find_item_by_name('Cheat Sheet') == item1
        True
        >>> loc.find_item_by_name('Nonexistent Item') is None
        True
        """
        # normalize the input item name to enable case-insensitive
        # case-insensitivity is a baseline requirement
        normalized_name = item_name.strip().lower()

        # iterate over each item in the location's list of available items
        for item in self._available_items:
            # compare the normalized names to check for a match
            if item.name.lower().strip() == normalized_name:
                # if a match is found, return the corresponding Item object
                return item
        # if no match, return None to indicate no item was found
        return None


###############################################################################
# restricted location class

# inherits from Location and represents a location with
# restrictions or required items.
# manages access to the location based on the presence of required
# items and updates available actions accordingly.
###############################################################################


class RestrictedLocation(Location):
    """
    A subclass of Location for locations that have certain
    restrictions or items needed to access.

    This is our use of inheritance as required by the project.

    Instance Attributes:
        - _unavailable_actions: List of actions that are unavailable.
        - required_item: The item required to access this location.
        - _is_locked: A flag indicating whether the location is locked.

    Representation Invarients:
        - self.required_item is not None
    """
    _unavailable_actions: list[str]
    required_item: Item
    _is_locked: bool = True

    def __init__(self, map_dim: tuple[int, int], map_id: int, score: int,
                 description_short: str, description_long: str,
                 actions: list[str], required_item: Item,
                 npc_dialogue: str = "") -> None:
        """Initialize Restricted Locations in the game."""
        self._unavailable_actions = ["look", "speak", "collect"]
        self.required_item = required_item
        super().__init__(map_dim, map_id, score, description_short,
                         description_long, actions, npc_dialogue)

    def get_description(self) -> None:
        """Print the description of the location, indicating if it's locked."""
        # check if the location is locked
        # if so, print a message indicating the required item for access
        if self._is_locked:
            print(f"Access Denied: "
                  f"This location needs a {self.required_item.name} to enter.")
        # if the location is not locked
        # use the parent class's method to print the location description.
        else:
            super().get_description()

    def update_available_actions(self, actions: list[str]) -> None:
        """
        Update available actions at the location
        based on its locked status.
        """
        # filter out unavailable actions if the location is locked
        self._available_actions = [action for action in actions if
                                   action not in self._unavailable_actions]

    def get_available_actions(self) -> list[str]:
        """
        Return the available actions at the location,
        considering its locked status.
        """
        # include unavailable actions if the location is unlocked
        if not self._is_locked:
            return self._available_actions + self._unavailable_actions
        else:
            return self._available_actions

    def update_access(self, player: Player) -> None:
        """
        Update the locked status of the location
        based on player's inventory.
        """
        # update the locked status
        # based on the presence of the required item in player inventory
        self._is_locked = self.required_item not in player.get_inventory()


def load_map(map_data: TextIO) -> list[list[int]]:
    """
    Store map from open file map_data as the map attribute of
    this object, as a nested list of integers like so:

    If map_data is a file containing the following text:
        1 2 5
        3 -1 4
    then load_map should assign this World object's map to be
    [[1, 2, 5], [3, -1, 4]].

    Return this list representation of the map.
    """
    # reads each line of the input file
    # splits it by spaces to separate the integers
    # converts each string to an integer
    # constructs a list of these integers for each line
    return [[int(num) for num in line.split()] for line in map_data]


###############################################################################
# world class

# represents the game world with attributes for the map,
# locations, items, and NPCs.
# manages loading map data, items, locations, and NPCs, as well
# as adding items to locations.
###############################################################################


class World:
    """
    A text adventure game world storing all location, item and map data.

    Instance Attributes:
        - map: a nested list representation of this world's map.
        - items: A list of Item objects in the game.
        - _restricted_locations: A list of location ids for locations
          that have restricted access.
        - _locations: A dictionary mapping location numbers to Location objects.
        - _npcs: A dictionary mapping location numbers to location objects.

    Representation Invariants:
        - all(len(row) == len(self.map[0]) for row in self.map)
        - len(self.map) > 0
        - all(location_number in self._locations for row in self.map for \
              location_number in row if location_number != -1)
        - all(item.start_position in self._locations and item.target_position in self._locations for item in self.items)
    """
    map: list[list[int]]
    items: dict[int, Item]
    _restricted_locations: list[int]
    _locations: dict[int, Location]
    _npcs: dict[int, str]

    def __init__(self, map_data: TextIO, locations_data: TextIO,
                 items_data: TextIO, npc_data: TextIO,
                 menu_actions: list[str],
                 restricted_locations: list[int]) -> None:
        """
        Initialize a new World for a text adventure game,
        based on the data in the given open files.

        - map_data: name of a text file containing map data.
        - location_data: name of text file containing location data.
        - items_data: name of text file containing item data.
        - npc_data: name of the text file containing npc data.
        """
        self.map = load_map(map_data)
        self.items = self.load_items(items_data)
        self._restricted_locations = restricted_locations
        self._locations = self.load_locations(locations_data, menu_actions)
        self.load_npcs(npc_data)
        self.add_location_items()

    def get_locations_id(self) -> list[int]:
        """
        Return a list of all location IDs.

        >>> w = World(open('map.txt'), open('locations.txt'), open('items.txt'), open('npc.txt'), [], [])
        >>> w.get_locations_id()
        [1, 2, -1, -1, -1, 3, -1, 4, -1, -1, 5, 6, 7, 8, -1, 9, -1, -1, 10, 11, 12, 13, -1, -1, -1]
        """
        location_ids = []
        # iterate through each row in the map
        # to extract all unique location IDs
        for row in self.map:
            location_ids.extend(row)
        return location_ids

    def get_location(self, x: int, y: int) -> Optional[Location]:
        """
        Return Location object associated with the coordinates (x, y)
        in the world map, if a valid location exists at that position.
        Otherwise, return None. (Remember, locations represented by
        the number -1 on the map should return None.)

        >>> w = World(open('map.txt'), open('locations.txt'), open('items.txt'), open('npc.txt'), [], [])
        >>> location = w.get_location(1, 2)
        >>> location.map_id
        6
        >>> empty_location = w.get_location(3, 1)
        >>> empty_location is None
        True
        """
        # check if the given coordinates are within the bounds of the map
        if 0 <= y < len(self.map) and 0 <= x < len(self.map[0]):
            # fetch the location ID at the given coordinates
            location_number = self.map[y][x]
            # return the Location object if the ID is valid
            if location_number != -1:
                return self._locations.get(location_number)
        # return None if the location is invalid
        # or the coordinates are out of bounds.
        return None

    def exists_in_map(self, location: Location) -> bool:
        """ Determines whether a location exists in this world map.

        >>> w = World(open('map.txt'), open('locations.txt'), open('items.txt'), open('npc.txt'), [], [])
        >>> valid_location = w.get_location(0, 0)
        >>> invalid_location = Location((1, 2), 21, 3000, 'idk', 'i  d  k', [])
        >>> w.exists_in_map(valid_location)
        True
        >>> w.exists_in_map(invalid_location)
        False
        """
        if location is None:
            return False
        if location.map_id in self._locations:
            return self._locations[location.map_id] == location
        return False

    def add_location_items(self) -> None:
        """
        Updates the locations based on where items are located.

        >>> w = World(open('map.txt'), open('locations.txt'), open('items.txt'), open('npc.txt'), [], [])
        >>> w.add_location_items()
        >>> location = w._locations[3]
        >>> location.look_for_items() != []
        True
        """
        # iterate over each item in the game
        for item_num in self.items:
            # if the item's location ID matches a valid location
            # add the item to that location
            if item_num in self.get_locations_id():
                self._locations[item_num].add_item(self.items[item_num])

    def load_items(self, items_data: TextIO) -> dict[int, Item]:
        """
        Load and return the items as a list of dictionaries
        representing Item objects. Each dictionary contains the
        item's name and its properties.

        If items_data is a file containing the following text:
            3 1 5 T-card
            8 1 5 Cheat Sheet
            13 1 5 Lucky Pen
        then load_items should assign this World items to be

        {3: Item("T-card", 1, 3, 5, '1244', True),
         8: Item("Cheat Sheet", 1, 8, 5, '3124', True),
         13: Item("Lucky Pen", 1, 13, 5, '1568', True)}

        Return this list representation of the items.

        >>> w = World(open('map.txt'), open('locations.txt'), open('items.txt'), open('npc.txt'), [], [])
        >>> w.items != []
        True
        >>> w.items[3].name == "T-card" and w.items[8].name == "Cheat Sheet" and w.items[13].name == "Lucky Pen"
        True
        """
        items = {}
        # read each line from the items data file
        for line in items_data:
            # split the line into components representing item attributes
            parts = line.strip().split()
            # ensure the line has the correct number
            # of parts to represent an item
            if len(parts) < 5:
                continue
            # extract item attributes and create an Item object
            start = int(parts[0])
            target = int(parts[1])
            points = int(parts[2])
            code = parts[-1]
            item_name = " ".join(parts[3:-1])
            items[start] = Item(item_name, start, target, points, code, True)
        return items

    def load_locations(self, location_data: TextIO,
                       lst_of_actions: list[str]) -> Dict[int, Location]:
        """
        Load location data from the given file and return a
        dictionary mapping location numbers to Location objects.

        Each location entry in the file should be in the following format:

        LOCATION <number>
        <score_value>
        <detailed_description>

        <brief_description>
        END

        >>> w = World(open('map.txt'), open('locations.txt'), open('items.txt'), open('npc.txt'), [], [2])
        >>> w._locations != []
        True
        >>> location = w._locations[2]
        >>> location is not None
        True
        >>> location.get_description()
        Access Denied: This location needs a T-card to enter.
        """
        locations = {}
        loc_number = -1
        loc_score = 0
        descriptions = ''

        # process each line from the location data file
        for line in location_data:
            if 'LOCATION' in line:
                # new location entry begins,
                # reset description and parse location number
                descriptions = ''
                loc_number = int(line.strip()[line.index(' ') + 1:])
            elif line.strip().isdigit():
                # line contains the score for the location
                loc_score = int(line)
            elif line == '\n':
                # line break encountered
                # add it to the description for formatting.
                descriptions += line
            elif 'END' not in line:
                # line is part of the location's description
                # add it to the descriptions string.
                descriptions += line.strip()
            else:
                # 'END' indicates the end of a location's entry
                # process the accumulated data
                descriptions_lst = descriptions.split('\n')
                map_dim = (len(self.map[0]), len(self.map))
                # check if the current location is restricted
                # and create the appropriate location object.
                if loc_number in self._restricted_locations:
                    locations[loc_number] = (
                        RestrictedLocation(map_dim, loc_number, loc_score,
                                           descriptions_lst[1],
                                           descriptions_lst[0],
                                           lst_of_actions, self.items[3]))
                else:
                    locations[loc_number] = (
                        Location(map_dim, loc_number, loc_score,
                                 descriptions_lst[1], descriptions_lst[0],
                                 lst_of_actions))
        # return the dictionary of locations
        return locations

    def _set_npc_dialogue(self, loc_id: int, dialogue_lines: list[str]) -> None:
        """
        Set the NPC dialogue for the specified location,
        if the location exists.

        >>> w = World(open('map.txt'), open('locations.txt'), open('items.txt'), open('npc.txt'), [], [])
        >>> w._locations[4] != '' and w._locations[5] != '' and w._locations[10] != ''
        True
        """
        if loc_id is not None and dialogue_lines and loc_id in self._locations:
            self._locations[loc_id].set_npc_dialogue(" ".join(dialogue_lines))

    def load_npcs(self, npc_data: TextIO) -> None:
        """
        Load NPCs from the given file and update their
        dialogues in their respective locations.

        Each npc entry in the file should be in the following format:

        LOCATION <number>
        <score_value>
        <dialogue>
        END

        >>> w = World(open('map.txt'), open('locations.txt'), open('items.txt'), open('npc.txt'), [], [])
        >>> w._locations[4].has_npc and w._locations[5].has_npc and w._locations[10].has_npc
        True
        """
        loc_id = None
        dialogue_lines = []

        # process each line from the NPC data file
        for line in npc_data:
            line = line.strip()
            if line.startswith("LOCATION"):
                # new NPC entry begins
                # apply accumulated dialogue to the previous NPC if any
                self._set_npc_dialogue(loc_id, dialogue_lines)
                loc_id = int(line.split()[1])
                dialogue_lines = []
            elif line == "END":
                # 'END' indicates the end of an NPC's dialogue
                # apply it to the current NPC
                self._set_npc_dialogue(loc_id, dialogue_lines)
                loc_id = None
                dialogue_lines = []
            else:
                # line is part of the NPC's dialogue
                # add it to the dialogue_lines list
                dialogue_lines.append(line)
        # apply dialogue to the last NPC in the file
        # if 'END' was not explicitly stated
        self._set_npc_dialogue(loc_id, dialogue_lines)


###############################################################################
# game controller class

# controls the game logic by interacting with the world and player.
# manages actions like collecting/dropping items, checking win conditions,
# and ensuring essential items are in the right place.
###############################################################################


class GameController:
    """
    Manages the game's logic and interactions between the player,
    world, and essential game items.

    Instance Attributes:
        - world: The game world containing all locations, items, and NPCs.
        - player: The player object representing the user in the game.
        - essential_items: The items required to win the game.

    Representation Invariants:
        - len(self.essential_items) > 0
    """
    world: World
    player: Player
    essential_items: list[Item]

    def __init__(self, world: World, player: Player) -> None:
        """Initialize a new GameController with the given world and player."""
        self.world = world
        self.player = player
        self.essential_items = self.get_essential_items(self.world.items)

    def get_essential_items(self, items: dict[int, Item]) -> list[Item]:
        """
        Return a list of essential items from the
        given dictionary of items.

        >>> w = World(open('map.txt'), open('locations.txt'), open('items.txt'), open('npc.txt'), [], [])
        >>> p = Player(0, 0, w.map, 50, "")
        >>> gc = GameController(w, p)
        >>> gc.essential_items != []
        True
        >>> gc.essential_items[0].name == "T-card"
        True
        """
        # initializes an empty list for essential items
        lst_of_items = []
        # iterates over all items in the game
        for item_id in items:
            lst_of_items.append(items[item_id])
        # returns the compiled list of essential items
        return lst_of_items

    def collect_item(self, item_name: str, location: Location, code_needed: bool = True) -> bool:
        """
        Collect an item from the given location.

        >>> w = World(open('map.txt'), open('locations.txt'), open('items.txt'), open('npc.txt'), [], [])
        >>> p = Player(0, 0, w.map, 50, "")
        >>> gc = GameController(w, p)
        >>> gc.collect_item("T-card", w.get_location(0, 1), False)
        Collected T-card.
        True
        """
        # searches for the item in the current location
        item = location.find_item_by_name(item_name)
        if item:
            # prompts the player to enter the item's collection code
            player_code = ''
            if code_needed:
                player_code = \
                    (input("Enter the 4-digit code to collect this item: ").strip())
            if item.verify_code(player_code) or not code_needed:
                # verifies the entered code against the item's code
                # first checks if the player's inventory has space
                # then adds the item to the player's inventory
                if not self.player.inventory_full():
                    self.player.add_item(item)
                    location.remove_item(item)
                    print(f"Collected {item.name}.")
                    return True
                else:
                    print("Not enough space in inventory.")
            else:
                print("Incorrect code. Could not collect the item.")
        else:
            print("Item not found.")
        return False

    def drop_item(self, item: Item, location: Location) -> bool:
        """
        Drop an item at the given location.

        Preconditions:
            - item is not None
            - location.map_id in self.world.get_location_ids

        >>> w = World(open('map.txt'), open('locations.txt'), open('items.txt'), open('npc.txt'), [], [])
        >>> p = Player(0, 0, w.map, 50, "")
        >>> gc = GameController(w, p)
        >>> gc.collect_item("T-card", w.get_location(0, 1), False)
        Collected T-card.
        True
        >>> gc.drop_item(p.get_inventory()[0], w.get_location(0, 0))
        Dropped T-card.
        True
        >>> p.get_player_score()
        100
        """
        # checks if the item is in the player's inventory
        if item in self.player.get_inventory():
            # removes the item from the inventory
            self.player.remove_item(item)
            # adds the item back to the current location
            location.add_item(item)
            # awards points to the player
            # if essential items are dropped at the specified location.
            if (location.map_id == 1 and item in
                    self.essential_items and not item.was_dropped()):
                self.player.add_score(item.target_points)
            print(f"Dropped {item.name}.")
            # marks the item as dropped
            item.drop()
            return True
        print("Item not found in inventory.")
        return False

    def drop_item_name(self, item_name: str, location: Location) -> bool:
        """
        Drop an item with the given name at the given location.

        Preconditions:
            - location.map_id in self.world.get_location_ids
            - item_name != ""

        >>> w = World(open('map.txt'), open('locations.txt'), open('items.txt'), open('npc.txt'), [], [])
        >>> p = Player(0, 0, w.map, 50, "")
        >>> gc = GameController(w, p)
        >>> gc.collect_item("T-card", w.get_location(0, 1), False)
        Collected T-card.
        True
        >>> gc.drop_item_name("T-card", w.get_location(0, 0))
        Dropped T-card.
        True
        """
        # finds the item by name in the player's inventory
        item = self.player.find_item_by_name(item_name)
        # drops the found item at the current location
        return self.drop_item(item, location)

    def all_essentials_dropped(self) -> bool:
        """
        Check if all essential items are dropped at
        location 1 (0, 0), The Dorm Room.

        >>> w = World(open('map.txt'), open('locations.txt'), open('items.txt'), open('npc.txt'), [], [])
        >>> p = Player(0, 0, w.map, 50, "")
        >>> gc = GameController(w, p)
        >>> start_location = w.get_location(0, 0)
        >>> for item1 in gc.essential_items: \
                start_location.add_item(item1)
        >>> gc.all_essentials_dropped()
        True
        """
        # set the designated location for dropping items.
        location_00 = self.world.get_location(0, 0)

        if location_00 is None:
            return False

        # iterates over all essential items
        for item in self.essential_items:
            # checks if each essential item is dropped
            if not location_00.find_item_by_name(item.name):
                return False
        return True

    def check_for_win(self) -> bool:
        """
        Check if the player has won the game.

        >>> w = World(open('map.txt'), open('locations.txt'), open('items.txt'), open('npc.txt'), [], [])
        >>> p = Player(0, 0, w.map, 50, "")
        >>> gc = GameController(w, p)
        >>> start_location = w.get_location(0, 0)
        >>> for item in gc.essential_items: \
                start_location.add_item(item)
        >>> p.position = (4, 3)
        >>> gc.check_for_win()
        True
        """
        # the coordinates of the win location
        target_x, target_y = 4, 3

        # checks if the player is at the win location
        # and all essential items are dropped
        if self.player.position == (target_x, target_y) and self.all_essentials_dropped():
            self.player.calculate_final_player_score()
            return True
        return False


###############################################################################
# the main block
###############################################################################


if __name__ == '__main__':
    # import python_ta for code analysis and checking.
    import python_ta

    # run python_ta
    python_ta.check_all()

    # import doctest to automatically test doctests.
    import doctest

    # run the doctest
    doctest.testmod(verbose=True)
