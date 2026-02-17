import glfw
from OpenGL.GL import *
import random
import glm
import pygame

from core import Mesh, load_obj
from core import constants as const
from entities import Player, Coin, Creeper, Magnet, Obstacle
from graphics import load_shader_program, load_texture


class Game:
    def __init__(self):
        self.width = const.WIDTH
        self.height = const.HEIGHT

        self.window = self._init_window()
        self._init_audio()
        self._init_assets()
        self._init_game_entities()
        self._init_game_state()

    def _init_window(self):
        glfw.init()
        window = glfw.create_window(
            self.width, self.height, "Byte Runner", None, None)
        glfw.make_context_current(window)
        glfw.set_framebuffer_size_callback(window, self.update_window_size)
        glfw.set_key_callback(window, self.keyboard)
        glEnable(GL_DEPTH_TEST)
        return window

    def _init_audio(self):
        # inicia os audios do jogo
        pygame.mixer.init()
        self.sfx_coin = pygame.mixer.Sound("src/assets/sounds/coin.mp3")
        self.sfx_game_over = pygame.mixer.Sound(
            "src/assets/sounds/game_over.mp3")

        self.sfx_coin.set_volume(0.1)
        self.sfx_game_over.set_volume(0.5)

        pygame.mixer.music.load("src/assets/sounds/music.mp3")
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)

    def _init_assets(self):
        self.textures = {
            "road": load_texture("src/assets/textures/road/road.png"),
            "separator": load_texture("src/assets/textures/road/separator.jpg"),
            "floor": load_texture("src/assets/textures/background/floor.png"),
            "wall": load_texture("src/assets/textures/background/wall.png"),
            "metal": load_texture("src/assets/textures/obstacle/body.jpg"),
            "gold": load_texture("src/assets/textures/coin/gold.png"),
            "player": load_texture("src/assets/textures/player/player.jpg")
        }

        self.shader_texture = load_shader_program(
            "src/assets/shaders/vertexShader.glsl", "src/assets/shaders/fragmentShader.glsl")
        glUseProgram(self.shader_texture)

        self.uniforms_texture = {
            "model": glGetUniformLocation(self.shader_texture, "model"),
            "view": glGetUniformLocation(self.shader_texture, "view"),
            "proj": glGetUniformLocation(self.shader_texture, "projection"),
            "uv_offset": glGetUniformLocation(self.shader_texture, "uvOffset"),
            "light_pos": glGetUniformLocation(self.shader_texture, "lightPos"),
            "light_color": glGetUniformLocation(self.shader_texture, "lightColor"),
            "view_pos": glGetUniformLocation(self.shader_texture, "viewPos"),
        }

        self.shader_color = load_shader_program(
            "src/assets/shaders/colorVertex.glsl", "src/assets/shaders/colorFragment.glsl"
        )
        glUseProgram(self.shader_color)

        self.uniforms_color = {
            "model": glGetUniformLocation(self.shader_color, "model"),
            "view": glGetUniformLocation(self.shader_color, "view"),
            "proj": glGetUniformLocation(self.shader_color, "projection"),
            "light_pos": glGetUniformLocation(self.shader_color, "lightPos"),
            "light_color": glGetUniformLocation(self.shader_color, "lightColor"),
            "view_pos": glGetUniformLocation(self.shader_color, "viewPos"),
        }

    def _init_game_entities(self):
        self.meshes = {
            "lane_left": Mesh(const.LANE_LEFT_VERTICES, 6, has_texture=True),
            "lane_center": Mesh(const.LANE_CENTER_VERTICES, 6, has_texture=True),
            "lane_right": Mesh(const.LANE_RIGHT_VERTICES, 6, has_texture=True),
            "separator": Mesh(const.SEPARATOR_VERTICES, 12, has_texture=True),
            "floor": Mesh(const.FLOOR_VERTICES, 18, has_texture=True),
            "walls": Mesh(const.WALL_VERTICES, 12, has_texture=True),
            "ceiling": Mesh(const.CEILING_VERTICES, 6, has_texture=True),
            "obs_body": Mesh(const.OBSTACLE_BODY_VERTICES, len(const.OBSTACLE_BODY_VERTICES), has_texture=True),
            "obs_legs": Mesh(const.OBSTACLE_LEGS_VERTICES, len(const.OBSTACLE_LEGS_VERTICES), has_texture=True),
            "magnet": Mesh(const.MAGNET_VERTICES, len(const.MAGNET_VERTICES), has_texture=False),
            "coin": Mesh(const.COIN_VERTICES, 36, has_texture=True)
        }

        # carregamento do Player
        steve_data = load_obj(
            "src/assets/models/player/steve.obj")
        self.player_mesh = Mesh(steve_data, len(steve_data), has_texture=True)

        self.player = Player()
        self.creeper = Creeper()

    def _init_game_state(self):
        self.camera_pos = glm.vec3(0.0, 2.5, 3.0)
        self.camera_target = glm.vec3(0.0, 0.0, -10.0)
        self.world_up = glm.vec3(0.0, 1.0, 0.0)

        self.is_game_over = False
        self.jump_buffer = 0.0
        self.current_speed = const.OBSTACLE_SPEED
        self.track_offset = 0.0
        self.last_frame_time = glfw.get_time()

        self.active_obstacles = []
        self.active_coins = []
        self.active_magnets = []

        self._spawn_initial_obstacles()
        self._spawn_initial_coins()

    def run(self):
        while not glfw.window_should_close(self.window):
            current_time = glfw.get_time()
            delta_time = current_time - self.last_frame_time
            self.last_frame_time = current_time

            glfw.poll_events()
            self._process_system_input()

            self.update(delta_time)
            self.render()

            glfw.swap_buffers(self.window)

        self.cleanup()

    def update(self, delta_time):
        if self.is_game_over:
            return

        if self.current_speed < const.MAX_SPEED:
            self.current_speed += const.SPEED_INCREMENT * delta_time

        self.track_offset = (self.track_offset +
                             const.OBSTACLE_SPEED * delta_time * 0.1) % 100.0

        if self.jump_buffer > 0:
            self.jump_buffer -= delta_time

        self.player.update(delta_time)
        self.creeper.update(
            delta_time, self.player.position.x, self.player.position.y)

        self._update_obstacles(delta_time)
        self._update_magnets(delta_time)
        self._update_coins(delta_time)
        self._check_grounded_status()

    def _update_obstacles(self, delta_time):
        new_obstacles = []
        player_aabb = self.player.get_aabb()

        for obstacle in self.active_obstacles:
            obstacle.update(delta_time, self.current_speed)

            if self.check_aabb_collision(player_aabb, obstacle.get_aabb()):
                self._handle_obstacle_collision(obstacle, player_aabb)
                if self.is_game_over:
                    return

            if obstacle.is_out_of_bounds():
                new_obstacles.append(self.create_obstacle())
            else:
                new_obstacles.append(obstacle)

        if not self.active_obstacles and not new_obstacles:
            self._spawn_initial_obstacles()

        self.active_obstacles = new_obstacles

    def _handle_obstacle_collision(self, obstacle, player_aabb):
        feet_y = player_aabb[2]
        top_obstacle_y = obstacle.position.y + (obstacle.size.y / 2.0)

        is_above = feet_y >= (top_obstacle_y - 0.3)
        is_falling = self.player.y_velocity <= 0

        if is_above and is_falling:
            self.player.land_on_obstacle(top_obstacle_y)
            if self.jump_buffer > 0:
                self.player.jump()
                self.jump_buffer = 0.0
        else:
            self.trigger_game_over()

    def _check_grounded_status(self):
        if self.player.position.y > const.PLAYER_BASE_Y and not self.player.is_jumping:
            pass

            if self.player.position.y > const.PLAYER_BASE_Y + 0.1:
                self.player.is_jumping = True

    def render(self):
        if self.is_game_over:
            glClearColor(0.2, 0.0, 0.0, 1.0)
        else:
            glClearColor(0.0, 0.1, 0.05, 1.0)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        light_pos = glm.vec3(0.0, 10.0, 2.0)
        light_color = glm.vec3(1.0, 1.0, 1.0)

        #  camera
        view_matrix = glm.lookAt(
            self.camera_pos, self.camera_target, self.world_up)
        aspect_ratio = self.width / self.height if self.height > 0 else 1.0
        projection_matrix = glm.perspective(glm.radians(
            45.0), aspect_ratio, 0.1, const.LANE_LENGTH + 10.0)

        glUseProgram(self.shader_texture)

        glUniformMatrix4fv(self.uniforms_texture["view"], 1, GL_FALSE,
                           glm.value_ptr(view_matrix))
        glUniformMatrix4fv(self.uniforms_texture["proj"], 1, GL_FALSE,
                           glm.value_ptr(projection_matrix))

        # iluminacao
        glUniform3fv(
            self.uniforms_texture["light_pos"], 1, glm.value_ptr(light_pos))
        glUniform3fv(
            self.uniforms_texture["light_color"], 1, glm.value_ptr(light_color))
        glUniform3fv(
            self.uniforms_texture["view_pos"], 1, glm.value_ptr(self.camera_pos))

        identity_matrix = glm.mat4(1.0)
        glUniformMatrix4fv(self.uniforms_texture['model'], 1, GL_FALSE,
                           glm.value_ptr(identity_matrix))

        glActiveTexture(GL_TEXTURE0)

        glUniform2f(self.uniforms_texture["uv_offset"], 0.0, self.track_offset)
        # cao
        glBindTexture(GL_TEXTURE_2D, self.textures["floor"])
        self.meshes["floor"].draw()

        glBindTexture(GL_TEXTURE_2D, self.textures["wall"])
        self.meshes["ceiling"].draw()

        # pistas
        glBindTexture(GL_TEXTURE_2D, self.textures["road"])  # ou texture_chip1
        self.meshes["lane_left"].draw()
        self.meshes["lane_center"].draw()
        self.meshes["lane_right"].draw()

        # separadores
        glBindTexture(GL_TEXTURE_2D, self.textures["separator"])
        self.meshes["separator"].draw()

        # paredes
        glUniform2f(self.uniforms_texture["uv_offset"], self.track_offset, 0.0)
        glBindTexture(GL_TEXTURE_2D, self.textures["wall"])
        self.meshes["walls"].draw()
        glUniform2f(self.uniforms_texture["uv_offset"], 0.0, 0.0)

        # obstaculos
        glBindTexture(GL_TEXTURE_2D, self.textures["metal"])
        for obstacle in self.active_obstacles:
            model = obstacle.get_model_matrix()
            glUniformMatrix4fv(self.uniforms_texture['model'], 1,
                               GL_FALSE, glm.value_ptr(model))
            self.meshes["obs_body"].draw()
        glBindTexture(GL_TEXTURE_2D, self.textures["gold"])
        for obstacle in self.active_obstacles:
            model = obstacle.get_model_matrix()
            glUniformMatrix4fv(self.uniforms_texture['model'], 1,
                               GL_FALSE, glm.value_ptr(model))
            self.meshes["obs_legs"].draw()

        # oedas
        glBindTexture(GL_TEXTURE_2D, self.textures["gold"])
        for coin in self.active_coins:
            model = coin.get_model_matrix()
            glUniformMatrix4fv(self.uniforms_texture['model'], 1,
                               GL_FALSE, glm.value_ptr(model))
            self.meshes["coin"].draw()

        # player
        glBindTexture(GL_TEXTURE_2D, self.textures["player"])
        model = self.player.get_model_matrix()
        glUniformMatrix4fv(self.uniforms_texture['model'], 1,
                           GL_FALSE, glm.value_ptr(model))
        self.player_mesh.draw()

        self.creeper.draw(self.shader_texture)

        glUseProgram(self.shader_color)

        glUniformMatrix4fv(self.uniforms_color["view"], 1, GL_FALSE,
                           glm.value_ptr(view_matrix))
        glUniformMatrix4fv(self.uniforms_color["proj"], 1, GL_FALSE,
                           glm.value_ptr(projection_matrix))

        glUniform3fv(
            self.uniforms_color["light_pos"], 1, glm.value_ptr(light_pos))
        glUniform3fv(
            self.uniforms_color["light_color"], 1, glm.value_ptr(light_color))
        glUniform3fv(self.uniforms_color["view_pos"],
                     1, glm.value_ptr(self.camera_pos))

        glUniformMatrix4fv(self.uniforms_color["model"], 1, GL_FALSE,
                           glm.value_ptr(glm.mat4(1.0)))

        glUniformMatrix4fv(self.uniforms_color["model"], 1,
                           GL_FALSE, glm.value_ptr(model))

        glUniform3f(self.uniforms_color["light_color"], 1.0,
                    0.6, 0.0)
        self.player_mesh.draw()
        glUniform3f(self.uniforms_color["light_color"], 1.0,
                    1.0, 1.0)

        # ima
        for magnet in self.active_magnets:
            model = magnet.get_model_matrix()
            glUniformMatrix4fv(self.uniforms_color["model"], 1,
                               GL_FALSE, glm.value_ptr(model))
            self.meshes["magnet"].draw()

    def _update_magnets(self, delta_time):
        player_aabb = self.player.get_aabb()
        new_magnets = []

        for magnet in self.active_magnets:
            magnet.update(delta_time, self.current_speed)

            if not magnet.collected and self.check_aabb_collision(player_aabb, magnet.get_aabb()):
                magnet.collected = True
                self.player.activate_magnet()
                self.sfx_coin.play()
                continue

            if not magnet.is_out_of_bounds():
                new_magnets.append(magnet)
        self.active_magnets = new_magnets

    def _update_coins(self, delta_time):
        player_aabb = self.player.get_aabb()
        new_coins = []
        magnet_active = self.player.magnet_timer > 0

        for coin in self.active_coins:
            if coin.collected:
                continue

            # atracao do ima
            direction = self.player.position - coin.position
            dist = glm.length(direction)
            should_attract = magnet_active and (dist < const.MAGNET_RADIUS)

            if should_attract:
                if dist < 1.0:
                    self.collect_coin(coin)
                    continue

                direction = glm.normalize(direction)
                move_speed = const.MAGNET_SPEED_ATTRACTION + self.current_speed
                coin.position += direction * move_speed * delta_time
            else:
                coin.update(delta_time, self.current_speed)
                if self.check_aabb_collision(player_aabb, coin.get_aabb()):
                    self.collect_coin(coin)
                    continue

            if not coin.is_out_of_bounds():
                new_coins.append(coin)

        self.active_coins = new_coins
        self._check_spawn_new_coin_group()

    def create_obstacle(self, is_initial=False, z_start=None):
        x = random.choice(const.LANE_POSITIONS)
        z = const.CREATE_Z

        if is_initial:
            limit_near = z_start if z_start else (const.Z_NEAR - 40.0)
            z = random.uniform(const.CREATE_Z, limit_near)

        h = random.uniform(const.OBSTACLE_MIN_HEIGHT,
                           const.OBSTACLE_MAX_HEIGHT)
        d = random.uniform(const.OBSTACLE_MIN_DEPTH, const.OBSTACLE_MAX_DEPTH)
        return Obstacle(x, z, const.OBSTACLE_WIDTH, h, d)

    def _spawn_initial_obstacles(self):
        self.active_obstacles = []
        safe_z_start = const.Z_NEAR - 40.0
        count = 0

        # loop para evitar infinito
        for _ in range(const.MAX_OBSTACLES * 5):
            if count >= const.MAX_OBSTACLES:
                break

            new_obs = self.create_obstacle(
                is_initial=True, z_start=safe_z_start)
            if not self._check_obstacle_overlap(new_obs):
                self.active_obstacles.append(new_obs)
                count += 1

    def _check_obstacle_overlap(self, new_obs):
        margin = 5.0
        for existing in self.active_obstacles:
            if abs(new_obs.position.x - existing.position.x) < 0.5:
                # verifica distancia Z
                dist_z = abs(new_obs.position.z - existing.position.z)
                if dist_z < (new_obs.size.z + existing.size.z + margin):
                    return True
        return False

    def _spawn_initial_coins(self):
        z_cursor = const.Z_NEAR - 10.0
        while z_cursor > const.CREATE_Z:
            self._spawn_coin_group(z_cursor)
            z_cursor -= const.GROUP_DISTANCE

    def _spawn_coin_group(self, z_start):
        # spawnar ima
        if random.random() < 0.15:
            magnet_lane = random.choice(const.LANE_POSITIONS)
            if not self._check_spawn_overlap(magnet_lane, z_start):
                self.active_magnets.append(Magnet(magnet_lane, z_start))
                z_start -= 5.0

        # spawna moedas
        lane_x = random.choice(const.LANE_POSITIONS)
        num_coins = random.randint(const.GROUP_MIN_SIZE, const.GROUP_MAX_SIZE)
        for i in range(num_coins):
            z = z_start - (i * const.COIN_GAP)
            if not self._check_spawn_overlap(lane_x, z):
                self.active_coins.append(Coin(lane_x, z))

    def _check_spawn_new_coin_group(self):
        should_spawn = False
        if not self.active_coins:
            should_spawn = True
        elif self.active_coins[-1].position.z > (const.CREATE_Z + const.GROUP_DISTANCE):
            should_spawn = True

        if should_spawn and len(self.active_coins) < 100:
            self._spawn_coin_group(const.CREATE_Z)

    def _check_spawn_overlap(self, x, z, margin=2.0):
        # cria uma box para checar colisão no ponto de spawn
        check_min_z = z - 0.5 - margin
        check_max_z = z + 0.5 + margin

        for obs in self.active_obstacles:
            aabb = obs.get_aabb()

            if x > (aabb[0] - 0.5) and x < (aabb[1] + 0.5):
                if check_max_z > aabb[4] and check_min_z < aabb[5]:
                    return True
        return False

    def collect_coin(self, coin):
        coin.collected = True
        self.player.coins += 1
        self.sfx_coin.play()

    def trigger_game_over(self):
        self.player.die()
        self.sfx_game_over.play()
        pygame.mixer.music.stop()
        self.is_game_over = True

    def reset_game(self):
        self.player.reset()
        self.active_obstacles.clear()
        self.active_coins.clear()
        self.active_magnets.clear()

        self._spawn_initial_obstacles()
        self._spawn_initial_coins()
        self.current_speed = const.OBSTACLE_SPEED
        self.is_game_over = False

        pygame.mixer.music.play(-1)

    def check_aabb_collision(self, box1, box2):
        return (box1[0] < box2[1] and box1[1] > box2[0] and
                box1[2] < box2[3] and box1[3] > box2[2] and
                box1[4] < box2[5] and box1[5] > box2[4])

    def _process_system_input(self):
        if glfw.get_key(self.window, glfw.KEY_ESCAPE) == glfw.PRESS:
            glfw.set_window_should_close(self.window, True)

    def keyboard(self, window, key, scancode, action, mods):
        if action != glfw.PRESS:
            return

        if self.is_game_over:
            if key == glfw.KEY_SPACE:
                self.reset_game()
            return

        if key == glfw.KEY_LEFT or key == glfw.KEY_A:
            self.player.move_left()
        elif key == glfw.KEY_RIGHT or key == glfw.KEY_D:
            self.player.move_right()
        elif key == glfw.KEY_SPACE or key == glfw.KEY_W:
            if not self.player.is_jumping:
                self.player.jump()
            else:
                self.jump_buffer = 0.2

    def update_window_size(self, window, width, height):
        self.width, self.height = width, height
        glViewport(0, 0, width, height)

    def cleanup(self):
        for mesh in self.meshes.values():
            mesh.cleanup()
        self.player_mesh.cleanup()
        self.creeper.cleanup()
        glDeleteProgram(self.shader_texture)
        glDeleteProgram(self.shader_color)
        pygame.mixer.quit()
        glfw.terminate()
