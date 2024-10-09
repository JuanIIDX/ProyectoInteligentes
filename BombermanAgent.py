from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import SimultaneousActivation
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
import random
from queue import PriorityQueue


class BombermanAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.movimientos = []
        self.power = 1  # Poder inicial de destrucción
        
        self.pos_vec=0
        self.direction = 2  # Dirección en la que se mueve el agente

        self.mov=False
        self.victoria=False

    def step(self):
        if self.mov:

            if self.pos_vec<len(self.movimientos):
                #Calcula la direccion hacia donde se va a dirigir luego de obtener el siguiente movimiento, si es para abajo se asigna 2 a pos_vec, si es para arriba 8, si es para la derecha 4 y si es para la izquierda 6
                #Se calcula la direccion a partir de la primera posicion y la siguiente en el vector de movimientos
                if self.movimientos[self.pos_vec-1][0]==self.movimientos[self.pos_vec][0]:
                    if self.movimientos[self.pos_vec-1][1]>self.movimientos[self.pos_vec][1]:
                        self.direction=2
                    else:
                        self.direction=8
                else:
                    if self.movimientos[self.pos_vec-1][0]>self.movimientos[self.pos_vec][0]:
                        self.direction=4
                    else:
                        self.direction=6
                
                print('direccion:',self.direction)
                #Se mueve a la siguiente posicion en el vector de movimientos


                nuevo_movimiento=self.movimientos[self.pos_vec]
                self.model.grid.move_agent(self, nuevo_movimiento)
                #print(self.movimientos[self.pos_vec])
                self.pos_vec+=1
            
            else:
                self.victoria=True
                self.direction=5
                self.pos_vec+=1

        else:
            print("No se puede mover")


    def asigna_movimientos(self,camino):
        self.mov=True
        self.movimientos=camino
        nuevo_movimiento=self.movimientos[self.pos_vec]
        self.model.grid.move_agent(self, nuevo_movimiento)

        self.pos_vec+=1

        


