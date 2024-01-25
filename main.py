import pygame
from pygame.image import load
from pygame.math import Vector2
import random
from sys import exit
from pygame.locals import *

pygame.init()

block_width, block_height = 30, 30
RED = (255, 0, 0)
LIGHT_BLUE = (173, 216, 230)
DARK_YELLOW = (175, 175, 0)
YELLOW = (255, 255, 0)
LEMON_YELLOW = (250, 245, 175)
BLUE = (0, 0, 255)
DEEP_BLUE = (0, 0, 175)
LIGHT_GREEN = (0, 255, 0)
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)
score = 0
game_over = False
game_start = False
CLOCK = pygame.time.Clock
FPS = 60
overlay = pygame.Surface((900, 600))
overlay.set_alpha(240)
overlay.fill(BLACK)
last_update = 0
start_font = pygame.font.SysFont("couriernew", 300, True)
start_colors = [BLUE, RED, YELLOW, LIGHT_GREEN]
game_speed = 320
level = 1


class Fruit:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.pos = Vector2(self.x, self.y)
        self.randomize()
        self.img = load("images/apple.png").convert_alpha()

    def randomize(self):
        self.x = random.randrange(0, 30)
        self.y = random.randrange(0, 20)
        self.pos = Vector2(self.x, self.y)

    def draw(self):
        # pygame.draw.rect(display, RED, (self.x * block_width, self.y * block_height, block_width, block_height))
        display.blit(self.img, (self.x * block_width, self.y * block_height))


