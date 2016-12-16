"""
File: mainScreen.py
Author: Ping
Email: billy3962@hotmail.com
Github: Ping-Lin
Description: show the main game screen and the game process
"""

import pygame
import sys
from pygame.locals import *
import gbv
from character.pika import Pika
from obstacle.wall import Wall
from ball.pikaBall import PikaBall
import button


# Kinect
from visual import *
import pykinect
from pykinect import nui
from pykinect.nui import JointId
class Skeleton:
    """Kinect skeleton represented as a VPython frame.
    """

    def __init__(self, f):
        """Create a skeleton in the given VPython frame f.
        """
        self.frame = f
        self.joints = [sphere(frame=f, radius=0.08, color=color.yellow)
                       for i in range(20)]
        self.joints[3].radius = 0.125
        self.bones = [cylinder(frame=f, radius=0.05, color=color.yellow)
                      for bone in _bone_ids]

    def update(self):
        """Update the skeleton joint positions in the depth sensor frame.

        Return true iff the most recent sensor frame contained a tracked
        skeleton.
        """
        updated = False
        for skeleton in _kinect.skeleton_engine.get_next_frame().SkeletonData:
            if skeleton.eTrackingState == nui.SkeletonTrackingState.TRACKED:

                # Move the joints.
                for joint, p in zip(self.joints, skeleton.SkeletonPositions):
                    joint.pos = (p.x, p.y, p.z)

                # Move the bones.
                for bone, bone_id in zip(self.bones, _bone_ids):
                    p1, p2 = [self.joints[id].pos for id in bone_id]
                    bone.pos = p1
                    bone.axis = p2 - p1
                updated = True
        return updated

def draw_sensor(f):
    """Draw 3D model of the Kinect sensor.

    Draw the sensor in the given (and returned) VPython frame f, with
    the depth sensor frame aligned with f.
    """
    box(frame=f, pos=(0, 0, 0), length=0.2794, height=0.0381, width=0.0635,
        color=color.blue)
    cylinder(frame=f, pos=(0, -0.05715, 0), axis=(0, 0.0127, 0), radius=0.0381,
             color=color.blue)
    cone(frame=f, pos=(0, -0.04445, 0), axis=(0, 0.01905, 0), radius=0.0381,
         color=color.blue)
    cylinder(frame=f, pos=(0, -0.05715, 0), axis=(0, 0.0381, 0), radius=0.0127,
             color=color.blue)
    cylinder(frame=f, pos=(-0.0635, 0, 0.03175), axis=(0, 0, 0.003),
             radius=0.00635, color=color.red)
    cylinder(frame=f, pos=(-0.0127, 0, 0.03175), axis=(0, 0, 0.003),
             radius=0.00635, color=color.red)
    cylinder(frame=f, pos=(0.0127, 0, 0.03175), axis=(0, 0, 0.003),
             radius=0.00635, color=color.red)
    text(frame=f, text='KINECT', pos=(0.06985, -0.00635, 0.03175),
         align='center', height=0.0127, depth=0.003)
    return f
    




def runGame(spriteGroup, wallList, pikaList, pikaBall, clickButton, txtImgs,
            buttonGroup):
 
    
    
    
    """
    Run the main loop of game
    """
    global NEWGAME, STARTDELAY
    background = pygame.image.load('bg.jpg').convert()
    background = pygame.transform.scale(background, (gbv.WINWIDTH, gbv.WINHEIGHT))
    pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP, MOUSEBUTTONUP])   # improve the FPS
    while True:        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_F2:
                    if DISPLAYSURF.get_flags() & FULLSCREEN:
                        pygame.display.set_mode((gbv.WINWIDTH, gbv.WINHEIGHT), DOUBLEBUF, 0)
                    else:
                        pygame.display.set_mode((gbv.WINWIDTH, gbv.WINHEIGHT), FLAGS, 0)
                elif event.key == pygame.K_LEFT:
                    clickButton['left'] = True
                elif event.key == pygame.K_RIGHT:
                    clickButton['right'] = True
                elif event.key == pygame.K_UP:
                    clickButton['up'] = True
                elif event.key == pygame.K_DOWN:
                    clickButton['down'] = True
                elif event.key == pygame.K_SPACE:
                    clickButton['space'] = True
                elif event.key == pygame.K_a:
                    clickButton['a'] = True
                elif event.key == pygame.K_d:
                    clickButton['d'] = True
                elif event.key == pygame.K_w:
                    clickButton['w'] = True
                elif event.key == pygame.K_s:
                    clickButton['s'] = True
                elif event.key == pygame.K_LSHIFT:
                    clickButton['lshift'] = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    clickButton['left'] = False
                elif event.key == pygame.K_RIGHT:
                    clickButton['right'] = False
                elif event.key == pygame.K_UP:
                    clickButton['up'] = False
                elif event.key == pygame.K_DOWN:
                    clickButton['down'] = False
                elif event.key == pygame.K_SPACE:
                    clickButton['space'] = False
                elif event.key == pygame.K_a:
                    clickButton['a'] = False
                elif event.key == pygame.K_d:
                    clickButton['d'] = False
                elif event.key == pygame.K_w:
                    clickButton['w'] = False
                elif event.key == pygame.K_s:
                    clickButton['s'] = False
                elif event.key == pygame.K_LSHIFT:
                    clickButton['lshift'] = False
            elif event.type == MOUSEBUTTONUP:
                clickPos = pygame.mouse.get_pos()
                buttonGroup.update(clickPos, pikaList, wallList)

        # draw the image
        DISPLAYSURF.blit(background, (0, 0))
        pikaBall.drawShadow(DISPLAYSURF)
        spriteGroup.update(clickButton, wallList)
        pikaBall.update(clickButton, wallList, pikaList)
        spriteGroup.draw(DISPLAYSURF)
        buttonGroup.draw(DISPLAYSURF)
        if pikaBall.ifAttack:
            pikaBall.drawHistory(DISPLAYSURF)
        pikaBall.draw(DISPLAYSURF)
        if pikaBall.ifHitPic:
            pikaBall.drawHitPic(DISPLAYSURF)

        # check if score
        if wallList[3].ifScore[0] or wallList[3].ifScore[1]:
            wallList[0].pointSound.play()
            if not NEWGAME:
                txtImgs = setScore(txtImgs, wallList)
                NEWGAME = True

        DISPLAYSURF.blit(txtImgs[0], (gbv.POINTLEFT, gbv.POINTHEIGHT))
        DISPLAYSURF.blit(txtImgs[1], (gbv.POINTRIGHT, gbv.POINTHEIGHT))

        # check if new game
        if NEWGAME:
            setNewGame(pikaList, pikaBall, wallList)
        else:
            DISPLAYSURF.set_alpha(None)   # improve the FPS

        pygame.display.update()
        # a new game start need to delay a time
        if STARTDELAY != 0:
            if STARTDELAY == 1000:
                pygame.time.delay(STARTDELAY)
                STARTDELAY = 0
            else:
                STARTDELAY = 1000
                pygame.mixer.music.unpause()

        # print CLOCK.get_fps()
        CLOCK.tick(40)


