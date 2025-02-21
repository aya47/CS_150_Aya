"""
Core class definitions for Cats vs. Homework
Last edited by Geisler 2024
"""

import pathlib
import tkinter as tk
import random

# The overall sizes of the game window, kept as a constant
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600

# The height of the board within the game window
BOARD_HEIGHT = 450

# The size of a single tile "button"
TILE_WIDTH = 100
TILE_HEIGHT = 100

# The amount of width allocated for information (end turn/batteries)\
INFO_WIDTH = 200

# The number of tiles in a "lane"
LANE_WIDTH = 7

# A list of all images by name
ACTOR_IMAGE_NAMES = [
    'calico',
    'charger',
    'empty',
    'kitten',
    'laser',
    'snacks',
    'tabby',
    'thrower',
]

# starting batteries
STARTING_BATTERIES = 8

# How many rounds until the game ends
WIN_ROUND = 40

# --------------------------------
# A bunch of background classes that manage the game logic
# You shouldn't need to work with these directly


class GameManager:
    """
    Manages the game state and holds constant image references
    """

    _instance = None
    """
    There is exactly one instance of GameManager that is globally accessible
    We use the Singleton design pattern to enforce this
    """

    _root = None
    """
    The root of the drawn game window
    """

    _board = None
    """
    The frame and container for the game board
    """

    _selection_manager = None
    """
    The frame and container for the contraption selector
    """

    _actor_images = None
    """
    The dictionary of all images used for constructing units (public)
    We use the name of the image as an access to avoid reloading images
    """

    _batteries = None
    """
    The number of batteries the player has
    """

    _rounds = 0
    """
    How many rounds have passed
    """

    _contraptions = None
    """
    A list of all the contraptions currently on the board
    """

    _cats = None
    """
    A list of all the cats in the game
    """

    _game_ended = None
    """
    Whether or not the game has ended
    """

    def initialize(lanes,
                   contraptions,
                   cats):
        """
        Sets up the (unique) GameManager with a window at the root
        Constructs a game board with the number of given 'lanes',
          the provided list of contraptions that can be build
          and the provided list of initialized cats
        """
        # Checks on the provided parameters
        assert isinstance(lanes, int)
        assert isinstance(contraptions, list)
        assert isinstance(cats, list)

        # Assert we haven't yet been initialized and then initialize
        assert not GameManager.is_initialized()
        singleton = GameManager()
        GameManager._instance = singleton

        # Setup the root of the window
        root = tk.Tk()
        root.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')
        root.resizable(width=False, height=False)
        singleton._root = root

        # Read images into the dictionary
        actor_images = {}
        for image_name in ACTOR_IMAGE_NAMES:
            path = pathlib.Path('resources') / \
                pathlib.Path(f'{image_name}.png')
            actor_images[image_name] = tk.PhotoImage(file=path)
        singleton._actor_images = actor_images

        singleton._batteries = STARTING_BATTERIES
        singleton._rounds = 0

        # construct the selection manager
        singleton._selection_manager = SelectionManager(
            contraptions, singleton.batteries())

        # construct a board
        singleton._board = Board(lanes)

        # keep track of all the contraptions on the board
        # this list needs to be updated when a contraption is removed
        singleton._contraptions = []

        # initialize all of the cats
        singleton._cats = []
        for cat in cats:
            singleton._cats.append(cat())
        singleton.update_attentions()

        singleton._game_ended = False

    def is_initialized():
        """
        Returns true if a singleton instance of GameManager has been initialized
        """
        return GameManager._instance is not None

    def manager():
        """
        Gets the unique GameManager
        Re  quires that such a GameManager exist
        """
        assert GameManager.is_initialized()
        return GameManager._instance

    def destroy():
        """
        Destroys the singleton instance of GameManager
        Requires that such an instance exist
        """
        assert GameManager.is_initialized()
        GameManager._instance._root.destroy()
        GameManager._instance._game_ended = True
        GameManager._instance = None

    def root(self):
        """
        Returns a reference to the root tkinter container
        """
        return self._root

    def selection_manager(self):
        """
        Returns a reference to the selection manager used by this game
        """
        return self._selection_manager

    def board(self):
        """
        Returns a reference to the board used by this game
        """
        return self._board

    def get_empty_image(self):
        """
        Returns the empty tile image
        """
        return self.get_actor_image('empty')

    def get_actor_image(self, image_name):
        """
        Returns the image associated with the given string name
        Requires that the provided image_name be in our list of IMAGE_NAMES
        """
        assert isinstance(image_name, str)
        assert image_name in ACTOR_IMAGE_NAMES
        return self._actor_images[image_name]

    def batteries(self):
        """
        Returns the number of batteries we currently have
        """
        return self._batteries

    def spend_batteries(self, amount):
        """
        Removes the non-negative 'amount' of batteries from this game
        Requires that we have at least as many batteries as 'amount'
        """
        assert amount >= 0 and self._batteries >= amount
        self._batteries -= amount
        self._selection_manager.update_battery_text(self._batteries)

    def add_contraption(self, contraption):
        """
        Adds the given contraption to the list of contraptions on the board
        """
        assert isinstance(contraption, Contraption)
        self._contraptions.append(contraption)

    def remove_contraption(self, contraption):
        """
        Removes the given contraption (by ID) from the board
        If no such contraption exists, this function will error
        """
        assert isinstance(contraption, Contraption)
        self._contraptions.remove(contraption)

    def increment_round(self):
        """
        Increases the number of rounds by one
        If we've reached WIN_ROUNDS, end the game in a win
        """
        self._rounds += 1
        self._selection_manager.update_round_text(self._rounds)
        if self._rounds >= WIN_ROUND:
            self.win_game()

    def add_batteries(self, amount):
        """
        Adds the non-negative 'amount' of batteries to this game
        """
        assert amount >= 0
        self._batteries += amount
        self._selection_manager.update_battery_text(self._batteries)

    def update_attentions(self):
        """
        Updates the attention display of all cats
        """
        attentions = [cat.attention() for cat in self._cats]
        self._selection_manager.update_attention_text(attentions)

    def end_round(self):
        """
        Ends the current player turn and takes cat/contraption actions
        """
        self.add_batteries(1)
        for contraption in self._contraptions:
            contraption.end_round()
        for cat in self._cats:
            cat.end_round()
            # if the game ended when this cat moved
            if (self._game_ended):
                return
        self.update_attentions()
        self.increment_round() # may end the game

    def lose_game(self):
        """
        Ends the game in a loss
        """
        print("You lose!")
        GameManager.destroy()

    def win_game(self):
        """
        Ends the game with a win
        """
        print("You win!")
        GameManager.destroy()

