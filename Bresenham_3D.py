import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

pygame.init()

screen_width = 900
screen_height = 600
#vc para el obser.
FOVY=60.0
ZNEAR=1.0
ZFAR=500.0
#Variables para definir la posicion del observador
#gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
EYE_X=5.0
EYE_Y=5.0
EYE_Z=5.0
CENTER_X=0
CENTER_Y=0
CENTER_Z=0
UP_X=0
UP_Y=1
UP_Z=0
#Variables para dibujar los ejes del sistema
X_MIN=-500
X_MAX=500
Y_MIN=-500
Y_MAX=500
Z_MIN=-500
Z_MAX=500

def bresenham_3d(inicio, fin):
    """ Se imprimen los vóxeles de una línea 3D entre dos puntos enteros.
        Las coordenadas de inicio y fin deben ser enteras
    """
    x, y, z = inicio
    x1, y1, z1 = fin

    dx, dy, dz = abs(x1 - x), abs(y1 - y), abs(z1 - z)
    sx = 1 if x1 > x else -1 if x1 < x else 0
    sy = 1 if y1 > y else -1 if y1 < y else 0
    sz = 1 if z1 > z else -1 if z1 < z else 0

    #puntos = [(x, y, z)]
    glBegin(GL_POINTS)
    glVertex3i(x, y, z)
    #glEnd()

    if dx >= dy and dx >= dz:
        ey, ez = 2 * dy - dx, 2 * dz - dx
        for _ in range(dx):
            x += sx
            if ey >= 0:
                y += sy
                ey -= 2 * dx
            if ez >= 0:
                z += sz
                ez -= 2 * dx
            ey += 2 * dy
            ez += 2 * dz
            #puntos.append((x, y, z))
            #glBegin(GL_POINTS)
            glVertex3i(x, y, z)
            #glEnd()

    elif dy >= dx and dy >= dz:
        ex, ez = 2 * dx - dy, 2 * dz - dy
        for _ in range(dy):
            y += sy
            if ex >= 0:
                x += sx
                ex -= 2 * dy
            if ez >= 0:
                z += sz
                ez -= 2 * dy
            ex += 2 * dx
            ez += 2 * dz
            #puntos.append((x, y, z))
            #glBegin(GL_POINTS)
            glVertex3i(x, y, z)
            #glEnd()            
    else:
        ex, ey = 2 * dx - dz, 2 * dy - dz
        for _ in range(dz):
            z += sz
            if ex >= 0:
                x += sx
                ex -= 2 * dz
            if ey >= 0:
                y += sy
                ey -= 2 * dz
            ex += 2 * dx
            ey += 2 * dy
            #puntos.append((x, y, z)
            #glBegin(GL_POINTS)
            glVertex3i(x, y, z)
            #glEnd()
    #return puntos
    glEnd()


def Axis():
    glShadeModel(GL_FLAT)
    #glLineWidth(3.0)
    glPointSize(3.0)
    #X axis in red
    glColor3f(1.0,0.0,0.0)
    """
    glBegin(GL_LINES)
    glVertex3f(X_MIN,0.0,0.0)
    glVertex3f(X_MAX,0.0,0.0)
    glEnd()
    """
    bresenham_3d([X_MIN, 0, 0],[X_MAX,0,0])
    #Y axis in green
    glColor3f(0.0,1.0,0.0)
    glBegin(GL_LINES)
    glVertex3f(0.0,Y_MIN,0.0)
    glVertex3f(0.0,Y_MAX,0.0)
    glEnd()
    #Z axis in blue
    glColor3f(0.0,0.0,1.0)
    glBegin(GL_LINES)
    glVertex3f(0.0,0.0,Z_MIN)
    glVertex3f(0.0,0.0,Z_MAX)
    glEnd()
    glLineWidth(1.0)

def Init():
    screen = pygame.display.set_mode(
    (screen_width, screen_height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("OpenGL: ejes 3D")

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(FOVY, screen_width/screen_height, ZNEAR, ZFAR)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
    glClearColor(0,0,0,0)
    glEnable(GL_DEPTH_TEST)

    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

Init()
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    Axis()

    pygame.display.flip()
    pygame.time.wait(100)

pygame.quit()