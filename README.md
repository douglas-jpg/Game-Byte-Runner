# 🎮 Game-Byte-Runner

> Um jogo runner em 3D desenvolvido com **PyOpenGL** como implementação prática dos princípios de Computação Gráfica.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![PyOpenGL](https://img.shields.io/badge/PyOpenGL-3.1.10-green.svg)](https://pyopengl.sourceforge.net/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 Descrição do Projeto

**Game-Byte-Runner** é um jogo tipo runner infinito onde o jogador controla um personagem que corre por uma pista em constante movimento. O objetivo é desviar de obstáculos, coletar moedas e sobreviver o máximo de tempo possível.

O projeto foi desenvolvido como trabalho acadêmico para demonstrar a aplicação de conceitos fundamentais de **Computação Gráfica**, como:

- `Rendering 3D` com matrizes de transformação
- `Shaders` customizados (vertex e fragment)
- `Texturas` e mapeamento UV
- `Iluminação` (modelo Phong)
- `Detecção de colisão` com bounding boxes
- `Transformações geométricas` (translação, rotação, escala)

---

## ✨ Recursos

✅ **Mecânicas do Jogo:**
- Movimento lateral em 3 pistas
- Sistema de pulo com física realista (gravidade)
- Obstáculos dinâmicos com variações de altura
- Coleta de moedas em grupos
- Ímã modificador que atrai moedas próximas
- Inimigo (Creeper) que persegue o jogador
- Sistema de pontuação

✅ **Gráficos:**
- Renderização 3D com perspectiva
- Texturas para todos os elementos
- Iluminação dinâmica
- Efeitos visuais de animação
- Câmera fixa acompanhando o jogador

✅ **Áudio:**
- Música de fundo em loop
- Efeito sonoro ao coletar moedas
- Efeito sonoro de game over

---

## 🛠️ Requisitos do Sistema

- **Python** 3.8 ou superior
- **pip** (gerenciador de pacotes Python)
- Placa gráfica com suporte a **OpenGL 3.0+**
- **Windows, macOS ou Linux**

### Dependências do Projeto

```
glfw==2.10.0              # Janelas e entrada do usuário
numpy==2.3.5              # Operações matemáticas
pillow==12.1.0            # Carregamento de imagens
pygame==2.6.1             # Áudio
pyglm==2.8.3              # Matemática linear (matrizes e vetores)
PyOpenGL==3.1.10          # Bindings de OpenGL
PyOpenGL-accelerate==3.1.10  # Otimizações de performance
readchar==4.2.1           # Leitura de entrada do teclado
```

---

## 📦 Instalação

### Passo 1: Clonar o Repositório

```bash
git clone https://github.com/douglas-jpg/Game-Byte-Runner.git
cd Game-Byte-Runner
```

### Passo 2: Criar um Ambiente Virtual (Recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### Passo 3: Instalar as Dependências

```bash
pip install -r requirements.txt
```

### Passo 4: Verificar a Instalação

Para verificar se tudo foi instalado corretamente:

```bash
python -c "import OpenGL; print('OpenGL OK')"
python -c "import glfw; print('GLFW OK')" 
python -c "import glm; print('GLM OK')"
```

---

## 🚀 Como Executar

```bash
python src/main.py
```

A janela do jogo abrirá automaticamente. O jogo é iniciado e o jogador pode começar a jogar imediatamente!

---

## 🎮 Controles do Jogo

| Tecla | Ação |
|:-----:|:-----|
| `A ou ← Seta Esquerda` | Mover para a pista da esquerda |
| `D ou → Seta Direita` | Mover para a pista da direita |
| `W ou ↑ Seta Acima` | Pular |
| `ESPAÇO` | Pular (alternativo) |
| `ESC` | Sair do jogo |

---

## 📁 Estrutura do Projeto

```
Game-Byte-Runner/
│
├── src/                              # Código-fonte principal
│   ├── main.py                       # Ponto de entrada do programa
│   ├── game.py                       # Lógica principal do jogo
│   │
│   ├── core/                         # Módulo de infraestrutura
│   │   ├── constants.py              # Constantes do jogo
│   │   ├── mesh.py                   # Classe para gerenciar geometria
│   │   └── model_loader.py           # Carregamento de modelos OBJ
│   │
│   ├── entities/                     # Entidades do jogo
│   │   ├── player.py                 # Classe do jogador
│   │   ├── obstacle.py               # Classe dos obstáculos
│   │   ├── coin.py                   # Classe das moedas
│   │   ├── magnet.py                 # Classe do ímã modificador
│   │   ├── creeper.py                # Classe do inimigo
│   │   └── collectible.py            # Classe base para itens
│   │
│   ├── graphics/                     # Módulo de gráficos
│   │   ├── shader_loader.py          # Carregamento de shaders
│   │   └── texture_loader.py         # Carregamento de texturas
│   │
│   └── assets/                       # Recursos do jogo
│       ├── shaders/                  # Programas de shader (GLSL)
│       │   ├── vertexShader.glsl
│       │   ├── fragmentShader.glsl
│       │   ├── colorVertex.glsl
│       │   └── colorFragment.glsl
│       │
│       ├── textures/                 # Texturas (PNG/JPG)
│       │   ├── player/
│       │   ├── obstacle/
│       │   ├── coin/
│       │   ├── road/
│       │   ├── background/
│       │   └── creeper/
│       │
│       ├── sounds/                   # Arquivos de áudio (MP3)
│       │
│       └── models/                   # Modelos 3D (OBJ)
│           ├── player/
│           └── creeper/
│
├── docs/                             # Documentação
├── requirements.txt                  # Dependências do projeto
├── LICENSE                           # Licença MIT
└── README.md                         # Este arquivo
```

---

## 🎯 Mecânicas de Jogo

### 🏃 Jogador (Player)

- **Posição**: Fixo em Z, pode se mover horizontalmente entre 3 pistas
- **Pulo**: Ativa gravidade, sobe e desce com física realista
- **Animação**: Bounce durante a corrida
- **Moedas**: Exibidas no HUD, acumulam durante o jogo

### 🪨 Obstáculos

- Aparecem aleatoriamente em profundidades variadas
- Têm altura variável (desafio aumentado)
- Colisão termina o jogo
- Movimento contínuo em direção ao jogador

### 💰 Moedas

- Aparecem em grupos
- Espalhadas pelas 3 pistas
- Podem ser coletadas para aumentar pontuação
- Atraídas pelo ímã quando ativo

### 🧲 Ímã (Magnet)

- Modificador temporário (10 segundos)
- Atrai moedas em um raio de 30 unidades
- Aumenta a pontuação significativamente quando ativo

### 👹 Criatura (Creeper)

- Inimigo que persegue o jogador
- Segue a posição horizontal do jogador
- Pode resultar em game over se colidir

---

## 🎨 Conceitos de Computação Gráfica

### 1. **Transformações Geométricas (MVP Matrix)**

O projeto utiliza as três matrizes de transformação fundamentais:

- **Model Matrix**: Posiciona e orienta cada objeto no espaço 3D
- **View Matrix**: Define a câmera e sua visão do mundo
- **Projection Matrix**: Transforma o espaço de câmera para o espaço de tela (perspectiva)

```glsl
// No vertex shader:
gl_Position = projection * view * model * vec4(aPosition, 1.0);
```

### 2. **Shaders (GLSL)**

O projeto implementa dois tipos de shaders:

**Texture Shaders** (`vertexShader.glsl` + `fragmentShader.glsl`):
- Iluminação Phong com texturas
- Cálculo de normal, especular e difusa
- Mapeamento UV para texturas

```glsl
// Iluminação Phong
vec3 ambient = lightColor * texture(texSampler, uv).rgb * 0.1;
vec3 diffuse = lightColor * diff * texture(texSampler, uv).rgb;
vec3 specular = lightColor * spec * vec3(1.0);
```

**Color Shaders** (`colorVertex.glsl` + `colorFragment.glsl`):
- Iluminação sem textura
- Cores sólidas para certos objetos

### 3. **Texturas e UV Mapping**

- Carregamento de texturas PNG/JPG via PIL
- Coordenadas UV para mapeamento de textura
- Offset UV para animação de movimento

### 4. **Detecção de Colisão (AABB)**

Utiliza **Axis-Aligned Bounding Boxes** para detecção rápida:

```python
def is_colliding(player_pos, entity_pos, player_extent, entity_extent):
    return (abs(player_pos.x - entity_pos.x) < player_extent.x + entity_extent.x and
            abs(player_pos.y - entity_pos.y) < player_extent.y + entity_extent.y and
            abs(player_pos.z - entity_pos.z) < player_extent.z + entity_extent.z)
```

### 5. **Câmera e Perspectiva**

- Câmera fixa que acompanha o jogador
- Projeção em perspectiva
- Campo de visão (FOV) de 45 graus

### 6. **Animação**

- Interpolação suave de posições
- Animação de personagem baseada em tempo
- Efeitos de bounce durante corrida

---

## 🔧 Desenvolvimento e Extensões

### Como Adicionar um Novo Obstáculo

1. Defina as vértices em `core/constants.py`
2. Crie uma classe em `entities/` herança de `Collectible`
3. Instancie em `game.py`
4. Adicione textura em `assets/textures/`

### Como Modificar a Dificuldade

Edite em `core/constants.py`:

```python
SPEED_INCREMENT = 0.5       # Aumentar para mais rápido
MAX_SPEED = 50.0            # Limite de velocidade
OBSTACLE_WIDTH = 1.5        # Larura dos obstáculos
```

### Performance

Para melhorar a performance:

- Use `PyOpenGL-accelerate` (já incluído)
- Reduza o número máximo de obstáculos
- Otimize shaders
- Use vertex buffer objects (VBO)

---

## 📊 Fluxo do Jogo

```
┌──────────────────┐
│   Inicialização  │
│  (Janela, Audio) │
└────────┬─────────┘
         │
         ▼
┌──────────────────────┐
│  Loop de Renderização │
│  (Update + Render)   │
└────────┬─────────────┘
         │
         ├─► Atualizar Jogador
         │   (Gravidade, Pulo)
         │
         ├─► Atualizar Entidades
         │   (Obstáculos, Moedas)
         │
         ├─► Detectar Colisões
         │   │
         │   ├─► Moeda: +1 ponto
         │   ├─► Ímã: Ativar efeito
         │   └─► Obstáculo: Game Over
         │
         └─► Renderizar
             (Câmera, Shaders)
```

---

## 🐛 Solução de Problemas

### Erro: "ModuleNotFoundError: No module named 'OpenGL'"

**Solução**: Instale as dependências novamente:
```bash
pip install -r requirements.txt
```

### Erro: "GLFW error: No context current"

**Solução**: Verifique se sua placa gráfica suporta OpenGL 3.0+. Atualize os drivers da GPU.

### O jogo está muito lento

**Solução**: Reduza o número de obstáculos em `constants.py` ou desative `GL_DEPTH_TEST`.

### Sons não funcionam

**Solução**: Verifique se os arquivos MP3 estão em `src/assets/sounds/`:
- `coin.mp3`
- `game_over.mp3`
- `music.mp3`

---

## 📚 Referências e Recursos

- [PyOpenGL Documentation](https://pyopengl.sourceforge.net/)
- [GLFW Documentation](https://www.glfw.org/)
- [OpenGL Tutorial](https://learnopengl.com/)
- [GLM Mathematics](https://glm.g-truc.net/)

---

## 👨‍💻 Autores

**Giulia Salders** - Desenvolvedor e Estudante de Computação Gráfica

**Francisco Mikael** - Desenvolvedor e Estudante de Computação Gráfica

**Douglas de Lima** - Desenvolvedor e Estudante de Computação Gráfica

---

## 🤝 Contribuições

Contribuições são bem-vindas! Para contribuir:

1. Faça um **Fork** do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um **Pull Request**

---

**Divirta-se jogando e explorando os conceitos de Computação Gráfica!** 🎮✨
