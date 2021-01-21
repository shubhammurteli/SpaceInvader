import pygame
import random
import math

from pygame import mixer


# Initialize the pygame
pygame.init()

# Creating window/screen for game (width, height)
screen = pygame.display.set_mode((800, 600))

# Background image
background = pygame.image.load("./assets/background.png")

# Background Sound
mixer.music.load('assets/bgmusic.mp3')
mixer.music.play(-1)
mixer.music.set_volume(0.1)

# Title and Icon of Window
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("./assets/ufo.png")
pygame.display.set_icon(icon)


# Defining player and its coordinates
playerImg = pygame.image.load("./assets/player.png")
playerX = 370
playerY = 480
playerX_change = 0


# Defining enemy and its coordinates
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = random.randint(4, 8)
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("./assets/enemy.png"))
    enemyX.append(random.randint(-4, 740))
    enemyY.append(random.randint(20, 150))
    enemyX_change.append(4.5)
    enemyY_change.append(40)

# Bullet image
bulletImg = pygame.image.load("./assets/bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"  # ready state means we can't see the bullet

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game Over font
over_font = pygame.font.Font('freesansbold.ttf', 64)

# Defining player object in function


def player(x, y):
    # Blit(image, (x-coordinate, y-coordinate))
    screen.blit(playerImg, (x, y))

# Defining enemy object in function


def enemy(x, y, i):
    # Blit(image, (x-coordinate, y-coordinate))
    screen.blit(enemyImg[i], (x, y))


def bullet_fire(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x+16, y))


def ifCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow((enemyX-bulletX), 2) +
                         math.pow((enemyY-bulletY), 2))
    if distance <= 27:
        return True
    return False


def game_over_text():
    game_over = over_font.render("GAME OVER!", True, (255, 255, 255))
    screen.blit(game_over, (200, 255))


def scoreBoard(x, y):
    score = font.render("Score:" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


# Game Loop (Here you add something you want it to run continously throught the game)
runlog = True  # Keeps the infinite loop running
while runlog:

    # Screen background RGB
    screen.fill((38, 38, 38))

    # Adding Background
    screen.blit(background, (0, 0))

    for event in pygame.event.get():  # pygame.event.get() gives list of all events happening in pygame screen
        if event.type == pygame.QUIT:  # Checks if close button is pressed or not
            runlog = False  # stops the loop

        # Check Keyboard Events to control player
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change -= 5

            if event.key == pygame.K_RIGHT:
                playerX_change += 5

            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('assets/laser.wav')
                    bullet_sound.play()
                    bullet_sound.set_volume(0.4)
                    bulletX = playerX  # Gets the current coordinate of player when spacebar was pressed
                    bullet_fire(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Changing player coordinates on key press
    playerX += playerX_change
    # Displaying Player on screen
    player(playerX, playerY)

    # Boundry condition for player
    if playerX <= -4:
        playerX = -4
    if playerX >= 740:
        playerX = 740

    # To display Multiple enemies on screen
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] >= 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        # Enemy Keeps moving
        enemyX[i] += enemyX_change[i]
        # Boundry condition for enemy
        if enemyX[i] <= -4:
            enemyX_change[i] = 4.5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 740:
            enemyX_change[i] = -4.5
            enemyY[i] += enemyY_change[i]

        # Collision Check
        collision = ifCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('assets/explosion.wav')
            explosion_sound.play()
            explosion_sound.set_volume(0.4)
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(-4, 740)
            enemyY[i] = random.randint(20, 150)

        # Displaying Enemy on Screen
        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        bullet_fire(bulletX, bulletY)
        bulletY -= bulletY_change
    # Showing Score
    scoreBoard(textX, textY)
    # To update any changes happening in Game Loop
    pygame.display.update()
