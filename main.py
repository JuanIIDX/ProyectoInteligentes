from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import SimultaneousActivation
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
import random
from queue import PriorityQueue
import mesa

from GameModel import GameModel
from BombermanAgent import BombermanAgent, Bomba
from GloboAgent import GloboAgent
from GameModel import Roca, Camino, Metal, Salida

WIDTH = 20
HEIGHT = 20

simulation_parameters = {
    "modo_busqueda": mesa.visualization.Slider(name="0-Anch 1-Prof 2-Unifor 3-Beam Search 4-Hill Climbing 5-A*", value=0,min_value=0, max_value=5, step=1, description="Modo de busqueda"),
    "modo_aleatorio": mesa.visualization.Slider(name="0-Aleatorio 1-Carga Archivo", value=0,min_value=0, max_value=1, step=1, description="Modo aleatorio de creacion de mundo"),
"width": WIDTH,
"height": HEIGHT,
"num_globos": 0,
"numero_rocas": mesa.visualization.Slider(name="Probabilidad de roca", value=5, min_value=1, max_value=200, step=1, description="Probabilidad de rocas en modo aleatorio"),
"visualizar_camino": mesa.visualization.Checkbox(name="Visualizar camino", value=False, description="Visualizar camino de busqueda"),                     
    
}


    
def dibuja_bomberman(agent):
   
    #Se consigue la direccion del agente

    direction=agent.model.personaje.direction

    if agent.model.personaje.victoria is False:
        if direction == 2:
            return {"Shape": "images/S.png",  "Layer": 0, "w": 1, "h": 1}
        elif direction == 4:
            return {"Shape": "images/W.png",  "Layer": 0, "w": 1, "h": 1}
        elif direction == 6:
            return {"Shape": "images/E.png",  "Layer": 0, "w": 1, "h": 1}
        elif direction == 8:
            return {"Shape": "images/N.png",  "Layer": 0, "w": 1, "h": 1}


    if agent.model.personaje.victoria is True:
        animacion=agent.model.schedule.steps%2
        if animacion==0:
            return {"Shape": "images/V_B.png",  "Layer": 0, "w": 1, "h": 1}
        else:
            return {"Shape": "images/V_A.png",  "Layer": 0, "w": 1, "h": 1}

def bomberman_visualization(agent):
    if agent is None:
        return
    elif isinstance(agent, Bomba):
        if agent.en_explosion:
            return {"Shape": "rect", "Filled": "true", "Color": "orange", "Layer": 0, "w": 1, "h": 1}
        else:
            return {"Shape": "circle", "Filled": "true", "Color": "black", "Layer": 0, "r": 0.5}

    elif isinstance(agent, BombermanAgent):
        return dibuja_bomberman(agent)
    elif isinstance(agent, GloboAgent):
        return {"Shape": "circle", "Filled": "true", "Color": "red", "Layer": 0, "r": 0.8}
    elif isinstance(agent, Roca):
        return {"Shape": "rect", "Filled": "true", "Color": "black", "Layer": 0, "w": 1, "h": 1}
    elif isinstance(agent, Camino):
        return dibujo_camino(agent)
    elif isinstance(agent, Metal):
        return {"Shape": "rect", "Filled": "true", "Color": "gray", "Layer": 0, "w": 1, "h": 1}
    elif isinstance(agent, Salida):
        return dibujo_salida(agent)
    elif isinstance(agent, GloboAgent):
        return {"Shape": "circle", "Filled": "true", "Color": "red", "Layer": 0, "r": 0.8}


#Cambiar luego
def dibujo_camino(agent):
    if agent.model.game_over is True:
        return {"Shape": "rect", "Filled": "true", "Color": "Red", "Layer": 0, "w": 1, "h": 1 }




    if agent.model.personaje.can_mov == False and (agent.model.victoria is False and agent.model.game_over is False):

        if agent.model.personaje.bomba_activa:
            if agent.pos == agent.model.personaje.bomba.pos:
                return {"Shape": "circle", "Filled": "true", "Color": "blue", "Layer": 0, "w": 1, "h": 1}
            

                

        posiciones_dict=agent.model.get_camino_busqueda()

        if not posiciones_dict:
            return {"Shape": "rect", "Filled": "true", "Color": "Red", "Layer": 0, "w": 1, "h": 1}
        
        # Iterar sobre el diccionario y dibujar los números
        for level, positions in posiciones_dict.items():
            for pos in positions:
                if agent.pos == pos:
                    return {"Shape": "rect","Color": "green","Filled": "true","Layer": 0,"w": 1,"h": 1,"text": str(level),"text_color": "black"}
                
    else:
        camino_bomberman=agent.model.personaje.movimientos

        if agent.model.personaje.muestra_explosion:
            if agent.pos in agent.model.personaje.area_explosiones:
                return {"Shape": "rect", "Filled": "true", "Color": "orange", "Layer": 1, "w": 1, "h": 1}

        if camino_bomberman is []:
            return {"Shape": "rect", "Filled": "true", "Color": "Red", "Layer": 0, "w": 1, "h": 1}
        
        for pos in range(len(camino_bomberman)):
            if agent.pos == camino_bomberman[pos]:
                return {"Shape": "rect", "Filled": "true",  "Color": "purple" ,"Layer": 0, "w": 1, "h": 1,"text":str(pos),"text_color": "black"}
        pass
        return {"Shape": "rect", "Filled": "true", "Color": "white", "Layer": 0, "w": 1, "h": 1}


#Cambiar luego
def dibujo_salida(agent):

        for agent_aux in agent.model.grid.get_cell_list_contents(agent.pos):
            if isinstance(agent_aux, (Roca, GloboAgent)) and agent_aux.pos == agent.pos:
                return {"Shape": "rect", "Filled": "true", "Color": "black", "Layer": 0, "w": 1, "h": 1}
        return {"Shape": "rect", "Filled": "true", "Color": "green", "Layer": 0, "w": 1, "h": 1}







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