class SelectionManager:
    """
    Manages the player's ability to select a Contraption
    """

    _frame = None
    """
    The TKinter frame on which we draw the lanes of the board
    """

    _selector_frame = None
    """
    The TKinter frame on which we draw selector buttons
    """

    _information_frame = None
    """
    The TKinter frame on which we draw battery information and the end turn button
    """

    _battery_text = None
    """
    Text indicating the number of batteries
    """

    _round_text = None
    """
    Text indicating the number of Rounds that have passed
    """

    _end_turn = None
    """
    Button used to end the player turn
    """

    _selectors = None
    """
    Ordered list of selectors that the player can interact with
    Strictly speaking, this need not be stored, but that feels wrong to just drop
    """

    _current_selector = None
    """
    The currently clicked selector, which holds the selected contraption
    If no selector is clicked or after placing a contraption, then this can be None
    """

    def __init__(self, contraptions, batteries):
        """
        Constructs a selector from the provided (ordered) list of contraptions
        Also must be provided a (non-negative) number of starting batteries
        The allowed contraptions may depend on the specific game
        """
        assert batteries >= 0
        assert isinstance(contraptions, list)

        # Setup the frames
        frame = tk.Frame(
            GameManager.manager().root(),
            width=WINDOW_WIDTH,
            height=WINDOW_HEIGHT - BOARD_HEIGHT)
        self._frame = frame

        frame.pack(side=tk.TOP)

        selector_frame = tk.Frame(frame,
                                  width=WINDOW_WIDTH - INFO_WIDTH)
        self._selector_frame = selector_frame

        information_frame = tk.Frame(frame,
                                     width=INFO_WIDTH)
        self._information_frame = information_frame

        attention_frame = tk.Frame(frame,
                                    width=INFO_WIDTH)

        selector_frame.place(relx=0, rely=0.5, relheight=1.0, anchor=tk.W)
        information_frame.place(relx=1.0, rely=0.5, relheight=1.0, anchor=tk.E)
        attention_frame.place(relx=0.6, rely=0, relheight=1.0, anchor=tk.N)

        # Setup the selectors
        self._selector = []
        for column, contraption in enumerate(contraptions):
            self._selector.append(Selector(selector_frame, contraption, column))
        self._current_selector = None
    
        # Setup the attention text
        attention_text = tk.Label(attention_frame, font=('consolas', 22, ''), text=f'')
        attention_text.pack()
        self._attention_text = attention_text

        # Setup the end turn button
        end_turn = tk.Button(
            information_frame,
            bg='white',
            font=('consolas', 22, ''),
            command=self._end_turn_clicked,
            text='End Turn'
        )
        self._end_turn = end_turn
        end_turn.pack()

        # Setup the battery and round texts
        self._battery_text = tk.Label(
            information_frame, font=('consolas', 22, ''))
        self.update_battery_text(batteries)
        self._battery_text.pack()
        self._round_text = tk.Label(
            information_frame, font=('consolas', 22, ''))
        self.update_round_text(0)
        self._round_text.pack()

    def frame(self):
        """
        Returns the frame on which this selection manager is displayed
        """
        return self._frame

    def get_current_contraption(self):
        """
        Returns the currently selected Contraption if one is selected
        """
        if self._current_selector is None:
            return None
        return self._current_selector.contraption()

    def get_current_constructor(self):
        """
        Returns the currently selected Contraption constructor if one is selected
        """
        if self._current_selector is None:
            return None
        return self._current_selector.constructor()

    def set_current_selector(self, selector):
        """
        Updates the current selector to the given selector
        """
        if self._current_selector is not None:
            self._current_selector.deselect()
        self._current_selector = selector
        selector.select()

    def clear_current_selector(self):
        """
        Clears any selected contraption
        """
        if self._current_selector is not None:
            self._current_selector.deselect()
        self._current_selector = None

    def update_round_text(self, round):
        """
        Updates the number of rounds displayed to the user
        The round number is validated to be positive
        """
        assert round >= 0
        self._round_text.config(text=f'Round: {round}')

    def update_battery_text(self, batteries):
        """
        Updates the number of batteries displayed to the user
        The number of batteries are validated to be positive
        """
        assert batteries >= 0
        self._battery_text.config(text=f'Batteries: {batteries}')

    def _end_turn_clicked(self):
        """
        The event triggered when the end-of-turn button is clicked
        """
        self.clear_current_selector()
        GameManager.manager().end_round()

    def update_attention_text(self, attentions):
        """
        Updates the list of attention per-Cat
        Concretely, this list of attention spans must be already formatted as an int
        """
        assert isinstance(attentions, list)
        text = 'Cat Attentions:\n'
        for attention in attentions:
            assert isinstance(attention, int)
            if attention == 0:
                text += f'R '
            else:
                text += f'{attention} '
        self._attention_text.config(text=text)


