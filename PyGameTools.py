import pygame


def crop_to_colour(surface, colour, cushion=0, left=True, right=True, top=True, bottom=True, include=False):
    """Crops a surface to delete as much background as possible.
    if include is False, it will crop to delete as much of that colour as possible, while not deleting any ther colour
    if include is True, it will crop to keep all pixels of that colour"""
    colour = tuple(colour)
    x = 0
    y = -1
    if include:
        col = tuple([255 - c for c in colour])
    else:
        col = colour
    not_there = False
    while include != (col == colour):
        y += 1
        if y == surface.get_height():
            y = 0
            x += 1
        if x == surface.get_width():
            not_there = True
            include = col == colour
        else:
            col = surface.get_at((x, y))
    if not_there:
        right = False
        top = False
        bottom = False
    elif left: l_crop = max(0, x - cushion)
    else: l_crop = 0
        
    if right:
        x = surface.get_width() - 1
        y = -1
        if include:
            col = tuple([255 - c for c in colour])
        else:
            col = colour
        while include != (col == colour):
            y += 1
            if y == surface.get_height():
                x -= 1
                y = 0
            col = surface.get_at((x, y))
        r_crop = min(surface.get_width(), x + 1 + cushion)
    else: r_crop = surface.get_width()
    
    if top:
        x = -1
        y = 0
        if include:
            col = tuple([255 - c for c in colour])
        else:
            col = colour
        while include != (col == colour):
            x += 1
            if x == surface.get_width():
                x = 0
                y += 1
            col = surface.get_at((x, y))
        t_crop = max(0, y - cushion)
    else: t_crop = 0
    
    if bottom:
        x = -1
        y = surface.get_height() - 1
        if include:
            col = tuple([255 - c for c in colour])
        else:
            col = colour
        while include != (col == colour):
            x += 1
            if x == surface.get_width():
                x = 0
                y -= 1
            col = surface.get_at((x, y))
        b_crop = min(y + cushion, surface.get_height())
    else: b_crop = surface.get_height()
    
    if not_there:
        l_crop = surface.get_width()
        t_crop = surface.get_height()
    
    result_surface = pygame.Surface((r_crop - l_crop, b_crop - t_crop))
    result_surface.set_colorkey(surface.get_colorkey())
    if surface.get_colorkey() is not None: result_surface.fill(surface.get_colorkey())
    result_surface.blit(surface, (0, 0), area=(l_crop, t_crop, r_crop, b_crop))
    return result_surface, (r_crop, l_crop, t_crop, b_crop)
    

def join(surface1, surface2, background, cushion=0, transparent=False, align=(("right", "outside"), ("top", "inside"))):
    """joins surface1 onto surface2.
    surface1 - pygame.Surface - the surface to stick surface 2 next to
    surface2 - pygame.Surface - the surface to stick next to surface1
    cushion - int - the cushion (space) in pixels betweeen the surfaces
    background - list(int, int, int) - the colour of the background. if transparent is True, this will be the colour selected to be transparent.
    align - list((str1, str2), (str3, str4)) - how to align surface1 relative to surface2.
    str1 can be "left", "centre" or "right"
    str2 can be "inside" or "outside"
    str3 can be "top", "centre" or "bottom".
    str4 can be "inside" or "outside"."""
    
    if align[0][0] == "centre":
        width = max(surface1.get_width(), surface2.get_width())
        x1 = (width - surface1.get_width()) // 2
        x2 = (width - surface2.get_width()) // 2
    else:
        if align[0][1] == "inside": width = max(surface1.get_width(), surface2.get_width())
        else: width = surface1.get_width() + surface2.get_width() + cushion
        
        if align[0][0] == "left":
            if align[0][1] == "inside":
                x1 = 0
                x2 = 0
            else:
                x1 = surface2.get_width() + cushion
                x2 = 0
        else:
            if align[0][1] == "inside":
                x1 = width - surface1.get_width()
                x2 = width - surface2.get_width()
            else:
                x1 = 0
                x2 = surface1.get_width() + cushion

    if align[1][0] == "centre":
        height = max(surface1.get_height(), surface2.get_height())
        y1 = (height - surface1.get_height()) // 2
        y2 = (height - surface2.get_height()) // 2
    else:
        if align[1][1] == "inside": height = max(surface1.get_height(), surface2.get_height())
        else: height = surface1.get_height() + surface2.get_height() + cushion

        if align[1][0] == "top":
            if align[1][1] == "inside":
                y1 = 0
                y2 = 0
            else:
                y1 = surface2.get_height() + cushion
                y2 = 0
        else:
            if align[1][1] == "inside":
                y1 = height - surface1.get_height()
                y2 = height - surface1.get_height()
            else:
                y1 = 0
                y2 = surface1.get_height() + cushion

    result_surface = pygame.Surface((width, height))
    result_surface.fill(background)
    if transparent: result_surface.set_colorkey(background)
    result_surface.blit(surface1, (x1, y1))
    result_surface.blit(surface2, (x2, y2))
    return result_surface
    

