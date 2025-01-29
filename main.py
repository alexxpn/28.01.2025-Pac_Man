"""
PAC-MAN BY ALEXANDER PAN
ICS3U
January 20, 2025

This is an original replica of the authentic game. I tried to preserve most of the characteristics while incorporating some
new ideas and creativity into it.

SOURCES:
https://www.gamedeveloper.com/design/the-pac-man-dossier#close-modal [1]
Overall very helpful article detailing the history and basic mechanics behind Pac-Man.

https://gameinternals.com/understanding-pac-man-ghost-behavior [2]
Basis of many of my ideas I tried to incorporate, including a 2D-list tile-based board and player-tracking AI concepts.

https://open.spotify.com/track/5Jt6qtZfj0YSHfFBJUyviK?si=cd5cdffa4fb34a79 [3]
Pac-Man Theme Remix by Arsenic1987
Background music from spotify that gives a modern feel yet retains the original melody.

https://www.pygame.org/docs/genindex.html
pygame index of all commands used

https://docs.python.org/3/library/copy.html
copy library information for an immutable list

Special thanks to Angus Sun [4] and Timothy Wu [5] for helping me with logic for pathfinding and ghost behaviour.
"""

#importing all libraries
import copy
import pygame
from pygame import *
import random

#initializing pygame
pygame.init()

#defining width, height, setting up screen, screen title
WIDTH, HEIGHT = 900, 950
screen = display.set_mode((WIDTH, HEIGHT))
display.set_caption('PAC-MAN 2024 ALEXANDER PAN')

#defining colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREY = (127, 127, 127)

#dimensions and position of buttons/rectangles
startRect = Rect(400, 528, 100, 45)
tutorialRect = Rect(25,443,145,45)
textRect = Rect(250, 220, 400, 472)
smalltextRect = Rect(300, 356, 300, 220)
settingsRect = Rect(740, 443, 145, 45)
muteRect = Rect(355, 370, 200, 45)
sfxRect = Rect(365, 430, 180, 45)

