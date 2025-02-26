"""
Test cases for Cats vs. Homework
Last edited by Geisler 2024
"""

import src.contraptions as contraptions
import src.cats as cats
from src.managers import *
from src.main_menu import CONTRAPTIONS
import math

DEFAULT_CATS = [lambda: cats.Tabby(1)]

def eq_test(expected, actual, test):
    """
    Helper to provide error context
    """
    assert expected == actual, \
        f'  Error in {test}: expected {expected} got {actual}'

def float_eq_test(expected, actual, test):
    """
    Helper to provide float error context
    """
    assert math.isclose(expected, actual), \
        f'  Error in {test}: expected {expected} got {actual}'
    

def test_tabby_constructor(test):
    """
    Tests our Tabby constructor
    """
    # setup for testing
    GameManager.initialize(1, CONTRAPTIONS, [
        lambda: cats.Tabby(1),
        lambda: cats.Tabby(2)
    ])
    manager = GameManager.manager()
    
    # we just need to test parameters
    assert len(manager._cats) == 2
    cat1 = manager._cats[0]
    cat2 = manager._cats[1]
    eq_test(4, cat1._starting_attention, test)
    eq_test(4, cat2._starting_attention, test)
    eq_test(4, cat1._needed_rest_time, test)
    eq_test(4, cat2._needed_rest_time, test)
    eq_test(1, cat1.rest_time(), test)
    eq_test(2, cat2.rest_time(), test)

    # Cleanup
    GameManager.destroy()

def test_tabby_rest(test):
    """
    Tests our Tabby resting setup
    """
    # setup for testing
    GameManager.initialize(1, CONTRAPTIONS, [
        lambda: cats.Tabby(2)
    ])
    manager = GameManager.manager()
    
    # test initial parameters
    assert len(manager._cats) == 1
    cat = manager._cats[0]
    eq_test(2, cat.rest_time(), test)
    eq_test(False, cat.is_on_board(), test)

    # rest cat by one
    cat.end_round()
    eq_test(1, cat.rest_time(), test)
    eq_test(False, cat.is_on_board(), test)

    # finish resting
    cat.end_round()
    eq_test(0, cat.rest_time(), test)
    eq_test(4, cat.attention(), test)
    eq_test(True, cat.is_on_board(), test)

    # Cleanup
    GameManager.destroy()

def test_tabby_move(test):
    """
    Tests our Tabby movement setup
    """
    # setup for testing
    GameManager.initialize(1, CONTRAPTIONS, [
        lambda: cats.Tabby(1)
    ])
    manager = GameManager.manager()
    
    # test initial parameters
    assert len(manager._cats) == 1
    cat = manager._cats[0]

    # add cat to board
    cat.end_round()
    eq_test(True, cat.is_on_board(), test)
    eq_test(True, cat.current_tile().entrance() is None, test)
    starting_tile = cat.current_tile()

    # move the cat by one
    cat.end_round()
    eq_test(True, cat.is_on_board(), test)
    eq_test(starting_tile, cat.current_tile().entrance(), test)

    # Cleanup
    GameManager.destroy()

def test_tabby():
    """
    Runs all of our Tabby tests
    """
    test_tabby_constructor('Tabby constructor')
    test_tabby_rest('Tabby rest')
    test_tabby_move('Tabby move')

    print("All Tabby tests passed")

def test_laser_constructor(test):
    """
    Tests our laser pointer constructor
    """
    # setup for testing
    GameManager.initialize(1, CONTRAPTIONS, DEFAULT_CATS)
    manager = GameManager.manager()
    
    # we just need to test cost
    laser = contraptions.LaserPointer()
    eq_test(7, laser.cost(), test)

    # Cleanup
    GameManager.destroy()

def test_laser_interaction(test):
    """
    Tests that our laser pointer is knocked over in one interaction
    """
    # setup for testing
    GameManager.initialize(1, CONTRAPTIONS, DEFAULT_CATS)
    manager = GameManager.manager()
    
    # build the laser and place it
    laser = contraptions.LaserPointer()
    laser.place(manager.board().get_lane_entrance(0))
    eq_test(True, laser.is_on_board(), test)
    eq_test(1, len(manager._contraptions), test)

    # interact with the laser
    laser.interact()
    eq_test(False, laser.is_on_board(), test)
    eq_test(0, len(manager._contraptions), test)

    # Cleanup
    GameManager.destroy()

