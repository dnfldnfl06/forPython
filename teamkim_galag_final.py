'''20.12.03 too difficult to make a collided method on imageObject
   change the solution make the fitted Square on image 
   to use a rect.colliderect(other_rect)'''
#basic structure refered https://www.youtube.com/watch?v=aHmtOrrLmxg&list=LL&index=1 
#12.07 add a hp bar on rocket // try to make a shotgun but failed  I think an easy way to solve it is just bigger square with bigger bullet image
#12.09 enemies shoot done, item done, It would be nice start animation: background move
#12.10 add a condition variable name change  /  boss
#12.11 pause,retry mathud when gameover & fixed scenario, var done 
#12.13 item class
#12.14 all the other things.... 후우...
import pygame, math, random

pygame.init()

#Initialize variables:
clock = pygame.time.Clock()
s_w = 800 #screen_width
s_h = 600 #screen_height
screen = pygame.display.set_mode((s_w,s_h)) # ==screen  pygame.FULLSCREEN

scenario = [[0,0,0,0,0],[0,0,5,0,0],[0,0,3,1,4],
            [0,1,7,0,1],[0,1,10,0,2],[0,2,10,0,4],
            [0,2,30,0,5],[0,3,20,0,1],[0,3,5,2,3],
            [0,3,10,1,0],[0,4,10,2,2],[0,4,15,0,4],
            [0,3,15,3,3],[0,4,15,3,1]] 
#장면 page [background,mini_monster_type,mini_monster_counts,boss_type,item,?]
monster_type = [0,1,2,3,4]
boss_type = [[],#boss type  [[boss_img,skill_counts,width,height,xchange,ychange,Hp]]
             [0,5,100,200,-50,-50,20],
             [1,6,100,60,-50,-20,30],
             [2,7,100,60,-60,-50,50]]

item_type = [0,0,0,0,0,0]
rockets = [0,1,2]
boss_attack = [0,1,2,3,4,5,6,7]
laser = [0,1,2,3,4,5]
enm_laser = [0,1,2,3,4]
effect = [0,1,2,3,4]
scene_counts = 0
change = False
green = 0,255,0
red = 255,0,0
blue = 0,0,255
yellow = 255,255,0
white = 255,255,255
black = 0,0,0
directory = '/Users/dnfld/Desktop/teamKimImg/'
for i in range(0,14): 
    scenario[i][0] = pygame.image.load(directory+'background/'+str(i)+'.png')#str(int((i+1)/2)) 이걸로 이미지파일을 두번씩 사용하려고 했지만 그냥 배경이미지를 늘리는게 실행면에서는 유리할 것 이다 용량은 좀 늘어났다

for i in range(0,5): #images match monster types 
    monster_type[i]= pygame.image.load(directory+'/monster/'+str(i)+'.png')
    enm_laser[i]   = pygame.image.load(directory+'/enm_laser/'+str(i)+'.png')
    item_type[i+1] = pygame.image.load(directory+'/item/item'+str(i+1)+'.png')
    laser[i] = pygame.image.load(directory+'/laser/'+str(i)+'.png')
    boss_attack[i+1] = pygame.image.load(directory+'/boss_skill/'+str(i)+'.png')
    effect[i] = pygame.image.load(directory+'/effect/'+str(i)+'.png')
laser[5] = pygame.image.load(directory+'/laser/5.png')
boss_attack[6] = pygame.image.load(directory+'/boss_skill/5.png')
boss_attack[7] = pygame.image.load(directory+'/boss_skill/6.png')

for i in range(0,3):#boss type update
    boss_type[i+1][0] = pygame.image.load(directory+'/boss/'+str(i)+'.png')
    rockets[i] = pygame.image.load(directory+'/rocket/r'+str(i)+'.png')

background = scenario[0][0]
monster_mini = monster_type[0]

