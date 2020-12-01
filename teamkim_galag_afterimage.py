import pygame, math, random

pygame.init()

#Initialize variables:
clock = pygame.time.Clock()
s_w = 1000 #screen_width
s_h = 600 #screen_height
screen = pygame.display.set_mode((s_w,s_h)) # ==screen
green = 0,255,0
red = 255,0,0
blue = 0,0,255
yellow = 255,255,0
white = 255,255,255
black = 0,0,0
background = pygame.image.load('/Users/dnfld/Desktop/img.png')
rocket = pygame.image.load('/Users/dnfld/Desktop/rocket.png')

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
        if self.direction =='E':
            self.x = self.x+self.speed
            if self.x>s_w:
                self.x = -self.width/4 #smooth movement when Obj come out the Screen
        elif self.direction =='W':
            self.x = self.x-self.speed
            if self.x<-self.width/4:
                self.x=s_w-self.width/4
        elif self.direction =='N':
            self.y = self.y-self.speed
            if self.y<-self.height/4:
                self.y = s_h-self.height/4
        elif self.direction =='S':
            self.y = self.y+self.speed
            if self.y >s_h:
                self.y = -self.height/4
     #아 그냥 hp만 만들어 두고 true일때 rck.hp-=1하면 되겠네    
    '''def damaged(self,other_rect):             #2     1,2중에 뭐가 더 효율적일까..
        if(super().collided(other_rect)):
            hp-=1                                
        '''
#Main Program loop
done = False
screen.blit(background,(0,0))
#Build Objects
rck = Rocket(100,100,5,rocket,50,50)
bullets = []
while not done:
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
                bullet = Obj(spawnX,spawnY,10,rocket)# need a bullet image
                bullets.append(bullet)
        for b in bullets:
            b.move()
        rck.move()
    #All the drawing
        screen.fill(white)
        for b in bullets:
            b.draw(screen)

        rck.draw(screen)

        pygame.display.flip()
        clock.tick(30)#30 FPS
pygame.quit()
exit()

