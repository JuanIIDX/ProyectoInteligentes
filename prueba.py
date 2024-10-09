from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation

# Definimos el agente
class Personaje(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

# Definimos el modelo
class MiModelo(Model):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(width, height, torus=False)

        # Creamos los agentes y los ubicamos en la grilla
        for i in range(2):
            a = Personaje(i, self)
            self.schedule.add(a)
            # Colocamos a los agentes en posiciones aleatorias
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            self.grid.place_agent(a, (x, y))

        # Creamos algunos bloques
        for _ in range(10):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            self.grid.place_agent(Block(self.next_id(), self), (x, y))

    def step(self):
        self.schedule.step()
class Block(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

# Ejecutamos el modelo
model = MiModelo(20, 20)
for i in range(10):
    model.step()