def test_laser_action(test):
    """
    Tests that our laser pointer distracts all cats in the row
    """
    # setup for testing
    GameManager.initialize(1, CONTRAPTIONS, 
                           # two cats
                        [lambda: cats.Tabby(1), lambda: cats.Tabby(1)])
    manager = GameManager.manager()

    # get references to the cats
    assert len(manager._cats) == 2
    cat1 = manager._cats[0]
    cat2 = manager._cats[1]
    
    # build the laser and place it
    laser = contraptions.LaserPointer()
    # place the laser 2 spaces from the entrance
    laser.place(manager.board().get_lane_entrance(0).exit().exit())

    # check that the cats aren't on the board
    eq_test(False, cat1.is_on_board(), test)

    # add cat1 to the board
    cat1.end_round()
    eq_test(True, cat1.is_on_board(), test)
    eq_test(4, cat1.attention(), test)

    # take the laser_pointer action
    laser.end_round()
    eq_test(3, cat1.attention(), test)

    # move cat1 and add cat2 to the board
    cat1.end_round()
    cat2.end_round()
    eq_test(True, cat2.is_on_board(), test)
    eq_test(4, cat2.attention(), test)

    # take the laser_pointer action again
    laser.end_round()
    eq_test(2, cat1.attention(), test)
    eq_test(3, cat2.attention(), test)

    # Cleanup
    GameManager.destroy()

def test_laser():
    """
    Runs all of our laser pointer tests
    """
    test_laser_constructor('LaserPointer constructor')
    test_laser_interaction('LaserPointer interaction')
    test_laser_action('LaserPointer action')

    print("All Laser Pointer tests passed")

def test_snack_constructor(test):
    """
    Tests our snack dispenser constructor
    """
    # setup for testing
    GameManager.initialize(1, CONTRAPTIONS, DEFAULT_CATS)
    manager = GameManager.manager()
    
    # we just need to test cost
    snack = contraptions.SnackDispenser()
    eq_test(4, snack.cost(), test)

    # Cleanup
    GameManager.destroy()

def test_snack_interaction(test):
    """
    Tests that our snack dispenser is knocked over in exactly 5 interactions
    """
    # setup for testing
    GameManager.initialize(1, CONTRAPTIONS, DEFAULT_CATS)
    manager = GameManager.manager()
    
    # build the snack dispenser and place it
    snack = contraptions.SnackDispenser()
    snack.place(manager.board().get_lane_entrance(0))
    eq_test(True, snack.is_on_board(), test)
    eq_test(1, len(manager._contraptions), test)

    # interact with the snack dispenser 4 times, should be on the board each time
    snack.interact()
    eq_test(True, snack.is_on_board(), test)
    snack.interact()
    eq_test(True, snack.is_on_board(), test)
    snack.interact()
    eq_test(True, snack.is_on_board(), test)
    snack.interact()
    eq_test(True, snack.is_on_board(), test)
    
    # interact with the snack dispenser a 5th time, knocking it over
    snack.interact()
    eq_test(False, snack.is_on_board(), test)
    eq_test(0, len(manager._contraptions), test)

    # Cleanup
    GameManager.destroy()

def test_snack():
    """
    Runs all of our snack dispenser tests
    """
    test_snack_constructor('SnackDispenser constructor')
    test_snack_interaction('SnackDispenser interaction')

    print("All Snack Dispenser tests passed")

def test_charger_constructor(test):
    """
    Tests our charger constructor
    """
    # setup for testing
    GameManager.initialize(1, CONTRAPTIONS, DEFAULT_CATS)
    manager = GameManager.manager()
    
    # we just need to test cost
    charger = contraptions.BatteryCharger()
    eq_test(3, charger.cost(), test)

    # Cleanup
    GameManager.destroy()

def test_charger_interaction(test):
    """
    Tests that our charger is knocked over on the first interaction
    """
    # setup for testing
    GameManager.initialize(1, CONTRAPTIONS, DEFAULT_CATS)
    manager = GameManager.manager()
    
    # build the charger and place it
    charger = contraptions.BatteryCharger()
    charger.place(manager.board().get_lane_entrance(0))
    eq_test(True, charger.is_on_board(), test)
    eq_test(1, len(manager._contraptions), test)

    # interact with the charger
    charger.interact()
    eq_test(False, charger.is_on_board(), test)
    eq_test(0, len(manager._contraptions), test)

    # Cleanup
    GameManager.destroy()

