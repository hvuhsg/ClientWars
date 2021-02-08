from functools import wraps
from requests import Session, Response, ConnectionError
from loguru import logger
from time import sleep

from .config import GAME_HOST


GAME_HOST = "https://" + GAME_HOST


def check_status(func):
    @wraps(func)
    def wrapper(*args, **kwargs) -> dict:
        while True:
            try:
                res: Response = func(*args, **kwargs)
            except ConnectionError as CE:
                logger.error(CE)
                sleep(1)
                continue
            if res.status_code != 200:
                if "X-TIME" in res.headers:
                    logger.debug(res.json()['detail'])
                    sleep(float(res.headers["X-TIME"]) + 1)
                    continue
                raise ValueError(res.json()["detail"])
            return res.json()
    return wrapper


class Client:
    def __init__(self, token, client_id):
        self.token = token
        self.client_id = client_id
        self.session = Session()
        logger.info(f"Start session to game server at {GAME_HOST}")

    @check_status
    def load_map(self, x: int, y: int, chunk_size: int) -> Response:
        args = {
            "x": x,
            "y": y,
            "chunk_size": chunk_size,
            "token": self.token,
            "client_id": self.client_id,
        }
        return self.session.get(GAME_HOST + "/map", params=args)

    @check_status
    def move(self, src_x: int, src_y: int, dst_x: int, dst_y: int, power: int = None) -> Response:
        args = {
            "src_x": src_x,
            "src_y": src_y,
            "dst_x": dst_x,
            "dst_y": dst_y,
            "power": power,
            "token": self.token
        }
        if not power:
            args.pop("power")
        response = self.session.post(GAME_HOST + "/move", params=args)
        return response

    @check_status
    def me(self):
        args = {"token": self.token}
        return self.session.get(GAME_HOST + "/me", params=args)

    def link_to_gui_map(self):
        args = {"token": self.token}
        response = self.session.get(GAME_HOST + f"/guiMap", params=args)
        return response.url