def main():
    global IMAGE, DISPLAYSURF, CLOCK, SCORETXT, FONT, ALPHA, NEWGAME, STARTDELAY, FLAGS
    pygame.init()
    pygame.display.set_icon( pygame.image.load('icon.icns') )
    FLAGS = FULLSCREEN | DOUBLEBUF
    DISPLAYSURF = pygame.display.set_mode((gbv.WINWIDTH, gbv.WINHEIGHT), FLAGS, 0)
    DISPLAYSURF.set_alpha(None)
    pygame.display.set_caption('PikaBall X Connect')
    CLOCK = pygame.time.Clock()
    FONT = pygame.font.Font(None, 100)
    FONT.set_italic(True)
    pygame.mixer.music.load('bg.wav')

    # Load the element
    pikaLeft = Pika(True)
    pikaRight = Pika()
    pikaList = [pikaLeft, pikaRight]
    spriteGroup = pygame.sprite.Group(pikaLeft)
    spriteGroup.add(pikaRight)
    wallList = []   # left, right, up, down and stick
    wallList.append(
        Wall(pygame.Rect(0, 0, 1, gbv.WINHEIGHT)))
    wallList.append(
        Wall(pygame.Rect(gbv.WINWIDTH, 0, 500, gbv.WINHEIGHT)))
    wallList.append(
        Wall(pygame.Rect(0, 0, gbv.WINWIDTH, 10)))
    wallList.append(
        Wall(pygame.Rect(0, gbv.WINHEIGHT-50, gbv.WINWIDTH, 500)))
    wallList.append(
        Wall(pygame.Rect(
            gbv.STICKPOS[0], gbv.STICKPOS[1], gbv.STICKWIDTH, gbv.STICKHEIGHT), img=True))
    spriteGroup.add(wallList[-1])   # add the stick, need to show
    # spriteGroup.add(wallList)
    musicButton = button.Button(pygame.Rect(gbv.WINWIDTH-200, 20, 60, 60), 1)
    soundButton = button.Button(pygame.Rect(gbv.WINWIDTH-100, 20, 60, 60), 2)
    buttonGroup = pygame.sprite.Group(musicButton)
    buttonGroup.add(soundButton)

    # some initial value
    SCORETXT = [0, 0]
    clickButton = dict.fromkeys(
        ['left', 'right', 'up', 'down', 'space',
         'a', 'd', 'w', 's', 'lshift'])
    txtImgs = [FONT.render("0", 1, (255, 0, 0))]*2
    NEWGAME = False
    ALPHA = 0
    STARTDELAY = 0
    pygame.mixer.music.play(-1, 0.0)

    runGame(spriteGroup, wallList, pikaList, PikaBall(),
            clickButton, txtImgs, buttonGroup)


def setScore(txtImgs, wallList):
    if wallList[3].ifScore[0]:
        SCORETXT[0] += 1
    elif wallList[3].ifScore[1]:
        SCORETXT[1] += 1
    txtImgs[0] = FONT.render(str(SCORETXT[0]), 1, (255, 0, 0))
    txtImgs[1] = FONT.render(str(SCORETXT[1]), 1, (255, 0, 0))
    return txtImgs


def setNewGame(pikaList, pikaBall, wallList):
    global NEWGAME, ALPHA, STARTDELAY
    pikaBall.ifAttack = False
    ALPHA += 10
    background = pygame.Surface(DISPLAYSURF.get_size())
    background.set_alpha(ALPHA)
    background.fill((0, 0, 0))
    if ALPHA >= 255:
        NEWGAME = False
        ALPHA = 0
        # set the ball and pika to origin place
        for pika in pikaList:
            pika.moveOrigin()
        if wallList[3].ifScore[0]:
            pikaBall.moveOrigin(0)
        else:
            pikaBall.moveOrigin(1)
        wallList[3].ifScore = [False]*2
        STARTDELAY = 1001
        pygame.mixer.music.pause()

    DISPLAYSURF.blit(background, (0, 0))
    pygame.time.delay(30)

if __name__ == '__main__':
    main()
