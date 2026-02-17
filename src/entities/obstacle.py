import glm
from core import constants as const


class Obstacle:
    def __init__(self, x: float, z: float, width: float, height: float, depth: float):
        start_y = height / 3.0

        self.position = glm.vec3(x, start_y, z)
        self.size = glm.vec3(width, height, depth)

        self.scale_matrix = glm.scale(glm.mat4(1.0), self.size)

    def update(self, delta_time: float, current_speed: float):
        self.position.z += current_speed * delta_time

    def is_out_of_bounds(self) -> bool:
        return self.position.z > const.UNCREATE_Z

    def get_model_matrix(self):
        translate_matrix = glm.translate(glm.mat4(1.0), self.position)
        return translate_matrix * self.scale_matrix

    def get_aabb(self):
        half_size = self.size / 2.0
        min_point = self.position - half_size
        max_point = self.position + half_size

        return (
            min_point.x, max_point.x,
            min_point.y, max_point.y,
            min_point.z, max_point.z
        )
