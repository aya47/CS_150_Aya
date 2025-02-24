"""
Contraption definitions for Cats vs Homework
Author: Aya Ben Saghroune
Edit Date: Wednesday, February 27th, 2025
"""

from src.managers import GameManager, Contraption, Actor, Cat


class LaserPointer(Contraption):
    """
    Each round, points a laser to attempt to distract _every_ cat in this row
    """
    def __init__(self):
        super().__init__('laser', 7)

    def end_round(self):
        next = self._tile.entrance()
        while next is not None:
            if isinstance(next.actor(), Cat):
                next.actor().distract(1)
            next = next.entrance()


class SnackDispenser(Contraption):
    """
    Requires multiple (5) interactions from cats to knock over
    Note that interacting with a Snack Dispenser does not lower a cat's attention,
      A snack dispenser only delays the cats from advancing
    """

    # TODO: Part 1: implement this class!
    # You may find adding new methods (and perhaps a field) to be helpful
    def __init__(self):
        super().__init__('snacks', 100)

class BatteryCharger(Contraption):
    """
    Every _other_ round, charges a new battery
    Does not charge a battery the round it is placed
    Note that a Battery Charger does not lower a cat's attention,
      and only produces batteries
    """
    # TODO: Part 1: implement this class!
    # You may find adding new methods (and perhaps a field) to be helpful
    # Hint: note that you can access the game manager directly (and update batteries) with
    #  Gamemanager.manager()

    def __init__(self):
        super().__init__('charger', 100)

class BallThrower(Contraption):
    """
    Each round, throws a ball to distract the nearest Cat within 3 spaces
    If there is no such Cat, this contraption does nothing
    """
    # TODO: Part 3: implement this class!
    # You may find adding new methods to be helpful

    def __init__(self):
        super().__init__('thrower', 100)
