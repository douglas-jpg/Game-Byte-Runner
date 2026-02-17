from OpenGL.GL import *
import ctypes
import numpy as np

class Mesh:
    def __init__(self, vertices_data, vertices_count, has_texture=False):
        self.FLOAT_BYTE_SIZE = 4

        self.vertices_count = vertices_count
        vertices = np.array(vertices_data, dtype=np.float32)

        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)

        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(
            GL_ARRAY_BUFFER,
            vertices.nbytes,
            vertices,
            GL_STATIC_DRAW
        )

        self._configure_attributes(has_texture)
        
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def _configure_attributes(self, has_texture):
        if has_texture:
            stride = 8 * self.FLOAT_BYTE_SIZE
            attr_config = {"size": 2, "index": 1}
        else:
            stride = 9 * self.FLOAT_BYTE_SIZE
            attr_config = {"size": 3, "index": 1}

        self._enable_attribute(0, 3, stride, 0)

        self._enable_attribute(2, 3, stride, 3 * self.FLOAT_BYTE_SIZE)

        self._enable_attribute(
            attr_config["index"],
            attr_config["size"],
            stride,
            6 * self.FLOAT_BYTE_SIZE
        )

    def _enable_attribute(self, location, size, stride, offset):
        glVertexAttribPointer(
            location, size, GL_FLOAT, GL_FALSE,
            stride, ctypes.c_void_p(offset)
        )
        glEnableVertexAttribArray(location)

    def draw(self):
        glBindVertexArray(self.vao)
        glDrawArrays(GL_TRIANGLES, 0, self.vertices_count)
        glBindVertexArray(0)

    def cleanup(self):
        if hasattr(self, 'vao'):
            glDeleteVertexArrays(1, [self.vao])
        if hasattr(self, 'vbo'):
            glDeleteBuffers(1, [self.vbo])