#information image
continue_image = pygame.image.load(directory+'/information/continue.png')
gameover_image = pygame.image.load(directory+'/information/game_over.png')
go_image = pygame.image.load(directory+'/information/go.png')
ending = pygame.image.load(directory+'/information/ending.png')
explosions = pygame.image.load(directory+'/effect/0.png')

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
       # pygame.draw.rect(screen,self.color,self.rect) //사각형 안그려주면 된다
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
        self.hp_rect.width -= self.tic# *damage
    
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
            if self.rect.y<-self.height/4 and not enemies and not boss:
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
class Enemy2(Enemy):
    def makingEnm(self,counts):    
        for i in range(0,counts):
             rand = random.randint(0,200)
             e = Enemy2(white,rand*s_h/150,rand+self.height,self.width,self.height,self.speed,self.direction,self.img,self.xchange,self.ychange,False)
             enemies.append(e)
    def move(self):
            if self.direction=='EN':
                self.rect.x=self.rect.x+self.speed
                self.rect.y=self.rect.y-self.speed
                if(self.rect.y<0):
                    self.direction='ES'
                elif(self.rect.x>s_w-self.width/2):
                        self.direction='WN'
            elif self.direction == 'ES':
                self.rect.x = self.rect.x+self.speed
                self.rect.y=self.rect.y+self.speed
                if(self.rect.x>s_w-self.width/2):
                    self.direction='WS'
                elif(self.rect.y>s_h-self.height/2):
                    self.direction='EN'
                
            elif self.direction == 'WS':
                    self.rect.x=self.rect.x-self.speed
                    self.rect.y = self.rect.y+self.speed
                    if(self.rect.y>s_h-self.height/2):
                        self.direction='WN'
                    elif(self.rect.x<0):
                        self.direction='ES'
                
            elif self.direction == 'WN':
                    self.rect.x=self.rect.x-self.speed
                    self.rect.y = self.rect.y-self.speed
                    if(self.rect.x<0):
                        self.direction='EN'
                    elif(self.rect.y<0):
                        self.direction='WS'

class Boss(Obj):
    def move(self):
        if self.direction =='E':
            self.rect.x = self.rect.x+self.speed
            if self.rect.x>s_w+200: 
                self.rect.x = 400
                self.rect.y = 100
                self.speed = 0
        elif self.direction =='W':
            self.rect.x = self.rect.x-self.speed
            if self.rect.x<-200: 
                self.rect.x = 400
                self.rect.y = 100
                self.speed = 0
            self.dirction = 'S'
        elif self.direction =='N':
            self.rect.y = self.rect.y-self.speed
            if self.rect.y<-200:
                self.rect.x = 400
                self.rect.y = 100
                self.speed = 0
        elif self.direction =='S':
            self.rect.y = self.rect.y+self.speed
            if self.rect.y>s_h+200: 
                self.rect.x = 400
                self.rect.y = 100
                self.speed = 0
    def draw(self,screen):
        #pygame.draw.rect(screen,self.color,self.rect) //사각형 안그려주면 된다
        screen.blit(self.img,(self.rect.x+self.xchange,self.rect.y+self.ychange))
       
        if self.hp: # hp_bar existence
                if self.hp_rect.width>0:
                    self.hp_rect.x = self.rect.x-self.rect.width/2
                    self.hp_rect.y = self.rect.y+self.rect.height/2+150
                    self.hp_rect.height = 20
                    pygame.draw.rect(screen,green,self.hp_rect)
                    red_rect = pygame.Rect(self.hp_rect.x+self.hp_rect.width,self.hp_rect.y,self.rect.width*2-self.hp_rect.width,self.hp_rect.height)
                    pygame.draw.rect(screen,red,red_rect)    
    
    
    def skill(self,num):
        global boss_ult_skill
        global damage_count
        self.speed = 3
        if   num==0:             #move to center
            self.rect.x = 400
            self.rect.y = 50 
            self.dirction = 'S'
            self.launch(1)
        elif num == 1:          #move to right center and moving to left
            self.rect.x = 700
            self.rect.y = 200 
            self.dirction = 'W'
            self.launch(1)
        elif num == 2:          #move to left  center
            self.rect.x = 100
            self.rect.y = 200 
            self.dirction = 'E'
        elif num == 3:
            self.rect.x = 400
            self.rect.y = 600
            self.direction='N'
        elif num == 4:
            self.speed+=1     #boss speed up
        elif num == 5:
            self.ult_skill()
            rocket.speed = 8
        elif num == 6:
            self.ult_skill2()
            rocket.speed=5
        elif num == 7:
            e = Enemy2(white,0,0,10,6,10,'ES',monster_type[3],-5,-3,False)
            e.makingEnm(5)
            rocket.speed=4
        
        damage_count=1
       # elif num == 6:
    def launch(self,count):
        for i in range(0,count):
             e = S_bullet(white,self.rect.centerx,self.rect.centery,50,50,-70,-50,3,boss_attack[scene[3]],rocket.rect.x,rocket.rect.y)
             bullets_boss.append(e)
    def ult_skill(self):
        e = Obj(white,random.randint(1,7)*100,-500,50,600,5+scene_counts,'S',boss_attack[scene[3]+3],-70,-100,False)
        bullets_boss.append(e)
    def ult_skill2(self):
        e = Obj(white,random.randint(1,7)*100,-500,50,50,5+scene_counts,'S',boss_attack[7],-70,-50,False)
        bullets_boss.append(e)   
