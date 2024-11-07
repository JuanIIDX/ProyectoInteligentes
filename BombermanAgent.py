from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import SimultaneousActivation
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
import random
from queue import PriorityQueue
from GloboAgent import GloboAgent
from busquedas import Busquedas
from clases import Roca, Camino, Metal, Salida
from collections import deque  # Cola para la búsqueda en anchura (BFS)

class BombermanAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        

        self.power = 1  # Poder inicial de destrucción (rango de la bomba)
        self.pos_vec = 0
        self.direction = 2  # Dirección en la que se mueve el agente
        self.can_mov = False
        self.victoria = False
        self.bomba_activa = False  # Estado que indica si hay una bomba activa colocada por Bomberman
        self.esperando_explosion = False  # Indica si Bomberman está esperando que la bomba explote


        self.arbol_movimientos = {}  # Árbol de movimientos para la búsqueda de caminos
        self.movimientos = {}
        

        self.modulo_busqueda = Busquedas()  # Módulo de búsqueda seleccionado


        #----------------
        self.modo_busqueda = 0  # Modo de búsqueda (0: Anchura, 1: Profundidad, 2: Busqueda Uniforme)
        self.inicio= (0,0)
        self.salida= (0,0)
        self.grid= None

        self.bomba_activa = False  # Estado que indica si hay una bomba activa colocada por Bomberman
        self.esperando_explosion = False  # Indica si Bomberman está esperando que la bomba explote
        self.movimientos_realizados = 0  # Contador de pasos
        self.escapando = False  # Estado que indica si Bomberman está en ruta de escape


        self.modulo_busqueda = Busquedas()  # Módulo de búsqueda seleccionado
        self.movimientos = {}  # Almacena el camino a seguir
        self.salida = (0, 0)  # Posición de la salida
        self.bomba = None  # Bomba actual
        self.area_explosiones = []  # Lista para guardar las posiciones de la onda expansiva

        self.muestra_explosion=False
        self.contador_explosion=3



    def step(self):

        if self.muestra_explosion:
            self.contador_explosion-=1
            if self.contador_explosion==0:
                self.muestra_explosion=False
                self.contador_explosion=0




        # Controlar el temporizador y explosión de la bomba
        if self.bomba_activa and self.bomba:
            self.bomba.temporizador -= 1
            if self.bomba.temporizador <= 0:
                self.bomba.explotar(self)
                self.bomba_activa = False
                self.bomba = None
                self.reanudar_camino()  # Reanuda el camino original después de la explosión

        # Si está esperando la explosión, no moverse
        if self.esperando_explosion:
            if not self.escapando:
                # Genera un camino seguro alejándose de la zona de explosión
                self.generar_camino_escape_bfs()
                self.escapando = True
            else:
                # Seguir el camino de escape mientras espera la explosión
                if self.movimientos:
                    next_position = self.movimientos[self.pos_vec]
                    self.model.grid.move_agent(self, next_position)
                    self.pos_vec += 1
                    if self.pos_vec >= len(self.movimientos):
                        self.pos_vec = 0
                return  # Suspende cualquier otra acción hasta que la bomba explote

        if self.can_mov and self.movimientos and not self.victoria:
            # Verificar si estamos adyacentes a la salida
            if self.adyacente_a_salida():
                # Colocar una bomba antes de llegar a la salida
                self.colocar_bomba()
                return  # Suspender el movimiento hacia la meta hasta que la bomba explote

            # Moverse hacia la siguiente posición en la lista de movimientos
            next_position = self.movimientos[self.pos_vec]
            self.model.grid.move_agent(self, next_position)  # Mover a la siguiente posición
            self.pos_vec += 1  # Avanzar en el vector de movimientos
            self.movimientos_realizados += 1

            # Colocar una bomba cada 5 movimientos (si no estamos adyacentes a la meta)
            if self.movimientos_realizados % 5 == 0 and not self.bomba_activa:
                self.colocar_bomba()

            # Revisar si ha alcanzado la salida
            if next_position == self.salida:
                self.victoria = True
                print("Bomberman ha alcanzado la salida y ganó el juego.")

            # Reiniciar la posición en el vector de movimientos si se llega al final
            if self.pos_vec >= len(self.movimientos):
                self.pos_vec = 0  # Reiniciar al comienzo de la lista

        else:
            print("Bomberman no puede moverse o ya ha alcanzado la salida.")

    def colocar_bomba(self):
        # Colocar una bomba en la posición actual de Bomberman
        unique_id = self.model.next_id()  # Genera un ID único para la bomba
        self.bomba_activa = True
        self.bomba = Bomba(unique_id, self.model, self.pos, self.power)
        self.model.grid.place_agent(self.bomba, self.pos)  # Agregar la bomba a la grilla para visualización
        self.esperando_explosion = True
        
        # Calcular y guardar el área de explosión de la bomba
        self.area_explosiones = self.calcular_area_explosion(self.pos, self.power)
        print("Bomberman colocó una bomba en:", self.pos)
        print("Área de explosión:", self.area_explosiones)
        

    def generar_camino_escape_bfs(self):
        # Genera un camino seguro utilizando BFS para alejarse de la zona de explosión
        area_explosion = self.calcular_area_explosion(self.pos, self.power)
        queue = deque([(self.pos, [])])  # Cola para BFS (posición, camino hasta esa posición)
        visited = set()
        visited.add(self.pos)

        while queue:
            current_pos, path = queue.popleft()

            # Limitar la búsqueda a 10 celdas de profundidad
            if len(path) > 10:
                break

            # Si encontramos una posición segura fuera del área de explosión
            if current_pos not in area_explosion and self.model.grid.is_cell_empty(current_pos):
                self.movimientos = path + [current_pos]
                self.pos_vec = 0
                print(f"Bomberman encontró un camino de escape hacia {current_pos} usando BFS.")
                return

            # Expandir a posiciones vecinas
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (current_pos[0] + dx, current_pos[1] + dy)
                if (
                    0 <= neighbor[0] < self.model.grid.width and
                    0 <= neighbor[1] < self.model.grid.height and
                    neighbor not in visited
                ):
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        # Si no encuentra un camino seguro en 10 pasos, selecciona una posición aleatoria
        posiciones_seguras = [
            pos for pos in self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
            if pos not in area_explosion and self.model.grid.is_cell_empty(pos)
        ]
        if posiciones_seguras:
            escape_path = [random.choice(posiciones_seguras)]
            self.movimientos = escape_path
            self.pos_vec = 0
            print(f"Bomberman no encontró una posición segura en 10 pasos, elige una aleatoria en {escape_path[0]}.")

    def reanudar_camino(self):
        # Reanuda el movimiento hacia la meta después de que la bomba explota
        self.esperando_explosion = False
        self.escapando = False
        print("Bomba explotó, Bomberman reanuda su camino hacia la meta.")
        self.muestra_explosion=True
        self.contador_explosion=3
        

    def adyacente_a_salida(self):
        # Verificar si Bomberman está en una posición adyacente a la salida
        for dx, dy in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            if (self.pos[0] + dx, self.pos[1] + dy) == self.salida:
                return True
        return False

    def calcular_area_explosion(self, pos, power):
        area = [pos]
        for i in range(1, power + 1):
            area.extend([
                (pos[0] + i, pos[1]), (pos[0] - i, pos[1]),  # Horizontal
                (pos[0], pos[1] + i), (pos[0], pos[1] - i)   # Vertical
            ])
        return [p for p in area if 0 <= p[0] < self.model.grid.width and 0 <= p[1] < self.model.grid.height]






    def selecciona_modo_busqueda(self,modo_busqueda, inicio, fin, grid):
        self.modo_busqueda = modo_busqueda
        self.inicio = inicio
        self.salida = fin
        self.grid = grid
        self.arbol_movimientos = {}
        self.movimientos = {}

    def camino_busqueda(self, inicio, fin, grid):
        if self.modo_busqueda == 0:
            self.arbol_movimientos = self.modulo_busqueda.busqueda_anchura(inicio, fin, grid)
            self.movimientos = self.modulo_busqueda.obtiene_camino_anchura(inicio, fin, grid)
            print("Se selecciono busqueda en anchura")
        elif self.modo_busqueda == 1:
            self.arbol_movimientos = self.modulo_busqueda.busqueda_profundidad(inicio, fin, grid)
            self.movimientos = self.modulo_busqueda.obtiene_camino_profundidad(inicio, fin, grid)
            print("Se selecciono busqueda en profundidad")
        elif self.modo_busqueda == 2:
            self.arbol_movimientos = self.modulo_busqueda.busqueda_costo_uniforme(inicio, fin, grid)
            self.movimientos = self.modulo_busqueda.obtiene_camino_uniforme(inicio, fin, grid)
            print("Se selecciono busqueda en costo uniforme")
        elif self.modo_busqueda == 3: #Beam Search
            self.arbol_movimientos = self.modulo_busqueda.busqueda_beam(inicio, fin, grid)
            self.movimientos = self.modulo_busqueda.obtiene_camino_beam(inicio, fin, grid)
            print("Se selecciono busqueda en beam")
        elif self.modo_busqueda == 4: #Hill Climbing
            self.arbol_movimientos = self.modulo_busqueda.busqueda_hill_climbing(inicio, fin, grid)
            self.movimientos = self.modulo_busqueda.obtiene_camino_hill_climbing(inicio, fin, grid)
            print("Se selecciono busqueda en hill climbing")
        else: #A*
            self.arbol_movimientos = self.modulo_busqueda.busqueda_a_estrella(inicio, fin, grid)
            self.movimientos = self.modulo_busqueda.obtiene_camino_a_estrella(inicio, fin, grid)
            print("Se selecciono busqueda en A*")

class Bomba(Agent):
    def __init__(self, unique_id, model, pos, power):
        super().__init__(unique_id, model)  # Inicializa el unique_id en la clase padre Agent
        self.pos = pos
        self.power = power
        self.temporizador = 3
        self.en_explosion = False

    def explotar(self, bomberman):
        self.en_explosion = True
        area_explosion = bomberman.calcular_area_explosion(self.pos, self.power)
        for pos in area_explosion:
            agentes = bomberman.model.grid.get_cell_list_contents(pos)
            for agente in agentes:
                if isinstance(agente, (Roca, GloboAgent)):
                    bomberman.model.grid.remove_agent(agente)
        print("¡Bomba explotó en la posición:", self.pos)
        bomberman.model.grid.remove_agent(self)  # Elimina la bomba después de explotar