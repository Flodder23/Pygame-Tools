import pygame


def text_box(text, colour=(0, 0, 0), size=20, screen=None, coords=None, max_len=2000, gap="auto", font="Arial", rotate=0, align=("left", "top"), background=None):
    """Creates a textbox.
    text - str - the text to be written
    colour - list (int, int, int) - the colour of the text
    size - int - the size of the text.
    screen - pygame,Surface, NoneType - the screen to be written onto
    coords - list (int, int) - the coordinates on the screen on which to put the text.
    max_len - int - the maximum length (in pixels) of a line before the text wraps around
    gap - int, str "auto" - the gap between lines.
    font - str - the font used. if not a valid font, reverts to pygame's default, which you can find out with the pygame.font.get_default_font() command.
    rotate - int - how far (clockwise) to rotate the text.
    align - list (str, str) - the alignment of the text. first string can be "left", "centre" or "right". second string can be "top", "centre" or "bottom".
    background - list (int, int, int), NoneType - the background colour. if NoneType, the background will be transparent.
    returns list(pygame.Surface, list(int, int, int))
    the pygame.Surface is the surface the textbox is written onto, and is returned regardless of whether it is blitted onto the screen in the function."""
    
    if gap == "auto":
        gap = size // 3
    if background is None:
        background = [255 - c for c in colour]
        transparent = True
    else:
        transparent = False
    font_obj = pygame.font.SysFont(font, size)
    text_surface = pygame.Surface((0, 0))
    text_surface.fill(background)
    wordinc = None
    text = text.split("\n")
    width = 0
    height = 0
    
    for line in text:
        if line == "":
            height += size + gap
            temp_surface = pygame.Surface((width, height))
            temp_surface.fill(background)
            temp_surface.blit(text_surface, (0, 0))
            text_surface = temp_surface
        inc = len(line.split())
        while inc > 0:
            line_surface = font_obj.render(line, False, colour)
            a = line_surface.get_width()
            if a > max_len:
                inc = round(len(line.split()) * (max_len / a))
                line_surface = font_obj.render(" ".join(line.split()[:inc]), False, colour)
                a = line_surface.get_width()
                if a > max_len:
                    if inc == 1:
                        word = line.split()[0]
                        wordinc = round(len(word) * (max_len / a))
                        line_surface = font_obj.render(word[:wordinc], False, colour)
                        a = line_surface.get_width()
                        if a > max_len:
                            while a > max_len:
                                wordinc -= 1
                                line_surface = font_obj.render(word[:wordinc], False, colour)
                                a = line_surface.get_width()
                        elif a < max_len:
                            while a < max_len:
                                wordinc += 1
                                line_surface = font_obj.render(word[:wordinc], False, colour)
                                a = line_surface.get_width()
                    else:
                        while a > max_len:
                            inc -= 1
                            line_surface = font_obj.render(" ".join(line.split()[:inc]), False, colour)
                            a = line_surface.get_width()
                elif a < max_len:
                    while a < max_len:
                        inc += 1
                        line_surface = font_obj.render(" ".join(line.split()[:inc]), False, colour)
                        a = line_surface.get_width()
                    inc -= 1
                    line_surface = font_obj.render(" ".join(line.split()[:inc]), False, colour)
            height += size + gap
            if a > width:
                width = a
            if inc == 1 and wordinc is not None:
                line = " ".join([word[wordinc:]] + line.split()[1:])
                wordinc = None
            else:
                line = " ".join(line.split()[inc:])

            temp_surface = pygame.Surface((width, height))
            temp_surface.fill(background)
            if align[0] == "left":
                temp_surface.blit(text_surface, (0, 0))
                temp_surface.blit(line_surface, (0, text_surface.get_height()))
            elif align[0] == "centre":
                temp_surface.blit(text_surface, ((width - text_surface.get_width()) // 2, 0))
                temp_surface.blit(line_surface, ((width - line_surface.get_width()) // 2, text_surface.get_height()))
            else:
                temp_surface.blit(text_surface, (width - text_surface.get_width(), 0))
                temp_surface.blit(line_surface, (width - line_surface.get_width(), text_surface.get_height()))
            text_surface = temp_surface
            
            inc = len(line.split())
    width += 2 * gap
    height += gap
    temp_surface = pygame.Surface((width, height))
    temp_surface.fill(background)
    temp_surface.blit(text_surface, (gap, gap))
    text_surface = temp_surface
    if transparent:
        text_surface.set_colorkey(background)
    
    if (screen, coords) != (None, None):
        x, y = coords
        if align[0] == "centre":
            x -= text_surface.get_width() // 2
        elif align[0] == "right":
            x -= text_surface.get_width()
        
        if align[1] == "centre":
            y -= text_surface.get_height() // 2
        elif align[1] == "bottom":
            y -= text_surface.get_height()

        screen.blit(text_surface, (x, y))
    return text_surface
