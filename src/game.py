from typing import List, Callable
from loguru import logger
from time import sleep

from client import Client
from map import Map
from tile import Tile
from websocket_updater import MapUpdater


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
            tile_object = self.map.get((my_tile["x"], my_tile["y"]), None)
            tile_objects.append(tile_object)
        self.my = self.map.players_on_map[self.my["player"]["name"]]
        self.my.spawn_point = spawn_point
        logger.info("End game setup.")

    def set_turn_method(self, turn_method):
        if not callable(turn_method):
            raise TypeError("Turn method mast be callable.")
        self.play = turn_method

    def move(self, src: Tile, dst: Tile, power=None):
        self._client.move(src.x, src.y, dst.x, dst.y, power)

    def weakest_tile(self):
        return min(self.attackable_tiles())

    def touching_tiles(self, tile: Tile) -> List[Tile]:
        return (
            self.map.get(tile.left()),
            self.map.get(tile.right()),
            self.map.get(tile.up()),
            self.map.get(tile.down())
        )

    def touching_ally(self, tile: Tile):
        return list(filter(lambda tilex: tilex.owner == self.my.name, self.touching_tiles(tile)))

    def attackable_tiles(self):
        attackables = []
        for tile in self.my.tiles():
            left = self.map.get(tile.left())
            up = self.map.get(tile.up())
            right = self.map.get(tile.right())
            down = self.map.get(tile.down())

            if left and not left.owner:
                attackables.append(left)
            if down and not down.owner:
                attackables.append(down)
            if up and not up.owner:
                attackables.append(up)
            if right and not right.owner:
                attackables.append(right)
        return attackables

    def neighbors(self, tile):
        response = []
        left = self.map.get(tile.left())
        if left:
            response.append(left)
        right = self.map.get(tile.right())
        if right:
            response.append(right)
        up = self.map.get(tile.up())
        if up:
            response.append(up)
        down = self.map.get(tile.down())
        if down:
            response.append(down)
        return tuple(response)

    def conquerable_tiles(self):
        conquerables = []
        for tile in self.attackable_tiles():
            for neighbor in self.neighbors(tile):
                if neighbor.owner == self.my.name and neighbor > tile:
                    conquerables.append((tile, neighbor))
                    break
        return conquerables

    def run(self):
        while True:
            try:
                self.play(self)
            except ValueError as VE:
                print(VE)
            sleep(self.time_per_move*2 - 1)
