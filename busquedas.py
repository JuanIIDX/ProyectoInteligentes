from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import SimultaneousActivation
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
import random
from queue import PriorityQueue
from collections import deque
import os
from clases import Roca, Camino, Metal, Salida

class Busquedas():

    def __init__(self):
        pass


    """★★★★★★★★★★★★★★★★★★★★Metodos de busqueda★★★★★★★★★★★★★★★★★★★★★★★★★★★★★"""

    """★★BFS★★"""

    """★Busqueda con pasos★"""
    def busqueda_anchura(self, start, end, grid):
        queue = deque()
        visited = {}
        step_dict = {}
        step = 0
        queue.append((start, step))
        visited[start] = step
        step_dict[step] = [start]
        
        # Prioridades de movimiento: izquierda, arriba, derecha, abajo
        priority_directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        
        while queue:
            current, step = queue.popleft()
            if current == end:
                break
            next_step = step + 1
            
            # Calcular vecinos en el orden de prioridad
            neighbors = [
                (current[0] + dx, current[1] + dy)
                for dx, dy in priority_directions
                if grid.out_of_bounds((current[0] + dx, current[1] + dy)) == False
            ]
            
            for neighbor in neighbors:
                if neighbor not in visited:
                    cell = grid.get_cell_list_contents(neighbor)
                    if cell:
                        if type(cell[0]) is Salida:
                            visited[neighbor] = next_step
                            if next_step not in step_dict:
                                step_dict[next_step] = []
                            step_dict[next_step].append(neighbor)
                            return step_dict
                        elif type(cell[0]) is Camino:
                            visited[neighbor] = next_step
                            queue.append((neighbor, next_step))
                            if next_step not in step_dict:
                                step_dict[next_step] = []
                            step_dict[next_step].append(neighbor)
        return {}

    """★Camino★"""
    
    def obtiene_camino_anchura(self, start, end, grid):
        step_dict = self.busqueda_anchura(start, end, grid)

        if not step_dict:
            return []

        path = []
        current = end
        path.append(current)

        for step in range(max(step_dict.keys()), 0, -1):
            for neighbor in grid.get_neighborhood(current, moore=False, include_center=False):
                if neighbor in step_dict[step - 1]:
                    path.append(neighbor)
                    current = neighbor
                    break

        path.reverse()
        return path

        

    """★Busqueda en profundidad básica con prioridad fija★"""
    def busqueda_profundidad(self, start, end, grid):
        stack = deque()
        visited = set()
        step_dict = {}
        step = 0
        stack.append((start, step))
        visited.add(start)
        step_dict[step] = [start]

        # Prioridades de movimiento: izquierda, arriba, derecha, abajo
        priority_directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

        while stack:
            current, step = stack.pop()
            next_step = step + 1

            # Explorar en el orden de prioridad
            for dx, dy in priority_directions:
                neighbor = (current[0] + dx, current[1] + dy)

                # Verificar que el vecino esté dentro de los límites de la cuadrícula y no haya sido visitado
                if 0 <= neighbor[0] < grid.width and 0 <= neighbor[1] < grid.height and neighbor not in visited:
                    cell = grid.get_cell_list_contents(neighbor)
                    if cell:
                        # Si encontramos la salida, añadimos y terminamos
                        if type(cell[0]) is Salida:
                            visited.add(neighbor)
                            if next_step not in step_dict:
                                step_dict[next_step] = []
                            step_dict[next_step].append(neighbor)
                            return step_dict

                        # Si encontramos un camino, avanzamos en esa dirección
                        elif type(cell[0]) is Camino:
                            visited.add(neighbor)
                            stack.append((neighbor, next_step))
                            if next_step not in step_dict:
                                step_dict[next_step] = []
                            step_dict[next_step].append(neighbor)

        return {}

    """★Camino★"""
    def obtiene_camino_profundidad(self, start, end, grid):
        step_dict = self.busqueda_profundidad(start, end, grid)

        if not step_dict:
            return []

        path = []
        current = end
        path.append(current)

        # Reconstruir el camino desde el diccionario de pasos
        for step in range(max(step_dict.keys()), 0, -1):
            for neighbor in grid.get_neighborhood(current, moore=False, include_center=False):
                if neighbor in step_dict.get(step - 1, []):
                    path.append(neighbor)
                    current = neighbor
                    break

        path.reverse()
        return path
    """★ Búsqueda de costo uniforme con prioridad de dirección ★"""
    def busqueda_costo_uniforme(self, start, end, grid):
        queue = PriorityQueue()
        visited = {}
        step_dict = {}
        step = 0
        queue.put((0, start, step))  # (costo acumulado, posición actual, paso)
        visited[start] = 0  # Guardar el costo acumulado en cada nodo
        step_dict[step] = [start]

        # Prioridades de movimiento: izquierda, arriba, derecha, abajo
        priority_directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

        while not queue.empty():
            current_cost, current, step = queue.get()
            next_step = step + 1

            # Si hemos llegado al nodo final
            if current == end:
                break

            # Explorar vecinos en el orden de prioridad
            for dx, dy in priority_directions:
                neighbor = (current[0] + dx, current[1] + dy)

                # Verificar que el vecino esté dentro de los límites de la cuadrícula
                if 0 <= neighbor[0] < grid.width and 0 <= neighbor[1] < grid.height:
                    cell = grid.get_cell_list_contents(neighbor)
                    if cell:
                        # Costo acumulado del vecino
                        new_cost = current_cost + 1  # Asumiendo que cada movimiento tiene un costo de 1

                        # Si encontramos la salida, añadimos y terminamos
                        if type(cell[0]) is Salida:
                            visited[neighbor] = new_cost
                            if next_step not in step_dict:
                                step_dict[next_step] = []
                            step_dict[next_step].append(neighbor)
                            return step_dict

                        # Si encontramos un camino y el nuevo costo es menor, actualizamos
                        elif type(cell[0]) is Camino and (neighbor not in visited or new_cost < visited[neighbor]):
                            visited[neighbor] = new_cost
                            queue.put((new_cost, neighbor, next_step))
                            if next_step not in step_dict:
                                step_dict[next_step] = []
                            step_dict[next_step].append(neighbor)

        return {}

    """★ Camino ★"""
    def obtiene_camino_uniforme(self, start, end, grid):
        step_dict = self.busqueda_costo_uniforme(start, end, grid)

        if not step_dict:
            return []

        path = []
        current = end
        path.append(current)

        # Reconstruir el camino desde el diccionario de pasos
        for step in range(max(step_dict.keys()), 0, -1):
            for neighbor in grid.get_neighborhood(current, moore=False, include_center=False):
                if neighbor in step_dict.get(step - 1, []):
                    path.append(neighbor)
                    current = neighbor
                    break

        path.reverse()
        return path

    """★★Beam Search★★"""
    """★ Búsqueda Beam Search con prioridad de dirección ★"""
    def busqueda_beam(self, start, end, grid, beam_width=2):
        queue = PriorityQueue()
        visited = set()
        step_dict = {}
        step = 0
        queue.put((0, start, step))  # (heurístico/costo acumulado, posición actual, paso)
        visited.add(start)
        step_dict[step] = [start]

        # Prioridades de movimiento: izquierda, arriba, derecha, abajo
        priority_directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]

        while not queue.empty():
            next_level = PriorityQueue()  # Cola de prioridad para el siguiente nivel
            current_nodes = []
            
            # Extraer los nodos del nivel actual (limitado por `beam_width`)
            for _ in range(min(beam_width, queue.qsize())):
                current_cost, current, step = queue.get()
                current_nodes.append((current_cost, current, step))
                
                # Si hemos llegado al nodo final
                if current == end:
                    return step_dict

            next_step = step + 1

            # Explorar cada nodo actual en el orden de prioridad
            for current_cost, current, step in current_nodes:
                for dx, dy in priority_directions:
                    neighbor = (current[0] + dx, current[1] + dy)

                    # Verificar que el vecino esté dentro de los límites de la cuadrícula
                    if 0 <= neighbor[0] < grid.width and 0 <= neighbor[1] < grid.height and neighbor not in visited:
                        cell = grid.get_cell_list_contents(neighbor)
                        if cell:
                            # Heurístico: distancia Manhattan (para priorizar nodos cercanos al objetivo)
                            heuristic_cost = current_cost + 1 + abs(neighbor[0] - end[0]) + abs(neighbor[1] - end[1])

                            # Si encontramos la salida, añadimos y terminamos
                            if type(cell[0]) is Salida:
                                visited.add(neighbor)
                                if next_step not in step_dict:
                                    step_dict[next_step] = []
                                step_dict[next_step].append(neighbor)
                                return step_dict

                            # Si encontramos un camino, lo agregamos al siguiente nivel
                            elif type(cell[0]) is Camino:
                                visited.add(neighbor)
                                next_level.put((heuristic_cost, neighbor, next_step))
                                if next_step not in step_dict:
                                    step_dict[next_step] = []
                                step_dict[next_step].append(neighbor)

            # Actualizar la cola principal con los nodos del siguiente nivel, limitando el ancho del beam
            queue = next_level

        return {}

    """★ Camino ★"""
    def obtiene_camino_beam(self, start, end, grid, beam_width=2):
        step_dict = self.busqueda_beam(start, end, grid, beam_width)

        if not step_dict:
            return []

        path = []
        current = end
        path.append(current)

        # Reconstruir el camino desde el diccionario de pasos
        for step in range(max(step_dict.keys()), 0, -1):
            for neighbor in grid.get_neighborhood(current, moore=False, include_center=False):
                if neighbor in step_dict.get(step - 1, []):
                    path.append(neighbor)
                    current = neighbor
                    break

        path.reverse()
        return path

    """★ Búsqueda Hill Climbing con prioridad de dirección y retroceso ★"""
    def busqueda_hill_climbing(self, start, end, grid):
        stack = deque()
        visited = set()
        step_dict = {}
        step = 0
        stack.append((start, step))
        visited.add(start)
        step_dict[step] = [start]

        # Prioridades de movimiento: izquierda, arriba, derecha, abajo
        priority_directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]

        while stack:
            current, step = stack.pop()

            # Si hemos llegado al nodo final
            if current == end:
                break

            best_neighbor = None
            best_heuristic = float('inf')
            next_step = step + 1

            # Explorar vecinos en el orden de prioridad y calcular heurísticos
            for dx, dy in priority_directions:
                neighbor = (current[0] + dx, current[1] + dy)

                # Verificar que el vecino esté dentro de los límites de la cuadrícula y no haya sido visitado
                if 0 <= neighbor[0] < grid.width and 0 <= neighbor[1] < grid.height and neighbor not in visited:
                    cell = grid.get_cell_list_contents(neighbor)
                    if cell:
                        # Calcular heurístico: distancia Manhattan al objetivo
                        heuristic = abs(neighbor[0] - end[0]) + abs(neighbor[1] - end[1])

                        # Si encontramos la salida, añadimos y terminamos
                        if type(cell[0]) is Salida:
                            visited.add(neighbor)
                            if next_step not in step_dict:
                                step_dict[next_step] = []
                            step_dict[next_step].append(neighbor)
                            return step_dict

                        # Si encontramos un camino y su heurística es mejor, lo consideramos como el mejor vecino
                        elif type(cell[0]) is Camino and heuristic < best_heuristic:
                            best_neighbor = neighbor
                            best_heuristic = heuristic

            # Si encontramos un mejor vecino, lo visitamos
            if best_neighbor:
                visited.add(best_neighbor)
                stack.append((current, step))  # Guardar el nodo actual para posibles retrocesos
                stack.append((best_neighbor, next_step))  # Avanzar al mejor vecino
                if next_step not in step_dict:
                    step_dict[next_step] = []
                step_dict[next_step].append(best_neighbor)
            else:
                # Si no encontramos un mejor vecino, retrocedemos al último nodo en el `stack`
                continue

        return {}

    """★ Camino ★"""
    def obtiene_camino_hill_climbing(self, start, end, grid):
        step_dict = self.busqueda_hill_climbing(start, end, grid)

        if not step_dict:
            return []

        path = []
        current = end
        path.append(current)

        # Reconstruir el camino desde el diccionario de pasos
        for step in range(max(step_dict.keys()), 0, -1):
            for neighbor in grid.get_neighborhood(current, moore=False, include_center=False):
                if neighbor in step_dict.get(step - 1, []):
                    path.append(neighbor)
                    current = neighbor
                    break

        path.reverse()
        return path
    """★ Búsqueda A* (A estrella) con prioridad de dirección ★"""
    def busqueda_a_estrella(self, start, end, grid):
        queue = PriorityQueue()
        visited = {}
        step_dict = {}
        step = 0
        queue.put((0, start, step))  # (f(n), posición actual, paso)
        visited[start] = 0  # Guardar el costo acumulado g(n) en cada nodo
        step_dict[step] = [start]

        # Prioridades de movimiento: izquierda, arriba, derecha, abajo
        priority_directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]

        while not queue.empty():
            current_f, current, step = queue.get()
            next_step = step + 1

            # Si hemos llegado al nodo final
            if current == end:
                break

            # Explorar vecinos en el orden de prioridad
            for dx, dy in priority_directions:
                neighbor = (current[0] + dx, current[1] + dy)

                # Verificar que el vecino esté dentro de los límites de la cuadrícula
                if 0 <= neighbor[0] < grid.width and 0 <= neighbor[1] < grid.height:
                    cell = grid.get_cell_list_contents(neighbor)
                    if cell:
                        # Calcular g(n) para el vecino
                        new_g = visited[current] + 1  # Asumiendo que cada movimiento tiene un costo de 1
                        
                        # Calcular h(n) usando la distancia Manhattan al objetivo
                        h = abs(neighbor[0] - end[0]) + abs(neighbor[1] - end[1])
                        
                        # Calcular f(n) = g(n) + h(n)
                        f = new_g + h

                        # Si encontramos la salida, añadimos y terminamos
                        if type(cell[0]) is Salida:
                            visited[neighbor] = new_g
                            if next_step not in step_dict:
                                step_dict[next_step] = []
                            step_dict[next_step].append(neighbor)
                            return step_dict

                        # Si encontramos un camino y el nuevo costo es menor o el nodo no ha sido visitado
                        elif type(cell[0]) is Camino and (neighbor not in visited or new_g < visited[neighbor]):
                            visited[neighbor] = new_g
                            queue.put((f, neighbor, next_step))
                            if next_step not in step_dict:
                                step_dict[next_step] = []
                            step_dict[next_step].append(neighbor)

        return {}

    """★ Camino ★"""
    def obtiene_camino_a_estrella(self, start, end, grid):
        step_dict = self.busqueda_a_estrella(start, end, grid)

        if not step_dict:
            return []

        path = []
        current = end
        path.append(current)

        # Reconstruir el camino desde el diccionario de pasos
        for step in range(max(step_dict.keys()), 0, -1):
            for neighbor in grid.get_neighborhood(current, moore=False, include_center=False):
                if neighbor in step_dict.get(step - 1, []):
                    path.append(neighbor)
                    current = neighbor
                    break

        path.reverse()
        return path