import glm
import math
from OpenGL.GL import *
from core import constants as const
from core import Mesh, load_obj
from graphics import load_texture


class Creeper:
    def __init__(self):
        self.SCALE = 0.3
        self.VISUAL_Y_OFFSET = -0.3
        self.BOUNCE_HEIGHT = 0.05
        self.ROTATION_SPEED = 3.0
        self.DELAY_SECONDS = 0.15
        self.HISTORY_RETENTION = 2.0
        self.LERP_SPEED_X = 10.0
        self.LERP_SPEED_Y = 15.0
        self.ANIMATION_SPEED = 15.0

        self._init_resources()
        self._init_state()

    def _init_resources(self):
        model_path = "src/assets/models/creeper/creeper.obj"
        texture_path = "src/assets/textures/creeper/creeper.png"

        vertices_data = load_obj(model_path)
        vertex_count = len(vertices_data) // 8

        self.mesh = Mesh(vertices_data, vertex_count, has_texture=True)
        self.texture_id = load_texture(texture_path)

    def _init_state(self):
        # estado inicial
        self.position = glm.vec3(0.0, const.PLAYER_BASE_Y, const.CREEPER_Z)
        self.timer = 0.0
        self.run_animation_time = 0.0

        self.position_history = []

    def update(self, delta_time: float, player_x: float, player_y: float):
        self.timer += delta_time
        self.run_animation_time += delta_time * self.ANIMATION_SPEED

        self._update_history(player_x, player_y)
        target_x, target_y = self._get_delayed_target(player_x, player_y)

        self._apply_movement(target_x, target_y, delta_time)

    def _update_history(self, p_x, p_y):
        self.position_history.append((self.timer, p_x, p_y))
        cutoff_time = self.timer - self.HISTORY_RETENTION
        self.position_history = [
            p for p in self.position_history if p[0] > cutoff_time]

    def _get_delayed_target(self, current_x, current_y):
        target_time = self.timer - self.DELAY_SECONDS

        # procura a posição que o player estava
        for t, h_x, h_y in self.position_history:
            if t >= target_time:
                return h_x, h_y

        return current_x, current_y

    def _apply_movement(self, target_x, target_y, delta_time):
        self.position.x += (target_x - self.position.x) * \
            self.LERP_SPEED_X * delta_time
        self.position.y += (target_y - self.position.y) * \
            self.LERP_SPEED_Y * delta_time

    def draw(self, shader_program):
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)

        model_matrix = self._compute_model_matrix()

        loc_model = glGetUniformLocation(shader_program, "model")
        glUniformMatrix4fv(loc_model, 1, GL_FALSE, glm.value_ptr(model_matrix))

        glBindVertexArray(self.mesh.vao)
        glDrawArrays(GL_TRIANGLES, 0, self.mesh.vertices_count)
        glBindVertexArray(0)

    def _compute_model_matrix(self):
        visual_y = self.position.y + self.VISUAL_Y_OFFSET

        if self.position.y < const.PLAYER_BASE_Y + 0.1:
            visual_y += abs(math.sin(self.run_animation_time)
                            ) * self.BOUNCE_HEIGHT

        rotation_z = math.cos(self.run_animation_time) * self.ROTATION_SPEED

        # construção da Matriz
        mat_transform = glm.translate(glm.mat4(1.0), glm.vec3(
            self.position.x, visual_y, self.position.z))
        mat_rotation_y = glm.rotate(
            glm.mat4(1.0), glm.radians(180), glm.vec3(0.0, 1.0, 0.0))
        mat_anim_rot = glm.rotate(glm.mat4(1.0), glm.radians(
            rotation_z), glm.vec3(0.0, 0.0, 1.0))
        mat_scale = glm.scale(glm.mat4(1.0), glm.vec3(self.SCALE))

        return mat_transform * mat_rotation_y * mat_anim_rot * mat_scale

    def cleanup(self):
        if hasattr(self, 'mesh'):
            glDeleteVertexArrays(1, [self.mesh.vao])
            glDeleteBuffers(1, [self.mesh.vbo])
        if hasattr(self, 'texture_id'):
            glDeleteTextures(1, [self.texture_id])
