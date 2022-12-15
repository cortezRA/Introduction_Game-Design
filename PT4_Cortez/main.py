import pygame, sys
from settings import *
from overworld import Overworld
from level import Level
from ui import UI

class Game:
    def __init__(self):
        #game attributes
        self.max_level = 0
        self.max_health = 75
        self.current_health = 75
        self.coins = 0

        #overworld creation
        self.overworld = Overworld(0,self.max_level,window,self.create_level)
        self.status = 'overworld'

        #UI
        self.ui = UI(window)

        #audio
        self.level_music = pygame.mixer.Sound('audio/level_music.wav')
        self.overworld_music = pygame.mixer.Sound('audio/overworld_music.wav')
        self.overworld_music.play(loops = -1)

    def create_level(self,current_level):
        self.level = Level(current_level,window,self.create_overworld,self.change_coins,self.change_health)
        self.status = 'level'
        self.overworld_music.stop()
        self.level_music.play(loops = -1)

    def create_overworld(self,current_level,new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(current_level,self.max_level,window,self.create_level)
        self.status = 'overworld'
        self.level_music.stop()
        self.overworld_music.play(loops = -1)

    def change_coins(self,coin_amount):
        self.coins += coin_amount

    def change_health(self,amount):
        self.current_health += amount

    def check_game_over(self):
        if self.current_health <= 0:
            self.current_health = 75
            self.coins = 0
            self.max_level = 0
            self.overworld = Overworld(0,self.max_level,window,self.create_level)
            self.status = 'overworld'
            self.level_music.stop()

    def updateFile(self):
        f = open('scores.txt','r')
        file = f.readlines()
        last = int(file[0])

        if last < self.coins:
            f.close()
            file = open('scores.txt', 'w')
            file.write(str(self.coins))
            file.close()

            return self.coins
                
        return last
    
    def show_best(self):
        font = pygame.font.Font('assets/ui/ARCADEPI.ttf',30)
        lastScore = font.render('Best Score: ' + str(self.updateFile()),1,(0,0,0))
        window.blit(lastScore, (900,50))

    def run (self):
        if self.status == 'overworld':
            self.overworld.run()
        elif self.status == 'level':
            self.level.run()
            self.ui.show_health(self.current_health,self.max_health)
            self.ui.show_coins(self.coins)
            self.show_best()
            self.check_game_over()

#pygame setup
pygame.init()
window = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Treasure Isle")
clock = pygame.time.Clock()
game = Game()

bg = pygame.image.load('assets/bg_layers/game_background_1.png').convert_alpha()
bg = pygame.transform.smoothscale(bg,(1280,720))

run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    window.blit(bg,(0,0))
    
    game.run()

    pygame.display.update()
    clock.tick(60)