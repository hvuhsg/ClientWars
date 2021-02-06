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
    _updated_at: Union[datetime, None] = None

    def __getitem__(self, item):
        return getattr(self, item)

    @property
    def power(self):
        if self.owner is None:
            return self._power
        return self._power + (datetime.now() - self._updated_at) // NEW_POWER_RATE

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

    @classmethod
    def from_dict(cls, dictt):
        dictt["_power"] = dictt["power"]
        if "updated_at" in dictt:
            dictt["_updated_at"] = datetime.fromtimestamp(dictt["updated_at"])
            dictt.pop("updated_at")
        dictt.pop("power")
        return cls(**dictt)

    @classmethod
    def from_dicts_to_tiles(cls, dicts):
        return [cls.from_dict(item) for item in dicts]
