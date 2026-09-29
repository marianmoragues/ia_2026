""" Fitxer que conté els diferents agents aspiradors.

Percepcions:
    "Loc": [0]
    "Net": [1]

Accions:
    AccionsAspirador.DRETA
    AccionsAspirador.ESQUERRA
    AccionsAspirador.ATURA
    AccionsAspirador.ASPIRA

Autor: Miquel Miró Nicolau (UIB), 2022
"""
import abc
from importlib.resources import files

import pygame

from iaLib import agent


class Aspirador(agent.Agent):
    def __init__(self):
        super().__init__(long_memoria=1)

    def pinta(self, display):
        img_path = files("aspirador.images") / "sprite.png"

        img = pygame.image.load(img_path)
        img = pygame.transform.scale(img, (100, 100))
        display.blit(img, self._posicio_pintar)

    @abc.abstractmethod
    def actua(self, percepcio):
        pass


class AspiradorTaula(Aspirador):
    TAULA = {
        (0, True): "D",
        (0, False): "A",
        (1, True): "E",
        (1, False): "A",
    }

    def actua(self, percepcio: dict):
        return AspiradorTaula.TAULA[
            (percepcio["Loc"], percepcio["Net"])
        ]

#  Agent reflex simple: actua nom´es en funci´o de l’estat actual percebut (si la sala est`a bruta, neteja; si est`a neta, es mou).
class AspiradorReflex(Aspirador):
    def actua(self, percepcio: dict):
        if not percepcio["Net"]:    # Si l'habitació on es troba és bruta, netejar-la
            return "A"
        else:
            if percepcio["Loc"] == 0:
                return "D"
            else:
                return "E"

class AspiradorMemoria(Aspirador):
    def actua(self, percepcio: dict):
        # Inicialment no sabem com estan les habitacions
        habitacions = {0: None, 1: None}

        loc = percepcio["Loc"]
        net = percepcio["Net"]

        # Posició actual
        habitacions[loc] = net

        # Si la sala actual està bruta, s'ha d'aspirar
        if not net:
            habitacions[loc] = True
            return "A"
        
        # Si sabem que totes dues estan netes, ens aturam
        if habitacions[0] is True and habitacions[1] is True:
            return "ATURA"
        
        # Si la sala actual està neta però l'altra no o encara no la coneixem, ens movem
        if loc == 0:
            return "D"
        else:
            return "E"

