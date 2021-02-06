from game import Game

game = Game("65b2c230-5ee0-4344-a1b8-4bb500546534")


def turn(game):
    conquers = game.conquerable_tiles()
    """
    You'r tile has more power then the enemy tile
    >>> conquers
    >>> [(your_tile, enemy_tile), ...]
    """

    if not conquers:
        print("No conquers")
        return  # Here you can move reinforcements to the outside tiles for example

    game.move(conquers[0][0], conquers[0][1])
    print("Conquer", conquers[0][1])

game.set_turn_method(turn)
game.run()
