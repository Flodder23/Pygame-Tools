import pygame
import PyGameTools

##-- TEXT BOX --##

h = 750
w = 1300
m = 400
pygame.init()
Screen = pygame.display.set_mode((w, h))
Screen.fill((255, 255, 255))
pygame.draw.line(Screen, (0, 0, 0), (m, 0), (m, h))
pygame.draw.line(Screen, (0, 0, 0), ((w - m) // 2, 0), ((w - m) // 2, h))
pygame.draw.line(Screen, (0, 0, 0), (w // 2, 0), (w // 2, h))
pygame.draw.line(Screen, (0, 0, 0), ((w + m) // 2, 0), ((w + m) // 2, h))
pygame.draw.line(Screen, (0, 0, 0), (w - m, 0), (w - m, h))
pygame.draw.line(Screen, (0, 0, 0), (0, h // 2), (w, h // 2))

t = """This is the start of the text.
This is a new line.

That was a blank line.
This is a longer line to make sure that everything is wrapping correctly."""

r, g, b = 0, 0, 0
while True:
    pygame.display.update()
    for x, xal in ((0, "left"), (w // 2, "centre"), (w, "right")):
        for y, yal in ((0, "top"), (h // 2, "centre"), (h, "bottom")):
            PyGameTools.text_box(t, (r, g, b), 20, screen=Screen, coords=(x, y), align=(xal, yal), max_len=m)#, background=(255 - r, 255 - g, 255 - b))
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
    #break