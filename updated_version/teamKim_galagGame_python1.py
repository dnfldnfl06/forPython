import pygame, math, random
#11.29 map 밖으로 나갔을 경우 반대쪽으로 나온다던지 하는 기능 만들어보기 #1
#11.29 dash 를 만들수 있을듯 #2
#11.29 sqaure위치가 가운데가 아니라 직관적이지 못하다#3
#11.29 set_mode에 flags Sequence depth 파악하기 #4
pygame.init()

#Initialize variables:
clock = pygame.time.Clock()
s_w = 850 #screen_width
s_h = 600 #screen_height
surface = pygame.display.set_mode((s_w,s_h)) # ==screen
green = 0,255,0
red = 255,0,0
blue = 0,0,255
yellow = 255,255,0
white = 255,255,255
black = 0,0,0
background = pygame.image.load('/Users/dnfld/Desktop/img.png')
aircraft = pygame.image.load('/Users/dnfld/Desktop/aircraft.png')
class Obj:
    def __init__(self,x,y,speed,img):
        self.img = img
        self.rect = img.get_rect()
        self.rect.center = (x,y)
        self.direction = 'w'
        self.speed = speed
    def draw(self):
        pygame.draw.rect(surface,self.rect)
    def move(self):
        if self.direction =='E':
            self.rect.center.x = self.rect.center.x+self.speed
            if self.rect.x>s_w: #1 구현 
                self.rect.x =-50
        elif self.direction =='W':
            self.rect.center.x = self.rect.center.x-self.speed
            if self.rect.x<-50: 
                self.rect.x =s_w
        elif self.direction =='N':
            self.rect.center.y = self.rect.center.y-self.speed
            if self.rect.y<-50:
                self.rect.y =s_h
        elif self.direction =='S':
            self.rect.y = self.rect.y+self.speed
            if self.rect.y>s_h: 
                self.rect.y =-50
        
class Square:
    def __init__(self,color,x,y,width,height,speed):
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x,y,width,height) #Rect(left,top, width, height)->Rect 사각형 만드는애
        self.color = color
        self.direction = 'W' # north N south S east E west
        self.speed = speed #square #2 구현
        
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
    
    def draw(self,surface):
        pygame.draw.rect(surface,self.color,self.rect)
        
    def collided(self, other_rect):
        #Return True if self collided with other_rect
        return self.rect.colliderect(other_rect)  #cross line같이 여러 상황에서 충돌 판별함수 제작 어려우니 있는 mathud사용
   
        
#Build a square 화면에 만들기
sq = Square(blue,200,200,50,50,5)
airplane = Obj(200,200,5,aircraft)
bullets = []
enemies = []
#Main Program loop
done = False

while not done:
    for event in pygame. event.get():
        if event.type == pygame.QUIT:
            done =True
        elif event.type ==pygame.KEYDOWN:
            print(event.key) #Print value of key press
            if event.key == 119:#w
                sq.direction = 'N'
            elif event.key == 97: #A
                sq.direction = 'W'
            elif event.key == 115: #S
                sq.direction = 'S'
            elif event.key == 100: #D
                sq.direction = 'E'
            elif event.key == 32: #spacebar
                # Fire a bullet
                spawnX =sq.rect.x-10+sq.rect.width/2
                spawnY = sq.rect.y-10+sq.rect.height/2
                bullet = Square(green,spawnX,spawnY,20,20,10)
                bullet.direction = sq.direction
                bullets.append(bullet)
    #Updare game objects
    for b in bullets:
        b.move()
    for e in enemies:
        e.move()
    sq.move()
    airplane.move()
    #spawn enemies on the top of the screen and tell them to move down
    if random.randint(1,30) == 15:  #15  doesn't matter
        x = random.randint(0,s_w-40)
        e = Square(red,x,-40,40,40,3)
        e.direction = 'S'
        enemies.append(e)
        
    #check for collisions
    for b in bullets:
        for e in enemies:
            if b.collided(e.rect):
                e.color = "white"#Testing
                enemies.remove(e)
                bullets.remove(b)
    '''for i in reversed(range(len(bullets))):
        for j in reversed(range(len(enemies))):
            if bullets[i].collided(enemies[j].rect):
                del enemies[j]
                del enemies[i]'''
    #All the drawing
    surface.fill(white)#fill surface배경
    surface.blit(background, (0,0))
    airplane.draw()
    #sq.draw(surface)
    for b in bullets:
        b.draw(surface)
    for e in enemies:
        e.draw(surface)
    #Drawing goes here
    pygame.display.flip()
    clock.tick(30)#30 FPS
    
pygame.quit()
exit()