class Item(Obj):
    def move(self):
            if self.direction=='EN':
                self.rect.x=self.rect.x+self.speed
                self.rect.y=self.rect.y-self.speed
                if(self.rect.y<0):
                    self.direction='ES'
                elif(self.rect.x>s_w-self.width/2):
                        self.direction='WN'
            elif self.direction == 'ES':
                self.rect.x = self.rect.x+self.speed
                self.rect.y=self.rect.y+self.speed
                if(self.rect.x>s_w-self.width/2):
                    self.direction='WS'
                elif(self.rect.y>s_h-self.height/2):
                    self.direction='EN'
                
            elif self.direction == 'WS':
                    self.rect.x=self.rect.x-self.speed
                    self.rect.y = self.rect.y+self.speed
                    if(self.rect.y>s_h-self.height/2):
                        self.direction='WN'
                    elif(self.rect.x<0):
                        self.direction='ES'
                
            elif self.direction == 'WN':
                    self.rect.x=self.rect.x-self.speed
                    self.rect.y = self.rect.y-self.speed
                    if(self.rect.x<0):
                        self.direction='EN'
                    elif(self.rect.y<0):
                        self.direction='WS'
    def item_type(self,type):
        global gun_type,bullet_speed,enemies
        if type == 1:
            rocket.hp_rect.width=10*rocket.tic
        elif type ==2:
            rocket.speed +=3
        elif type ==3:
            gun_type +=1
        elif type ==4:
            bullet_speed +=5
        elif type ==5:
            effect_spots.append(7)
            effect_spots.append((400,300))
            effect_spots.append(effect[4])
            enemies = []
class S_bullet: #Rocket Skill
    def __init__(self, color, x, y, width, height,xchange,ychange,speed,img,targetx,targety):
        self.rect = pygame.Rect(x,y,width,height)
        self.xchange = xchange
        self.ychange = ychange
        self.color = color
        self.speed = speed
        self.img = img
        angle = math.atan2(targety-y, targetx-x) #get angle to target in radians
        print('Angle in degrees:', int(angle*180/math.pi))
        self.dx = math.cos(angle)*speed
        self.dy = math.sin(angle)*speed
        self.x = x
        self.y = y
        self.out_check = True
    def draw(self,screen):
        screen.blit(self.img,(self.rect.x+self.xchange,self.rect.y+self.ychange))
    def move(self):
        #self.x and self.y are floats (decimals) so I get more accuracy
        #if I change self.x and y and then convert to an integer for
        #the rectangle.
        self.x = self.x + self.dx
        self.y = self.y + self.dy
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        if self.x<0 or self.x>s_w or self.y<0 or self.y>s_h:
            self.out_check = False

    def collided(self, other_rect):
        #Return True if self collided with other_rect
        return self.rect.colliderect(other_rect)
#구성요소       

class Effects:
    def __init__(self,img):
       self.img = img
       self.count = 5
    def draw(self,x,y):
        screen.blit(self.img, x,y)
        self.count -=1



rocket = Rocket(white,350,450,70,40,6,'S',rockets[0],-20,-10,10)
bullets = []
gun_type = 0  
bullet_speed =10
damage_count = 0 #보스한테 닿을때마다 damage입는게 아니라 보스가 스킬쓸때마다 count를 주고 count 있을때 damage줌
tries = 0

items = []

enemies = []
bullets_enm = []
boss = False
bullets_boss = []
boss_ult_skill=False
launch_order = 0 #boss launch

effect_spots = []

#Main Program loop
done = False

    #start part input w 
