# Adding scoring and chracter health, enemy-to-player collision

import pygame

pygame.init()

WINDOW_SIZE = 1200
WINDOW_HEIGHT = 667
window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_HEIGHT))

pygame.display.set_caption("Game with Sprites and Assets")
pygame.display.update()

# source images/sprite
bg = pygame.image.load('assets/bg.jpg')
walkRight = [pygame.image.load('assets/walk_right/r1.png'),pygame.image.load('assets/walk_right/r2.png'),
    pygame.image.load('assets/walk_right/r3.png'),pygame.image.load('assets/walk_right/r4.png'),pygame.image.load('assets/walk_right/r5.png'),
    pygame.image.load('assets/walk_right/r6.png'),pygame.image.load('assets/walk_right/r7.png'),pygame.image.load('assets/walk_right/r8.png'),
    pygame.image.load('assets/walk_right/r9.png'),pygame.image.load('assets/walk_right/r10.png'),pygame.image.load('assets/walk_right/r11.png'),
    pygame.image.load('assets/walk_right/r12.png')]
walkRight = [pygame.transform.smoothscale(x, (260,220)) for x in walkRight]
walkLeft = [pygame.transform.smoothscale(x, (260,220)) for x in walkRight]
walkLeft = [pygame.transform.flip(x, True, False) for x in walkLeft]
idle_right = [pygame.image.load('assets/idle/i1.png'),pygame.image.load('assets/idle/i2.png'),pygame.image.load('assets/idle/i3.png'),
    pygame.image.load('assets/idle/i4.png'),pygame.image.load('assets/idle/i5.png'),pygame.image.load('assets/idle/i6.png'),
    pygame.image.load('assets/idle/i7.png'),pygame.image.load('assets/idle/i8.png'),pygame.image.load('assets/idle/i9.png'),
    pygame.image.load('assets/idle/i10.png'),pygame.image.load('assets/idle/i11.png'),pygame.image.load('assets/idle/i12.png')]
idle_right = [pygame.transform.smoothscale(x, (260,220)) for x in idle_right]
idle_left = [pygame.transform.smoothscale(x, (260,220)) for x in idle_right]
idle_left = [pygame.transform.flip(x, True, False) for x in idle_left]
spellcast_right = [pygame.image.load('assets/spellcast_right/sr1.png'),pygame.image.load('assets/spellcast_right/sr2.png'),pygame.image.load('assets/spellcast_right/sr3.png'),
    pygame.image.load('assets/spellcast_right/sr4.png'),pygame.image.load('assets/spellcast_right/sr5.png'),pygame.image.load('assets/spellcast_right/sr6.png'),
    pygame.image.load('assets/spellcast_right/sr7.png'),pygame.image.load('assets/spellcast_right/sr8.png'),pygame.image.load('assets/spellcast_right/sr9.png'),
    pygame.image.load('assets/spellcast_right/sr10.png'),pygame.image.load('assets/spellcast_right/sr11.png'),pygame.image.load('assets/spellcast_right/sr12.png'),
    pygame.image.load('assets/spellcast_right/sr13.png'),pygame.image.load('assets/spellcast_right/sr14.png'),pygame.image.load('assets/spellcast_right/sr15.png'),
    pygame.image.load('assets/spellcast_right/sr16.png'),pygame.image.load('assets/spellcast_right/sr17.png'),pygame.image.load('assets/spellcast_right/sr18.png')]
spellcast_right = [pygame.transform.smoothscale(x, (260,220)) for x in spellcast_right]
spellcast_left = [pygame.transform.smoothscale(x, (260,220)) for x in spellcast_right]
spellcast_left = [pygame.transform.flip(x, True, False) for x in spellcast_left]
orb = pygame.image.load('assets/orb.png')
orb = pygame.transform.smoothscale(orb, (32,32))
hurt_right = [pygame.image.load('assets/hurt/h1.png'),pygame.image.load('assets/hurt/h2.png'),pygame.image.load('assets/hurt/h3.png'),
    pygame.image.load('assets/hurt/h4.png'),pygame.image.load('assets/hurt/h5.png'),pygame.image.load('assets/hurt/h6.png'),
    pygame.image.load('assets/hurt/h7.png'),pygame.image.load('assets/hurt/h8.png'),pygame.image.load('assets/hurt/h9.png'),
    pygame.image.load('assets/hurt/h10.png'),pygame.image.load('assets/hurt/h11.png'),pygame.image.load('assets/hurt/h12.png')]