class Snake:
    def __init__(self):
        self.body = [Vector2(12, 3), Vector2(11, 3), Vector2(10, 3)]
        self.right = Vector2(1, 0)
        self.left = Vector2(-1, 0)
        self.up = Vector2(0, -1)
        self.down = Vector2(0, 1)
        self.direction = self.right
        self.directions = [self.left * 2, self.right * 2, self.up * 2, self.down * 2]
        self.new_block = False

        # head
        self.head_up = load("images/head_up.png").convert_alpha()
        self.head_down = load("images/head_down.png").convert_alpha()
        self.head_left = load("images/head_left.png").convert_alpha()
        self.head_right = load("images/head_right.png").convert_alpha()

        # tail
        self.tail_up = load("images/tail_up.png").convert_alpha()
        self.tail_down = load("images/tail_down.png").convert_alpha()
        self.tail_left = load("images/tail_left.png").convert_alpha()
        self.tail_right = load("images/tail_right.png").convert_alpha()

        # straight
        self.horizontal = load("images/body_horizontal.png").convert_alpha()
        self.vertical = load("images/body_vertical.png").convert_alpha()

        # bends
        self.body_tr = load("images/body_topright.png").convert_alpha()
        self.body_br = load("images/body_bottomright.png").convert_alpha()
        self.body_tl = load("images/body_topleft.png").convert_alpha()
        self.body_bl = load("images/body_bottomleft.png").convert_alpha()

    def update_head(self, part):
        # head
        if self.direction == self.up:
            display.blit(self.head_up, (part.x * block_width, part.y * block_height))

        elif self.direction == self.down:
            display.blit(self.head_down, (part.x * block_width, part.y * block_height))

        elif self.direction == self.left:
            display.blit(self.head_left, (part.x * block_width, part.y * block_height))

        elif self.direction == self.right:
            display.blit(self.head_right, (part.x * block_width, part.y * block_height))

    def update_tail(self, part):
        # tail
        if self.body[-2] - self.body[-1] == self.down:
            display.blit(self.tail_up, (part.x * block_width, part.y * block_height))

        elif self.body[-2] - self.body[-1] == self.up:
            display.blit(self.tail_down, (part.x * block_width, part.y * block_height))

        elif self.body[-2] - self.body[-1] == self.right:
            display.blit(self.tail_left, (part.x * block_width, part.y * block_height))

        elif self.body[-2] - self.body[-1] == self.left:
            display.blit(self.tail_right, (part.x * block_width, part.y * block_height))

    def update_body_straight(self, part, index):
        if self.body[index] - self.body[index + 1] == self.right or self.body[index] - self.body[index + 1] == self.left:
            display.blit(self.horizontal, (part.x * block_width, part.y * block_height))
        else:
            display.blit(self.vertical, (part.x * block_width, part.y * block_height))

    def draw(self):
        for index, part in enumerate(self.body):
            if index == 0:
                self.update_head(part)

            elif index == len(self.body) - 1:
                self.update_tail(part)

            else:
                next_block = self.body[index - 1] - part
                previous_block = self.body[index + 1] - part
                if self.body[index - 1] - self.body[index + 1] in self.directions:
                    self.update_body_straight(part, index)
                else:
                    if next_block.x == 1 and previous_block.y == 1 or next_block.y == 1 and previous_block.x == 1:
                        display.blit(self.body_br, (part.x * block_width, part.y * block_height))
                    elif next_block.x == -1 and previous_block.y == 1 or next_block.y == 1 and previous_block.x == -1:
                        display.blit(self.body_bl, (part.x * block_width, part.y * block_height))
                    elif next_block.x == 1 and previous_block.y == -1 or next_block.y == -1 and previous_block.x == 1:
                        display.blit(self.body_tr, (part.x * block_width, part.y * block_height))
                    elif next_block.x == -1 and previous_block.y == -1 or next_block.y == -1 and previous_block.x == -1:
                        display.blit(self.body_tl, (part.x * block_width, part.y * block_height))

    def move(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy

    def collided(self):
        if 0 > snake.body[0].x or 29 < snake.body[0].x:
            return True
        elif 0 > snake.body[0].y or 19 < snake.body[0].y:
            return True
        else:
            for i in self.body[1:]:
                if self.body[0] == i:
                    return True

        return False


class Sounds:
    openning = pygame.mixer.Sound("sounds/openning.wav")
    gameover = pygame.mixer.Sound("sounds/gameover.wav")
    collect = pygame.mixer.Sound("sounds/collect.wav")
    background = pygame.mixer.Sound("sounds/in-game.wav")
    background.set_volume(0.3)
    countdown = pygame.mixer.Sound("sounds/countdown.wav")


def draw_board():
    display.fill(LIGHT_GREEN)
    for x in range(0, 30, 2):
        for y in range(0, 20):
            if not y % 2 == 0:
                x += 1
            pygame.draw.rect(display, GREEN, (x * block_width, y * block_height, block_width, block_height))
            if not y % 2 == 0:
                x -= 1


def restart_button(mouse_pos):
    if 339 < mouse_pos[0] < 561:
        if 389 < mouse_pos[1] < 510:
            Sounds.countdown.play()
            return True
    return False


display = pygame.display.set_mode((900, 600))
pygame.display.set_caption("snake")
fruit = Fruit()
snake = Snake()
start_counter = 0
start_in = 3
Sounds.countdown.play()


def handle_events():
    global game_over, game_start, score, last_update, start_counter, start_in, level
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if not game_over and game_start:
            if event.type == KEYDOWN:
                if event.key == pygame.K_UP:
                    if not snake.direction == snake.down:
                        snake.direction = snake.up
                elif event.key == pygame.K_DOWN:
                    if not snake.direction == snake.up:
                        snake.direction = snake.down
                elif event.key == pygame.K_RIGHT:
                    if not snake.direction == snake.left:
                        snake.direction = snake.right
                elif event.key == pygame.K_LEFT:
                    if not snake.direction == snake.right:
                        snake.direction = snake.left
        if game_over:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button(pygame.mouse.get_pos()):
                    fruit.randomize()
                    snake.body = [Vector2(12, 3), Vector2(11, 3), Vector2(10, 3)]
                    score = 0
                    game_over = False
                    game_start = False
                    last_update = 0
                    start_counter = 0
                    start_in = 4
                    snake.direction = Vector2(1, 0)
                    level = 1


while True:
    handle_events()
    if not game_start:
        draw_board()
        display.blit(overlay, (0, 0))
        if pygame.time.get_ticks() - 500 >= start_counter:
            start_counter = pygame.time.get_ticks()
            start_in -= 1
            if start_in == -1:
                game_start = True
                Sounds.openning.play()
                Sounds.background.play(100)
        surface = start_font.render(str(start_in), True, start_colors[start_in])
        start_text = surface.get_rect()
        start_text.center = (450, 300)
        display.blit(surface, start_text)
        pygame.display.flip()
        continue
    if not game_over:
        draw_board()
        fruit.draw()
        if pygame.time.get_ticks() - game_speed / level >= last_update:
            if snake.body[0] == fruit.pos:
                snake.new_block = True
                snake.move()
                fruit.randomize()
                score += 1
                if score == level * 5:
                    level += 1
                Sounds.collect.play()
            else:
                snake.move()
            if snake.collided():
                game_over = True
                Sounds.background.stop()
                Sounds.gameover.play()
                # pygame.quit()
                # exit(f"you lost your score is: {score}")
            last_update = pygame.time.get_ticks()
        snake.draw()
        font = pygame.font.Font('freesansbold.ttf', 32)
        score_surface = font.render(f"score: {score}  level: {level}", True, DEEP_BLUE)
        score_text = score_surface.get_rect()
        score_text.topleft = (30, 30)
        display.blit(score_surface, score_text)
    else:
        display.fill(BLACK)
        font = pygame.font.SysFont('couriernew', 48)
        # score
        score_surface = font.render(f"score: {score}", True, RED, BLACK)
        score_text = score_surface.get_rect()
        score_text.center = (450, 300)
        display.blit(score_surface, score_text)
        # level
        score_surface = font.render(f"level: {level}", True, RED, BLACK)
        score_text = score_surface.get_rect()
        score_text.center = (450, 240)
        display.blit(score_surface, score_text)

        pygame.draw.rect(display, DARK_YELLOW, (340, 390, 220, 120), border_radius=5)
        pygame.draw.rect(display, YELLOW, (350, 400, 200, 100), border_radius=15)
        pygame.draw.rect(display, LEMON_YELLOW, (355, 410, 10, 80), border_top_left_radius=10, border_bottom_left_radius=5)
        pygame.draw.rect(display, LEMON_YELLOW, (355, 480, 30, 10))

        font = pygame.font.SysFont('couriernew.ttf', 40)
        score_surface = font.render("Restart", True, (100, 100, 0))
        score_text = score_surface.get_rect()
        score_text.center = (450, 450)
        display.blit(score_surface, score_text)
    pygame.display.flip()
    CLOCK.tick(pygame.time.Clock(), FPS)
