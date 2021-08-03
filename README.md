# ClientWars

#### War game, but for programmers.

#### [register now](https://game.qwhale.ml)


Python Library for playing in ServerWars Game.

### Install
```shell script
pip3 install -U ClientWars
```

### Example code:
```python
from client_wars import Game

game = Game("<TOKEN>")


def turn(game):
    conquers = game.conquerable_tiles()
    """
    The method conquerable_tiles return's list of per of neighbors tiles when your tile has more power
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

```

### Usage
```
python3 your_code.py
```

### [Wiki](https://github.com/hvuhsg/ClientWars/wiki)


