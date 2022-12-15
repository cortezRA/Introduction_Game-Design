import pygame
from support import *
from settings import *
from game_data import levels
from tile import *
from enemies import *
from decoration import Water
from player import Player
from particles import ParticleEffect

class Level:
    def __init__(self,current_level,surface,create_overworld,change_coins,change_health):
        #general setup
        self.display_surface = surface
        self.world_shift = 0
        self.current_x = None
        self.player_on_ground = False

        #sound effects
        self.coin_sound = pygame.mixer.Sound('audio/sfx/coin.wav')
        self.stomp_sound = pygame.mixer.Sound('audio/sfx/stomp.wav')

        #overworld connection
        self.create_overworld = create_overworld
        self.current_level = current_level
        level_data = levels[self.current_level]
        self.new_max_level = level_data['unlock']

        #user interface
        self.change_coins = change_coins

        #dust
        self.dust_sprite = pygame.sprite.GroupSingle()
        #explosion
        self.explosion_sprites = pygame.sprite.Group()

        #player setup
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal  = pygame.sprite.GroupSingle()
        self.player_setup(player_layout,change_health)
        #terrain setup
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout,'terrain')
        #midterrain setup
        midterrain_layout = import_csv_layout(level_data['midterrain'])
        self.midterrain_sprites = self.create_tile_group(midterrain_layout,'midterrain')
        #backterrain setup
        backterrain_layout = import_csv_layout(level_data['backterrain'])
        self.backterrain_sprites = self.create_tile_group(backterrain_layout,'terrain')
        #grass setup
        grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout,'grass')
        #coins setup
        coin_layout = import_csv_layout(level_data['coins'])
        self.coin_sprites = self.create_tile_group(coin_layout,'coins')
        #foreground palms
        fore_ptrees_layout = import_csv_layout(level_data['fore_ptrees'])
        self.fore_ptrees_sprites = self.create_tile_group(fore_ptrees_layout,'fore_ptrees')
        #background palms
        back_ptrees_layout = import_csv_layout(level_data['back_ptrees'])
        self.back_ptrees_sprites = self.create_tile_group(back_ptrees_layout,'back_ptrees')
        #enemies
        enemyM_layout = import_csv_layout(level_data['enemy_melee'])
        self.enemyM_sprites = self.create_tile_group(enemyM_layout,'enemy_melee')
        if current_level == 1:
            enemyH_layout = import_csv_layout(level_data['enemy_helmet'])
            self.enemyH_sprites = self.create_tile_group(enemyH_layout,'enemy_helmet')
        #constraints
        constraint_layout = import_csv_layout(level_data['constraints'])
        self.constraint_sprites = self.create_tile_group(constraint_layout,'constraints')
        #decoration
        level_width = len(terrain_layout[0]) * tile_size
        self.water = Water(screen_height - 40, level_width)

    def create_tile_group(self,layout,type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphics('assets/terrain/terrain_tiles.png')
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y,tile_surface)
                    if type == 'midterrain':
                        midterrain_tile_list = import_cut_graphics('assets/terrain/terrain_tiles.png')
                        tile_surface = midterrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y,tile_surface)
                    if type == 'backterrain':
                        backterrain_tile_list = import_cut_graphics('assets/terrain/terrain_tiles.png')
                        tile_surface = backterrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y,tile_surface)
                    if type == 'grass':
                        grass_tile_list = import_cut_graphics('assets/decoration/grass/grass.png')
                        tile_surface = grass_tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y,tile_surface)
                    if type == 'coins':
                        if val == '0': sprite = Coin(tile_size,x,y,'assets/coins/gold',5)
                        if val == '1': sprite = Coin(tile_size,x,y,'assets/coins/silver',1)
                    if type == 'fore_ptrees':
                        if val == '1': sprite = Palm(tile_size,x,y,'assets/terrain/palm_large',68)
                        if val == '2': sprite = Palm(tile_size,x,y,'assets/terrain/palm_small',38)
                    if type == 'back_ptrees':
                        sprite = Palm(tile_size,x,y,'assets/terrain/palm_bg',68)
                    if type == 'enemy_melee':
                        sprite = EnemyMelee(tile_size,x,y)
                    if type == 'enemy_helmet':
                        sprite = EnemyHelmet(tile_size,x,y)
                    if type == 'constraints':
                        sprite = Tile(tile_size,x,y)

                    sprite_group.add(sprite)
    
        return sprite_group

    def player_setup(self,layout,change_health):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                
                if val == '2':
                    sprite = Player((x,y),self.display_surface,self.create_jump_particles,change_health)
                    self.player.add(sprite)
                if val == '1':
                    character_surface = pygame.image.load('assets/player/orb.png').convert_alpha()
                    sprite = StaticTile(tile_size,x,y,character_surface)
                    self.goal.add(sprite)
                    
    def enemy_collision_reverse(self):
        for enemy in self.enemyM_sprites.sprites():
            if pygame.sprite.spritecollide(enemy,self.constraint_sprites,False):
                enemy.reverse()
        
        if self.current_level == 1:
            for enemy in self.enemyH_sprites.sprites():
                if pygame.sprite.spritecollide(enemy,self.constraint_sprites,False):
                    enemy.reverse()

    def create_jump_particles(self,pos):
        if self.player.sprite.rfacing:
            pos -= pygame.math.Vector2(10,5)
        else:
            pos += pygame.math.Vector2(10,5)
        jump_particle_sprite = ParticleEffect(pos,'jump')
        self.dust_sprite.add(jump_particle_sprite)
    
    def x_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        collidable_sprites = self.terrain_sprites.sprites() #+ self.fore_ptrees_sprites.sprites() + self.midterrain_sprites.sprites()

        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_lwall = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_rwall = True
                    self.current_x = player.rect.right
        
        if player.on_lwall and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_lwall = False
        if player.on_rwall and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_rwall = False
    
    def y_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        collidable_sprites = self.terrain_sprites.sprites() #+ self.fore_ptrees_sprites.sprites() + self.midterrain_sprites.sprites()

        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True
        
        for sprite in self.midterrain_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if sprite.rect.top - player.rect.top >= 60 and player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False
    
    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 5
            player.speed = 0
        elif player_x > screen_width*(3/4) and direction_x > 0:
            self.world_shift = -5
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 5
    
    def check_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def landing_dust(self):
        if not(self.player_on_ground) and self.player.sprite.on_ground and not(self.dust_sprite.sprites()):
            if self.player.sprite.rfacing:
                offset = pygame.math.Vector2(5,15)
            else:
                offset = pygame.math.Vector2(5,15)
            
            fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset,'land')
            self.dust_sprite.add(fall_dust_particle)

    def check_death(self):
        if self.player.sprite.rect.top > screen_height:
            self.create_overworld(self.current_level,0)

    def check_win(self):
        if pygame.sprite.spritecollide(self.player.sprite,self.goal,False):
            self.create_overworld(self.current_level,self.new_max_level)

    def check_coin_collisions(self):
        collided_coins = pygame.sprite.spritecollide(self.player.sprite,self.coin_sprites,True)
        if collided_coins:
            for coin in collided_coins:
                self.change_coins(coin.value)
                self.coin_sound.play()
        
        enemyM_collisions = pygame.sprite.spritecollide(self.player.sprite,self.enemyM_sprites,False)
        if enemyM_collisions:
            for coin in enemyM_collisions:
                self.change_coins(2)

        if self.current_level == 1:
            enemyH_collisions = pygame.sprite.spritecollide(self.player.sprite,self.enemyH_sprites,False)

            if enemyH_collisions:
                for coin in enemyM_collisions:
                    self.change_coins(3)

    def check_enemy_collisions(self):
        enemyM_collisions = pygame.sprite.spritecollide(self.player.sprite,self.enemyM_sprites,False)

        if enemyM_collisions:
            for enemy in enemyM_collisions:
                enemy_center = enemy.rect.centery
                enemy_top = enemy.rect.top
                player_bottom = self.player.sprite.rect.bottom

                if enemy_top < player_bottom < enemy_center and self.player.sprite.direction.y >= 0:
                    self.stomp_sound.play()
                    self.player.sprite.direction.y = -15
                    explosion_sprite = ParticleEffect(enemy.rect.center,'explosion')
                    self.explosion_sprites.add(explosion_sprite)
                    enemy.kill()
                else:
                    self.player.sprite.get_damaged()
            
        if self.current_level == 1:
            enemyH_collisions = pygame.sprite.spritecollide(self.player.sprite,self.enemyH_sprites,False)

            if enemyH_collisions:
                for enemy in enemyH_collisions:
                    enemy_center = enemy.rect.centery
                    enemy_top = enemy.rect.top
                    player_bottom = self.player.sprite.rect.bottom

                    if enemy_top < player_bottom < enemy_center and self.player.sprite.direction.y >= 0:
                        self.stomp_sound.play()
                        self.player.sprite.direction.y = -15
                        explosion_sprite = ParticleEffect(enemy.rect.center,'explosion')
                        self.explosion_sprites.add(explosion_sprite)
                        enemy.kill()
                    else:
                        self.player.sprite.get_damaged()

    def run(self):
        #background palms
        self.back_ptrees_sprites.update(self.world_shift)
        self.back_ptrees_sprites.draw(self.display_surface)

        #backterrains
        self.backterrain_sprites.update(self.world_shift)
        self.backterrain_sprites.draw(self.display_surface)

        #dust particles
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)

        #terrains
        self.midterrain_sprites.update(self.world_shift)
        self.midterrain_sprites.draw(self.display_surface)
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)

        #grass
        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display_surface)

        #enemy melee and constraints
        self.enemyM_sprites.update(self.world_shift)
        if self.current_level == 1:
            self.enemyH_sprites.update(self.world_shift)
        self.constraint_sprites.update(self.world_shift)
        self.enemy_collision_reverse()
        self.enemyM_sprites.draw(self.display_surface)
        if self.current_level == 1:
            self.enemyH_sprites.draw(self.display_surface)
        self.explosion_sprites.update(self.world_shift)
        self.explosion_sprites.draw(self.display_surface)

        #player
        self.player.update()
        self.x_movement_collision()
        self.check_on_ground()
        self.y_movement_collision()
        self.landing_dust()

        self.scroll_x()
        self.player.draw(self.display_surface)
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)

        self.check_death()
        self.check_win()
        self.check_coin_collisions()
        self.check_enemy_collisions()

        #foreground palms
        self.fore_ptrees_sprites.update(self.world_shift)
        self.fore_ptrees_sprites.draw(self.display_surface)

        #coins
        self.coin_sprites.update(self.world_shift)
        self.coin_sprites.draw(self.display_surface)

        #water
        self.water.draw(self.display_surface,self.world_shift)
