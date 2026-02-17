from OpenGL.GL import *
from PIL import Image

def load_texture(path: str) -> int:
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    # configuracao de repetição e filtro
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,
                    GL_LINEAR_MIPMAP_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    # processamento da imagem
    img = Image.open(path).transpose(Image.FLIP_TOP_BOTTOM).convert("RGBA")

    width, height = img.size
    img_data = img.tobytes()

    glTexImage2D(
        GL_TEXTURE_2D, 0, GL_RGBA, width, height,
        0, GL_RGBA, GL_UNSIGNED_BYTE, img_data
    )
    glGenerateMipmap(GL_TEXTURE_2D)

    return texture_id
