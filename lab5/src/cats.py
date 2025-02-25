"""
Contraption definitions for Cats vs Homework
Author: Aya Ben Saghroune
Edit Date: Wednesday, February 27th, 2025
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

    Also, from pdf instructions: increase _starting_attention by 1
    """
    # TODO: Part 2: implement this class!
    # You may find adding new methods to be helpful
    def __init__(self, initial_rest_time : int):
        super().__init__('calico', 4, 4, initial_rest_time)
        #assert False, "Calico unimplemented"
    def distract(self, amount):
        if self.attention ==0:
            self.initial_rest_time += 1

        self._attention -= amount
        if self._attention <= 0:
            self._attention = 0
            self._rest_time = self._needed_rest_time
            self.remove_from_board()
        
        # when cat rests, add 1 to its _starting_attention
        if not self.is_on_board():
            self._starting_attention += 1
        
class Kitten(Cat):
    """
    Especially energetic, kittens get to take two moves _per turn_
    Fortunately, kittens are easily distractable and take long rests
    """
    # TODO: Part 2:  implement this class!
    # You may find adding new methods to be helpful
    def __init__(self, initial_rest_time : int):
        super().__init__('kitten', 3, 6, initial_rest_time)
        #assert False, "Kitten unimplemented"

    def end_round(self):
        """
        Runs the behavior of this cat for the end of the round
        If this cat is on the board, move forward
        Otherwise, this cat rests and possibly is placed on the board
        """
        if self.is_on_board():
            self._move()
            self._move()
        else:
            self._rest()
