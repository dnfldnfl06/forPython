'''20.12.03 too difficult to make a collided method on imageObject
   change the solution make the fitted Square on image 
   to use a rect.colliderect(other_rect)'''
#basic structure refered https://www.youtube.com/watch?v=aHmtOrrLmxg&list=LL&index=1 
#12.07 add a hp bar on rocket // try to make a shotgun but failed  I think an easy way to solve it is just bigger square with bigger bullet image
#12.09 enemies shoot done, item done, It would be nice start animation: background move
#12.10 add a condition variable name change  /  boss
#12.11 pause,retry mathud when gameover & fixed scenario, var done 
import pygame, math, random

pygame.init()

#Initialize variables:
clock = pygame.time.Clock()
s_w = 800 #screen_width
s_h = 600 #screen_height
screen = pygame.display.set_mode((s_w,s_h)) # ==screen  pygame.FULLSCREEN
 
scenario = [[0,0,0,0,0,0],[0,3,5,0,0,0],
            [0,1,3,1,1,0],[0,1,0,0,0,0],
            [0,2,5,0,0,0],[0,1,0,0,0,2],
            [0,3,10,0,0,0],[0,1,0,4,0,0],#bosstype: 4 => boss1 X 2 + boss2 X 1
            [0,4,5,0,0,0],[0,3,0,0,0,0],
            [0,4,2,0,0,0],[0,3,0,0,0,0],
            [0,4,1,0,0,0],[0,3,0,0,0,0],
            [0,3,0,0,0,0]] #scenes list  scene_list is better?
#장면 page [background,mini_monster_type,minimonster_counts,boss_type,item,?]
monster_type = [0,1,2,3,4]
boss_type = [[0,3,150,100,-50,-50,30],[1,5,200,200,-100,-100,70],[3,7,200,200,-100,-100,100]]#boss type  [[boss_img,skill_counts,width,height,xchange,ychange,Hp]]
scene_counts = 0
change = False
green = 0,255,0
red = 255,0,0
blue = 0,0,255
yellow = 255,255,0
white = 255,255,255
black = 0,0,0

for i in range(0,14): # scenario background setting #좀 길게 늘이고 싶으면 배경 사진 추가하고 list range 조절
    scenario[i][0] = '/Users/dnfld/Desktop/teamKimImg/background/'+str(int((i+1)/2))+'.png'
scenario[14][0] = scenario[0][0]
for i in range(0,5): #images match monster types 
    monster_type[i] = '/Users/dnfld/Desktop/teamKimImg/monster/mini_monster'+str(i)+'.png'
for i in range(0,3):#boss type update
    boss_type[i] = '/Users/dnfld/Desktop/teamKimImg/boss/boss'+str(i)+'.png'

background = pygame.image.load(scenario[0][0])
rocket = pygame.image.load('/Users/dnfld/Desktop/teamKimImg/rocket/r1.png')
laser = pygame.image.load('/Users/dnfld/Desktop/teamKimImg/laser/lc6.png')
laser_e = pygame.image.load('/Users/dnfld/Desktop/teamKimImg/laser/laser5.png')
monster_mini = pygame.image.load(monster_type[0])
monster_Boss = pygame.image.load('/Users/dnfld/Desktop/teamKimImg/boss/boss0.png')
item1 = pygame.image.load('/Users/dnfld/Desktop/teamKimImg/monster/monster6.png')

        
class Obj:
    def __init__(self,color,x,y,width,height,speed,direction,img,xchange,ychange,hp):
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x,y,width,height) #Rect(left,top, width, height)->Rect 사각형 만드는애
        self.color = color
        self.direction = direction # north N south S east E west
        self.speed = speed #square #2 구현
        self.img = img
        self.xchange = xchange
        self.ychange = ychange
        self.hp = hp #hp 
        if hp:
            self.hp_rect = pygame.Rect(self.rect.x-self.rect.width/2,self.rect.y+self.rect.height+20,self.rect.width*2,self.height/4)
            self.tic = self.hp_rect.width/hp #single tic
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
       
        if self.hp: # hp_bar existence
                if self.hp_rect.width>0:
                    self.hp_rect.x = self.rect.x-self.rect.width/2
                    self.hp_rect.y = self.rect.y+self.rect.height+self.hp_rect.height*5
                    pygame.draw.rect(screen,green,self.hp_rect)
                    red_rect = pygame.Rect(self.hp_rect.x+self.hp_rect.width,self.hp_rect.y,self.rect.width*2-self.hp_rect.width,self.hp_rect.height)
                    pygame.draw.rect(screen,red,red_rect)
                
                #gameover 적용 가능
    def collided(self, other_rect):
        #Return True if self collided with other_rect
        return self.rect.colliderect(other_rect)  #cross line같이 여러 상황에서 충돌 판별함수 제작 어려우니 있는 mathud사용
    def damaged(self):
        self.hp_rect.width -= self.tic
    