hurt_right = [pygame.transform.smoothscale(x, (260,220)) for x in hurt_right]
hurt_left = [pygame.transform.smoothscale(x, (260,220)) for x in hurt_right]
hurt_left = [pygame.transform.flip(x, True, False) for x in hurt_left]
dead_right = [pygame.image.load('assets/dead/d1.png'),pygame.image.load('assets/dead/d2.png'),pygame.image.load('assets/dead/d3.png'),
    pygame.image.load('assets/dead/d4.png'),pygame.image.load('assets/dead/d5.png'),pygame.image.load('assets/dead/d6.png'),
    pygame.image.load('assets/dead/d7.png'),pygame.image.load('assets/dead/d8.png'),pygame.image.load('assets/dead/d9.png'),
    pygame.image.load('assets/dead/d10.png'),pygame.image.load('assets/dead/d11.png'),pygame.image.load('assets/dead/d12.png'),
    pygame.image.load('assets/dead/d13.png'),pygame.image.load('assets/dead/d14.png'),pygame.image.load('assets/dead/d15.png')]
dead_right = [pygame.transform.smoothscale(x, (260,220)) for x in dead_right]
dead_left = [pygame.transform.smoothscale(x, (260,220)) for x in dead_right]
dead_left = [pygame.transform.flip(x, True, False) for x in dead_left]


score = 0 # new added variable

