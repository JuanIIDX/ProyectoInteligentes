from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import SimultaneousActivation
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
import random
from queue import PriorityQueue
from BombermanAgent import BombermanAgent
from collections import deque

class Roca(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

class Camino(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

class Metal(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

class Salida(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)


# Modelo del juego
class GameModel(Model):
    def __init__(self, width, height, num_globos, modo_busqueda,modo_aleatorio, numero_rocas):
        super().__init__()

        # Se crea la grilla y el schedule
        self.grid = MultiGrid(width, height, True) #Se crear una grilla de tamaño width x height(Poner aleatorio luego)
        self.schedule = SimultaneousActivation(self) #Se crea un schedule para los agentes
        
        # Se crear una posicion de salida que no este en un x,y par ni en las paredes
        self.inicio= (0,0)
        self.salida = (0,0)
        self.tipo_busqueda = 'X'
        self.numero_rocas = numero_rocas

        self.camino_busqueda = {}
        self.caminos = []


        """Modo de carga---Se crea el escenario"""

        #Si el modo de carga es 0, entonces se crea el mundo de forma aleatorio
        if modo_aleatorio == 0:
            print('Se activo la carga aleatoria')
            self.crea_mundo_aleatorio()

        #Si el modo de carga es 1, entonces se crea el mundo a partir de un archivo
        else:
            print('Se activo la carga por un archivo')
            self.crea_mundo_aleatorio()      
        



        """Modo de busqueda"""
        #Si el modo de busqueda es 0, entonces se hace una busqueda en anchura
        if modo_busqueda == 0:
            self.tipo_busqueda = 'A'
            self.camino_busqueda=self.busqueda_anchura(self.inicio, self.salida)
            self.caminos=self.get_road_breadth(self.inicio, self.salida)

        #Si el modo de busqueda es 1, entonces se hace una busqueda en profundidad
        elif modo_busqueda == 1:
            print('Se activo la busqueda en profundidad')
            self.tipo_busqueda = 'P'
            self.camino_busqueda=self.busqueda_profundidad(self.inicio, self.salida)
            self.caminos=self.get_road_depth(self.inicio, self.salida)


        #Si el modo de busqueda es 2, entonces se hace una busqueda A
        else:
            print('Se activo la busqueda por costos uniformes')
            self.tipo_busqueda = 'C'
            self.camino_busqueda=self.busqueda_costo_uniforme(self.inicio, self.salida)
            self.caminos=self.get_road_uniform(self.inicio, self.salida)



        
        # Se crea el agente Bomberman con la posicion de inicio
        self.personaje = BombermanAgent(1, self)
        self.grid.place_agent(self.personaje, self.inicio)
        self.schedule.add(self.personaje)

        #Se establecen las variables booleanas para saber si el bomberman se puede mover o no
        self.bomberman_mueve = False
        self.muestra_camino = False
        self.nivel_maximo = 0
        self.state = "Estado Inicial"



        print("Inicio: ", self.inicio)
        print("Salida: ", self.salida)
       

        # Añadir globos (enemigos) en posiciones aleatorias
        # POR EL MOMENTO NO SE ACTIVAN
    """         for i in range(num_globos):
            globo = GloboAgent(i + 2, self)
            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)
            self.grid.place_agent(globo, (x, y))
            self.schedule.add(globo) """
    
    """★★★★★★★★★★★★★★★★★★★★Metodos de creacion de mundo★★★★★★★★★★★★★★★★★★★★★★★★★★★★★"""
    
    def crea_mundo_aleatorio(self):

        def crea_paredes_externas(self):
            """Crea las paredes externas del mundo"""
            for x in range(self.grid.width):
                metal = Metal(self.next_id(), self)
                self.grid.place_agent(metal, (x, 0))
                metal = Metal(self.next_id(), self)
                self.grid.place_agent(metal, (x, self.grid.height - 1))

            for y in range(1,self.grid.height-1):
                metal = Metal(self.next_id(), self)
                self.grid.place_agent(metal, (self.grid.width - 1, y))
                metal = Metal(self.next_id(), self)
                self.grid.place_agent(metal, (0, y))



        def crea_paredes_internas_y_caminos(self):

            flag_salida = False
            posiciones_camino = []


            """Crea las paredes internas y los caminos"""
            for x in range(1, self.grid.width - 1):
                for y in range(1, self.grid.height - 1):
                    """Si x y y son pares, entonces se coloca una pared, Si x y y son impares, entonces se coloca un camino"""
                    if x % 2 == 0 and y % 2 == 0:
                        metal = Metal(self.next_id(), self)
                        self.grid.place_agent(metal, (x, y))
                    else:
                        camino = Camino(self.next_id(), self)
                        self.grid.place_agent(camino, (x, y))
                        posiciones_camino.append((x,y))

            #Se hace un for para colocar las rocas

            for i in range(self.numero_rocas):
                pos = random.choice(posiciones_camino)
                roca = Roca(self.next_id(), self)
                cell = self.grid.get_cell_list_contents(pos)
                self.grid.remove_agent(cell[0])
                self.grid.place_agent(roca, pos)
                posiciones_camino.remove(pos)

            #Se crea una salida
            pos= random.choice(posiciones_camino)
            salida = Salida(self.next_id(), self)
            cell = self.grid.get_cell_list_contents(pos)
            self.grid.remove_agent(cell[0])
            self.grid.place_agent(salida, pos)
            posiciones_camino.remove(pos)

            self.inicio = random.choice(posiciones_camino)
            self.salida = pos

            self.caminos = posiciones_camino



        

        def coloca_salida(self):
            """Coloca la salida"""
            salida = Salida(self.next_id(), self)
            self.grid.place_agent(salida, self.salida)

        crea_paredes_externas(self)
        crea_paredes_internas_y_caminos(self)
        coloca_salida(self)


    

    def crea_mundo_carga(self, archivo):
        """Crea el mundo a partir de un archivo"""
        pass


    """★★★★★★★★★★★★★★★★★★★★Metodos de busqueda★★★★★★★★★★★★★★★★★★★★★★★★★★★★★"""

    """★★BFS★★"""
    def busqueda_anchura(self, start, end):
        """
        Perform a breadth-first search (BFS) from the start node to the end node.
        Args:
            start (tuple): The starting node coordinates.
            end (tuple): The target node coordinates.
        Returns:
            dict: A dictionary where keys are levels (int) and values are lists of nodes (tuples) at that level.
              If the end node is found, the dictionary up to that level is returned.
              If the end node is not found, an empty dictionary is returned.
        Notes:
            - The search is performed on a grid where each node can have neighbors.
            - The neighbors are determined using the Moore neighborhood (excluding the center).
            - The search distinguishes between different types of cells (Salida and Camino).
            - If a Salida cell is found, the search stops and the current level dictionary is returned.
            - If a Camino cell is found, it is added to the queue for further exploration.
        """
        queue = deque()
        visited = {}
        level_dict = {}
        level = 0
        queue.append((start, level))
        visited[start] = level
        level_dict[level] = [start]
        
        while queue:
            current, level = queue.popleft()
            if current == end:
                break
            next_level = level + 1
            for neighbor in self.grid.get_neighborhood(current, moore=False, include_center=False):
                if neighbor not in visited:
                    cell = self.grid.get_cell_list_contents(neighbor)
                    if cell:
                        if type(cell[0]) is Salida:
                            visited[neighbor] = next_level
                            if next_level not in level_dict:
                                level_dict[next_level] = []
                            level_dict[next_level].append(neighbor)
                            #print(level_dict)
                            return level_dict

                        elif type(cell[0]) is Camino :
                            visited[neighbor] = next_level
                            queue.append((neighbor, next_level))
                            if next_level not in level_dict:
                                level_dict[next_level] = []
                            level_dict[next_level].append(neighbor)

                        #Si el vecino es la salida, se agrega al diccionario de visitados y se rompe el ciclo

        
        #print("No existe camino")
       #print(level_dict)
        return {}
    

    def get_road_breadth(self, start, end):
        """
        Obtains the path from the start to the end using breadth-first search and backtracking, and prints it, including the end. 
        It also checks if the search did not return empty.
        Args:
            start (tuple): The starting coordinates of the path.
            end (tuple): The ending coordinates of the path.
        Returns:
            list: A list of coordinates representing the path from start to end. 
                  Returns an empty list if no path is found.
        """

        level_dict = self.camino_busqueda

        #Si el diccionario de caminos esta vacio, es decir que es {}, se retorna un camino vacio
        if level_dict == {}:
            return []
        

        
        path = []
        path.append(end)
        current = end
        level = level_dict[max(level_dict.keys())]
        #print(level)
        for i in range(max(level_dict.keys()), 0, -1):
            for neighbor in self.grid.get_neighborhood(current, moore=False, include_center=False):
                if neighbor in level_dict[i-1]:
                    path.append(neighbor)
                    current = neighbor
                    break
        #print("Camino")
        #print(path)
        return path
    
    """★★DFS★★"""
    def busqueda_profundidad(self, start, end):
        """
        Perform a depth-first search (DFS) from the start node to the end node.
        Args:
            start (tuple): The starting node coordinates.
            end (tuple): The target node coordinates.
        Returns:
            dict: A dictionary where keys are levels (int) and values are lists of nodes (tuples) at that level.
              If the end node is found, the dictionary up to that level is returned.
              If the end node is not found, an empty dictionary is returned.
        Notes:
            - The search is performed on a grid where each node can have neighbors.
            - The neighbors are determined using the Moore neighborhood (excluding the center).
            - The search distinguishes between different types of cells (Salida and Camino).
            - If a Salida cell is found, the search stops and the current level dictionary is returned.
            - If a Camino cell is found, it is added to the queue for further exploration.
        """
        
        """Hace una busque por profundidad revisando cuando llega a la salida, usando una pila para poder guardar los datos"""
        stack = []
        visited = {}
        level_dict = {}
        level = 0
        stack.append((start, level))
        visited[start] = level
        level_dict[level] = [start]

        while stack:
            current, level = stack.pop()
            if current == end:
                break
            next_level = level + 1
            for neighbor in self.grid.get_neighborhood(current, moore=False, include_center=False):
                if neighbor not in visited:
                    cell = self.grid.get_cell_list_contents(neighbor)
                    if cell:
                        if type(cell[0]) is Salida:
                            visited[neighbor] = next_level
                            if next_level not in level_dict:
                                level_dict[next_level] = []
                            level_dict[next_level].append(neighbor)
                            return level_dict

                        elif type(cell[0]) is Camino :
                            visited[neighbor] = next_level
                            stack.append((neighbor, next_level))
                            if next_level not in level_dict:
                                level_dict[next_level] = []
                            level_dict[next_level].append(neighbor)
        return {}
    
    def get_road_depth(self, start, end):

        """
        Obtains the path from the start to the end using depth-first search and backtracking, and prints it, including the end. 
        It also checks if the search did not return empty.
        Args:
            start (tuple): The starting coordinates of the path.
            end (tuple): The ending coordinates of the path.
        Returns:
            list: A list of coordinates representing the path from start to end. 
                  Returns an empty list if no path is found.
        """
        level_dict = self.camino_busqueda
        if level_dict == {}:
            return []
        path = []
        path.append(end)
        current = end
        level = level_dict[max(level_dict.keys())]
        for i in range(max(level_dict.keys()), 0, -1):
            for neighbor in self.grid.get_neighborhood(current, moore=False, include_center=False):
                if neighbor in level_dict[i-1]:
                    path.append(neighbor)
                    current = neighbor
                    break
        return path
    
    """★★Busqueda de costo uniforme★★"""
    
    def busqueda_costo_uniforme(self, start, end):
    #Se hace uso de la busqueda por costo uniforme(Uniform Cost Search ) para encontrar el camino del inicio al fin
        """
        Perform a uniform cost search (UCS) from the start node to the end node.
        Args:
            start (tuple): The starting node coordinates.
            end (tuple): The target node coordinates.
        Returns:

            dict: A dictionary where keys are levels (int) and values are lists of nodes (tuples) at that level.
                If the end node is found, the dictionary up to that level is returned.
                If the end node is not found, an empty dictionary is returned.
        Notes:

            - The search is performed on a grid where each node can have neighbors.
            - The neighbors are determined using the Moore neighborhood (excluding the center).
            - The search distinguishes between different types of cells (Salida and Camino).
            - If a Salida cell is found, the search stops and the current level dictionary is returned.
            - If a Camino cell is found, it is added to the queue for further exploration.
        """


        #Se crea una cola de prioridad
        queue = PriorityQueue()
        #Se crea un diccionario de visitados
        visited = {}
        #Se crea un diccionario de niveles
        level_dict = {}
        #Se crea un nivel
        level = 0
        #Se agrega el inicio a la cola de prioridad
        queue.put((0, start, level))
        #Se agrega el inicio a los visitados
        visited[start] = level
        #Se agrega el inicio al diccionario de niveles
        level_dict[level] = [start]
        #Mientras la cola de prioridad no este vacia

        while not queue.empty():
            #Se obtiene el nodo actual
            current_cost, current, level = queue.get()
            #Si el nodo actual es igual al nodo final, entonces se rompe el ciclo
            if current == end:
                break
            #Se incrementa el nivel
            next_level = level + 1
            #Se obtiene los vecinos del nodo actual
            for neighbor in self.grid.get_neighborhood(current, moore=False, include_center=False):
                #Si el vecino no esta en los visitados
                if neighbor not in visited:
                    #Se obtiene el contenido de la celda
                    cell = self.grid.get_cell_list_contents(neighbor)
                    #Si la celda no esta vacia
                    if cell:
                        #Si la celda es una salida
                        if type(cell[0]) is Salida:
                            #Se agrega al visitado
                            visited[neighbor] = next_level
                            #Si el nivel no esta en el diccionario de niveles, se agrega
                            if next_level not in level_dict:
                                level_dict[next_level] = []
                            #Se agrega al diccionario de niveles
                            level_dict[next_level].append(neighbor)
                            #Se retorna el diccionario de niveles
                            return level_dict
                        #Si la celda es un camino
                        elif type(cell[0]) is Camino :
                            #Se agrega al visitado
                            visited[neighbor] = next_level
                            #Se agrega a la cola de prioridad
                            queue.put((next_level, neighbor, next_level))
                            #Si el nivel no esta en el diccionario de niveles, se agrega
                            if next_level not in level_dict:
                                level_dict[next_level] = []
                            #Se agrega al diccionario de niveles
                            level_dict[next_level].append(neighbor)

        return {}
    
    def get_road_uniform(self, start, end):
        """
        Obtains the path from the start to the end using uniform cost search and backtracking, and prints it, including the end. 
        It also checks if the search did not return empty.
        Args:
            start (tuple): The starting coordinates of the path.
            end (tuple): The ending coordinates of the path.
        Returns:
            list: A list of coordinates representing the path from start to end. 
                  Returns an empty list if no path is found.
        """
        level_dict = self.camino_busqueda
        if level_dict == {}:
            return []
        path = []
        path.append(end)
        current = end
        level = level_dict[max(level_dict.keys())]
        for i in range(max(level_dict.keys()), 0, -1):
            for neighbor in self.grid.get_neighborhood(current, moore=False, include_center=False):
                if neighbor in level_dict[i-1]:
                    path.append(neighbor)
                    current = neighbor
                    break
        return path
    
     

            



    def imprime_mundo_en_matriz(self):
        """
        Prints the world grid in a matrix format.
        This method prints the coordinates of each cell in the grid for testing purposes,
        followed by a representation of the world where:
        - 'R' represents a Roca object.
        - 'C' represents a Camino object.
        - 'M' represents a Metal object.
        - 'E' represents a Salida object.
        - 'X' represents an empty cell.
        Note: This method is intended for testing ENSERIO BORRAR LUEGO DE PROBAR QUE FUNCIONA
        """

        for x in range(self.grid.width):
            for y in range(self.grid.height):
                    print('['+str(x)+','+str(y)+']', end="")
            print()

        print("-----------------------Imprimiendo mundo")
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                cell = self.grid.get_cell_list_contents((x, y))
                if cell:
                    if type(cell[0]) is Roca:
                        print('R', end="")
                    elif type(cell[0]) is Camino:
                        print('C', end="")
                    elif type(cell[0]) is Metal:
                        print('M', end="")
                    elif type(cell[0]) is Salida:
                        print('E', end="")
                else:
                    print("X", end="")
            print()


    def get_dicc_path(self):
        #Si bomberman ya se puede mover, entonces devuelve un diccionario vacio
        if self.bomberman_mueve is True:
            return {}
        else:
            #Si self.camino_busqueda es un diccionario vacio, entonces se retorna un diccionario vacio
            if not self.camino_busqueda :
                return {}

            diccionario=self.camino_busqueda

        #Devuelve un pedazo del diccionario de caminos, desde el nivel 0 hasta el nivel maximo
            dicc = {}
            for i in range(self.nivel_maximo+1):
                dicc[i] = diccionario[i]
        return dicc
    
    def step(self):


        self.schedule.step()
        if self.bomberman_mueve is False:
            self.nivel_maximo = self.nivel_maximo+1
            #Si el nuvel maximo alcanza el tamanio de la lista de caminos, entonces se puede mover el bomberman
            if self.nivel_maximo == len(self.camino_busqueda):
                self.bomberman_mueve = True
                #Le da a bomberman el vector de caminos en reversa
                self.personaje.movimientos = self.caminos[::-1]

                self.personaje.mov=True
                

        else:
            pass



        
        


        
    def get_exit_position(self):
        return self.salida