class Rocket(Obj):
        
    def moveDirection(self,direction):
        global change #scene이 전역 변수기 때문에 가져와야 쓸수 있음
        global scene_counts
        if direction == 'E':
            self.rect.x = self.rect.x+self.speed
            if self.rect.x>s_w: #1 11.30 level1구현 level2 width/4 
                self.rect.x =-self.width/4
        if direction == 'W':
            self.rect.x = self.rect.x-self.speed
            if self.rect.x<-50: 
                self.rect.x=s_w-self.width/4
        if direction == 'N':
            self.rect.y = self.rect.y-self.speed
            if self.rect.y<-self.height/4 and len(enemies)==0:
                self.rect.y =s_h
                scene_counts+=1
                change=True #change check
            elif self.rect.y<-self.height/4:
                 self.rect.y =s_h
        if direction == 'S':
            self.rect.y = self.rect.y+self.speed
            if self.rect.y>s_h: 
                self.rect.y =-self.height/4
                  #gameover 적용 가능
class Enemy(Obj):
    global enemies
    def makingEnm(self,counts):    
        for i in range(0,counts):
             rand = random.randint(0,200)
             e = Enemy(white,rand*s_h/150,rand+self.height,self.width,self.height,self.speed,self.direction,monster_mini,-20,-25,False)
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

class Boss(Obj):
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
        
    def skill(self,skill_num):
        if skill_num ==0:
            self.rect.x = 400
            self.rect.y = 300 
       # elif skill_num ==1:
           
#구성요소        
bullets = []
enemies = []
bullets_enm = []
items = []
bosses = []
gun_type = 0  
rocket = Rocket(white,400,500,10,20,8,'S',rocket,-20,-10,5)

launch_order = False #boss launch
#Main Program loop
done = False
#Main Program loop
done = False
while not done:
    if scene_counts==13:
        done = True
    elif change:          #change check
        enemies = []
        bullets_enm = []
        e = Enemy(white,0,40,35,20,3,'W',monster_mini,-20,-25,False)
        e.makingEnm(scenario[scene_counts][2])
        background = pygame.image.load(scenario[scene_counts][0])
        monster_mini = pygame.image.load(monster_type[scenario[scene_counts][1]])
        if scene_counts == 4:
            item = Obj(black,100,200,100,100,1,'S',item1,50,50,False)
            items.append(item)
        if scene_counts ==5 :
            boss = Boss(black,400,200,100,100,3,'W',boss_type[1],0,0,True)
      
        change=False #convert to False again for don't make a infinite chage 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done =True
        elif event.type ==pygame.KEYDOWN:
            print(event.key) #Print value of key press
            if event.key == 32: #spacebar
                # Fire a bullet
                spawnX = rocket.rect.x+rocket.rect.width/2
                spawnY = rocket.rect.y+rocket.rect.height/2
                if gun_type == 0: #nomal gun
                    bullet = Obj(white,spawnX-4,spawnY,7,10,10,'N',laser,-2,-2,False)
                elif gun_type ==1:#more biiger one
                    bullet = Obj(black,spawnX-4,spawnY,20,20,10,'N',laser,-2,-2,False)
                bullets.append(bullet)
            elif event.key==27:
                done =True
            elif event.key == 104: #H
                rocket.rect.y+=100
                
    #Handle held down keys
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_w]:
        rocket.moveDirection('N')
    if pressed[pygame.K_a]:
        rocket.moveDirection('W')
    if pressed[pygame.K_s]:
        rocket.moveDirection('S')
    if pressed[pygame.K_d]:
        rocket.moveDirection('E')
    
    #Updare game objects
    
    for b in bullets:
        b.move()
    for e in enemies:
        e.move()
    for b_e in bullets_enm:
        b_e.move()
    
    if enemies and random.randint(1,20)==10:
            e = enemies[random.randint(0,len(enemies)-1)]
            spawnX = e.rect.x+e.rect.width/2
            spawnY = e.rect.y+e.rect.height/2
            bullet_enm = Obj(white,spawnX-10,spawnY-10,7,10,10,'S',laser_e,-2,-2,False)
            bullets_enm.append(bullet_enm)
    if bosses and random.randint(1,70) == 35:
        for boss in bosses:
            boss.skill(random.randint(1,3))
            if  launch_order:
                    spawnX = boss.rect.x+boss.rect.width/2
                    spawnY = boss.rect.y+boss.rect.height/2
                    bullet_enm = Obj(white,spawnX-10,spawnY-10,7,10,10,'S',laser_e,-2,-2,False)
                 
                
    #check for collisions
    for e in enemies:
        if rocket.collided(e):
            rocket.damaged()
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
            rocket.damaged()
            bullets_enm.remove(b_e)
        elif b_e.out_check == False:
                bullets_enm.remove(b_e)
    for item in items:
        if rocket.collided(item):
            bullets=[]
            items.remove(item)
            gun_type =1
        
    #All the drawing
    #fill surface배경
    sf = pygame.font.SysFont("Monospace",20)
    text = sf.render("move to next Sky",True,blue)
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
    if not enemies:screen.blit(text,(100,100))
    #Drawing goes here
    pygame.display.flip()
    
    
    if rocket.hp_rect.width<=0:
        
        ch = True
        while ch:
            screen.blit(background, (0,0))
            sf = pygame.font.SysFont("Monospace",20)
            text1 = sf.render("retry:Y\n stop:N",True,blue)
            screen.blit(text1,(400,200))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type ==pygame.KEYDOWN:
                    print(event.key) #Print value of key press
                    if event.key == 121: # Y
                        ch = False
                        rocket.hp_rect.width = 5*rocket.tic
                    elif event.key == 110: # N
                            ch =False
                            done = True
            
    clock.tick(35)#30 FPS

pygame.quit()
        