class Selector:
    """
    Manages a specific contraption selection the player can make
    """

    _contraption = None
    """
    The read-only contraption associated with this Selector
    """

    _constructor = None
    """
    The contraption constructor expression associated with this Selector
    """

    _button = None
    """
    The Tkinter button the player can interact with to select a contraption
    """

    _selected = None
    """
    Whether or not this selector is currently selected by the player
    """

    def __init__(self, frame, constructor, column):
        """
        Builds a selector for the given contraption on the given frame
        """
        assert isinstance(frame, tk.Frame)
        assert isinstance(column, int)

        self._constructor = constructor
        contraption = constructor()
        assert isinstance(contraption, Contraption)

        self._contraption = contraption
        button = tk.Button(
            frame,
            bg='white',
            width=TILE_WIDTH,
            height=TILE_HEIGHT,
            command=self._clicked,
            # start with the empty image
            image=contraption.image(),
        )
        label = tk.Label(frame, font=('consolas', 16, ''), text=f'Cost {contraption.cost()}')
        self._button = button
        button.grid(row=0, column=column)
        label.grid(row=1, column=column)

    def contraption(self):
        """
        Returns the contraption associated with this Selector
        """
        return self._contraption

    def constructor(self):
        """
        Returns the contraption associated with this Selector
        """
        return self._constructor

    def selected(self):
        """
        Returns true if this Selector is selected
        """
        return self._selected

    def select(self):
        """
        Selects this selector, which changes the button color
        """
        self._selected = True
        self._button.config(bg='darkgray')

    def deselect(self):
        """
        Removes the selection from this selector, which changes the button color
        """
        self._selected = False
        self._button.config(bg='white')

    def _clicked(self):
        """
        Called when this button is pressed
        The selection manager handles calling `select()` on this object
        """
        GameManager.manager().selection_manager().set_current_selector(self)