class player(object):
    def __init__(self,x,y,width,height):
        # sprite facing position
        self.left = False    # facing left
        self.right = True   # facing right
        self.walk_ctr = 0    #character animation
        self.stand_ctr = 0
        self.cast_ctr = 0
        self.hurt_ctr = 0
        self.dead_ctr = 0

        #initial character positions
        self.x = x
        self.y = y

        #character dimensions
        self.width = width
        self.height = height
        self.speed = 8

        self.isJump = False
        self.jumpCount = 10 #gravity
        self.isStanding = False
        self.isWalking = False
        self.isCasting = False
        self.isHurt = False
        self.isDead = False

        self.hitSize = (self.x+70, self.y+15, self.width-150, self.height-50) #rectangle hit size of player

        self.health = 3
        self.totalHealth = 3

        self.visible = True

    def draw(self,window):
        
        if (self.walk_ctr +1 >= 36):
            self.walk_ctr = 0
        if (self.stand_ctr +1 >= 36):
            self.stand_ctr = 0
        if (self.cast_ctr +1 >= 36):
            self.cast_ctr = 0
        if (self.hurt_ctr +1 >= 36):
            self.isHurt = False
            self.hurt_ctr = 0
        if (self.dead_ctr +1 >= 45):
            self.visible = False
        
        if self.visible:
            if self.isDead:
                if self.left:
                    window.blit(dead_left[self.dead_ctr//3],(self.x,self.y))
                    self.walk_ctr = 0
                    self.stand_ctr = 0
                    self.cast_ctr = 0
                    self.hurt_ctr = 0
                    self.dead_ctr += 1
                elif self.right:
                    window.blit(dead_right[self.dead_ctr//3],(self.x,self.y))
                    self.walk_ctr = 0
                    self.stand_ctr = 0
                    self.cast_ctr = 0
                    self.hurt_ctr = 0
                    self.dead_ctr += 1
            elif self.isHurt:
                if self.left:
                    window.blit(hurt_left[self.hurt_ctr//3],(self.x,self.y))
                    self.walk_ctr = 0
                    self.stand_ctr = 0
                    self.cast_ctr = 0
                    self.hurt_ctr += 1
                elif self.right:
                    window.blit(hurt_right[self.hurt_ctr//3],(self.x,self.y))
                    self.walk_ctr = 0
                    self.stand_ctr = 0
                    self.cast_ctr = 0
                    self.hurt_ctr += 1
            elif self.isCasting:
                if self.left:
                    window.blit(spellcast_left[self.cast_ctr//2],(self.x,self.y))
                    self.walk_ctr = 0
                    self.stand_ctr = 0
                    self.cast_ctr += 1
                elif self.right:
                    window.blit(spellcast_right[self.cast_ctr//2],(self.x,self.y))
                    self.walk_ctr = 0
                    self.stand_ctr = 0
                    self.cast_ctr += 1
            elif self.isWalking:
                if self.left:
                    window.blit(walkLeft[self.walk_ctr//3],(self.x,self.y))
                    self.walk_ctr +=1
                    self.stand_ctr = 0
                    self.cast_ctr = 0
                elif self.right:
                    window.blit(walkRight[self.walk_ctr//3],(self.x,self.y))
                    self.walk_ctr +=1
                    self.stand_ctr = 0
                    self.cast_ctr = 0
            else:
                if self.left:
                    window.blit(idle_left[self.stand_ctr//3], (self.x,self.y))
                    self.walk_ctr = 0
                    self.cast_ctr = 0
                    self.stand_ctr += 1
                elif self.right:
                    window.blit(idle_right[self.stand_ctr//3], (self.x,self.y))
                    self.walk_ctr = 0
                    self.cast_ctr = 0
                    self.stand_ctr += 1
            
            pygame.draw.rect(window, (255,0,0), (self.hitSize[0],self.hitSize[1],self.hitSize[2],self.hitSize[3] - 150))
            pygame.draw.rect(window, (0,255,0), (self.hitSize[0],self.hitSize[1],self.hitSize[2] * (self.health/self.totalHealth),self.hitSize[3] - 150))

            if self.isDead:
                self.hitSize = (0,0,0,0)
            elif self.left:
                self.hitSize = (self.x+85, self.y+15, self.width-150, self.height-50) #rectangle hit size of player
            elif self.right:
                self.hitSize = (self.x+70, self.y+15, self.width-150, self.height-50) #rectangle hit size of player
        
    def hit(self):
        if self.health > 1:
            self.health -= 1
        else:
            self.health = 0


#Player projectile handling
class projectile(object):
    def __init__(self,x,y,facing):
        self.x = x
        self.y = y
        self.facing = facing
        self.speed = 8 * facing
    
    def draw(self,window):
        window.blit(orb, (self.x,self.y))


#enemy class
class enemy(object):
    walkRight = [pygame.image.load('assets/enemy_walk/r1.png'),pygame.image.load('assets/enemy_walk/r2.png'),pygame.image.load('assets/enemy_walk/r3.png'),
        pygame.image.load('assets/enemy_walk/r4.png'),pygame.image.load('assets/enemy_walk/r5.png'),pygame.image.load('assets/enemy_walk/r6.png'),
        pygame.image.load('assets/enemy_walk/r7.png'),pygame.image.load('assets/enemy_walk/r8.png'),pygame.image.load('assets/enemy_walk/r9.png'),
        pygame.image.load('assets/enemy_walk/r10.png'),pygame.image.load('assets/enemy_walk/r11.png'),pygame.image.load('assets/enemy_walk/r12.png')]
    walkRight = [pygame.transform.smoothscale(x, (260,220)) for x in walkRight]
    walkLeft = [pygame.transform.smoothscale(x, (260,220)) for x in walkRight]
    walkLeft = [pygame.transform.flip(x, True, False) for x in walkLeft]
    dead_right = [pygame.image.load('assets/enemy_dead/d1.png'),pygame.image.load('assets/enemy_dead/d2.png'),pygame.image.load('assets/enemy_dead/d3.png'),
        pygame.image.load('assets/enemy_dead/d4.png'),pygame.image.load('assets/enemy_dead/d5.png'),pygame.image.load('assets/enemy_dead/d6.png'),
        pygame.image.load('assets/enemy_dead/d7.png'),pygame.image.load('assets/enemy_dead/d8.png'),pygame.image.load('assets/enemy_dead/d9.png'),
        pygame.image.load('assets/enemy_dead/d10.png'),pygame.image.load('assets/enemy_dead/d11.png'),pygame.image.load('assets/enemy_dead/d12.png'),
        pygame.image.load('assets/enemy_dead/d13.png'),pygame.image.load('assets/enemy_dead/d14.png'),pygame.image.load('assets/enemy_dead/d15.png'),]
    dead_right = [pygame.transform.smoothscale(x, (260,220)) for x in dead_right]
    dead_left = [pygame.transform.smoothscale(x, (260,220)) for x in dead_right]
    dead_left = [pygame.transform.flip(x, True, False) for x in dead_left]

    def __init__(self,x,y,width,height,end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.path = [x,end] #walking path for enemy
        
        self.hitSize = (self.x+70, self.y+15, self.width-150, self.height-50) #rectangle hit size of enemy

        self.walk_ctr = 0
        self.dead_ctr = 0
        self.speed = 3

        self.health = 10
        self.totalHealth = 10

        self.isDead = False
        self.visible = True
    
    def draw (self,window):
        self.move()

        if (self.walk_ctr +1 >= 36):
            self.walk_ctr = 0
        if (self.dead_ctr +1 >= 45):
            self.visible = False

        if self.visible:
            if self.isDead:
                if self.speed > 0:
                    window.blit(self.dead_right[self.dead_ctr//3],(self.x,self.y))
                    self.dead_ctr +=1
                    self.walk_ctr = 0
                elif self.speed < 0:
                    window.blit(self.dead_left[self.dead_ctr//3],(self.x,self.y))
                    self.dead_ctr +=1
                    self.walk_ctr = 0
            else:
                if self.speed > 0:
                    window.blit(self.walkRight[self.walk_ctr//3],(self.x,self.y))
                    self.walk_ctr +=1
                    self.walk_ctr = 0
                elif self.speed < 0:
                    window.blit(self.walkLeft[self.walk_ctr//3],(self.x,self.y))
                    self.walk_ctr +=1
                    self.walk_ctr = 0

            pygame.draw.rect(window, (255,0,0), (self.hitSize[0],self.hitSize[1],self.hitSize[2],self.hitSize[3] - 150))
            pygame.draw.rect(window, (255,255,0), (self.hitSize[0],self.hitSize[1],self.hitSize[2] * (self.health/self.totalHealth),self.hitSize[3] - 150))

            if self.isDead:
                self.hitSize = (0,0,0,0)
            else:
                self.hitSize = (self.x+70, self.y+15, self.width-135, self.height-50) #rectangle hit size of enemy
    
    def move(self):
        if not(self.isDead):    
            if self.speed > 0: #move to right
                if self.x < self.path[1] + self.speed: #reaching right end path
                    self.x += self.speed
                else: #change direction to left
                    self.speed = self.speed * -1
                    self.x += self.speed
                    self.walk_ctr = 0
            else: #move to left
                if self.x > self.path[0] + self.speed: #reaching left end path
                    self.x += self.speed
                else: #change direction to right
                    self.speed = self.speed * -1
                    self.x += self.speed
                    self.walk_ctr = 0
    
    def hit(self):
        if self.health > 1:
            self.health -= 1
        else:
            self.health = 0
        print("hit!!!")


def windowUpdate():
    window.blit(bg, (0,0)) # draw background image from 0,0

    if play.health == 0:
        lose = arial2.render('YOU LOSE!', 1, (255,0,0), (0,0,0))
        window.blit(lose, (475,200))
    elif m_spawn.health == 0:
        win = arial2.render('YOU WIN!', 1, (0,255,0), (0,0,0))
        window.blit(win, (500,200))

    text = arial.render('Score : ' + str(score), 1, (255,255,255))
    window.blit(text, (900,50))
    
    play.draw(window)
    m_spawn.draw(window)
    
    for bullet in bullets:
        bullet.draw(window)

    pygame.display.update()


clock = pygame.time.Clock()

play = player(50,420,260,220) #instance of player class
m_spawn = enemy(350,420,260,220,800) #instance of enemy class
bullets = []
run = True
arial = pygame.font.SysFont('arial', 50, True, True)
arial2 = pygame.font.SysFont('arial', 50, True)

# Main Game Loop
while run:
    clock.tick(36) #frame rate

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    #add projectile
    for bullet in bullets:
        
        #projectile hitting enemy
        if bullet.x+16 >= m_spawn.hitSize[0] and bullet.x+16 <= m_spawn.hitSize[0] + m_spawn.hitSize[2]:
            if bullet.y+16 >= m_spawn.hitSize[1] and bullet.y+16 <= m_spawn.hitSize[1] + m_spawn.hitSize[3]:
                bullets.pop(bullets.index(bullet))
                score += 1
                m_spawn.hit()

                if m_spawn.health == 0:
                    m_spawn.isDead = True

        if bullet.x < WINDOW_SIZE and bullet.x > 0:
            bullet.x += bullet.speed
        else:
            bullets.pop(bullets.index(bullet))

    # enemy-to-player collision
    if play.hitSize[0]+50 >= m_spawn.hitSize[0] and play.hitSize[0]+50 <= m_spawn.hitSize[0] + m_spawn.hitSize[2]:
        if play.hitSize[1]+50 >= m_spawn.hitSize[1] and play.hitSize[1]+50 <= m_spawn.hitSize[1] + m_spawn.hitSize[3]:
            play.hit()

            if play.health == 0:
                play.isDead = True
                if play.x < m_spawn.x:
                    play.x -= 100
                elif play.x > m_spawn.x:
                    play.x += 100
            else:
                play.isHurt = True
                if play.x < m_spawn.x:
                    play.x -= 150
                elif play.x > m_spawn.x:
                    play.x += 150

    keys = pygame.key.get_pressed()

    if not(play.isDead):
        if not(play.isHurt):
            #LEFT AND RIGHT ANIMATION
            if (keys[pygame.K_d] and play.x < WINDOW_HEIGHT + 200):
                play.x += play.speed
                play.left = False
                play.right = True
                play.isStanding = False
                play.isWalking = True
                play.isCasting = False
            elif (keys[pygame.K_a] and play.x > play.speed):
                play.x -= play.speed
                play.left = True
                play.right = False
                play.isStanding = False
                play.isWalking = True
                play.isCasting = False
            else: #if the character is not moving
                play.isStanding = True
                play.isWalking = False
                play.isCasting = False
                play.walk_ctr = 0

            #CASTING SPELLS
            if(keys[pygame.K_j]):
                play.isCasting = True
                play.isStanding = False
                play.isWalking = False

                if play.left:
                    facing = -1
                else:
                    facing = 1

                if play.cast_ctr == 18 and len(bullets) < 5:
                    if play.left: 
                        bullets.append(projectile(round(play.x + play.width // 2) - 60, round(play.y + play.height // 2), facing))
                    else:
                        bullets.append(projectile(round(play.x + play.width // 2) + 25, round(play.y + play.height // 2), facing))
                        
        #CONDITIONAL FOR JUMPING
            if not(play.isJump):
                if (keys[pygame.K_w]):
                    play.isJump = True
                    play.walk_ctr = 0
                    play.speed *= 1.25
            else:
                if (play.jumpCount >= -10):
                    play.y -= (play.jumpCount *abs(play.jumpCount)) *.5
                    play.jumpCount -=1
                else:
                    play.speed = 8
                    play.jumpCount = 10 
                    play.isJump = False

    windowUpdate()

pygame.quit()
