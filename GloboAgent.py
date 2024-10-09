from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import SimultaneousActivation
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
import random
from queue import PriorityQueue

# Definir el agente enemigo (Globo)
class GloboAgent(Agent):
# Agente Bomberman
    def __init__(self, unique_id, model, pos_ini):
        super().__init__(unique_id, model)
        self.camino_recorrido = []  # Guardar el camino recorrido
        self.posicion_actual = (0, 0)  # Posición inicial
        
    def step(self):
        print("Se movio un paso adelante")
        pass
