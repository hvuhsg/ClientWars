from typing import List

from tile import Tile


class Player:
    def __init__(self, name: str, tiles: List[Tile]):
        self.name = name
        self._dict_tiles = {}
        self.power = sum(map(lambda tile: tile.power, tiles))
        self.spawn_point = None

    def update(self, tiles: List[Tile]):
        self._dict_tiles.update({tile.coordinates(): tile for tile in tiles})
        self.power = sum(map(lambda tile: tile.power, self.tiles()))

    def tiles(self):
        return set(self._dict_tiles.values())
