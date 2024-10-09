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
    def __init__(self, width, height, num_globos, algoritmo_busqueda):
        super().__init__()

        # Se crea la grilla y el schedule
        self.grid = MultiGrid(width, height, True) #Se crear una grilla de tamaño width x height(Poner aleatorio luego)
        self.schedule = SimultaneousActivation(self) #Se crea un schedule para los agentes
        
        # Se crear una posicion de salida que no este en un x,y par ni en las paredes
        self.inicio= (1,1)
        self.salida = ()
        self.tipo_busqueda = 'X'
        self.camino_busqueda = {}
        self.caminos = []
        
        #Se crea el mundo
        self.crea_mundo()
        self.inicio = random.choice(self.caminos)
        self.camino_busqueda=self.busqueda_anchura(self.inicio, self.salida)
        self.caminos=self.get_path(self.inicio, self.salida)

      
        

        
        # Se crea el agente Bomberman con la posicion de inicio
        self.personaje = BombermanAgent(1, self, algoritmo_busqueda)
        self.grid.place_agent(self.personaje, self.inicio)
        self.schedule.add(self.personaje)

        #Se establecen las variables booleanas para saber si el bomberman se puede mover o no
        self.bomberman_mueve = False
        self.muestra_camino = False
        self.nivel_maximo = 0



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
    
        
    
    def crea_mundo(self):


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

            #Se hace un for 10 veces recorriendo el vector de caminos y escogiendo en cada iteracion un elemento aleatorio

            for i in range(10):
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
            self.salida = pos

            self.caminos = posiciones_camino

            print("Salida-: ", self.salida)


        

        def coloca_salida(self):
            """Coloca la salida"""
            salida = Salida(self.next_id(), self)
            self.grid.place_agent(salida, self.salida)

        crea_paredes_externas(self)
        crea_paredes_internas_y_caminos(self)
        coloca_salida(self)

    def get_exit_position(self):
        return self.salida
    
    #Se hace un algoritmo de anchura que recorre el mundo por nivelees, y agregar en cada nivel los nodos pertenecientes
    #de la forma {0:[(1,1)], 1:[(2,1),(1,2)], 2:[(3,1),(2,2),(1,3)]} siempre que el nodo sea un camino

    def busqueda_anchura(self, start, end):
        """Busqueda en anchura"""
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
                            print(level_dict)
                            return level_dict

                        elif type(cell[0]) is Camino :
                            visited[neighbor] = next_level
                            queue.append((neighbor, next_level))
                            if next_level not in level_dict:
                                level_dict[next_level] = []
                            level_dict[next_level].append(neighbor)

                        #Si el vecino es la salida, se agrega al diccionario de visitados y se rompe el ciclo

        
        print("No existe camino")
        print(level_dict)
        return {}
    
    #Se hace un algoritmo que usa el algoritmo de anchura y saca un camino a partir de ese algortimo

    def get_path(self, start, end):
        """Obtiene el camino del inicio al fin a partir de la busqueda en anchura y por medio de backtracking, y lo imprime, incluyendo el final, tambien debe revisar si la busqueda no devolvio None"""
 

        level_dict = self.camino_busqueda

        #Si el diccionario de caminos esta vacio, es decir que es {}, se retorna un camino vacio
        if level_dict == {}:
            return []
        

        
        path = []
        path.append(end)
        current = end
        level = level_dict[max(level_dict.keys())]
        print(level)
        for i in range(max(level_dict.keys()), 0, -1):
            for neighbor in self.grid.get_neighborhood(current, moore=False, include_center=False):
                if neighbor in level_dict[i-1]:
                    path.append(neighbor)
                    current = neighbor
                    break
        print("Camino")
        print(path)
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

        print("datos--------------------------------------------------")
        print('bomberman_mueve', self.bomberman_mueve)
        print('nivel_maximo', self.nivel_maximo)
        print('caminos', self.caminos)
        print('camino_busqueda', self.camino_busqueda)







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



        
        


        








