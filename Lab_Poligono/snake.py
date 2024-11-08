import pygame
import graphics
import random
import copy

def texto(texto, posx, posy, color=(171,13,78), tam=40, bold=False):
    fuente = pygame.font.Font("DroidSans.ttf",tam)

    salida = pygame.font.Font.render(fuente,texto,1, color,)
    salida_rect=salida.get_rect()
    salida_rect.centerx = posx
    salida_rect.centery = posy
    return salida, salida_rect

class player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        
        self.puntos = 0
        self.fac_mov = 300        
        self.player_pos = pygame.Vector2(x, y)
        self.image = graphics.load_image("perrito1.gif")#
        #graphics.load_image("images/mini_atackP.gif")
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.type = "Player"
        


class food(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        
        self.puntos = 10        
        self.food_pos = pygame.Vector2(x, y)
        self.image = graphics.load_image("pierna.gif")
        #graphics.load_image("images/mini_atackP.gif")
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.type = "food"
        

class trap(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        
        self.puntos_neg = 15        
        self.pos = pygame.Vector2(x, y)
        self.image = graphics.load_image("pataMala.gif")
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.type = "trap"

class wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        
        self.pos = pygame.Vector2(x, y)
        self.image = graphics.load_image("muro.gif")
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.type = "wall"


width = 1280 
lenght = 720
pygame.init()
screen = pygame.display.set_mode((width, lenght))
back = graphics.load_image("fondo_jardin.jpg")
#pygame.mixer.music.load('/home/beto/Música/battle-neo-team-plasma-extended-hd.mp3')
pygame.mixer.music.load('/home/beto/Música/Vampire Killer.mp3')
pygame.mixer.music.play(-1)
clock = pygame.time.Clock()
running = True
limTmp = 30
dt = 0
trap_time = 0
food_time = 0
snake = player(screen.get_width() / 2, screen.get_height() / 2)
player_pos = pygame.Vector2()
all_sprites = pygame.sprite.Group()
all_sprites.add(snake)

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,200,0)

appear = False
exist_trap = False

n_paredes = 5
paredes = []

for n in range(n_paredes):
    posx_pared = random.randint(0, width)
    posy_pared = random.randint(0, lenght)
    p = wall(posx_pared, posy_pared)          
    all_sprites.add(p)

pause=True
timer = 3
radio_trampa=int(width/6)


while pause:
    screen.blit(back, (0,0))
    t_start, t_start_rect = texto("Comenzando en:  "+str(int(timer)), width/8*3, lenght/8*4, color=black, tam=80)
    screen.blit(t_start, t_start_rect)

    #teclas = pygame.key.get_pressed()
    if timer<=0:
        pause= False
    timer-= clock.tick(60)/1000
    pygame.display.flip() 


while running and not pause:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window


    fac_mov = 300 * dt
  


    if limTmp<=0:
        limTmp=0
        #print("Si entra al if...")        
        fac_mov = 0        

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    appear_trap = random.random()
    if appear_trap>=0.975 and not exist_trap:

        posx_trap = random.randint(posx_food-radio_trampa, posx_food+radio_trampa)
        posy_trap = random.randint(posy_food-radio_trampa, posy_food+radio_trampa)
        t = trap(posx_trap, posy_trap)          
        all_sprites.add(t)
        exist_trap = True
        trap_time = copy.copy(limTmp)

    if not appear:
        appear = True
        
        posx_food = random.randint(0, width)
        posy_food = random.randint(0, lenght)
        c = food(posx_food, posy_food) 
        food_time = copy.copy(limTmp)       
        all_sprites.add(c)

    if appear and limTmp<=(food_time-5):
        c.kill()                
        appear = False

    if exist_trap and limTmp<=(trap_time-3):
        t.kill()        
        exist_trap = False

    # fill the screen with a color to wipe away anything from last frame
    screen.blit(back, (0,0))



    #pygame.draw.circle(screen, "white", food_pos, 40)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        snake.rect.centery -= fac_mov
        if snake.rect.centery <=0:
            snake.rect.centery = lenght
    if keys[pygame.K_DOWN]:
        snake.rect.centery += fac_mov
        if snake.rect.centery >=lenght:
            snake.rect.centery = 0

    if keys[pygame.K_LEFT]:
        snake.image = graphics.load_image("perrito2.gif")
        snake.rect.centerx -= fac_mov
        if snake.rect.centerx <=0:
            snake.rect.centerx = width

    if keys[pygame.K_RIGHT]:
        snake.image = graphics.load_image("perrito1.gif")
        snake.rect.centerx += fac_mov
        if snake.rect.centerx >= width:
            snake.rect.centerx = 0

    wallR = False
    wallL = False
    wallT = False
    wallB = False
    hits = pygame.sprite.spritecollide(snake, all_sprites, False)
    for h in hits:
        if h.type == "food":
            snake.puntos+=h.puntos
            h.kill()
            try:
                t.kill()
            except:
                print("t aun no existe")
            exist_trap = False
            appear = False
        if h.type =="trap":
            snake.puntos-=h.puntos_neg
            h.kill()
            exist_trap = False
        if h.type == "wall":
            if h.rect.centerx>snake.rect.centerx:
                wallR = True
            if h.rect.centerx<=snake.rect.centerx:
                wallL = True

            if h.rect.centery<=snake.rect.centery:
                wallT = True

            if h.rect.centery>snake.rect.centery:
                wallB = True
            #Leve rebote con la pared

            if wallL:
                snake.rect.centerx+=8
                
            if wallR:
                snake.rect.centerx-=8
            
            if wallT:       
                snake.rect.centery+=8

            if wallB:       
                snake.rect.centery-=8


    # flip() the display to put your work on screen
    
    dt = clock.tick(60) / 1000
    limTmp-= dt

    all_sprites.draw(screen)
    

    t_jug, t_jug_rect = texto("Tiempo  "+str(int(limTmp)), width/9*2,40, color=white)
    screen.blit(t_jug, t_jug_rect)
    puntos, puntos_rect = texto("Puntos  "+str(int(snake.puntos)), width/9*4,40, color=white)
    screen.blit(puntos, puntos_rect)


    if limTmp<=0:
        limTmp=0
        #print("Si entra al if...")
        t_end, t_end_rect = texto("LA PARTIDA HA TERMINADO", width/8*4, lenght/8*4, color=black, tam=80)
        screen.blit(t_end, t_end_rect)
        fac_mov = 0
        if keys[pygame.K_INSERT] or keys[pygame.K_a]:
            running = False

    
    pygame.display.flip()   
    #clock.tick(60)  # limits FPS to 60

pygame.quit()