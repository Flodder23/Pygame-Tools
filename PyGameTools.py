import pygame


def other_text_box(text, colour=(0, 0, 0), size=20, screen=None, coords=None, max_len=None, gap="auto", font="Arial", italic_font="auto", bold_font="auto", rotate=0, rotate_mode="centre", align=("left", "top"), background=None):
    """Creates a textbox.
    text - str - the text to be written
    colour - list (int, int, int) - the colour of the text
    size - int - the size of the text.
    screen - pygame,Surface, NoneType - the screen to be written onto
    coords - list (int, int) - the coordinates on the screen on which to put the text.
    max_len - int - the maximum length (in pixels) of a line before the text wraps around
    gap - int, str "auto" - the gap between lines.
    font - str - the font used. if not a valid font, reverts to pygame's default, which you can find out with the pygame.font.get_default_font() command.
    rotate - int - how far (clockwise) to rotate the text. it tends to do unexpected things if not a multiple of 90.
    rotate_mode - str - the mode of rotation. for "centre", when written onto the screen, it is rotated around its centre. if "absolute" it is rotated and then that surface is aligned.
    align - list (str, str) - the alignment of the text. first string can be "left", "centre" or "right". second string can be "top", "centre" or "bottom".
    background - list (int, int, int), NoneType - the background colour. if NoneType, the background will be transparent.
    returns list(pygame.Surface, list(int, int, int))
    the pygame.Surface is the surface the textbox is written onto, and is returned regardless of whether it is blitted onto the screen in the function, and is as it was before rotation"""
    
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
    text = [t.split() for t in text.split("\n")]
    width = 0
    height = 0
    space = font_obj.size(" ")[0]

    for line in text:
        line_surface = pygame.Surface((0, 0))
        line_surface.fill(background)
        for word in line:
            word_surface = pygame.Surface((0, 0))
            word_surface.fill(background)
            asterisks = 0
            for letter in word:
                if letter == "*":
                    asterisks += 1
                    if asterisks == 3:
                        font_obj.set_italic(not font_obj.get_italic())
                        font_obj.set_bold(not font_obj.get_bold())
                        asterisks = 0
                else:
                    if asterisks == 1:
                        font_obj.set_italic(not font_obj.get_italic())
                    elif asterisks == 2:
                        font_obj.set_bold(not font_obj.get_bold())
                    asterisks = 0
                    letter_surface = font_obj.render(letter, False, colour)
                    if font_obj.get_italic():
                        x = 0
                        y = -1
                        col = background
                        while col != tuple(colour):
                            y += 1
                            if y == letter_surface.get_height():
                                y = 0
                                x += 1
                            col = letter_surface.get_at((x, y))
                        left = x
                        x = letter_surface.get_width() - 1
                        y = -1
                        col = background
                        while col != tuple(colour):
                            y += 1
                            if y == letter_surface.get_height():
                                x -= 1
                                y = 0
                            col = letter_surface.get_at((x, y))
                        right = x + 1.
                        temp_surface = pygame.Surface((right - left, letter_surface.get_height()))
                        temp_surface.fill(background)
                        temp_surface.blit(letter_surface, (0, 0), area=(left, 0, right, letter_surface.get_height()))
                        letter_surface = temp_surface
                    temp_surface = pygame.Surface((letter_surface.get_width() + word_surface.get_width(), max(letter_surface.get_height(), word_surface.get_height())))
                    temp_surface.fill(background)
                    temp_surface.blit(word_surface, (0, 0))
                    temp_surface.blit(letter_surface, (word_surface.get_width(), 0))
                    word_surface = temp_surface
            if max_len is None:
                temp_surface = pygame.Surface((line_surface.get_width() + word_surface.get_width() + space, max(line_surface.get_height(), word_surface.get_height())))
                temp_surface.fill(background)
                temp_surface.blit(line_surface, (0, 0))
                temp_surface.blit(word_surface, (line_surface.get_width() + space, 0))
                line_surface = temp_surface
            else:
                if line_surface.get_width() == 0:
                    line_surface = word_surface
                else:
                    if line_surface.get_width() + word_surface.get_width() + space <= max_len:
                        temp_surface = pygame.Surface((line_surface.get_width() + word_surface.get_width() + space, max(line_surface.get_height(), word_surface.get_height())))
                        temp_surface.fill(background)
                        temp_surface.blit(line_surface, (0, 0))
                        temp_surface.blit(word_surface, (line_surface.get_width() + space, 0))
                        line_surface = temp_surface
                    else:
                        width = max(width, line_surface.get_width())
                        height += size + gap
                        temp_surface = pygame.Surface((width, height))
                        temp_surface.fill(background)
                        if align[0] == "left":
                            temp_surface.blit(text_surface, (0, 0))
                            temp_surface.blit(line_surface, (0, text_surface.get_height()))
                        elif align[0] == "centre":
                            temp_surface.blit(text_surface,
                                              ((width - text_surface.get_width()) // 2, 0))
                            temp_surface.blit(line_surface, (
                            (width - line_surface.get_width()) // 2, text_surface.get_height()))
                        else:
                            temp_surface.blit(text_surface, (width - text_surface.get_width(), 0))
                            temp_surface.blit(line_surface, (
                            width - line_surface.get_width(), text_surface.get_height()))
                        text_surface = temp_surface
                        line_surface = word_surface
            if asterisks == 1:
                font_obj.set_italic(not font_obj.get_italic())
            elif asterisks == 2:
                font_obj.set_bold(not font_obj.get_bold())
        width = max(width, line_surface.get_width())
        height += size + gap
        temp_surface = pygame.Surface((width, height))
        temp_surface.fill(background)
        if align[0] == "left":
            temp_surface.blit(text_surface, (0, 0))
            temp_surface.blit(line_surface, (0, text_surface.get_height()))
        elif align[0] == "centre":
            temp_surface.blit(text_surface, ((width - text_surface.get_width()) // 2, 0))
            temp_surface.blit(line_surface,
                              ((width - line_surface.get_width()) // 2, text_surface.get_height()))
        else:
            temp_surface.blit(text_surface, (width - text_surface.get_width(), 0))
            temp_surface.blit(line_surface,
                              (width - line_surface.get_width(), text_surface.get_height()))
        text_surface = temp_surface
    if (screen, coords) != (None, None):
        if rotate_mode == "absolute":
            text_surface = pygame.transform.rotate(text_surface, rotate)
        else:
            a, b = text_surface.get_size()
        x, y = coords
        if align[0] == "centre":
            x -= text_surface.get_width() // 2
        elif align[0] == "right":
            x -= text_surface.get_width()
        if align[1] == "centre":
            y -= text_surface.get_height() // 2
        elif align[1] == "bottom":
            y -= text_surface.get_height()
        if rotate_mode == "centre":
            text_surface = pygame.transform.rotate(text_surface, rotate)
            c, d = text_surface.get_size()
            x -= (c - a) // 2
            y -= (d - b) // 2
        if transparent:
            text_surface.set_colorkey(background)
        screen.blit(text_surface, (x, y))
