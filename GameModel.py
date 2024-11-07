from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import SimultaneousActivation
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
import random
from queue import PriorityQueue
from BombermanAgent import BombermanAgent, CustomAgent
from collections import deque
import os
from clases import Roca, Camino, Metal, Salida
from busquedas import Busquedas



# Modelo del juego
class GameModel(Model):
    def __init__(self, width, height, num_globos, modo_busqueda,modo_aleatorio, numero_rocas, visualizar_camino):
        super().__init__()

        # Se crea la grilla y el schedule
        self.grid = MultiGrid(width, height, True) #Se crear una grilla de tamaño width x height(Poner aleatorio luego)
        self.schedule = SimultaneousActivation(self) #Se crea un schedule para los agentes
        
        # Se crear una posicion de salida que no este en un x,y par ni en las paredes
        self.inicio= (0,0)
        self.salida = (0,0)
        self.tipo_busqueda = 'X'
        self.numero_rocas = numero_rocas






        #Se crea el mundo
        self.crea_mundo(modo_aleatorio)

        # Se crea el agente Bomberman con la posicion de inicio
        self.personaje = BombermanAgent(1, self)
        self.grid.place_agent(self.personaje, self.inicio)
        self.schedule.add(self.personaje)

        self.personaje.selecciona_modo_busqueda(modo_busqueda, self.inicio, self.salida, self.grid)
        self.personaje.camino_busqueda(self.inicio,self.salida, self.grid)

        print("Arbol")
        print(self.personaje.arbol_movimientos)
        print("Movimientos")
        print(self.personaje.movimientos)



        #Se establecen las variables booleanas para saber si el bomberman se puede mover o no
        self.bomberman_mueve = False
        self.muestra_camino = False
        self.nivel_maximo = 0
        self.state = "Estado Inicial"

        





        print("Inicio: ", self.inicio)
        print("Salida: ", self.salida)

        """ self.imprime_mundo_en_matriz() """
       

        # Añadir globos (enemigos) en posiciones aleatorias
        # POR EL MOMENTO NO SE ACTIVAN

        #Contadores
        self.contador_niveles = 0

        if visualizar_camino is False:
            self.personaje.can_mov = True 
            self.contador_niveles = sum(len(vector) for vector in self.personaje.arbol_movimientos.values())















    def crea_mundo(self,modo_aleatorio):
        """Crea el mundo"""
        """Modo de carga---Se crea el escenario"""

        #Si el modo de carga es 0, entonces se crea el mundo de forma aleatorio
        if modo_aleatorio == 0:
            print('Se activo la carga aleatoria')
            self.crea_mundo_aleatorio()

        #Si el modo de carga es 1, entonces se crea el mundo a partir de un archivo
        else:
            print('Se activo la carga por un archivo')
            self.leer_mapa('archivo.txt') 



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

            #Coloca una roca en la salida
            roca = Roca(self.next_id(), self)
            self.grid.place_agent(roca, pos)



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

    def leer_mapa(self,ruta_relativa):
        try:
            # Obtener la ruta absoluta del archivo
            ruta_absoluta = os.path.join(os.getcwd(), ruta_relativa)
            
            # Verifica si el archivo existe
            if not os.path.isfile(ruta_absoluta):
                raise FileNotFoundError(f"El archivo '{ruta_relativa}' no se encontró en el proyecto.")
            
            with open(ruta_absoluta, 'r') as f:
                posiciones_camino = []
                # Lee el archivo y guarda cada línea en una lista
                for y, line in enumerate(f):
                    for x, char in enumerate(line.strip()):
                        print(f"({x}, {y}): {char}")

                        if char == 'R':
                            roca = Roca(self.next_id(), self)
                            self.grid.place_agent(roca, (x, y))
                        elif char == 'C':
                            camino = Camino(self.next_id(), self)
                            self.grid.place_agent(camino, (x, y))
                            posiciones_camino.append((x, y))
                        elif char == 'M':
                            metal = Metal(self.next_id(), self)
                            self.grid.place_agent(metal, (x, y))
                        elif char == 'E':
                            salida = Salida(self.next_id(), self)
                            self.grid.place_agent(salida, (x, y))
                            self.salida = (x, y)
                        elif char == 'P':
                            self.inicio = (x, y)
                        else:
                            raise MapaError(f"Carácter no válido en la posición ({x}, {y}): '{char}'")
                        


                self.caminos = posiciones_camino
                

            


        except FileNotFoundError as e:
            print(e)
        except MapaError as e:
            print(f"Error en el mapa: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")


    

 





















     

            



    def imprime_mundo_en_matriz(self):
        
        print("-----------------------Imprimiendo mundo invertido")

        #Empieza de abajo a arriba en x

        for y in range(self.grid.height-1,-1,-1):
            for x in range(self.grid.width):
                cell = self.grid.get_cell_list_contents((x, y))
                if cell:
                    if type(cell[0]) is Salida:
                        if type(cell[1]) is Roca:
                            print('✵', end="")
                        else:
                            print('E', end="")
                        
                    elif type(cell[0]) is BombermanAgent:
                        print('✵', end="")
                    elif type(cell[0]) is Roca:
                        print('X', end="")
                    elif type(cell[0]) is Camino:
                        print('◇', end="")
                    elif type(cell[0]) is Metal:
                        print('◆', end="")

                    
                else:
                    print("X", end="")
            print()

        print('fin')
        

       



    def get_camino_busqueda(self):
        #Retorna el diccionario de camino de busqueda desde 0 hasta el contador de niveles, si llego al final, entonces retorna el camino completo

        diccionario={}

        #Si el contador llega a la longitud maxima de la mayor llave de camino busqueda, 
        #entonces se retorna el camino completo, se usa un metodo de diccionario para saber la llave maxima
        if self.personaje.arbol_movimientos:
            #Obtiene el numero total de todos los elementos en cada nivel del diccionario

            contador=0

            for nivel in self.personaje.arbol_movimientos.values():
                for pos in nivel:
                    # Mostramos el elemento
                    diccionario[contador] = [pos]
                    contador += 1
                    # Detenemos el bucle si alcanzamos el número de iteraciones deseadas
                    if contador > self.contador_niveles:
                        break
                if contador > self.contador_niveles:
                    break

            print(diccionario)
            return diccionario

        else:
            return diccionario
       
        


        
    def get_exit_position(self):
        return self.salida
    


    def step(self):
        self.schedule.step()

        self.contador_niveles += 1
        if self.personaje.arbol_movimientos and self.contador_niveles >= sum(len(vector) for vector in self.personaje.arbol_movimientos.values()):
            self.personaje.can_mov = True
        
        #if not self.personaje.can_mov:
        #    print(self.get_camino_busqueda())
        #else:
        #    print(self.personaje.movimientos)





        
    

    