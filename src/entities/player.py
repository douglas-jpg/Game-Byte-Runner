import glm
import math
from core import constants as const

class Player:

    def __init__(self):
        # configuracao visual
        self.SCALE = 0.3
        self.MODEL_OFFSET_Y = -0.23
        self.ANIMATION_SPEED = 15.0
        self.RUN_BOUNCE_HEIGHT = 0.05
        self.RUN_ROTATION_STRENGTH = 3.0

        # configuracao de colisao
        self.EXTENT_X = 0.15
        self.EXTENT_Y = 0.25
        self.EXTENT_Z = 0.15

        self._init_state()

    def _init_state(self):
        self.lane_index = 1
        self.target_x = const.LANE_POSITIONS[1]

        self.position = glm.vec3(
            self.target_x, const.PLAYER_BASE_Y, const.PLAYER_Z)

        self.y_velocity = 0.0
        self.is_jumping = False

        self.is_dead = False
        self.coins = 0
        self.magnet_timer = 0.0

        self.run_animation_time = 0.0

    def update(self, delta_time: float):
        if self.is_dead:
            return

        self._apply_gravity(delta_time)
        self._apply_strafe(delta_time)
        self._update_animation(delta_time)
        self._update_magnet(delta_time)

    def _apply_gravity(self, delta_time):
        if self.is_jumping:
            self.y_velocity += const.GRAVITY * delta_time
            self.position.y += self.y_velocity * delta_time

            if self.position.y < const.PLAYER_BASE_Y:
                self.position.y = const.PLAYER_BASE_Y
                self.is_jumping = False
                self.y_velocity = 0.0

    def _apply_strafe(self, delta_time):
        self.target_x = const.LANE_POSITIONS[self.lane_index]
        diff = self.target_x - self.position.x
        self.position.x += diff * const.STRAFE_SPEED * delta_time

    def _update_animation(self, delta_time):
        if not self.is_jumping:
            self.run_animation_time += delta_time * self.ANIMATION_SPEED

    def _update_magnet(self, delta_time):
        if self.magnet_timer > 0.0:
            self.magnet_timer = max(0.0, self.magnet_timer - delta_time)

    def move_left(self):
        if not self.is_dead and self.lane_index > 0:
            self.lane_index -= 1

    def move_right(self):
        if not self.is_dead and self.lane_index < 2:
            self.lane_index += 1

    def jump(self):
        if not self.is_dead and not self.is_jumping:
            self.is_jumping = True
            self.y_velocity = const.JUMP_STRENGTH

    def land_on_obstacle(self, obstacle_top_y):
        self.position.y = obstacle_top_y - self.MODEL_OFFSET_Y
        self.y_velocity = 0.0
        self.is_jumping = False

    def die(self):
        self.is_dead = True

    def activate_magnet(self):
        self.magnet_timer = const.MAGNET_DURATION

    def reset(self):
        self._init_state()

    def get_aabb(self):
        return (
            self.position.x - self.EXTENT_X, self.position.x + self.EXTENT_X,
            self.position.y - self.EXTENT_Y, self.position.y + self.EXTENT_Y,
            self.position.z - self.EXTENT_Z, self.position.z + self.EXTENT_Z
        )

    def get_model_matrix(self):
        visual_y = self.position.y + self.MODEL_OFFSET_Y
        rotation_z = 0.0
        death_rotation_x = 0.0

        if self.is_dead:
            visual_y -= 0.2
            death_rotation_x = -90.0
        elif not self.is_jumping:
            visual_y += abs(math.sin(self.run_animation_time)
                            ) * self.RUN_BOUNCE_HEIGHT
            rotation_z = math.cos(self.run_animation_time) * \
                self.RUN_ROTATION_STRENGTH

        # construcao da matriz
        mat_trans = glm.translate(glm.mat4(1.0), glm.vec3(
            self.position.x, visual_y, self.position.z))

        # rotacoes
        mat_rot_base = glm.rotate(
            glm.mat4(1.0), glm.radians(180), glm.vec3(0.0, 1.0, 0.0))
        mat_rot_anim = glm.rotate(glm.mat4(1.0), glm.radians(
            rotation_z), glm.vec3(0.0, 0.0, 1.0))
        mat_rot_death = glm.rotate(glm.mat4(1.0), glm.radians(
            death_rotation_x), glm.vec3(1.0, 0.0, 0.0))

        mat_scale = glm.scale(glm.mat4(1.0), glm.vec3(self.SCALE))

        return mat_trans * mat_rot_base * mat_rot_death * mat_rot_anim * mat_scale
