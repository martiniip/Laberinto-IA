#!/usr/bin/env python3
from collections import deque
import argparse

def parse_input(filename):
    mazes = []
    with open(filename, "r") as file:
        while True:
            header = file.readline().strip()
            if header == '0':
                break
            m, n, start_x, start_y, end_x, end_y = map(int, header.split())
            grid = []
            for _ in range(m):
                grid.append(list(map(int, file.readline().strip().split())))
            mazes.append((m, n, start_x, start_y, end_x, end_y, grid))
    return mazes

class AgenteDFS:
    def __init__(self, laberinto, start_x, start_y, end_x, end_y):
        self.laberinto = laberinto
        self.visited = [[False] * len(laberinto[0]) for _ in range(len(laberinto))]
        self.best_path = []  # Almacenar el camino más corto encontrado hasta el momento
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y

    def dfs(self, x, y, steps, path):
        if x < 0 or x >= len(self.laberinto) or y < 0 or y >= len(self.laberinto[0]) or \
                self.visited[x][y]:
            return  # Retornar si la ruta no es válida o si la celda ya ha sido visitada

        if (x, y) == (self.end_x, self.end_y):
            if steps < len(self.best_path) or not self.best_path:
                self.best_path = path[:]  # Guardar el camino actual como el mejor camino encontrado
            return

        self.visited[x][y] = True
        path.append((x, y))

        # Obtener el valor de la celda actual para determinar la cantidad de pasos
        current_steps = self.laberinto[x][y]

        # Realizar el movimiento en cada dirección posible
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_x, new_y = x + dx * current_steps, y + dy * current_steps
            self.dfs(new_x, new_y, steps + 1, path)

        self.visited[x][y] = False
        path.pop()

    def find_path(self):
        self.dfs(self.start_x, self.start_y, 0, [])
        return self.best_path

def main():
    # Setup del parser de argumentos
    parser = argparse.ArgumentParser(description="Parse and solve jumping mazes.")
    parser.add_argument("filename", type=str, help="The filename of the maze input.")
    
    # Parsear los argumentos
    args = parser.parse_args()

    # Procesar el archivo de entrada
    try:
        mazes = parse_input(args.filename)
        for maze in mazes:
            m, n, start_x, start_y, end_x, end_y, grid = maze
            agent_dfs = AgenteDFS(grid, start_x, start_y, end_x, end_y)
            optimal_path = agent_dfs.find_path()
            count = len(optimal_path)
            print(f"Laberinto resuelto. Pasos necesarios: {count}")
    except FileNotFoundError:
        print(f"Error: El archivo '{args.filename}' no se encuentra.")

if __name__ == "__main__":
    main()
