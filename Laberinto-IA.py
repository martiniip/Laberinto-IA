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

class AgenteDFS:
    def __init__(self, laberinto, start_row, start_col, end_row, end_col):
        self.laberinto = laberinto
        self.visited = [[False] * len(laberinto[0]) for _ in range(len(laberinto))]
        self.best_path = []  # Almacenar el camino más corto encontrado hasta el momento
        self.start_row = start_row
        self.start_col = start_col
        self.end_row = end_row
        self.end_col = end_col

    def dfs(self, row, col, steps, path):
        if row < 0 or row >= len(self.laberinto) or col < 0 or col >= len(self.laberinto[0]) or \
                self.visited[row][col]:
            return  # Retornar si la ruta no es válida o si la celda ya ha sido visitada

        if self.laberinto[row][col] in [0, 'G']:
            if steps < len(self.best_path) or not self.best_path:
                self.best_path = path[:]  # Guardar el camino actual como el mejor camino encontrado
            return

        self.visited[row][col] = True
        path.append((row, col))

        # Obtener el valor de la celda actual para determinar la cantidad de pasos
        current_steps = self.laberinto[row][col]

        # Realizar el movimiento en cada dirección posible
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_row, new_col = row + dr * current_steps, col + dc * current_steps
            self.dfs(new_row, new_col, steps + 1, path)

        self.visited[row][col] = False
        path.pop()

    def find_path(self):
        self.dfs(self.start_row, self.start_col, 0, [])
        return self.best_path

def draw_laberinto(agent, optimal_path):
    for i, row in enumerate(laberinto):
        for j, cell in enumerate(row):
            x = j * CELL_SIZE
            y = i * CELL_SIZE
            if cell == 0:
                cell = "G"  # Convertir 0 a "G" para visualizar mejor en la ventana
            pygame.draw.rect(window, (0, 0, 0), (x, y, CELL_SIZE, CELL_SIZE), 1)  # Dibujar cuadrado negro
            font = pygame.font.Font(None, 20)
            text = font.render(str(cell), True, (0, 0, 0))
            text_rect = text.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
            window.blit(text, text_rect)

    # Dibujar el camino óptimo en rojo
    for pos in optimal_path:
        x = pos[1] * CELL_SIZE
        y = pos[0] * CELL_SIZE
        pygame.draw.rect(window, (255, 0, 0), (x, y, CELL_SIZE, CELL_SIZE),1)

def main():
    agent_dfs = AgenteDFS(laberinto, start_row, start_col, end_row, end_col)
    optimal_path = agent_dfs.find_path()
    count=0
    for pos in optimal_path:
        count+=1
    print(count)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        window.fill((255, 255, 255))
        draw_laberinto(agent_dfs, optimal_path)  # Dibujar el laberinto y el camino óptimo
        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
