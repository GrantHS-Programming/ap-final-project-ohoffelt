import pygame
import random
import sys
from pygame.locals import *

pygame.init()
mainClock = pygame.time.Clock()
WINDOWWIDTH = 700
WINDOWHEIGHT = 300
jesus = pygame.image.load("jesus.png")
window = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Jesus Jumps')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 100, 255)
BROWN = (150, 100, 50)
SKY = (0, 200, 255)
YELLOW = (255, 255, 0)
GRAY = (100, 100, 100)
DARK_GREY = (75, 75, 75)

charW = 20
charH = 35
terrainH = 25
blockD = 50
holeD = 75
levelSize = 5000
colorVariance = 20
xVariance = 20
jesus = pygame.transform.scale(jesus,(charW,charH))
char = pygame.Rect(0 + charW * 3, WINDOWHEIGHT / 2 - charH / 2, charW, charW)
terrain = pygame.Rect(0, WINDOWHEIGHT - terrainH, WINDOWWIDTH, terrainH)
ceiling = pygame.Rect(0, 0, WINDOWWIDTH, terrainH)
basicFontSmall = pygame.font.SysFont('Arial', 20)
basicFont = pygame.font.SysFont('Arial', 35)
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


def createCloudLevel():
    block_x = []
    block_y = []
    blocks.clear()
    add = True
    for i in range(levelSize):
        if i % 250 == 0:
            block_x.append(i)
    for i in block_x:
        block_y.append(pygame.Rect(WINDOWWIDTH + i, random.randint(0, WINDOWHEIGHT - holeD), holeD,
                                   random.randint(holeD - 10, holeD + 10)))
    for x in block_x:
        for y in range(30):
            block = {"rect": pygame.Rect(WINDOWWIDTH + random.randint(x - xVariance, x + xVariance),
                                         random.randint(0, WINDOWHEIGHT - blockD), blockD, blockD), "color": WHITE}
            add = True
            for i in block_y:
                if block["rect"].colliderect(i):
                    add = False
            if add:
                blocks.append(block)


def createSpaceLevel():
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
        game_speed = 3
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
                            speed_up = 2
                        elif event.key == K_a or event.key == K_LEFT:
                            speed_up = -2
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

            for i in blocks:
                if char.colliderect(i["rect"]) and char.bottom > i["rect"].top + 25 and char.right <= i["rect"].left + 10:
                    playing = False
                if ((char.colliderect(i["rect"]) and char.bottom <= i["rect"].top + 12) or (
                        char.colliderect(i["rect"]) and grav >= 10)) and grav >= up:
                    on_ground = True
                    char.bottom = i["rect"].top
                elif char.bottom >= terrain.top:
                    on_ground = True
                    char.bottom = terrain.top
                else:
                    on_ground = False
                if not on_ground and frame_count >= grace_period:
                    grav += 0.01
                else:
                    grav = 0
                    up = 0
                if on_ground and space_pressed and grav <= 50:
                    up = 12
                i["rect"].centerx -= game_speed + speed_up
                score_counter += (game_speed + speed_up) / 1000
                if high_score_temp < score_counter:
                    high_score_temp = score_counter
                if i["rect"].right <= 0:
                    i["rect"].right += levelSize
                    if game_speed <= 10:
                        game_speed += 1 / len(blocks)
                pygame.draw.rect(window, i["color"], i["rect"])
            pygame.draw.rect(window, BROWN, terrain)
            window.blit(jesus, char)
            if frame_count <= grace_period and frame_count % 20 >= 10:
                pygame.draw.rect(window, SKY, char)
            window.blit(score, score_rect)
            window.blit(high_score, high_score_rect)
            pygame.display.update()
            window.fill(SKY)
            mainClock.tick(40)
    return high_score_temp


