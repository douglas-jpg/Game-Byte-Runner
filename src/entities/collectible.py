import glm
from core import constants as const


class Collectible:
    def __init__(self, x: float, y: float, z: float, size: float, scale_vec=None, collision_factor=0.5):
        self.position = glm.vec3(x, y, z)
        self.size = size
        self.collected = False
        self.collision_factor = collision_factor

        if scale_vec is None:
            final_scale = glm.vec3(size)
        else:
            final_scale = scale_vec

        self.scale_matrix = glm.scale(glm.mat4(1.0), final_scale)

    def update(self, delta_time: float, current_speed: float):
        self.position.z += current_speed * delta_time

    def is_out_of_bounds(self) -> bool:
        return self.position.z > const.UNCREATE_Z

    def get_aabb(self):
        radius = self.size * self.collision_factor
        return (
            self.position.x - radius, self.position.x + radius,
            self.position.y - radius, self.position.y + radius,
            self.position.z - radius, self.position.z + radius
        )

    def get_model_matrix(self):
        translate_matrix = glm.translate(glm.mat4(1.0), self.position)
        return translate_matrix * self.scale_matrix
