import pygame
import random

# 游戏参数
WIDTH = 10  # 游戏区域宽度（单位：方块数）
HEIGHT = 20  # 游戏区域高度（单位：方块数）
BLOCK_SIZE = 30  # 方块大小（单位：像素）

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 128, 0)
PURPLE = (128, 0, 128)

# 不同类型方块的形状定义
SHAPES = [
    [[1, 1, 1, 1]],  # I形
    [[1, 1],
     [1, 1]],       # O形
    [[1, 1, 0],
     [0, 1, 1]],    # S形
    [[0, 1, 1],
     [1, 1, 0]],    # Z形
    [[1, 1, 1],
     [0, 1, 0]],    # T形
    [[1, 1, 1],
     [0, 0, 1]],    # J形
    [[1, 1, 1],
     [1, 0, 0]]     # L形
]

SHAPES_COLORS = [
    CYAN,    # I形
    YELLOW,  # O形
    GREEN,   # S形
    RED,     # Z形
    PURPLE,  # T形
    BLUE,    # J形
    ORANGE   # L形
]

# 初始化 Pygame
pygame.init()

# 设置屏幕和游戏区域大小
SCREEN_WIDTH = WIDTH * BLOCK_SIZE
SCREEN_HEIGHT = HEIGHT * BLOCK_SIZE
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("俄罗斯方块")

clock = pygame.time.Clock()

# 创建游戏区域
def create_board():
    return [[BLACK for _ in range(WIDTH)] for _ in range(HEIGHT)]

# 旋转方块
def rotate_shape(shape):
    return [[shape[j][i] for j in range(len(shape))] for i in range(len(shape[0]) - 1, -1, -1)]

# 检查方块是否与游戏区域发生碰撞
def check_collision(board, shape, offset):
    shape_height = len(shape)
    shape_width = len(shape[0])
    for i in range(shape_height):
        for j in range(shape_width):
            if shape[i][j] and (offset[1] + i >= HEIGHT or board[offset[1] + i][offset[0] + j] != BLACK):
                return True
    return False

# 绘制游戏区域
def draw_board(board):
    for i in range(HEIGHT):
        for j in range(WIDTH):
            pygame.draw.rect(screen, board[i][j], (j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

# 主游戏循环
def main():
    board = create_board()
    current_shape = random.choice(SHAPES)
    current_color = random.choice(SHAPES_COLORS)
    shape_x = WIDTH // 2 - len(current_shape[0]) // 2
    shape_y = 0
    game_over = False
    fall_time = 0
    fall_speed = 0.5  # 方块下落速度（单位：秒）

    while not game_over:
        screen.fill(WHITE)

        # 控制方块下落速度
        delta_time = clock.tick() / 1000
        fall_time += delta_time

        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if shape_x > 0 and not check_collision(board, current_shape, (shape_x - 1, shape_y)):
                        shape_x -= 1
                elif event.key == pygame.K_RIGHT:
                    if shape_x < WIDTH - len(current_shape[0]) and not check_collision(board, current_shape, (shape_x + 1, shape_y)):
                        shape_x += 1
                elif event.key == pygame.K_DOWN:
                    if not check_collision(board, current_shape, (shape_x, shape_y + 1)):
                        shape_y += 1
                elif event.key == pygame.K_UP:
                    rotated_shape = rotate_shape(current_shape)
                    if not check_collision(board, rotated_shape, (shape_x, shape_y)):
                        current_shape = rotated_shape

        # 计算方块下落
        if fall_time >= fall_speed:
            if not check_collision(board, current_shape, (shape_x, shape_y + 1)):
                shape_y += 1
            else:
                # 将方块固定到游戏区域
                for i in range(len(current_shape)):
                    for j in range(len(current_shape[0])):
                        if current_shape[i][j]:
                            board[shape_y + i][shape_x + j] = current_color
                # 检查消除行
                rows_to_remove = []
                for i in range(HEIGHT):
                    if all(color != BLACK for color in board[i]):
                        rows_to_remove.append(i)

                # 消除满行
                for row in rows_to_remove:
                    board.pop(row)
                    board.insert(0, [BLACK for _ in range(WIDTH)])

                # 生成新的方块
                current_shape = random.choice(SHAPES)
                current_color = random.choice(SHAPES_COLORS)
                shape_x = WIDTH // 2 - len(current_shape[0]) // 2
                shape_y = 0
                if check_collision(board, current_shape, (shape_x, shape_y)):
                    game_over = True

            fall_time = 0

        # 绘制游戏区域和方块
        draw_board(board)
        for i in range(len(current_shape)):
            for j in range(len(current_shape[0])):
                if current_shape[i][j]:
                    pygame.draw.rect(screen, current_color, ((shape_x + j) * BLOCK_SIZE, (shape_y + i) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

        pygame.display.update()

    # 游戏结束
    font = pygame.font.Font(None, 64)
    text = font.render("Game Over", True, RED)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.update()
    pygame.time.delay(2000)

# 启动游戏
if __name__ == "__main__":
    main()
