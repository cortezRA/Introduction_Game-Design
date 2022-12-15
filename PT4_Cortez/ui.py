import pygame

class UI:
    def __init__(self,surface):

        #setup
        self.display_surface = surface

        #health
        self.health_bar = pygame.image.load('assets/ui/health_bar.png').convert_alpha()
        self.health_bar_tleft = (54,39)
        self.bar_width = 152
        self.bar_height = 4

        #coins
        self.coin = pygame.image.load('assets/ui/coins.png').convert_alpha()
        self.coin_rect = self.coin.get_rect(topleft = (50,61))
        self.font = pygame.font.Font('assets/ui/ARCADEPI.ttf',30)
    
    def show_health(self,current,full):
        self.display_surface.blit(self.health_bar,(20,10))
        current_health_ratio = current / full
        current_bar_width = self.bar_width * current_health_ratio
        health_bar_rect = pygame.Rect((self.health_bar_tleft),(current_bar_width,self.bar_height))
        pygame.draw.rect(self.display_surface,'#dc4949',health_bar_rect)

    def show_coins(self,amount):
        self.display_surface.blit(self.coin,self.coin_rect)
        coin_amount_surface = self.font.render(str(amount), False, '#000000')
        coin_amount_rect = coin_amount_surface.get_rect(midleft = (self.coin_rect.right + 4,self.coin_rect.centery))
        self.display_surface.blit(coin_amount_surface,coin_amount_rect)