def test_charger_end_turn(test):
    """
    Tests that our charger adds batteries every _other_ round
    """
    # setup for testing
    GameManager.initialize(1, CONTRAPTIONS, DEFAULT_CATS)
    manager = GameManager.manager()
    
    # build the charger and place it
    charger = contraptions.BatteryCharger()
    charger.place(manager.board().get_lane_entrance(0))
    eq_test(True, charger.is_on_board(), test)
    eq_test(1, len(manager._contraptions), test)

    # end the charger round twice (without directly adjusting the game manager)
    eq_test(8, manager.batteries(), test)
    charger.end_round()
    eq_test(8, manager.batteries(), test)
    charger.end_round() # add a battery after the second round
    eq_test(9, manager.batteries(), test)

    # Cleanup
    GameManager.destroy()

def test_charger():
    """
    Runs all of our charger tests
    """
    test_charger_constructor('BatteryCharger constructor')
    test_charger_interaction('BatteryCharger interaction')
    test_charger_end_turn('BatteryCharger end turn')

    print('All BatteryCharger Tests Passed')

def test_calico_constructor(test):
    """
    Tests our Calico constructor
    """
    # setup for testing
    GameManager.initialize(1, CONTRAPTIONS, [
        lambda: cats.Calico(1),
        lambda: cats.Calico(2)
    ])
    manager = GameManager.manager()
    
    # we just need to test parameters
    assert len(manager._cats) == 2
    cat1 = manager._cats[0]
    cat2 = manager._cats[1]
    eq_test(4, cat1._starting_attention, test)
    eq_test(4, cat2._starting_attention, test)
    eq_test(4, cat1._needed_rest_time, test)
    eq_test(4, cat2._needed_rest_time, test)
    eq_test(1, cat1.rest_time(), test)
    eq_test(2, cat2.rest_time(), test)

    # Cleanup
    GameManager.destroy()

def test_calico_distracted(test):
    """
    Tests our Calico distraction setup
    """
    # setup for testing
    GameManager.initialize(1, CONTRAPTIONS, [
        lambda: cats.Calico(1)
    ])
    manager = GameManager.manager()
    
    # test initial parameters
    assert len(manager._cats) == 1
    cat = manager._cats[0]
    eq_test(1, cat.rest_time(), test)
    eq_test(False, cat.is_on_board(), test)

    # add cat to board
    cat.end_round()
    eq_test(True, cat.is_on_board(), test)
    eq_test(4, cat.attention(), test)
    

    # distract the cat
    cat.distract(4)
    eq_test(False, cat.is_on_board(), test)

    # check the rest time and new attention
    eq_test(4, cat.rest_time(), test)
    eq_test(5, cat._starting_attention, test)

    # add the cat back to the board and double-check attention
    cat.end_round()
    cat.end_round()
    cat.end_round()
    cat.end_round()
    eq_test(True, cat.is_on_board(), test)
    eq_test(5, cat.attention(), test)

    # Cleanup
    GameManager.destroy()

def test_calico():
    """
    Runs all of our Calico tests
    """
    test_calico_constructor('Calico constructor')
    test_calico_distracted('Calico distracted')

    print("All Calico tests passed")

def test_kitten_constructor(test):
    """
    Tests our Kitten constructor
    """
    # setup for testing
    GameManager.initialize(1, CONTRAPTIONS, [
        lambda: cats.Kitten(1)
    ])
    manager = GameManager.manager()
    
    # we just need to test parameters
    assert len(manager._cats) == 1
    cat = manager._cats[0]
    eq_test(3, cat._starting_attention, test)
    eq_test(6, cat._needed_rest_time, test)
    eq_test(1, cat.rest_time(), test)

    # Cleanup
    GameManager.destroy()