class Board:
    """
    Manages the geometry of the game board
    """

    _frame = None
    """
    The TKinter frame on which we draw the lanes of the board
    """

    _lanes = None
    """
    The entry tile for each lane from the perspective of the cats
    """

    _attention_text = None
    """
    The Label listing the attention spans of each cat
    """

    def __init__(self, lanes):
        # Construct and assign the frame
        frame = tk.Frame(
            GameManager.manager().root(),
            width=WINDOW_WIDTH,
            height=BOARD_HEIGHT)
        self._frame = frame

        # Center the main frame on the root
        frame.pack(side=tk.TOP, expand=True)

        # Setup lanes along the window
        # Each tile constructs their own buttons
        self._lanes = []
        for row in range(lanes):
            next = Tile(frame)
            next.align(row, 0)
            # Subtract one to account for the head already being made
            for column in range(1, LANE_WIDTH):
                next = Tile(frame, next)
                next.align(row, column)
            self._lanes.append(next)

    def get_lane_count(self):
        """
        Returns the number of lanes in this game
        """
        return len(self._lanes)

    def get_lane_entrance(self, index):
        """
        Returns the entrance tile of the given in-bounds lane index
        """
        return self._lanes[index]

    def frame(self):
        """
        Returns a reference to the main frame on which we draw
        """
        return self._frame

# --------------------------------
# The classes you'll be interacting with


