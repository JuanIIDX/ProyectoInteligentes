from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import SimultaneousActivation
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
import random
from queue import PriorityQueue
import mesa

from GameModel import GameModel
from BombermanAgent import BombermanAgent
from GloboAgent import GloboAgent
from GameModel import Roca, Camino, Metal, Salida

WIDTH = 30
HEIGHT = 30

simulation_parameters = {
    "modo_busqueda": mesa.visualization.Slider(name="1-Anchura 2-Profundidad 3-Busqueda Uniforme", value=0,min_value=0, max_value=2, step=1, description="Modo de busqueda"),
    "modo_aleatorio": mesa.visualization.Slider(name="0-Aleatorio 1-Carga Archivo", value=0,min_value=0, max_value=1, step=1, description="Modo aleatorio de creacion de mundo"),
"width": WIDTH,
"height": HEIGHT,
"num_globos": 0,
"numero_rocas": mesa.visualization.Slider(name="Probabilidad de roca", value=10, min_value=1, max_value=200, step=1, description="Probabilidad de rocas en modo aleatorio"),
                            
    
}


    
def dibuja_bomberman(agent):
   
    #Se consigue la direccion del agente

    direction=agent.model.personaje.direction

    if direction == 2:
        return {"Shape": "images/S.png",  "Layer": 0, "w": 1, "h": 1}
    elif direction == 4:
        return {"Shape": "images/W.png",  "Layer": 0, "w": 1, "h": 1}
    elif direction == 6:
        return {"Shape": "images/E.png",  "Layer": 0, "w": 1, "h": 1}
    elif direction == 8:
        return {"Shape": "images/N.png",  "Layer": 0, "w": 1, "h": 1}
    elif direction == 5:
        #Se obtiene el numero del step en el modelo y se imprime

        #El numero del step actual es
        


        animacion=agent.model.schedule.steps%2
        if animacion==0:
            return {"Shape": "images/V_B.png",  "Layer": 0, "w": 1, "h": 1}
        else:
            return {"Shape": "images/V_A.png",  "Layer": 0, "w": 1, "h": 1}

    




def bomberman_visualization(agent):
    if agent is None:
        return
    else:
        # Si el agente es un bomberman, se dibuja con un circulo azul
        if isinstance(agent, BombermanAgent):
            portrayal = dibuja_bomberman(agent)
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
            camino_bomberman=agent.model.personaje.movimientos

            if camino_bomberman is []:
                return {"Shape": "rect", "Filled": "true", "Color": "Red", "Layer": 0, "w": 1, "h": 1}

            for pos in range(len(camino_bomberman)):
                if agent.pos == camino_bomberman[pos]:
                    return {"Shape": "rect", "Filled": "true", "Color": "purple", "Layer": 0, "w": 1, "h": 1,"text":str(pos),"text_color": "black"}
                
            return {"Shape": "rect", "Filled": "true", "Color": "white", "Layer": 0, "w": 1, "h": 1}


#Cambiar luego
def dibujo_salida(agent):

        return {"Shape": "rect", "Filled": "true", "Color": "yellow", "Layer": 0, "w": 1, "h": 1}







# Configurar la visualización
def lanzar_simulacion(algoritmo_busqueda):


    grid = CanvasGrid(bomberman_visualization, WIDTH, HEIGHT, 1000, 1000)
    server = ModularServer(model_cls=GameModel, visualization_elements=[grid], name="Bomberman", model_params=simulation_parameters
                           )
    server.port = 8521  # El puerto donde se verá en el navegador
    server.launch()

# Llama a esta función para lanzar la simulación con el algoritmo seleccionado
if __name__ == '__main__':
    # Cambia "Anchura", "Profundidad", o "Costo Uniforme" según el algoritmo que desees usar
    lanzar_simulacion("Anchura")