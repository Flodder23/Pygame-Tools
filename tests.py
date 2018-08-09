import pygame
import PyGameTools
pygame.init()

###--- Test file: how to use ---##
### - Cut the tests for the desired function to the top (each function is seperated by a header
###   with two hashes)
###  - Cut the specific test you want to run to the top of that section (each test is seperated by a
###    header with one hash, be careful not to cut off the config at the very start of each section)



##-- WRITE --##

t = """This is the first line.

That was a blank line.
This is a slightly longer line to make sure that everything is wrapping as it should be.
Therearenospacesinthislinetocheckthatlongwordsdonotcauseanyproblems.
 There  are   too    many     spaces    in   this  line
n *i* **b** -u- --s-- ***ib** -iu- --is--* **-bu- --bs--** ---us---
***-ibu- --ibs** -ius* **bus *busi***--- n
Ignorance is bliss. /* /- //
This is the last line."""


#- Easier to see, doesn't test alignment or rotation -#

w = 800
h = 800
Screen = pygame.display.set_mode((w, h))
Screen.fill((255, 255, 255))
PyGameTools.write(t, (0, 0, 0), 40, screen=Screen, coords=(0, 0), max_len=w, background=(0, 200, 70))
pygame.display.update()
while True:
    pass


#- Harder to see, tests alignment and rotation -#

h = 900
w = 1400
m = 400
cushion = 0
r, g, b, rot = 0, 0, 0, 0
Screen = pygame.display.set_mode((w, h))

while True:
    pygame.display.update()
    Screen.fill((255, 255, 255))
    for x, xal in ((0, "left"), (w // 2, "centre"), (w, "right")):
        for y, yal in ((0, "top"), (h // 2, "centre"), (h, "bottom")):
            PyGameTools.write(t, (r, g, b), 18, screen=Screen, coords=(x, y), align=(xal, yal), max_len=m, background=(255 - r, 255 - g, 255 - b), rotate=rot)
    pygame.draw.line(Screen, (0, 0, 0), (cushion, 0), (cushion, h))
    pygame.draw.line(Screen, (0, 0, 0), (m + cushion, 0), (m + cushion, h))
    pygame.draw.line(Screen, (0, 0, 0), ((w - m) // 2, 0), ((w - m) // 2, h))
    pygame.draw.line(Screen, (0, 0, 0), (w // 2, 0), (w // 2, h))
    pygame.draw.line(Screen, (0, 0, 0), ((w + m) // 2, 0), ((w + m) // 2, h))
    pygame.draw.line(Screen, (0, 0, 0), (w - m - cushion, 0), (w - m - cushion, h))
    pygame.draw.line(Screen, (0, 0, 0), (w - cushion, 0), (w - cushion, h))
    pygame.draw.line(Screen, (0, 0, 0), (0, h // 2), (w, h // 2))
    pygame.draw.line(Screen, (0, 0, 0), (0, cushion), (w, cushion))
    pygame.draw.line(Screen, (0, 0, 0), (0, h - cushion), (w, h - cushion))
    #for _ in range(1000000):
    #    pass
    if r < 255:
        r += 1
    else:
        if g < 255:
            g += 1
        else:
            if b < 255:
                b += 1
            else:
                r, g, b = 0, 0, 0
    if rot < 360:
        rot += 1
    else:
        rot = 0
