'''20.12.03 too difficult to make a collided method on imageObject
   change the solution make the fitted Square on image 
   to use a rect.colliderect(other_rect)'''
# add a hp bar on rocket
import pygame, math, random

pygame.init()

#Initialize variables:
clock = pygame.time.Clock()
s_w = 800 #screen_width
s_h = 600 #screen_height
screen = pygame.display.set_mode((s_w,s_h)) # ==screen
scene = 0 #장면 page
scenario = [] #scenes list  scene_list is better?

green = 0,255,0
red = 255,0,0
blue = 0,0,255
yellow = 255,255,0
white = 255,255,255
black = 0,0,0


background = pygame.image.load('/Users/dnfld/Desktop/teamKimImg/background/4.png')
rocket = pygame.image.load('/Users/dnfld/Desktop/teamKimImg/rocket/r1.png')
laser = pygame.image.load('/Users/dnfld/Desktop/teamKimImg/laser/laser3.png')
monster_mini1 = pygame.image.load('/Users/dnfld/Desktop/teamKimImg/monster/monster8.png')
monster_Boss = pygame.image.load('/Users/dnfld/Desktop/teamKimImg/monster/monster.png')


        
class Obj:
    def __init__(self,color,x,y,width,height,speed,img,xchange,ychange,hp_check):
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x,y,width,height) #Rect(left,top, width, height)->Rect 사각형 만드는애
        self.color = color
        self.direction = 'N' # north N south S east E west
        self.speed = speed #square #2 구현
        self.img = img
        self.xchange = xchange
        self.ychange = ychange
        self.hp_check = hp_check #hp 존재 유무
        self.hp_rect = pygame.Rect(0,0,self.rect.width*2,10)
        self.out_check = True
    def move(self):
        if self.direction =='E':
            self.rect.x = self.rect.x+self.speed
            if self.rect.x>s_w+200: #1 11.30 level1구현 level2 width/4 
                self.out = False
        elif self.direction =='W':
            self.rect.x = self.rect.x-self.speed
            if self.rect.x<-200: 
                self.out = False
        elif self.direction =='N':
            self.rect.y = self.rect.y-self.speed
            if self.rect.y<-200:
                self.out = False
        elif self.direction =='S':
            self.rect.y = self.rect.y+self.speed
            if self.rect.y>s_h+200: 
                self.out = False
    
    def draw(self,screen):
        if self.hp_check:
            if self.hp_rect.width>0:
                self.hp_rect.x = self.rect.x-5
                self.hp_rect.y = self.rect.y+40
                pygame.draw.rect(screen,green,self.hp_rect)
                red_rect = pygame.Rect(self.hp_rect.x+self.hp_rect.width,self.hp_rect.y,20-self.hp_rect.width,10)
                pygame.draw.rect(screen,red,red_rect)
            #else: gameover 적용 가능
                
        pygame.draw.rect(screen,self.color,self.rect)
        screen.blit(self.img,(self.rect.x+self.xchange,self.rect.y+self.ychange))
        
    def collided(self, other_rect):
        #Return True if self collided with other_rect
        return self.rect.colliderect(other_rect)  #cross line같이 여러 상황에서 충돌 판별함수 제작 어려우니 있는 mathud사용
class Rocket(Obj):
    def move(self):
        if self.direction =='E':
            self.rect.x = self.rect.x+self.speed
            if self.rect.x>s_w: #1 11.30 level1구현 level2 width/4 
                self.rect.x =-self.width/4
        elif self.direction =='W':
            self.rect.x = self.rect.x-self.speed
            if self.rect.x<-50: 
                self.rect.x=s_w-self.width/4
        elif self.direction =='N':
            self.rect.y = self.rect.y-self.speed
            if self.rect.y<-self.height/4:
                self.rect.y =s_h
        elif self.direction =='S':
            self.rect.y = self.rect.y+self.speed
            if self.rect.y>s_h: 
                self.rect.y =-self.height/4



rocket = Rocket(white,10,10,10,20,5,rocket,-20,-10,True)
bullets = []
enemies = []
#Main Program loop
done = False
#Main Program loop
done = False
while not done:
    for event in pygame. event.get():
        if event.type == pygame.QUIT:
            done =True
        elif event.type ==pygame.KEYDOWN:
            print(event.key) #Print value of key press
            if event.key == 119:#w
                rocket.direction = 'N'
            elif event.key == 97: #A
                rocket.direction = 'W'
            elif event.key == 115: #S
                rocket.direction = 'S'
            elif event.key == 100: #D
                rocket.direction = 'E'
            elif event.key == 32: #spacebar
                # Fire a bullet
                spawnX =rocket.rect.x-10+rocket.rect.width/2
                spawnY = rocket.rect.y-10+rocket.rect.height/2
                bullet = Obj(white,spawnX,spawnY,7,10,10,laser,-2,-2,False)
                bullet.direction = 'N'
                bullets.append(bullet)
    #Updare game objects
    for b in bullets:
        b.move()
    for e in enemies:
        e.move()
    rocket.move()
    #spawn enemies on the top of the screen and tell them to move down
    if random.randint(1,30) == 15:  #15  doesn't matter
        x = random.randint(0,s_w-40)
        e = Obj(white,x,-40,35,20,3,monster_mini1,-20,-25,False)
        e.direction = 'S'
        enemies.append(e)
       
    #check for collisions
    for e in enemies:
        if rocket.collided(e):
            rocket.hp_rect.width -=5
            enemies.remove(e)
        for b in bullets:
            if b.out_check == False:
                bullets.remove(b)
                break
            elif e.out_check == False:
                enemies.remove(e)
                break
            elif b.collided(e.rect):
                enemies.remove(e)
                bullets.remove(b)
            
    '''for i in reversed(range(len(bullets))):
        for j in reversed(range(len(enemies))):
            if bullets[i].collided(enemies[j].rect):
                del enemies[j]
                del bullets[i]'''
    #All the drawing
    #fill surface배경
    screen.blit(background, (0,0))
    rocket.draw(screen)
    for b in bullets:
        b.draw(screen)
    for e in enemies:
        e.draw(screen)
    #Drawing goes here
    pygame.display.flip()
    clock.tick(30)#30 FPS
    
pygame.quit()
exit()
        