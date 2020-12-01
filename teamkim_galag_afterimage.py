import pygame, math, random

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
aircraft = pygame.image.load('/Users/dnfld/Desktop/rocket.png')

class Obj:
    def __init__(self,x,y,speed,img):
        #self.width = width
       # self.height = height
        self.x = x
        self.y =y
        self.speed = speed
        self.direction='W'
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
'''class plane(Obj):
    def __init__(self,x,y,width,height,speed,img):
        super().__init__(x,y,width,height,speed,img)
    def move(self):
        '''
#Main Program loop
done = False
apl = Obj(100,100,5,aircraft)
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            print(event.key) #print value of key press
            if event.key == 119:#w
                apl.direction = 'N'
            elif event.key == 97: #A
                apl.direction = 'W'
            elif event.key == 115: #S
                apl.direction = 'S'
            elif event.key == 100: #D
                apl.direction = 'E'
        apl.move()
        #All the drawing
        surface.fill(white)
        surface.blit(background,(0,0))
        apl.draw(surface)

        pygame.display.flip()
        clock.tick(30)#30 FPS
pygame.quit()
exit()

