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

        self.victoria = False  # Bandera de victoria
        self.bomba_activa = False
        self.esperando_explosion = False
        self.escapando = False
        self.historial_posiciones = []  # Guardar el historial de posiciones de Bomberman
        self.arbol_movimientos = {}  # Árbol de movimientos para la búsqueda de caminos
        self.movimientos = {}
        self.bomba = None
        self.area_explosiones = []
        self.power = 1  # Poder inicial de destrucción (rango de la bomba)
        self.pos_vec = 0
        self.movimientos = []  # Vector de movimientos a seguir
        self.bomba_activa = False
        self.victoria = False  # Flag para indicar si alcanzó la salida
        self.movimientos_realizados = 0  # Contador de movimientos realizados
        self.bomba = None  # Referencia a la bomba actual colocada
        self.area_explosiones = []  # Lista para guardar el área de explosión de cada bomba
        self.muestra_explosion = False  # Flag para mostrar la explosión en la visualización
        self.contador_explosion = 3  # Contador para mostrar la explosión en la visualización

        self.contador_global = 0  # Contador global para la búsqueda en profundidad

    def step(self):
        if self.muestra_explosion:
            self.contador_explosion -= 1
            if self.contador_explosion <= 0:
                self.muestra_explosion = False
                self.contador_explosion = 3

        # Si hay una bomba activa, reducir su temporizador y detonar si es necesario
        if self.bomba and self.bomba.temporizador > 0:
            self.bomba.temporizador -= 1
            if self.bomba.temporizador <= 0:
                self.detonar_bomba()



        if self.can_mov is False:
            return


        self.contador_global += 1
         # Colocar una bomba cada 5 movimientos
        if self.contador_global  % 5 == 0 and not self.bomba_activa and self.victoria == False:
            self.colocar_bomba()







        # Detener el movimiento si ha alcanzado la victoria
        if self.victoria:
            print("Bomberman alcanzó la meta y ganó el juego.")
            self.victoria = True
            return


        


        

        # Revisar si se alcanzó el final del vector de movimientos
        if self.pos_vec >= len(self.movimientos):
            print("No hay más movimientos en el vector.")
            return

        # Obtener la siguiente posición del vector de movimientos
        next_position = self.movimientos[self.pos_vec]



        # Verificar si la siguiente posición tiene una roca
        agentes_en_celda = self.model.grid.get_cell_list_contents(next_position)
        if any(isinstance(agent, Roca) for agent in agentes_en_celda):
            print("Hay una roca en el camino. Bomberman no puede moverse a:", next_position)
        else:
            # Moverse hacia la siguiente posición
            self.model.grid.move_agent(self, next_position)
            self.pos_vec += 1  # Avanzar en el vector de movimientos
            self.movimientos_realizados += 1
                    # Revisar si ha alcanzado la salida
            if next_position == self.model.salida:
                self.victoria = True  # Activar flag de victoria
                print("Bomberman alcanzó la salida y ganó el juego.")







    def colocar_bomba(self):
        # Colocar una bomba en la posición actual de Bomberman
        unique_id = self.model.next_id()  # Genera un ID único para la bomba
        self.bomba_activa = True
        self.bomba = Bomba(unique_id, self.model, self.pos, self.power)
        self.model.grid.place_agent(self.bomba, self.pos)  # Agregar la bomba a la grilla
        print("Bomberman colocó una bomba en:", self.pos)

    def detonar_bomba(self):
        # Método para detonar automáticamente la bomba después de que el temporizador llegue a 0
        if self.bomba and self.bomba_activa:
            self.bomba.explotar(self)
            self.bomba_activa = False
            self.bomba = None  # Limpiar referencia a la bomba después de explotar
            print("La bomba explotó automáticamente.")






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
        super().__init__(unique_id, model)
        self.pos = pos
        self.power = power
        self.temporizador = 3  # La bomba explotará después de 3 pasos
        self.en_explosion = False

    def explotar(self, bomberman):
        # Método para detonar la bomba y aplicar el efecto de la explosión
        self.en_explosion = True
        area_explosion = self.calcular_area_explosion()
        
        # Guardar el área de explosión en Bomberman
        bomberman.area_explosiones=area_explosion
        bomberman.muestra_explosion = True  # Mostrar la explosión en la visualización
        bomberman.contador_explosion = 3  # Contador para mostrar la explosión en la visualización
        
        # Remover agentes (ej. rocas) en el área de explosión
        for pos in area_explosion:
            agentes = self.model.grid.get_cell_list_contents(pos)
            for agente in agentes:
                if isinstance(agente, Roca):
                    self.model.grid.remove_agent(agente)
                    
        print("¡Bomba explotó en la posición:", self.pos, "con área de explosión:", area_explosion)
        self.model.grid.remove_agent(self)  # Elimina la bomba después de explotar

    def calcular_area_explosion(self):
        # Calcula el área de explosión de la bomba según su poder
        area = [self.pos]
        for i in range(1, self.power + 1):
            area.extend([
                (self.pos[0] + i, self.pos[1]), (self.pos[0] - i, self.pos[1]),  # Horizontal
                (self.pos[0], self.pos[1] + i), (self.pos[0], self.pos[1] - i)   # Vertical
            ])
        return [p for p in area if 0 <= p[0] < self.model.grid.width and 0 <= p[1] < self.model.grid.height]