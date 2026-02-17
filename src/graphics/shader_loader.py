from OpenGL.GL import *
from OpenGL.GL import shaders


def load_shader_program(vertex_path: str, fragment_path: str) -> int:
    vert_shader = _compile_shader_from_file(vertex_path, GL_VERTEX_SHADER)
    frag_shader = _compile_shader_from_file(fragment_path, GL_FRAGMENT_SHADER)

    program = shaders.compileProgram(vert_shader, frag_shader)

    # limpeza
    glDeleteShader(vert_shader)
    glDeleteShader(frag_shader)

    return program


def _compile_shader_from_file(filepath: str, shader_type: int):
    with open(filepath, 'r') as f:
        source_code = f.read()

    return shaders.compileShader(source_code, shader_type)
