from requests import Session, Response
from loguru import logger
from time import sleep


SERVER_URL = "http://127.0.0.1:8000"


def check_status(func):
    def wrapper(*args, **kwargs):
        while True:
            res: Response = func(*args, **kwargs)
            if res.status_code != 200:
                if "X-TIME" in res.headers:
                    logger.debug(res.json()['detail'])
                    sleep(float(res.headers["X-TIME"]))
                    continue
                raise ValueError(res.json()["detail"])
            return res.json()
    return wrapper


class Client:
    def __init__(self, token, client_id):
        self.token = token
        self.client_id = client_id
        self.session = Session()
        logger.info(f"Start session to game server at {SERVER_URL}")

    @check_status
    def load_map(self, x: int, y: int, chunk_size: int) -> Response:
        args = {
            "x": x,
            "y": y,
            "chunk_size": chunk_size,
            "token": self.token,
            "client_id": self.client_id,
        }
        return self.session.get(SERVER_URL + "/map", params=args)

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
        response = self.session.post(SERVER_URL + "/move", params=args)
        return response

    @check_status
    def me(self) -> Response:
        args = {"token": self.token}
        return self.session.get(SERVER_URL + "/me", params=args)
