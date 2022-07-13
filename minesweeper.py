import pygame
import os
import random

pygame.font.init()

#window
WIDTH, HEIGHT = 500, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")

#background
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background.png")), (WIDTH, HEIGHT))

class Options:
    def __init__(self, board_size, bombsamount):
        self.board_size = board_size
        self.bombsamount = bombsamount


options = Options(20,10)
tile_size = WIDTH/options.board_size


#game assets
BLIND = pygame.transform.scale(pygame.image.load(os.path.join("assets", "blind.png")), (200,200))
OPEN_0 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "tile_0.png")), (200,200))
OPEN_1 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "tile_1.png")), (200,200))
OPEN_2 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "tile_2.png")), (200,200))
OPEN_3 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "tile_3.png")), (200,200))
OPEN_4 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "tile_4.png")), (200,200))
OPEN_5 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "tile_5.png")), (200,200))
OPEN_6 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "tile_6.png")), (200,200))
OPEN_7 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "tile_7.png")), (200,200))
OPEN_8 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "tile_8.png")), (200,200))
OPEN_BOMB = pygame.transform.scale(pygame.image.load(os.path.join("assets", "bomb.png")), (200,200))
FLAG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "flag.png")), (200,200))

TILES_NUMBER = [OPEN_0,OPEN_1,OPEN_2,OPEN_3,OPEN_4,OPEN_5,OPEN_6,OPEN_7,OPEN_8]

class Tile:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.img = BLIND
        self.blind = True
        self.is_bomb = False
        self.value = value
        self.flaged = False
        self.rect = self.img.get_rect()
        self.rect.width = tile_size
        self.rect.width = tile_size
        self.rect.x = (self.x - 1)*tile_size
        self.rect.y = (self.y - 1)*tile_size + 100
        if self.value=="*":
            self.is_bomb = True
    
    def reverse(self):
        if self.blind and not(self.flaged) and not(self.value == "*" ):
            self.blind = False
            self.img = TILES_NUMBER[self.value]
           

        if self.value == "*":
            self.img = OPEN_BOMB
            

    def flag(self):
        if not(self.flaged):
            self.flaged = True
            self.img = FLAG
    def unflag(self):
        if self.flaged:
            self.flaged = False
            self.img = BLIND


    def draw(self, window, tile_size):
        window.blit(pygame.transform.scale(self.img,(tile_size,tile_size)), ((self.x - 1)*tile_size,(self.y - 1)*tile_size + 100))

