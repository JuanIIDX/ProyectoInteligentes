from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import SimultaneousActivation
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
import random
from queue import PriorityQueue

from clases import Camino

class GloboAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.can_move = False

    def step(self):
        if self.can_move is False:
            return
        # Verificar si la posición actual está definida
        if self.pos is not None:
            # Obtener movimientos posibles solo en celdas de tipo Camino
            possible_moves = self.get_possible_moves()
            if possible_moves:
                new_position = random.choice(possible_moves)
                self.model.grid.move_agent(self, new_position)

    def get_possible_moves(self):
        """Obtener las celdas adyacentes que son caminos para moverse"""
        if self.pos is None:
            return []

        neighbors = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
        possible_moves = []

        # Filtrar solo las celdas de camino
        for pos in neighbors:
            cell_contents = self.model.grid.get_cell_list_contents(pos)
            if all(isinstance(agent, Camino) for agent in cell_contents) or not cell_contents:
                possible_moves.append(pos)

        return possible_moves