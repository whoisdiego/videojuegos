import pygame
import math


screen_width = 900
screen_height = 600
#vc para el obser.
FOV_Y=60.0
ZNEAR=1.0
ZFAR=500.0
#Variables para definir la posicion del observador
#gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
CAMARA = (10.0, 10.0, 10.0)
OBJETIVO = (0.0, 0.0, 0.0)
ARRIBA = (0.0, 1.0, 0.0)
#Variables para dibujar los ejes del sistema
X_MIN=-500
X_MAX=500
Y_MIN=-500
Y_MAX=500
Z_MIN=-500
Z_MAX=500

# funciones basadas en operadores sobre vectores
def restar(a, b):
    return tuple(x - y for x, y in zip(a, b))


def producto_punto(a, b):
    return sum(x * y for x, y in zip(a, b))


def producto_cruz(a, b):
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )

def normalizar(v):
    magnitud = math.sqrt(producto_punto(v, v))
    return tuple(c / magnitud for c in v)

# Sistema de coordenadas de la cámara, equivalente en intención a gluLookAt.
frente = normalizar(restar(OBJETIVO, CAMARA))
derecha = normalizar(producto_cruz(frente, ARRIBA))
arriba_camara = producto_cruz(derecha, frente)

def proyectar(punto):
    """Transforma un punto 3D en un píxel (x, y) de la pantalla."""
    relativo = restar(punto, CAMARA)

    x_camara = producto_punto(relativo, derecha)
    y_camara = producto_punto(relativo, arriba_camara)
    profundidad = producto_punto(relativo, frente)

    if profundidad <= ZNEAR:
        return None  # El punto está detrás del plano cercano.

    focal = (screen_height / 2) / math.tan(math.radians(FOV_Y) / 2)

    x_pantalla = round(screen_width / 2 + focal * x_camara / profundidad)
    y_pantalla = round(screen_height / 2 - focal * y_camara / profundidad)

    return x_pantalla, y_pantalla

def bresenham_2d(inicio, fin):
    """Genera todos los píxeles entre dos posiciones de pantalla."""
    x, y = inicio
    x1, y1 = fin

    dx, dy = abs(x1 - x), abs(y1 - y)
    sx = 1 if x < x1 else -1
    sy = 1 if y < y1 else -1
    error = dx - dy

    while True:
        yield x, y

        if (x, y) == (x1, y1):
            break

        doble_error = 2 * error

        if doble_error > -dy:
            error -= dy
            x += sx

        if doble_error < dx:
            error += dx
            y += sy

def bresenham_3d(inicio, fin):
    """Genera los puntos enteros de una trayectoria discreta 3D."""
    x, y, z = inicio
    x1, y1, z1 = fin

    dx, dy, dz = abs(x1 - x), abs(y1 - y), abs(z1 - z)
    sx = (x1 > x) - (x1 < x)
    sy = (y1 > y) - (y1 < y)
    sz = (z1 > z) - (z1 < z)

    yield x, y, z

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
            yield x, y, z

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
            yield x, y, z

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
            yield x, y, z

def dibujar_segmento_2d(superficie, inicio, fin, color):
    for x, y in bresenham_2d(inicio, fin):
        if 0 <= x < screen_width and 0 <= y < screen_height:
            superficie.set_at((x, y), color)

def dibujar_bresenham_3d(superficie, inicio, fin, color):
    anterior = None

    for punto_3d in bresenham_3d(inicio, fin):
        actual = proyectar(punto_3d)

        if anterior is not None and actual is not None:
            dibujar_segmento_2d(superficie, anterior, actual, color)
        elif actual is not None:
            x, y = actual
            if 0 <= x < screen_width and 0 <= y < screen_height:
                superficie.set_at(actual, color)

        anterior = actual

pygame.init()
pantalla = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Bresenham 3D proyectado y rasterizado en 2D")

pantalla.fill((0, 0, 0))

# Ejes 3D de ejemplo.
dibujar_bresenham_3d(pantalla, (X_MIN, 0, 0), (X_MAX, 0, 0), (255, 0, 0))
dibujar_bresenham_3d(pantalla, (0, Y_MIN, 0), (0, Y_MAX, 0), (0, 255, 0))
dibujar_bresenham_3d(pantalla, (0, 0, Z_MIN), (0, 0, Z_MAX), (0, 0, 255))

pygame.display.flip()

ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

pygame.quit()
