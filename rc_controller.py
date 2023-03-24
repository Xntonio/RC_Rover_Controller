import rospy
from std_msgs.msg import Int16MultiArray
from mavros_msgs.msg import OverrideRCIn
import pygame
import subprocess

pygame.init()

screen = pygame.display.set_mode((350, 300))
pygame.display.set_caption("RC Override Controller")

fuente  = pygame.font.Font(None, 25)
fuente2 = pygame.font.Font(None, 20)

text_1 = "Manual" 
manual_txt = fuente.render(text_1, 1, (255, 255, 255))

text_2 = "Armed" 
armed_txt = fuente.render(text_2, 1, (255, 255, 255))

text_3 = "Stop" 
break_txt = fuente.render(text_3, 1, (255, 255, 255))

text_4 = "Warning, the vehicle is disarmed!" 
warning_txt = fuente2.render(text_4, 1, (255, 255, 0))

text_5 = "Use the arrows " 
advice_txt = fuente.render(text_5, 1, (200, 200, 200))
text_6 = "to drive the vehicule" 
advice2_txt = fuente.render(text_6, 1, (200, 200, 200))
text_7 = "P -> Armar  \n\nQ -> Desarmar\n\nA -> Automatic \n\nM -> Manual \n\nK -> Stop" 
advice3_txt = fuente.render(text_7, 1, (200, 200, 200))

lines = text_7.splitlines()

BG_IMAGE_SIZE = (350,300)
DEFAULT_IMAGE_SIZE = (160, 160)
SMALL_IMAGE_SIZE = (70,50)

img_up     = pygame.image.load("pygame_files/v_up.png")
img_down   = pygame.image.load("pygame_files/v_down.png")
img_left   = pygame.image.load("pygame_files/v_left.png")
img_right  = pygame.image.load("pygame_files/v_right.png")
img_on     = pygame.image.load("pygame_files/arm.png")
img_off    = pygame.image.load("pygame_files/disarm.png")
img_bg     = pygame.image.load("pygame_files/v_ui.png")

img_up     = pygame.transform.scale(img_up,    DEFAULT_IMAGE_SIZE)
img_down   = pygame.transform.scale(img_down,  DEFAULT_IMAGE_SIZE)
img_left   = pygame.transform.scale(img_left,  DEFAULT_IMAGE_SIZE)
img_right  = pygame.transform.scale(img_right, DEFAULT_IMAGE_SIZE)
img_on     = pygame.transform.scale(img_on,    SMALL_IMAGE_SIZE)
img_off    = pygame.transform.scale(img_off,   SMALL_IMAGE_SIZE)
img_bg     = pygame.transform.scale(img_bg,    BG_IMAGE_SIZE)

button_rect = img_on.get_rect()
button_rect.center = (15,25)

button_rect2 = img_on.get_rect()
button_rect2.center = (15,115)

button_rect3 = img_on.get_rect()
button_rect3.center = (15,205)

# Inicializar nodo ROS
rospy.init_node('rc_override')

# Publicador para el topico rc/override
pub = rospy.Publisher('/mavros/rc/override', OverrideRCIn, queue_size=10)

# Definir valores de comando
CMD_THROTTLE = 1500
CMD_ROLL     = 1500
CMD_PITCH    = 1500
CMD_YAW      = 1500
CMD_AUX1     = 1500
CMD_AUX2     = 1000
CMD_AUX3     = 1500
CMD_AUX4     = 1500

VEL_LINEAR  = 20
VEL_ANGULAR = 30

running = True
armed   = False
manual  = True
breik   = False

def init():
    cmd = OverrideRCIn()
    cmd.channels = [1500, 1500, 1200, 2000, 1000, 1000, 1000, 5000]
    cmd.channels = [1500, 1500, 1500, 2000, 1000, 1000, 1000, 5000]
    pub.publish(cmd)
    pygame.time.wait(1000)
    cmd.channels = [1500, 1500, 1200, 2000, 1000, 2000, 1000, 5000]
    pub.publish(cmd)


# Funcion para enviar comando al topico rc/override
def send_command():
    cmd = OverrideRCIn()
    cmd.channels = [CMD_THROTTLE, CMD_PITCH, CMD_YAW, CMD_ROLL, CMD_AUX1, CMD_AUX2, CMD_AUX3, CMD_AUX4]
    pub.publish(cmd)

