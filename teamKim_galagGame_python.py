import pygame
#11.29 map 밖으로 나갔을 경우 반대쪽으로 나온다던지 하는 기능 만들어보기 #1
#11.29 dash 를 만들수 있을듯 #2
#11.29 sqaure위치가 가운데가 아니라 직관적이지 못하다#3
pygame.init()

#Initialize variables:
clock = pygame.time.Clock()
surface = pygame.display.set_mode((800,600)) # ==screen
green = 0,255,0
red = 255,0,0
blue = 0,0,255
yellow = 255,255,0
white = 255,255,255
black = 0,0,0

class Square:
    def __init__(self,color,x,y,width,height,speed):
        self.rect = pygame.Rect(x,y,width,height) #Rect(left,top, width, height)->Rect 사각형 만드는애
        self.color = color
        self.direction = 'W' # north N south S east E west
        self.speed = speed #square #2 구현
        
    def move(self):
        if self.direction =='E':
            self.rect.x = self.rect.x+self.speed
            if self.rect.x>800: #1 구현 very lower level
                self.rect.x =-100
        elif self.direction =='W':
            self.rect.x = self.rect.x-self.speed
            if self.rect.x<-50: 
                self.rect.x =800
        elif self.direction =='N':
            self.rect.y = self.rect.y-self.speed
            if self.rect.y<-50:
                self.rect.y =600
        elif self.direction =='S':
            self.rect.y = self.rect.y+self.speed
            if self.rect.y>550: 
                self.rect.y =-50
    
    def draw(self,surface):
        pygame.draw.rect(surface,self.color,self.rect)
        
#Build a square 화면에 만들기
sq = Square(blue,200,200,50,50,5)

bullets = []


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
    sq.move()
    for b in bullets:
        b.move()
    #All the drawing
    surface.fill(black) #fill surface with black 배경
    for b in bullets:
        b.draw(surface)
    #Drawing goes here
    sq.draw(surface)
    
    pygame.display.flip()
    clock.tick(30)#30 FPS
    
pygame.quit()
exit()
