import glm
from core import constants as const
from .collectible import Collectible


class Magnet(Collectible):
    def __init__(self, x: float, z: float):
        super().__init__(
            x=x,
            y=const.COIN_Y,
            z=z,
            size=const.MAGNET_SIZE,
            scale_vec=glm.vec3(1.0),
            collision_factor=0.5
        )
