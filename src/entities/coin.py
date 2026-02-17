from core import constants as const
from .collectible import Collectible


class Coin(Collectible):
    def __init__(self, x: float, z: float):
        super().__init__(
            x=x,
            y=const.COIN_Y,
            z=z,
            size=const.COIN_SIZE,
            scale_vec=None,
            collision_factor=0.8
        )
