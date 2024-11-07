from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import SimultaneousActivation
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer



class MapaError(Exception):
    pass

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
