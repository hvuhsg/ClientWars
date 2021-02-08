from threading import Thread
from websocket import WebSocketApp, enableTrace
from time import sleep
from json import loads
from loguru import logger

from .tile import Tile
from .config import GAME_HOST, SECURE_CONNECTION


class MapUpdater(Thread):
    def __init__(self, token, map, client_id):
        super().__init__()
        enableTrace(False)
        protocol = "wss" if SECURE_CONNECTION else "ws"
        ws_url = f"{protocol}://{GAME_HOST}/ws?token={token}&client_id={client_id}"
        self.websocket = WebSocketApp(
            ws_url,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
            on_open=self.on_open
          )
        self.map = map
        self._close = False

    def run(self):
        logger.info("Starting MapUpdater... (for getting map updates)")
        while not self._close:
            self.websocket.run_forever()
            sleep(1)

    def close(self):
        logger.info("Closing MapUpdater...")
        self._close = True
        self.websocket.close()

    def on_message(self, message):
        tile_dict = loads(message)
        self.map.update([Tile.from_dict(tile_dict)])

    def on_error(self, error):
        logger.error(error)

    def on_close(self):
        logger.debug("MapUpdater Closed")

    def on_open(self, *args, **kwargs):
        logger.debug("MapUpdater Started")