class Tile:
    """
    Holds information for a single tile on the board
    Each tile can hold exactly one actor, and may have a successor and predecessor
    """

    _button = None
    """
    The Tkinter button used to interact with this Tile (e.g. to place a contraption)
    """

    _actor = None
    """
    The Actor contained in this Tile
    Only one Actor can be on a tile at once
    """

    _entrance = None
    """
    The Tile _entrance_ from this particular board tile.  
    Visually this is the Tile _left_ of this Tile
    """

    _exit = None
    """
    The Tile _exit_ from this particular board tile.  
    Visually this is the Tile _right_ of this Tile
    """

    def __init__(self, frame, exit= None):
        """
        Initializes a tile with a given frame to attach to
            along with an (optional) tile entrance
        We choose to restrict constructing a tile with an explicit exit
        Instead, adding a tile as an entrance will update the provided tile's exit
        """
        assert isinstance(frame, tk.Frame)
        assert (exit is None) or isinstance(exit, Tile)

        # constant-size buttons for the tiles
        self._button = tk.Button(
            frame,
            bg='white',
            width=TILE_WIDTH,
            height=TILE_HEIGHT,
            command=self._clicked,
            # start with the empty image
            image=GameManager.manager().get_empty_image())

        self._actor = None
        self._entrance = None
        self._exit = exit

        # Update the link for the entrance
        if exit is not None:
            exit._entrance = self

    def align(self, row, column):
        """
        Packs this tile into the board along the specified alignment
        """
        self._button.grid(row=row, column=column)

    def _clicked(self):
        """
        The function called when this tile is clicked
        """
        manager = GameManager.manager()
        selected = manager.selection_manager().get_current_contraption()
        if selected is None:
            return

        # We can't build a contraption on the "entrance" to a lane or an occupied Tile
        can_build = self.entrance() is not None and self.is_empty()
        # We also can only build a contraption if we can afford it
        can_build = can_build and selected.cost() <= manager.batteries()
        if can_build:
            manager.spend_batteries(selected.cost())

            # a bunch of silliness to construct a new contraption and place it
            constructor = manager.selection_manager().get_current_constructor()
            new_contraption = constructor()
            manager.selection_manager().clear_current_selector()

            new_contraption.place(self) # semi-evil reference trickery

    def _set_image(self, image):
        """
        An internal helper function to set the image displayed by this tile
        """
        assert (isinstance(image, tk.PhotoImage))
        self._button.config(image=image)

    def entrance(self):
        """
        Returns a reference to the tile that _enters_ this tile in the lane
          (from the perspective of the cats)
        Returns none if no such tile exists
        """
        return self._entrance

    def exit(self):
        """
        Returns a reference to the tile that is the _exit_ from this tile
          (from the perspective of the cats)
        Returns none if no such tile exists
        """
        return self._exit

    def actor(self):
        """
        Returns a reference to the actor in this tile if one exists
        """
        return self._actor

    def is_empty(self):
        """
        Returns true if this tile is empty, that is, it does not contain an actor
        """
        return self._actor is None

    def set_actor(self, actor):
        """
        Updates this tile to contain a new actor
        This tile must not have an actor to take on a new actor
        """
        assert self.is_empty()
        assert isinstance(actor, Actor)
        self._actor = actor
        self._set_image(actor.image())
            

    def clear_actor(self):
        """
        Clears the actor from this tile
        Requires that this tile contain an actor
        This should be called when an actor is moved to another tile
        or when it is removed from the game
        """
        assert not self.is_empty()
        self._actor = None
        self._set_image(GameManager.manager().get_empty_image())


class Actor:
    """
    Holds information about a single Actor
    Every Actor has an associated image
    """

    _image = None
    """
    The (constant) image associated with this Actor
    """

    _tile = None
    """
    The Tile that this Actor is on within the game board
    If this Actor is not on the Board, this will be None
    """

    def __init__(self, image_name):
        """
        Requires the name of a valid image and a GameManager to setup an actor
        """
        self._image = GameManager.manager().get_actor_image(image_name)
        self._tile = None

    def image(self):
        """
        Returns the image associated with this actor
        """
        return self._image

    def current_tile(self):
        """
        Returns the tile of the board this Actor is on
        Note
        """
        assert self.is_on_board()
        return self._tile

    def is_on_board(self):
        """
        Returns whether or not this Actor is on the board
        """
        return self._tile is not None

    def remove_from_board(self):
        """
        Removes this Actor from the board
        """
        self._tile.clear_actor()
        self._tile = None

    def move(self, tile):
        """
        Moves this Actor to another tile
        """
        assert isinstance(tile, Tile)
        if self.is_on_board():
            self._tile.clear_actor()
        self._tile = tile
        tile.set_actor(self)

    def __repr__(self):
        # A quick and dirty inspection function to help with debugging
        return f'{self.__class__.__name__} : {vars(self)}'


class Contraption(Actor):
    """
    Base class that represents all contraptions
    """

    _cost = None
    """
    Cost (in batteries) to place this contraption
    """

    def __init__(self, image_name, cost):
        """
        Initializes this contraption with a positive cost
        """
        super().__init__(image_name)
        assert isinstance(cost, int) and cost >= 0
        self._cost = cost

    def cost(self):
        """
        Returns the cost in batteries for this contraption
        """
        return self._cost
    
    def place(self, tile):
        """
        Places this contraption on the board
        """
        assert isinstance(tile, Tile)
        
        GameManager.manager().add_contraption(self)
        self.move(tile)

    def end_round(self):
        """
        Takes some action as a contraption
        By default, a contraption does nothing at the end of the round
        """
        pass

    def interact(self):
        """
        A cat interacts with this contraption
        Any interaction immediately knocks the base contraption over
          and removes it from the board
        """
        self._tile.clear_actor()
        self._tile = None
        GameManager.manager().remove_contraption(self)