screen.blit(background, (0,0))
rocket.draw(screen)
sf = pygame.font.SysFont("Monospace",20)
text1 = sf.render("press 'W' 2 times to leave a rocket or ",True,blue)
text2 = sf.render("want to quit press'ESC' ",True,blue)
screen.blit(text1, (150,250))
screen.blit(text2, (150,300))
pygame.display.flip()
ct = 0
while ct<2:       
    for event in pygame.event.get():
        if event.type ==pygame.KEYDOWN:
            print(event.key) #Print value of key press
            if event.key == 119: # W
                ct+=1
            elif event.key==27:
                ct=3
                done = True
rocket.img = rockets[1]
while not done:
    if scene_counts==14:
        end =Obj(white,0,0,10,10,3,'N',ending,0,0,False)
        while end.rect.y>-1000:
            end.move()
            end.draw(screen)
            pygame.display.flip()
            clock.tick(35)
        done = True
        break
    elif change:          #change check
        print(scene_counts)
        bullets = []
        bullets_enm = []
        scene = scenario[scene_counts]
        background = scene[0]
        monster_mini = monster_type[scene[1]]
        if scene[1]==0:
            e = Enemy(white,0,0,20,20,3,'W',monster_mini,-10,-10,False)
        elif scene[1]==1:
            e = Enemy(white,0,0,25,15,6,'E',monster_mini,-12,-8,False)
        elif scene[1]==2:
            e = Enemy(white,0,0,30,20,7,'W',monster_mini,-15,-10,False)
        elif scene[1]==3:
            e = Enemy2(white,0,0,10,6,10,'ES',monster_mini,-5,-3,False)
        else:
            e = Enemy(white, 0, 0, 30, 20, 10, 'E', monster_mini, -15, -10, False)
        e.makingEnm(scene[2])
        item_num  = scene[4]
        if item_num:
            img = item_type[item_num]
            item = Item(black,100,200,100,100,3,'EN',img,50,50,False)
            items.append(item)
        boss_num = scene[3]
        if boss_num :
            bs_t = boss_type[boss_num]
            img = bs_t[0]
            if boss_num==1:
                boss = Boss(black,200,100,bs_t[2],bs_t[3],0,'S',img,bs_t[4],bs_t[5],bs_t[6])
            elif boss_num==2:
                boss = Boss(black,150,100,bs_t[2],bs_t[3],0,'S',img,bs_t[4],bs_t[5],bs_t[6])
            elif boss_num==3:
                boss = Boss(black,100,100,bs_t[2],bs_t[3],0,'S',img,bs_t[4],bs_t[5],bs_t[6])
            
        
        change=False #convert to False again for don't make a infinite chage 
    
    for event in pygame.event.get():
        spawnX = rocket.rect.centerx
        spawnY = rocket.rect.centery
        if event.type == pygame.QUIT:
            done =True
        elif event.type ==pygame.KEYDOWN:
            print(event.key) #Print value of key press
            if event.key == 32: #spacebar
                # Fire a bullet
                if gun_type == 0: #nomal gun
                    bullet = Obj(white,spawnX,spawnY,7,10,bullet_speed,'N',laser[2],-2,-2,False)
                elif gun_type ==1:#more biiger one
                    bullet = Obj(white,spawnX,spawnY,20,20,bullet_speed,'N',laser[3],-5,-5,False)
                elif gun_type ==2:#more biiger one
                    bullet = Obj(white,spawnX,spawnY,20,20,bullet_speed,'N',laser[4],-5,-5,False)
                    bullets.append(bullet)#*2배로 데미지
                bullets.append(bullet)
            elif event.key==27:
                done =True
            elif event.key == 104: #H
                rocket.rect.y+=100
        if event.type == pygame.MOUSEBUTTONDOWN:
            x,y = pygame.mouse.get_pos()
            if gun_type==0:
                b = S_bullet(black,spawnX,spawnY,20,20,-5,-5,bullet_speed,laser[0],x,y)
            elif gun_type==1:
                b = S_bullet(black,spawnX,spawnY,25,25,-8,-8,bullet_speed,laser[1],x,y)
            elif gun_type==2:
                b = S_bullet(black,spawnX,spawnY,30,30,-10,-10,bullet_speed,laser[5],x,y)
                bullets.append(b)
            bullets.append(b)
                
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
    if boss:boss.move()
    
    for b in bullets:
        b.move()
    for e in enemies:
        e.move()
    for b_e in bullets_enm:
        b_e.move()
    for i in items:
        i.move()
    for b_b in bullets_boss:
        b_b.move()
    if enemies and random.randint(1,35-scene_counts)==10:
            e = enemies[random.randint(0,len(enemies)-1)]
            spawnX = e.rect.centerx
            spawnY = e.rect.centery
            bullet_enm = Obj(white,spawnX,spawnY,7,10,10,'S',enm_laser[scene[1]],-2,-2,False)
            bullets_enm.append(bullet_enm)
    if boss and random.randint(1,40-3*scene[3]) == 2:#보스 스킬사용 확률결정
        boss.skill(random.randint(0,boss_type[scene[3]][1]))
                
                 
                
    #check for collisions
    for e in enemies:
        if rocket.collided(e):
                rocket.damaged()
                enemies.remove(e)
                break
        elif e.out_check == False:
                enemies.remove(e)
                break
                
        for b in bullets:
            if b.out_check == False:
                bullets.remove(b)
                break
                
            elif b.collided(e.rect):
                effect_spots.append(5)
                effect_spots.append((b.rect.x,b.rect.y))
                effect_spots.append(effect[0])
                enemies.remove(e)
                bullets.remove(b)
                break
    '''I tried to append enemies bullet at list enemies for forloop reuse but
        it could make enemies bullets making enemies bullets problem'''
    if boss:
        for b in bullets:
                if boss.collided(b):
                    boss.damaged()
                    bullets.remove(b)
                    effect_spots.append(5)
                    effect_spots.append((b.rect.x,b.rect.y))
                    effect_spots.append(effect[2])
                    break
    
    for b_e in bullets_enm:  
        if rocket.collided(b_e):
            rocket.damaged()
            bullets_enm.remove(b_e)
            effect_spots.append(5)
            effect_spots.append((b.rect.x,b.rect.y))
            effect_spots.append(effect[2])
        elif b_e.out_check == False:
            bullets_enm.remove(b_e)
    for item in items:
        if rocket.collided(item):
            bullets=[]
            item.item_type(scenario[scene_counts][4])
            items.remove(item)
    for boss_b in bullets_boss:
        if rocket.collided(boss_b):
            rocket.damaged()
            rocket.damaged()
            bullets_boss.remove(boss_b)
            break
    if boss:
        if rocket.collided(boss)and damage_count:
            damage_count=0
            rocket.damaged()
    
    #All the drawing
    #fill surface배경
    screen.blit(background, (0,0))
    rocket.draw(screen)
    if boss: boss.draw(screen)
    for item in items:
        item.draw(screen)
    for b in bullets:
        b.draw(screen)
    for e in enemies:
        e.draw(screen)
    for b_e in bullets_enm:
        b_e.draw(screen)
    for b_b in bullets_boss:
        b_b.draw(screen)
    for i in range(0,len(effect_spots),3):
        if effect_spots[i]:
            effect_spots[i]-=1
            screen.blit(effect_spots[i+2],effect_spots[i+1])
    for i in range(0,len(effect_spots),3):
        if not effect_spots[i]:
            del effect_spots[i]
            del effect_spots[i]
            del effect_spots[i]
            break
            
    
    if boss: 
        if boss.hp_rect.width<0:
            boss = False
            bullets_boss=[]
            enemies =[]
    if not enemies and not boss:
        rocket.speed = 8
        screen.blit(go_image,(100,100))
    text_try = sf.render("tried: "+str(tries)+" times",True,red)
    screen.blit(text_try, (700,10))
    #Drawing goes here
    pygame.display.flip()
    
    if rocket.hp_rect.width<=0:
        screen.blit(gameover_image,(200,100))
        screen.blit(continue_image,(200,300))
        pygame.display.flip()
        ch = True
        while ch:
            for event in pygame.event.get():
                if event.type ==pygame.KEYDOWN:
                    print(event.key) #Print value of key press
                    if event.key == 121: # Y
                        tries+=1
                        ch = False
                        rocket.hp_rect.width = 10*rocket.tic
                    elif event.key == 110: # N
                            ch =False
                            done = True
    
    clock.tick(35)#30 FPS

#while done:
    

pygame.quit()
        