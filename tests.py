import pygame
import PyGameTools


##-- TEXT BOX --##

h = 800
w = 1400
m = 400
cushion = 0
pygame.init()
Screen = pygame.display.set_mode((w, h))

t = """This is the first line.
This is a new line.

That was a blank line.
This is a longer line to make sure that everything is wrapping correctly.
Therearenospacesinthislinetocheckthatlongwordsdon'tcauseaproblem
*italic* **bold *both***
This is the last line."""
r, g, b, rot = 0, 0, 0, 0
while True:
    pygame.display.update()
    Screen.fill((255, 255, 255))
    for x, xal in ((0, "left"), (w // 2, "centre"), (w, "right")):
        for y, yal in ((0, "top"), (h // 2, "centre"), (h, "bottom")):
            PyGameTools.other_text_box(t, (r, g, b), 18, screen=Screen, coords=(x, y), align=(xal, yal), max_len=m, rotate=rot, background=(255 - r, 255 - g, 255 - b))
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
    #break