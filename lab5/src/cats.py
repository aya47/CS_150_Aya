"""
Contraption definitions for Cats vs Homework
"""

from src.managers import Cat

class Tabby(Cat):
    """
    A moderately distractable cat that just wants to hang out
    """
    def __init__(self, initial_rest_time : int):
        super().__init__('tabby', 4, 4, initial_rest_time)

class Calico(Cat):
    """
    A particularly clever cat
    They become less distractable after each rest
    Concretely, a Calico's _starting_rest_time increases by one 
      each time the Calico's attention is reduced to zero
    """
    # TODO: Part 2: implement this class!
    # You may find adding new methods to be helpful
    def __init__(self, initial_rest_time : int):
        super().__init__('calico', 1, 1, 0)
        assert False, "Calico unimplemented"

class Kitten(Cat):
    """
    Especially energetic, kittens get to take two moves _per turn_
    Fortunately, kittens are easily distractable and take long rests
    """
    # TODO: Part 2:  implement this class!
    # You may find adding new methods to be helpful
    def __init__(self, initial_rest_time : int):
        super().__init__('kitten', 1, 1, 0)
        assert False, "Kitten unimplemented"