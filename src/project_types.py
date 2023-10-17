from enum import Enum

type Tile = int
type Action = (ActionType, Tile)


class ActionType(Enum):
    NONE = 1
    TAKE_TILE = 2
    STEAL_TILE = 3