def main():
    run = True
    FPS = 60
    main_font = pygame.font.SysFont("arial",40)
    bombs_amount = options.bombsamount
    size = options.board_size
    tile_size = WIDTH/options.board_size 
    flags_amount = bombs_amount
    correct_flags = 0
    values = []
    win = False
    alive = True
    timer = 0
    timer_counter = 0

    for i in range(size):
        values_row = [-1,-1]
        for j in range(size):
            values_row.insert(1,0)
        values.append(values_row)
    border_row = []
    for i in range(size+2):
        border_row.append(-1)
    values.insert(0,border_row)
    values.append(border_row)

    tiles_coordinates=[]
    for i in range(1,size+1):
        for j in range(1,size+1):
            tiles_coordinates.append([i,j])
    bombs_coordinates = random.sample(tiles_coordinates, bombs_amount)
    for i in range(bombs_amount):
        values[bombs_coordinates[i][1]][bombs_coordinates[i][0]]="*"

    for i in bombs_coordinates:
        for j in range(i[0]-1,i[0]+2):
            for h in range(i[1]-1, i[1]+2):
                if not(values[h][j] == -1) and not(values[h][j]=="*"):
                    values[h][j] += 1

    tiles = []
    for i in range(1,size+1):
        for j in range(1,size+1):
            tile = Tile(i,j,values[j][i])
            tile.img = pygame.transform.scale(tile.img, (tile_size,tile_size))
            tile.rect = tile.img.get_rect()
            tile.rect.width = tile_size
            tile.rect.width = tile_size
            tile.rect.x = (tile.x - 1)*tile_size
            tile.rect.y = (tile.y - 1)*tile_size + 100
            tiles.append(tile)
    
    clock = pygame.time.Clock()

    def redraw_window():
        WINDOW.blit(BACKGROUND, (0,0))

        for tile in tiles:
            tile.draw(WINDOW,tile_size)

        flags_label = main_font.render(f"Flags left:{flags_amount}", 1, (255,255,255))
        WINDOW.blit(flags_label, (10,10))

        timer_label = main_font.render(f"Timer : {timer}", 1, (255,255,255))
        WINDOW.blit(timer_label,(WIDTH - timer_label.get_width()-10,10))
        
        pygame.display.update()
    
    def detonate():
        
        for tile in tiles:
            if tile.is_bomb:
                tile.reverse()
        
    while run:
        clock.tick(FPS)
        if not(win):
            redraw_window()
        
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and alive:
                x, y = event.pos
                for tile in tiles:
                    if tile.rect.collidepoint(x, y) and not(tile.flaged):
                        tile.reverse()
                        if tile.is_bomb:
                            detonate()
                            alive = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and alive:
                x, y =event.pos
                for tile in tiles:
                    if tile.rect.collidepoint(x, y) and tile.blind:
                        if not (tile.flaged):
                            if flags_amount > 0:
                                tile.flag()
                                flags_amount -= 1
                                if tile.value == "*":
                                    correct_flags +=1
                        else:
                            tile.unflag()
                            flags_amount += 1
                            if tile.value == "*":
                                correct_flags -=1 
           
        for tile in tiles:
            if tile.value == 0 and not(tile.blind):
                for tile2 in tiles:
                    if tile2.x - tile.x <= 1 and tile2.x - tile.x >= -1 and tile2.y - tile.y <= 1 and tile2.y - tile.y >= -1:
                        tile2.reverse()
        
        if correct_flags == bombs_amount + 1:
            win = True

            win_label = main_font.render("VICTORY" , 1, (0,255,0))
            pygame.draw.rect(WINDOW, (0,0,0), pygame.Rect(WIDTH/2 - win_label.get_width()/2 - 10, HEIGHT/2 - 10, win_label.get_width()+20, win_label.get_height()+20))
            WINDOW.blit(win_label, (WIDTH/2 - win_label.get_width()/2, HEIGHT/2))
            continue_label = main_font.render("Press space to continue", 1, (255,255,255))
            WINDOW.blit(continue_label, (WIDTH/2 - continue_label.get_width()/2, HEIGHT/2 + continue_label.get_height() + 30))
            pygame.display.update()
            
            if keys[pygame.K_SPACE]:
                run = False

        if alive:
            timer_counter += 1
            if timer_counter >= 60:
                timer += 1
                timer_counter = 0
        
        if not(win) and correct_flags==bombs_amount:
            correct_flags+=1

#buttons assets
START_BUTTON = pygame.transform.scale(pygame.image.load(os.path.join("assets", "startbutton.png")), (300,113))
OPTIONS_BUTTON = pygame.transform.scale(pygame.image.load(os.path.join("assets", "optionsbutton.png")), (300,113))
HIGHSCORES_BUTTON = pygame.transform.scale(pygame.image.load(os.path.join("assets", "highscoresbutton.png")), (300,113))
BUTTON_20X20 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "20x20.png")), (150,90))
BUTTON_10X10 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "10x10.png")), (150,90))
BUTTON_15X15 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "15x15.png")), (150,90))
BUTTON_5X5 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "5x5.png")), (150,90))
BUTTON_20 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "20.png")), (150,90))
BUTTON_10 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "10.png")), (150,90))
BUTTON_15 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "15.png")), (150,90))
BUTTON_5 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "5.png")), (150,90))

