'''20.12.03 too difficult to make a collided method on imageObject
   change the solution make the fitted Square on image 
   to use a rect.colliderect(other_rect)'''
# add a hp bar on rocket
#12.07 make gun_type but shotgun failure  I think an easy way to solve it is just bigger square with bigger bullet image
#12.09 It would be nice start animation: background move
import pygame, math, random

pygame.init()

#Initialize variables:
clock = pygame.time.Clock()
s_w = 800 #screen_width
s_h = 600 #screen_height
screen = pygame.display.set_mode((s_w,s_h)) # ==screen  pygame.FULLSCREEN
 
scenario = [[0,0,0,False,0],[0,3,5,False,0],
            [0,1,5,False,1],[0,1,5,False,0],
            [0,2,20,False,0],[0,1,5,False,0],
            [0,3,20,False,0],[0,1,5,False,0],
            [0,2,20,False,0],[0,3,5,False,0]] #scenes list  scene_list is better?
#장면 page [background,mini_monster_type,minimonster_counts,boss_existence,item]
scene_counts = 0

green = 0,255,0
red = 255,0,0
blue = 0,0,255
yellow = 255,255,0
white = 255,255,255
black = 0,0,0

for i in range(0,10): # scenario background setting #좀 길게 늘이고 싶으면 배경 사진 추가하고 list range 조절
    scenario[i][0] = '/Users/dnfld/Desktop/teamKimImg/background/'+str(int(i/2))+'.png'
monster_type = [0,1,2,3,4]
for i in range(0,5):
    monster_type[i] = '/Users/dnfld/Desktop/teamKimImg/monster/mini_monster'+str(i)+'.png'


background = pygame.image.load(scenario[0][0])
rocket0 = pygame.image.load('/Users/dnfld/Desktop/teamKimImg/rocket/r0.png')
rocket = pygame.image.load('/Users/dnfld/Desktop/teamKimImg/rocket/r1.png')
laser = pygame.image.load('/Users/dnfld/Desktop/teamKimImg/laser/laser3.png')
laser_e = pygame.image.load('/Users/dnfld/Desktop/teamKimImg/laser/laser5.png')
monster_mini = pygame.image.load(monster_type[0])
monster_Boss = pygame.image.load(monster_type[4])
item1 = pygame.image.load('/Users/dnfld/Desktop/teamKimImg/monster/monster6.png')

        
class Obj:
    def __init__(self,color,x,y,width,height,speed,direction,img,xchange,ychange,hp_check):
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x,y,width,height) #Rect(left,top, width, height)->Rect 사각형 만드는애
        self.color = color
        self.direction = direction # north N south S east E west
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
        pygame.draw.rect(screen,self.color,self.rect)
        screen.blit(self.img,(self.rect.x+self.xchange,self.rect.y+self.ychange))
       
        if self.hp_check: # hp_bar existence
            if self.hp_rect.width>0:
                self.hp_rect.x = self.rect.x-5
                self.hp_rect.y = self.rect.y+40
                pygame.draw.rect(screen,green,self.hp_rect)
                red_rect = pygame.Rect(self.hp_rect.x+self.hp_rect.width,self.hp_rect.y,20-self.hp_rect.width,10)
                pygame.draw.rect(screen,red,red_rect)
            #else: gameover 적용 가능
    def collided(self, other_rect):
        #Return True if self collided with other_rect
        return self.rect.colliderect(other_rect)  #cross line같이 여러 상황에서 충돌 판별함수 제작 어려우니 있는 mathud사용
        
    
