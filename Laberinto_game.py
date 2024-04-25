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

# Inicializar Pygame
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

def draw_laberinto(player_row, player_col, valid_moves, steps):
    window.fill((255, 255, 255))  # Limpiar la ventana
    pygame.draw.rect(window, (0, 255, 0), (start_col * CELL_SIZE, start_row * CELL_SIZE, CELL_SIZE, CELL_SIZE)) #pinta verde inicio 
    pygame.draw.rect(window, (255, 0, 0), (end_col * CELL_SIZE, end_row * CELL_SIZE, CELL_SIZE, CELL_SIZE)) # pinta rojo final
    for i, row in enumerate(laberinto):
        for j, cell in enumerate(row):
            x = j * CELL_SIZE
            y = i * CELL_SIZE
            if cell == 0:
                cell = "G"  # Convertir 0 a "G" para visualizar mejor en la ventana
            pygame.draw.rect(window, (0, 0, 0), (x, y, CELL_SIZE, CELL_SIZE), 1)  # pinta negro solo exteriores
            font = pygame.font.Font(None, 20)
            text = font.render(str(cell), True, (0, 0, 0))
            text_rect = text.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
            window.blit(text, text_rect)

    # Dibujar celdas de movimiento permitidas
    for move in valid_moves:
        row, col = move
        pygame.draw.rect(window, (0, 255, 0), (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)

    # Dibujar casilla actual del jugador en azul
    pygame.draw.rect(window, (0, 0, 255), (player_col * CELL_SIZE, player_row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)

    # Mostrar cantidad de pasos
    font = pygame.font.Font(None, 24)
    steps_text = font.render(f"Steps: {steps}", True, (0, 0, 0))
    window.blit(steps_text, (10, 10))

    pygame.display.update()

def get_valid_moves(row, col):
    max_distance = laberinto[row][col]
    valid_moves = []
    for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        new_row, new_col = row + dr * max_distance, col + dc * max_distance
        if 0 <= new_row < m and 0 <= new_col < n:
            valid_moves.append((new_row, new_col))
    return valid_moves


def main():
    player_row, player_col = start_row, start_col  # Posición inicial del jugador
    steps = 0  # Contador de pasos

    running = True
    logrado= False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                clicked_row = mouse_pos[1] // CELL_SIZE
                clicked_col = mouse_pos[0] // CELL_SIZE
                if (clicked_row, clicked_col) in get_valid_moves(player_row, player_col):
                    player_row, player_col = clicked_row, clicked_col
                    steps += 1
                    if laberinto[player_row][player_col] == "G" or laberinto[player_row][player_col] == 0:  # Si llegamos a la casilla "G"
                        logrado=True
                        running = False  # Terminar el juego

        draw_laberinto(player_row, player_col, get_valid_moves(player_row, player_col), steps)  # Dibujar el laberinto con las celdas de movimiento permitidas
        pygame.display.update()

    # Mostrar mensaje de victoria y pasos al llegar a la casilla "G"
    if logrado== True:
        print("¡Victoria!")
        print(f"Pasos necesarios: {steps}")

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
