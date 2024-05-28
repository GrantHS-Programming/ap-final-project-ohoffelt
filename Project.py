import pygame
import random
import sys
from pygame.locals import *

pygame.init()
mainClock = pygame.time.Clock()

SCALE = 3

WINDOWWIDTH = 700 * SCALE
WINDOWHEIGHT = 300 * SCALE
window = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Jesus Jumps')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (175, 0, 0)
DARK_RED = (75, 30, 30)
REDDISH = (100, 15, 15)
BLUE = (0, 150, 225)
DARK_BLUE = (0, 75, 200)
BROWN = (150, 100, 50)
LIGHT_BLUE = (0, 200, 255)
YELLOW = (255, 255, 0)
GRAY = (100, 100, 100)
DARK_GREY = (75, 75, 75)

charW = 20 * SCALE
charH = 35 * SCALE
terrainH = 25 * SCALE
blockD = 50 * SCALE
holeD = 75 * SCALE
levelSize = 5000 * SCALE
colorVariance = 20
xVariance = 20 * SCALE

jesus = pygame.image.load("jesus.png")
wave = pygame.image.load("wave.png")
crate = pygame.image.load("crate.png")
cross = pygame.image.load("cross.png")
fish1 = pygame.image.load("fish1.png")
fish1 = pygame.transform.flip(fish1,True,False)
fish2 = pygame.image.load("fish2.png")
fish3 = pygame.image.load("fish3.png")
fish4 = pygame.image.load("fish4.png")
fish5 = pygame.image.load("fish5.png")
fish6 = pygame.image.load("fish6.png")
fish7 = pygame.image.load("fish7.png")
fish8 = pygame.image.load("fish8.png")
fish = [fish1, fish2, fish3, fish4, fish5, fish6, fish7, fish8]
rock = pygame.image.load("not_netherrack.jpeg")
y = 0
for x in fish:
    x = pygame.transform.scale(x, (blockD, blockD))
    fish[y] = x
    y += 1
jesus = pygame.transform.scale(jesus, (charW, charW))
wave = pygame.transform.scale(wave, (blockD, blockD))
crate = pygame.transform.scale(crate, (blockD, blockD))
cross = pygame.transform.scale(cross, (charW, charH))
cross = pygame.transform.rotate(cross, 40)
jesus_upside_down = pygame.transform.flip(jesus, False, True)
jesus_rotated = pygame.transform.rotate(jesus, -90)
rock = pygame.transform.scale(rock, (blockD, blockD))

char = pygame.Rect(0 + charW * 3, WINDOWHEIGHT / 2 - charH / 2, charW, charW)
terrain = pygame.Rect(0, WINDOWHEIGHT - terrainH, WINDOWWIDTH, terrainH)
ceiling = pygame.Rect(0, 0, WINDOWWIDTH, terrainH)
basicFontSmall = pygame.font.SysFont('Arial', 20 * SCALE)
basicFont = pygame.font.SysFont('Arial', 35 * SCALE)
highScoreDirt = 0
highScoreCloud = 0
highScoreSpace = 0

blocks = []


def createDirtLevel():
    blocks.clear()
    l1_l = []
    for i in range(40):
        l_one_pos = random.randint(0, levelSize)
        bcolor = (random.randint(BROWN[0] - colorVariance, BROWN[0] + colorVariance),
                  random.randint(BROWN[1] - colorVariance, BROWN[1] + colorVariance),
                  random.randint(BROWN[2] - colorVariance, BROWN[2] + colorVariance))
        block_l1 = {"rect": pygame.Rect(WINDOWWIDTH + l_one_pos, terrain.top - blockD, blockD, blockD), "color": bcolor}
        l1_l.append(l_one_pos)
        blocks.append(block_l1)
    for i in range(25):
        l1_l.sort()
        l_two_pos = random.randint(l1_l[0] + blockD, l1_l[-1] - blockD * 2)
        bcolor = (random.randint(BROWN[0] - colorVariance, BROWN[0] + colorVariance),
                  random.randint(BROWN[1] - colorVariance, BROWN[1] + colorVariance),
                  random.randint(BROWN[2] - colorVariance, BROWN[2] + colorVariance))
        block_l2 = {"rect": pygame.Rect(WINDOWWIDTH + l_two_pos, terrain.top - blockD * 2, blockD, blockD),
                    "color": bcolor}
        blocks.append(block_l2)


