from typing import List, Callable, Union, Tuple
from loguru import logger
from time import sleep

from .client import Client
from .map import Map
from .tile import Tile
from .websocket_updater import MapUpdater


TileList = List[Tile]
TileTuple = Tuple[Tile]


class Game:
    def __init__(self, token):
        self.client_id = "LIB-ID"
        self._client = Client(token, self.client_id)
        self.token = token
        self.map = Map(self._client)
        self.map_updater = MapUpdater(token, self.map, self.client_id)
        self.my = None
        self.time_per_move = None  # Seconds
        self.started: bool = None
        self.play: Callable = None
        self._setup()

    def _setup(self):
        logger.info("Start game setup.")
        self.map_updater.start()

        self.my = self._client.me()
        self.time_per_move = self.my["game"]["time_per_move"]
        self.started = self.my["game"]["started"]
        spawn_point = self.my["player"]["spawn_point"]

        tile_objects = []
        for my_tile in self.my["tiles"]:
            tile_object = self.map.get((my_tile["x"], my_tile["y"]))
            tile_objects.append(tile_object)
        self.my = self.map.players_on_map[self.my["player"]["name"]]
        self.my.spawn_point = spawn_point
        logger.info("End game setup.")
        logger.success(f"For GUI view of the game map goto {self._client.link_to_gui_map()}")
        logger.warning("Do not share this link is't contain you'r secret token!")

    def set_turn_method(self, turn_method):
        if not callable(turn_method):
            raise TypeError("Turn method mast be callable.")
        self.play = turn_method

    def move(self, src: Tile, dst: Tile, power: Union[int, None] = None):
        self._client.move(src.x, src.y, dst.x, dst.y, power)

    def weakest_tile(self):
        return min(self.attackable_tiles())

    def neighbors(self, tile: Tile) -> TileTuple:
        return (
            self.map.get(tile.left()),
            self.map.get(tile.right()),
            self.map.get(tile.up()),
            self.map.get(tile.down())
        )

    def touching_ally(self, tile: Tile) -> TileList:
        return list(filter(lambda tilex: tilex.owner == tile.owner, self.neighbors(tile)))

    def attackable_tiles(self) -> TileList:
        attackables = []
        for tile in self.my.tiles():
            neighbors = self.neighbors(tile)
            for neighbor in neighbors:
                if neighbor.owner != self.my.name:
                    attackables.append(neighbor)

        return attackables

    def conquerable_tiles(self) -> TileList:
        conquerables = []
        for tile in self.attackable_tiles():
            for neighbor in self.neighbors(tile):
                if neighbor.owner == self.my.name and neighbor > tile:
                    conquerables.append((neighbor, tile))
                    break
        return conquerables

    def run(self):
        while True:
            try:
                self.play(self)
            except ValueError as VE:
                print(VE)
            sleep(self.time_per_move*2 - 1)
