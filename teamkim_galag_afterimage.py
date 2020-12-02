#12.02 snap off occur #5 sesolved 12.02// blanc reset 

import pygame, math, random

pygame.init()

#Initialize variables:
clock = pygame.time.Clock()
s_w = 800 #screen_width
s_h = 600 #screen_height
screen = pygame.display.set_mode((s_w,s_h)) # ==screen
green = 0,255,0
red = 255,0,0
blue = 0,0,255
yellow = 255,255,0
white = 255,255,255
black = 0,0,0
background = pygame.image.load('/Users/dnfld/Desktop/teamKimImg/img.png')
rocket = pygame.image.load('/Users/dnfld/Desktop/teamKimImg/rocket.png')
laser = pygame.image.load('/Users/dnfld/Desktop/teamKimImg/laser.png')
monster_mini1 = pygame.image.load('/Users/dnfld/Desktop/teamKimImg/monster8.png')
monster_Boss = pygame.image.load('/Users/dnfld/Desktop/teamKimImg/monster1.png')
class Obj:
    def __init__(self,x,y,speed,img):
        self.x = x
        self.y =y
        self.speed = speed
        self.direction='N'
        self.img = img
    def draw(self,surface):
        surface.blit(self.img,(self.x,self.y))
    def move(self):
        if self.direction =='E':
            self.x = self.x+self.speed
        elif self.direction =='W':
            self.x = self.x-self.speed
        elif self.direction =='N':
            self.y = self.y-self.speed
        elif self.direction =='S':
            self.y = self.y+self.speed
    def collided(self,other_rect):
        #Return True if self collided with other_rect
        return self.rect.colliderect(other_rect) #cross line같이 여러 상황에서 충돌 판별함수 제작 어려우니 있는 mathud사용
class Rocket(Obj):
    hp = 5
    def __init__(self,x,y,speed,img,width,height):
        super().__init__(x,y,speed,img)
        self.width = width
        self.height = height
    def move(self):
        xchange = 0
        ychange = 0
        if self.direction =='E':
            xchange = self.speed
            if self.x>s_w:
                self.x = -self.width/4 #smooth movement when Obj come out the Screen
        elif self.direction =='W':
            xchange = -self.speed
            if self.x<-self.width/4:
                self.x=s_w-self.width/4
        elif self.direction =='N':
            ychange = -self.speed
            if self.y<-self.height/4:
                self.y = s_h-self.height/4
        elif self.direction =='S':
            ychange = +self.speed
            if self.y >s_h:
                self.y = -self.height/4
        self.x = self.x+xchange
        self.y = self.y+ychange
     #아 그냥 hp만 만들어 두고 true일때 rck.hp-=1하면 되겠네
class Enemy(Obj):
     def __init__(self,x,y,speed,img,width,height):
         super().__init__(x,y,speed,img)
         self.width =width
         self.direction = 'S'
     def making(self,e_count):
         while e_count>0:
             if random.randint(1,30) == 15:
                 self.x = random.randint(self.width,s_w-self.width)
                 e = Enemy(self.x,self.y,self.speed,self.img,20,20)
                 enemies.append(e)
                 e_count = e_count-1
#Main Program loop
done = False
#Build Objects
rck = Rocket(100,100,5,rocket,50,50)
enemy1 = Enemy(0,-40,3,monster_mini1,20,20) #mini Space ship
enemy2 = Enemy(0,0,0,monster_Boss,100,100) #Boss monster
bullets = [] #총알list
enemies = [] # 적생성
count = 0
while not done:
    #Get user input
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            print(event.key) #print value of key press
            if event.key == 119:#w
                rck.direction = 'N'
            elif event.key == 97: #A
                rck.direction = 'W'
            elif event.key == 115: #S
                rck.direction = 'S'
            elif event.key == 100: #D
                rck.direction = 'E'
            elif event.key == 32: #spacebar
            #Fire a bullet
                spawnX = rck.x+rck.width/2
                spawnY = rck.y+rck.height/2
                bullet = Obj(spawnX,spawnY,10,laser)# need a bullet image
                bullets.append(bullet)
                count = count+1
                enemy1.making(1) 
    if count>3:
        enemy2.making(1)
        count=0
#upload game objects
    for b in bullets:
        b.move()
    for e in enemies:
        e.move()
    rck.move()
    
    
    
    #All the drawing
    screen.fill(white)
    screen.blit(background,(0,0))
    for b in bullets:
        b.draw(screen)
    for e in enemies:
        e.draw(screen)

    rck.draw(screen)

    pygame.display.flip()
    clock.tick(30)#30 FPS
pygame.quit()
exit()

