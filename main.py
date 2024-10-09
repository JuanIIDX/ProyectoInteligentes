from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import SimultaneousActivation
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
import random
from queue import PriorityQueue

from GameModel import GameModel
from BombermanAgent import BombermanAgent
from GloboAgent import GloboAgent
from GameModel import Roca, Camino, Metal, Salida

WIDTH = 10
HEIGHT = 10


# Función para representar gráficamente el entorno con circulos dentro del CanvasGrid
#AGREGAR LUEGO EL GLOBO
def agent_portrayal(agent):
    """ Dibuja los agentes y el laberinto. """
    if isinstance(agent, BombermanAgent):
        return {"Shape": "circle", "Filled": "true", "Color": "blue", "Layer": 0, "r": 0.8}
    else:
        #Se obtiene el tipo de objeto del agente para dibujarlo en la matriz, si es roca, camino, metal o salida
        if isinstance(agent, Roca):
            return {"Shape": "rect", "Filled": "true", "Color": "black", "Layer": 0, "w": 1, "h": 1}
        elif isinstance(agent, Camino):
            return {"Shape": "rect", "Filled": "true", "Color": "white", "Layer": 0, "w": 1, "h": 1}
        elif isinstance(agent, Metal):
            return {"Shape": "rect", "Filled": "true", "Color": "gray", "Layer": 0, "w": 1, "h": 1}
        elif isinstance(agent, Salida):
            return {"Shape": "rect", "Filled": "true", "Color": "green", "Layer": 0, "w": 1, "h": 1}
        
        return None




def bomberman_visualization(agent):
    if agent is None:
        return
    else:
        # Si el agente es un bomberman, se dibuja con un circulo azul
        if isinstance(agent, BombermanAgent):
            portrayal = {"Shape": "circle", "Filled": "true", "Color": "blue", "Layer": 0, "r": 0.8}
        # Si el agente es un globo, se dibuja con un circulo rojo
        elif isinstance(agent, GloboAgent):
            portrayal = {"Shape": "circle", "Filled": "true", "Color": "red", "Layer": 0, "r": 0.8}
        # Si el agente es una roca, se dibuja con un cuadrado
        elif isinstance(agent, Roca):
            portrayal = {"Shape": "rect", "Filled": "true", "Color": "black", "Layer": 0, "w": 1, "h": 1}
        # Si el agente es un camino, se dibuja con un cuadrado
        elif isinstance(agent, Camino):
            portrayal = dibujo_camino(agent)
        # Si el agente es un metal, se dibuja con un cuadrado
        elif isinstance(agent, Metal):
            portrayal = {"Shape": "rect", "Filled": "true", "Color": "gray", "Layer": 0, "w": 1, "h": 1}
        # Si el agente es una salida, se dibuja con un cuadrado
        elif isinstance(agent, Salida):
            portrayal = dibujo_salida(agent)
        
    return portrayal

#Cambiar luego
def dibujo_camino(agent):
        
        #Si el bomberman no se mueve, se muestran todos los caminos posibles
        if agent.model.bomberman_mueve == False:
            posiciones_dict = agent.model.get_dicc_path()

            if not posiciones_dict :
                return {"Shape": "rect", "Filled": "true", "Color": "Red", "Layer": 0, "w": 1, "h": 1}

            # Iterar sobre el diccionario y dibujar los números
            for level, positions in posiciones_dict.items():
                for pos in positions:
                    if agent.pos == pos:
                        return {"Shape": "rect","Color": "green","Filled": "true","Layer": 0,"w": 1,"h": 1,"text": str(level),"text_color": "black"}
                    
            return {"Shape": "rect", "Filled": "true", "Color": "white", "Layer": 0, "w": 1, "h": 1}
        
        #Si el bomberman se mueve, se muestran los caminos que se pueden recorrer
        else:
            camino_bomberman=agent.model.caminos

            if camino_bomberman is []:
                return {"Shape": "rect", "Filled": "true", "Color": "Red", "Layer": 0, "w": 1, "h": 1}

            for camino in camino_bomberman:
                if agent.pos == camino:
                    return {"Shape": "rect", "Filled": "true", "Color": "purple", "Layer": 0, "w": 1, "h": 1}
                
            return {"Shape": "rect", "Filled": "true", "Color": "white", "Layer": 0, "w": 1, "h": 1}


#Cambiar luego
def dibujo_salida(agent):

        return {"Shape": "rect", "Filled": "true", "Color": "yellow", "Layer": 0, "w": 1, "h": 1}



        

        

        
    
        
    
    




# Configurar la visualización
def lanzar_simulacion(algoritmo_busqueda):


    grid = CanvasGrid(bomberman_visualization, WIDTH, HEIGHT, 1000, 1000)
    server = ModularServer(GameModel, [grid], "Bomberman", 
                           {"width": WIDTH, "height": HEIGHT, "num_globos": 0, 
                            "algoritmo_busqueda": algoritmo_busqueda})
    server.port = 8521  # El puerto donde se verá en el navegador
    server.launch()

# Llama a esta función para lanzar la simulación con el algoritmo seleccionado
if __name__ == '__main__':
    # Cambia "Anchura", "Profundidad", o "Costo Uniforme" según el algoritmo que desees usar
    lanzar_simulacion("Anchura")