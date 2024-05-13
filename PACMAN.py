import pygame
import random

# 游戏初始化
pygame.init()

# 定义常量
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
FPS = 60

# 设置屏幕
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("吃豆人游戏")

clock = pygame.time.Clock()

# 定义游戏对象
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    def update(self, walls):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.move(-5, 0, walls)
        elif keys[pygame.K_RIGHT]:
            self.move(5, 0, walls)
        elif keys[pygame.K_UP]:
            self.move(0, -5, walls)
        elif keys[pygame.K_DOWN]:
            self.move(0, 5, walls)

    def move(self, dx, dy, walls):
        # 移动并检测碰撞
        self.rect.x += dx
        self.rect.y += dy

        for wall in pygame.sprite.spritecollide(self, walls, False):
            if dx > 0:  # 向右移动
                self.rect.right = wall.rect.left
            elif dx < 0:  # 向左移动
                self.rect.left = wall.rect.right
            elif dy > 0:  # 向下移动
                self.rect.bottom = wall.rect.top
            elif dy < 0:  # 向上移动
                self.rect.top = wall.rect.bottom

class Bean(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

class Monster(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = random.choice(['left', 'right', 'up', 'down'])

    def update(self, walls):
        if self.direction == 'left':
            self.move(-2, 0, walls)
        elif self.direction == 'right':
            self.move(2, 0, walls)
        elif self.direction == 'up':
            self.move(0, -2, walls)
        elif self.direction == 'down':
            self.move(0, 2, walls)

        # 随机改变移动方向
        if random.randint(0, 100) < 2:
            self.direction = random.choice(['left', 'right', 'up', 'down'])

    def move(self, dx, dy, walls):
        # 移动并检测碰撞
        self.rect.x += dx
        self.rect.y += dy

        for wall in pygame.sprite.spritecollide(self, walls, False):
            if dx > 0:  # 向右移动
                self.rect.right = wall.rect.left
            elif dx < 0:  # 向左移动
                self.rect.left = wall.rect.right
            elif dy > 0:  # 向下移动
                self.rect.bottom = wall.rect.top
            elif dy < 0:  # 向上移动
                self.rect.top = wall.rect.bottom

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# 创建游戏对象
player = Player()
beans = pygame.sprite.Group()
monsters = pygame.sprite.Group()
walls = pygame.sprite.Group()

# 创建豆子
for _ in range(40):
    x, y = random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)
    bean = Bean(x, y)
    beans.add(bean)

# 创建怪物
for _ in range(3):
    x, y = random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)
    monster = Monster(x, y)
    monsters.add(monster)

# 创建墙体障碍物
wall_positions = [
    (100, 100, 400, 20),
    (200, 200, 20, 200),
    (400, 200, 20, 200),
    (0, 0, SCREEN_WIDTH, 10),
    (0, 0, 10, SCREEN_HEIGHT),
    (SCREEN_WIDTH - 10, 0, 10, SCREEN_HEIGHT),
    (0, SCREEN_HEIGHT - 10, SCREEN_WIDTH, 10)
]

for pos in wall_positions:
    wall = Wall(*pos)
    walls.add(wall)

# 主循环
running = True
score = 0
font = pygame.font.Font(None, 36)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 更新游戏对象
    player.update(walls)
    monsters.update(walls)

    # 碰撞检测
    hit_beans = pygame.sprite.spritecollide(player, beans, True)
    if hit_beans:
        score += len(hit_beans)

    hit_monsters = pygame.sprite.spritecollide(player, monsters, False)
    if hit_monsters:
        running = False  # 碰到怪物，游戏结束

    # 渲染屏幕
    screen.fill(BLACK)
    beans.draw(screen)
    monsters.draw(screen)
    walls.draw(screen)
    screen.blit(player.image, player.rect)

    # 显示得分
    score_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
print("游戏结束，得分：", score)