def createWaterLevel():
    print(len(fish))
    block_x = []
    block_y = []
    blocks.clear()
    add = True
    for i in range(levelSize):
        if i % (250 * SCALE) == 0:
            block_x.append(i)
    for i in block_x:
        block_y.append(pygame.Rect(WINDOWWIDTH + i, random.randint(0, WINDOWHEIGHT - holeD), holeD,
                                   random.randint(holeD - 10 * SCALE, holeD + 10 * SCALE)))
    for x in block_x:
        for y in range(30):
            block = {"rect": pygame.Rect(WINDOWWIDTH + random.randint(x - xVariance, x + xVariance),
                                         random.randint(0, WINDOWHEIGHT - blockD), blockD, blockD),
                     "fish": fish[random.randint(0, len(fish) - 1)]}
            add = True
            for i in block_y:
                if block["rect"].colliderect(i):
                    add = False
            if add:
                blocks.append(block)


def createHellLevel():
    blocks.clear()
    block_x = []
    for i in range(levelSize):
        if i % blockD == 0:
            block_x.append(i)
    for x in block_x:
        block_y = random.randint(0, 2)
        if block_y == 0:
            block = {"rect": pygame.Rect(WINDOWWIDTH + x, terrain.top - blockD, blockD, blockD), "color": GRAY}
        elif block_y == 1:
            block = {"rect": pygame.Rect(WINDOWWIDTH + x, window.get_rect().centery - (blockD / 2), blockD, blockD),
                     "color": GRAY}
        else:
            block = {"rect": pygame.Rect(WINDOWWIDTH + x, ceiling.bottom, blockD, blockD), "color": GRAY}
        blocks.append(block)


def dirtLevel():
    high_score_temp = highScoreDirt
    exit = False
    while not exit:
        space_pressed = False
        playing = True
        on_ground = False
        grav = 0
        up = 0
        game_speed = 3 * SCALE
        frame_count = 0
        speed_up = 0
        score_counter = 0
        grace_period = 50
        createDirtLevel()
        char.centery = window.get_rect().centery

        while playing:
            score = basicFont.render(str(int(score_counter) * 10), True, WHITE, None)
            high_score = basicFontSmall.render(str(int(high_score_temp) * 10), True, WHITE, None)
            score_rect = score.get_rect()
            high_score_rect = high_score.get_rect()
            score_rect.topright = window.get_rect().topright
            high_score_rect.topright = score_rect.bottomright
            frame_count += 1
            char.centery += grav - up

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if frame_count >= grace_period:
                        if event.key == K_SPACE:
                            space_pressed = True
                        elif event.key == K_d or event.key == K_RIGHT:
                            speed_up = 2 * SCALE
                        elif event.key == K_a or event.key == K_LEFT:
                            speed_up = -2 * SCALE
                    if event.key == K_BACKSPACE:
                        exit = True
                        playing = False
                if event.type == KEYUP:
                    if event.key == K_SPACE:
                        space_pressed = False
                    if event.key == K_d or event.key == K_RIGHT:
                        speed_up = 0
                    elif event.key == K_a or event.key == K_LEFT:
                        speed_up = 0

            for i in blocks:
                if char.colliderect(i["rect"]) and char.bottom > i["rect"].top + 25 * SCALE and char.right <= i[
                    "rect"].left + 10 * SCALE:
                    playing = False
                if ((char.colliderect(i["rect"]) and char.bottom <= i["rect"].top + 12 * SCALE) or (
                        char.colliderect(i["rect"]) and grav >= 10 * SCALE)) and grav >= up:
                    on_ground = True
                    char.bottom = i["rect"].top
                elif char.bottom >= terrain.top:
                    on_ground = True
                    char.bottom = terrain.top
                else:
                    on_ground = False
                if not on_ground and frame_count >= grace_period:
                    grav += 0.01 * SCALE
                else:
                    grav = 0
                    up = 0
                if on_ground and space_pressed and grav <= 50:
                    up = 12 * SCALE
                i["rect"].centerx -= game_speed + speed_up
                score_counter += (game_speed + speed_up) / (500 * SCALE)
                if high_score_temp < score_counter:
                    high_score_temp = score_counter
                if i["rect"].right <= 0:
                    i["rect"].right += levelSize
                    if game_speed <= 10 * SCALE:
                        game_speed += 1 / len(blocks) * SCALE
                window.blit(crate, i["rect"])
            pygame.draw.rect(window, BROWN, terrain)
            if frame_count > grace_period or frame_count % 20 < 10:
                window.blit(cross, (char.left - charW / 3, char.top - charW / 1.25))
                window.blit(jesus, char)
            window.blit(score, score_rect)
            window.blit(high_score, high_score_rect)
            pygame.display.update()
            window.fill(LIGHT_BLUE)
            mainClock.tick(40)
    return high_score_temp