def draw_icons():

    screen.fill((100,100,100))
    screen.blit(img_bg,(0,0))
    screen.blit(armed_txt, (20, 10))
    screen.blit(manual_txt, (20, 100))
    screen.blit(break_txt, (26, 190))

    if CMD_THROTTLE >= 1550:
        screen.blit(img_up, (140, 10))
    if CMD_THROTTLE <= 1490:
        screen.blit(img_down, (140, 10))
    if CMD_YAW <= 1419:
        screen.blit(img_left, (110, 150))
    if CMD_YAW >= 1550:
        screen.blit(img_right, (170, 150))
    if armed:
        screen.blit(img_on, (15, 25))
        screen.blit(vel_txt, (130, 25))

    if armed != True:
        screen.blit(img_off, (15, 25))
        screen.blit(warning_txt, (118, 40))
        screen.blit(advice_txt,(160,90))
        screen.blit(advice2_txt,(140,110))
        x = 160
        y = 145
        for line in lines:
            text_surface = fuente.render(line, True, (220,220,220))
            screen.blit(text_surface, (x, y))
            y += fuente2.get_height()

    if manual:
        screen.blit(img_on, (15, 115))
    if manual != True:
        screen.blit(img_off, (15, 115))
    if breik:
        screen.blit(img_on, (15, 205))
    if breik != True:
        screen.blit(img_off, (15, 205))

    pygame.display.update()   


init()

# Bucle principal del juego
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            rospy.signal_shutdown("Quit")

    # Obtener el estado del teclado
    keys = pygame.key.get_pressed()

    # Actualizar comandos en funcion del estado del teclado
    if keys[pygame.K_q] and armed:
        CMD_AUX2 = 1000
        armed = False

    if keys[pygame.K_p] and armed!=True:
        CMD_AUX2 = 2000
        armed = True

    if keys[pygame.K_UP]:
        CMD_THROTTLE += VEL_LINEAR
        pygame.time.wait(100)        
    elif keys[pygame.K_DOWN]:
        CMD_THROTTLE -= VEL_LINEAR
        pygame.time.wait(100)
    else:
        if manual!=True:
            pass
        else:
            CMD_THROTTLE = 1500

    if keys[pygame.K_LEFT]:
        CMD_YAW -= VEL_ANGULAR
        pygame.time.wait(100)        
    elif keys[pygame.K_RIGHT]:
        CMD_YAW += VEL_ANGULAR
        pygame.time.wait(100)        
    else:
        if manual!=True:
            pass
        else:
            CMD_YAW = 1420

    if keys[pygame.K_k]:
        CMD_THROTTLE = 1500
        CMD_ROLL     = 1500
        CMD_PITCH    = 1500
        CMD_YAW      = 1500

    if keys[pygame.K_m]:
        manual = True

    if keys[pygame.K_a]:
        manual = False

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            print("escape pressed")
            running = False

    #Buttons on screen
    if event.type == pygame.MOUSEBUTTONDOWN and button_rect.collidepoint(event.pos):
        if armed:
            CMD_AUX2 = 1000
            armed = False
        else:
            CMD_AUX2 = 2000
            armed = True
        pygame.time.wait(300)


    if event.type == pygame.MOUSEBUTTONDOWN and button_rect2.collidepoint(event.pos):
        if manual:
            manual = False
        else:
            manual = True
        pygame.time.wait(300)


    if event.type == pygame.MOUSEBUTTONDOWN and button_rect3.collidepoint(event.pos):
        if breik:
            CMD_AUX2     = 1000
            CMD_THROTTLE = 1500
            CMD_ROLL     = 1500
            CMD_PITCH    = 1500
            CMD_YAW      = 1500
            armed  = False
            breik  = False
            manual = True
        else:
            breik = True
        

    vel_txt = fuente.render(str(CMD_THROTTLE) + "                      " +  str(CMD_YAW), 1, (255, 255, 255))

    draw_icons()

    # Actualizar los valores de los canales adicionales
    CMD_AUX1 = 1500
    CMD_AUX3 = 1500
    CMD_AUX4 = 1500

    TOP_LINEAR  = 1660
    LOW_LINEAR  = 1200

    if CMD_THROTTLE >= TOP_LINEAR:
        CMD_THROTTLE = TOP_LINEAR
    if CMD_THROTTLE <= LOW_LINEAR:
        CMD_THROTTLE = LOW_LINEAR

    TOP_ANGULAR  = 1750
    LOW_ANGULAR  = 1200

    if CMD_YAW >= TOP_ANGULAR:
        CMD_YAW = TOP_ANGULAR
    if CMD_YAW <= LOW_ANGULAR:
        CMD_YAW = LOW_ANGULAR

    print("CMD_THROTTLE:",CMD_THROTTLE)
    print("CMD_YAW:", CMD_YAW)
    print(" ")

    # Enviar comando al topico rc/override
    send_command()


