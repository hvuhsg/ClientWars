from typing import Union
from dataclasses import dataclass
from datetime import datetime

from config import NEW_POWER_RATE


@dataclass(frozen=True)
class Tile:
    x: int
    y: int
    _power: int
    owner: Union[None, str]
    downloaded_at: datetime = datetime.now()

    def __getitem__(self, item):
        return getattr(self, item)

    @property
    def power(self):
        if self.owner is None:
            return self._power
        return self._power + (datetime.now() - self.downloaded_at) // NEW_POWER_RATE

    def coordinates(self) -> str:
        return self.x, self.y

    def left(self):
        return self.x - 1, self.y

    def right(self):
        return self.x + 1, self.y

    def up(self):
        return self.x, self.y + 1

    def down(self):
        return self.x, self.y - 1

    @classmethod
    def from_dict(cls, dictt):
        dictt["_power"] = dictt["power"]
        dictt.pop("power")
        return cls(**dictt)

    @classmethod
    def from_dicts_to_tiles(cls, dicts):
        return [cls.from_dict(item) for item in dicts]

    def __eq__(self, other):
        return self.power == other.power

    def __gt__(self, other):
        return self.power > other.power

    def __hash__(self):
        return hash((self.x, self.y, self.power, "Tile"))

    def __str__(self):
        return f"{self.__class__.__name__}(x={self.x}, y={self.y}, power={self.power}, owner={self.owner})"

    def __repr__(self):
        return str(self)