def waterLevel():
    high_score_temp = highScoreCloud
    exit = False
    while not exit:
        playing = True
        up = False
        down = False
        vert = 0
        game_speed = 2 * SCALE
        frame_count = 0
        jump_count = 0
        speed_up = 0
        score_counter = 0
        grace_period = 100
        createWaterLevel()
        char.centery = window.get_rect().centery

        while playing:
            if game_speed <= 15:
                game_speed += 0.0005 * SCALE
            score = basicFont.render(str(int(score_counter) * 10), True, WHITE, None)
            high_score = basicFontSmall.render(str(int(high_score_temp) * 10), True, WHITE, None)
            score_rect = score.get_rect()
            high_score_rect = high_score.get_rect()
            score_rect.topright = window.get_rect().topright
            high_score_rect.topright = score_rect.bottomright
            frame_count += 1
            char.centery += vert

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if (event.key == K_UP or event.key == K_w) and frame_count >= grace_period:
                        up = True
                    elif (event.key == K_DOWN or event.key == K_s) and frame_count >= grace_period:
                        down = True
                    elif event.key == K_BACKSPACE:
                        exit = True
                        playing = False
                    elif (event.key == K_d or event.key == K_RIGHT) and frame_count >= grace_period:
                        speed_up = 1 * SCALE
                    elif (event.key == K_a or event.key == K_LEFT) and frame_count >= grace_period:
                        speed_up = -1 * SCALE
                    elif event.key == K_0:
                        char.top = WINDOWHEIGHT
                if event.type == KEYUP:
                    if event.key == K_UP or event.key == K_w:
                        up = False
                    if event.key == K_DOWN or event.key == K_s:
                        down = False
                    if event.key == K_d or event.key == K_RIGHT:
                        speed_up = 0
                    elif event.key == K_a or event.key == K_LEFT:
                        speed_up = 0

            for i in blocks:
                if char.colliderect(i["rect"]):
                    playing = False
                i["rect"].centerx -= game_speed + speed_up
                score_counter += (game_speed + speed_up) / (2500 * SCALE)
                if high_score_temp < score_counter:
                    high_score_temp = score_counter
                if i["rect"].right <= 0:
                    i["rect"].right += levelSize
                window.blit(i["fish"], i["rect"])

            if up:
                vert -= 0.2 * SCALE
            if down:
                vert += 0.2 * SCALE
            if not (up or down):
                vert /= 1.05

            if char.top > WINDOWHEIGHT:
                char.top = 0
            if char.bottom < 0:
                char.bottom = WINDOWHEIGHT

            if frame_count > grace_period or frame_count % 40 < 20:
                window.blit(jesus_rotated, char)
            window.blit(score, score_rect)
            window.blit(high_score, high_score_rect)
            if frame_count % 2 == 0:
                pygame.display.update()
            window.fill(BLUE)
            mainClock.tick(80)
    return high_score_temp