class Cat(Actor):
    """
    Base class that represents all cats
    """

    _starting_attention = None
    """
    Starting attention of this Cat when entering the board
    """

    _attention = None
    """
    The current attention of this Cat
    If attention reaches zero, this Cat becomes distracted
      and is removed from the board
    If this Cat is not on the board, this value will always be zero
    """

    _needed_rest_time = None
    """
    How many turns this cat needs to rest after becoming distracted
    """

    _rest_time = None
    """
    How long until this cat returns to the board
      If this cat is on the board, this value will always be zero
    """

    def __init__(self, image_name,
                 starting_attention,
                 needed_rest_time,
                 starting_rest_time):
        """
        Initializes this cat with the given attention and rest times

        Note that "needed_rest_time" must be greater than or equal to 1
            (a cat must rest at least one round)

        Note that we also must provide a distinct "starting rest time"
          to indicate how many rounds this cat rests
          before initially entering the board
          (this value can be larger than rest_time)
        """
        super().__init__(image_name)
        assert isinstance(starting_attention, int) and starting_attention >= 0
        assert isinstance(needed_rest_time, int) and needed_rest_time >= 1
        assert isinstance(starting_rest_time, int) and starting_rest_time >= 0

        self._attention = 0
        self._starting_attention = starting_attention
        self._needed_rest_time = needed_rest_time
        self._rest_time = starting_rest_time

    def attention(self):
        """
        Returns the current attention of this Cat
        """
        return self._attention

    def rest_time(self):
        """
        Returns how long this cat needs to rest
        """
        return self._rest_time

    def end_round(self):
        """
        Runs the behavior of this cat for the end of the round
        If this cat is on the board, move forward
        Otherwise, this cat rests and possibly is placed on the board
        """
        if self.is_on_board():
            self._move()
        else:
            self._rest()

    def _move(self):
        """
        Moves this Cat forward, if able
        If there is a contraption in the way, 
          instead "interact" with the contraption
        """
        tile = self.current_tile()

        # if we've reached the end of the lane, we interrupt the roommate and lose
        if tile.exit() is None:
            GameManager.manager().lose_game()
            return

        # if the next space is empty, move to it
        if tile.exit().is_empty():
            self.move(tile.exit())
        # otherwise, if there is a contraption in the next tile, interact with it
        elif isinstance(tile.exit().actor(), Contraption):
            tile.exit().actor().interact()
        # if there's another Cat in front of us, then there's nothing to do
        else:
            return

    def _rest(self):
        """
        Reduces the current rest time of this cat by one
        If this Cat is finished resting, attempts to place this cat
          on an empty starting board position
        If there are no available board positions, this Cat rests another round
        """
        self._rest_time -= 1

        # if we're done resting, attempt to add this Cat to the board
        if self._rest_time == 0:
            board = GameManager.manager().board()
            # First, find all of the empty lanes
            empty_lanes= []
            for lane_index in range(board.get_lane_count()):
                lane = board.get_lane_entrance(lane_index)
                if lane.is_empty():
                    empty_lanes.append(lane)

            # if there are no empty lanes, rest another round
            if len(empty_lanes) == 0:
                self._rest_time = 1

            # otherwise, add self to an empy lane at random
            else:
                index = random.randint(0, len(empty_lanes)-1)
                lane_to_add = empty_lanes[index]
                self._attention = self._starting_attention
                self.move(lane_to_add)

    def distract(self, amount):
        """
        Distracts this cat by the given amount
        If this cat is fully distracted (has no attention left)
          this cat is removed from the board and starts resting
        """
        self._attention -= amount
        if self._attention <= 0:
            self._attention = 0
            self._rest_time = self._needed_rest_time
            self.remove_from_board()
