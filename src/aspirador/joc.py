from iaLib import agent, joc

class Aspirador(joc.JocNoGrafic):

    # Definir l'estat inicial del joc
    def __init__(self, agents: list[agent.Agent] | None = None):
        if agents is None:
            agents=[]
        super(Aspirador, self).__init__(agents=agents)
        self.habitacions = {"esquerra": "Neta", "dreta": "Bruta"}   # Representar les dues habitacions i indicar si cada habitació està neta o bruta
        self.posicio_aspirador = "dreta"    # Inicialitzar la posició de l'aspirador
    
    # Mostrar per pantalla l'estat actual del joc
    def _draw(self):
        # Indicar quina habitació conté l'aspirador
        if self.posicio_aspirador == "esquerra":
            print("L'aspirador es troba dins l'habitació esquerra")
        elif self.posicio_aspirador == "dreta":
            print("L'aspirador es troba dins l'habitació dreta")
        
        # Mostrar si cada habitació està neta o bruta
        for hab in self.habitacions:
            estat = self.habitacions[hab]
            print(f"L'habitació {hab} està {estat}.")

    # Retornar la informació que l'agent pot observar
    def percepcio(self):
        # Posició actual de l'aspirador
        pos_actual = self.posicio_aspirador

        # Estat (net/brut) de l'habitació on es troba
        estat_actual = self.habitacions[pos_actual]

        return (pos_actual, estat_actual)

    # Actualitzar l'estat del joc segons l'acció escollida per l'agent
    def _aplica(self, accio, params=None, agent_actual=None):
        # Acció de netejar: l'habitació actual passa a estar neta
        if accio == "Netejar":
            self.habitacions[self.posicio_aspirador] = "Neta"

        # Acció de moure's: l'aspirador canvia d'habitació
        elif accio == "Moure":
            if self.posicio_aspirador == "esquerra":
                self.posicio_aspirador = "dreta"
            else:
                self.posicio_aspirador = "esquerra"

        # Comprovar si ambdues habitacions estan netes (fi del joc)
        for hab, estat in self.habitacions.items():
            if estat == "Bruta":
                joc_acabat = False
            else:
                joc_acabat = True
        
        return joc_acabat
