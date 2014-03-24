import pygame, sys
from pygame.locals import *

pygame.init()

WINWIDTH  = 800
WINHEIGHT = 500
FPS = 30 # frames per sec
fpsClock = pygame.time.Clock()
Jump      = False
SPEED = 9
ground = WINHEIGHT-60
nuground = False
ceiling = -20
#gravity = 0.2


class Platform:
    def __init__ (self, pos, img):
        self.pos = pos
        self.img = pygame.image.load(img).convert()
        self.rect = self.img.get_rect()
        self.left = pos[0] + self.rect.left
        self.right = pos[0] + self.rect.right
        self.top = pos[1] + self.rect.top
        self.bottom = pos[1] + self.rect.bottom

class Box:
    def __init__ (self, pos, img, text, ticks):
        self.pos = pos
        self.img = pygame.image.load(img).convert()
        self.rect = self.img.get_rect()
        self.text = text
        self.left = pos[0] + self.rect.left
        self.right = pos[0] + self.rect.right
        self.top = pos[1] + self.rect.top
        self.bottom = pos[1] + self.rect.bottom
        self.ticks = ticks
        self.number = len(text)
        

    def tick():
        self.tick +=1
        
        
    
class Avatar:
    def __init__(self, pos, img, vel, gravity, speed):
        self.pos = pos
        self.image = pygame.image.load(img).convert()
        self.vel = vel
        self.rect = self.image.get_rect()
        self.gravity = gravity
        
    def update(self):
        global ground, nuground, ceiling
        self.pos[0] = clip(0, self.pos[0], 0, WINWIDTH-60)
        nuground = False
                
        for pf in platforms:
            if self.rect.centerx+self.pos[0] in range(pf.left, pf.right):
                if (self.pos[1]+self.rect.bottom)<= pf.top:# and self.vel[1] >=0 :
                    ground = pf.pos[1]-self.rect.bottom
                    nuground = True

        if nuground == False:
            ground = WINHEIGHT - 60
        
        for box in boxes:
            if self.rect.centerx+self.pos[0] in range(box.left, box.right):
                if self.pos[1] - self.rect.top >= box.bottom:
                    #print('self.vel', self.vel)
                    ceiling = box.bottom
                    #collision(self, box)
            else: ceiling = -20
            #print ('boxtixk', box.ticks)

        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.vel[1] += self.gravity
        self.rect.move(self.vel)
        
        
        self.pos[1] = clip(box, self.pos[1], ceiling, ground)
        self.vel[1] = clip(box, self.vel[1], -20,20)


def clip(box, pos, minpos, maxpos):
    global blob
    if min(max(pos, minpos), maxpos) == ceiling:
        blob.vel[1] = 0.1
        box.ticks += 1
        print (box.ticks) 
        
    return min(max(pos, minpos), maxpos)
    
'''
def collision(avatar, boxie):
    boxie.ticks += 1
    avatar.vel[1] = 0
        '''
def main():
    global blob, platforms, ground, boxes, ceiling, nuground, SPEED
    DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT),0,32)
    pygame.display.set_caption('Blobjump')
    bgImg = pygame.image.load('bg.jpg').convert()
    box_uni = Box((100,300), 'box.bmp', ['text 1', 'text2'], 0)

    WHITE = (255,255,255)
    
    #print (avImg.topleft)
    blob = Avatar([40, WINHEIGHT-60], 'av.gif', [0,0], 1, SPEED)
    #blob = Avatar([0,0], 'av.gif', [0,0], 1, SPEED)
    
    while True:
        key=pygame.key.get_pressed()  #checking pressed keys
        if key[pygame.K_RIGHT] or key[pygame.K_d]:
            #print ('key right')
            blob.vel[0] = SPEED
        elif key[pygame.K_LEFT] or key[pygame.K_a]:
            blob.vel[0] = -SPEED
        else:
            blob.vel[0] = 0
        if key[pygame.K_UP] and (blob.vel[1] >0) and blob.pos[1] == ground:
                print (blob.pos[1] + ground)
                blob.vel[1] = -20
        '''
        if (key[pygame.K_UP] or key[pygame.K_w]):
            blob.vel[1] = -20
        else:
            blob.vel[1] = 0
            
        if key[pygame.K_LEFT] or key[pygame.K_a]:
            blob.move('left')
        else:
            blob.move('stop')
            '''
        #if (key[pygame.K_UP] or key[pygame.K_w]):
         #   blob.move('jump')
                
            
        for event in pygame.event.get(): #event handling loop
            if event.type == QUIT:
                terminate()
                '''
            elif event.type == KEYDOWN:
             #   if (event.key == K_RIGHT or event.key == K_d):
              #      blob.vel[0] += SPEED
                if (event.key == K_LEFT or event.key == K_a):
                    blob.vel[0] -= SPEED
                if (event.key == K_UP or event.key == K_w) and blob.pos[1] == ground:
                    blob.vel[1] = -20
                    #print ("grav  "+str(blob.gravity))
            elif event.type == KEYUP:
                if (event.key == K_RIGHT or event.key == K_d):
                    blob.vel[0] = 0
                if (event.key == K_LEFT or event.key == K_a):
                    blob.vel[0] = 0
                    '''


        pf1 = Platform([300,300],'platform.bmp')
        
        platforms = [pf1, box_uni]
        boxes = [box_uni]
    
        DISPLAYSURF.blit(bgImg, [0,0])
        DISPLAYSURF.blit(pf1.img, pf1.pos)
        DISPLAYSURF.blit(box_uni.img, box_uni.pos)
        DISPLAYSURF.blit(blob.image, blob.pos)
        myfont = pygame.font.SysFont("monospace", 15)
        label = myfont.render("Some text!", 1, (255,255,0))



        #collision detection
        for box in boxes:
            if box.ticks > 0:
                label = myfont.render(box.text[0], 1, (255,255,0))
                DISPLAYSURF.blit(label, (box.left-3, box.top - 30))
    
            #if blob.topcenter[0] in range(box.left, box.right) and blob.top == box.bottom:
             #   print ('collision!')
              #  collision(blob, box)
             
            
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

        #print ("self vel")
        #print(blob.vel)
        #print (blob.gravity)
        blob.update()
        pygame.display.update()
        fpsClock.tick(FPS)
        
#def move(thing, direction):

def terminate():
    pygame.quit()
    sys.exit()

main()