#2D list of the entire maze:
#0 - empty, 1 - dots, 2 - power pellets, 3 - vertical line, 4 - horizontal line, 5 - top right corners, 6 - top left corners, 7 - bottom left corners, 8 - bottom right corners, 9 - gate
boards = [
[6, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5],
[3, 6, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 6, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 3],
[3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3],
[3, 3, 1, 6, 4, 4, 5, 1, 6, 4, 4, 4, 5, 1, 3, 3, 1, 6, 4, 4, 4, 5, 1, 6, 4, 4, 5, 1, 3, 3],
[3, 3, 2, 3, 0, 0, 3, 1, 3, 0, 0, 0, 3, 1, 3, 3, 1, 3, 0, 0, 0, 3, 1, 3, 0, 0, 3, 2, 3, 3],
[3, 3, 1, 7, 4, 4, 8, 1, 7, 4, 4, 4, 8, 1, 7, 8, 1, 7, 4, 4, 4, 8, 1, 7, 4, 4, 8, 1, 3, 3],
[3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3],
[3, 3, 1, 6, 4, 4, 5, 1, 6, 5, 1, 6, 4, 4, 4, 4, 4, 4, 5, 1, 6, 5, 1, 6, 4, 4, 5, 1, 3, 3],
[3, 3, 1, 7, 4, 4, 8, 1, 3, 3, 1, 7, 4, 4, 5, 6, 4, 4, 8, 1, 3, 3, 1, 7, 4, 4, 8, 1, 3, 3],
[3, 3, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 3, 3],
[3, 7, 4, 4, 4, 4, 5, 1, 3, 7, 4, 4, 5, 0, 3, 3, 0, 6, 4, 4, 8, 3, 1, 6, 4, 4, 4, 4, 8, 3],
[3, 0, 0, 0, 0, 0, 3, 1, 3, 6, 4, 4, 8, 0, 7, 8, 0, 7, 4, 4, 5, 3, 1, 3, 0, 0, 0, 0, 0, 3],
[3, 0, 0, 0, 0, 0, 3, 1, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 1, 3, 0, 0, 0, 0, 0, 3],
[8, 0, 0, 0, 0, 0, 3, 1, 3, 3, 0, 6, 4, 9, 9, 9, 9, 4, 5, 0, 3, 3, 1, 3, 0, 0, 0, 0, 0, 7],
[4, 4, 4, 4, 4, 4, 8, 1, 7, 8, 0, 3, 0, 0, 0, 0, 0, 0, 3, 0, 7, 8, 1, 7, 4, 4, 4, 4, 4, 4],
[0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
[4, 4, 4, 4, 4, 4, 5, 1, 6, 5, 0, 3, 0, 0, 0, 0, 0, 0, 3, 0, 6, 5, 1, 6, 4, 4, 4, 4, 4, 4],
[5, 0, 0, 0, 0, 0, 3, 1, 3, 3, 0, 7, 4, 4, 4, 4, 4, 4, 8, 0, 3, 3, 1, 3, 0, 0, 0, 0, 0, 6],
[3, 0, 0, 0, 0, 0, 3, 1, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 1, 3, 0, 0, 0, 0, 0, 3],
[3, 0, 0, 0, 0, 0, 3, 1, 3, 3, 0, 6, 4, 4, 4, 4, 4, 4, 5, 0, 3, 3, 1, 3, 0, 0, 0, 0, 0, 3],
[3, 6, 4, 4, 4, 4, 8, 1, 7, 8, 0, 7, 4, 4, 5, 6, 4, 4, 8, 0, 7, 8, 1, 7, 4, 4, 4, 4, 5, 3],
[3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3],
[3, 3, 1, 6, 4, 4, 5, 1, 6, 4, 4, 4, 5, 1, 3, 3, 1, 6, 4, 4, 4, 5, 1, 6, 4, 4, 5, 1, 3, 3],
[3, 3, 1, 7, 4, 5, 3, 1, 7, 4, 4, 4, 8, 1, 7, 8, 1, 7, 4, 4, 4, 8, 1, 3, 6, 4, 8, 1, 3, 3],
[3, 3, 2, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 2, 3, 3],
[3, 7, 4, 5, 1, 3, 3, 1, 6, 5, 1, 6, 4, 4, 4, 4, 4, 4, 5, 1, 6, 5, 1, 3, 3, 1, 6, 4, 8, 3],
[3, 6, 4, 8, 1, 7, 8, 1, 3, 3, 1, 7, 4, 4, 5, 6, 4, 4, 8, 1, 3, 3, 1, 7, 8, 1, 7, 4, 5, 3],
[3, 3, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 3, 3],
[3, 3, 1, 6, 4, 4, 4, 4, 8, 7, 4, 4, 5, 1, 3, 3, 1, 6, 4, 4, 8, 7, 4, 4, 4, 4, 5, 1, 3, 3],
[3, 3, 1, 7, 4, 4, 4, 4, 4, 4, 4, 4, 8, 1, 7, 8, 1, 7, 4, 4, 4, 4, 4, 4, 4, 4, 8, 1, 3, 3],
[3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3],
[3, 7, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 8, 3],
[7, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 8]
         ]

#setting up frames and clock, level colour, font, level map
myClock = time.Clock()
fps = 60
lvlcolour = BLUE
font = font.Font("assets/fonts/retrogaming.ttf", 20)
level = copy.deepcopy(boards)
levels = 1

#defining game states
running = True
startup = True
tutorial = False
settings = False
gameovertext = False
gameover = False
gamewon = False

#music booleans
music = True
sfx = True

#player size and ghost size
playersize = 45
ghostsize = 45

#music and sound effects [3]
mixer.music.load('assets/music/theme.mp3')
mixer.music.set_volume(0.3)
mixer.music.play(-1)
beeps = mixer.Sound('assets/music/beeps.mp3')
death = mixer.Sound('assets/music/death.wav')
chomp1 = mixer.Sound('assets/music/chomp1.mp3')
chomp2 = mixer.Sound('assets/music/chomp2.mp3')
eat = mixer.Sound('assets/music/eat.wav')
siren = mixer.Sound('assets/music/siren.mp3')
gover = mixer.Sound('assets/music/gameover.wav')

#initial volume of all sounds
beeps.set_volume(0.9)
death.set_volume(0.9)
chomp1.set_volume(0.9)
chomp2.set_volume(0.9)
eat.set_volume(0.5)
siren.set_volume(0.9)
gover.set_volume(0.9)

#high score file logic
highscorefile = open("assets/data/highscore.txt", "r")
highscore = int(highscorefile.read().strip())
highscorefile.close()

#lists for bliting differing images depending on direction
playerimgs = []
for i in range(1, 5):
    img = image.load(f"assets/player/{i}.png")
    scaledimg = transform.scale(img, (playersize, playersize))
    playerimgs.append(scaledimg)
blinkyimgs = []
for i in range(1, 5):
    blinkyimg = image.load(f"assets/enemies/blinky/{i}.png")
    blinky = transform.scale(blinkyimg, (ghostsize, ghostsize))
    blinkyimgs.append(blinky)
pinkyimgs = []
for i in range(1, 5):
    pinkyimg = image.load(f"assets/enemies/pinky/{i}.png")
    blinky = transform.scale(pinkyimg, (ghostsize, ghostsize))
    pinkyimgs.append(blinky)
inkyimgs = []
for i in range(1, 5):
    inkyimg = image.load(f"assets/enemies/inky/{i}.png")
    inky = transform.scale(inkyimg, (ghostsize, ghostsize))
    inkyimgs.append(inky)
clydeimgs = []
for i in range(1, 5):
    clydeimg = image.load(f"assets/enemies/clyde/{i}.png")
    clyde = transform.scale(clydeimg, (ghostsize, ghostsize))
    clydeimgs.append(clyde)
spookedimgs = []
for i in range(1, 5):
    spookedimg = image.load(f"assets/enemies/spooked/{i}.png")
    spooked = transform.scale(spookedimg, (ghostsize, ghostsize))
    spookedimgs.append(spooked)
deadimgs = []
for i in range(1, 5):
    deadimg = image.load(f"assets/enemies/dead/{i}.png")
    dead = transform.scale(deadimg, (ghostsize, ghostsize))
    deadimgs.append(dead)
changeimgs = []
for i in range (1,5):
    changeimg = image.load(f"assets/enemies/changing/{i}.png")
    change = transform.scale(changeimg, (ghostsize, ghostsize))
    changeimgs.append(change)

#starting positions of player and ghosts
blinkyx = 427
blinkyy = 357
blinkydirection = 0
inkyx = 489
inkyy = 442
inkydirection = 2
pinkyx = 428
pinkyy = 442
pinkydirection = 2
clydex = 365
clydey = 442
clydedirection = 2
playerx = 427
playery = 693
plyrdirection = 0

#counters, flickering boolean, valid turns for player, starting direction, speeds
counter = 0
flicker = False
validturns = [False, False, False, False]  # R,L,U,D
plyrdirection_cmmd = 0
plyrspeed = 3
ghostspeeds = [3,3,3,3]
score = 0
powerup = False
powerupcounter = 0
dotcounter = 0
sirencounter = 0

startupcounter = 0
playing = False
moving = False
lives = 2

#game mode booleans + counters
chasecounter = 0
spooked = False
chasing = False
scattering = False

#ghost states
blinkydead = False
pinkydead = False
inkydead = False
clydedead = False

blinkyspooked = False
pinkyspooked = False
inkyspooked = False
clydespooked = False

blinkyinbox = False
pinkyinbox = True
inkyinbox = True
clydeinbox = True

#how many ghosts have been eaten for incremental points
eatenghosts = [False, False, False, False]

def drawboard(): #draws the board according to the 2D list
    theight = ((HEIGHT - 50) // 32) #height of 1 tiles
    twidth = (WIDTH // 30) #width of 1 tile
    for i in range(len(level)): #for each row in level
        for j in range(len(level[i])): #in each column
            if level[i][j] == 1: #draws a small dot
                draw.circle(screen, WHITE, (j * twidth + (0.5 * twidth), i * theight + (0.5 * theight) + 30), 4)
            if level[i][j] == 2 and not flicker: #draws the power pellet
                draw.circle(screen, WHITE, (j * twidth + (0.5 * twidth), i * theight + (0.5 * theight) + 30), 10)
            if level[i][j] == 3: #draws a vertical line
                draw.line(screen, lvlcolour, (j * twidth + (0.5 * twidth), i * theight + 30),
                          (j * twidth + (0.5 * twidth), i * theight + theight + 30), 3)
            if level[i][j] == 4: #draws a horizontal line
                draw.line(screen, lvlcolour, (j * twidth, i * theight + (0.5 * theight) + 30),
                          (j * twidth + twidth, i * theight + (0.5 * theight) + 30), 3)
            if level[i][j] == 5: #draws top right corners
                midleft = (j * twidth, i * theight + theight / 2 + 30)
                midbottom = (j * twidth + twidth / 2, i * theight + theight + 30)
                draw.line(screen, lvlcolour, midleft, midbottom, 4)
            if level[i][j] == 6: #draws top left corners
                midbottom = (j * twidth + twidth / 2, i * theight + theight + 30)
                midright = (j * twidth + twidth, i * theight + theight / 2 + 30)
                draw.line(screen, lvlcolour, midbottom, midright, 4)
            if level[i][j] == 7: #draws bottom left corners
                midtop = (j * twidth + twidth / 2, i * theight + 30)
                midright = (j * twidth + twidth, i * theight + theight / 2 + 30)
                draw.line(screen, lvlcolour, midtop, midright, 4)
            if level[i][j] == 8: #draws bottom right corners
                midtop = (j * twidth + twidth / 2, i * theight + 30)
                midleft = (j * twidth, i * theight + theight / 2 + 30)
                draw.line(screen, lvlcolour, midtop, midleft, 4)
            if level[i][j] == 9: #draws ghost gate
                draw.line(screen, WHITE, (j * twidth, i * theight + (0.5 * theight) + 30),
                          (j * twidth + twidth, i * theight + (0.5 * theight) + 30), 3)
def drawplayer(): #drawing the player depending on the direction
    if plyrdirection == 0:
        screen.blit(playerimgs[counter // 5], (playerx, playery))
    if plyrdirection == 1:
        screen.blit(transform.flip(playerimgs[counter // 5], True, False), (playerx, playery))
    if plyrdirection == 2:
        screen.blit(transform.rotate(playerimgs[counter // 5], 90), (playerx, playery))
    if plyrdirection == 3:
        screen.blit(transform.rotate(playerimgs[counter // 5], -90), (playerx, playery))
def checkpos(cx, cy): #checks for valid turns given an x,y coordinate
    turns = [False, False, False, False] #initial list
    theight = (HEIGHT - 50) // 32 #height of a tile
    twidth = (WIDTH // 30) #width of one tile
    num3 = 15 #margin number for adjustments
    #checks collisions based on center x and center y of player +/- margin
    if cx // 30 < 29: #must be within the tiles shown on screen
        if plyrdirection == 0:
            if level[(cy - 30) // theight][(cx - num3) // twidth] < 3:
                turns[1] = True
        if plyrdirection == 1:
            if level[(cy - 30) // theight][(cx + num3) // twidth] < 3:
                turns[0] = True
        if plyrdirection == 2:
            if level[((cy - 30) + num3) // theight][cx // twidth] < 3:
                turns[3] = True
        if plyrdirection == 3:
            if level[((cy - 30) - num3) // theight][cx // twidth] < 3:
                turns[2] = True
        if plyrdirection == 2 or plyrdirection == 3:
            if 10 <= cx % twidth <= 20:
                if level[((cy - 30) + num3) // theight][cx // twidth] < 3:
                    turns[3] = True
                if level[((cy - 30) - num3) // theight][cx // twidth] < 3:
                    turns[2] = True
            if 10 <= (cy - 30) % theight <= 20:
                if level[(cy - 30) // theight][(cx - twidth) // twidth] < 3:
                    turns[1] = True
                if level[(cy - 30) // theight][(cx + twidth) // twidth] < 3:
                    turns[0] = True
        if plyrdirection == 0 or plyrdirection == 1:
            if 10 <= cx % twidth <= 20:
                if level[((cy - 30) + theight) // theight][cx // twidth] < 3:
                    turns[3] = True
                if level[((cy - 30) - theight) // theight][cx // twidth] < 3:
                    turns[2] = True
            if 10 <= (cy - 30) % theight <= 20:
                if level[(cy - 30) // theight][(cx - num3) // twidth] < 3:
                    turns[1] = True
                if level[(cy - 30) // theight][(cx + num3) // twidth] < 3:
                    turns[0] = True
    else:
        turns[0] = True
        turns[1] = True

    return turns
def moveplyr(playx, playy):
    # rlud
    if plyrdirection == 0 and validturns[0]:
        playx += plyrspeed
    elif plyrdirection == 1 and validturns[1]:
        playx -= plyrspeed
    if plyrdirection == 2 and validturns[2]:
        playy -= plyrspeed
    elif plyrdirection == 3 and validturns[3]:
        playy += plyrspeed
    return playx, playy
def checkcol(s, powerdot, powerdotcounter, eaten, levelc): #checks for collisions between player and dots/ghosts for points. updates the score
    global spooked
    global dotcounter
    theight = (HEIGHT - 50) // 32  #tile height
    twidth = WIDTH // 30  #tile width

    scale = 1 + (levelc // 5) * 0.1  #every 5 levels, increase by 10%

    if 0 < playerx < 870:
        if level[(centery - 30) // theight][centerx // twidth] == 1:  #small dot
            level[(centery - 30) // theight][centerx // twidth] = 0  #changes it to empty space
            s += int(10 * scale)  #scale the points for small dot

            #playing the sound effect based on every other dot eaten like the original game
            if dotcounter % 2 == 0:
                chomp1.play()
            else:
                chomp2.play()
            dotcounter += 1

        if level[(centery - 30) // theight][centerx // twidth] == 2:  #big power pellet/dot
            level[(centery - 30) // theight][centerx // twidth] = 0
            s += int(50 * scale)  #scale the points for big dot
            powerdot = True
            powerdotcounter = 0  #for the timing
            eaten = [False, False, False, False]  #cleans up the eaten list for usage

    return s, powerdot, powerdotcounter, eaten

def drawmisc(): #draws score, high score, lives, and levels
    scoretext = font.render(f'Score: {score}', True, WHITE)
    screen.blit(scoretext, (10, 10))
    highscoretext = font.render(f'HIGH SCORE: {highscore}', True, WHITE)
    htextw = highscoretext.get_width()
    hxpos = (WIDTH - htextw) // 2
    screen.blit(highscoretext, (hxpos, 10))

    leveltext = font.render(f'LEVEL {levels}', True, WHITE)
    ltextw = leveltext.get_width()
    lxpos = WIDTH - ltextw - 130
    screen.blit(leveltext, (lxpos, 10))

    for life in range(lives+1):
        screen.blit(pygame.transform.scale(playerimgs[0], (30, 30)), (780 + life * 40, 8))

#DRAWS GHOSTS DEPENDING ON DIRECTION AND STATE: NORMAL, SPOOKED, AND DEAD (very similar to draw player)
def drawblinky():
    bcenterx = blinkyx + 23
    bcentery = blinkyy + 23
    if not blinkyspooked and not blinkydead:
        if blinkydirection == 0:
            screen.blit(blinkyimgs[0], (blinkyx, blinkyy))
        if blinkydirection == 1:
            screen.blit(blinkyimgs[1], (blinkyx, blinkyy))
        if blinkydirection == 2:
            screen.blit(blinkyimgs[2], (blinkyx, blinkyy))
        if blinkydirection == 3:
            screen.blit(blinkyimgs[3], (blinkyx, blinkyy))
    if blinkydead:
        if blinkydirection == 0:
            screen.blit(deadimgs[0], (blinkyx, blinkyy))
        if blinkydirection == 1:
            screen.blit(deadimgs[1], (blinkyx, blinkyy))
        if blinkydirection == 2:
            screen.blit(deadimgs[2], (blinkyx, blinkyy))
        if blinkydirection == 3:
            screen.blit(deadimgs[3], (blinkyx, blinkyy))
    elif blinkyspooked:
        if blinkydirection == 0:
            screen.blit(spookedimgs[0], (blinkyx, blinkyy))
        if blinkydirection == 1:
            screen.blit(spookedimgs[1], (blinkyx, blinkyy))
        if blinkydirection == 2:
            screen.blit(spookedimgs[2], (blinkyx, blinkyy))
        if blinkydirection == 3:
            screen.blit(spookedimgs[3], (blinkyx, blinkyy))
def drawpinky():
    if not pinkyspooked and not pinkydead:
        if pinkydirection == 0:
            screen.blit(pinkyimgs[0], (pinkyx, pinkyy))
        if pinkydirection == 1:
            screen.blit(pinkyimgs[1], (pinkyx, pinkyy))
        if pinkydirection == 2:
            screen.blit(pinkyimgs[2], (pinkyx, pinkyy))
        if pinkydirection == 3:
            screen.blit(pinkyimgs[3], (pinkyx, pinkyy))
    if pinkydead:
        if pinkydirection == 0:
            screen.blit(deadimgs[0], (pinkyx, pinkyy))
        if pinkydirection == 1:
            screen.blit(deadimgs[1], (pinkyx, pinkyy))
        if pinkydirection == 2:
            screen.blit(deadimgs[2], (pinkyx, pinkyy))
        if pinkydirection == 3:
            screen.blit(deadimgs[3], (pinkyx, pinkyy))
    elif pinkyspooked:
        if pinkydirection == 0:
            screen.blit(spookedimgs[0], (pinkyx, pinkyy))
        if pinkydirection == 1:
            screen.blit(spookedimgs[1], (pinkyx, pinkyy))
        if pinkydirection == 2:
            screen.blit(spookedimgs[2], (pinkyx, pinkyy))
        if pinkydirection == 3:
            screen.blit(spookedimgs[3], (pinkyx, pinkyy))
def drawinky():
    if not inkyspooked and not inkydead:
        if inkydirection == 0:
            screen.blit(inkyimgs[0], (inkyx, inkyy))
        if inkydirection == 1:
            screen.blit(inkyimgs[1], (inkyx, inkyy))
        if inkydirection == 2:
            screen.blit(inkyimgs[2], (inkyx, inkyy))
        if inkydirection == 3:
            screen.blit(inkyimgs[3], (inkyx, inkyy))
    if inkydead:
        if inkydirection == 0:
            screen.blit(deadimgs[0], (inkyx, inkyy))
        if inkydirection == 1:
            screen.blit(deadimgs[1], (inkyx, inkyy))
        if inkydirection == 2:
            screen.blit(deadimgs[2], (inkyx, inkyy))
        if inkydirection == 3:
            screen.blit(deadimgs[3], (inkyx, inkyy))
    elif inkyspooked:
        if inkydirection == 0:
            screen.blit(spookedimgs[0], (inkyx, inkyy))
        if inkydirection == 1:
            screen.blit(spookedimgs[1], (inkyx, inkyy))
        if inkydirection == 2:
            screen.blit(spookedimgs[2], (inkyx, inkyy))
        if inkydirection == 3:
            screen.blit(spookedimgs[3], (inkyx, inkyy))
def drawclyde():
    if not clydespooked and not clydedead:
        if clydedirection == 0:
            screen.blit(clydeimgs[0], (clydex, clydey))
        if clydedirection == 1:
            screen.blit(clydeimgs[1], (clydex, clydey))
        if clydedirection == 2:
            screen.blit(clydeimgs[2], (clydex, clydey))
        if clydedirection == 3:
            screen.blit(clydeimgs[3], (clydex, clydey))
    if clydedead:
        if clydedirection == 0:
            screen.blit(deadimgs[0], (clydex, clydey))
        if clydedirection == 1:
            screen.blit(deadimgs[1], (clydex, clydey))
        if clydedirection == 2:
            screen.blit(deadimgs[2], (clydex, clydey))
        if clydedirection == 3:
            screen.blit(deadimgs[3], (clydex, clydey))
    elif clydespooked:
        if clydedirection == 0:
            screen.blit(spookedimgs[0], (clydex, clydey))
        if clydedirection == 1:
            screen.blit(spookedimgs[1], (clydex, clydey))
        if clydedirection == 2:
            screen.blit(spookedimgs[2], (clydex, clydey))
        if clydedirection == 3:
            screen.blit(spookedimgs[3], (clydex, clydey))

#[4], [5]
def checkghostpos(cx, cy, gdirection, ginbox, gdead): #similar to player's, checks for valid turns. smaller margins for less errors/bugs
    turns = [False, False, False, False]
    h = (HEIGHT - 50) // 32  # height of one tile
    w = (WIDTH // 30)  # width of one tile
    # check collisions based on center x and center y of ghost +/- margin number
    if 0 < cx // 30 < 29:
        if level[((cy-30) - h) // h][cx // w] == 9:
            turns[2] = True
            turns[3] = True
        if level[((cy-30) + h) // h][cx // w] == 9 and gdead:
            turns[3] = True
            turns[2] = True
        if gdirection == 0:
            if level[(cy-30) // h][(cx - w) // w] < 3 or (level[(cy-30) // h][(cx - w) // w] == 9 and (ginbox or gdead)):
                turns[1] = True
        elif gdirection == 1:
            if level[(cy-30) // h][(cx + w) // w] < 3 or (level[(cy-30) // h][(cx + w) // w] == 9 and (ginbox or gdead)):
                turns[0] = True
        elif gdirection == 2:
            if level[((cy-30) + h) // h][cx // w] < 3 or (level[((cy-30) + h) // h][cx // w] == 9 and (ginbox or gdead)):
                turns[3] = True
        elif gdirection == 3:
            if level[((cy-30) - h) // h][cx // w] < 3 or (level[((cy-30) - h) // h][cx // w] == 9 and (ginbox or gdead)):
                turns[2] = True

        if gdirection == 0 or gdirection == 1:
            if 15 <= cx % w <= 17:
                if level[((cy-30) + h) // h][cx // w] < 3 or (level[((cy-30) + h) // h][cx // w] == 9 and (ginbox or gdead)):
                    turns[3] = True
                if level[((cy-30) - h) // h][cx // w] < 3 or (level[((cy-30) - h) // h][cx // w] == 9 and (ginbox or  gdead)):
                    turns[2] = True
            if 15 <= cy % h <= 17:
                if level[(cy-30) // h][(cx - w) // w] < 3 or (level[(cy-30) // h][(cx - w) // w] == 9 and (ginbox or gdead)):
                    turns[1] = True
                if level[(cy-30) // h][(cx + w) // w] < 3 or (level[(cy-30) // h][(cx + w) // w] == 9 and (ginbox or gdead)):
                    turns[0] = True
        if gdirection == 2 or gdirection == 3:
            if 15 <= cx % h <= 17:
                if level[((cy-30) + h) // h][cx // w] < 3 or (level[((cy-30) + h) // h][cx // w] == 9 and (ginbox or gdead)):
                    turns[3] = True
                if level[((cy-30) - h) // h][cx // w] < 3 or (level[((cy-30) - h) // h][cx // w] == 9 and (ginbox or gdead)):
                    turns[2] = True
            if 15 <= cy % h <= 17:
                if level[(cy-30) // h][(cx - w) // w] < 3 or (level[(cy-30) // h][(cx - w) // w] == 9 and (ginbox or gdead)):
                    turns[1] = True
                if level[(cy-30) // h][(cx + w) // w] < 3 or (level[(cy-30) // h][(cx + w) // w] == 9 and (ginbox or gdead)):
                    turns[0] = True
    else:
        turns[0] = True
        turns[1] = True
    return turns
def checkbox(gx, gy): #checks if the ghost is in the box given x,y coords
    if 350 < gx < 550 and 380 < gy < 460:
        inbox = True
    else:
        inbox = False
    return inbox

#[2], [5]
def moveghost(gx, gy, tx, ty, ghostdirection, turns, gspeed): #moves ghosts towards a target x,y using the distance formula
    # RLUD
    dx = [1, -1, 0, 0] #right or left
    dy = [0, 0, -1, 1] #up or down
    shortest = float("inf") #shortest length is set to infinite for start
    bestdirection = ghostdirection #best direction is set to current direction

    if ghostdirection == 0:
        #checks all possible turns (does not allow to backtrack/reverse direction)
        if turns[0]:
            #simulates new coordinates if the turn is completed
            newx = gx + dx[0] * 30
            newy = gy + dy[0] * 32
            dist = ((tx - newx) ** 2 + (ty - newy) ** 2) ** 0.5 #uses distance formula to calculate the distance to the target
            if dist < shortest: #if it is the shortest, then update that to the best turn/direction
                shortest = dist
                bestdirection = 0
        if turns[2]:
            newx = gx + dx[2] * 30
            newy = gy + dy[2] * 32
            dist = ((tx - newx) ** 2 + (ty - newy) ** 2) ** 0.5
            if dist < shortest:
                shortest = dist
                bestdirection = 2
        if turns[3]:
            newx = gx + dx[3] * 30
            newy = gy + dy[3] * 32
            dist = ((tx - newx) ** 2 + (ty - newy) ** 2) ** 0.5
            if dist < shortest:
                shortest = dist
                bestdirection = 3

    if ghostdirection == 1:
        if turns[1]:
            newx = gx + dx[1] * 30
            newy = gy + dy[1] * 32
            dist = ((tx - newx) ** 2 + (ty - newy) ** 2) ** 0.5
            if dist < shortest:
                shortest = dist
                bestdirection = 1
        if turns[2]:
            newx = gx + dx[2] * 30
            newy = gy + dy[2] * 32
            dist = ((tx - newx) ** 2 + (ty - newy) ** 2) ** 0.5
            if dist < shortest:
                shortest = dist
                bestdirection = 2
        if turns[3]:
            newx = gx + dx[3] * 30
            newy = gy + dy[3] * 32
            dist = ((tx - newx) ** 2 + (ty - newy) ** 2) ** 0.5
            if dist < shortest:
                shortest = dist
                bestdirection = 3
    if ghostdirection == 2:
        if turns[0]:
            newx = gx + dx[0] * 30
            newy = gy + dy[0] * 32
            dist = ((tx - newx) ** 2 + (ty - newy) ** 2) ** 0.5
            if dist < shortest:
                shortest = dist
                bestdirection = 0
        if turns[1]:
            newx = gx + dx[1] * 30
            newy = gy + dy[1] * 32
            dist = ((tx - newx) ** 2 + (ty - newy) ** 2) ** 0.5
            if dist < shortest:
                shortest = dist
                bestdirection = 1
        if turns[2]:
            newx = gx + dx[2] * 30
            newy = gy + dy[2] * 32
            dist = ((tx - newx) ** 2 + (ty - newy) ** 2) ** 0.5
            if dist < shortest:
                shortest = dist
                bestdirection = 2
    if ghostdirection == 3:
        if turns[0]:
            newx = gx + dx[0] * 30
            newy = gy + dy[0] * 32
            dist = ((tx - newx) ** 2 + (ty - newy) ** 2) ** 0.5
            if dist < shortest:
                shortest = dist
                bestdirection = 0
        if turns[1]:
            newx = gx + dx[1] * 30
            newy = gy + dy[1] * 32
            dist = ((tx - newx) ** 2 + (ty - newy) ** 2) ** 0.5
            if dist < shortest:
                shortest = dist
                bestdirection = 1
        if turns[3]:
            newx = gx + dx[3] * 30
            newy = gy + dy[3] * 32
            dist = ((tx - newx) ** 2 + (ty - newy) ** 2) ** 0.5
            if dist < shortest:
                shortest = dist
                bestdirection = 3

    ghostdirection = bestdirection

    if ghostdirection == 0:
        gx += gspeed #right
    if ghostdirection == 1:
        gx -= gspeed #left
    if ghostdirection == 2:
        gy -= gspeed #up
    if ghostdirection == 3:
        gy += gspeed #down

    return gx, gy, ghostdirection
def movespooked(gx, gy, gdirection, turns, sspeed): #similar to move ghost, except turns are random so no targets
    if gdirection < 2:
        opposite = (gdirection + 1) % 2 #finds the opposite direction to exclude it (right/left)
    else:
        opposite = (gdirection + 1) % 2 + 2 #up/down
    valid = [i for i in range(4) if turns[i] and i != opposite] #checks all valid directions

    if valid:
        new = random.choice(valid)
        gdirection = new

    # Move the ghost in the chosen direction
    if gdirection == 0:
        gx += sspeed
    elif gdirection == 1:
        gx -= sspeed
    elif gdirection == 2:
        gy -= sspeed
    elif gdirection == 3:
        gy += sspeed

    return gx, gy, gdirection
def movedead(gx, gy, ghostdirection, turns, gspeed): #similar to move ghost, but there's two different targets depending on which side of the board the ghost is on (due to bugs)
    # RLUD
    dx = [1, -1, 0, 0]
    dy = [0, 0, -1, 1]
    shortest = float("inf")
    bestdirection = ghostdirection

    if gx <= 450:
        tx = 473
    if gx > 450:
        tx = 427
    ty = 400

    if ghostdirection == 0:
        if turns[0]:
            newx = gx + dx[0] * 30
            newy = gy + dy[0] * 32
            dist = ((tx - newx) ** 2 + (ty - newy) ** 2) ** 0.5
            if dist < shortest:
                shortest = dist
                bestdirection = 0
        if turns[2]:
            newx = gx + dx[2] * 30
            newy = gy + dy[2] * 32
            dist = ((tx - newx) ** 2 + (ty - newy) ** 2) ** 0.5
            if dist < shortest:
                shortest = dist
                bestdirection = 2
        if turns[3]:
            newx = gx + dx[3] * 30
            newy = gy + dy[3] * 32
            dist = ((tx - newx) ** 2 + (ty - newy) ** 2) ** 0.5
            if dist < shortest:
                shortest = dist
                bestdirection = 3

    if ghostdirection == 1:
        if turns[1]:
            newx = gx + dx[1] * 30
            newy = gy + dy[1] * 32
            dist = ((tx - newx) ** 2 + (ty - newy) ** 2) ** 0.5
            if dist < shortest:
                shortest = dist
                bestdirection = 1
        if turns[2]:
            newx = gx + dx[2] * 30
            newy = gy + dy[2] * 32
            dist = ((tx - newx) ** 2 + (ty - newy) ** 2) ** 0.5
            if dist < shortest:
                shortest = dist
                bestdirection = 2
        if turns[3]:
            newx = gx + dx[3] * 30
            newy = gy + dy[3] * 32
            dist = ((tx - newx) ** 2 + (ty - newy) ** 2) ** 0.5
            if dist < shortest:
                shortest = dist
                bestdirection = 3
    if ghostdirection == 2:
        if turns[0]:
            newx = gx + dx[0] * 30
            newy = gy + dy[0] * 32
            dist = ((tx - newx) ** 2 + (ty - newy) ** 2) ** 0.5
            if dist < shortest:
                shortest = dist
                bestdirection = 0
        if turns[1]:
            newx = gx + dx[1] * 30
            newy = gy + dy[1] * 32
            dist = ((tx - newx) ** 2 + (ty - newy) ** 2) ** 0.5
            if dist < shortest:
                shortest = dist
                bestdirection = 1
        if turns[2]:
            newx = gx + dx[2] * 30
            newy = gy + dy[2] * 32
            dist = ((tx - newx) ** 2 + (ty - newy) ** 2) ** 0.5
            if dist < shortest:
                shortest = dist
                bestdirection = 2
    if ghostdirection == 3:
        if turns[0]:
            newx = gx + dx[0] * 30
            newy = gy + dy[0] * 32
            dist = ((tx - newx) ** 2 + (ty - newy) ** 2) ** 0.5
            if dist < shortest:
                shortest = dist
                bestdirection = 0
        if turns[1]:
            newx = gx + dx[1] * 30
            newy = gy + dy[1] * 32
            dist = ((tx - newx) ** 2 + (ty - newy) ** 2) ** 0.5
            if dist < shortest:
                shortest = dist
                bestdirection = 1
        if turns[3]:
            newx = gx + dx[3] * 30
            newy = gy + dy[3] * 32
            dist = ((tx - newx) ** 2 + (ty - newy) ** 2) ** 0.5
            if dist < shortest:
                shortest = dist
                bestdirection = 3

    ghostdirection = bestdirection

    if ghostdirection == 0:
        gx += gspeed
    if ghostdirection == 1:
        gx -= gspeed
    if ghostdirection == 2:
        gy -= gspeed
    if ghostdirection == 3:
        gy += gspeed

    return gx, gy, ghostdirection

#finding targets for each ghost for personalities
def pinkytarget(): #4 tiles ahead of Pac-Man
    if plyrdirection == 0:
        tx = centerx + 4*30
        ty = centery
    if plyrdirection == 1:
        tx = centerx - 4*30
        ty = centery
    if plyrdirection == 2: #in the original game there is an overflow error where if pacman faces up the target is also 4 tiles to the left
        tx = centerx - 4*30
        ty = centery - 4*32
    if plyrdirection == 3:
        tx = centerx
        ty = centery + 4*32
    return tx, ty
def inkytarget(): #uses Blinky position and distance from pac man
    #checks two tiles ahead of pac man
    if plyrdirection == 0:
        frontx = playerx + 2 * 30
        fronty = playery
    elif plyrdirection == 1:
        frontx = playerx - 2 * 30
        fronty = playery
    elif plyrdirection == 2: #in the original game there is an overflow error where when pacman is facing up the target is also two tiles to the left
        frontx = playerx - 2 * 30
        fronty = playery - 2 * 32
    elif plyrdirection == 3:
        frontx = playerx
        fronty = playery + 2 * 32

    #finds the vector from blinky position to that tile
    vectorx = frontx - blinkyx
    vectory = fronty - blinkyy

    #doubles that distance, and the end of the vector is inky target
    tx = blinkyx + 2 * vectorx
    ty = blinkyy + 2 * vectory

    return tx, ty
def clydetarget(): #clyde's target is pacman unless he is within 8 tiles: otherwise he runs away to a corner
    if ((clydex - centerx) ** 2 + (clydey - centery) ** 2) ** 0.5 > 8: #if the distance is more than 8 tiles
        tx = centerx
        ty = centery
    elif ((clydex - centerx) ** 2 + (clydey - centery) ** 2) ** 0.5 <= 8: #if the distance is less than 8 tiles
        tx = 56
        ty = 842
    return tx, ty

def writehighscore(newhighscore): #updates high score
    newhighscorefile = open("assets/data/highscore.txt", "w")
    newhighscorefile.write(str(newhighscore))

while running:
    for evt in event.get():
        if evt.type == QUIT:
            running = False
        if evt.type == KEYDOWN:
            if evt.key == K_RIGHT:
                plyrdirection_cmmd = 0 #sends that the player wants to turn right
            if evt.key == K_LEFT:
                plyrdirection_cmmd = 1 #sends that the player wants to turn left
            if evt.key == K_UP:
                plyrdirection_cmmd = 2 #sends that the player wants to turn up
            if evt.key == K_DOWN:
                plyrdirection_cmmd = 3 #sends that the player wants to turn down
            if evt.key == K_SPACE:
                tutorial = False #closes tutorial page
                settings = False #closes settings page
                gameovertext = False #closes game over page
                score = 0 #resets the score
        if evt.type == KEYUP: #cancels player direction command if the button is released (player changes their mind)
            if evt.key == K_RIGHT and plyrdirection_cmmd == 0:
                plyrdirection_cmmd = plyrdirection
            if evt.key == K_LEFT and plyrdirection_cmmd == 1:
                plyrdirection_cmmd = plyrdirection
            if evt.key == K_UP and plyrdirection_cmmd == 2:
                plyrdirection_cmmd = plyrdirection
            if evt.key == K_DOWN and plyrdirection_cmmd == 3:
                plyrdirection_cmmd = plyrdirection
        if evt.type == MOUSEBUTTONUP:
            if muteRect.collidepoint(mx, my):
                if music:
                    music = False
                    mixer_music.pause()
                    siren.set_volume(0)
                else:
                    music = True
                    mixer_music.unpause()
                    siren.set_volume(0.5)
            if sfxRect.collidepoint(mx, my):
                if sfx:
                    sfx = False
                    beeps.set_volume(0)
                    death.set_volume(0)
                    chomp1.set_volume(0)
                    chomp2.set_volume(0)
                    eat.set_volume(0)
                    siren.set_volume(0)
                    gover.set_volume(0)
                else:
                    sfx = True
                    beeps.set_volume(0.9)
                    death.set_volume(0.9)
                    chomp1.set_volume(0.9)
                    chomp2.set_volume(0.9)
                    eat.set_volume(0.5)
                    siren.set_volume(0.9)
                    gover.set_volume(0.9)

    mx, my = mouse.get_pos() #gets the x,y coordinates of the mouse
    mb = mouse.get_pressed() #checks if the mouse is clicked

    # CONSTANTLY RUNS TO CHECK IF THE PLAYER IS TRYING TO TURN
    for i in range(0, 4):
        if plyrdirection_cmmd == i and validturns[i]:
            plyrdirection = i

    # TELEPORTING HALLWAY FEATURE
    if playerx > 900:
        playerx = -47
    elif playerx < -50:
        playerx = 897
    if blinkyx > 900:
        blinkyx = -30
    elif blinkyx < -30:
        blinkyx = 900
    if pinkyx > 900:
        pinkyx = -30
    elif pinkyx < -30:
        pinkyx = 900
    if inkyx > 900:
        inkyx = -30
    elif inkyx < -30:
        inkyx = 900
    if clydex > 900:
        clydex = -30
    elif clydex < -30:
        clydex = 900

    # UPDATING SCREEN
    screen.fill(BLACK)

    # DRAWING MAZE
    drawboard()
    drawplayer()
    drawmisc()

    # DRAWING GHOSTS
    drawblinky()
    drawpinky()
    drawinky()
    drawclyde()

    #IF THERE IS NO MORE DOTS THE GAME MOVES TO THE NEXT LEVEL
    gamewon = True
    for i in range(len(level)):
        if 1 in level[i] or 2 in level[i]:
            gamewon = False

    # FLICKER EFFECT
    if counter < 19:
        counter += 1
        if counter > 3:
            flicker = False
    else:
        counter = 0
        flicker = True

    #STARTUP SETUP
    if startup:
        if not flicker: #BUTTONS
            draw.rect(screen, WHITE, startRect, 3)
            draw.rect(screen, WHITE, tutorialRect, 3)
            draw.rect(screen, WHITE, settingsRect, 3)
        playtext = font.render('START', True, WHITE) #TEXT
        screen.blit(playtext, (410, 537))
        tutorialtext = font.render('TUTORIAL', True, WHITE)
        screen.blit(tutorialtext, (36, 452))
        settingstext = font.render('SETTINGS', True, WHITE)
        screen.blit(settingstext, (751, 452))
        if startRect.collidepoint(mx, my): #COLOUR FEEDBACK WHEN HOVERING
            draw.rect(screen, GREEN, startRect, 3)
        if tutorialRect.collidepoint(mx, my):
            draw.rect(screen, GREEN, tutorialRect, 3)
        if settingsRect.collidepoint(mx, my):
            draw.rect(screen, GREEN, settingsRect, 3)

        if mb[0]:
            if startRect.collidepoint(mx, my) and not tutorial and not settings and not gameovertext: #starts playing
                tutorial = False
                settings = False
                startup = False
                gameovertext = False
                playing = True
                mixer.music.pause()
                beeps.play()
            if tutorialRect.collidepoint(mx, my): #opens tutorial page
                tutorial = True
                settings = False
                gameovertext = False
            if settingsRect.collidepoint(mx,my): #opens settings page
                settings = True
                tutorial = False
                gameovertext = False

    if tutorial: #tutorial screen
        draw.rect(screen, BLACK, textRect)
        line1 = font.render('HOW TO PLAY:', True, WHITE)
        screen.blit(line1, (250, 240))
        line2 = font.render('1. USE THE ARROW KEYS TO', True, WHITE)
        screen.blit(line2, (250, 290))
        line3 = font.render('CHANGE DIRECTION', True, WHITE)
        screen.blit(line3, (273, 315))
        line4 = font.render('2. AVOID THE GHOSTS AND EAT', True, WHITE)
        screen.blit(line4, (250, 365))
        line5 = font.render('DOTS FOR POINTS', True, WHITE)
        screen.blit(line5, (280, 390))
        line6 = font.render('3. POWER PELLETS GIVE YOU A', True, WHITE)
        screen.blit(line6, (250, 440))
        line7 = font.render('POWERUP TO TEMPORARILY', True, WHITE)
        screen.blit(line7, (280, 465))
        line8 = font.render('EAT GHOSTS FOR EXTRA', True, WHITE)
        screen.blit(line8, (280, 490))
        line9 = font.render('POINTS', True, WHITE)
        screen.blit(line9, (280, 515))
        line10 = font.render('PRESS [SPACE] TO EXIT', True, WHITE)
        screen.blit(line10, (305, 600))

    if settings: #settings screen
        draw.rect(screen, BLACK, smalltextRect)
        if not flicker:
            if music: #if there is music, make it green
                draw.rect(screen, GREEN, muteRect, 3)
            else: #if there isn't music, make it red
                draw.rect(screen, RED, muteRect, 3)
            if sfx: #if sfx is turned on, highlight green, otherwise red
                draw.rect(screen, GREEN, sfxRect, 3)
            else:
                draw.rect(screen, RED, sfxRect, 3)
        if muteRect.collidepoint(mx, my): #colour feedback
            draw.rect(screen, WHITE, muteRect, 3)
        if sfxRect.collidepoint(mx, my):
            draw.rect(screen, WHITE, sfxRect, 3)
        mutemusic = font.render('TOGGLE MUSIC', True, WHITE) #text
        screen.blit(mutemusic, (367, 380))
        mutesoundeffects = font.render('TOGGLE SFX', True, WHITE)
        screen.blit(mutesoundeffects, (381, 440))
        line10 = font.render('PRESS [SPACE] TO EXIT', True, WHITE)
        screen.blit(line10, (305, 530))

    if gameovertext: #game over screen
        draw.rect(screen, BLACK, smalltextRect)
        line1 = font.render('GAME OVER', True, WHITE)
        screen.blit(line1, (382, 430))
        line2 = font.render(f'FINAL SCORE: {score}', True, WHITE)
        stextw = line2.get_width()
        sxpos = (WIDTH - stextw) // 2
        screen.blit(line2, (sxpos, 460))
        line3 = font.render('PRESS [SPACE] TO EXIT', True, WHITE)
        screen.blit(line3, (305, 490))

    # MOVING PLAYER
    if playing:
        # startup counter
        if startupcounter < 180:
            moving = False
            chasing = False
            scattering = False
            startupcounter += 1
            if startupcounter < 60:
                countertext = font.render('3', True, WHITE)
                screen.blit(countertext, (440, 537))
            if 120 > startupcounter > 60:
                countertext = font.render('2', True, WHITE)
                screen.blit(countertext, (440, 537))
            if startupcounter > 120:
                countertext = font.render('1', True, WHITE)
                screen.blit(countertext, (443, 537))
        else:
            moving = True

        # powerup counter
        if powerup and powerupcounter < 420:
            powerupcounter += 1
        elif powerup and powerupcounter >= 420:
            powerupcounter = 0
            powerup = False
            eatenghosts = [False, False, False, False]

        #hitboxes
        playerRect = Rect(playerx + 6, playery + 6, 33, 33)
        blinkyRect = Rect(blinkyx + 6, blinkyy + 6, 33, 33)
        pinkyRect = Rect(pinkyx + 6, pinkyy + 6, 33, 33)
        inkyRect = Rect(inkyx + 6, inkyy + 6, 33, 33)
        clydeRect = Rect(clydex + 6, clydey + 6, 33, 33)

        '''
        draw.rect(screen, RED, playerRect, 2)
        draw.rect(screen, GREEN, blinkyRect, 2)
        draw.rect(screen, GREEN, pinkyRect, 2)
        draw.rect(screen, GREEN, inkyRect, 2)
        draw.rect(screen, GREEN, clydeRect, 2)
        '''

        #center of player
        centerx = playerx + 23
        centery = playery + 23
        # draw.circle(screen,WHITE,(centerx,centery),3)
        validturns = checkpos(centerx, centery) #checks for valid turns

        #center of ghosts, checks if they're in the box, checks for valid turns, updates target
        cblinkyx = blinkyx + 23
        cblinkyy = blinkyy + 23
        blinkyinbox = checkbox(blinkyx, blinkyy)
        validblinkyturns = checkghostpos(cblinkyx, cblinkyy, blinkydirection, blinkyinbox, blinkydead)
        btx, bty = centerx, centery

        cpinkyx = pinkyx + 23
        cpinkyy = pinkyy + 23
        pinkyinbox = checkbox(pinkyx, pinkyy)
        validpinkyturns = checkghostpos(cpinkyx, cpinkyy, pinkydirection, pinkyinbox, pinkydead)
        ptx, pty = pinkytarget()

        cinkyx = inkyx + 23
        cinkyy = inkyy + 23
        inkyinbox = checkbox(inkyx, inkyy)
        validinkyturns = checkghostpos(cinkyx, cinkyy, inkydirection, inkyinbox, inkydead)
        itx, ity = inkytarget()

        cclydex = clydex + 23
        cclydey = clydey + 23
        clydeinbox = checkbox(clydex,clydey)
        validclydeturns = checkghostpos(cclydex, cclydey, clydedirection, clydeinbox, clydedead)
        ctx, cty = clydetarget()

        if moving:
            #siren sound timer
            sirencounter += 1
            if sirencounter%18 == 0:
                siren.play()

            playerx, playery = moveplyr(playerx, playery) #moves the player

            #chase/scatter alternator
            if not powerup:
                blinkyspooked = False
                pinkyspooked = False
                inkyspooked = False
                clydespooked = False
                if chasecounter < 420:
                    scattering = True
                    chasing = False
                if 420 < chasecounter < 1620:
                    scattering = False
                    chasing = True
                    # print("chasing")
                if 1620 < chasecounter < 2040:
                    scattering = True
                    chasing = False
                    # print("scattering")
                if 2040 < chasecounter < 3240:
                    scattering = False
                    chasing = True
                    # print("chasing")
                if 3240 < chasecounter < 3540:
                    scattering = True
                    chasing = False
                    # print("scattering")
                if 3540 < chasecounter < 4740:
                    scattering = False
                    chasing = True
                    # print("chasing")
                if 4740 < chasecounter < 5040:
                    scattering = True
                    chasing = False
                    # print("scattering")
                if chasecounter > 5040:
                    scattering = False
                    chasing = True
                    # print("chasing")
                chasecounter += 1

            #updates states of ghosts
            if powerup and not blinkydead and not eatenghosts[0]:
                blinkyspooked = True
            if powerup and not pinkydead and not eatenghosts[1]:
                pinkyspooked = True
            if powerup and not inkydead and not eatenghosts[2]:
                inkyspooked = True
            if powerup and not clydedead and not eatenghosts[3]:
                clydespooked = True

            #incremental counting of points (100,200,400,800) as more ghosts are eaten
            if powerup and playerRect.colliderect(blinkyRect) and not blinkydead and not eatenghosts[0]:
                blinkydead = True
                blinkyspooked = False
                eatenghosts[0] = True
                score += (2 ** eatenghosts.count(True)) * 100
                eat.play()
            if powerup and playerRect.colliderect(pinkyRect) and not pinkydead and not eatenghosts[1]:
                pinkydead = True
                pinkyspooked = False
                eatenghosts[1] = True
                score += (2 ** eatenghosts.count(True)) * 100
                eat.play()
            if powerup and playerRect.colliderect(inkyRect) and not inkydead and not eatenghosts[2]:
                inkydead = True
                inkyspooked = False
                eatenghosts[2] = True
                score += (2 ** eatenghosts.count(True)) * 100
                eat.play()
            if powerup and playerRect.colliderect(clydeRect) and not clydedead and not eatenghosts[3]:
                clydedead = True
                clydespooked = False
                eatenghosts[3] = True
                score += (2 ** eatenghosts.count(True)) * 100
                eat.play()

            #GHOST BEHAVIOUR: INBOX PRIORITIZED OVER DEAD, DEAD OVER SPOOKED, SPOOKED OVER CHASE. Different targets for each situation
            if blinkyinbox:
                blinkyx, blinkyy, blinkydirection = moveghost(blinkyx, blinkyy, 450, 300, blinkydirection,
                                                                  validblinkyturns, 3)
            elif blinkydead:
                blinkyx, blinkyy, blinkydirection = movedead(blinkyx, blinkyy, blinkydirection, validblinkyturns, 3)
                blinkyspooked = False
            elif blinkyspooked:
                blinkyx, blinkyy, blinkydirection = movespooked(blinkyx, blinkyy, blinkydirection, validblinkyturns, 2)
            else:
                if chasing:
                    blinkyx, blinkyy, blinkydirection = moveghost(blinkyx, blinkyy, playerx, playery, blinkydirection,
                                                                  validblinkyturns, 3)
                elif scattering:
                    blinkyx, blinkyy, blinkydirection = moveghost(blinkyx, blinkyy, 56, 58, blinkydirection,
                                                                  validblinkyturns, 3)

            if pinkyinbox:
                if score < 100:  # Keep Inky in the box if the score is less than 100
                    # Move Inky up and down within the box
                    if pinkyy <= 425:  # Top of the box (adjust coordinates as needed)
                        pinkydirection = 3
                    elif pinkyy >= 455:  # Bottom of the box (adjust coordinates as needed)
                        pinkydirection = 2
                    if pinkydirection == 3:
                        pinkyy += 2
                    elif pinkydirection == 2:
                        pinkyy -= 2
                else:
                    pinkyx, pinkyy, pinkydirection = moveghost(pinkyx, pinkyy, 450, 300, pinkydirection,
                                                                  validpinkyturns, 3)
            elif pinkydead:
                pinkyx, pinkyy, pinkydirection = movedead(pinkyx, pinkyy, pinkydirection, validpinkyturns, 3)
            elif pinkyspooked:
                pinkyx, pinkyy, pinkydirection = movespooked(pinkyx, pinkyy, pinkydirection, validpinkyturns, 2)
            else:
                if chasing:
                    pinkyx, pinkyy, pinkydirection = moveghost(pinkyx,pinkyy,ptx,pty,pinkydirection,validpinkyturns,3)
                elif scattering:
                    pinkyx, pinkyy, pinkydirection = moveghost(pinkyx, pinkyy, 844, 58, pinkydirection, validpinkyturns,
                                                               3)

            if inkyinbox:
                if score < 400:  # Keep Inky in the box if the score is less than 300
                    # Move Inky up and down within the box
                    if inkyy <= 425:  # Top of the box (adjust coordinates as needed)
                        inkydirection = 3
                    elif inkyy >= 455:  # Bottom of the box (adjust coordinates as needed)
                        inkydirection = 2
                    if inkydirection == 3:
                        inkyy += 2
                    elif inkydirection == 2:
                        inkyy -= 2
                else:
                    # Allow Inky to leave the box once the score is 300 or more
                    inkyx, inkyy, inkydirection = moveghost(inkyx, inkyy, 450, 300, inkydirection,
                                                            validinkyturns, 3)
            elif inkydead:
                inkyx, inkyy, inkydirection = movedead(inkyx, inkyy, inkydirection, validinkyturns, 3)
            elif inkyspooked:
                inkyx, inkyy, inkydirection = movespooked(inkyx, inkyy, inkydirection, validinkyturns, 2)
            else:
                if chasing:
                    inkyx, inkyy, inkydirection = moveghost(inkyx, inkyy, itx, ity, inkydirection, validinkyturns, 3)
                elif scattering:
                    inkyx, inkyy, inkydirection = moveghost(inkyx, inkyy, 844, 842, inkydirection, validinkyturns, 3)

            if clydeinbox:
                if score < 800:
                    if clydey <= 425:  # Top of the box (adjust coordinates as needed)
                        clydedirection = 3
                    elif clydey >= 455:  # Bottom of the box (adjust coordinates as needed)
                        clydedirection = 2
                    if clydedirection == 3:
                        clydey += 2
                    elif clydedirection == 2:
                        clydey -= 2
                else:
                    # Allow Clyde to leave the box once the score is 800 or more
                    clydex, clydey, clydedirection = moveghost(clydex, clydey, 450, 300, clydedirection,
                                                               validclydeturns, 3)
            elif clydedead:
                clydex, clydey, clydedirection = movedead(clydex, clydey, clydedirection, validclydeturns, 3)
            elif clydespooked:
                clydex, clydey, clydedirection = movespooked(clydex, clydey, clydedirection, validclydeturns, 2)
            else:
                if chasing:
                    clydex, clydey, clydedirection = moveghost(clydex, clydey, ctx, cty, clydedirection,
                                                               validclydeturns, 3)
                elif scattering:
                    clydex, clydey, clydedirection = moveghost(clydex, clydey, 56, 842, clydedirection,
                                                               validclydeturns, 3)

        score, powerup, powerupcounter, eatenghosts = checkcol(score, powerup, powerupcounter, eatenghosts, levels) #updates score, checks for eaten dots and ghosts

        #CHECKS FOR COLLISIONS WITH GHOSTS WHEN NOT SPOOKED (LIFE LOST)
        if not powerup:
            if (playerRect.colliderect(blinkyRect) and not blinkydead) or \
                    (playerRect.colliderect(pinkyRect) and not pinkydead) or \
                    (playerRect.colliderect(inkyRect) and not inkydead) or \
                    (playerRect.colliderect(clydeRect) and not clydedead):
                if lives > 0:
                    death.play()
                    lives -= 1
                    startupcounter = 0
                    powerup = False
                    powerupcounter = 0
                    blinkyx = 427
                    blinkyy = 357
                    blinkydirection = 0
                    inkyx = 489
                    inkyy = 442
                    inkydirection = 2
                    pinkyx = 428
                    pinkyy = 442
                    pinkydirection = 2
                    clydex = 365
                    clydey = 442
                    clydedirection = 2
                    playerx = 427
                    playery = 693
                    plyrdirection = 0
                    plyrdirection_cmmd = 0
                    eatenghosts = [False, False, False, False]
                    blinkydead = False
                    pinkydead = False
                    inkydead = False
                    clydedead = False
                    blinkyspooked = False
                    pinkyspooked = False
                    inkyspooked = False
                    clydespooked = False
                else:
                    gameover = True
                    moving = False
                    playing = False
        if powerup and playerRect.colliderect(blinkyRect) and eatenghosts[0] and not blinkydead:
            if lives > 0:
                death.play()
                lives -= 1
                startupcounter = 0
                powerup = False
                powerupcounter = 0
                blinkyx = 427
                blinkyy = 357
                blinkydirection = 0
                inkyx = 489
                inkyy = 442
                inkydirection = 2
                pinkyx = 428
                pinkyy = 442
                pinkydirection = 2
                clydex = 365
                clydey = 442
                clydedirection = 2
                playerx = 427
                playery = 693
                plyrdirection = 0
                plyrdirection_cmmd = 0
                eatenghosts = [False, False, False, False]
                blinkydead = False
                pinkydead = False
                inkydead = False
                clydedead = False
                blinkyspooked = False
                pinkyspooked = False
                inkyspooked = False
                clydespooked = False
            else:
                gameover = True
                moving = False
                playing = False
        if powerup and playerRect.colliderect(pinkyRect) and eatenghosts[1] and not pinkydead:
            if lives > 0:
                death.play()
                lives -= 1
                startupcounter = 0
                powerup = False
                powerupcounter = 0
                blinkyx = 427
                blinkyy = 357
                blinkydirection = 0
                inkyx = 489
                inkyy = 442
                inkydirection = 2
                pinkyx = 428
                pinkyy = 442
                pinkydirection = 2
                clydex = 365
                clydey = 442
                clydedirection = 2
                playerx = 427
                playery = 693
                plyrdirection = 0
                plyrdirection_cmmd = 0
                eatenghosts = [False, False, False, False]
                blinkydead = False
                pinkydead = False
                inkydead = False
                clydedead = False
                blinkyspooked = False
                pinkyspooked = False
                inkyspooked = False
                clydespooked = False
            else:
                gameover = True
                moving = False
                playing = False
        if powerup and playerRect.colliderect(inkyRect) and eatenghosts[2] and not inkydead:
            if lives > 0:
                death.play()
                lives -= 1
                startupcounter = 0
                powerup = False
                powerupcounter = 0
                blinkyx = 427
                blinkyy = 357
                blinkydirection = 0
                inkyx = 489
                inkyy = 442
                inkydirection = 2
                pinkyx = 428
                pinkyy = 442
                pinkydirection = 2
                clydex = 365
                clydey = 442
                clydedirection = 2
                playerx = 427
                playery = 693
                plyrdirection = 0
                plyrdirection_cmmd = 0
                eatenghosts = [False, False, False, False]
                blinkydead = False
                pinkydead = False
                inkydead = False
                clydedead = False
                blinkyspooked = False
                pinkyspooked = False
                inkyspooked = False
                clydespooked = False
            else:
                gameover = True
                moving = False
                playing = False
        if powerup and playerRect.colliderect(clydeRect) and eatenghosts[3] and not clydedead:
            if lives > 0:
                death.play()
                lives -= 1
                startupcounter = 0
                powerup = False
                powerupcounter = 0
                blinkyx = 427
                blinkyy = 357
                blinkydirection = 0
                inkyx = 489
                inkyy = 442
                inkydirection = 2
                pinkyx = 428
                pinkyy = 442
                pinkydirection = 2
                clydex = 365
                clydey = 442
                clydedirection = 2
                playerx = 427
                playery = 693
                plyrdirection = 0
                plyrdirection_cmmd = 0
                eatenghosts = [False, False, False, False]
                blinkydead = False
                pinkydead = False
                inkydead = False
                clydedead = False
                blinkyspooked = False
                pinkyspooked = False
                inkyspooked = False
                clydespooked = False
            else:
                gameover = True
                moving = False
                playing = False

        #Indicates the powerup is almost over by flashing ghosts
        if 420 > powerupcounter > 300 and flicker:
            if blinkyspooked:
                if blinkydirection == 0:
                    screen.blit(changeimgs[0], (blinkyx, blinkyy))
                if blinkydirection == 1:
                    screen.blit(changeimgs[1], (blinkyx, blinkyy))
                if blinkydirection == 2:
                    screen.blit(changeimgs[2], (blinkyx, blinkyy))
                if blinkydirection == 3:
                    screen.blit(changeimgs[3], (blinkyx, blinkyy))
            if pinkyspooked:
                if pinkydirection == 0:
                    screen.blit(changeimgs[0], (pinkyx, pinkyy))
                if pinkydirection == 1:
                    screen.blit(changeimgs[1], (pinkyx, pinkyy))
                if pinkydirection == 2:
                    screen.blit(changeimgs[2], (pinkyx, pinkyy))
                if pinkydirection == 3:
                    screen.blit(changeimgs[3], (pinkyx, pinkyy))
            if inkyspooked:
                if inkydirection == 0:
                    screen.blit(changeimgs[0], (inkyx, inkyy))
                if inkydirection == 1:
                    screen.blit(changeimgs[1], (inkyx, inkyy))
                if inkydirection == 2:
                    screen.blit(changeimgs[2], (inkyx, inkyy))
                if inkydirection == 3:
                    screen.blit(changeimgs[3], (inkyx, inkyy))
            if clydespooked:
                if clydedirection == 0:
                    screen.blit(changeimgs[0], (clydex, clydey))
                if clydedirection == 1:
                    screen.blit(changeimgs[1], (clydex, clydey))
                if clydedirection == 2:
                    screen.blit(changeimgs[2], (clydex, clydey))
                if clydedirection == 3:
                    screen.blit(changeimgs[3], (clydex, clydey))

    #changes ghosts back to life if in box
    if blinkyinbox and blinkydead:
        blinkydead = False
    if pinkyinbox and pinkydead:
        pinkydead = False
    if inkyinbox and inkydead:
        inkydead = False
    if clydeinbox and clydedead:
        clydedead = False

    #resets the board if game is over
    if gameover:
        gameovertext = True
        gover.play()
        startupcounter = 0
        powerup = False
        powerupcounter = 0
        chasecounter = 0
        blinkyx = 427
        blinkyy = 357
        blinkydirection = 0
        inkyx = 489
        inkyy = 442
        inkydirection = 2
        pinkyx = 428
        pinkyy = 442
        pinkydirection = 2
        clydex = 365
        clydey = 442
        clydedirection = 2
        playerx = 427
        playery = 693
        plyrdirection = 0
        plyrdirection_cmmd = 0
        eatenghosts = [False, False, False, False]
        blinkydead = False
        pinkydead = False
        inkydead = False
        clydedead = False
        blinkyspooked = False
        pinkyspooked = False
        inkyspooked = False
        clydespooked = False
        lives = 3
        level = copy.deepcopy(boards)
        gameover = False
        gamewon = False
        playing = False
        startup = True
        levels = 1

    #resets the board to the next level
    if gamewon:
        startupcounter = 0
        powerup = False
        powerupcounter = 0
        blinkyx = 427
        blinkyy = 357
        blinkydirection = 0
        inkyx = 489
        inkyy = 442
        inkydirection = 2
        pinkyx = 428
        pinkyy = 442
        pinkydirection = 2
        clydex = 365
        clydey = 442
        clydedirection = 2
        playerx = 427
        playery = 693
        plyrdirection = 0
        plyrdirection_cmmd = 0
        eatenghosts = [False, False, False, False]
        blinkydead = False
        pinkydead = False
        inkydead = False
        clydedead = False
        blinkyspooked = False
        pinkyspooked = False
        inkyspooked = False
        clydespooked = False
        level = copy.deepcopy(boards)
        gameover = False
        gamewon = False
        playing = True
        levels += 1

    #updates highscore if current score is higher than the previous
    if score > highscore:
        highscore = score
    writehighscore(highscore)

    myClock.tick(fps)
    display.flip()

quit()