buttons_imgs = {"start": START_BUTTON, 
                "options": OPTIONS_BUTTON, 
                "highscore": HIGHSCORES_BUTTON,
                "20x20": BUTTON_20X20,
                "15x15": BUTTON_15X15,
                "10x10": BUTTON_10X10,
                "5x5": BUTTON_5X5,
                "20": BUTTON_20,
                "15": BUTTON_15,
                "10": BUTTON_10,
                "5": BUTTON_5
                }

class Button:
    def __init__(self, x, y, func):
        self.x = x
        self.y = y
        self.func = func
        self.img = buttons_imgs[func]
        self.rect = self.img.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
    
    def draw(self,window):
        window.blit(self.img , (self.x, self.y))

def options_window():
    run = True
    FPS = 60
    main_font = pygame.font.SysFont("arialblack", 60)
    clock = pygame.time.Clock()
    button_20x20 = Button(255, 200, "20x20")
    button_15x15 = Button(95, 200, "15x15")
    button_10x10 = Button(255, 100, "10x10")
    button_5x5 = Button(95, 100, "5x5")
    button_20 = Button(255, 500, "20")
    button_15 = Button(95, 500, "15")
    button_10 = Button(255, 400, "10")
    button_5 = Button(95, 400, "5")
    option_buttons = [button_5,button_10,button_15,button_20,button_5x5,button_10x10,button_15x15,button_20x20]
    
    def redraw_options():
        WINDOW.blit(BACKGROUND, (0,0))
        for buton in option_buttons:
            buton.draw(WINDOW)
        size_label = main_font.render("BOARD SIZE", 1,(200,200,200))
        WINDOW.blit(size_label, (WIDTH/2 - size_label.get_width()/2,10))
        bombs_label = main_font.render("BOMBS", 1,(200,200,200))
        WINDOW.blit(bombs_label, (WIDTH/2 - bombs_label.get_width()/2,310))

        pygame.display.update()
    
    while run:
        clock.tick(FPS)
        redraw_options()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if button_5.rect.collidepoint(x, y):
                    options.bombsamount = 5
                    print("bombs set to 5")
                elif button_10.rect.collidepoint(x, y):
                    options.bombsamount = 10
                    print("bombs set to 10")
                elif button_15.rect.collidepoint(x, y):
                    options.bombsamount = 15
                    print("bombs set to 15")
                elif button_20.rect.collidepoint(x, y):
                    options.bombsamount = 20
                    print("bombs set to 20")
                elif button_5x5.rect.collidepoint(x, y):
                    options.board_size = 5
                    print("size set to 5")
                elif button_10x10.rect.collidepoint(x, y):
                    options.board_size = 10
                    print("size set to 10")
                elif button_15x15.rect.collidepoint(x, y):
                    options.board_size = 15
                    print("size set to 15")
                elif button_20x20.rect.collidepoint(x, y):
                    options.board_size = 20
                    print("size set to 20")

def main_menu():
    run = True
    FPS = 60
    main_menu_font = pygame.font.SysFont("arialblack", 50)
    clock = pygame.time.Clock()
    title_label = main_menu_font.render("MINESWEEPER", 1,(200,200,200))
    start_button = Button(100, 293.5, "start")
    options_button = Button(100, 443.5, "options")

    buttons = [start_button, options_button]
    
    def redraw_main_menu():
        WINDOW.blit(BACKGROUND, (0,0))
        
        WINDOW.blit(title_label, (WIDTH/2 - title_label.get_width()/2,10))
        size_label = main_menu_font.render(f"Size:{options.board_size}X{options.board_size}", 1,(200,200,200))
        bombs_label = main_menu_font.render(f"Bombs:{options.bombsamount}", 1,(200,200,200))
        WINDOW.blit(size_label, (WIDTH/2 - size_label.get_width()/2,100))
        WINDOW.blit(bombs_label, (WIDTH/2 - bombs_label.get_width()/2,200))
        for button in buttons:
            button.draw(WINDOW)
        
        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_main_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if start_button.rect.collidepoint(x, y):
                    main()
                elif options_button.rect.collidepoint(x, y):
                    options_window()
main_menu()

        