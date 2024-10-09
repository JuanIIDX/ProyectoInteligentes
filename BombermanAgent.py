from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import SimultaneousActivation
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
import random
from queue import PriorityQueue


class BombermanAgent(Agent):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)
        self.movimientos = []
        self.pos = pos
        self.power = 1  # Poder inicial de destrucción
        self.mov=False
        self.pos_vec=0

    def step(self):
        if self.mov:
            print(self.movimientos)

            if self.pos_vec<len(self.movimientos):
                nuevo_movimiento=self.movimientos[self.pos_vec]
                self.model.grid.move_agent(self, nuevo_movimiento)
                print(self.movimientos[self.pos_vec])
                self.pos_vec+=1
            """print(self.movimientos[self.pos_vec])
                self.pos_vec+=1
                
                new_position = (5,5)
                self.model.grid.move_agent(self, new_position) """
            print(self.movimientos)
            print("Se esta moviendo")
        else:
            print("No se puede mover")
        


