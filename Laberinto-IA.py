import pygame
import sys

# Función para leer el laberinto desde un archivo de texto
def leer_laberinto(nombre_archivo):
    laberinto = []
    with open(nombre_archivo, 'r') as archivo:
        for linea in archivo:
            valores = list(map(int, linea.strip().split()))
            laberinto.append(valores)
    return laberinto

# Tamaño de cada celda del laberinto en píxeles
CELL_SIZE = 100

# Inicializar Pygamepython -m pip install pygame

pygame.init()

# Leer el laberinto desde el archivo
laberinto = leer_laberinto('laberintos.txt')

# Extraer información de la primera línea
m, n, start_row, start_col, end_row, end_col = laberinto.pop(0)

# Dimensiones de la ventana
WIDTH = n * CELL_SIZE
HEIGHT = m * CELL_SIZE

# Crear la ventana
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Laberinto")

# Dibujar el laberinto en la ventana
def draw_laberinto():
    for i, row in enumerate(laberinto):
        for j, cell in enumerate(row):
            x = j * CELL_SIZE
            y = i * CELL_SIZE
            if cell == 0:
                cell = "G"
            pygame.draw.rect(window, (0, 0, 0), (x, y, CELL_SIZE, CELL_SIZE), 1)  # Dibujar cuadrado negro
            font = pygame.font.Font(None, 20)
            text = font.render(str(cell), True, (0, 0, 0))
            text_rect = text.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
            window.blit(text, text_rect)

    # Marcar la celda de inicio y la celda de destino
    start_x = start_col * CELL_SIZE
    start_y = start_row * CELL_SIZE
    end_x = end_col * CELL_SIZE
    end_y = end_row * CELL_SIZE

    pygame.draw.rect(window, (0, 255, 0), (start_x, start_y, CELL_SIZE, CELL_SIZE), 2)
    pygame.draw.rect(window, (255, 0, 0), (end_x, end_y, CELL_SIZE, CELL_SIZE), 2)

# Bucle principal del juego
def main():
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        window.fill((255, 255, 255))
        draw_laberinto()
        pygame.display.update()

    pygame.quit()
    sys.exit()

# Iniciar el juego
if __name__ == "__main__":
    main()
