# ClientWars

#### War game, but for programmers.


Python Library for playing in ServerWars Game.

### Install
```shell script
pip3 install clients_wars
```

### Example code:
```python
from game import Game

game = Game("34f97bfd-8547-4977-827e-cd82cbeeeb4c")

def turn(game):
    conquers = game.conquerable_tiles()

    if not conquers:
        print("No conquers")
        return  # Here you can move reinforcements to the outside tiles for example

    game.move(conquers[0][1], conquers[0][0])
    print("Conquer", conquers[0][0])

game.set_turn_method(turn)
game.run()
```

### Usage
```
python3 your_code.py
```
