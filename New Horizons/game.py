import pygame
import random as rand
from playsound import playsound

pygame.init()
pygame.mixer.init()

class Bullet:
    def __init__(self, x, y, velocity, damage):
        self.x = x
        self.y = y
        self.velocity = velocity
        self.damage = damage

    def move(self):
        self.x += self.velocity

    def draw(self, screen):
        screen.blit(bullet_picture, (self.x, self.y))

class EnemyObj:
    def __init__(self, x, y, health):
        self.image = pygame.image.load('New Horizons/img/enemies/enemy.png')
        self.x = x
        self.y = y
        self.health = health
        self.x_vel = 0

    def mechanics(self):
        if self.x_vel < 4:
            if player_x > self.x:
                self.x_vel += 2
            elif player_x < self.x:
                self.x_vel -= 2

        if self.x_vel < 0:
            self.x_vel += de_acc
        if self.x_vel > 0:
            self.x_vel -= de_acc
        if player_x >= left_border:
            self.x += self.x_vel
        if self.x >= right_border:
            self.x_vel *= -1
        if self.x <= left_border:
            self.x_vel *= -1
        if self.y < ground:
            self.y += gravity

        if self.health <= 0:
            global kills
            kills += 1
            return True  

        if player_x > self.x - 20 and player_x < self.x + 20 and player_y == self.y:
            global lifes
            if lifes > 0:
                lifes -= 1
                heart.pop(0)
            if lifes <= 0:
                end_game()

        return False  
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))


def end_game():
    global running
    loser.play()
    screen.fill((0, 255, 0))
    color = (255,255,255)
    end = font.render("End Game", True, color)
    end_btn = end.get_rect(center=(screen_width / 2, screen_height / 2))
    restart = font.render("Restart", True, color)
    restart_btn = restart.get_rect(center=(screen_width / 2, screen_height / 2 + 200))

    text = font.render(rand.choice(defeat), True, (0, 0, 0))
    screen.blit(pygame.image.load('New Horizons/img/Backgrounds/endgame.png'), (0, 0))
    screen.blit(end, end_btn)
    screen.blit(restart, restart_btn)
    screen.blit(text, (300, 0))

    pygame.display.flip()

    while True:
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if end_btn.collidepoint(mouse):
                    pygame.quit()
                    exit()
                elif restart_btn.collidepoint(mouse):
                    reset()
                    return

def reset():
    global level, player_x, player_y, x_vel, y_vel, lifes, heart, enemy_act, deaths
    lifes = 3
    heart.clear()
    player_x = 0
    player_y = ground
    x_vel = 0
    y_vel = 0
    enemy_act.clear()
    level = 1
    load_level(level)
    deaths += 1

def load_level(lvl):
    global bg_img, cel_obj_img, enemy_act
    bg_img, cel_obj_img = backgrounds[lvl % len(backgrounds)]
    enemy_act = []  # Reset the enemy list
    x = player_x + 200
    if level > 1:
            x = rand.randint(left_border, right_border)
            y = ground
            health = 3 + lvl
            enemy_act.append(EnemyObj(x, y, health))


def update_player():
    kill_count = font.render(f'kills: {kills}', True, (0, 255, 0))
    death_count = font.render(f'Deaths: {deaths}', True, (0, 255, 0))
    level_count = font.render(f'Level: {level}', True, (0, 255,0))
    screen.blit(death_count, (500, 0))
    screen.blit(kill_count, (300, 0))
    screen.blit(player, (player_x, player_y))

FPS = 60
screen_width = 800
screen_height = 600
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer')
backgrounds = [
    (pygame.image.load('New Horizons/img/backgrounds/sky.png'), pygame.image.load('New Horizons/img/backgrounds/sun.png')),
    (pygame.image.load('New Horizons/img/backgrounds/level2.png'), pygame.image.load('New Horizons/img/backgrounds/bloodmoon.png')),
]

loser = pygame.mixer.Sound(r'New Horizons\audio\loser.mp3')
right_border = 770
left_border = -10
ground = 570
gravity = 5
font = pygame.font.Font('freesansbold.ttf', 32)

player_x = 0
player_y = ground
y_vel = 0
x_vel = 0
de_acc = 1
y_acc = 30
x_acc = 3
stamina = 60
jump = False
lifes = 3
player = pygame.image.load('New Horizons/img/player/player.png')
heart_img = pygame.image.load('New Horizons/img/player/Heart.png')
heart = []
kills = 0
deaths = 0

bullet_picture = pygame.image.load('New Horizons/img/player/Bullet.png')
max_bullets = 4
bullet_velocity = 10
bullets = []
gunshot = pygame.mixer.Sound(r"New Horizons\audio\gunshot.mp3")
enemy_act = []



level = 1
load_level(level)

defeat = ["git gud Tom", "helt forferdelig", "jeg klarte til level 40", "Du skuffer meg", "Et barn kunne gjørt bedre", "trash", "not on my level", "tenk å tape til basic ai", "hvordan klarer du å tape", "ass", "shit performance", "'lagger' du?"]
running = True
while running:
    clock.tick(FPS)
    screen.blit(bg_img, (0, 0))
    screen.blit(cel_obj_img, (100, 100))

    for i in range(lifes):
        screen.blit(heart_img, (650 + i * 50, 0))
        heart.append(i)

    update_player()

    # Update and draw enemies, remove defeated ones
    for enemy in enemy_act[:]:  # Copy the list to avoid issues while removing items
        enemy.draw(screen)
        if enemy.mechanics():
            enemy_act.remove(enemy)

    for bullet in bullets:
        bullet.move()
        bullet.draw(screen)
        if bullet.x > right_border or bullet.x < left_border:
            bullets.remove(bullet)
        for enemy in enemy_act:
            if enemy.x < bullet.x < enemy.x + 20:
                enemy.health -= bullet.damage
                bullets.remove(bullet)
                break

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and not jump:
                y_vel = -y_acc
                jump = True
            elif event.key == pygame.K_e and len(bullets) < max_bullets:
                damage = 1 + (level - 2) // 2
                bullets.append(Bullet(player_x, player_y, bullet_velocity, damage))
                gunshot.play()
            elif event.key == pygame.K_q and len(bullets) < max_bullets:
                damage = 1 + (level - 2) // 2
                bullets.append(Bullet(player_x, player_y, -bullet_velocity, damage))
                gunshot.play()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and x_vel > -10:
        x_vel -= x_acc
    if keys[pygame.K_d] and x_vel < 10:
        x_vel += x_acc

    if x_vel < 0:
        x_vel += de_acc
    if x_vel > 0:
        x_vel -= de_acc

    player_x += x_vel
    player_y += y_vel

    if jump and player_y < ground:
        y_vel += gravity

    if player_y >= ground:
        player_y = ground
        jump = False

    if player_x < left_border and level > 1:
        player_x = right_border
        x_vel = 0
        y_vel = 0

    if player_x > right_border:
        player_x = left_border
        x_vel = 0
        y_vel = 0
        level += 1
        load_level(level)

    pygame.display.flip()