def test_kitten_move(test):
    """
    Tests our Kitten end_round/movement setup
    """
    # setup for testing
    GameManager.initialize(1, CONTRAPTIONS, [
        lambda: cats.Kitten(1)
    ])
    manager = GameManager.manager()
    
    # test initial parameters
    assert len(manager._cats) == 1
    cat = manager._cats[0]
    eq_test(1, cat.rest_time(), test)
    eq_test(False, cat.is_on_board(), test)

    # add kitten to board
    cat.end_round()
    eq_test(True, cat.is_on_board(), test)
    eq_test(True, cat.current_tile().entrance() is None, test)
    starting_tile = cat.current_tile()

    # move the kitten (moves twice!)
    cat.end_round()
    eq_test(True, cat.is_on_board(), test)
    eq_test(starting_tile, cat.current_tile().entrance().entrance(), test)
    new_tile = cat.current_tile()

    # Put a contraption in front of the kitten
    charger = contraptions.LaserPointer()
    charger.place(manager.board().get_lane_entrance(0).exit().exit().exit())
    eq_test(1, len(manager._contraptions), test)

    # move the kitten (interact and then move!)
    cat.end_round()
    eq_test(0, len(manager._contraptions), test)
    eq_test(new_tile, cat.current_tile().entrance(), test)

    # Cleanup
    GameManager.destroy()

def test_kitten():
    """
    Runs all of our Kitten tests
    """
    test_kitten_constructor('Kitten constructor')
    test_kitten_move('Kitten move')

    print("All Kitten tests passed")

def test_ballthrower_constructor(test):
    """
    Tests our laser pointer constructor
    """
    # setup for testing
    GameManager.initialize(1, CONTRAPTIONS, DEFAULT_CATS)
    manager = GameManager.manager()
    
    # we just need to test cost
    thrower = contraptions.BallThrower()
    eq_test(3, thrower.cost(), test)

    # Cleanup
    GameManager.destroy()

def test_ballthrower_interaction(test):
    """
    Tests that our laser pointer is knocked over in one interaction
    """
    # setup for testing
    GameManager.initialize(1, CONTRAPTIONS, DEFAULT_CATS)
    manager = GameManager.manager()
    
    # build the thrower and place it
    thrower = contraptions.BallThrower()
    thrower.place(manager.board().get_lane_entrance(0))
    eq_test(True, thrower.is_on_board(), test)
    eq_test(1, len(manager._contraptions), test)

    # interact with the thrower
    thrower.interact()
    eq_test(False, thrower.is_on_board(), test)
    eq_test(0, len(manager._contraptions), test)

    # Cleanup
    GameManager.destroy()

def test_ballthrower_action(test):
    """
    Tests that our thrower distracts only the first cat in a row
    Also test the range of our thrower
    """
    # setup for testing
    GameManager.initialize(1, CONTRAPTIONS, 
                           # two cats
                        [lambda: cats.Tabby(1), lambda: cats.Tabby(1)])
    manager = GameManager.manager()

    # get references to the cats
    assert len(manager._cats) == 2
    cat1 = manager._cats[0]
    cat2 = manager._cats[1]
    
    # build the laser and place it
    thrower = contraptions.BallThrower()
    # place the laser 2 spaces from the entrance
    thrower.place(manager.board().get_lane_entrance(0).exit().exit().exit().exit())

    # check that the cats aren't on the board
    eq_test(False, cat1.is_on_board(), test)

    # add cat1 to the board
    cat1.end_round()
    eq_test(True, cat1.is_on_board(), test)
    eq_test(4, cat1.attention(), test)

    # take the ballthrower action, which misses
    print('Test 1, should miss\n')
    thrower.end_round()
    eq_test(4, cat1.attention(), test)

    # move cat1 and add cat2 to the board
    cat1.end_round()
    cat2.end_round()
    eq_test(True, cat2.is_on_board(), test)
    eq_test(4, cat2.attention(), test)

    # take the ballthrower action again, which hits the first cat
    print('\nTest 2, should hit cat 1\n')
    thrower.end_round()
    eq_test(3, cat1.attention(), test)
    eq_test(4, cat2.attention(), test)
    

    # move both cats
    cat1.end_round()
    cat2.end_round()

    # take the ballthrower action again, which hits only the first cat
    print('\nTest 3\n')
    thrower.end_round()
    eq_test(2, cat1.attention(), test)
    eq_test(4, cat2.attention(), test)

    # Cleanup
    GameManager.destroy()

def test_ballthrower():
    """
    Runs all of our laser pointer tests
    """
    test_ballthrower_constructor('BallThrower constructor')
    test_ballthrower_interaction('BallThrower interaction')
    test_ballthrower_action('BallThrower action')

    print('All BallThrower tests passed')


def main():
    """
    Run all of our tests, even if some fail
    We report errors without crashing for each test
    """

    test_tabby()
    test_laser()
    test_snack()
    test_charger()
    test_calico()
    test_kitten()
    test_ballthrower()

    print(f'All tests passed')

if __name__ == "__main__":
    main()