def hellLevel():
    high_score_temp = highScoreSpace
    exit = False
    while not exit:
        playing = True
        on_ground = False
        space_pressed = False
        grav = 0
        up = 0
        game_speed = 2.5 * SCALE
        frame_count = 0
        speed_up = 0
        score_counter = 0
        grace_period = 50
        grav_dir = 1
        createHellLevel()
        char.centery = window.get_rect().centery

        while playing:
            collided = False
            game_speed += 0.001 * SCALE
            score = basicFont.render(str(int(score_counter) * 10), True, WHITE, None)
            high_score = basicFontSmall.render(str(int(high_score_temp) * 10), True, WHITE, None)
            score_rect = score.get_rect()
            high_score_rect = high_score.get_rect()
            score_rect.topright = window.get_rect().topright
            high_score_rect.topright = score_rect.bottomright
            frame_count += 1
            if not on_ground:
                char.centery += grav
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if frame_count >= grace_period:
                        if event.key == K_SPACE:
                            space_pressed = True
                            char.centery += grav_dir
                        elif event.key == K_d or event.key == K_RIGHT:
                            speed_up = 2 * SCALE
                        elif event.key == K_a or event.key == K_LEFT:
                            speed_up = -2 * SCALE
                    if event.key == K_BACKSPACE:
                        exit = True
                        playing = False
                if event.type == KEYUP:
                    if event.key == K_SPACE:
                        space_pressed = False
                    elif event.key == K_d or event.key == K_RIGHT:
                        speed_up = 0
                    elif event.key == K_a or event.key == K_LEFT:
                        speed_up = 0
            if space_pressed and on_ground:
                grav_dir *= -1
                char.centery += grav_dir * 2 * SCALE
            for i in blocks:
                i["rect"].centerx -= game_speed + speed_up
                if i["rect"].right < 0:
                    i["rect"].centerx += levelSize
                if i["rect"].colliderect(char):
                    collided = True
                    if checkOnGround(i, grav_dir):
                        on_ground = True
                        grav = 0
                        if grav_dir > 0:
                            char.bottom = i["rect"].top + 1
                        else:
                            char.top = i["rect"].bottom - 1
                    else:
                        playing = False
                window.blit(rock, i["rect"])
            if collided:
                on_ground = True
                grav = 0
            else:
                on_ground = False
            if char.bottom >= terrain.top:
                on_ground = True
                char.bottom = terrain.top
                grav = 0
            if char.top <= ceiling.bottom:
                on_ground = True
                char.top = ceiling.bottom
                grav = 0
            if frame_count > grace_period and not on_ground:
                grav += 1 * grav_dir * SCALE
            game_speed += 0.1 / len(blocks) * SCALE
            if grav_dir > 0:
                window.blit(jesus, char)
            else:
                window.blit(jesus_upside_down, char)
            pygame.draw.rect(window, DARK_RED, terrain)
            pygame.draw.rect(window, DARK_RED, ceiling)
            if frame_count <= grace_period and frame_count % 20 >= 10:
                pygame.draw.rect(window, REDDISH, char)
            score_counter += (game_speed + speed_up) / (6 * SCALE)
            if high_score_temp < score_counter:
                high_score_temp = score_counter
            window.blit(score, score_rect)
            window.blit(high_score, high_score_rect)
            pygame.display.update()
            window.fill(REDDISH)
            mainClock.tick(40)
    return high_score_temp


def checkOnGround(i, grav_dir):
    rect = i["rect"]
    if grav_dir > 0:
        if char.bottom <= rect.top + 20 * SCALE:
            return True
    else:
        if char.top >= rect.bottom - 20 * SCALE:
            return True
    return False


while True:
    highScoreSpace = hellLevel()
    highScoreCloud = waterLevel()
    highScoreDirt = dirtLevel()