class Rocket(Obj):
    
    def move(self):
        global scene_counts #scene이 전역 변수기 때문에 가져와야 쓸수 있음
        global background
        global monster_mini
        global enemies
        global bullets_enm
        global items
        if self.direction =='E':
            self.rect.x = self.rect.x+self.speed
            if self.rect.x>s_w: #1 11.30 level1구현 level2 width/4 
                self.rect.x =-self.width/4
        elif self.direction =='W':
            self.rect.x = self.rect.x-self.speed
            if self.rect.x<-50: 
                self.rect.x=s_w-self.width/4
        elif self.direction =='N':
            if self.speed==0:
                self.speed=5
            self.rect.y = self.rect.y-self.speed
            if self.rect.y<-self.height/4 and len(enemies)==0:
                self.rect.y =s_h
                scene_counts+=1
                enemies = []
                bullets_enm = []
                e = Enemy(white,0,40,35,20,3,'W',monster_mini,-20,-25,False)
                e.makingEnm(scenario[scene_counts][2])
                background = pygame.image.load(scenario[scene_counts][0])
                monster_mini = pygame.image.load(monster_type[scenario[scene_counts][1]])
                if scenario[scene_counts][4]==1:
                    item = Obj(black,100,200,100,100,1,'S',item1,50,50,False)
                    items.append(item)
            elif self.rect.y<-self.height/4:
                 self.rect.y =s_h
        elif self.direction =='S':
            self.rect.y = self.rect.y+self.speed
            if self.rect.y>s_h: 
                self.rect.y =-self.height/4
class Enemy(Obj):
    global enemies
    def makingEnm(self,counts):    
        for i in range(0,counts):
             rand = random.randint(0,200)
             e = Enemy(white,rand*s_h/100,rand+self.height,self.width,self.height,self.speed,self.direction,monster_mini,-20,-25,False)
             enemies.append(e)
    def move(self):
        if self.direction =='E':
            self.rect.x = self.rect.x+self.speed
            if self.rect.x>s_w: #1 11.30 level1구현 level2 width/4 
                self.direction = 'W'
        elif self.direction =='W':
            self.rect.x = self.rect.x-self.speed
            if self.rect.x<0: 
                self.direction = 'E'

rocket = Rocket(white,400,500,10,20,0,'S',rocket,-20,-10,True)
bullets = []
enemies = []
bullets_enm = []
items = []
gun_type = 0
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
            spawnX = rocket.rect.x+rocket.rect.width/2
            spawnY = rocket.rect.y+rocket.rect.height/2
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
                if gun_type == 0: #nomal gun
                    bullet1 = Obj(white,spawnX-10,spawnY-10,7,10,10,'N',laser,-2,-2,False)
                elif gun_type ==1:#more biiger one
                    bullet1 = Obj(black,spawnX-10,spawnY-10,20,20,10,'N',laser,-2,-2,False)
                bullets.append(bullet1)
            elif event.key==27:
                done =True
    #Updare game objects
    
    for b in bullets:
        b.move()
    for e in enemies:
        e.move()
    for b_e in bullets_enm:
        b_e.move()
    rocket.move()
    #spawn enemies on the top of the screen and tell them to move down
    if enemies and random.randint(1,20)==10:
            e = enemies[random.randint(0,len(enemies)-1)]
            spawnX = e.rect.x+rocket.rect.width/2
            spawnY = e.rect.y+rocket.rect.height/2
            bullet_enm = Obj(white,spawnX-10,spawnY-10,7,10,10,'S',laser_e,-2,-2,False)
            bullets_enm.append(bullet_enm)
            
        
    #check for collisions
    for e in enemies:
        if rocket.collided(e):
            rocket.hp_rect.width -=5
            enemies.remove(e)
        elif e.out_check == False:
                enemies.remove(e)
                
        for b in bullets:
            if b.out_check == False:
                bullets.remove(b)
                
            elif b.collided(e.rect):
                enemies.remove(e)
                bullets.remove(b)
    
    '''I tried to append enemies bullet at list enemies for forloop reuse but
        it could make enemies bullets making enemies bullets problem'''
    
    for b_e in bullets_enm:  
        if rocket.collided(b_e):
            rocket.hp_rect.width -=5
            bullets_enm.remove(b_e)
        elif b_e.out_check == False:
                bullets_enm.remove(b_e)
    for item in items:
        if rocket.collided(item):
            items.remove(item)
            gun_type =1
        
    #All the drawing
    #fill surface배경
    screen.blit(background, (0,0))
    rocket.draw(screen)
    for item in items:
        item.draw(screen)
    for b in bullets:
        b.draw(screen)
    for e in enemies:
        e.draw(screen)
    for b_e in bullets_enm:
        b_e.draw(screen)
    #Drawing goes here
    pygame.display.flip()
    clock.tick(30)#30 FPS
    
    
pygame.quit()
        