from typing import Dict, List, Tuple, Union
from loguru import logger

from .client import Client
from .tile import Tile
from .player import Player
from .config import CHUNK_SIZE


class Map:
    def __init__(self, client: Client):
        self.tiles: Dict[Tuple[int, int], Tile] = {}
        self._client = client
        self.players_on_map: Dict[str, Player] = {}
        self.me: Player = None

    def get(self, coordinates: Tuple[int, int]) -> Union[Tile, None]:
        result = self.tiles.get(coordinates, None)
        if result is None:
            self.load(coordinates[0], coordinates[1], chunk_size=CHUNK_SIZE)
            result = self.tiles.get(coordinates, None)
            logger.debug(f"Load map at {coordinates}, with rage of {CHUNK_SIZE}")
        return result

    def update(self, tiles: List[Tile]) -> None:
        tiles_of_players = filter(lambda tile: tile.owner, tiles)
        self._update_players(tiles_of_players)
        self.tiles.update({tile.coordinates(): tile for tile in tiles})

    def load(self, x: int, y: int, chunk_size=CHUNK_SIZE) -> None:
        tiles = self._client.load_map(x, y, chunk_size)
        tiles = self._json_to_objects(tiles)
        self.update(tiles.values())

    def _json_to_objects(self, tiles: dict) -> Dict[str, Tile]:
        objects_dict = {}
        for coordinates, tile in tiles.items():
            objects_dict[tuple(map(int, coordinates.split(",")))] = Tile.from_dict(tile)
        return objects_dict

    def _update_players(self, tiles: List[Tile]) -> None:
        for tile in tiles:
            if tile.owner not in self.players_on_map:
                self.players_on_map[tile.owner] = Player(name=tile.owner, tiles=[tile])
            player = self.players_on_map[tile.owner]
            player.update([tile])