def cloudLevel():
    high_score_temp = highScoreCloud
    exit = False
    while not exit:
        space_pressed = False
        playing = True
        grav = 0
        up = 0
        game_speed = 3
        frame_count = 0
        jump_count = 0
        speed_up = 0
        score_counter = 0
        grace_period = 50
        createCloudLevel()
        char.centery = window.get_rect().centery

        while playing:
            if game_speed <= 10:
                game_speed += 0.0005
            if space_pressed:
                jump_count += 1
                if jump_count >= 8:
                    grav = 0
                    up = 5
            if frame_count >= grace_period:
                grav += 0.25
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
                    if event.key == K_SPACE and frame_count >= grace_period:
                        space_pressed = True
                        grav = 0
                        up = 4
                    elif event.key == K_BACKSPACE:
                        exit = True
                        playing = False
                if event.type == KEYUP:
                    if event.key == K_SPACE:
                        space_pressed = False
                        jump_count = 0

            for i in blocks:
                if char.colliderect(i["rect"]) or char.top > WINDOWHEIGHT or char.bottom < 0:
                    playing = False
                i["rect"].centerx -= game_speed + speed_up
                score_counter += game_speed / 5000
                if high_score_temp < score_counter:
                    high_score_temp = score_counter
                if i["rect"].right <= 0:
                    i["rect"].right += levelSize
                pygame.draw.rect(window, i["color"], i["rect"])

            pygame.draw.rect(window, YELLOW, char)
            if frame_count <= grace_period and frame_count % 20 >= 10:
                pygame.draw.rect(window, SKY, char)
            window.blit(score, score_rect)
            window.blit(high_score, high_score_rect)
            pygame.display.update()
            window.fill(SKY)
            mainClock.tick(40)
    return high_score_temp


def spaceLevel():
    high_score_temp = highScoreSpace
    exit = False
    while not exit:
        playing = True
        on_ground = False
        space_pressed = False
        grav = 0
        up = 0
        game_speed = 2.5
        frame_count = 0
        speed_up = 0
        score_counter = 0
        grace_period = 50
        grav_dir = 1
        createSpaceLevel()
        char.centery = window.get_rect().centery

        while playing:
            collided = False
            game_speed += 0.001
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
                            speed_up = 2
                        elif event.key == K_a or event.key == K_LEFT:
                            speed_up = -2
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
                char.centery += grav_dir*2
            for i in blocks:
                i["rect"].centerx -= game_speed+speed_up
                if i["rect"].right < 0:
                    i["rect"].centerx += levelSize
                if i["rect"].colliderect(char):
                    collided = True
                    if checkOnGround(i, grav_dir):
                        on_ground = True
                        grav = 0
                        if grav_dir > 0:
                            char.bottom = i["rect"].top+1
                        else:
                            char.top = i["rect"].bottom-1
                    else:
                        playing = False
                pygame.draw.rect(window, GRAY, i["rect"])
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
                grav += 1 * grav_dir
            game_speed += 0.1 / len(blocks)
            pygame.draw.rect(window, YELLOW, char)
            pygame.draw.rect(window, DARK_GREY, terrain)
            pygame.draw.rect(window, DARK_GREY, ceiling)
            if frame_count <= grace_period and frame_count % 20 >= 10:
                pygame.draw.rect(window, BLACK, char)
            score_counter += (game_speed + speed_up) / 7.5
            if high_score_temp < score_counter:
                high_score_temp = score_counter
            window.blit(score, score_rect)
            window.blit(high_score, high_score_rect)
            pygame.display.update()
            window.fill(BLACK)
            mainClock.tick(40)
    return high_score_temp


def checkOnGround(i, grav_dir):
    rect = i["rect"]
    if grav_dir > 0:
        if char.bottom <= rect.top + 20:
            return True
    else:
        if char.top >= rect.bottom - 20:
            return True
    return False


while True:
    highScoreSpace = spaceLevel()
    highScoreCloud = cloudLevel()
    highScoreDirt = dirtLevel()