def write(text, colour=(0, 0, 0), size=20, screen=None, coords=None, max_len=None, gap="auto", font="Arial", rotate=0, rotate_mode="centre", align=("left", "top"), background=None, fill_space=True):
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
    fill_space - bool - if this is True, the surface with the text will be the size of the max_len, otherwise it will be the size of the longest line of text
    returns pygame.Surface - the surface the textbox is written onto, and is returned regardless of whether it is blitted onto the screen in the function, and is as it was before rotation"""
    
    if gap == "auto": gap = size // 3
    if background is None:
        background = [255 - c for c in colour]
        transparent = True
    else: transparent = False
    font_obj = pygame.font.SysFont(font, size)
    text_surface = pygame.Surface((0, 0))
    text_surface.fill(background)
    space, height = font_obj.size(" ")
    cropped_e = crop_to_colour(font_obj.render("e", False, colour), colour, include=True, left=False, right=False)
    strike_height = (cropped_e[1][2] + cropped_e[1][3]) // 2
    strike_size = size // 8
    underline_size = strike_size
    underline_height = cropped_e[1][3] + underline_size // 2 + 2
    line_surface = pygame.Surface((0, height))
    line_surface.fill(background)
    word_surface = pygame.Surface((0, height))
    word_surface.fill(background)
    asterisks = 0
    hyphens = 0
    strike = False
    underline = False
    ignore = False

    for place, letter in enumerate(text):
        if letter == "/" and not ignore: ignore = True
        elif letter == "*" and not ignore:
            asterisks += 1
            if hyphens == 1: underline = not underline
            elif hyphens == 2: strike = not strike
            hyphens = 0
            if asterisks == 3:
                font_obj.set_italic(not font_obj.get_italic())
                font_obj.set_bold(not font_obj.get_bold())
                asterisks = 0
        elif letter == "-" and not ignore:
            hyphens += 1
            if asterisks == 1: font_obj.set_italic(not font_obj.get_italic())
            elif asterisks == 2: font_obj.set_bold(not font_obj.get_bold())
            asterisks = 0
            if hyphens == 3:
                underline = not underline
                strike = not strike
                hyphens = 0
        else:
            if asterisks == 1: font_obj.set_italic(not font_obj.get_italic())
            elif asterisks == 2: font_obj.set_bold(not font_obj.get_bold())
            elif hyphens == 1: underline = not underline
            elif hyphens == 2: strike = not strike
            asterisks = 0
            hyphens = 0
            ignore = False

            if letter == "\n":
                line_surface = join(line_surface, word_surface, background)
                text_surface = join(text_surface, line_surface, background, cushion=gap, align=((align[0], "inside"), ("bottom", "outside")))
                line_surface = pygame.Surface((0, height))
                word_surface = pygame.Surface((0, height))
            else:
                letter_surface = font_obj.render(letter, False, colour)
                cushion = 2 if font_obj.get_italic() else 1
                if letter == " ":
                    line_surface = join(line_surface, word_surface, background)
                    word_surface = pygame.Surface((0, height))
                else: letter_surface = crop_to_colour(letter_surface, colour, top=False, bottom=False, include=True, cushion=cushion)[0]
                if strike: pygame.draw.line(letter_surface, colour, (0, strike_height), (letter_surface.get_width(), strike_height), strike_size)
                if underline: pygame.draw.line(letter_surface, colour, (0, underline_height), (letter_surface.get_width(), underline_height), underline_size)
                if max_len is not None:
                    if line_surface.get_width() + word_surface.get_width() + letter_surface.get_width() >= max_len:
                        if line_surface.get_width() > 0:
                            text_surface = join(text_surface, line_surface, background, cushion=gap, align=((align[0], "inside"), ("bottom", "outside")))
                            line_surface = pygame.Surface((0, height))
                            if word_surface.get_width() > 0: word_surface = crop_to_colour(word_surface, colour, top=False, bottom=False, right=False, include=True)[0]
                        else:
                            text_surface = join(text_surface, word_surface, background, cushion=gap, align=((align[0], "inside"), ("bottom", "outside")))
                            word_surface = pygame.Surface((0, height))
                word_surface = join(word_surface, letter_surface, background)
                
    line_surface = join(line_surface, word_surface, background)
    text_surface = join(text_surface, line_surface, background, cushion=gap, align=((align[0], "inside"), ("bottom", "outside")))
    if fill_space and max_len is not None:
        temp_surface = pygame.Surface((max_len, text_surface.get_height()))
        temp_surface.fill(background)
        text_surface = join(temp_surface, text_surface, background, cushion=gap, align=((align[0], "inside"), ("top", "inside")))
    if transparent: text_surface.set_colorkey(background)
    plain_text_surface = text_surface
    if (screen, coords) != (None, None):
        if rotate_mode == "absolute": text_surface = pygame.transform.rotate(text_surface, rotate)
        else: a, b = text_surface.get_size()
        x, y = coords
        if align[0] == "centre": x -= text_surface.get_width() // 2
        elif align[0] == "right": x -= text_surface.get_width()
        if align[1] == "centre": y -= text_surface.get_height() // 2
        elif align[1] == "bottom": y -= text_surface.get_height()
        if rotate_mode == "centre":
            text_surface = pygame.transform.rotate(text_surface, rotate)
            c, d = text_surface.get_size()
            x -= (c - a) // 2
            y -= (d - b) // 2
        screen.blit(text_surface, (x, y))
    return plain_text_surface
