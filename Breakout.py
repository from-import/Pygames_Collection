import pygame
import random

# 初始化Pygame
pygame.init()

# 游戏窗口尺寸
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# 定义颜色
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# 创建游戏窗口
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Breakout Game")

# 游戏参数
ball_radius = 10
ball_speed = [5, 5]
paddle_width = 100
paddle_height = 10
paddle_speed = 20
brick_width = 80
brick_height = 30
brick_gap = 10
brick_rows = 5
brick_cols = 10

# 创建滑板
paddle = pygame.Rect((WINDOW_WIDTH - paddle_width) // 2, WINDOW_HEIGHT - paddle_height - 10,
                     paddle_width, paddle_height)

# 创建小球
ball = pygame.Rect(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, ball_radius * 2, ball_radius * 2)

# 创建砖块
bricks = []
for row in range(brick_rows):
    for col in range(brick_cols):
        brick_left = col * (brick_width + brick_gap)
        brick_top = row * (brick_height + brick_gap) + 50
        brick = pygame.Rect(brick_left, brick_top, brick_width, brick_height)
        bricks.append(brick)

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle.right < WINDOW_WIDTH:
        paddle.x += paddle_speed

    # 移动小球
    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

    # 碰撞检测
    if ball.top <= 0:
        ball_speed[1] = -ball_speed[1]
    if ball.bottom >= WINDOW_HEIGHT:
        # 游戏结束
        running = False
    if ball.left <= 0 or ball.right >= WINDOW_WIDTH:
        ball_speed[0] = -ball_speed[0]
    if ball.colliderect(paddle):
        ball_speed[1] = -ball_speed[1]
    for brick in bricks:
        if ball.colliderect(brick):
            bricks.remove(brick)
            ball_speed[1] = -ball_speed[1]

    # 渲染界面
    window.fill(WHITE)
    pygame.draw.rect(window, BLUE, paddle)
    pygame.draw.circle(window, RED, ball.center, ball_radius)
    for brick in bricks:
        pygame.draw.rect(window, BLUE, brick)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
